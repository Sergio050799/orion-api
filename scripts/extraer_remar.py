"""
Extrae CIFs e identificadores de los correos+xlsx de REMAR.
Objetivo: descubrir cuántas sub-flotas (empresas distintas) componen REMAR.
"""
from __future__ import annotations

import email
import email.policy
import re
from pathlib import Path

from openpyxl import load_workbook

CARPETA = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\REMAR_correos")
OUT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\08_remar_sub_flotas.md")

CIF_RE = re.compile(r'\b([ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]|\d{8}[A-HJ-NP-TV-Z])\b')


def parse_eml(path: Path) -> dict:
    try:
        with open(path, 'rb') as f:
            msg = email.message_from_bytes(f.read(), policy=email.policy.default)
        subject = msg['subject'] or ''
        from_ = msg['from'] or ''
        to_ = msg['to'] or ''
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
        return {'path': path.name, 'subject': subject, 'from': from_, 'to': to_, 'body': body}
    except Exception as e:
        return {'path': path.name, 'error': str(e)}


def parse_xlsx(path: Path) -> dict:
    out = {'path': path.name, 'hojas': [], 'cifs': set(), 'tomadores': set(), 'texto_cabeceras': []}
    try:
        wb = load_workbook(path, read_only=True, data_only=True)
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            out['hojas'].append(sheet_name)
            # Buscar cabeceras tomador/cif en primeras 5 filas
            rows_iter = ws.iter_rows(values_only=True, max_row=200)
            headers = None
            header_row_idx = 0
            for i, row in enumerate(rows_iter):
                row_str = [str(c) if c else '' for c in row]
                # detectar cabecera
                if any(('CIF' in c.upper() or 'TOMADOR' in c.upper() or 'MATRICULA' in c.upper() or 'MATRÍCULA' in c.upper() or 'RAZ' in c.upper() or 'NIF' in c.upper()) for c in row_str):
                    headers = row_str
                    header_row_idx = i
                    out['texto_cabeceras'].append(f'{sheet_name}: {headers}')
                    break
                # buscar cifs en cualquier fila
                for cell in row_str:
                    for m in CIF_RE.findall(cell.upper()):
                        out['cifs'].add(m)
            # Si hay cabecera, extraer tomador por fila
            if headers:
                cif_col = next((i for i, h in enumerate(headers) if 'CIF' in h.upper() or 'NIF' in h.upper()), None)
                tom_col = next((i for i, h in enumerate(headers) if 'TOMADOR' in h.upper() or 'RAZ' in h.upper() or 'TITULAR' in h.upper() or 'NOMBRE' in h.upper()), None)
                if cif_col is not None or tom_col is not None:
                    for row in ws.iter_rows(min_row=header_row_idx + 2, max_row=header_row_idx + 300, values_only=True):
                        cif_val = str(row[cif_col]) if cif_col is not None and cif_col < len(row) and row[cif_col] else ''
                        tom_val = str(row[tom_col]) if tom_col is not None and tom_col < len(row) and row[tom_col] else ''
                        if cif_val.strip():
                            m = CIF_RE.search(cif_val.upper().strip())
                            if m:
                                out['cifs'].add(m.group(1))
                        if tom_val.strip() and len(tom_val) > 3:
                            out['tomadores'].add(tom_val.strip())
    except Exception as e:
        out['error'] = str(e)
    return out


def main():
    print(f"Analizando REMAR en {CARPETA}")

    emls = list(CARPETA.rglob('*.eml'))
    xlsxs = list(CARPETA.rglob('*.xlsx'))

    print(f"Correos: {len(emls)}")
    print(f"Excels:  {len(xlsxs)}")

    # Parse correos
    eml_data = [parse_eml(p) for p in emls]
    all_cifs_emails = set()
    all_subjects = []
    for e in eml_data:
        if 'error' in e:
            continue
        all_subjects.append(e['subject'])
        text = e['subject'] + '\n' + e['from'] + '\n' + e['body']
        for m in CIF_RE.findall(text.upper()):
            all_cifs_emails.add(m)

    # Parse xlsx
    xlsx_data = [parse_xlsx(p) for p in xlsxs]
    all_cifs_xlsx = set()
    all_tomadores = set()
    for x in xlsx_data:
        if 'error' in x:
            continue
        all_cifs_xlsx |= x['cifs']
        all_tomadores |= x['tomadores']

    total_cifs = all_cifs_emails | all_cifs_xlsx
    print(f"\nCIFs distintos encontrados (total): {len(total_cifs)}")
    print(f"  De correos: {len(all_cifs_emails)}")
    print(f"  De xlsx:    {len(all_cifs_xlsx)}")
    print(f"\nTomadores distintos en xlsx: {len(all_tomadores)}")

    # Markdown
    md = []
    md.append("# REMAR — sub-flotas descubiertas\n\n")
    md.append(f"Carpeta Drive: `FLOTAS/ACTIVAS/UBICA/Remar - Goyo`\n\n")
    md.append(f"- Correos parseados: **{len(emls)}**\n")
    md.append(f"- Excels parseados: **{len(xlsxs)}**\n")
    md.append(f"- CIFs distintos totales: **{len(total_cifs)}**\n\n")
    md.append("## Todos los CIFs/NIFs encontrados\n\n")
    for cif in sorted(total_cifs):
        en_eml = ' (en correos)' if cif in all_cifs_emails else ''
        en_xlsx = ' (en xlsx)' if cif in all_cifs_xlsx else ''
        md.append(f"- `{cif}`{en_eml}{en_xlsx}\n")
    md.append("\n## Todos los tomadores/razones sociales únicos en los xlsx\n\n")
    for t in sorted(all_tomadores)[:200]:
        md.append(f"- {t}\n")
    md.append("\n## Resumen por archivo xlsx\n\n")
    for x in xlsx_data:
        if 'error' in x:
            md.append(f"- **{x['path']}** → ERROR: {x['error']}\n")
            continue
        md.append(f"- **{x['path']}** — hojas: {x['hojas']}\n")
        md.append(f"    - CIFs: {sorted(x['cifs'])}\n")
        md.append(f"    - Tomadores detectados: {len(x['tomadores'])}\n")
        for t in sorted(x['tomadores'])[:15]:
            md.append(f"      - {t}\n")
    md.append("\n## Correos (asuntos)\n\n")
    for s in all_subjects:
        md.append(f"- {s}\n")
    OUT.write_text(''.join(md), encoding='utf-8')
    print(f"\n[OK] {OUT}")


if __name__ == '__main__':
    main()
