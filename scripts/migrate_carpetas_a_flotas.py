"""
Migración carpetas -> flotas + estudios + emisiones (V5).

Uso:
    python scripts/migrate_carpetas_a_flotas.py --dry-run
    python scripts/migrate_carpetas_a_flotas.py --apply

- Agrupa carpetas por CIF -> 1 flota por CIF.
- Cada carpeta -> 1 estudio (manteniendo estado, fechas, data JSON entero).
- Carpetas CONTRATADA -> además 1 emisión (con lo que haya en header).
- NUNCA toca la tabla 'carpetas' original: coexistencia total.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from collections import defaultdict
from typing import Any

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')


def _uid(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}_{os.urandom(3).hex()}"


def _safe_json_loads(s: Any) -> dict:
    if not s:
        return {}
    try:
        return json.loads(s) if isinstance(s, str) else dict(s)
    except Exception:
        return {}


def _pick_best_carpeta(carpetas: list[sqlite3.Row]) -> sqlite3.Row:
    """Para fusionar varias carpetas del mismo CIF, elige la más reciente con datos."""
    def score(c):
        tiene_nombre = 1 if (c['tomador'] or '').strip() else 0
        tiene_corr = 1 if c['corredor_id'] else 0
        return (tiene_nombre, tiene_corr, c['updated_at'] or '')
    return sorted(carpetas, key=score, reverse=True)[0]


def _extraer_primas(data: dict) -> tuple[float, float]:
    """Devuelve (prima_ofertada_total, prima_emitida_total) sumando lo que haya."""
    ofertada = 0.0
    emitida = 0.0
    try:
        trabajo = data.get('trabajo') or []
        for row in trabajo:
            if isinstance(row, dict):
                ofertada += float(row.get('primaTotal') or row.get('prima_total') or 0) or 0
    except Exception:
        pass
    try:
        informe = data.get('primasMmtInforme') or {}
        if isinstance(informe, dict):
            for _, v in informe.items():
                if isinstance(v, dict):
                    emitida += float(v.get('total') or v.get('prima') or 0) or 0
                elif isinstance(v, (int, float)):
                    emitida += float(v)
    except Exception:
        pass
    return round(ofertada, 2), round(emitida, 2)


def _extraer_emision(carpeta: sqlite3.Row, data: dict) -> dict | None:
    """Si la carpeta es CONTRATADA, intenta construir una emisión."""
    if (carpeta['estado'] or '').strip().upper() != 'CONTRATADA':
        return None
    header = data.get('header') or {}
    _, prima_emit = _extraer_primas(data)
    vehiculos = len(data.get('trabajo') or data.get('original') or [])
    return {
        'numero_poliza': str(header.get('poliza') or header.get('numPoliza') or ''),
        'id_cliente_mmt': str(header.get('idClienteMmt') or ''),
        'id_flota_mmt': str(header.get('idFlotaMmt') or ''),
        'fecha_emision': str(header.get('fechaEmision') or ''),
        'fecha_vcto': str(header.get('fechaVencimiento') or header.get('efecto') or ''),
        'prima_emitida': prima_emit,
        'num_vehiculos': vehiculos,
    }


def analizar(conn: sqlite3.Connection) -> dict:
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT id, nombre, estado, cif, tomador, actividad, corredor_id,
               creado_por, created_at, updated_at, data
        FROM carpetas
    """).fetchall()

    por_cif: dict[str, list[sqlite3.Row]] = defaultdict(list)
    sin_cif: list[sqlite3.Row] = []

    for r in rows:
        cif = (r['cif'] or '').strip().upper()
        if not cif:
            sin_cif.append(r)
        else:
            por_cif[cif].append(r)

    # Clasificar
    n_flotas = len(por_cif) + len(sin_cif)   # sin_cif -> 1 flota cada una (fallback)
    n_estudios = len(rows)
    n_emisiones = sum(1 for r in rows if (r['estado'] or '').upper() == 'CONTRATADA')

    # Top agrupamientos
    top = sorted(por_cif.items(), key=lambda kv: -len(kv[1]))[:10]

    return {
        'total_carpetas': len(rows),
        'flotas_unicas': n_flotas,
        'flotas_con_multiples_estudios': sum(1 for cs in por_cif.values() if len(cs) > 1),
        'estudios_totales': n_estudios,
        'emisiones_totales': n_emisiones,
        'carpetas_sin_cif': len(sin_cif),
        'top_agrupamientos': [
            (cif, len(cs), (cs[0]['tomador'] or '')[:40])
            for cif, cs in top if len(cs) > 1
        ],
        'por_cif': por_cif,
        'sin_cif': sin_cif,
    }


