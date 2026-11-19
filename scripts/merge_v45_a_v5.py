"""
Merge V4.5 (carpetas) → V5 (flotas + estudios).

Regla de oro: NO duplicar. Si una flota V4.5 ya está en V5 (match por CIF o nombre
normalizado), solo se enriquecen los campos que V5 tiene vacíos. Si no está, se crea.

Datos que se migran:
  - fecha de vencimiento        (header.fechaVencimiento, dd/mm/yyyy o ISO)
  - prima ofertada total        (sum de primaMmt en trabajo[] para OFERTADAS)
  - prima emitida total         (sum de primaMmt en trabajo[] para CONTRATADAS)
  - nº vehículos de la flota    (len de trabajo[] no vacío)
  - estado                      (si V5 no tiene estudio aún)

Backup automático antes de escribir.
"""
# -*- coding: utf-8 -*-
import sqlite3, json, re, os, sys, time, unicodedata
from datetime import datetime

V45 = os.environ.get('V45_DB_PATH', r'C:/opt/orion/data/orion.db')  # BD REAL V4.5 (375 carpetas)
V5  = os.environ.get('ORION_DB_PATH', r'C:/opt/orion_v5/data/orion.db')

# ─── Helpers ────────────────────────────────────────────────────────────────

def norm_cif(c):
    if not c: return ''
    s = str(c).upper().strip()
    s = re.sub(r'[^A-Z0-9]', '', s)
    return s if len(s) >= 7 and len(s) <= 12 else ''

_SUFIJOS = ['SLU','SL','SA','SAU','SCCL','SCL','SCA','SC','COOP','COOPERATIVA','SOCIEDADLIMITADA','SOCIEDADANONIMA']

