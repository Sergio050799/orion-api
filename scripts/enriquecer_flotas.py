"""
Enriquece flotas V5 con datos derivados:
  1. Rescata CIF desde el JSON data de la carpeta origen (header, original, oferta, sinco...).
  2. Deduce sucursal desde corredor.sucursal si la flota tiene corredor.
  3. Detecta duplicados por nombre normalizado y los lista.

Uso:
    python scripts/enriquecer_flotas.py --dry-run
    python scripts/enriquecer_flotas.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')

# CIF espanol: letra inicial + 7 digitos + digito o letra de control
CIF_RE = re.compile(r'\b([ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J])\b')
# NIF persona fisica (autonomos) por si acaso
NIF_RE = re.compile(r'\b(\d{8}[A-HJ-NP-TV-Z])\b')

# Sufijos societarios a limpiar al normalizar nombres
SUFIJOS = [
    'SOCIEDAD LIMITADA', 'SOCIEDAD ANONIMA', 'SOCIEDAD COOPERATIVA',
    'SOCIEDAD CIVIL', 'SOCIEDAD LIMITADA UNIPERSONAL',
    'S.L.U.', 'SLU', 'S.A.U.', 'SAU',
    'S.L.N.E.', 'SLNE', 'S.COOP.', 'SCOOP', 'S.COOP',
    'S.L.', 'SL', 'S.A.', 'SA', 'S.C.', 'SC',
    'C.B.', 'CB', 'S.R.L.', 'SRL',
]


def normalizar_nombre(s: str) -> str:
    if not s:
        return ''
    # quitar acentos
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    # quitar puntuacion/comas
    s = re.sub(r'[.,;:\-_/\\]', ' ', s)
    # quitar sufijos (ordenados por longitud desc para que no se coman piezas)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    # comprimir espacios
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _buscar_cif_en(obj) -> str | None:
    """Busca recursivamente un CIF en claves tipo 'cif' o aplica regex al JSON string."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        # claves explicitas primero
        for k, v in obj.items():
            if str(k).lower() in ('cif', 'nif', 'cifnif', 'cif_nif', 'cif/nif'):
                if isinstance(v, str) and (m := CIF_RE.search(v.upper())):
                    return m.group(1)
        # recursivo
        for v in obj.values():
            if (r := _buscar_cif_en(v)):
                return r
    elif isinstance(obj, list):
        for v in obj:
            if (r := _buscar_cif_en(v)):
                return r
    elif isinstance(obj, str):
        m = CIF_RE.search(obj.upper())
        if m:
            return m.group(1)
    return None


def rescatar_cif(data_json: str, nombre_flota: str = '') -> tuple[str | None, str]:
    """Devuelve (cif_o_none, fuente) tras barrer el JSON."""
    data = None
    try:
        data = json.loads(data_json or '{}')
    except Exception:
        return None, 'json-invalido'

    # 1. Prioridad: data.header.cif
    hdr_cif = ((data.get('header') or {}).get('cif') or '').strip().upper()
    if hdr_cif and CIF_RE.match(hdr_cif):
        return hdr_cif, 'header.cif'

    # 2. Buscar en claves 'cif' explicitas
    cif = _buscar_cif_en(data)
    if cif:
        return cif, 'json-recursivo'

    # 3. Regex sobre string completo (ultimo recurso)
    raw = (data_json or '').upper()
    cifs = list(set(CIF_RE.findall(raw)))
    if len(cifs) == 1:
        return cifs[0], 'regex-unico'
    elif len(cifs) > 1:
        # Varios CIFs — devolver el que aparece mas veces en el string
        counts = {c: raw.count(c) for c in cifs}
        top = max(counts, key=counts.get)
        if counts[top] >= 2 * (sum(counts.values()) - counts[top]):
            return top, f'regex-dominante({len(cifs)})'
        return None, f'ambiguo-{len(cifs)}-cifs'
    return None, 'no-encontrado'


def paso1_rescatar_cifs(conn: sqlite3.Connection, dry: bool) -> dict:
    conn.row_factory = sqlite3.Row
    # Para cada flota sin CIF, miramos sus estudios y sus carpetas origen
    flotas_sin_cif = conn.execute("""
        SELECT f.id, f.nombre
        FROM flotas f
        WHERE f.cif = '' OR f.cif IS NULL
    """).fetchall()

    recuperados = 0
    ambiguos = 0
    no_encontrados = 0
    log = []

    for f in flotas_sin_cif:
        # Cada flota tiene estudios; data del estudio = data de la carpeta origen
        estudios = conn.execute("""
            SELECT id, data FROM estudios WHERE flota_id = ?
        """, (f['id'],)).fetchall()

        cif_final = None
        fuente_final = ''
        for e in estudios:
            cif, fuente = rescatar_cif(e['data'] or '{}', f['nombre'])
            if cif:
                cif_final = cif
                fuente_final = fuente
                break

        if cif_final:
            recuperados += 1
            log.append((f['id'], f['nombre'][:30], cif_final, fuente_final))
            if not dry:
                conn.execute("UPDATE flotas SET cif=?, actualizada_en=datetime('now') WHERE id=?",
                             (cif_final, f['id']))
        elif 'ambiguo' in fuente_final:
            ambiguos += 1
        else:
            no_encontrados += 1

    if not dry:
        conn.commit()

    return {
        'flotas_sin_cif': len(flotas_sin_cif),
        'recuperados': recuperados,
        'ambiguos': ambiguos,
        'no_encontrados': no_encontrados,
        'log': log,
    }