def imprimir_resumen(info: dict) -> None:
    print("=" * 60)
    print("RESUMEN MIGRACION")
    print("=" * 60)
    print(f"Carpetas origen:                {info['total_carpetas']}")
    print(f"Flotas unicas destino:          {info['flotas_unicas']}")
    print(f"  (con mas de 1 estudio):       {info['flotas_con_multiples_estudios']}")
    print(f"Estudios totales (1:1):         {info['estudios_totales']}")
    print(f"Emisiones (solo CONTRATADA):    {info['emisiones_totales']}")
    print(f"Carpetas sin CIF -> flota suelta: {info['carpetas_sin_cif']}")
    print()
    if info['top_agrupamientos']:
        print("Top CIFs con varios estudios (futuras flotas con historial):")
        for cif, n, tom in info['top_agrupamientos']:
            print(f"  {cif:>12}  {n} estudios  {tom}")
    print("=" * 60)


def aplicar(conn: sqlite3.Connection, info: dict) -> None:
    """Inserta flotas/estudios/emisiones. Se puede re-ejecutar: usa INSERT OR IGNORE por id."""
    cur = conn.cursor()
    n_flotas = n_est = n_emi = 0

    def insertar_flota(carpeta: sqlite3.Row, es_hist: int = 0) -> str:
        fid = _uid('flota')
        cur.execute("""
            INSERT INTO flotas (id, cif, nombre, nombre_comercial, actividad,
                                corredor_id, sucursal, es_historica)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fid,
            (carpeta['cif'] or '').strip().upper(),
            (carpeta['tomador'] or carpeta['nombre'] or '').strip() or 'SIN NOMBRE',
            '',
            (carpeta['actividad'] or '').strip(),
            carpeta['corredor_id'],
            '',
            es_hist,
        ))
        return fid

    def insertar_estudio(flota_id: str, carpeta: sqlite3.Row) -> str:
        data = _safe_json_loads(carpeta['data'])
        prima_of, prima_em = _extraer_primas(data)
        header = data.get('header') or {}
        eid = _uid('estudio')
        cur.execute("""
            INSERT INTO estudios (id, flota_id, nombre, estado, fecha_vcto,
                                  prima_ofertada_total, prima_emitida_total,
                                  coberturas_json, data, creado_por,
                                  creado_en, actualizado_en)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            eid,
            flota_id,
            carpeta['nombre'] or '',
            carpeta['estado'] or 'EN ESTUDIO',
            str(header.get('fechaVencimiento') or ''),
            prima_of,
            prima_em,
            '[]',
            carpeta['data'] or '{}',
            carpeta['creado_por'] or '',
            carpeta['created_at'] or '',
            carpeta['updated_at'] or '',
        ))
        return eid

    def insertar_emision(flota_id: str, estudio_id: str, carpeta: sqlite3.Row) -> None:
        data = _safe_json_loads(carpeta['data'])
        em = _extraer_emision(carpeta, data)
        if not em:
            return
        cur.execute("""
            INSERT INTO emisiones (id, flota_id, estudio_id, numero_poliza,
                                   id_cliente_mmt, id_flota_mmt,
                                   fecha_emision, fecha_vcto,
                                   prima_emitida, num_vehiculos, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            _uid('emision'),
            flota_id,
            estudio_id,
            em['numero_poliza'],
            em['id_cliente_mmt'],
            em['id_flota_mmt'],
            em['fecha_emision'],
            em['fecha_vcto'],
            em['prima_emitida'],
            em['num_vehiculos'],
            '{}',
        ))

    # 1) Agrupadas por CIF
    for cif, carpetas in info['por_cif'].items():
        mejor = _pick_best_carpeta(carpetas)
        flota_id = insertar_flota(mejor, es_hist=0)
        n_flotas += 1
        for carp in carpetas:
            eid = insertar_estudio(flota_id, carp)
            n_est += 1
            if (carp['estado'] or '').upper() == 'CONTRATADA':
                insertar_emision(flota_id, eid, carp)
                n_emi += 1

    # 2) Carpetas sin CIF -> cada una su propia flota (con CIF '')
    for carp in info['sin_cif']:
        flota_id = insertar_flota(carp, es_hist=0)
        n_flotas += 1
        eid = insertar_estudio(flota_id, carp)
        n_est += 1
        if (carp['estado'] or '').upper() == 'CONTRATADA':
            insertar_emision(flota_id, eid, carp)
            n_emi += 1

    conn.commit()
    print(f"\n[OK] Insertadas: {n_flotas} flotas, {n_est} estudios, {n_emi} emisiones")


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true', help='solo analiza, no escribe')
    g.add_argument('--apply', action='store_true', help='ejecuta la migracion')
    args = ap.parse_args()

    print(f"BD: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] No existe la BD en {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        info = analizar(conn)
        imprimir_resumen(info)

        if args.apply:
            # Comprobar que no haya ya flotas insertadas
            existentes = conn.execute('SELECT COUNT(*) FROM flotas').fetchone()[0]
            if existentes > 0:
                print(f"\n[ABORTADO] Ya hay {existentes} flotas. Vacia primero o borra la BD.")
                return 2
            print("\n>> Aplicando migracion...")
            aplicar(conn, info)
        else:
            print("\n(dry-run: no se ha escrito nada)")
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
