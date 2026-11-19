"""
Asignar el corredor correcto (según carpeta padre en Drive) a cada flota V5 que
corresponde con una carpeta en Drive_dump.

Usa mapping manual para los 8 casos con typo + fuzzy match para los 15 que sí cuadran.
Si una flota Drive no existe en V5, se deja para el siguiente script (import_from_drive).
"""
# -*- coding: utf-8 -*-
import os, sqlite3, re, unicodedata, time, shutil
from datetime import datetime

V5 = r'C:/opt/orion_v5/data/orion.db'
BASE = r'C:/Users/garci/Downloads/ORION_auditoria_17_11_2026/Drive_dump'
shutil.copy2(V5, f'{V5}.pre_asignar_cor_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
c = sqlite3.connect(V5); c.row_factory = sqlite3.Row

# Mapping manual Drive carpeta → V5 corredor_codigo
MAP_MANUAL = {
    'ARAGONES Y CEBORIAN': 'CM030',
    'BIDASOA -IKER': 'CTN0Z0014',
    'COTASEGUR SL': 'CM095',
    'DELTA CORREDURIA - IKER': 'CTN0Z0009',
    'Gruas y Porta vehículos Pedro SL - JUYENT -ENRIC': 'CTC0Z0006',
    'PEDRO MARTINEZ DE QUER': 'CM088',
    'JOSEFINA FERREIROS SANCHEZ-GUISANDE (LA RIOJA-IKER)': 'CTN0Z0007',
    'KIDEKA - IKER': 'CTN0Z0004',  # KALIBO contiene a KIDEKA
}

# Crear corredores nuevos para los que no existen en V5
CREAR = {
    'COBIAN': {'nombre': 'COBIÁN CORREDURÍA DE SEGUROS', 'sucursal': 'MEDIACION'},
    'IURISCAR': {'nombre': 'IURISCAR CORREDURÍA DE SEGUROS', 'sucursal': 'MEDIACION'},
}

def norm(s):
    if not s: return ''
    s = str(s).upper().strip()
    s = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    s = s.replace('Ñ', 'N')
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

# Cargar índice de corredores V5
cor_by_codigo = {r['codigo']: r for r in c.execute("SELECT * FROM corredores WHERE codigo IS NOT NULL AND codigo!=''").fetchall()}
cor_by_nombre = {norm(r['nombre']): r for r in c.execute("SELECT * FROM corredores").fetchall()}

# Crear los nuevos
created = 0
for drive_name, info in CREAR.items():
    if not any(drive_name.upper() in k.upper() for k in cor_by_nombre):
        cid = f'corr_drive_{int(time.time()*1000)}_{created:04x}'
        c.execute("INSERT INTO corredores(id,nombre,sucursal,codigo) VALUES(?,?,?,?)",
                  (cid, info['nombre'], info['sucursal'], f'DR-{drive_name[:6]}'))
        print(f'[CREAR] {drive_name} → {cid}')
        cor_by_nombre[norm(info['nombre'])] = {'id': cid, 'nombre': info['nombre'], 'sucursal': info['sucursal']}
        created += 1
c.commit()

# Resolver carpeta Drive → corredor V5 id
def resolver_corredor_drive(carpeta_drive):
    if carpeta_drive in MAP_MANUAL:
        cod = MAP_MANUAL[carpeta_drive]
        if cod in cor_by_codigo: return cor_by_codigo[cod]['id']
    # Fuzzy por nombre
    cd_norm = norm(carpeta_drive)
    # Match exacto primero
    if cd_norm in cor_by_nombre: return cor_by_nombre[cd_norm]['id']
    # Match contains primera palabra >3 chars
    palabras = [p for p in cd_norm.split() if len(p) > 3 and p not in ('IKER','ENRIC','JUYENT','MEDI','CORREDURIA')]
    for p in palabras[:1]:
        for k, v in cor_by_nombre.items():
            if p in k and p not in ('VEHICULOS','PORTA','GRUAS'):
                return v['id']
    # CREAR si está en lista
    if carpeta_drive in CREAR:
        return cor_by_nombre[norm(CREAR[carpeta_drive]['nombre'])]['id']
    return None

# Procesar Drive ACTIVAS
activas_dir = os.path.join(BASE, 'ACTIVAS')
stats = {'match_flota_asignada': 0, 'match_flota_ya_correcta': 0, 'no_match_flota': 0, 'no_resuelto_corredor': 0}
flotas_sin_match_v5 = []

carpetas_v5_norm = {norm(r['nombre']): r['id'] for r in c.execute("SELECT id,nombre FROM carpetas").fetchall()}

for carpeta_drive in os.listdir(activas_dir):
    full = os.path.join(activas_dir, carpeta_drive)
    if not os.path.isdir(full): continue
    cor_id = resolver_corredor_drive(carpeta_drive)
    if not cor_id:
        print(f'[SIN RESOLVER] carpeta corredor: {carpeta_drive}')
        stats['no_resuelto_corredor'] += 1
        continue

    for flota_drive in os.listdir(full):
        if not os.path.isdir(os.path.join(full, flota_drive)): continue
        # Limpiar nombre flota (quitar sufijos del drive tipo "- JAVIER DE ATSYR")
        nombre_limpio = re.split(r'\s*[-·]\s*(iker|enric|javier|roberto|comercial|titan|mediacion|cobian|cotasegur|atsyr|de quel|delta|ruiz|molyma|bidasoa|aragones)',
                                  flota_drive, flags=re.IGNORECASE)[0].strip()
        cand_norms = [norm(nombre_limpio), norm(flota_drive)]
        matched_v5 = None
        for n in cand_norms:
            if not n or len(n) < 4: continue
            if n in carpetas_v5_norm:
                matched_v5 = carpetas_v5_norm[n]; break
            for k, v in carpetas_v5_norm.items():
                if (n in k or k in n) and abs(len(n) - len(k)) < 15:
                    matched_v5 = v; break
            if matched_v5: break

        if matched_v5:
            # Verificar si ya tiene el corredor correcto
            cur = c.execute("SELECT corredor_id FROM carpetas WHERE id=?", (matched_v5,)).fetchone()
            if cur and cur['corredor_id'] == cor_id:
                stats['match_flota_ya_correcta'] += 1
            else:
                c.execute("UPDATE carpetas SET corredor_id=? WHERE id=?", (cor_id, matched_v5))
                stats['match_flota_asignada'] += 1
        else:
            stats['no_match_flota'] += 1
            flotas_sin_match_v5.append((carpeta_drive, flota_drive))

c.commit()

print('\n=== RESULTADO ===')
for k, v in stats.items():
    print(f'  {k:28}: {v}')
if flotas_sin_match_v5:
    print(f'\nFlotas Drive ACTIVAS sin match V5 ({len(flotas_sin_match_v5)}):')
    for d, f in flotas_sin_match_v5:
        print(f'  [{d[:30]:32}] {f[:50]}')
