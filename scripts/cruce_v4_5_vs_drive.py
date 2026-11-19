"""
Cruce V4.5 (BD prod fresca en C:\\opt\\orion\\data\\orion.db) ↔ Drive V2 (10_extraccion_masiva_v2.csv).

Clasifica cada flota en 5 categorías:
  A) ORION sin CIF + Drive con CIF    → CANDIDATA A RELLENAR
  B) ORION con CIF + Drive con CIF (igual)  → ya ok
  C) ORION con CIF + Drive con CIF (distinto) → ALERTA discrepancia
  D) ORION con CIF + Drive sin CIF    → ok, Drive menos info que ORION
  E) Drive con CIF + sin match en ORION → NUEVA flota candidata a importar

Produce:
  12_cruce_v4_5_vs_drive.md             resumen legible
  13_candidatas_rellenar_cif.csv        clase A
  14_discrepancias_cif.csv              clase C
  15_nuevas_desde_drive.csv             clase E
  16_sin_cif_en_ningun_lado.csv         para búsqueda manual del jefe
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

BD_V4_5 = Path(r"C:\opt\orion\data\orion.db")
DRIVE_CSV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\10_extraccion_masiva_v2.csv")
SIN_CIF_CSV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\11_sin_cif_para_revisar.csv")
OUT_DIR = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026")

SUFIJOS = [
    'SOCIEDAD LIMITADA', 'SOCIEDAD ANONIMA', 'S.L.U.', 'SLU', 'S.A.U.', 'SAU',
    'S.L.', 'SL', 'S.A.', 'SA', 'S.C.', 'SC', 'CB',
]
RUIDO = re.compile(r'\b(IKER|JOSEFINA|DELTA|AON|MDS|WILLIS|GESA|PIQUE|PIQUÉ|ENRIC|AGUSTIN|ARAGONES|MIGUEL|ROBERTO|OUMAIMA|SUSANA|TITAN|MOLYMA|JUNYENT|RUIZ|DOMINGUEZ|PREMIUM|CONFIGRUP|ERSM|ALCOSEGUR|ANTONIO|SEMECO|TRIVE|LARREA|ATSYR)\b', re.IGNORECASE)


def norm(s: str) -> str:
    if not s:
        return ''
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    s = RUIDO.sub(' ', s)
    if '-' in s:
        s = s.split('-')[0]
    s = re.sub(r'[.,;:_/\\()]', ' ', s)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def main():
    if not BD_V4_5.exists():
        print(f"[ERROR] no existe BD V4.5 en {BD_V4_5}", file=sys.stderr)
        return 1
    if not DRIVE_CSV.exists():
        print(f"[ERROR] no existe CSV Drive", file=sys.stderr)
        return 1

    # Cargar ORION (tabla carpetas, modelo V4.5)
    conn = sqlite3.connect(str(BD_V4_5))
    conn.row_factory = sqlite3.Row
    orion = []
    for r in conn.execute("""
        SELECT id, nombre, cif, estado, corredor_id, tomador, actividad
        FROM carpetas
    """).fetchall():
        d = dict(r)
        d['nombre_norm'] = norm(r['nombre'] or '')
        orion.append(d)
    conn.close()
    print(f"ORION V4.5: {len(orion)} carpetas")

    # Cargar Drive V2 (solo las que tienen CIF estricto)
    drive = []
    with open(DRIVE_CSV, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            cifs = [c for c in (row['CIFS_ESTRICTOS'] or '').split(',') if c.strip()]
            if cifs:
                drive.append({
                    'categoria': row['CATEGORIA'],
                    'flota': row['FLOTA'],
                    'raw': row['RAW_CARPETA'],
                    'nombre_norm': norm(row['FLOTA']),
                    'corredor': row['CORREDOR_SUGERIDO'],
                    'comercial': row['COMERCIAL_SUGERIDO'],
                    'cifs': cifs,
                })
    print(f"Drive V2 con CIF estricto: {len(drive)}")

    # Índices
    orion_by_norm = defaultdict(list)
    for o in orion:
        if o['nombre_norm']:
            orion_by_norm[o['nombre_norm']].append(o)

    drive_by_norm = defaultdict(list)
    for d in drive:
        if d['nombre_norm']:
            drive_by_norm[d['nombre_norm']].append(d)

    # Clasificar
    candidatas_rellenar = []  # A
    discrepancias = []         # C
    nuevas_desde_drive = []    # E
    coinciden = []             # B
    orion_cif_drive_sin = []   # D

    matched_orion_ids = set()

    for norm_name, drive_items in drive_by_norm.items():
        if norm_name not in orion_by_norm:
            # E: Drive con CIF, no en ORION
            for d in drive_items:
                nuevas_desde_drive.append(d)
            continue
        orion_items = orion_by_norm[norm_name]
        # Cruce N:M
        for d in drive_items:
            cif_drive = d['cifs'][0]  # el primero; si hay múltiples, se muestran todos
            for o in orion_items:
                matched_orion_ids.add(o['id'])
                cif_orion = (o['cif'] or '').strip().upper()
                if not cif_orion:
                    candidatas_rellenar.append({
                        'orion_id': o['id'],
                        'orion_nombre': o['nombre'],
                        'orion_estado': o['estado'],
                        'drive_flota': d['flota'],
                        'drive_categoria': d['categoria'],
                        'drive_cif': cif_drive,
                        'drive_cifs_todos': ','.join(d['cifs']),
                        'corredor_sugerido': d['corredor'],
                        'comercial_sugerido': d['comercial'],
                    })
                elif cif_drive == cif_orion:
                    coinciden.append({
                        'orion_id': o['id'],
                        'cif': cif_orion,
                        'nombre': o['nombre'],
                    })
                else:
                    # Discrepancia
                    discrepancias.append({
                        'orion_id': o['id'],
                        'nombre_orion': o['nombre'],
                        'cif_orion': cif_orion,
                        'drive_flota': d['flota'],
                        'drive_categoria': d['categoria'],
                        'cif_drive': cif_drive,
                        'drive_cifs_todos': ','.join(d['cifs']),
                    })

    # D: ORION con CIF pero Drive sin CIF para esa flota (o no está en Drive)
    for o in orion:
        if o['id'] in matched_orion_ids:
            continue
        if (o['cif'] or '').strip():
            orion_cif_drive_sin.append(o)

    # Sin CIF en ningún lado: ORION sin CIF ni en Drive
    sin_cif_total = []
    for o in orion:
        if (o['cif'] or '').strip():
            continue
        if o['id'] in matched_orion_ids:
            # Fue encontrado en Drive. Si sigue siendo candidata_rellenar o laxo... ya lo tenemos.
            continue
        sin_cif_total.append(o)

    print()
    print(f"A) Candidatas a rellenar CIF (ORION vacío + Drive confirma): {len(candidatas_rellenar)}")
    print(f"B) Ya coinciden (ambos CIF iguales):                         {len(coinciden)}")
    print(f"C) Discrepancias CIF (ambos tienen pero distintos):          {len(discrepancias)}")
    print(f"D) ORION con CIF, Drive sin match:                           {len(orion_cif_drive_sin)}")
    print(f"E) Nuevas en Drive (CIF + sin match ORION):                  {len(nuevas_desde_drive)}")
    print(f"Sin CIF en ningún lado:                                      {len(sin_cif_total)}")

    # CSVs
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUT_DIR / "13_candidatas_rellenar_cif.csv", 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['orion_id', 'orion_nombre', 'orion_estado',
                                          'drive_flota', 'drive_categoria', 'drive_cif',
                                          'drive_cifs_todos', 'corredor_sugerido', 'comercial_sugerido'])
        w.writeheader()
        for row in candidatas_rellenar:
            w.writerow(row)

    with open(OUT_DIR / "14_discrepancias_cif.csv", 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['orion_id', 'nombre_orion', 'cif_orion',
                                          'drive_flota', 'drive_categoria', 'cif_drive', 'drive_cifs_todos'])
        w.writeheader()
        for row in discrepancias:
            w.writerow(row)

    with open(OUT_DIR / "15_nuevas_desde_drive.csv", 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['FLOTA', 'CATEGORIA', 'CIFS', 'CORREDOR_SUGERIDO', 'COMERCIAL_SUGERIDO', 'RAW_CARPETA'])
        for d in nuevas_desde_drive:
            w.writerow([d['flota'], d['categoria'], ','.join(d['cifs']),
                       d['corredor'], d['comercial'], d['raw']])

    with open(OUT_DIR / "16_sin_cif_en_ningun_lado.csv", 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['ID_ORION', 'NOMBRE', 'ESTADO', 'TOMADOR', 'ACTIVIDAD'])
        for o in sorted(sin_cif_total, key=lambda x: (x['estado'] or '', x['nombre'] or '')):
            w.writerow([o['id'], o['nombre'], o['estado'], o['tomador'], o['actividad']])

    # Markdown
    md = []
    md.append("# Cruce ORION V4.5 ↔ Drive V2 — 18/11/2026\n\n")
    md.append(f"- ORION V4.5 (BD fresca): **{len(orion)}** carpetas\n")
    md.append(f"- Drive V2 (CIFs confirmados): **{len(drive)}** flotas\n\n")
    md.append("## Resultados del cruce\n\n")
    md.append("| Clasificación | Nº | Qué hacer |\n|---|---:|---|\n")
    md.append(f"| **A** Candidatas a rellenar CIF (ORION vacío + Drive confirma) | **{len(candidatas_rellenar)}** | **Aplicar en V5** |\n")
    md.append(f"| **B** Ya coinciden | {len(coinciden)} | Nada |\n")
    md.append(f"| **C** Discrepancia CIF (ambos tienen pero distintos) | **{len(discrepancias)}** | **Revisión manual** |\n")
    md.append(f"| **D** ORION con CIF, Drive sin match | {len(orion_cif_drive_sin)} | Nada |\n")
    md.append(f"| **E** Nuevas en Drive (sin match ORION) | **{len(nuevas_desde_drive)}** | **Decidir si importar** |\n")
    md.append(f"| Sin CIF en ningún lado | **{len(sin_cif_total)}** | **Búsqueda manual del jefe** |\n\n")

    md.append("## A — Candidatas a rellenar CIF (muestra primeras 15)\n\n")
    md.append("| ORION Nombre | ORION Estado | CIF Drive | Corredor | Comercial |\n|---|---|---|---|---|\n")
    for c in candidatas_rellenar[:15]:
        md.append(f"| {c['orion_nombre']} | {c['orion_estado']} | `{c['drive_cif']}` | {c['corredor_sugerido']} | {c['comercial_sugerido']} |\n")
    if len(candidatas_rellenar) > 15:
        md.append(f"\n... y {len(candidatas_rellenar)-15} más. Lista completa en `13_candidatas_rellenar_cif.csv`.\n")

    md.append("\n## C — Discrepancias CIF (importante revisar)\n\n")
    if discrepancias:
        md.append("| ORION Nombre | CIF ORION | CIF Drive |\n|---|---|---|\n")
        for d in discrepancias[:20]:
            md.append(f"| {d['nombre_orion']} | `{d['cif_orion']}` | `{d['cif_drive']}` |\n")
        if len(discrepancias) > 20:
            md.append(f"\n... y {len(discrepancias)-20} más.\n")
    else:
        md.append("_Ninguna. ORION y Drive concuerdan en CIFs._\n")

    md.append("\n## E — Flotas nuevas descubiertas en Drive (primeras 15)\n\n")
    for d in nuevas_desde_drive[:15]:
        md.append(f"- [{d['categoria']}] **{d['flota']}** — CIF: `{d['cifs'][0]}`  {('(+ ' + str(len(d['cifs'])-1) + ' más)') if len(d['cifs'])>1 else ''}\n")
    if len(nuevas_desde_drive) > 15:
        md.append(f"\n... y {len(nuevas_desde_drive)-15} más en `15_nuevas_desde_drive.csv`.\n")

    md.append("\n## Siguiente paso propuesto\n\n")
    md.append(f"1. Revisar `13_candidatas_rellenar_cif.csv` ({len(candidatas_rellenar)}) y aplicar CIFs con 1 script.\n")
    md.append(f"2. Revisar `14_discrepancias_cif.csv` ({len(discrepancias)}) manualmente.\n")
    md.append(f"3. Revisar `15_nuevas_desde_drive.csv` ({len(nuevas_desde_drive)}) y decidir cuáles importar.\n")
    md.append(f"4. Las `16_sin_cif_en_ningun_lado.csv` ({len(sin_cif_total)}) → búsqueda manual por nombre en Internet / eInforma / BORME.\n")

    (OUT_DIR / "12_cruce_v4_5_vs_drive.md").write_text(''.join(md), encoding='utf-8')
    print(f"\n[OK] Reporte: {OUT_DIR}\\12_cruce_v4_5_vs_drive.md")


if __name__ == '__main__':
    raise SystemExit(main() or 0)