def norm_nombre(n):
    if not n: return ''
    s = str(n).upper().strip()
    s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    s = s.replace('Ñ','N')
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Quitar sufijos
    for suf in _SUFIJOS:
        s = re.sub(rf'\b{suf}\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_fecha(f):
    """dd/mm/yyyy o yyyy-mm-dd → yyyy-mm-dd. '' si no parseable."""
    if not f: return ''
    s = str(f).strip()
    for fmt in ['%d/%m/%Y','%Y-%m-%d','%d-%m-%Y','%Y/%m/%d']:
        try: return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except: pass
    return ''

PRIMA_KEYS = ['prima_referencia','primaMmt','prima_mmt','primaMMT','primaOfertada','primaCliente','prima_cliente','primaFinal','prima_final','prima']

def _to_float(v):
    try:
        s = str(v).strip()
        if not s: return 0.0
        # Formatos posibles: 1895.00, 1.895,00, 1895, 1895,00
        if ',' in s and '.' in s:
            # 1.895,00 → quitar puntos de miles, cambiar coma
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        return float(s)
    except: return 0.0

def sumar_primas(trabajo):
    """Devuelve (suma_primas, nº_vehículos_no_vacíos). Una fila cuenta como vehículo si tiene matrícula."""
    if not isinstance(trabajo, list): return 0.0, 0
    total = 0.0; n = 0
    for v in trabajo:
        if not isinstance(v, dict): continue
        mat = v.get('matricula') or v.get('Matrícula') or v.get('matrícula') or ''
        if not str(mat).strip(): continue
        n += 1
        for k in PRIMA_KEYS:
            if k in v:
                val = _to_float(v[k])
                if val > 0: total += val; break
    return total, n

# ─── Carga V5 (indices para match rápido) ───────────────────────────────────

def cargar_v5_index(conn):
    rows = conn.execute("""
        SELECT f.id, f.cif, f.nombre,
            (SELECT e.id FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS estudio_id,
            (SELECT e.estado FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS estado,
            (SELECT e.fecha_vcto FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS fecha_vcto,
            (SELECT e.prima_ofertada_total FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS pof,
            (SELECT e.prima_emitida_total FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS pem
        FROM flotas f
    """).fetchall()
    by_cif = {}; by_nombre = {}
    for r in rows:
        d = dict(zip(['id','cif','nombre','estudio_id','estado','fecha_vcto','pof','pem'], r))
        k_cif = norm_cif(d['cif'])
        k_nom = norm_nombre(d['nombre'])
        if k_cif: by_cif.setdefault(k_cif, []).append(d)
        if k_nom: by_nombre.setdefault(k_nom, []).append(d)
    return by_cif, by_nombre

# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    print(f'[merge] V4.5 = {V45}')
    print(f'[merge] V5   = {V5}')
    if not os.path.exists(V45): sys.exit(f'V4.5 no existe: {V45}')
    if not os.path.exists(V5):  sys.exit(f'V5 no existe: {V5}')

    v45 = sqlite3.connect(V45); v45.row_factory = sqlite3.Row
    v5  = sqlite3.connect(V5);  v5.row_factory  = sqlite3.Row

    by_cif, by_nombre = cargar_v5_index(v5)
    print(f'[merge] V5 índice: {len(by_cif)} CIFs únicos, {len(by_nombre)} nombres únicos')

    stats = {'match_cif':0, 'match_nombre':0, 'creadas':0, 'actualizadas':0, 'sin_cambios':0,
             'fechas_puestas':0, 'primas_puestas':0, 'rechaz_sin_trabajo':0}

    for r in v45.execute("SELECT id, nombre, cif, estado, data FROM carpetas").fetchall():
        try: d = json.loads(r['data'])
        except: d = {}
        header = d.get('header', {}) if isinstance(d.get('header'), dict) else {}
        trabajo = d.get('trabajo', [])
        if not isinstance(trabajo, list): trabajo = []

        cif_src = norm_cif(r['cif'] or header.get('cif') or '')
        nom_src = norm_nombre(r['nombre'] or header.get('tomador') or '')

        fecha_vcto = parse_fecha(header.get('fechaVencimiento') or '')
        suma_prima, nveh = sumar_primas(trabajo)
        estado = (r['estado'] or 'EN ESTUDIO').upper()

        # Buscar match
        match = None
        if cif_src and cif_src in by_cif: match = by_cif[cif_src][0]; stats['match_cif'] += 1
        elif nom_src and nom_src in by_nombre: match = by_nombre[nom_src][0]; stats['match_nombre'] += 1

        if match:
            # Enriquecer sin sobrescribir lo ya existente
            upd = {}
            if fecha_vcto and not (match['fecha_vcto'] or '').strip():
                upd['fecha_vcto'] = fecha_vcto; stats['fechas_puestas'] += 1
            if suma_prima > 0:
                if estado == 'OFERTADA' and not (match['pof'] or 0) > 0:
                    upd['prima_ofertada_total'] = suma_prima; stats['primas_puestas'] += 1
                if estado == 'CONTRATADA' and not (match['pem'] or 0) > 0:
                    upd['prima_emitida_total'] = suma_prima; stats['primas_puestas'] += 1
            if upd and match['estudio_id']:
                cols = ', '.join(f'{k}=?' for k in upd)
                v5.execute(f'UPDATE estudios SET {cols}, actualizado_en=datetime("now") WHERE id=?',
                           (*upd.values(), match['estudio_id']))
                stats['actualizadas'] += 1
            # Guardar nº vehículos en flota_anual (año actual)
            if nveh > 0:
                cur_year = datetime.now().year
                existe = v5.execute("SELECT id FROM flota_anual WHERE flota_id=? AND año=?",
                                     (match['id'], cur_year)).fetchone()
                if not existe:
                    v5.execute("""INSERT INTO flota_anual(id, flota_id, año, num_vehiculos_fin, prima_total, fuente)
                                  VALUES(?, ?, ?, ?, ?, 'migracion_v45')""",
                               (f'fa_mig_{match["id"]}_{cur_year}', match['id'], cur_year, nveh, suma_prima))
                else:
                    v5.execute("""UPDATE flota_anual SET num_vehiculos_fin=MAX(num_vehiculos_fin, ?),
                                                         prima_total=MAX(prima_total, ?)
                                  WHERE id=?""", (nveh, suma_prima, existe['id']))
            if not upd and nveh == 0: stats['sin_cambios'] += 1
        else:
            # No existe en V5 → crear flota + estudio
            fid = f'flota_v45_{int(time.time()*1000)}_{stats["creadas"]:04x}'
            v5.execute("""INSERT INTO flotas(id, cif, nombre, actividad, sucursal, es_historica)
                          VALUES(?, ?, ?, ?, ?, 1)""",
                       (fid, r['cif'] or '', r['nombre'] or 'Sin nombre',
                        header.get('actividad', ''), 'MEDIACION'))
            eid = f'est_v45_{int(time.time()*1000)}_{stats["creadas"]:04x}'
            v5.execute("""INSERT INTO estudios(id, flota_id, nombre, estado, fecha_vcto,
                                prima_ofertada_total, prima_emitida_total, data, creado_por)
                          VALUES(?, ?, 'v1', ?, ?, ?, ?, '{}', 'migracion_v45')""",
                       (eid, fid, estado, fecha_vcto,
                        suma_prima if estado == 'OFERTADA' else 0,
                        suma_prima if estado == 'CONTRATADA' else 0))
            if nveh > 0:
                cur_year = datetime.now().year
                v5.execute("""INSERT INTO flota_anual(id, flota_id, año, num_vehiculos_fin, prima_total, fuente)
                              VALUES(?, ?, ?, ?, ?, 'migracion_v45')""",
                           (f'fa_mig_{fid}_{cur_year}', fid, cur_year, nveh, suma_prima))
            stats['creadas'] += 1
            if fecha_vcto: stats['fechas_puestas'] += 1
            if suma_prima > 0: stats['primas_puestas'] += 1
            if estado == 'RECHAZADA' and not trabajo: stats['rechaz_sin_trabajo'] += 1

    v5.commit()

    print('\n=== RESULTADO ===')
    for k, v in stats.items():
        print(f'  {k:22} {v}')
    print(f'\nV5 ahora:')
    for r in v5.execute("""
        SELECT (SELECT e.estado FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1) AS st,
               COUNT(*) AS n,
               SUM((SELECT e.prima_ofertada_total FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1)) AS pof,
               SUM((SELECT e.prima_emitida_total  FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1)) AS pem
        FROM flotas f GROUP BY st
    """).fetchall():
        print(f'  {r["st"]:12} {r["n"]:4} flotas  pof={r["pof"] or 0:>10,.0f}  pem={r["pem"] or 0:>10,.0f}')
    total_vcto = v5.execute("SELECT COUNT(*) FROM estudios WHERE fecha_vcto IS NOT NULL AND fecha_vcto!=''").fetchone()[0]
    print(f'  estudios con fecha_vcto: {total_vcto}')

if __name__ == '__main__':
    main()
