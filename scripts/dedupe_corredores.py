"""
Dedupe corredores en V5 por CIF.

Regla: por cada CIF con ≥2 entradas, elegir canónico (preferencia código CM*/CTC* del TXT
del jefe sobre números sueltos tipo "26683"), reasignar carpetas.corredor_id al canónico
y borrar duplicados.

No toca carpetas, solo corredores y la fk.
"""
# -*- coding: utf-8 -*-
import sqlite3, re, collections, shutil
from datetime import datetime

V5 = r'C:/opt/orion_v5/data/orion.db'
shutil.copy2(V5, f'{V5}.pre_dedupe_cor_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
c = sqlite3.connect(V5); c.row_factory = sqlite3.Row

def cif_norm(s):
    return re.sub(r'[^A-Z0-9]', '', (s or '').upper().strip())

# Prioridad de código: más alto = más deseable como canónico
# CM/CT* vienen del TXT oficial del jefe → ganan
def rank(codigo):
    if not codigo: return 0
    c = codigo.upper().strip()
    if re.match(r'^CM\d{3}$', c): return 100          # Mediación oficial
    if re.match(r'^CT[CLMNSBE]\d', c): return 100     # Titán oficial
    if re.match(r'^CM\d{3}_\d+$', c): return 90       # Mediación variante
    if re.match(r'^CT.*_\d+$', c): return 90          # Titán variante
    if re.match(r'^COR-\d+$', c): return 80           # formato COR-xx
    if re.match(r'^CM\d+$', c): return 70             # otros CM
    if re.match(r'^\d{5}$', c): return 50             # código antiguo 5 dígitos
    return 10

# Agrupar por CIF
by_cif = collections.defaultdict(list)
for r in c.execute("SELECT id,nombre,cif,codigo,sucursal FROM corredores").fetchall():
    cif = cif_norm(r['cif'])
    if cif: by_cif[cif].append(dict(r))

n_dup = sum(1 for v in by_cif.values() if len(v) > 1)
print(f'CIFs con ≥2 corredores: {n_dup}')

reasignadas = 0; borrados = 0
for cif, lst in by_cif.items():
    if len(lst) < 2: continue
    # Elegir canónico: mayor rank de código, en empate el más antiguo (ID menor)
    lst_sorted = sorted(lst, key=lambda x: (-rank(x['codigo']), x['id']))
    canon = lst_sorted[0]
    dups  = lst_sorted[1:]
    for d in dups:
        # Reasignar carpetas al canónico
        r = c.execute("UPDATE carpetas SET corredor_id=? WHERE corredor_id=?", (canon['id'], d['id']))
        reasignadas += r.rowcount
        # Eliminar duplicado
        c.execute("DELETE FROM corredores WHERE id=?", (d['id'],))
        borrados += 1

c.commit()
print(f'Carpetas reasignadas al canónico: {reasignadas}')
print(f'Corredores duplicados eliminados: {borrados}')
print(f'Corredores totales ahora: {c.execute("SELECT COUNT(*) FROM corredores").fetchone()[0]}')

# Verificación: flotas por corredor (top 10)
print('\nTop corredores por flotas (post-dedupe):')
rows = c.execute("""
  SELECT co.nombre, COUNT(ca.id) AS n
  FROM corredores co JOIN carpetas ca ON ca.corredor_id=co.id
  GROUP BY co.id ORDER BY n DESC LIMIT 10
""").fetchall()
for r in rows: print(f'  {r["n"]:4}  {r["nombre"][:50]}')
