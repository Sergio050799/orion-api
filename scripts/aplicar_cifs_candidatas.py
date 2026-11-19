"""
PASO 2: aplica los 150 CIFs de 13_candidatas_rellenar_cif.csv a las flotas V5.
Matching por nombre normalizado (flota V5 ↔ orion_nombre del CSV).
Idempotente: si ya tiene CIF igual, no toca; si distinto, deja log.
"""
from __future__ import annotations

import csv
import os
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

CSV_IN = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\13_candidatas_rellenar_cif.csv")
LOG_OUT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\20_paso2_aplicar_cifs.log")

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
        print(f"[ERROR] no existe BD en {DB}", file=sys.stderr); return 1
    if not CSV_IN.exists():
        print(f"[ERROR] no existe {CSV_IN}", file=sys.stderr); return 1

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    # Index V5 flotas por nombre normalizado
    v5 = {}
    for r in conn.execute("SELECT id, nombre, cif FROM flotas").fetchall():
        n = norm(r['nombre'] or '')
        if n:
            v5.setdefault(n, []).append(dict(r))

    # Candidatas
    with open(CSV_IN, 'r', encoding='utf-8-sig') as f:
        candidatas = list(csv.DictReader(f))

    aplicadas = 0
    ya_ok = 0
    no_match = 0
    conflictos = 0
    log = []

    for c in candidatas:
        key = norm(c['orion_nombre'])
        drive_cif = c['drive_cif']
        if key not in v5:
            no_match += 1
            log.append(f"NO_MATCH\t{c['orion_nombre']}\t{drive_cif}")
            continue
        for flota in v5[key]:
            cif_actual = (flota['cif'] or '').strip().upper()
            if not cif_actual:
                conn.execute("UPDATE flotas SET cif=?, actualizada_en=datetime('now') WHERE id=?",
                             (drive_cif, flota['id']))
                aplicadas += 1
                log.append(f"APLICADO\t{flota['id']}\t{flota['nombre']}\t{drive_cif}")
            elif cif_actual == drive_cif:
                ya_ok += 1
            else:
                conflictos += 1
                log.append(f"CONFLICTO\t{flota['id']}\t{flota['nombre']}\tactual={cif_actual}\tdrive={drive_cif}")

    conn.commit()
    conn.close()

    print(f"[PASO 2] Aplicadas: {aplicadas}, Ya OK: {ya_ok}, Conflictos: {conflictos}, Sin match V5: {no_match}")
    LOG_OUT.write_text('\n'.join(log), encoding='utf-8')
    print(f"[OK] Log -> {LOG_OUT}")


if __name__ == '__main__':
    raise SystemExit(main() or 0)
