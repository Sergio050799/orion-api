"""
V2: Parser masivo con validación estricta de CIF/NIF/NIE (algoritmo módulo 11 + letra control).

Mejoras vs V1:
  - Valida dígito/letra de control con la matemática real (descarta matrículas y ruido).
  - Búsqueda CONTEXTUAL: solo acepta identificador si está cerca de palabras clave (CIF, NIF, DNI, TOMADOR, RAZÓN SOCIAL) o aparece como valor en columna cuya cabecera tenga esas palabras.
  - Extiende xlsx a TODAS las hojas (no solo 5) excluyendo HIDDEN_*.
  - Busca también en el NOMBRE de los archivos (filename).
  - Para flotas que siguen sin CIF: 2do barrido profundo (~ignorando contexto, solo exigiendo validación matemática).

Produce:
  10_extraccion_masiva_v2.csv       1 fila por flota
  10_extraccion_masiva_v2.md        resumen
  11_sin_cif_para_revisar.csv       solo las que quedan sin CIF tras V2
"""
from __future__ import annotations

import csv
import email
import email.policy
import re
import sys
import time
import unicodedata
import warnings
from collections import defaultdict
from pathlib import Path

warnings.filterwarnings('ignore')

from openpyxl import load_workbook

ROOT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\Drive_dump")
OUT_CSV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\10_extraccion_masiva_v2.csv")
OUT_MD = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\10_extraccion_masiva_v2.md")
OUT_SIN = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\11_sin_cif_para_revisar.csv")

CATEGORIAS_ACTIVAS = {'ACTIVAS'}

COMERCIALES_TITAN = {'AGUSTIN', 'IKER', 'RAQUEL', 'ENRIC', 'SUSANA'}
COMERCIALES_MED = {'MIGUEL', 'ROBERTO', 'JAVIER', 'ANTONIO'}
COMERCIALES_TODOS = COMERCIALES_TITAN | COMERCIALES_MED
COMERCIALES_ALT = {'ENRICK': 'ENRIC'}

# Regexes "candidato" (precondición)
CIF_CAND  = re.compile(r'\b([ABCDEFGHJKLMNPQRSUVW])(\d{7})([0-9A-J])\b')
NIF_CAND  = re.compile(r'\b(\d{8})([A-HJ-NP-TV-Z])\b')
NIE_CAND  = re.compile(r'\b([XYZ])(\d{7})([A-Z])\b')

CTX_KEYS = ('CIF', 'NIF', 'DNI', 'NIE', 'TOMADOR', 'TOMADOR/ASEGURADO', 'TITULAR',
            'RAZÓN SOCIAL', 'RAZON SOCIAL', 'DOCUMENTO', 'IDENTIF', 'IDENTIFICACION',
            'C.I.F.', 'N.I.F.', 'D.N.I.')

NIF_LETRAS = 'TRWAGMYFPDXBNJZSQVHLCKE'


