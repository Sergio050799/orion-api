"""
PASO 3: importa las 41 flotas de 15_nuevas_desde_drive.csv como nuevas flotas en V5.
Antes de insertar, chequea por nombre normalizado y por CIF que no exista ya.

También aplica REMAR especial: la fila "REMAR SEFARAD flota" o similares se desdobla a las 6 sub-flotas con CIFs individuales.
"""
from __future__ import annotations

import csv
import os
import re
import sqlite3
import sys
import time
import unicodedata
from pathlib import Path

CSV_IN = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\15_nuevas_desde_drive.csv")
LOG_OUT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\21_paso3_importar_nuevas.log")

DB = os.environ.get('ORION_DB_PATH', r'C:\opt\orion_v5\data\orion.db')

# REMAR → 6 sub-flotas con CIFs específicos (mapping aprox del Drive INFORMACIÓN.xlsx)
REMAR_SUBFLOTAS = [
    ('REMAR CENTRAL',          'G09204884'),
    ('REMAR CASTILLA Y LEÓN',  'G35245893'),
    ('REMAR CANARIAS',         'G79059424'),
    ('REMAR CASTILLA LA MANCHA', 'G10111227'),
    ('REMAR EXTREMADURA',      'G19132059'),
    ('REMAR SEFARAD',          'G05366232'),
]
REMAR_IDS_MMT = {'REMAR CENTRAL':'50449','REMAR CASTILLA Y LEÓN':'50450','REMAR CANARIAS':'50451',
                 'REMAR CASTILLA LA MANCHA':'50452','REMAR EXTREMADURA':'50453','REMAR SEFARAD':'50454'}

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


def _uid(prefix): return f"{prefix}_{int(time.time()*1000)}_{os.urandom(3).hex()}"


def main():
    if not os.path.exists(DB):
        print(f"[ERROR] no existe BD", file=sys.stderr); return 1
    if not CSV_IN.exists():
        print(f"[ERROR] no existe CSV", file=sys.stderr); return 1

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    # Índice flotas existentes por CIF y por nombre
    v5_cif = {(r['cif'] or '').strip().upper(): r['id'] for r in conn.execute("SELECT id, cif FROM flotas").fetchall() if r['cif']}
    v5_nombre = {}
    for r in conn.execute("SELECT id, nombre FROM flotas").fetchall():
        n = norm(r['nombre'] or '')
        if n: v5_nombre.setdefault(n, []).append(r['id'])

    # Cargar nuevas candidatas
    with open(CSV_IN, 'r', encoding='utf-8-sig') as f:
        candidatas = list(csv.DictReader(f))

    insertadas = ya_existen = log_lines = 0
    log = []

    def insertar_flota(nombre, cif, categoria_drive, raw_carpeta, remar=False, corredor=''):
        nonlocal insertadas, ya_existen, log
        cif_up = (cif or '').strip().upper()
        if cif_up and cif_up in v5_cif:
            ya_existen += 1
            log.append(f"YA_EXISTE_POR_CIF\t{cif_up}\t{nombre}")
            return
        key = norm(nombre)
        if key and key in v5_nombre:
            ya_existen += 1
            log.append(f"YA_EXISTE_POR_NOMBRE\t{nombre}")
            return
        # Insertar flota
        fid = _uid('flota')
        conn.execute("""
            INSERT INTO flotas (id, cif, nombre, actividad, sucursal, es_historica)
            VALUES (?, ?, ?, '', '', 0)
        """, (fid, cif_up, nombre.strip()))
        # Y 1 estudio inicial (estado desde categoría)
        estado_map = {
            'ACTIVAS': 'CONTRATADA',
            'FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS': 'OFERTADA',
            'FLOTAS HECHAS POR TITAN 2025-2026': 'CONTRATADA',
            'ESTUDIOS': 'EN ESTUDIO',
            'FLOTAS REHUSADAS': 'RECHAZADA',
        }
        estado = estado_map.get(categoria_drive, 'EN ESTUDIO')
        eid = _uid('estudio')
        conn.execute("""
            INSERT INTO estudios (id, flota_id, nombre, estado, creado_por)
            VALUES (?, ?, ?, ?, 'importado-drive-18/11')
        """, (eid, fid, nombre.strip(), estado))
        if cif_up:
            v5_cif[cif_up] = fid
        if key:
            v5_nombre.setdefault(key, []).append(fid)
        insertadas += 1
        tag = 'REMAR' if remar else 'NUEVA'
        log.append(f"{tag}\t{fid}\t{nombre}\t{cif_up}\t{categoria_drive}")

    for c in candidatas:
        nombre = c['FLOTA']
        cifs_raw = (c['CIFS'] or '').split(',')
        cifs = [x.strip().upper() for x in cifs_raw if x.strip()]
        categoria = c['CATEGORIA']
        # Caso especial REMAR
        if 'REMAR' in nombre.upper():
            for subnom, subcif in REMAR_SUBFLOTAS:
                insertar_flota(subnom, subcif, 'ACTIVAS', c['RAW_CARPETA'], remar=True,
                              corredor=c.get('CORREDOR_SUGERIDO',''))
        else:
            # Para flotas con 1 CIF, 1 flota
            cif = cifs[0] if cifs else ''
            insertar_flota(nombre, cif, categoria, c['RAW_CARPETA'])

    conn.commit()
    conn.close()

    print(f"[PASO 3] Insertadas: {insertadas}, Ya existían: {ya_existen}")
    LOG_OUT.write_text('\n'.join(log), encoding='utf-8')
    print(f"[OK] Log -> {LOG_OUT}")


if __name__ == '__main__':
    raise SystemExit(main() or 0)
