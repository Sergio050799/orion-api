#!/usr/bin/env python3
"""
Migration: Unificar flotas contratadas como unica fuente de verdad.
  1. Actualiza nombres de corredores
  2. Elimina carpetas con estado CONTRATADA
  3. Inserta las 30 flotas contratadas del portfolio real
Ejecutar: python fix_contratadas.py
"""
import sqlite3
import json
import os
import uuid
from datetime import datetime

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')

# (patron LIKE, nombre limpio)
CORREDOR_UPDATES = [
    ('%AON%',                           'AON'),
    ('%ARAGONES%',                      'ARAGONES Y CEBORIAN'),
    ('%ATSYR%',                         'ATSYR CORREDURÍA DE SEGUROS'),
    ('%BIDASOA%',                       'BIDASOA'),
    ('%MDS%',                           'MDS'),
    ('%COTASEGUR%',                     'COTASEGUR SL'),
    ('%DELTA%CORRE%',                   'DELTA CORREDURIA'),
    ('%ERSM%',                          'ERSM'),
    ('%JUNYENT%',                       "JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L."),
    ('%FERREIROS%',                     'JOSEFINA FERREIROS SANCHEZ-GUISANDE'),
    ('%LARREA%',                        'LARREA & BAREA CORREDURÍA DE SEGUROS, S.L.'),
    ('%PIQUE%CORRE%',                   'M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.'),
    ('%MINGUEZ%',                       'MINGUEZ SAEZ BROKERS, S.L.'),
    ('%MOLYMA%',                        'MOLYMA, S.A. CORREDURIA DE SEGUROS'),
    ('%PEDRO%QUEL%',                    'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.'),
    ('%PREMIUM%QUALITY%',               'PREMIUM QUALITY INVESTMENTS, S.L.'),
    ('%SAEZ%MONTAGUT%',                 'SÁEZ DE MONTAGUT & MORENO'),
    ('%MONTAGUT%MORENO%',               'SÁEZ DE MONTAGUT & MORENO'),
    ('%WILLIS%',                        'WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA'),
]

# (nombre_corredor_exacto_tras_update, nombre_flota, fecha_vencimiento)
FLOTAS = [
    ('AON',                                                 'TRANSPORTES HERMANOS LAREDO, SA',             '31/03/2027'),
    ('ARAGONES Y CEBORIAN',                                 'TRES CAMPANAS',                               '01/07/2027'),
    ('ARAGONES Y CEBORIAN',                                 'TRANSPORTES ISIDRO SAN ROMAN E HIJOS SL',    '07/08/2027'),
    ('ATSYR CORREDURÍA DE SEGUROS',                         'FUNDACIÓN BANCO DE ALIMENTOS DE MADRID',      '01/06/2027'),
    ('BIDASOA',                                             'TRANSPORTES HIRUMUGETA',                      '01/10/2027'),
    ('BIDASOA',                                             'INTEROPTRANS SL',                             '01/10/2027'),
    ('MDS',                                                 'ALVEMACO',                                    '31/12/2026'),
    ('COTASEGUR SL',                                        'MARMOLES TOLEDANOS',                          '01/10/2027'),
    ('DELTA CORREDURIA',                                    'IGNACIO LIMA ZABALEGUI',                      '14/09/2027'),
    ('ERSM',                                                'EMBOTITS PORTELLA SL',                        '11/09/2027'),
    ("JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L.",        'GRUAS Y PORTA VEHÍCULOS PEDRO SL',            '10/07/2027'),
    ('JOSEFINA FERREIROS SANCHEZ-GUISANDE',                 'TRANSPORTES VALLE DEL OJA SL',                '29/05/2027'),
    ('LARREA & BAREA CORREDURÍA DE SEGUROS, S.L.',          'IMPULS WORLD LOGISTICS SL',                   '01/10/2027'),
    ('M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.',        'PSM VIVER DEL REC SL',                        '17/07/2027'),
    ('MINGUEZ SAEZ BROKERS, S.L.',                          'TRANSPORTES BRAMAR',                          '01/01/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'BENAYAS SERVICIOS LOGISTICOS SL',             '01/09/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'ALBERTO Y ANTONIO ESTRELLA GRANO DE ORO',    '01/09/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'ON-RED TRUCK LOGISTICS',                      '17/05/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'SERGETRANS SL',                               '01/07/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'SOTO ECOTRANS, SL',                           '25/03/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'TRANSPORTES BAS 2023 SL',                     '01/04/2027'),
    ('MOLYMA, S.A. CORREDURIA DE SEGUROS',                  'TRANSPORTES FARMACOLOGICOS CASTILLA, S.L.',   '24/02/2027'),
    ('PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.',   'LOGISTICA Y TRANSPORTES DE PEDRO',            '01/07/2027'),
    ('PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.',   'DPM LOGISTICA 1966 SL',                       '01/07/2027'),
    ('PREMIUM QUALITY INVESTMENTS, S.L.',                   'LOGISTICA NOGUERAS SL',                       '01/05/2027'),
    ('PREMIUM QUALITY INVESTMENTS, S.L.',                   'TRANSPORTES DALMUR, S.L',                     '31/12/2026'),
    ('PREMIUM QUALITY INVESTMENTS, S.L.',                   'AGUSTÍN MARTÍNEZ S.L.',                       '09/06/2027'),
    ('SÁEZ DE MONTAGUT & MORENO',                           'SEJERCON SL',                                 '20/07/2027'),
    ('WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA', 'GEODIS RT SPAIN S.A.',                        '01/01/2027'),
    ('WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA', 'TOPFORM S.L.',                                '31/12/2026'),
]


