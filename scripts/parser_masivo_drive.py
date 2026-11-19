"""
Parser masivo de la carpeta Drive_dump. Recorre cada flota y extrae:
  - CIFs encontrados (en eml + xlsx)
  - IDs MMT (números tipo 7 u 8 dígitos cerca de la palabra 'ID' o 'perceptor')
  - Corredor sugerido (del nombre de la carpeta)
  - Comercial sugerido (del nombre de la carpeta, si matchea con lista conocida)

Estructura asumida:
  Drive_dump/ACTIVAS/<CORREDOR>/<FLOTA>/...   ← ACTIVAS tiene capa CORREDOR intermedia
  Drive_dump/<OTRA_CATEGORIA>/<FLOTA>/...     ← Resto: FLOTA directo

Produce:
  09_extraccion_masiva.csv    1 fila por flota
  09_extraccion_masiva.md     resumen por categoría + top hallazgos
"""
from __future__ import annotations

import csv
import email
import email.policy
import json
import re
import sys
import time
import unicodedata
import warnings
from collections import defaultdict
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    from openpyxl import load_workbook
except ImportError:
    print("Falta openpyxl. pip install openpyxl", file=sys.stderr)
    raise

ROOT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\Drive_dump")
OUT_CSV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\09_extraccion_masiva.csv")
OUT_MD = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\09_extraccion_masiva.md")

CATEGORIAS_ACTIVAS = {'ACTIVAS'}
CATEGORIAS_PLANAS = {
    'FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS',
    'FLOTAS HECHAS POR TITAN 2025-2026',
    'ESTUDIOS',
    'FLOTAS REHUSADAS',
}

COMERCIALES_TITAN = {'AGUSTIN', 'IKER', 'RAQUEL'}
COMERCIALES_MED = {'MIGUEL', 'ROBERTO', 'JAVIER', 'ANTONIO', 'ANTOÑITO'}
COMERCIALES_TODOS = COMERCIALES_TITAN | COMERCIALES_MED
COMERCIALES_ALT = {'ENRIC': 'ENRIC', 'ENRICK': 'ENRIC', 'SUSANA': 'SUSANA', 'GOYO': 'GOYO',
                   'COBIAN': 'COBIAN', 'MARES': 'MARES'}  # detectados en nombres, no en seed

CIF_RE = re.compile(r'\b([ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]|\d{8}[A-HJ-NP-TV-Z])\b')
ID_MMT_NEAR_RE = re.compile(r'(?:ID|PERCEPTOR|id|perceptor|CODIGO|CÓDIGO)[:\s]+(\d{5,8})')