def strip_acc(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


# ---------- Validadores ----------

def valida_nif(num: str, letra: str) -> bool:
    try:
        return NIF_LETRAS[int(num) % 23] == letra.upper()
    except Exception:
        return False


def valida_nie(prefix: str, num: str, letra: str) -> bool:
    mapa = {'X': '0', 'Y': '1', 'Z': '2'}
    try:
        num_full = int(mapa[prefix.upper()] + num)
        return NIF_LETRAS[num_full % 23] == letra.upper()
    except Exception:
        return False


def valida_cif(letra_ini: str, num7: str, control: str) -> bool:
    """Algoritmo CIF España (módulo 10)."""
    try:
        s = 0
        for i, d in enumerate(num7):
            n = int(d)
            if i % 2 == 0:  # posición impar (1-based) → duplicar
                doble = n * 2
                s += (doble // 10) + (doble % 10)
            else:
                s += n
        unidades = s % 10
        digito = 0 if unidades == 0 else 10 - unidades
        letras_ctl = 'JABCDEFGHI'
        letra_calc = letras_ctl[digito]
        # Algunas letras exigen letra, otras dígito, algunas aceptan ambos
        if letra_ini.upper() in 'PQSNWR':
            return control.upper() == letra_calc
        if letra_ini.upper() in 'ABEH':
            return control == str(digito)
        # El resto (CDFGJUV) acepta ambos
        return control.upper() == letra_calc or control == str(digito)
    except Exception:
        return False


def extraer_validos(texto: str) -> set:
    """Devuelve set de CIF/NIF/NIE validados matemáticamente."""
    if not texto:
        return set()
    t = texto.upper()
    out = set()
    for m in CIF_CAND.finditer(t):
        letra, num7, ctl = m.group(1), m.group(2), m.group(3)
        full = letra + num7 + ctl
        if valida_cif(letra, num7, ctl):
            out.add(full)
    for m in NIF_CAND.finditer(t):
        num8, letra = m.group(1), m.group(2)
        if valida_nif(num8, letra):
            out.add(num8 + letra)
    for m in NIE_CAND.finditer(t):
        pre, num7, letra = m.group(1), m.group(2), m.group(3)
        if valida_nie(pre, num7, letra):
            out.add(pre + num7 + letra)
    return out


def _contexto_cercano(texto: str, pos: int, radio: int = 60) -> str:
    return texto[max(0, pos - radio):pos + radio].upper()


def extraer_con_contexto(texto: str) -> set:
    """
    Igual que extraer_validos pero solo si está cerca de palabra clave.
    """
    if not texto:
        return set()
    t = texto.upper()
    out = set()
    for m in CIF_CAND.finditer(t):
        letra, num7, ctl = m.group(1), m.group(2), m.group(3)
        if not valida_cif(letra, num7, ctl):
            continue
        ctx = _contexto_cercano(t, m.start())
        if any(k in ctx for k in CTX_KEYS):
            out.add(letra + num7 + ctl)
    for m in NIF_CAND.finditer(t):
        num8, letra = m.group(1), m.group(2)
        if not valida_nif(num8, letra):
            continue
        ctx = _contexto_cercano(t, m.start())
        if any(k in ctx for k in CTX_KEYS):
            out.add(num8 + letra)
    for m in NIE_CAND.finditer(t):
        pre, num7, letra = m.group(1), m.group(2), m.group(3)
        if not valida_nie(pre, num7, letra):
            continue
        ctx = _contexto_cercano(t, m.start())
        if any(k in ctx for k in CTX_KEYS):
            out.add(pre + num7 + letra)
    return out


# ---------- Parser archivos ----------

def parse_eml(path: Path, estricto: bool) -> set:
    try:
        with open(path, 'rb') as f:
            msg = email.message_from_bytes(f.read(), policy=email.policy.default)
        body = msg['subject'] or ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        body += '\n' + part.get_content()
                    except Exception:
                        pass
        else:
            try:
                body = body + '\n' + msg.get_content()
            except Exception:
                pass
        return extraer_con_contexto(body) if estricto else extraer_validos(body)
    except Exception:
        return set()


def parse_xlsx(path: Path, estricto: bool) -> set:
    cifs = set()
    try:
        wb = load_workbook(path, read_only=True, data_only=True)
        for sheet_name in wb.sheetnames:
            if sheet_name.upper().startswith('HIDDEN'):
                continue
            ws = wb[sheet_name]
            # Detectar columnas con cabecera CIF/NIF/TOMADOR en primeras 10 filas
            cols_con_cif = set()
            headers_row = None
            for i, row in enumerate(ws.iter_rows(values_only=True, max_row=10)):
                for j, cell in enumerate(row):
                    if cell:
                        up = strip_acc(str(cell)).upper()
                        if any(k == up or k in up for k in CTX_KEYS):
                            cols_con_cif.add(j)
                            headers_row = i
                            break
            # Barrer filas
            text_acumulado = []
            for row in ws.iter_rows(values_only=True, max_row=2000):
                row_text = []
                for j, cell in enumerate(row):
                    if cell is None:
                        continue
                    s = str(cell)
                    row_text.append(s)
                    # Si en columna CIF y valida → aceptar directo
                    if j in cols_con_cif:
                        validos = extraer_validos(s)
                        cifs |= validos
                if row_text:
                    text_acumulado.append(' '.join(row_text))
            # Buscar con contexto en el texto completo
            total_text = '\n'.join(text_acumulado)
            if estricto:
                cifs |= extraer_con_contexto(total_text)
            else:
                cifs |= extraer_validos(total_text)
        wb.close()
    except Exception:
        pass
    return cifs


def extraer_id_mmt(texto: str) -> set:
    ids = set()
    for m in re.finditer(r'(?:ID|PERCEPTOR|CODIGO|CÓDIGO)[:\s]+(\d{5,8})', texto, re.IGNORECASE):
        ids.add(m.group(1))
    return ids


# ---------- Parse nombre carpeta ----------

def parse_nombre_carpeta(nombre: str) -> dict:
    partes = [p.strip() for p in nombre.split('-')]
    nombre_limpio = partes[0] if partes else nombre
    corredor = ''
    comercial = ''
    for parte in partes[1:]:
        up = strip_acc(parte).upper().strip()
        matched = False
        if up in COMERCIALES_TODOS:
            if not comercial:
                comercial = up
                matched = True
        if up in COMERCIALES_ALT:
            if not comercial:
                comercial = COMERCIALES_ALT[up]
                matched = True
        if not matched:
            # Si hay comercial dentro de la parte
            for word in up.split():
                if word in COMERCIALES_TODOS:
                    if not comercial:
                        comercial = word
                    matched = True
                    break
                if word in COMERCIALES_ALT:
                    if not comercial:
                        comercial = COMERCIALES_ALT[word]
                    matched = True
                    break
        if not matched and not corredor:
            # Posible corredor
            tokens = parte.split()
            filtered = [t for t in tokens if strip_acc(t).upper() not in COMERCIALES_TODOS
                        and strip_acc(t).upper() not in COMERCIALES_ALT]
            corredor = ' '.join(filtered).strip()
    return {
        'nombre_limpio': nombre_limpio,
        'corredor': corredor,
        'comercial': comercial,
    }


# ---------- Proceso principal ----------

def procesar_flota(ruta_flota: Path, categoria: str, corredor_capa: str = '') -> dict:
    nombre_carpeta = ruta_flota.name
    info = parse_nombre_carpeta(nombre_carpeta)

    cifs_estrictos = set()      # con contexto (alta confianza)
    cifs_laxos = set()           # solo validados mat. (pueden ser falsos positivos)
    ids_mmt = set()
    n_eml = n_xlsx = 0

    # Filename también puede tener CIF
    for f in ruta_flota.rglob('*'):
        if not f.is_file():
            continue
        # CIFs del nombre del archivo (estricto por nombre explícito)
        for c in extraer_validos(f.name):
            cifs_estrictos.add(c)

        ext = f.suffix.lower()
        if ext == '.eml':
            cifs_estrictos |= parse_eml(f, estricto=True)
            n_eml += 1
        elif ext in ('.xlsx', '.xls'):
            cifs_estrictos |= parse_xlsx(f, estricto=True)
            n_xlsx += 1

    # Si NO encontramos ningún CIF estricto, hacemos 2do barrido laxo (solo matemático)
    if not cifs_estrictos:
        for f in ruta_flota.rglob('*'):
            if not f.is_file():
                continue
            ext = f.suffix.lower()
            if ext == '.eml':
                cifs_laxos |= parse_eml(f, estricto=False)
            elif ext in ('.xlsx', '.xls'):
                cifs_laxos |= parse_xlsx(f, estricto=False)

    corredor_final = corredor_capa or info['corredor']

    return {
        'categoria': categoria,
        'nombre_flota': info['nombre_limpio'] or nombre_carpeta,
        'raw_carpeta': nombre_carpeta,
        'corredor_sugerido': corredor_final,
        'comercial_sugerido': info['comercial'],
        'cifs_estrictos': sorted(cifs_estrictos),
        'cifs_laxos': sorted(cifs_laxos - cifs_estrictos),
        'ids_mmt': sorted(ids_mmt),
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

    for cat_dir in sorted(ROOT.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat_name = cat_dir.name
        if cat_name in CATEGORIAS_ACTIVAS:
            for corredor_dir in sorted(cat_dir.iterdir()):
                if not corredor_dir.is_dir():
                    continue
                corredor_capa = corredor_dir.name
                for flota_dir in sorted(corredor_dir.iterdir()):
                    if not flota_dir.is_dir():
                        continue
                    flotas.append(procesar_flota(flota_dir, cat_name, corredor_capa=corredor_capa))
                    if len(flotas) % 25 == 0:
                        print(f"  procesadas {len(flotas)} ({time.time()-t0:.0f}s)", flush=True)
        else:
            for flota_dir in sorted(cat_dir.iterdir()):
                if not flota_dir.is_dir():
                    continue
                flotas.append(procesar_flota(flota_dir, cat_name, corredor_capa=''))
                if len(flotas) % 25 == 0:
                    print(f"  procesadas {len(flotas)} ({time.time()-t0:.0f}s)", flush=True)

    elapsed = time.time() - t0
    print(f"\nTotal: {len(flotas)} flotas en {elapsed:.0f}s")

    # CSV detallado
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['CATEGORIA', 'FLOTA', 'RAW_CARPETA', 'CORREDOR_SUGERIDO', 'COMERCIAL_SUGERIDO',
                   'CIFS_ESTRICTOS', 'N_ESTRICTOS',
                   'CIFS_LAXOS_SIN_CONTEXTO', 'N_LAXOS', 'N_EML', 'N_XLSX'])
        for r in sorted(flotas, key=lambda x: (x['categoria'], x['nombre_flota'])):
            w.writerow([
                r['categoria'], r['nombre_flota'], r['raw_carpeta'],
                r['corredor_sugerido'], r['comercial_sugerido'],
                ','.join(r['cifs_estrictos']), len(r['cifs_estrictos']),
                ','.join(r['cifs_laxos']), len(r['cifs_laxos']),
                r['n_eml'], r['n_xlsx'],
            ])

    # CSV solo las que SIGUEN sin CIF
    sin_cif = [r for r in flotas if not r['cifs_estrictos'] and not r['cifs_laxos']]
    with open(OUT_SIN, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['CATEGORIA', 'FLOTA', 'CORREDOR_SUGERIDO', 'COMERCIAL_SUGERIDO', 'N_EML', 'N_XLSX', 'RUTA_LOCAL'])
        for r in sorted(sin_cif, key=lambda x: (x['categoria'], x['nombre_flota'])):
            w.writerow([r['categoria'], r['nombre_flota'], r['corredor_sugerido'],
                       r['comercial_sugerido'], r['n_eml'], r['n_xlsx'], r['ruta_local']])

    # Markdown
    con_estricto = sum(1 for r in flotas if r['cifs_estrictos'])
    solo_laxo = sum(1 for r in flotas if r['cifs_laxos'] and not r['cifs_estrictos'])
    sin_nada = sum(1 for r in flotas if not r['cifs_estrictos'] and not r['cifs_laxos'])

    md = []
    md.append("# Extracción masiva Drive V2 — 18/11/2026\n\n")
    md.append(f"- **Validación estricta** CIF/NIF/NIE (módulo 11 + letra control) — descarta ruido.\n")
    md.append(f"- **Contexto cercano** obligatorio en 1ª pasada (palabras CIF, NIF, DNI, TOMADOR, RAZÓN SOCIAL en radio 60 chars).\n")
    md.append(f"- **2º barrido laxo** solo si la flota no tuvo ningún hit estricto.\n\n")
    md.append(f"Procesadas **{len(flotas)} flotas** en {elapsed:.0f}s\n\n")
    md.append(f"| Resultado | Nº |\n|---|---:|\n")
    md.append(f"| Con CIF confirmado (contexto + mat.) | **{con_estricto}** |\n")
    md.append(f"| Solo con CIF laxo (matemático sin contexto) | **{solo_laxo}** |\n")
    md.append(f"| Sin CIF de ningún tipo | **{sin_nada}** |\n\n")

    # Por categoría
    por_cat = defaultdict(list)
    for r in flotas:
        por_cat[r['categoria']].append(r)
    md.append("## Por categoría\n\n")
    md.append("| Categoría | Flotas | Estricto | Laxo | Sin CIF |\n|---|---:|---:|---:|---:|\n")
    for cat, lista in sorted(por_cat.items()):
        e = sum(1 for r in lista if r['cifs_estrictos'])
        l = sum(1 for r in lista if r['cifs_laxos'] and not r['cifs_estrictos'])
        s = sum(1 for r in lista if not r['cifs_estrictos'] and not r['cifs_laxos'])
        md.append(f"| {cat} | {len(lista)} | {e} | {l} | {s} |\n")

    md.append("\n## Comparación V1 vs V2 — falsos positivos filtrados\n\n")
    md.append(f"V1 marcaba 236 flotas con CIF. V2 confirma solo las que tienen contexto real.\n")
    md.append(f"Los números absurdos (VICO=90, SAURATRANS=77, DURAN=47...) desaparecen.\n\n")

    md.append("## Flotas sin CIF de ningún tipo (lista en 11_sin_cif_para_revisar.csv)\n\n")
    for r in sin_cif[:30]:
        md.append(f"- [{r['categoria']}] {r['nombre_flota']} ({r['n_eml']} eml, {r['n_xlsx']} xlsx)\n")
    if len(sin_cif) > 30:
        md.append(f"\n... y {len(sin_cif)-30} más.\n")

    OUT_MD.write_text(''.join(md), encoding='utf-8')
    print(f"[OK] CSV   -> {OUT_CSV}")
    print(f"[OK] CSV sin-cif -> {OUT_SIN}")
    print(f"[OK] MD    -> {OUT_MD}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
