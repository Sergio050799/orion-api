#!/usr/bin/env python3
"""
Migration v2: Insertar 30 flotas contratadas con corredor asignado.
NO elimina carpetas existentes. Solo inserta las que faltan.
Ejecutar: python fix_contratadas.py
"""
import sqlite3, json, os, uuid, unicodedata
from datetime import datetime

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')


def norm(s: str) -> str:
    """Normaliza: minusculas, sin acentos, sin puntuacion extra."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()


# Palabras clave unicas por corredor → nombre definitivo en BD
CORREDOR_MAP = [
    (['aon'],                                          'AON'),
    (['aragones', 'ceborian'],                         'ARAGONES Y CEBORIAN'),
    (['atsyr'],                                        'ATSYR CORREDURÍA DE SEGUROS'),
    (['bidasoa'],                                      'BIDASOA'),
    (['mds'],                                          'MDS'),
    (['cotasegur'],                                    'COTASEGUR SL'),
    (['delta', 'corre'],                               'DELTA CORREDURIA'),
    (['ersm'],                                         'ERSM'),
    (['junyent'],                                      "JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L."),
    (['ferreiros'],                                    'JOSEFINA FERREIROS SANCHEZ-GUISANDE'),
    (['larrea'],                                       'LARREA & BAREA CORREDURÍA DE SEGUROS, S.L.'),
    (['pique', 'corre'],                               'M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.'),
    (['minguez'],                                      'MINGUEZ SAEZ BROKERS, S.L.'),
    (['molyma'],                                       'MOLYMA, S.A. CORREDURIA DE SEGUROS'),
    (['pedro', 'quel'],                                'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.'),
    (['premium', 'quality'],                           'PREMIUM QUALITY INVESTMENTS, S.L.'),
    (['saez', 'montagut'],                             'SÁEZ DE MONTAGUT & MORENO'),
    (['montagut', 'moreno'],                           'SÁEZ DE MONTAGUT & MORENO'),
    (['willis'],                                       'WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA'),
]

# (nombre_corredor_clave, nombre_flota, fecha_vencimiento)
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


def find_corredor_id(conn, target_nombre: str, corr_cache: dict) -> str | None:
    """Busca corredor por nombre normalizado. Si no existe, lo crea."""
    # 1. Match exacto (ya normalizado del update anterior)
    if target_nombre in corr_cache:
        return corr_cache[target_nombre]

    # 2. Match por palabras clave (normalizado)
    target_norm = norm(target_nombre)
    for keywords, canonical in CORREDOR_MAP:
        if all(kw in target_norm for kw in keywords):
            # Buscar en cache con el nombre canonico
            if canonical in corr_cache:
                return corr_cache[canonical]
            # Buscar por keywords en BD
            for nombre_bd, cid in corr_cache.items():
                nombre_bd_norm = norm(nombre_bd)
                if all(kw in nombre_bd_norm for kw in keywords):
                    # Actualizar nombre a canonico
                    conn.execute("UPDATE corredores SET nombre=? WHERE id=?", [canonical, cid])
                    corr_cache[canonical] = cid
                    del corr_cache[nombre_bd]
                    print(f"   ✎ Corredor renombrado: '{nombre_bd}' → '{canonical}'")
                    return cid

    # 3. No encontrado — crear corredor nuevo
    new_id = 'corr_' + uuid.uuid4().hex[:16]
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    conn.execute("""
        INSERT INTO corredores (id, nombre, creado_por, created_at, updated_at)
        VALUES (?, ?, 'SPIKE', ?, ?)
    """, [new_id, target_nombre, now, now])
    corr_cache[target_nombre] = new_id
    print(f"   ✚ Corredor creado: '{target_nombre}' (id={new_id})")
    return new_id


def run():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"\n=== fix_contratadas v2 === DB: {DB_PATH}\n")

    # ── Mostrar corredores actuales ───────────────────────────────────────────
    rows_corr = conn.execute("SELECT id, nombre FROM corredores ORDER BY nombre").fetchall()
    print(f"Corredores en BD ({len(rows_corr)}):")
    corr_cache = {}
    for r in rows_corr:
        print(f"  [{r['id']}] {r['nombre']}")
        corr_cache[r['nombre']] = r['id']

    print()

    # ── Flotas CONTRATADA actuales (no tocar) ─────────────────────────────────
    existing = conn.execute(
        "SELECT nombre FROM carpetas WHERE estado='CONTRATADA'"
    ).fetchall()
    existing_names = {norm(r['nombre']) for r in existing}
    print(f"Carpetas CONTRATADA existentes ({len(existing_names)}): {[r['nombre'] for r in existing]}\n")

    # ── Insertar flotas nuevas ────────────────────────────────────────────────
    inserted = 0
    skipped  = 0
    for corredor_nombre, flota_nombre, fecha_vcto in FLOTAS:
        if norm(flota_nombre) in existing_names:
            print(f"   → Existe: '{flota_nombre}' (skip)")
            skipped += 1
            continue

        corredor_id = find_corredor_id(conn, corredor_nombre, corr_cache)

        carp_id = 'carp_' + uuid.uuid4().hex[:16]
        data = {
            'id': carp_id,
            'nombre': flota_nombre,
            'estado': 'CONTRATADA',
            'corredor_id': corredor_id,
            'header': {
                'fechaVencimiento': fecha_vcto,
                'tomador': '', 'cif': '', 'actividad': '', 'fechaInicio': '',
            },
            'trabajo': [], 'original': [], 'oferta': [],
            'observaciones': '',
            'createdAt': now, 'updatedAt': now,
        }
        conn.execute("""
            INSERT INTO carpetas (id, nombre, estado, corredor_id, creado_por, created_at, updated_at, data)
            VALUES (?, ?, 'CONTRATADA', ?, 'SPIKE', ?, ?, ?)
        """, [carp_id, flota_nombre, corredor_id, now, now,
              json.dumps(data, ensure_ascii=False)])
        inserted += 1
        corr_label = corredor_nombre.split()[0] if corredor_nombre else 'SIN_CORREDOR'
        print(f"   ✓ '{flota_nombre}' → {corr_label} | vcto {fecha_vcto}")

    conn.commit()
    conn.close()

    print(f"\nResultado: {inserted} flotas insertadas, {skipped} ya existían.")
    print("=== FIN ===\n")


if __name__ == '__main__':
    run()
