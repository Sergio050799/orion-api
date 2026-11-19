"""
PASO 4: asigna comerciales detectados en 10_extraccion_masiva_v2.csv a flotas/estudios V5.

Regla:
  - flotas.comercial_traido_id ← el comercial detectado en el nombre de carpeta Drive
  - estudios.comercial_id       ← mismo comercial para TODOS los estudios de esa flota (en este primer pase)

Matching por nombre normalizado flota V5 ↔ flota Drive.
Solo se asigna si el comercial existe en la tabla `comerciales`.
"""
from __future__ import annotations

import csv
import os
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

CSV_IN = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\10_extraccion_masiva_v2.csv")
LOG_OUT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\22_paso4_asignar_comerciales.log")

DB = os.environ.get('ORION_DB_PATH', r'C:\opt\orion_v5\data\orion.db')

SUFIJOS = ['SOCIEDAD LIMITADA','SOCIEDAD ANONIMA','S.L.U.','SLU','S.A.U.','SAU',
           'S.L.','SL','S.A.','SA','S.C.','SC','CB']
RUIDO = re.compile(r'\b(IKER|JOSEFINA|DELTA|AON|MDS|WILLIS|GESA|PIQUE|PIQUÉ|ENRIC|AGUSTIN|ARAGONES|MIGUEL|ROBERTO|OUMAIMA|SUSANA|TITAN|MOLYMA|JUNYENT|RUIZ|DOMINGUEZ|PREMIUM|CONFIGRUP|ERSM|ALCOSEGUR|ANTONIO|SEMECO|TRIVE|LARREA|ATSYR)\b', re.IGNORECASE)


def norm(s: str) -> str:
    if not s: return ''
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    s = RUIDO.sub(' ', s)
    if '-' in s: s = s.split('-')[0]
    s = re.sub(r'[.,;:_/\\()]', ' ', s)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    if not os.path.exists(DB):
        print(f"[ERROR] no existe BD", file=sys.stderr); return 1
    if not CSV_IN.exists():
        print(f"[ERROR] no existe CSV", file=sys.stderr); return 1

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    # Comerciales disponibles
    com_ids = {r['nombre'].upper(): r['id'] for r in conn.execute("SELECT id, nombre FROM comerciales").fetchall()}

    # Flotas V5 por nombre
    flotas_v5 = {}
    for r in conn.execute("SELECT id, nombre FROM flotas").fetchall():
        k = norm(r['nombre'] or '')
        if k: flotas_v5.setdefault(k, []).append(r['id'])

    # Leer extracción
    with open(CSV_IN, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    aplic_flota = aplic_estudios = sin_comercial = sin_match = 0
    log = []

    for row in rows:
        com_nom = (row['COMERCIAL_SUGERIDO'] or '').strip().upper()
        if not com_nom:
            continue
        if com_nom not in com_ids:
            sin_comercial += 1
            log.append(f"COMERCIAL_NO_EXISTE\t{com_nom}\t{row['FLOTA']}")
            continue
        com_id = com_ids[com_nom]
        key = norm(row['FLOTA'])
        if key not in flotas_v5:
            sin_match += 1
            log.append(f"FLOTA_SIN_MATCH\t{row['FLOTA']}")
            continue
        for fid in flotas_v5[key]:
            # Flota: solo si no tiene ya
            r = conn.execute("SELECT comercial_traido_id FROM flotas WHERE id=?", (fid,)).fetchone()
            if not r['comercial_traido_id']:
                conn.execute("UPDATE flotas SET comercial_traido_id=? WHERE id=?", (com_id, fid))
                aplic_flota += 1
            # Estudios de esa flota: todos los que no tengan
            n = conn.execute("""
                UPDATE estudios SET comercial_id=?
                WHERE flota_id=? AND (comercial_id IS NULL OR comercial_id='')
            """, (com_id, fid)).rowcount
            aplic_estudios += n
            log.append(f"APLICADO\t{fid}\t{row['FLOTA']}\t{com_nom}")

    conn.commit()
    conn.close()

    print(f"[PASO 4] Flotas con comercial_traido: {aplic_flota}")
    print(f"[PASO 4] Estudios con comercial:      {aplic_estudios}")
    print(f"[PASO 4] Comercial no en seed:        {sin_comercial}")
    print(f"[PASO 4] Flota sin match V5:          {sin_match}")
    LOG_OUT.write_text('\n'.join(log), encoding='utf-8')
    print(f"[OK] Log -> {LOG_OUT}")


if __name__ == '__main__':
    raise SystemExit(main() or 0)
