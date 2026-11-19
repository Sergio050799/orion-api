"""
Parser de los 2 .txt de corredores que vienen del Drive del jefe:
  - CORREDORES DE MEDIACIÓN.txt
  - CORREDORES DE TITAN.txt

Normaliza a CSV y hace upsert sobre tabla corredores de V5.

Patrón detectado del texto bruto:
  Línea 1: "Corredor dependiente de sucursal" / "Colaborador"
  Línea 2: código (CMxxx, CTxxx, AVxxx, OBSxxx, AGETxxx...)
  Línea 3: CIF o NIF
  Línea 4: " NOMBRE Oficina mediación" o " NOMBRE Titán"
  Línea 5: fecha alta (dd/mm/yyyy)
  Línea 6: opcional fecha baja

Uso:
  python scripts/parse_corredores_drive.py --input-med <ruta>.txt --input-tit <ruta>.txt --out <ruta>.csv
  python scripts/parse_corredores_drive.py --input-med X --input-tit Y --apply   # upsert BD V5
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')

CIF_RE = re.compile(r'^([ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]|\d{8}[A-HJ-NP-TV-Z]|[WY]\d{7}[A-Z])$')
FECHA_RE = re.compile(r'^\d{2}/\d{2}/\d{4}$')


def _limpiar(s: str) -> str:
    return s.strip().replace('\\&', '&').replace('\\_', '_').replace('\\`', '`').replace("\\'", "'")


def parse_txt(path: Path) -> list[dict]:
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Dividir por líneas y limpiar
    lineas = [_limpiar(l) for l in raw.split('\n')]
    lineas = [l for l in lineas if l]  # quitar vacías

    # Detectar sucursal desde cabecera
    sucursal_txt = ''
    if lineas and 'MEDIACI' in lineas[0].upper():
        sucursal_txt = 'MEDIACION'
    elif lineas and 'TITAN' in lineas[0].upper():
        sucursal_txt = 'TITAN'

    corredores = []
    i = 0
    n = len(lineas)
    while i < n:
        linea = lineas[i]

        # Buscar inicio de registro
        if linea in ('Corredor dependiente de sucursal', 'Colaborador'):
            tipo = linea
            codigo = cif = nombre = fecha_alta = ''

            # Las siguientes líneas útiles (código, cif, nombre, fecha)
            j = i + 1
            recogido = 0
            while j < n and recogido < 10:
                t = lineas[j]
                # Siguiente registro empieza
                if t in ('Corredor dependiente de sucursal', 'Colaborador'):
                    break
                # Códigos: pueden ser CM001, CT..., AV..., OBS..., AGET..., CC..., CE..., CN..., CS...
                if re.match(r'^(CM|CT|CE|CC|CN|CS|AV|AGE|AGET|OBS|CTC|CTL|CTM|CTN|CTS|CTB|CTCL)', t) and len(t) < 20 and not codigo:
                    codigo = t
                # CIF o NIF
                elif CIF_RE.match(t) and not cif:
                    cif = t
                # Fecha
                elif FECHA_RE.match(t) and not fecha_alta:
                    fecha_alta = t
                # Nombre: la línea que contiene "Oficina mediación" o "Titán" al final
                elif ('Oficina mediación' in t or 'Titán' in t) and not nombre:
                    n_tmp = t
                    for suf in (' Oficina mediación', ' Titán'):
                        if n_tmp.endswith(suf):
                            n_tmp = n_tmp[:-len(suf)]
                    nombre = n_tmp.strip()
                recogido += 1
                j += 1

            if codigo or nombre:
                corredores.append({
                    'codigo': codigo,
                    'cif': cif,
                    'nombre': nombre,
                    'sucursal': sucursal_txt,
                    'fecha_alta': fecha_alta,
                    'tipo': tipo,
                })
            i = j
        else:
            i += 1

    return corredores


def exportar_csv(corredores: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['codigo', 'cif', 'nombre', 'sucursal', 'fecha_alta', 'tipo'])
        w.writeheader()
        for c in corredores:
            w.writerow(c)
    print(f"[OK] CSV -> {out}  ({len(corredores)} corredores)")


def _uid() -> str:
    return f"corredor_{int(time.time()*1000)}_{os.urandom(3).hex()}"


def upsert_bd(conn: sqlite3.Connection, corredores: list[dict], dry: bool) -> dict:
    """Upsert por codigo. Si codigo ya existe -> update. Si no -> insert."""
    conn.row_factory = sqlite3.Row
    insertados = actualizados = sin_cambios = 0
    cur = conn.cursor()
    for c in corredores:
        if not c['codigo']:
            continue
        existente = cur.execute("SELECT id, nombre, cif, sucursal FROM corredores WHERE codigo = ?",
                                (c['codigo'],)).fetchone()
        if existente:
            # Update solo si algo cambió
            if (existente['nombre'] != c['nombre']
                    or (existente['cif'] or '') != c['cif']
                    or (existente['sucursal'] or '') != c['sucursal']):
                if not dry:
                    cur.execute("""
                        UPDATE corredores
                        SET nombre = ?, cif = ?, sucursal = ?, updated_at = datetime('now')
                        WHERE id = ?
                    """, (c['nombre'], c['cif'], c['sucursal'], existente['id']))
                actualizados += 1
            else:
                sin_cambios += 1
        else:
            if not dry:
                cur.execute("""
                    INSERT INTO corredores (id, codigo, nombre, cif, sucursal, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (_uid(), c['codigo'], c['nombre'], c['cif'], c['sucursal']))
            insertados += 1
    if not dry:
        conn.commit()
    return {'insertados': insertados, 'actualizados': actualizados, 'sin_cambios': sin_cambios}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-med', required=True, help='Ruta a CORREDORES DE MEDIACIÓN.txt')
    ap.add_argument('--input-tit', required=True, help='Ruta a CORREDORES DE TITAN.txt')
    ap.add_argument('--out', default=str(Path.home() / 'Downloads' / 'corredores_drive.csv'))
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--apply', action='store_true', help='upsert sobre BD V5')
    g.add_argument('--dry-run', action='store_true', help='preview upsert sin escribir')
    args = ap.parse_args()

    corredores = []
    for path in (args.input_med, args.input_tit):
        p = Path(path)
        if not p.exists():
            print(f"[ERROR] No existe {p}", file=sys.stderr)
            return 1
        c = parse_txt(p)
        print(f"  {p.name}: {len(c)} corredores")
        corredores.extend(c)

    print(f"Total: {len(corredores)} corredores")
    exportar_csv(corredores, Path(args.out))

    if args.apply or args.dry_run:
        print(f"\nBD: {DB_PATH}")
        if not os.path.exists(DB_PATH):
            print(f"[ERROR] No existe BD", file=sys.stderr)
            return 1
        conn = sqlite3.connect(DB_PATH)
        try:
            r = upsert_bd(conn, corredores, args.dry_run)
            modo = '(dry-run)' if args.dry_run else '(APLICADO)'
            print(f"\n{modo} Upsert: {r['insertados']} nuevos, {r['actualizados']} actualizados, {r['sin_cambios']} sin cambios")
        finally:
            conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
