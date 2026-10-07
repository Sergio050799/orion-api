#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_historicas.py — Importa 241 flotas historicas a carpetas (EN ESTUDIO, OFERTADA, RECHAZADA).
Idempotente: no duplica si el nombre ya existe.
Compatible Python 3.8+
"""
import sqlite3, json, os, uuid, unicodedata
from datetime import datetime

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion-api/data/orion.db')

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()

CORREDOR_KEYS = [
    (['aon'],                 'AON'),
    (['aragones'],            'ARAGONES Y CEBORIAN'),
    (['atsyr'],               'ATSYR CORREDURÍA DE SEGUROS'),
    (['bidasoa'],             'BIDASOA'),
    (['mds'],                 'MDS RISK SOLUTIONS, S.L. (CE)'),
    (['cotasegur'],           'COTASEGUR SL'),
    (['delta'],               'DELTA CORREDURIA'),
    (['ersm'],                'ERSM'),
    (['junyent'],             "JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L."),
    (['ferreiros'],           'JOSEFINA FERREIROS SANCHEZ-GUISANDE'),
    (['larrea'],              'LARREA & BAREA CORREDURÍA DE SEGUROS, S.L.'),
    (['pique'],               'M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.'),
    (['minguez'],             'MINGUEZ SAEZ BROKERS, S.L.'),
    (['molyma'],              'MOLYMA, S.A. CORREDURIA DE SEGUROS'),
    (['pedro'],               'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.'),
    (['premium'],             'PREMIUM QUALITY INVESTMENTS, S.L.'),
    (['montagut'],            'SÁEZ DE MONTAGUT & MORENO'),
    (['willis'],              'WILLIS IBERIA CORREDURIA DE SEGUROS Y REASEGUROS SA'),
    (['ruizdominguez'],       'CORREDURIA DE SEGUROS RUIZ DOMINGUEZ 2000, S.L.'),
    (['ecocasbroker'],        'ECOCASBROKER, S.L.'),
    (['multigestion'],        'MULTIGESTIÓN ASEGURADORA, CORREDURÍA DE SEGUROS SL'),
    (['basurte'],             "BASURTE CORREDORIA D'ASSEGURANCES, S.L."),
    (['centregestor'],        'CENTRE GESTOR LLEIDA, S.A.'),
    (['gesa'],                'GESA MEDIACIÓN, SLU'),
    (['confide'],             'CONFIDE'),
    (['alcosegur'],           'ALCOSEGUR'),
    (['aenus'],               'AENUS'),
    (['mata'],                'MATA GESTIÓN'),
    (['anagan'],              'ANAGAN'),
    (['platinum'],            'PLATINUM'),
    (['marimon'],             'MARIMON'),
    (['calabuig'],            'CALABUIG'),
    (['peris'],               'PERIS'),
    (['vidasr'],              'VIDA SR'),
    (['iurisbroker'],         'IURISBROKER'),
    (['bfseguros'],           'BFSEGUROS'),
    (['brokers20'],           'BROKERS 20 MEDITERRANEA'),
    (['roig'],                'ROIG'),
    (['drij'],                'DRIJ CONSULTING'),
    (['hc'],                  'HC SEGUROS'),
    (['mares'],               'MARES'),
    (['proyectolider'],       'PROYECTO LIDER'),
    (['garciaochoa'],         'GARCIA OCHOA'),
    (['asmeval'],             'ASMEVAL'),
    (['kideka'],              'KIDEKA'),
    (['terranea'],            'TERRANEA'),
    (['mga'],                 'MGA'),
    (['assegura'],            'ASSEGURA CORREDURÍA'),
    (['davan'],               'DAVAN SEGUR'),
    (['gada'],                'GADA'),
    (['mocholi'],             'MOCHOLI'),
]

HISTORICAS = [
    ('', 'Muriel herrera', 'RECHAZADA', ''),
    ('', 'AMBULANCIAS DOMINGO', 'RECHAZADA', ''),
    ('confide', 'DAV S.L', 'RECHAZADA', ''),
    ('gesa', 'PRIMAFRIO', 'RECHAZADA', ''),
    ('gesa', 'RENTAFRIO', 'RECHAZADA', ''),
    ('', 'MEMORA', 'RECHAZADA', 'B85012441'),
    ('', 'ONDARA', 'RECHAZADA', ''),
    ('ersm', 'ALUMINIOS VALVERDEL DEL VALLES S.L', 'RECHAZADA', ''),
    ('alcosegur', 'Pan De Panes Aviva', 'RECHAZADA', ''),
    ('pedro', 'GRUAS PEDROSA', 'RECHAZADA', ''),
    ('aragones', 'Grupo Cron Logistica SLU', 'RECHAZADA', ''),
    ('molyma', 'GRUPO PENTA LOGIS, S.L', 'RECHAZADA', ''),
    ('', 'JESMAR ASTEC SL', 'RECHAZADA', ''),
    ('platinum', 'JOTPRO ELEVACION', 'RECHAZADA', ''),
    ('willis', 'MAÑERO TRANSPORTES LOGÍSTICA', 'RECHAZADA', 'B06623128'),
    ('aon', 'OCTAVIANO PALOMO', 'RECHAZADA', 'B40215402'),
    ('pique', 'pa igulada', 'RECHAZADA', ''),
    ('pique', 'placer gastronomico', 'RECHAZADA', ''),
    ('mds', 'RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT)', 'RECHAZADA', ''),
    ('willis', 'TOLEDANO FRESH SL', 'RECHAZADA', ''),
    ('molyma', 'TRANSDIOR, S.L', 'RECHAZADA', ''),
    ('', 'TRANSPORTES F. URIARTE', 'RECHAZADA', ''),
    ('molyma', 'TRANSPORTES MATEI FLORIN', 'RECHAZADA', ''),
    ('aon', 'AGENCIA TRANSPORTES ROBLES SA', 'RECHAZADA', 'A25042888'),
    ('aon', 'AKZO NOBEL', 'RECHAZADA', ''),
    ('willis', 'Albia Servicios Funerarios', 'RECHAZADA', ''),
    ('aon', 'ALIMERKA S.A', 'RECHAZADA', ''),
    ('bfseguros', 'ALMA ROAD SL', 'RECHAZADA', ''),
    ('molyma', 'ALVANA TRANSPORTES PERSONALIZADOS, S.L', 'RECHAZADA', ''),
    ('', 'AMBULANCIAS HABICHUELA', 'RECHAZADA', ''),
    ('', 'ANI CONSTRUCCIONES Y CONTRATAS', 'RECHAZADA', ''),
    ('', 'ANI CONSTRUCCIONES Y CONTRATAS SL', 'RECHAZADA', ''),
    ('larrea', 'ARRIETA LEAL Y TOMAS ARRIETA', 'RECHAZADA', ''),
    ('molyma', 'ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR', 'RECHAZADA', ''),
    ('aon', 'AUTOS VELASCO', 'RECHAZADA', ''),
    ('proyectolider', 'AVIMOLSA PROYECTO LIDER', 'RECHAZADA', ''),
    ('larrea', 'AYUNTAMIENTO DE SAGUNTO', 'RECHAZADA', ''),
    ('willis', 'AYUNTAMIENTO DEL BOALO WILLIS', 'RECHAZADA', ''),
    ('willis', 'AZVI, SA', 'RECHAZADA', ''),
    ('platinum', 'BOMBEOS MARBELLA', 'RECHAZADA', ''),
    ('willis', 'CALDERON Y RAMOS', 'RECHAZADA', ''),
    ('molyma', 'CAMIONAJE SL', 'RECHAZADA', ''),
    ('willis', 'CAMPEZO OBRAS Y SERVICIOS', 'RECHAZADA', ''),
    ('larrea', 'CARAVANAS ALQUILER LIBERTY ROAD', 'RECHAZADA', ''),
    ('premium', 'CARMOMATRANS  LOGISTICA V JORGE', 'RECHAZADA', ''),
    ('willis', 'CIRAC LOGISTICA', 'RECHAZADA', ''),
    ('peris', 'COEXA', 'RECHAZADA', ''),
    ('willis', 'Comercial Avícola Porcina SA', 'RECHAZADA', ''),
    ('vidasr', 'COMPAÑÍA EUROPEA DE VIAJEROS', 'RECHAZADA', ''),
    ('marimon', 'CONSTRUCCIONES SABATER', 'RECHAZADA', 'A08578395'),
    ('willis', 'COOPERATIVA AGRARIA SAN ISIDRO', 'RECHAZADA', ''),
    ('aon', 'DELIKIA AON', 'RECHAZADA', ''),
    ('pique', 'DIPRIMSA', 'RECHAZADA', ''),
    ('aon', 'DISBASE', 'RECHAZADA', ''),
    ('aon', 'DURAN GARRABE', 'RECHAZADA', ''),
    ('aon', 'EL MOSCA', 'RECHAZADA', ''),
    ('', 'ETG CIMENTACIONES', 'RECHAZADA', ''),
    ('molyma', 'EUROLOGIN EXPRESS', 'RECHAZADA', ''),
    ('molyma', 'EXCAVACIONES Y TRANSPORTES MOVITEXGA', 'RECHAZADA', ''),
    ('premium', 'FERMALUX S.L', 'RECHAZADA', ''),
    ('willis', 'FERROVIAL', 'RECHAZADA', ''),
    ('molyma', 'FESARU', 'RECHAZADA', ''),
    ('', 'fibratel UNOCORRE', 'RECHAZADA', ''),
    ('aon', 'FIRA CIRCUITS SL', 'RECHAZADA', ''),
    ('mds', 'FLOTA LIÑAGAR', 'RECHAZADA', ''),
    ('willis', 'FLOTA NUTRAVE', 'RECHAZADA', ''),
    ('pique', 'FLOTA PROSEÑAL', 'RECHAZADA', ''),
    ('iurisbroker', 'FLOTA RICARDO FUENTES E HIJOS', 'RECHAZADA', ''),
    ('willis', 'FLOTA TRANJOFE Y TEM', 'RECHAZADA', ''),
    ('calabuig', 'FLOTA TRANSRIBAL, SL', 'RECHAZADA', ''),
    ('pique', 'FORESTAL SOLIVA', 'RECHAZADA', 'B17656133'),
    ('montagut', 'FORZA HORMIGONES', 'RECHAZADA', ''),
    ('aon', 'FRAIKIN', 'RECHAZADA', 'W0017646A'),
    ('larrea', 'FRIO ALVAREZ SANCHEZ', 'RECHAZADA', ''),
    ('', 'GAMBIN CANARIAS', 'RECHAZADA', ''),
    ('platinum', 'GARCIA Y ATOCHA', 'RECHAZADA', ''),
    ('', 'GLASS LOGISTIC VLC SL', 'RECHAZADA', 'B19939222'),
    ('aon', 'GLOBAL SALCAI UTINSA', 'RECHAZADA', ''),
    ('aon', 'GLOBALIA', 'RECHAZADA', ''),
    ('vidasr', 'GOCON', 'RECHAZADA', ''),
    ('vidasr', 'GOCON SL', 'RECHAZADA', ''),
    ('molyma', 'GOYBER GRUPO LOGISTICO', 'RECHAZADA', ''),
    ('aon', 'GRUPIVAZGLE AUTO RENTING (LUGO) AON', 'RECHAZADA', 'B27480581'),
    ('aon', 'GRUPO BABE', 'RECHAZADA', ''),
    ('gesa', 'GRUPO BELZUNCES GESA', 'RECHAZADA', ''),
    ('willis', 'GRUPO CAMPAL', 'RECHAZADA', ''),
    ('aon', 'GRUPO COREN', 'RECHAZADA', ''),
    ('aon', 'GRUPO DAVILA', 'RECHAZADA', ''),
    ('aon', 'GRUPO KINETICO', 'RECHAZADA', ''),
    ('aon', 'GRUPO MAHOU', 'RECHAZADA', ''),
    ('willis', 'GRUPO MIGUEL RAMON', 'RECHAZADA', ''),
    ('aon', 'Grupo Molinero', 'RECHAZADA', ''),
    ('aon', 'GRUPO SADISA', 'RECHAZADA', ''),
    ('willis', 'GRUPO SERVIMAN', 'RECHAZADA', ''),
    ('', 'GRUPO TOTAL 2000, S.A', 'RECHAZADA', ''),
    ('molyma', 'GRUPO', 'RECHAZADA', ''),
    ('aon', 'GRUPO5', 'RECHAZADA', ''),
    ('', 'HERMANOS MORAN', 'RECHAZADA', 'B85668390'),
    ('garciaochoa', 'HIJOS DE MARINO PALOMO', 'RECHAZADA', ''),
    ('willis', 'ID Energy Group, S.A flota WILLIS', 'RECHAZADA', ''),
    ('willis', 'INDUSTRIAS CARNICAS TELLO', 'RECHAZADA', ''),
    ('aon', 'ITP', 'RECHAZADA', ''),
    ('aon', 'JEN CONSTRUCCIONES RENOVABLES', 'RECHAZADA', ''),
    ('peris', 'Leche Río carretillas', 'RECHAZADA', ''),
    ('delta', 'LESMARC DISTRIBUCIONES SL', 'RECHAZADA', ''),
    ('', 'LOGISTIC RACHEL', 'RECHAZADA', ''),
    ('molyma', 'LOGISTICA TRANSALPYNA', 'RECHAZADA', ''),
    ('willis', 'LOGISTICA Y TRANSPORTES LDR', 'RECHAZADA', 'B86994159'),
    ('aenus', 'LOGISTICA Y TRANSPORTES LDR S.L', 'RECHAZADA', ''),
    ('willis', 'LOPEZ ASISTENCIA', 'RECHAZADA', ''),
    ('willis', 'LOTRANS SL', 'RECHAZADA', 'B60568730'),
    ('willis', 'MARIN GIMENEZ HERMANOS, S.A', 'RECHAZADA', ''),
    ('proyectolider', 'MIGUEL FERNANDEZ DEL ESTAL', 'RECHAZADA', ''),
    ('willis', 'MIGUEL RAMON, SL', 'RECHAZADA', ''),
    ('willis', 'MONEGAS SA', 'RECHAZADA', ''),
    ('premium', 'NATURENGLISH', 'RECHAZADA', ''),
    ('aon', 'NAVARRO HERMANOS, AON', 'RECHAZADA', ''),
    ('willis', 'NAVILAND CARGO ESPAGNE', 'RECHAZADA', ''),
    ('willis', 'Newport logisctics and trading', 'RECHAZADA', ''),
    ('willis', 'OCON', 'RECHAZADA', ''),
    ('willis', 'ONSELLA GLOBAL SERVICES', 'RECHAZADA', ''),
    ('willis', 'OSGA, S.L', 'RECHAZADA', 'B26266395'),
    ('aon', 'P&O', 'RECHAZADA', ''),
    ('willis', 'PREZERO', 'RECHAZADA', ''),
    ('gesa', 'PRIMAVIA EUROPE SL', 'RECHAZADA', 'B05503594'),
    ('', 'RECAMBIOS COLON CATARROJA', 'RECHAZADA', ''),
    ('aon', 'RECOLLIDES SELECTIVES JOFER,SL', 'RECHAZADA', ''),
    ('willis', 'RED BULL', 'RECHAZADA', 'B62776216'),
    ('aon', 'REMEDIOS TORRES SL', 'RECHAZADA', ''),
    ('aon', 'SAMAT ESPAÑA SA', 'RECHAZADA', ''),
    ('pique', 'SCHAEFFLER IBERIA', 'RECHAZADA', ''),
    ('aon', 'SERTRANS', 'RECHAZADA', ''),
    ('willis', 'TAE TRANSPORTS I SERVEIS INTEGRALS', 'RECHAZADA', ''),
    ('molyma', 'TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ', 'RECHAZADA', ''),
    ('pique', 'TECNO SEGURETAT ANOIA', 'RECHAZADA', ''),
    ('pique', 'TECNOMATIC CATALUNYA', 'RECHAZADA', ''),
    ('pique', 'TECNOVE PIQUE', 'RECHAZADA', ''),
    ('iurisbroker', 'TECOZAN', 'RECHAZADA', ''),
    ('molyma', 'TIP S.A INT. PIPA', 'RECHAZADA', ''),
    ('aon', 'TIRME', 'RECHAZADA', ''),
    ('marimon', 'TORRES SERVICIOS TECNICOS', 'RECHAZADA', ''),
    ('willis', 'TRANJOFE Y TEM', 'RECHAZADA', ''),
    ('', 'transportes bernadet', 'RECHAZADA', ''),
    ('', 'TRANSPORTS BERNADET', 'RECHAZADA', ''),
    ('molyma', 'TRANS MORDU', 'RECHAZADA', ''),
    ('willis', 'TRANS SARRIA SL', 'RECHAZADA', ''),
    ('calabuig', 'TRANSANDAMA Y SURIBITRANS', 'RECHAZADA', ''),
    ('pedro', 'TRANSCUÑA', 'RECHAZADA', ''),
    ('aon', 'TRANSOLVER FINANCE', 'RECHAZADA', ''),
    ('willis', 'TRANSPORT SIMÓN', 'RECHAZADA', 'B17033465'),
    ('mata', 'TRANSPORTES CALLIZO SA', 'RECHAZADA', 'A50102516'),
    ('molyma', 'TRANSPORTES ESPECIALES DOBLE A', 'RECHAZADA', ''),
    ('aon', 'TRANSPORTES HIRUMUGETA', 'RECHAZADA', 'B71110571'),
    ('molyma', 'TRANSPORTES M. A GUTIERREZ', 'RECHAZADA', ''),
    ('molyma', 'TRANSPORTES MANDIOLA', 'RECHAZADA', ''),
    ('pique', 'TRANSPORTES MARITIMOS ALCUDIA', 'RECHAZADA', ''),
    ('larrea', 'TRANSPORTES OLIVERA', 'RECHAZADA', ''),
    ('willis', 'TRANSPORTES VARELA', 'RECHAZADA', ''),
    ('assegura', 'TRANSPORTES Y LOGISTICA AVANZADA S.L', 'RECHAZADA', ''),
    ('molyma', 'TRANSTECO', 'RECHAZADA', ''),
    ('aon', 'AON', 'RECHAZADA', ''),
    ('aon', 'WILLIS', 'RECHAZADA', 'A39020805'),
    ('', 'TRUCK & WHEEL', 'RECHAZADA', 'B31619570'),
    ('', 'VICO DE LA DUEÑA', 'RECHAZADA', ''),
    ('aon', 'VIRTO', 'RECHAZADA', ''),
    ('aragones', 'AGUSTIN TALÓN', 'OFERTADA', ''),
    ('pedro', 'ALQUILER O TRANSPORTES ALCOTRANS', 'OFERTADA', ''),
    ('brokers20', 'ANDREU TRUCKS SL', 'OFERTADA', ''),
    ('aenus', 'ANTA Y JESUS Sl', 'OFERTADA', ''),
    ('roig', 'ARIDOS BOFILL', 'OFERTADA', ''),
    ('', 'ARIDOS HNOS CURANTA', 'OFERTADA', ''),
    ('', 'ATALAYAS PORT, S', 'OFERTADA', ''),
    ('ersm', 'CHICARRO TRANSPORTES SL', 'OFERTADA', ''),
    ('mocholi', 'CITROGEST', 'OFERTADA', ''),
    ('', 'COMERCIAL BI', 'OFERTADA', ''),
    ('pique', 'CONGELATS SALMA', 'OFERTADA', ''),
    ('pedro', 'CONSTRUCCIONES MATESANZ SANZ', 'OFERTADA', ''),
    ('molyma', 'El cafetero 0', 'OFERTADA', ''),
    ('', 'FELIX BUQUERIN SL', 'OFERTADA', ''),
    ('drij', 'G.S.L', 'OFERTADA', ''),
    ('aragones', 'GOHERTRANS LOGISTICA SL', 'OFERTADA', ''),
    ('molyma', 'GRUPO LOGISTICA FOREVER', 'OFERTADA', ''),
    ('aragones', 'Hermanos Hernandez Matas SL', 'OFERTADA', 'B16152175'),
    ('aragones', 'LOALTRANS', 'OFERTADA', 'B73503757'),
    ('pique', 'MAGNA STELLA', 'OFERTADA', 'B66919531'),
    ('molyma', 'O.T TRANSIT QUALITY, S.L', 'OFERTADA', ''),
    ('delta', 'SARATEKUA', 'OFERTADA', ''),
    ('delta', 'SERJA', 'OFERTADA', ''),
    ('molyma', 'SETOAN LOGISTICA Y TTE. INTERNACIONAL', 'OFERTADA', ''),
    ('', 'TOY CENTRE', 'OFERTADA', ''),
    ('cotasegur', 'TRANSELEZ', 'OFERTADA', 'B45867751'),
    ('larrea', 'TRANSMONTENEGRO', 'OFERTADA', ''),
    ('larrea', 'TRANSMONTENEGRO SL', 'OFERTADA', ''),
    ('molyma', 'TRANSPORTES DE CEREALES Y LEÑA', 'OFERTADA', ''),
    ('mata', 'TRANSPORTES P. SARASA', 'OFERTADA', 'B22279251'),
    ('mares', 'TTE.S.J.GAMIZ', 'OFERTADA', ''),
    ('gada', 'TTES. PATRICIO', 'OFERTADA', ''),
    ('pique', 'WITTMANN TECHNOLOGY SPAIN', 'OFERTADA', ''),
    ('', 'ABONOS Y SEMILLAS SA', 'EN ESTUDIO', 'A09307935'),
    ('alcosegur', 'AFANDECOR, AFANMONTAJES Y APLOMO', 'EN ESTUDIO', ''),
    ('asmeval', 'ALTIPLANO TRANS', 'EN ESTUDIO', ''),
    ('', 'AMURIUZA CUBIERTAS', 'EN ESTUDIO', 'B48519425'),
    ('willis', 'ANSAREO AEB', 'EN ESTUDIO', 'B48619258'),
    ('hc', 'botanicas de levante', 'EN ESTUDIO', ''),
    ('molyma', 'CABEZOLARI', 'EN ESTUDIO', ''),
    ('aragones', 'CAMILO Y DEL ARCO SL', 'EN ESTUDIO', 'B87373643'),
    ('', 'CARA Y TTES.DE BURGOS', 'EN ESTUDIO', 'B09289406'),
    ('larrea', 'CIRAC LOGÍSTICA', 'EN ESTUDIO', ''),
    ('', 'cis flota agustin gonzalez', 'EN ESTUDIO', ''),
    ('', 'CONGELATS SALMA, S.L', 'EN ESTUDIO', ''),
    ('', 'CONTENEDORES CALVO VARGAS', 'EN ESTUDIO', ''),
    ('mata', 'CONTRATAS PÚBLICAS DEL NORTE', 'EN ESTUDIO', ''),
    ('', 'FLOTA AFANDECOR, AFANMONTAJES Y APLOMO', 'EN ESTUDIO', ''),
    ('', 'FRILESA & LEBROK', 'EN ESTUDIO', ''),
    ('mga', 'GARRIGA OBRES I SERVEIS, S.L', 'EN ESTUDIO', ''),
    ('mata', 'GESTIÓN DE INFRAESTRUCTURAS CIVILES', 'EN ESTUDIO', ''),
    ('gesa', 'GRUPO VIGILANT A30085401', 'EN ESTUDIO', 'A30085401'),
    ('mata', 'hidalgo', 'EN ESTUDIO', ''),
    ('pique', 'IDM', 'EN ESTUDIO', ''),
    ('pedro', 'JACINTO PEREZ', 'EN ESTUDIO', ''),
    ('aragones', 'LA ABUELA MARGA', 'EN ESTUDIO', ''),
    ('kideka', 'Nuñez Movilla S.L', 'EN ESTUDIO', 'B09259839'),
    ('premium', 'RECUPERACIONES MORALES', 'EN ESTUDIO', 'B84174341'),
    ('pique', 'REHABILITACIONS PONS', 'EN ESTUDIO', ''),
    ('', 'Remar', 'EN ESTUDIO', ''),
    ('molyma', 'RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS', 'EN ESTUDIO', ''),
    ('cotasegur', 'SANCHEZ VAZQUEZ', 'EN ESTUDIO', ''),
    ('anagan', 'SERVICIO DE ALQUILER CAIDERO S.L', 'EN ESTUDIO', ''),
    ('', 'SERVICIOS LOGISTICOS DEL SUR', 'EN ESTUDIO', ''),
    ('', 'Tea Tek en Personal Family Office', 'EN ESTUDIO', ''),
    ('molyma', 'TRACTOLE,S.A', 'EN ESTUDIO', ''),
    ('aenus', 'TRANS JJ JUNDE SL', 'EN ESTUDIO', ''),
    ('terranea', 'TRANSPORTE SEGOVIA', 'EN ESTUDIO', ''),
    ('willis', 'callejero bueno', 'EN ESTUDIO', ''),
    ('', 'TRANSPORTES JABOSIO', 'EN ESTUDIO', 'B02239952'),
    ('molyma', 'TRANSPORTES JACINTO DEL POZO', 'EN ESTUDIO', ''),
    ('molyma', 'TRANSPORTES MATAS', 'EN ESTUDIO', ''),
    ('', 'TTES.DELFIN ESPINOSA, S.L + LOGIESBER', 'EN ESTUDIO', ''),
    ('mds', 'UNECOL ADHESIVE IDEAS', 'EN ESTUDIO', ''),
    ('mata', 'VIDAL OBRAS Y SERVICIOS', 'EN ESTUDIO', ''),
    ('pique', 'ENVIRORENT XXI S L', 'RECHAZADA', ''),
]


def get_corredor_id(conn, clave, cache, now):
    if not clave:
        return None
    for keywords, canonical in CORREDOR_KEYS:
        if clave in keywords:
            # buscar en cache
            for nombre_bd, cid in list(cache.items()):
                if all(norm(k) in norm(nombre_bd) for k in keywords):
                    return cid
            # crear
            new_id = 'corr_' + uuid.uuid4().hex[:12]
            conn.execute(
                "INSERT INTO corredores (id, nombre, creado_por, created_at, updated_at) VALUES (?,?,?,?,?)",
                [new_id, canonical, 'SPIKE', now, now]
            )
            cache[canonical] = new_id
            print(f'  CORREDOR CREADO: {canonical}')
            return new_id
    return None

def run():
    if not os.path.exists(DB_PATH):
        print('ERROR: No se encuentra la BD en', DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    print('=== import_historicas ===')
    print('DB:', DB_PATH)

    # Cache corredores
    rows = conn.execute('SELECT id, nombre FROM corredores ORDER BY nombre').fetchall()
    cache = {r['nombre']: r['id'] for r in rows}

    # Nombres ya en carpetas (normalizados) para evitar duplicados
    existentes = set()
    for r in conn.execute('SELECT nombre FROM carpetas').fetchall():
        existentes.add(norm(r['nombre']))

    ok = skip = err = 0
    for clave, nombre, estado, cif in HISTORICAS:
        if norm(nombre) in existentes:
            skip += 1
            continue
        try:
            corredor_id = get_corredor_id(conn, clave, cache, now)
            cid = 'carp_' + uuid.uuid4().hex[:14]
            data = {
                'id': cid, 'nombre': nombre, 'estado': estado,
                'corredor_id': corredor_id,
                'header': {'tomador': nombre, 'cif': cif, 'actividad': '',
                           'fechaVencimiento': '', 'fechaInicio': ''},
                'trabajo': [], 'original': [], 'oferta': [], 'observaciones': '',
                'createdAt': now, 'updatedAt': now,
            }
            conn.execute(
                "INSERT INTO carpetas (id, nombre, estado, corredor_id, creado_por, created_at, updated_at, data) VALUES (?,?,?,?,?,?,?,?)",
                [cid, nombre, estado, corredor_id, 'HISTORICO', now, now, json.dumps(data, ensure_ascii=False)]
            )
            existentes.add(norm(nombre))
            ok += 1
        except Exception as e:
            print(f'  ERROR {nombre}: {e}')
            err += 1

    conn.commit()
    conn.close()
    print('Insertadas: %d  |  Saltadas: %d  |  Errores: %d' % (ok, skip, err))
    print('=== FIN ===')

if __name__ == '__main__':
    run()