def paso2_sucursal_por_corredor(conn: sqlite3.Connection, dry: bool) -> dict:
    conn.row_factory = sqlite3.Row
    # Flotas sin sucursal pero con corredor que si la tiene
    rows = conn.execute("""
        SELECT f.id, f.nombre, co.sucursal AS suc_corredor
        FROM flotas f
        JOIN corredores co ON co.id = f.corredor_id
        WHERE (f.sucursal = '' OR f.sucursal IS NULL)
          AND co.sucursal IS NOT NULL
          AND co.sucursal != ''
    """).fetchall()

    if not dry:
        for r in rows:
            conn.execute("UPDATE flotas SET sucursal=?, actualizada_en=datetime('now') WHERE id=?",
                         (r['suc_corredor'], r['id']))
        conn.commit()

    return {'actualizadas': len(rows)}


def paso4_propagar_cif_duplicados(conn: sqlite3.Connection, dry: bool) -> dict:
    """Si grupo de duplicados tiene 1 flota con CIF y el resto sin, propagar."""
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, nombre, cif FROM flotas WHERE nombre != ''").fetchall()
    grupos = defaultdict(list)
    for r in rows:
        grupos[normalizar_nombre(r['nombre'])].append(dict(r))

    propagados = []
    for norm, items in grupos.items():
        if len(items) < 2:
            continue
        con_cif = [it for it in items if (it['cif'] or '').strip()]
        sin_cif = [it for it in items if not (it['cif'] or '').strip()]
        if len(con_cif) == 1 and sin_cif:
            cif_fuente = con_cif[0]['cif']
            for destino in sin_cif:
                propagados.append((destino['id'], destino['nombre'], cif_fuente))
                if not dry:
                    conn.execute(
                        "UPDATE flotas SET cif=?, actualizada_en=datetime('now') WHERE id=?",
                        (cif_fuente, destino['id']))
    if not dry:
        conn.commit()
    return {'propagados': propagados}


def paso3_detectar_duplicados(conn: sqlite3.Connection) -> dict:
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT f.id, f.nombre, f.cif, f.sucursal,
               (SELECT e2.estado FROM estudios e2
                WHERE e2.flota_id = f.id
                ORDER BY e2.actualizado_en DESC LIMIT 1) AS estado_ultimo,
               (SELECT COUNT(*) FROM estudios e3 WHERE e3.flota_id = f.id) AS n_estudios
        FROM flotas f
        WHERE f.nombre != ''
    """).fetchall()

    grupos = defaultdict(list)
    for r in rows:
        norm = normalizar_nombre(r['nombre'])
        if norm:
            grupos[norm].append(dict(r))

    duplicados = {k: v for k, v in grupos.items() if len(v) > 1}

    # Clasificar: duplicados "sospechosos" = al menos 1 EN ESTUDIO/OFERTADA
    sospechosos = {}
    for k, v in duplicados.items():
        estados = {it['estado_ultimo'] for it in v}
        if estados & {'EN ESTUDIO', 'OFERTADA'}:
            sospechosos[k] = v

    return {
        'total_grupos_duplicados': len(duplicados),
        'grupos_sospechosos': sospechosos,
        'todos_grupos': duplicados,
    }


def imprimir_resumen(r1: dict, r2: dict, r3: dict, dry: bool) -> None:
    accion = "(dry-run)" if dry else "(APLICADO)"
    print("=" * 66)
    print(f"ENRIQUECIMIENTO FLOTAS V5  {accion}")
    print("=" * 66)
    print()
    print("[Paso 1] Rescate CIF desde JSON")
    print(f"  Flotas sin CIF:        {r1['flotas_sin_cif']}")
    print(f"  Recuperados:           {r1['recuperados']}")
    print(f"  Ambiguos (varios CIF): {r1['ambiguos']}")
    print(f"  No encontrados:        {r1['no_encontrados']}")
    if r1['log']:
        print("  Primeros 10 recuperados:")
        for id_, nom, cif, fuente in r1['log'][:10]:
            print(f"    {cif:>12}  {fuente:<20}  {nom}")
    print()
    print("[Paso 2] Sucursal por corredor")
    print(f"  Flotas actualizadas:   {r2['actualizadas']}")
    print()
    print("[Paso 3] Duplicados por nombre normalizado")
    print(f"  Grupos duplicados:        {r3['total_grupos_duplicados']}")
    print(f"  Sospechosos (hay EN ESTUDIO/OFERTADA): {len(r3['grupos_sospechosos'])}")
    if r3['grupos_sospechosos']:
        print("  Primeros 15 sospechosos:")
        for norm, items in list(r3['grupos_sospechosos'].items())[:15]:
            print(f"  --- '{norm}' ({len(items)} flotas) ---")
            for it in items:
                cif = it['cif'] or '(sin CIF)'
                est = it['estado_ultimo'] or '-'
                print(f"      {est:<12} {cif:<12} {it['nombre']}")
    print()
    print("=" * 66)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    print(f"BD: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] No existe la BD en {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        dry = args.dry_run
        r1 = paso1_rescatar_cifs(conn, dry)
        r2 = paso2_sucursal_por_corredor(conn, dry)
        r4 = paso4_propagar_cif_duplicados(conn, dry)
        r3 = paso3_detectar_duplicados(conn)
        imprimir_resumen(r1, r2, r3, dry)
        print(f"[Paso 4] CIFs propagados entre duplicados: {len(r4['propagados'])}")
        for id_, nom, cif in r4['propagados'][:10]:
            print(f"    {cif:>12}  -> {nom[:40]}")
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