def strip_acc(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def parse_nombre_flota(nombre_carpeta: str) -> dict:
    """
    Separa 'FLOTA - CORREDOR - COMERCIAL' en partes.
    Detecta comercial si matchea con lista conocida.
    """
    partes = [p.strip() for p in nombre_carpeta.split('-')]
    nombre = partes[0] if partes else nombre_carpeta
    corredor = partes[1] if len(partes) > 1 else ''
    comercial_raw = partes[2] if len(partes) > 2 else ''

    # Comercial: match con lista conocida (upper, sin acentos)
    comercial = ''
    for parte in partes[1:]:
        up = strip_acc(parte).upper().strip()
        if up in COMERCIALES_TODOS:
            comercial = up
            break
        if up in COMERCIALES_ALT:
            comercial = COMERCIALES_ALT[up]
            break
        # Casos "XX - YY - ZZ" donde ZZ es comercial
        for word in up.split():
            if word in COMERCIALES_TODOS:
                comercial = word
                break
            if word in COMERCIALES_ALT:
                comercial = COMERCIALES_ALT[word]
                break
        if comercial:
            break

    return {
        'nombre_limpio': nombre.strip(),
        'corredor_en_nombre': corredor.strip(),
        'comercial_en_nombre': comercial,
        'raw': nombre_carpeta,
    }


def parse_eml_rapido(path: Path) -> tuple[set, str]:
    """Devuelve (set de CIFs, texto_asunto)."""
    try:
        with open(path, 'rb') as f:
            msg = email.message_from_bytes(f.read(), policy=email.policy.default)
        subject = msg['subject'] or ''
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body += part.get_content()
                    except Exception:
                        pass
        else:
            try:
                body = msg.get_content()
            except Exception:
                body = ''
        text = (subject + '\n' + body).upper()
        cifs = set(CIF_RE.findall(text))
        return cifs, subject
    except Exception:
        return set(), ''


def parse_xlsx_rapido(path: Path, max_filas: int = 300) -> tuple[set, set]:
    """Devuelve (set de CIFs, set de IDs MMT encontrados)."""
    cifs = set()
    ids = set()
    try:
        wb = load_workbook(path, read_only=True, data_only=True)
        for sheet_name in wb.sheetnames[:5]:  # primeras 5 hojas
            if sheet_name.upper().startswith('HIDDEN'):
                continue
            ws = wb[sheet_name]
            for i, row in enumerate(ws.iter_rows(values_only=True, max_row=max_filas)):
                for cell in row:
                    if cell is None:
                        continue
                    s = str(cell).upper().strip()
                    for m in CIF_RE.findall(s):
                        cifs.add(m)
                    for m in ID_MMT_NEAR_RE.findall(s):
                        ids.add(m)
        wb.close()
    except Exception:
        pass
    return cifs, ids


def detectar_corredor(nombre_corredor_raw: str, nombre_flota: str) -> str:
    """Normaliza el corredor sacado del nombre."""
    if not nombre_corredor_raw:
        return ''
    # Quitar palabras que son comerciales
    tokens = nombre_corredor_raw.split()
    tokens = [t for t in tokens if strip_acc(t).upper() not in COMERCIALES_TODOS
              and strip_acc(t).upper() not in COMERCIALES_ALT]
    return ' '.join(tokens).strip()


def procesar_flota(ruta_flota: Path, categoria: str, corredor_capa: str = '') -> dict:
    """Procesa una carpeta de flota y extrae todo."""
    nombre_carpeta = ruta_flota.name
    info_nombre = parse_nombre_flota(nombre_carpeta)

    cifs_encontrados = set()
    ids_encontrados = set()
    n_eml = n_xlsx = n_otros = 0

    for f in ruta_flota.rglob('*'):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext == '.eml':
            cifs, _ = parse_eml_rapido(f)
            cifs_encontrados |= cifs
            n_eml += 1
        elif ext in ('.xlsx', '.xls'):
            cifs, ids = parse_xlsx_rapido(f)
            cifs_encontrados |= cifs
            ids_encontrados |= ids
            n_xlsx += 1
        else:
            n_otros += 1

    corredor_final = corredor_capa or detectar_corredor(info_nombre['corredor_en_nombre'], info_nombre['nombre_limpio'])

    return {
        'categoria': categoria,
        'nombre_flota': info_nombre['nombre_limpio'] or nombre_carpeta,
        'raw_carpeta': nombre_carpeta,
        'corredor_sugerido': corredor_final,
        'comercial_sugerido': info_nombre['comercial_en_nombre'],
        'cifs': sorted(cifs_encontrados),
        'ids_mmt': sorted(ids_encontrados),
        'n_eml': n_eml,
        'n_xlsx': n_xlsx,
        'ruta_local': str(ruta_flota),
    }


def main():
    print(f"ROOT: {ROOT}")
    if not ROOT.exists():
        print("[ERROR] no existe Drive_dump", file=sys.stderr)
        return 1

    flotas = []
    t0 = time.time()

    for cat_dir in ROOT.iterdir():
        if not cat_dir.is_dir():
            continue
        cat_name = cat_dir.name
        if cat_name in CATEGORIAS_ACTIVAS:
            # Dos niveles: corredor/flota
            for corredor_dir in cat_dir.iterdir():
                if not corredor_dir.is_dir():
                    continue
                corredor_capa = corredor_dir.name
                for flota_dir in corredor_dir.iterdir():
                    if not flota_dir.is_dir():
                        continue
                    r = procesar_flota(flota_dir, cat_name, corredor_capa=corredor_capa)
                    flotas.append(r)
                    if len(flotas) % 25 == 0:
                        print(f"  procesadas {len(flotas)} flotas ({time.time()-t0:.0f}s)", flush=True)
        elif cat_name in CATEGORIAS_PLANAS:
            for flota_dir in cat_dir.iterdir():
                if not flota_dir.is_dir():
                    continue
                r = procesar_flota(flota_dir, cat_name, corredor_capa='')
                flotas.append(r)
                if len(flotas) % 25 == 0:
                    print(f"  procesadas {len(flotas)} flotas ({time.time()-t0:.0f}s)", flush=True)

    elapsed = time.time() - t0
    print(f"\nTotal flotas procesadas: {len(flotas)} en {elapsed:.0f}s")

    # CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['CATEGORIA', 'FLOTA', 'RAW_CARPETA', 'CORREDOR_SUGERIDO', 'COMERCIAL_SUGERIDO',
                   'N_CIFS', 'CIFS', 'N_IDS_MMT', 'IDS_MMT', 'N_EML', 'N_XLSX'])
        for r in sorted(flotas, key=lambda x: (x['categoria'], x['nombre_flota'])):
            w.writerow([
                r['categoria'], r['nombre_flota'], r['raw_carpeta'],
                r['corredor_sugerido'], r['comercial_sugerido'],
                len(r['cifs']), ','.join(r['cifs']),
                len(r['ids_mmt']), ','.join(r['ids_mmt']),
                r['n_eml'], r['n_xlsx'],
            ])
    print(f"[OK] CSV -> {OUT_CSV}")

    # MD summary
    por_cat = defaultdict(list)
    for r in flotas:
        por_cat[r['categoria']].append(r)
    con_cif = sum(1 for r in flotas if r['cifs'])
    sin_cif = len(flotas) - con_cif
    con_comercial = sum(1 for r in flotas if r['comercial_sugerido'])

    md = []
    md.append("# Extracción masiva Drive — 18/11/2026\n\n")
    md.append(f"Procesadas **{len(flotas)} flotas** en {elapsed:.0f}s\n\n")
    md.append(f"| | Nº |\n|---|---:|\n")
    md.append(f"| Flotas con CIF detectado | **{con_cif}** |\n")
    md.append(f"| Flotas sin CIF detectado | **{sin_cif}** |\n")
    md.append(f"| Flotas con comercial detectado en nombre | **{con_comercial}** |\n\n")
    md.append("## Por categoría\n\n")
    md.append("| Categoría | Flotas | Con CIF | Con comercial |\n|---|---:|---:|---:|\n")
    for cat, lista in sorted(por_cat.items()):
        cc = sum(1 for r in lista if r['cifs'])
        cm = sum(1 for r in lista if r['comercial_sugerido'])
        md.append(f"| {cat} | {len(lista)} | {cc} | {cm} |\n")

    md.append("\n## Top flotas con más CIFs encontrados (candidatas a multi-tomador)\n\n")
    top_multi = sorted([r for r in flotas if len(r['cifs']) > 1], key=lambda x: -len(x['cifs']))[:15]
    for r in top_multi:
        md.append(f"- **{r['nombre_flota']}** ({r['categoria']}) — {len(r['cifs'])} CIFs: `{', '.join(r['cifs'][:8])}{'...' if len(r['cifs'])>8 else ''}`\n")

    md.append("\n## Flotas SIN CIF detectado (necesitan revisión manual)\n\n")
    for r in sorted([r for r in flotas if not r['cifs']], key=lambda x: (x['categoria'], x['nombre_flota']))[:50]:
        md.append(f"- [{r['categoria']}] {r['nombre_flota']}\n")
    sin = sum(1 for r in flotas if not r['cifs'])
    if sin > 50:
        md.append(f"\n... y {sin-50} más (ver CSV completo).\n")

    md.append("\n## Comerciales detectados en nombres de carpeta\n\n")
    por_com = defaultdict(int)
    for r in flotas:
        c = r['comercial_sugerido']
        if c:
            por_com[c] += 1
    for c, n in sorted(por_com.items(), key=lambda x: -x[1]):
        md.append(f"- **{c}**: {n} flotas\n")

    OUT_MD.write_text(''.join(md), encoding='utf-8')
    print(f"[OK] MD  -> {OUT_MD}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
