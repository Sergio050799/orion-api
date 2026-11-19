"""
Analiza el inventario_drive.json generado por rclone lsjson -R.

Produce:
  - resumen por categoría (ACTIVAS, SOLICITADAS, ...)
  - por flota (nivel 3): nº archivos, tipos, tamaño total, duplicados entre categorías
  - informe markdown en C:\\Users\\garci\\Downloads\\inventario_drive.md
  - CSV por flota con columnas útiles para merge
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

INV = Path(r"C:\Users\garci\Downloads\inventario_drive.json")
OUT_MD = Path(r"C:\Users\garci\Downloads\inventario_drive.md")
OUT_CSV = Path(r"C:\Users\garci\Downloads\inventario_flotas_drive.csv")

CATEGORIAS = {
    "FLOTAS/ACTIVAS": "ACTIVAS",
    "FLOTAS/FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS": "SOLICITADAS_NO_CONTR",
    "FLOTAS/FLOTAS HECHAS POR TITAN 2025-2026": "TITAN_2025_2026",
    "FLOTAS/ESTUDIOS": "ESTUDIOS",
    "FLOTAS/FLOTAS REHUSADAS": "REHUSADAS",
}

SUFIJOS = [
    'SOCIEDAD LIMITADA', 'SOCIEDAD ANONIMA', 'S.L.U.', 'SLU', 'S.A.U.', 'SAU',
    'S.L.', 'SL', 'S.A.', 'SA', 'S.C.', 'SC',
]


def norm(s: str) -> str:
    if not s:
        return ''
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    s = re.sub(r'[.,;:\-_/\\()]', ' ', s)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def clasificar(path: str) -> tuple[str, str, str]:
    """Devuelve (categoria, flota_name, path_relativo_dentro_flota)"""
    for prefix, cat in CATEGORIAS.items():
        if path.startswith(prefix + "/"):
            rest = path[len(prefix) + 1:]
            parts = rest.split("/", 1)
            flota = parts[0]
            sub = parts[1] if len(parts) > 1 else ""
            return cat, flota, sub
    return "", "", path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=str(INV))
    args = ap.parse_args()

    p = Path(args.input)
    if not p.exists():
        print(f"[ERROR] no existe {p}", file=sys.stderr)
        return 1

    with open(p, 'r', encoding='utf-8') as f:
        items = json.load(f)

    print(f"Items totales en JSON: {len(items)}")

    # Por flota: {(categoria, flota_name): {dict con stats}}
    flotas: dict[tuple[str, str], dict] = defaultdict(lambda: {
        'n_archivos': 0, 'n_subcarpetas': 0, 'bytes_total': 0,
        'extensiones': defaultdict(int),
        'ids_drive': '',
    })
    sin_clasificar = 0
    fuera_flotas = []

    for it in items:
        path = it.get('Path', '')
        is_dir = it.get('IsDir', False)
        size = int(it.get('Size', 0) or 0)
        name = it.get('Name', '')

        cat, flota, sub = clasificar(path)
        if not cat:
            if not path.startswith("FLOTAS/") and "/" not in path:
                fuera_flotas.append(path)
            sin_clasificar += 1
            continue

        key = (cat, flota)
        if sub == "":
            # Es la carpeta flota misma
            if is_dir:
                flotas[key]['ids_drive'] = it.get('ID', '')
            continue

        if is_dir:
            flotas[key]['n_subcarpetas'] += 1
        else:
            flotas[key]['n_archivos'] += 1
            flotas[key]['bytes_total'] += size
            ext = Path(name).suffix.lower().lstrip('.')
            flotas[key]['extensiones'][ext or '(sin)'] += 1

    # Por categoría: conteo flotas + archivos
    por_cat = defaultdict(lambda: {'n_flotas': 0, 'n_archivos': 0, 'bytes_total': 0, 'ext': defaultdict(int)})
    for (cat, flota), st in flotas.items():
        por_cat[cat]['n_flotas'] += 1
        por_cat[cat]['n_archivos'] += st['n_archivos']
        por_cat[cat]['bytes_total'] += st['bytes_total']
        for e, n in st['extensiones'].items():
            por_cat[cat]['ext'][e] += n

    # Duplicados por nombre normalizado entre categorías
    por_nombre = defaultdict(list)
    for (cat, flota) in flotas.keys():
        por_nombre[norm(flota)].append((cat, flota))
    duplicados = {k: v for k, v in por_nombre.items() if len(v) > 1 and k}

    # Imprimir resumen
    print()
    print("=" * 70)
    print("RESUMEN POR CATEGORÍA")
    print("=" * 70)
    total_flotas = 0
    for cat in CATEGORIAS.values():
        st = por_cat.get(cat, {})
        print(f"\n[{cat}]")
        print(f"  Flotas:     {st.get('n_flotas', 0)}")
        print(f"  Archivos:   {st.get('n_archivos', 0)}")
        print(f"  Tamaño:     {st.get('bytes_total', 0) / 1024 / 1024:.1f} MB")
        top_ext = sorted(st.get('ext', {}).items(), key=lambda x: -x[1])[:6]
        if top_ext:
            print(f"  Top ext:    {', '.join(f'{e}:{n}' for e, n in top_ext)}")
        total_flotas += st.get('n_flotas', 0)
    print()
    print(f"TOTAL FLOTAS: {total_flotas}")
    print(f"TOTAL ARCHIVOS: {sum(c['n_archivos'] for c in por_cat.values())}")
    print(f"TOTAL BYTES: {sum(c['bytes_total'] for c in por_cat.values()) / 1024 / 1024 / 1024:.2f} GB")
    print()
    print(f"Duplicados entre categorías: {len(duplicados)}")
    for k, v in list(duplicados.items())[:10]:
        print(f"  '{k}':")
        for cat, flota in v:
            print(f"      [{cat}] {flota}")

    # Exportar CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['CATEGORIA', 'FLOTA', 'FLOTA_NORMALIZADA', 'N_ARCHIVOS', 'N_SUBCARPETAS', 'MB', 'EXTENSIONES', 'ID_DRIVE'])
        for (cat, flota), st in sorted(flotas.items()):
            exts = ','.join(f'{e}:{n}' for e, n in sorted(st['extensiones'].items(), key=lambda x: -x[1]))
            w.writerow([
                cat, flota, norm(flota),
                st['n_archivos'], st['n_subcarpetas'],
                round(st['bytes_total'] / 1024 / 1024, 2),
                exts,
                st['ids_drive'],
            ])
    print(f"\n[OK] CSV -> {OUT_CSV}")

    # Markdown
    md = []
    md.append("# Inventario Drive FLOTAS-17-11-2026\n")
    md.append(f"Total flotas: **{total_flotas}**  |  archivos: **{sum(c['n_archivos'] for c in por_cat.values())}**  |  tamaño: **{sum(c['bytes_total'] for c in por_cat.values()) / 1024 / 1024 / 1024:.2f} GB**\n")
    md.append("\n## Por categoría\n")
    md.append("| Categoría | Flotas | Archivos | Tamaño (MB) | Ext top |\n")
    md.append("|---|---:|---:|---:|---|\n")
    for cat in CATEGORIAS.values():
        st = por_cat.get(cat, {})
        top_ext = sorted(st.get('ext', {}).items(), key=lambda x: -x[1])[:5]
        md.append(f"| {cat} | {st.get('n_flotas', 0)} | {st.get('n_archivos', 0)} | {st.get('bytes_total', 0) / 1024 / 1024:.1f} | {', '.join(f'`{e}`:{n}' for e, n in top_ext)} |\n")

    md.append("\n## Duplicados entre categorías\n")
    if duplicados:
        for k, v in sorted(duplicados.items()):
            md.append(f"\n- **{k}**\n")
            for cat, flota in v:
                md.append(f"  - [{cat}] {flota}\n")
    else:
        md.append("_Ninguno detectado por nombre normalizado._\n")

    md.append("\n## Flotas por categoría\n")
    for cat in CATEGORIAS.values():
        md.append(f"\n### {cat}\n")
        for (c, flota), st in sorted(flotas.items()):
            if c != cat:
                continue
            exts = ', '.join(f'`{e}`:{n}' for e, n in sorted(st['extensiones'].items(), key=lambda x: -x[1])[:4])
            md.append(f"- **{flota}** — {st['n_archivos']} archivos ({st['bytes_total']/1024/1024:.1f} MB) · {exts}\n")

    OUT_MD.write_text(''.join(md), encoding='utf-8')
    print(f"[OK] MD  -> {OUT_MD}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
