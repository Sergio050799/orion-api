"""
Cruza las flotas de BD V5 con las flotas detectadas en Drive (inventario_flotas_drive.csv).

Matching por nombre normalizado (upper + sin acentos + sin sufijos societarios).
Las flotas V5 pueden tener varios estudios → 1 flota V5 puede corresponder a N
carpetas Drive (duplicados intencionales por año/corredor).

Produce 4 artefactos en C:\\Users\\garci\\Downloads\\ORION_auditoria_17_11_2026\\:
  03_matching_v5_vs_drive.md     resumen legible
  04_solo_en_v5.csv              flotas que están en V5 pero no en Drive ← LO QUE PIDE EL JEFE
  05_solo_en_drive.csv           flotas que están en Drive pero no en V5
  06_en_ambos.csv                match N:M con categoría drive
"""
from __future__ import annotations

import csv
import os
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')
DRIVE_CSV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\02_inventario_flotas_drive.csv")
OUT_DIR = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026")

SUFIJOS = [
    'SOCIEDAD LIMITADA', 'SOCIEDAD ANONIMA', 'S.L.U.', 'SLU', 'S.A.U.', 'SAU',
    'S.L.', 'SL', 'S.A.', 'SA', 'S.C.', 'SC', 'CB',
]
RUIDO = re.compile(r'\b(IKER|JOSEFINA|DELTA|AON|MDS|WILLIS|GESA|PIQUE|PIQUÉ|ENRIC|AGUSTIN|ARAGONES|MIGUEL|ROBERTO|OUMAIMA|SUSANA|TIRAN|TITAN|MOLYMA|JUNYENT|RUIZ|DOMINGUEZ|PREMIUM|CONFIGRUP|ERSM|ALCOSEGUR|ANTONIO|SEMECO|TRIVE|LARREA|ATSYR)\b', re.IGNORECASE)


