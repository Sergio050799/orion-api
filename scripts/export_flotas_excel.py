"""
Exporta la tabla flotas a un Excel para que el jefe lo rellene a mano.
Luego hay un script hermano (import_flotas_excel.py) que lo vuelve a subir.

Columnas pensadas para:
- Dejarle rellenar lo que falta (CIF, sucursal, actividad, nombre_comercial).
- Que el matching de vuelta sea seguro (ID_FLOTA invisible/bloqueado).
- Que vea contexto para decidir (num estudios, estado ultimo, corredor).

Uso:
    python scripts/export_flotas_excel.py
    python scripts/export_flotas_excel.py --out "C:/ruta/alternativa.xlsx"
"""
from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    print("[ERROR] falta openpyxl. Instala con: pip install openpyxl", file=sys.stderr)
    raise

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')
DEFAULT_OUT = Path.home() / "Downloads" / "flotas_orion_v5.xlsx"

# Estilos
HEADER_FILL = PatternFill(start_color="FF002F82", end_color="FF002F82", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFFFF", size=11)
READONLY_FILL = PatternFill(start_color="FFEFEFEF", end_color="FFEFEFEF", fill_type="solid")
READONLY_FONT = Font(color="FF666666", italic=True)
EDIT_FILL = PatternFill(start_color="FFFFFBEA", end_color="FFFFFBEA", fill_type="solid")
ORFANA_FILL = PatternFill(start_color="FFFFD1D1", end_color="FFFFD1D1", fill_type="solid")
DUP_FILL = PatternFill(start_color="FFFFE1A8", end_color="FFFFE1A8", fill_type="solid")

SUFIJOS = [
    'SOCIEDAD LIMITADA', 'SOCIEDAD ANONIMA', 'SOCIEDAD COOPERATIVA',
    'S.L.U.', 'SLU', 'S.A.U.', 'SAU', 'S.COOP.', 'SCOOP', 'S.COOP',
    'S.L.', 'SL', 'S.A.', 'SA', 'S.C.', 'SC', 'C.B.', 'CB', 'S.R.L.', 'SRL',
]


def _norm(s: str) -> str:
    if not s:
        return ''
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.upper()
    s = re.sub(r'[.,;:\-_/\\]', ' ', s)
    for suf in sorted(SUFIJOS, key=len, reverse=True):
        s = re.sub(r'\b' + re.escape(suf) + r'\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# Columnas: (titulo, campo, ancho, editable, descripcion)
COLUMNAS = [
    ("ID_FLOTA",         "id",                12, False, "NO TOCAR (matching)"),
    ("FLOTA",            "nombre",            42, True,  "Razon social / tomador"),
    ("CIF",              "cif",               14, True,  "9 digitos, mayusculas"),
    ("NOMBRE_COMERCIAL", "nombre_comercial",  28, True,  "Nombre corto visible"),
    ("ACTIVIDAD",        "actividad",         34, True,  "Transporte publico, etc."),
    ("CORREDOR",         "corredor_nombre",   26, True,  "Nombre del corredor"),
    ("SUCURSAL",         "sucursal",          14, True,  "TITAN / MEDIACION / vacio"),
    ("ESTADO",           "estado_ultimo",     12, False, "estado del estudio reciente"),
    ("Nº_ESTUDIOS",      "n_estudios",         8, False, "info"),
    ("Nº_EMISIONES",     "n_emisiones",        8, False, "info"),
    ("ES_HISTORICA",     "es_historica",      10, True,  "1 si pre-ORION, 0 si no"),
    ("NOTAS",            "notas",             36, True,  "Libre"),
]


def cargar_flotas(conn: sqlite3.Connection) -> list[dict]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT
            f.id,
            f.cif,
            f.nombre,
            f.nombre_comercial,
            f.actividad,
            f.corredor_id,
            f.sucursal,
            f.es_historica,
            COALESCE(co.nombre, '') AS corredor_nombre,
            (SELECT COUNT(*) FROM estudios  e WHERE e.flota_id = f.id) AS n_estudios,
            (SELECT COUNT(*) FROM emisiones em WHERE em.flota_id = f.id) AS n_emisiones,
            (
                SELECT e2.estado FROM estudios e2
                WHERE e2.flota_id = f.id
                ORDER BY e2.actualizado_en DESC LIMIT 1
            ) AS estado_ultimo
        FROM flotas f
        LEFT JOIN corredores co ON co.id = f.corredor_id
        ORDER BY f.nombre COLLATE NOCASE
    """).fetchall()
    out = []
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        d['notas'] = ''
        out.append(d)
    return out


def generar_excel(flotas: list[dict], out_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Flotas ORION V5"

    # Fila 1: cabeceras
    for idx, (titulo, _, ancho, editable, _) in enumerate(COLUMNAS, start=1):
        col = get_column_letter(idx)
        cell = ws.cell(row=1, column=idx, value=titulo)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[col].width = ancho

    # Fila 2: hint de edicion
    for idx, (_, _, _, editable, desc) in enumerate(COLUMNAS, start=1):
        cell = ws.cell(row=2, column=idx, value=desc)
        cell.font = READONLY_FONT
        cell.alignment = Alignment(horizontal="center")
        if not editable:
            cell.fill = READONLY_FILL
        else:
            cell.fill = EDIT_FILL

    # Grupos de duplicados para marcar en fila
    grupos = defaultdict(list)
    for f in flotas:
        n = _norm(f.get('nombre') or '')
        if n:
            grupos[n].append(f['id'])
    ids_duplicados = {i for ids in grupos.values() if len(ids) > 1 for i in ids}

    # Datos (fila 3 en adelante)
    for i, flota in enumerate(flotas, start=3):
        es_huerfana = not (flota.get('cif') or '').strip()
        es_duplicada = flota['id'] in ids_duplicados
        for idx, (_, campo, _, editable, _) in enumerate(COLUMNAS, start=1):
            val = flota.get(campo, '')
            if val is None:
                val = ''
            cell = ws.cell(row=i, column=idx, value=val)
            if not editable:
                cell.fill = READONLY_FILL
                cell.font = Font(color="FF666666")
            # Resaltado en la columna FLOTA (idx 2) y CIF (idx 3)
            if idx in (2, 3):
                if es_duplicada:
                    cell.fill = DUP_FILL
                elif es_huerfana and idx == 3:
                    cell.fill = ORFANA_FILL

    # Freeze header + autofiltro
    ws.freeze_panes = "A3"
    ws.auto_filter.ref = ws.dimensions

    # Hoja Duplicados
    ws_dup = wb.create_sheet("Duplicados")
    for idx, h in enumerate(["GRUPO", "ID_FLOTA", "FLOTA", "CIF", "ESTADO_ULT", "Nº_ESTUDIOS", "SUCURSAL", "DECISION"], 1):
        c = ws_dup.cell(row=1, column=idx, value=h)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = Alignment(horizontal="center")
    anchos = [28, 14, 42, 14, 14, 10, 14, 24]
    for i, w in enumerate(anchos, 1):
        ws_dup.column_dimensions[get_column_letter(i)].width = w

    row_n = 2
    for norm, ids in sorted(grupos.items()):
        if len(ids) < 2:
            continue
        for fid in ids:
            f = next(x for x in flotas if x['id'] == fid)
            vals = [
                norm,
                f['id'],
                f['nombre'],
                f.get('cif') or '',
                f.get('estado_ultimo') or '',
                f.get('n_estudios') or 0,
                f.get('sucursal') or '',
                '',
            ]
            for idx, v in enumerate(vals, 1):
                c = ws_dup.cell(row=row_n, column=idx, value=v)
                c.fill = DUP_FILL if idx <= 3 else PatternFill()
            row_n += 1
    ws_dup.freeze_panes = "A2"
    ws_dup.auto_filter.ref = ws_dup.dimensions

    # Hoja 2: instrucciones
    ws2 = wb.create_sheet("Instrucciones")
    instrucciones = [
        ("Como rellenar este Excel", True),
        ("", False),
        ("1. NO tocar la columna ID_FLOTA (es el identificador).", False),
        ("2. Columnas en gris = informacion, no las modifiques.", False),
        ("3. Columnas en amarillo claro = editables.", False),
        ("4. CIF: 9 digitos sin guiones, mayusculas (A12345678).", False),
        ("5. SUCURSAL: TITAN, MEDIACION o dejar vacio.", False),
        ("6. ES_HISTORICA: 1 si es pre-ORION, 0 si es nueva.", False),
        ("7. Cuando acabes, me lo pasas y hago el upsert por ID_FLOTA.", False),
        ("", False),
        (f"Total flotas: {len(flotas)}", True),
    ]
    for i, (txt, bold) in enumerate(instrucciones, start=1):
        c = ws2.cell(row=i, column=1, value=txt)
        if bold:
            c.font = Font(bold=True, size=12)
    ws2.column_dimensions['A'].width = 70

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(DEFAULT_OUT))
    args = ap.parse_args()

    print(f"BD: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] No existe la BD en {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        flotas = cargar_flotas(conn)
        out = Path(args.out)
        generar_excel(flotas, out)
        print(f"[OK] {len(flotas)} flotas exportadas -> {out}")
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
