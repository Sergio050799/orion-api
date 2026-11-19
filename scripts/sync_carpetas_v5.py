"""
Sincroniza la tabla `carpetas` dentro de V5 BD para que coincida con la realidad:

  carpetas en V5 = carpetas de V4.5 real (/opt/orion/data/orion.db, 375)
                 + flotas del Drive que solo están en V5.flotas (las 24 extra)

Así Dashboard, Estudio (CarpetaScreen) y v7 miran la MISMA realidad.

Backup automático antes de escribir.
"""
# -*- coding: utf-8 -*-
import sqlite3, json, re, os, time, unicodedata, shutil
from datetime import datetime

V45 = r'C:/opt/orion/data/orion.db'           # BD real V4.5 (375 carpetas con Vidriera)
V5  = r'C:/opt/orion_v5/data/orion.db'        # BD V5 (destino)

# Backup
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
bk = f'{V5}.pre_sync_carpetas_{stamp}'
shutil.copy2(V5, bk)
print(f'[sync] backup → {bk}')

v45 = sqlite3.connect(V45); v45.row_factory = sqlite3.Row
v5  = sqlite3.connect(V5);  v5.row_factory  = sqlite3.Row

def norm_cif(c):
    if not c: return ''
    s = re.sub(r'[^A-Z0-9]', '', str(c).upper().strip())
    return s if 7 <= len(s) <= 12 else ''

def norm_nombre(n):
    if not n: return ''
    s = str(n).upper().strip()
    s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    s = s.replace('Ñ','N')
    s = re.sub(r'[^A-Z0-9 ]',' ',s)
    s = re.sub(r'\s+',' ',s).strip()
    for suf in ['SLU','SL','SA','SAU','SCCL','SCL','SCA','SC','COOP','COOPERATIVA']:
        s = re.sub(rf'\b{suf}\b','',s)
    return re.sub(r'\s+',' ',s).strip()

# ─── Paso 1: copiar las 375 carpetas V4.5 reales a V5.carpetas ──────────────
# Borramos las 364 stale de V5 y replicamos las 375 de V4.5 completas.
print('[sync] borrando carpetas stale V5...')
v5.execute('DELETE FROM carpetas')

cols_v45 = [r['name'] for r in v45.execute("PRAGMA table_info(carpetas)").fetchall()]
cols_v5  = [r['name'] for r in v5.execute("PRAGMA table_info(carpetas)").fetchall()]
cols_comunes = [c for c in cols_v45 if c in cols_v5]
print(f'[sync] columnas comunes: {cols_comunes}')

n = 0
for r in v45.execute(f"SELECT {','.join(cols_comunes)} FROM carpetas").fetchall():
    vals = tuple(r[c] for c in cols_comunes)
    placeholders = ','.join('?' * len(cols_comunes))
    v5.execute(f"INSERT INTO carpetas({','.join(cols_comunes)}) VALUES({placeholders})", vals)
    n += 1
print(f'[sync] insertadas {n} carpetas V4.5 → V5')

# ─── Paso 2: crear carpetas para las flotas V5 que NO están en V4.5 ─────────
# Son las que vinieron del Drive y nunca pasaron por V4.5.
existentes_cif = {norm_cif(r['cif']) for r in v5.execute('SELECT cif FROM carpetas').fetchall() if r['cif']}
existentes_nom = {norm_nombre(r['nombre']) for r in v5.execute('SELECT nombre FROM carpetas').fetchall()}

flotas = v5.execute("""
    SELECT f.id, f.cif, f.nombre, f.actividad,
           (SELECT estado FROM estudios WHERE flota_id=f.id ORDER BY actualizado_en DESC LIMIT 1) AS estado,
           (SELECT fecha_vcto FROM estudios WHERE flota_id=f.id ORDER BY actualizado_en DESC LIMIT 1) AS vto
    FROM flotas f
""").fetchall()

creadas = 0
for f in flotas:
    ncif = norm_cif(f['cif'])
    nnom = norm_nombre(f['nombre'])
    if (ncif and ncif in existentes_cif) or (nnom and nnom in existentes_nom):
        continue
    header = {
        'tomador': f['nombre'] or '',
        'cif': f['cif'] or '',
        'actividad': f['actividad'] or '',
        'fechaVencimiento': f['vto'] or '',
        'fechaInicio': '',
    }
    data = json.dumps({
        'id': f['id'],
        'nombre': f['nombre'] or 'Sin nombre',
        'estado': f['estado'] or 'EN ESTUDIO',
        'corredor_id': None,
        'header': header,
        'trabajo': [],
        'original': [],
        'oferta': [],
        'observaciones': '',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat(),
    }, ensure_ascii=False)
    # Insertar en V5.carpetas con los campos que existan
    cols = {'id': f['id'], 'nombre': f['nombre'] or 'Sin nombre',
            'estado': f['estado'] or 'EN ESTUDIO', 'cif': f['cif'] or '', 'data': data}
    kk = [c for c in cols if c in cols_v5]
    vv = [cols[c] for c in kk]
    placeholders = ','.join('?' * len(kk))
    v5.execute(f"INSERT INTO carpetas({','.join(kk)}) VALUES({placeholders})", vv)
    creadas += 1
    if ncif: existentes_cif.add(ncif)
    if nnom: existentes_nom.add(nnom)

print(f'[sync] carpetas creadas desde flotas V5 (Drive): {creadas}')

v5.commit()

# ─── Verificación ──────────────────────────────────────────────────────────
total = v5.execute('SELECT COUNT(*) FROM carpetas').fetchone()[0]
vid = v5.execute("SELECT COUNT(*) FROM carpetas WHERE UPPER(nombre) LIKE '%VIDRIERA%'").fetchone()[0]
import collections
by = collections.Counter([r['estado'] for r in v5.execute('SELECT estado FROM carpetas').fetchall()])

print()
print(f'=== V5.carpetas tras sync ===')
print(f'  total: {total}  vidriera: {vid}')
print(f'  por estado: {dict(by)}')
print(f'=== V5.flotas ===')
print(f'  total: {v5.execute("SELECT COUNT(*) FROM flotas").fetchone()[0]}')