def norm(s: str) -> str:
    """Normalización agresiva para matching."""
    if not s:
        return ''
    # Quitar sufijo típico 'NOMBRE - CORREDOR' / 'NOMBRE - CORREDOR - COMERCIAL'
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    # Quitar nombres de corredores y comerciales (ruido)
    s = RUIDO.sub(' ', s)
    # Cortar en el primer '-' después de limpiar ruido (segundo paso: ignorar lo que queda tras -)
    if '-' in s:
        s = s.split('-')[0]
    s = re.sub(r'[.,;:_/\\()]', ' ', s)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def cargar_v5(conn: sqlite3.Connection) -> list[dict]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT f.id, f.cif, f.nombre, f.sucursal, f.es_historica,
               (SELECT COUNT(*) FROM estudios e WHERE e.flota_id = f.id) AS n_estudios,
               (SELECT e.estado FROM estudios e WHERE e.flota_id = f.id
                ORDER BY e.actualizado_en DESC LIMIT 1) AS estado_ultimo,
               (SELECT COUNT(*) FROM emisiones em WHERE em.flota_id = f.id) AS n_emisiones
        FROM flotas f
    """).fetchall()
    out = []
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        d['nombre_norm'] = norm(r['nombre'] or '')
        out.append(d)
    return out


def cargar_drive(csv_path: Path) -> list[dict]:
    out = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append({
                'categoria': row['CATEGORIA'],
                'flota': row['FLOTA'],
                'flota_norm_original': row['FLOTA_NORMALIZADA'],
                'nombre_norm': norm(row['FLOTA']),
                'n_archivos': int(row['N_ARCHIVOS'] or 0),
                'mb': float(row['MB'] or 0),
                'id_drive': row['ID_DRIVE'],
            })
    return out


def main() -> int:
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] BD no existe en {DB_PATH}", file=sys.stderr)
        return 1
    if not DRIVE_CSV.exists():
        print(f"[ERROR] CSV Drive no existe en {DRIVE_CSV}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        v5 = cargar_v5(conn)
        drive = cargar_drive(DRIVE_CSV)
        print(f"V5:    {len(v5)} flotas")
        print(f"Drive: {len(drive)} flotas")

        # Indice por nombre normalizado
        v5_by_norm = defaultdict(list)
        for f in v5:
            if f['nombre_norm']:
                v5_by_norm[f['nombre_norm']].append(f)

        drive_by_norm = defaultdict(list)
        for d in drive:
            if d['nombre_norm']:
                drive_by_norm[d['nombre_norm']].append(d)

        # Categorización
        solo_v5 = []
        solo_drive = []
        match = []

        for norm_name, flotas in v5_by_norm.items():
            if norm_name in drive_by_norm:
                for f in flotas:
                    for d in drive_by_norm[norm_name]:
                        match.append({'v5': f, 'drive': d, 'match_key': norm_name})
            else:
                for f in flotas:
                    solo_v5.append(f)

        # Flotas V5 sin nombre normalizado (vacías, nulas, sin texto) → van a solo_v5
        for f in v5:
            if not f['nombre_norm']:
                solo_v5.append(f)

        for norm_name, dlist in drive_by_norm.items():
            if norm_name not in v5_by_norm:
                for d in dlist:
                    solo_drive.append(d)

        print()
        print(f"Solo en V5 (ORION):   {len(solo_v5)}")
        print(f"Solo en Drive:        {len(solo_drive)}")
        print(f"Match (N:M):          {len(match)} pares")

        # CSV solo_v5
        p = OUT_DIR / "04_solo_en_v5.csv"
        with open(p, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(['NOMBRE', 'CIF', 'SUCURSAL', 'N_ESTUDIOS', 'ESTADO_ULTIMO', 'N_EMISIONES', 'ID_V5'])
            for it in sorted(solo_v5, key=lambda x: (x['estado_ultimo'] or '', x['nombre'] or '')):
                w.writerow([
                    it['nombre'], it['cif'] or '', it['sucursal'] or '',
                    it['n_estudios'], it['estado_ultimo'] or '', it['n_emisiones'],
                    it['id'],
                ])
        print(f"[OK] {p.name}")

        # CSV solo_drive
        p = OUT_DIR / "05_solo_en_drive.csv"
        with open(p, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(['FLOTA', 'CATEGORIA_DRIVE', 'N_ARCHIVOS', 'MB', 'ID_DRIVE'])
            for it in sorted(solo_drive, key=lambda x: (x['categoria'], x['flota'])):
                w.writerow([it['flota'], it['categoria'], it['n_archivos'], it['mb'], it['id_drive']])
        print(f"[OK] {p.name}")

        # CSV match
        p = OUT_DIR / "06_en_ambos.csv"
        with open(p, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(['NOMBRE_V5', 'FLOTA_DRIVE', 'CATEGORIA_DRIVE', 'CIF', 'ESTADO_V5', 'N_ESTUDIOS_V5', 'N_ARCHIVOS_DRIVE', 'MATCH_KEY'])
            for m in sorted(match, key=lambda x: (x['drive']['categoria'], x['v5']['nombre'] or '')):
                w.writerow([
                    m['v5']['nombre'], m['drive']['flota'], m['drive']['categoria'],
                    m['v5']['cif'] or '', m['v5']['estado_ultimo'] or '',
                    m['v5']['n_estudios'], m['drive']['n_archivos'],
                    m['match_key'],
                ])
        print(f"[OK] {p.name}")

        # Markdown resumen
        md = []
        md.append("# Matching V5 (ORION) vs Drive — 17/11/2026\n\n")
        md.append(f"- Flotas en **V5 (ORION)**: `{len(v5)}`\n")
        md.append(f"- Flotas en **Drive**: `{len(drive)}`\n")
        md.append(f"- Nombres distintos normalizados que matchean: `{sum(1 for n in v5_by_norm if n in drive_by_norm)}`\n\n")
        md.append("## Resultados\n\n")
        md.append(f"| Clasificación | Nº |\n|---|---:|\n")
        md.append(f"| Solo en V5 (ORION extras) | **{len(solo_v5)}** |\n")
        md.append(f"| Solo en Drive (nuevas, no importadas) | **{len(solo_drive)}** |\n")
        md.append(f"| En ambos (match N:M por duplicados por año/corredor) | **{len(match)}** |\n\n")

        # Desglose solo_v5 por estado
        por_estado = defaultdict(int)
        for it in solo_v5:
            por_estado[it['estado_ultimo'] or '(sin estado)'] += 1
        md.append("### Solo en V5 — desglose por estado del estudio más reciente\n\n")
        for est, n in sorted(por_estado.items(), key=lambda x: -x[1]):
            md.append(f"- **{est}**: {n}\n")
        md.append("\nVer `04_solo_en_v5.csv` para la lista completa.\n\n")

        # Desglose solo_drive por categoria
        por_cat_d = defaultdict(int)
        for it in solo_drive:
            por_cat_d[it['categoria']] += 1
        md.append("### Solo en Drive — desglose por categoría\n\n")
        for cat, n in sorted(por_cat_d.items(), key=lambda x: -x[1]):
            md.append(f"- **{cat}**: {n}\n")
        md.append("\nVer `05_solo_en_drive.csv` para la lista completa.\n\n")

        # Match por categoria
        por_cat_m = defaultdict(int)
        for m in match:
            por_cat_m[m['drive']['categoria']] += 1
        md.append("### Match V5 ↔ Drive — desglose por categoría Drive\n\n")
        for cat, n in sorted(por_cat_m.items(), key=lambda x: -x[1]):
            md.append(f"- **{cat}**: {n} pares\n")
        md.append("\nVer `06_en_ambos.csv`.\n\n")

        md.append("## Interpretación\n\n")
        md.append("- **Solo en V5** = flotas que tú trabajaste directamente en ORION y nunca llegaron al Drive. Son datos reales, son las extras.\n")
        md.append("- **Solo en Drive** = flotas que trabajaste en el Drive pero nunca importaste a ORION. Oportunidad para traerlas.\n")
        md.append("- **Match N:M** = misma empresa con varias flotas en Drive (año/corredor distinto). Normal, el modelo V5 lo soporta como múltiples `estudios` por `flota`.\n")
        p = OUT_DIR / "03_matching_v5_vs_drive.md"
        p.write_text(''.join(md), encoding='utf-8')
        print(f"[OK] {p.name}")

    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
