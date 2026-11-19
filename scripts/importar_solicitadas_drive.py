"""
Importar flotas SOLICITADAS/COTIZADAS del Drive que no están en V5.
También ACTIVAS que no matchearon en el script anterior.

Las SOLICITADAS en Drive no tienen capa corredor, están sueltas → entran sin corredor_id.
Las ACTIVAS sí tienen corredor (carpeta padre) → entran con corredor_id resuelto.
"""
# -*- coding: utf-8 -*-
import os, sqlite3, json, re, unicodedata, time, shutil, uuid
from datetime import datetime

V5 = r'C:/opt/orion_v5/data/orion.db'
BASE = r'C:/Users/garci/Downloads/ORION_auditoria_17_11_2026/Drive_dump'
shutil.copy2(V5, f'{V5}.pre_import_solic_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
c = sqlite3.connect(V5); c.row_factory = sqlite3.Row

def norm(s):
    if not s: return ''
    s = str(s).upper().strip()
    s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    for w in ['IKER','ENRIC','JAVIER','ROBERTO','ANTONIO','PERSONA CONTACTO','EMISION POSTERIOR','ALTAS POSTERIORES']:
        s = s.replace(w, '')
    s = s.replace('Ñ','N')
    s = re.sub(r'[^A-Z0-9 ]',' ',s)
    s = re.sub(r'\s+',' ',s).strip()
    for suf in ['SL','SLU','SA','SAU','SCCL','LOGISTICS','LOGISTICOS','TTES','TRANSPORTES','DE']:
        s = re.sub(rf'\b{suf}\b','',s)
    return re.sub(r'\s+',' ',s).strip()

MAP_COR = {
    'ARAGONES Y CEBORIAN':'CM030','BIDASOA -IKER':'CTN0Z0014','COTASEGUR SL':'CM095',
    'DELTA CORREDURIA - IKER':'CTN0Z0009','Gruas y Porta vehículos Pedro SL - JUYENT -ENRIC':'CTC0Z0006',
    'PEDRO MARTINEZ DE QUER':'CM088','JOSEFINA FERREIROS SANCHEZ-GUISANDE (LA RIOJA-IKER)':'CTN0Z0007',
    'KIDEKA - IKER':'CTN0Z0004',
}
cor_by_cod = {r['codigo']:r['id'] for r in c.execute("SELECT id,codigo FROM corredores WHERE codigo!=''").fetchall()}
cor_by_nombre_norm = {norm(r['nombre']):r['id'] for r in c.execute("SELECT id,nombre FROM corredores").fetchall()}

def resolver_corredor(carpeta_padre):
    if carpeta_padre in MAP_COR and MAP_COR[carpeta_padre] in cor_by_cod:
        return cor_by_cod[MAP_COR[carpeta_padre]]
    cp = norm(carpeta_padre)
    if cp in cor_by_nombre_norm: return cor_by_nombre_norm[cp]
    palabras = [p for p in cp.split() if len(p)>3]
    for p in palabras[:1]:
        for k,v in cor_by_nombre_norm.items():
            if p in k: return v
    return None

# Carpetas V5 existentes (para evitar duplicar)
v5_norm = {norm(r['nombre']):r['id'] for r in c.execute("SELECT id,nombre FROM carpetas").fetchall()}
v5_cif  = {(r['cif'] or '').upper().strip(): r['id'] for r in c.execute("SELECT id,cif FROM carpetas WHERE cif IS NOT NULL AND cif!=''").fetchall()}

def existe_en_v5(nombre_drive):
    n = norm(nombre_drive)
    if n in v5_norm: return v5_norm[n]
    # Contiene
    for k,v in v5_norm.items():
        if k and n and (k in n or n in k) and abs(len(k)-len(n))<15:
            return v
    return None

# Procesar carpetas Drive por categoría
def importar_categoria(subcarpeta, estado_v5, con_corredor=False):
    """
    Si con_corredor=True, estructura es ACTIVAS/[CORREDOR]/[FLOTA].
    Si False, es directamente CATEGORÍA/[FLOTA].
    """
    dir_full = os.path.join(BASE, subcarpeta)
    if not os.path.exists(dir_full):
        print(f'[skip] {subcarpeta} no existe')
        return 0,0,0
    creadas = ya = sin_cor = 0
    items = os.listdir(dir_full)
    for item in items:
        full = os.path.join(dir_full, item)
        if not os.path.isdir(full): continue
        if con_corredor:
            # item es carpeta corredor, dentro están las flotas
            cor_id = resolver_corredor(item)
            if not cor_id: sin_cor += 1
            for flota in os.listdir(full):
                if not os.path.isdir(os.path.join(full,flota)): continue
                _importar_flota(flota, estado_v5, cor_id)
                v = existe_en_v5(flota)
                if v: ya += 1
                else: creadas += 1
        else:
            _importar_flota(item, estado_v5, None)
            v = existe_en_v5(item)
            if v: ya += 1
            else: creadas += 1
    return creadas, ya, sin_cor

stats_total = {'creadas':0, 'ya_existen':0}

def _importar_flota(nombre, estado, cor_id):
    v5id = existe_en_v5(nombre)
    if v5id:
        # Actualiza estado solo si está vacío, no sobrescribe trabajo
        cur = c.execute("SELECT estado,corredor_id FROM carpetas WHERE id=?", (v5id,)).fetchone()
        if cor_id and not cur['corredor_id']:
            c.execute("UPDATE carpetas SET corredor_id=? WHERE id=?", (cor_id, v5id))
        stats_total['ya_existen'] += 1
        return
    # Crear
    fid = f'carpeta_drive_{uuid.uuid4().hex[:16]}'
    nombre_limpio = re.split(r'\s*[-·]\s*(iker|enric|javier|roberto|antonio|comercial)', nombre, flags=re.I)[0].strip()
    data = json.dumps({
        'id': fid,
        'nombre': nombre_limpio or nombre,
        'estado': estado,
        'corredor_id': cor_id,
        'header': {'tomador': nombre_limpio or nombre, 'cif':'', 'actividad':'', 'fechaVencimiento':'', 'fechaInicio':''},
        'trabajo': [], 'original': [], 'oferta': [], 'automaticoVehicles': [],
        'observaciones': f'Importado desde Drive {datetime.now().strftime("%Y-%m-%d")}',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat(),
    }, ensure_ascii=False)
    c.execute("""INSERT INTO carpetas(id,nombre,estado,cif,tomador,actividad,corredor_id,creado_por,updated_at,data)
                 VALUES(?,?,?,?,?,?,?,?,?,?)""",
              (fid, nombre_limpio or nombre, estado, '', nombre_limpio or nombre, '', cor_id,
               'import_drive', datetime.now().isoformat(), data))
    v5_norm[norm(nombre)] = fid
    stats_total['creadas'] += 1

print('[1] FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS → OFERTADA')
c1, y1, _ = importar_categoria('FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS', 'OFERTADA', False)
print(f'   creadas={c1}  ya existían={y1}')

print('\n[2] ACTIVAS → CONTRATADA (con corredor)')
c2, y2, sc2 = importar_categoria('ACTIVAS', 'CONTRATADA', True)
print(f'   creadas={c2}  ya existían={y2}  sin corredor={sc2}')

print('\n[3] ESTUDIOS → EN ESTUDIO')
c3, y3, _ = importar_categoria('ESTUDIOS', 'EN ESTUDIO', False)
print(f'   creadas={c3}  ya existían={y3}')

print('\n[4] FLOTAS REHUSADAS → RECHAZADA')
c4, y4, _ = importar_categoria('FLOTAS REHUSADAS', 'RECHAZADA', False)
print(f'   creadas={c4}  ya existían={y4}')

print('\n[5] FLOTAS HECHAS POR TITAN 2025-2026 → CONTRATADA')
c5, y5, _ = importar_categoria('FLOTAS HECHAS POR TITAN 2025-2026', 'CONTRATADA', False)
print(f'   creadas={c5}  ya existían={y5}')

c.commit()
print('\n=== TOTAL ===')
for k,v in stats_total.items(): print(f'  {k}: {v}')
print(f'\nV5 ahora:')
import collections
by = collections.Counter(r['estado'] for r in c.execute("SELECT estado FROM carpetas").fetchall())
for k in ['EN ESTUDIO','OFERTADA','CONTRATADA','RECHAZADA']:
    print(f'  {k:12}: {by.get(k,0)}')
print(f'  TOTAL: {sum(by.values())}')