def run():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    print(f"\n[fix_contratadas] DB: {DB_PATH}\n")

    # ── 1. Actualizar nombres de corredores ────────────────────────────────────
    print("1. Actualizando nombres de corredores...")
    for pattern, new_name in CORREDOR_UPDATES:
        rows = conn.execute(
            "SELECT id, nombre FROM corredores WHERE UPPER(nombre) LIKE UPPER(?)", [pattern]
        ).fetchall()
        for r in rows:
            conn.execute("UPDATE corredores SET nombre=?, updated_at=? WHERE id=?",
                         [new_name, now, r['id']])
            print(f"   ✓ '{r['nombre']}' → '{new_name}'")

    conn.commit()

    # ── 2. Construir mapa corredor_nombre → id ─────────────────────────────────
    corredores = conn.execute("SELECT id, nombre FROM corredores").fetchall()
    corr_map = {r['nombre']: r['id'] for r in corredores}
    print(f"\n2. Corredores en BD: {len(corr_map)}")

    # ── 3. Eliminar carpetas CONTRATADA ────────────────────────────────────────
    deleted = conn.execute(
        "SELECT COUNT(*) FROM carpetas WHERE estado='CONTRATADA'"
    ).fetchone()[0]
    conn.execute("DELETE FROM carpetas WHERE estado='CONTRATADA'")
    conn.commit()
    print(f"\n3. Eliminadas {deleted} carpetas CONTRATADA")

    # ── 4. Insertar flotas del portfolio real ──────────────────────────────────
    print(f"\n4. Insertando {len(FLOTAS)} flotas contratadas...")
    inserted = 0
    missing_corredores = []

    for corredor_nombre, flota_nombre, fecha_vcto in FLOTAS:
        corredor_id = corr_map.get(corredor_nombre)
        if not corredor_id:
            # Fallback: buscar por nombre similar
            for nombre_bd, cid in corr_map.items():
                if corredor_nombre.upper()[:10] in nombre_bd.upper():
                    corredor_id = cid
                    break

        if not corredor_id:
            missing_corredores.append(corredor_nombre)
            print(f"   ✗ CORREDOR NO ENCONTRADO: '{corredor_nombre}' — flota '{flota_nombre}' sin asignar")

        carp_id = 'carp_' + uuid.uuid4().hex[:16]
        data = {
            'id': carp_id,
            'nombre': flota_nombre,
            'estado': 'CONTRATADA',
            'corredor_id': corredor_id,
            'header': {
                'fechaVencimiento': fecha_vcto,
                'tomador': '',
                'cif': '',
                'actividad': '',
                'fechaInicio': '',
            },
            'trabajo': [],
            'original': [],
            'oferta': [],
            'observaciones': '',
            'createdAt': now,
            'updatedAt': now,
        }
        conn.execute("""
            INSERT INTO carpetas (id, nombre, estado, corredor_id, creado_por, created_at, updated_at, data)
            VALUES (?, ?, 'CONTRATADA', ?, 'SPIKE', ?, ?, ?)
        """, [carp_id, flota_nombre, corredor_id, now, now, json.dumps(data, ensure_ascii=False)])
        inserted += 1
        status = f"corredor={corredor_nombre}" if corredor_id else "SIN CORREDOR"
        print(f"   ✓ '{flota_nombre}' ({status}, vcto {fecha_vcto})")

    conn.commit()
    print(f"\n✓ Insertadas {inserted} flotas contratadas")

    if missing_corredores:
        print(f"\n⚠ Corredores no encontrados: {missing_corredores}")
        print("  Crea estos corredores en Orion y vuelve a asignarlos manualmente.")

    conn.close()
    print("\n[fix_contratadas] Completado.\n")


if __name__ == '__main__':
    run()
