#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup_corredores.py — Fusiona corredores duplicados (mismo nombre).
Conserva el que tenga mas datos (comision, sucursal, cif). Reasigna carpetas.
Compatible Python 3.8+
"""
import sqlite3, os, unicodedata
from collections import defaultdict

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion-api/data/orion.db')

def norm(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()

def peso(row):
    """Puntuacion: cuantos campos tiene rellenos + flotas asignadas."""
    score = 0
    for col in ['sucursal', 'comercial', 'cif', 'comision']:
        v = row[col]
        if v and str(v).strip() and str(v).strip() not in ('0', '0.0', 'None'):
            score += 1
    return score

def run():
    if not os.path.exists(DB_PATH):
        print('ERROR: No se encuentra la BD en', DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Obtener todos los corredores
    corredores = conn.execute(
        'SELECT id, nombre, sucursal, comercial, cif, comision FROM corredores ORDER BY nombre'
    ).fetchall()

    # Agrupar por nombre normalizado
    grupos = defaultdict(list)
    for c in corredores:
        grupos[norm(c['nombre'])].append(c)

    duplicados = {k: v for k, v in grupos.items() if len(v) > 1}
    if not duplicados:
        print('No hay duplicados.')
        conn.close()
        return

    print(f'Grupos duplicados encontrados: {len(duplicados)}')

    total_fusionados = 0
    for nombre_norm, grupo in duplicados.items():
        # Contar flotas por corredor
        flotas_count = {}
        for c in grupo:
            n = conn.execute('SELECT COUNT(*) FROM carpetas WHERE corredor_id=?', [c['id']]).fetchone()[0]
            flotas_count[c['id']] = n

        # Elegir el "ganador": mayor peso primero, luego mayor numero de flotas
        ganador = max(grupo, key=lambda c: (peso(c), flotas_count[c['id']]))
        perdedores = [c for c in grupo if c['id'] != ganador['id']]

        print(f'\n[FUSIONAR] {grupo[0]["nombre"]}')
        print(f'  CONSERVAR: {ganador["id"]} ({flotas_count[ganador["id"]]} flotas, peso={peso(ganador)})')

        for p in perdedores:
            n_reasignadas = flotas_count[p['id']]
            print(f'  ELIMINAR:  {p["id"]} ({n_reasignadas} flotas) -> reasignando...')
            conn.execute(
                'UPDATE carpetas SET corredor_id=? WHERE corredor_id=?',
                [ganador['id'], p['id']]
            )
            conn.execute('DELETE FROM corredores WHERE id=?', [p['id']])
            total_fusionados += 1

    conn.commit()

    # Verificacion final
    print(f'\nCorredores eliminados (duplicados): {total_fusionados}')
    restantes = conn.execute('SELECT COUNT(*) FROM corredores').fetchone()[0]
    print(f'Corredores restantes en BD: {restantes}')
    conn.close()
    print('=== FIN ===')

if __name__ == '__main__':
    run()
