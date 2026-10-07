#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpia historicas + CONTRATADAS existentes e inserta el portfolio real.
Compatible Python 3.8+
"""
import sqlite3, json, os, uuid, unicodedata
from datetime import datetime

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion-api/data/orion.db')

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()

# keywords -> nombre definitivo
CORREDOR_KEYS = [
    (['aon'],                   'AON'),
    (['aragones'],              'ARAGONES Y CEBORIAN'),
    (['atsyr'],                 'ATSYR CORREDURÍA DE SEGUROS'),
    (['bidasoa'],               'BIDASOA'),
    (['mds'],                   'MDS'),
    (['cotasegur'],             'COTASEGUR SL'),
    (['delta'],                 'DELTA CORREDURIA'),
    (['ersm'],                  'ERSM'),
    (['junyent'],               "JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L."),
    (['ferreiros'],             'JOSEFINA FERREIROS SANCHEZ-GUISANDE'),
    (['larrea'],                'LARREA & BAREA CORREDURÍA DE SEGUROS, S.L.'),
    (['pique'],                 'M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.'),
    (['minguez'],               'MINGUEZ SAEZ BROKERS, S.L.'),
    (['molyma'],                'MOLYMA, S.A. CORREDURIA DE SEGUROS'),
    (['pedro', 'quel'],         'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.'),
    (['pedro', 'martinez'],     'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.'),
    (['premium'],               'PREMIUM QUALITY INVESTMENTS, S.L.'),
    (['montagut'],              'SÁEZ DE MONTAGUT & MORENO'),
    (['saez', 'moreno'],        'SÁEZ DE MONTAGUT & MORENO'),
    (['willis'],                'WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA'),
    (['ruizdominguez'],         'CORREDURIA DE SEGUROS RUIZ DOMINGUEZ 2000, S.L.'),
    (['ecocasbroker'],          'ECOCASBROKER, S.L.'),
    (['multigestion'],          'MULTIGESTIÓN ASEGURADORA, CORREDURÍA DE SEGUROS SL'),
    (['basurte'],               "BASURTE CORREDORIA D'ASSEGURANCES, S.L."),
    (['centregestor'],          'CENTRE GESTOR LLEIDA, S.A.'),
    (['gesa'],                  'GESA MEDIACIÓN, SLU'),
]

# (corredor_clave, flota, fecha_vto)
FLOTAS = [
    ('aon',       'TRANSPORTES HERMANOS LAREDO, SA',            '31/03/2027'),
    ('aragones',  'TRES CAMPANAS',                              '01/07/2027'),
    ('aragones',  'TRANSPORTES ISIDRO SAN ROMAN E HIJOS SL',   '07/08/2027'),
    ('atsyr',     'FUNDACION BANCO DE ALIMENTOS DE MADRID',     '01/06/2027'),
    ('bidasoa',   'TRANSPORTES HIRUMUGETA',                     '01/10/2027'),
    ('bidasoa',   'INTEROPTRANS SL',                            '01/10/2027'),
    ('mds',       'ALVEMACO',                                   '31/12/2026'),
    ('cotasegur', 'MARMOLES TOLEDANOS',                         '01/10/2027'),
    ('delta',     'IGNACIO LIMA ZABALEGUI',                     '14/09/2027'),
    ('ersm',      'EMBOTITS PORTELLA SL',                       '11/09/2027'),
    ('junyent',   'GRUAS Y PORTA VEHICULOS PEDRO SL',           '10/07/2027'),
    ('ferreiros', 'TRANSPORTES VALLE DEL OJA SL',               '29/05/2027'),
    ('larrea',    'IMPULS WORLD LOGISTICS SL',                  '01/10/2027'),
    ('pique',     'PSM VIVER DEL REC SL',                       '17/07/2027'),
    ('minguez',   'TRANSPORTES BRAMAR',                         '01/01/2027'),
    ('molyma',    'BENAYAS SERVICIOS LOGISTICOS SL',            '01/09/2027'),
    ('molyma',    'ALBERTO Y ANTONIO ESTRELLA GRANO DE ORO',    '01/09/2027'),
    ('molyma',    'ON-RED TRUCK LOGISTICS',                     '17/05/2027'),
    ('molyma',    'SERGETRANS SL',                              '01/07/2027'),
    ('molyma',    'SOTO ECOTRANS SL',                           '25/03/2027'),
    ('molyma',    'TRANSPORTES BAS 2023 SL',                    '01/04/2027'),
    ('molyma',    'TRANSPORTES FARMACOLOGICOS CASTILLA SL',     '24/02/2027'),
    ('pedro',     'LOGISTICA Y TRANSPORTES DE PEDRO',           '01/07/2027'),
    ('pedro',     'DPM LOGISTICA 1966 SL',                      '01/07/2027'),
    ('premium',   'LOGISTICA NOGUERAS SL',                      '01/05/2027'),
    ('premium',   'TRANSPORTES DALMUR SL',                      '31/12/2026'),
    ('premium',   'AGUSTIN MARTINEZ SL',                        '09/06/2027'),
    ('montagut',  'SEJERCON SL',                                '20/07/2027'),
    ('willis',          'GEODIS RT SPAIN SA',                              '01/01/2027'),
    ('willis',          'TOPFORM SL',                                      '31/12/2026'),
    # FLOTAS TITAN 2025-2026
    ('ruizdominguez',   'ALBIA GESTION DE SERVICIOS, S.L.',                '01/04/2027'),
    ('ecocasbroker',    'AMBULANCIAS CSA',                                  '30/09/2027'),
    ('multigestion',    'CAFES PONT, SL',                                   '31/12/2026'),
    ('basurte',         "CAN CET CENTRE D'INSERCIÓ SOCIO-LABORAL SL",       '16/07/2027'),
    ('ruizdominguez',   'ITMEE & MANTENIMIENTO S.L.',                       '02/12/2026'),
    ('centregestor',    'MVG TECHNOLOGY, SL',                               '07/05/2027'),
    ('ruizdominguez',   'SAURATRANS, S.L.',                                 '31/12/2026'),
    ('pique',           'SUMINISTROS ESMERALDA',                            '01/01/2027'),
    ('pique',           'TRANSSESROVIRES SL',                               '01/02/2027'),
    ('gesa',            'TRANSPORTES HERMANOS HERNANDEZ SL',                '31/12/2026'),
]

def get_or_create_corredor(conn, clave, cache, now):
    clave_norm = norm(clave)
    # buscar en cache normalizado
    for nombre_bd, cid in list(cache.items()):
        if clave_norm in norm(nombre_bd):
            return cid
    # buscar con keywords en CORREDOR_KEYS
    for keywords, canonical in CORREDOR_KEYS:
        if clave_norm in keywords or any(clave_norm == k for k in keywords):
            # buscar canonical en cache
            for nombre_bd, cid in list(cache.items()):
                if all(k in norm(nombre_bd) for k in keywords):
                    # actualizar nombre si es diferente
                    if nombre_bd != canonical:
                        conn.execute("UPDATE corredores SET nombre=? WHERE id=?", [canonical, cid])
                        cache[canonical] = cache.pop(nombre_bd)
                        print(f"  CORREDOR: '{nombre_bd}' -> '{canonical}'")
                    return cache[canonical]
            # no encontrado — crear
            new_id = 'corr_' + uuid.uuid4().hex[:12]
            conn.execute(
                "INSERT INTO corredores (id, nombre, creado_por, created_at, updated_at) VALUES (?,?,?,?,?)",
                [new_id, canonical, 'SPIKE', now, now]
            )
            cache[canonical] = new_id
            print(f"  CORREDOR CREADO: '{canonical}'")
            return new_id
    # fallback: crear con clave como nombre
    new_id = 'corr_' + uuid.uuid4().hex[:12]
    conn.execute(
        "INSERT INTO corredores (id, nombre, creado_por, created_at, updated_at) VALUES (?,?,?,?,?)",
        [new_id, clave.upper(), 'SPIKE', now, now]
    )
    cache[clave.upper()] = new_id
    print(f"  CORREDOR NUEVO (fallback): '{clave.upper()}'")
    return new_id

def run():
    if not os.path.exists(DB_PATH):
        print("ERROR: No se encuentra la BD en", DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    print("=== fix_contratadas v3 ===")
    print("DB:", DB_PATH)

    # Corredores actuales
    rows = conn.execute("SELECT id, nombre FROM corredores ORDER BY nombre").fetchall()
    cache = {r['nombre']: r['id'] for r in rows}
    print(f"\nCorredores en BD ({len(rows)}):")
    for r in rows:
        print(f"  {r['nombre']}")

    # Limpiar historicas
    n_hist = conn.execute("SELECT COUNT(*) FROM flotas_historicas").fetchone()[0]
    conn.execute("DELETE FROM flotas_historicas")
    print(f"\nHistoricas eliminadas: {n_hist}")

    # Limpiar CONTRATADAS
    n_cont = conn.execute("SELECT COUNT(*) FROM carpetas WHERE estado='CONTRATADA'").fetchone()[0]
    conn.execute("DELETE FROM carpetas WHERE estado='CONTRATADA'")
    print(f"Carpetas CONTRATADA eliminadas: {n_cont}")
    conn.commit()

    # Insertar nuevas
    print(f"\nInsertando {len(FLOTAS)} flotas...")
    ok = 0
    for clave, nombre_flota, fecha_vcto in FLOTAS:
        corredor_id = get_or_create_corredor(conn, clave, cache, now)
        cid = 'carp_' + uuid.uuid4().hex[:14]
        data = {
            'id': cid, 'nombre': nombre_flota, 'estado': 'CONTRATADA',
            'corredor_id': corredor_id,
            'header': {'fechaVencimiento': fecha_vcto, 'tomador': '', 'cif': '', 'actividad': '', 'fechaInicio': ''},
            'trabajo': [], 'original': [], 'oferta': [], 'observaciones': '',
            'createdAt': now, 'updatedAt': now,
        }
        conn.execute(
            "INSERT INTO carpetas (id, nombre, estado, corredor_id, creado_por, created_at, updated_at, data) VALUES (?,?,'CONTRATADA',?,?,?,?,?)",
            [cid, nombre_flota, corredor_id, 'SPIKE', now, now, json.dumps(data, ensure_ascii=False)]
        )
        ok += 1
        print(f"  OK: {nombre_flota} ({clave}) vcto={fecha_vcto}")

    conn.commit()
    conn.close()
    print(f"\nInsertadas: {ok}/{len(FLOTAS)}")
    print("=== FIN ===")

if __name__ == '__main__':
    run()
