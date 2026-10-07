#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_sucursales.py — Asigna sucursal a corredores que la tienen en blanco.
- Corredores exclusivos de TITAN: sucursal = TITAN
- Resto sin sucursal: sucursal = MEDIACION
- Nunca sobreescribe corredores que ya tienen sucursal asignada.
Compatible Python 3.8+
"""
import sqlite3, os, unicodedata

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion-api/data/orion.db')

def norm(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()

# Corredores que son exclusivamente de la sucursal TITAN
TITAN_KEYWORDS = [
    'ruiz dominguez',
    'ecocasbroker',
    'multigestion',
    'basurte',
    'centre gestor lleida',
    'gesa mediacion',
]

def es_titan(nombre):
    n = norm(nombre)
    return any(k in n for k in TITAN_KEYWORDS)

def run():
    if not os.path.exists(DB_PATH):
        print('ERROR: No se encuentra la BD en', DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    corredores = conn.execute(
        'SELECT id, nombre, sucursal FROM corredores'
    ).fetchall()

    titan_count = mediacion_count = skip_count = 0

    for c in corredores:
        # No tocar los que ya tienen sucursal
        if c['sucursal'] and c['sucursal'].strip():
            skip_count += 1
            continue

        if es_titan(c['nombre']):
            nueva = 'TITAN'
            titan_count += 1
        else:
            nueva = 'MEDIACION'
            mediacion_count += 1

        conn.execute('UPDATE corredores SET sucursal=? WHERE id=?', [nueva, c['id']])
        print(f'  [{nueva}] {c["nombre"]}')

    conn.commit()
    conn.close()

    print(f'\nActualizados TITAN: {titan_count}')
    print(f'Actualizados MEDIACION: {mediacion_count}')
    print(f'Sin tocar (ya tenian sucursal): {skip_count}')
    print('=== FIN ===')

if __name__ == '__main__':
    run()
