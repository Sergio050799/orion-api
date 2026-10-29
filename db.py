import sqlite3
import json
import os
import hashlib
import binascii

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')


# ─── Password hashing (PBKDF2-SHA256) ─────────────────────────────────────────

def hash_password(password: str) -> tuple:
    salt = binascii.hexlify(os.urandom(16)).decode()
    h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 260_000).hex()
    return h, salt


def verify_password(password: str, stored_hash: str, salt) -> bool:
    if salt is None:
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == stored_hash
    h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), str(salt).encode('utf-8'), 260_000).hex()
    return h == stored_hash

_HASH_DEFAULT = '30f2bc83fcd6b4d3834e8950c1cd6addb82cc807fc0eca261fe718da79cbbea5'

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS usuarios (
    id            TEXT PRIMARY KEY,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt          TEXT DEFAULT NULL,
    rol           TEXT NOT NULL DEFAULT 'usuario',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS corredores (
    id            TEXT PRIMARY KEY,
    codigo        TEXT NOT NULL DEFAULT '',
    nombre        TEXT NOT NULL DEFAULT '',
    cif           TEXT NOT NULL DEFAULT '',
    domicilio     TEXT NOT NULL DEFAULT '',
    comision      REAL NOT NULL DEFAULT 0,
    periodicidad  TEXT NOT NULL DEFAULT 'mensual',
    forma_pago    TEXT NOT NULL DEFAULT '',
    contacto      TEXT NOT NULL DEFAULT '',
    email         TEXT NOT NULL DEFAULT '',
    telefono      TEXT NOT NULL DEFAULT '',
    observaciones TEXT NOT NULL DEFAULT '',
    sucursal      TEXT NOT NULL DEFAULT '',
    comercial     TEXT NOT NULL DEFAULT '',
    id_perceptor  TEXT NOT NULL DEFAULT '',
    creado_por    TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS carpetas (
    id            TEXT PRIMARY KEY,
    nombre        TEXT NOT NULL DEFAULT '',
    estado        TEXT NOT NULL DEFAULT 'EN ESTUDIO',
    cif           TEXT NOT NULL DEFAULT '',
    tomador       TEXT NOT NULL DEFAULT '',
    actividad     TEXT NOT NULL DEFAULT '',
    corredor_id   TEXT,
    creado_por    TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
    data          TEXT NOT NULL DEFAULT '{{}}'
);

CREATE INDEX IF NOT EXISTS idx_carpetas_corredor ON carpetas(corredor_id);
CREATE INDEX IF NOT EXISTS idx_carpetas_estado   ON carpetas(estado);
CREATE INDEX IF NOT EXISTS idx_carpetas_updated  ON carpetas(updated_at DESC);

CREATE TABLE IF NOT EXISTS vehiculos_silverdat (
    matricula      TEXT PRIMARY KEY,
    datos          TEXT NOT NULL,
    fecha_consulta TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS historial_silverdat (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula      TEXT NOT NULL,
    fecha_consulta TEXT NOT NULL DEFAULT (datetime('now')),
    consultado_por TEXT NOT NULL DEFAULT '',
    carpeta_id     TEXT NOT NULL DEFAULT '',
    carpeta_nombre TEXT NOT NULL DEFAULT '',
    corredor_id    TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_historial_sd_mat   ON historial_silverdat(matricula);
CREATE INDEX IF NOT EXISTS idx_historial_sd_fecha ON historial_silverdat(fecha_consulta DESC);

CREATE TABLE IF NOT EXISTS sesiones_activas (
    carpeta_id TEXT NOT NULL,
    username   TEXT NOT NULL,
    last_seen  TEXT NOT NULL,
    PRIMARY KEY (carpeta_id, username)
);

-- ── PRIMAS CONFIGURABLES ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS primas_config (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_vehiculo TEXT NOT NULL,
    cobertura     TEXT NOT NULL,
    ambito        TEXT NOT NULL DEFAULT 'nacional',
    prima         REAL NOT NULL DEFAULT 0,
    updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_by    TEXT NOT NULL DEFAULT '',
    UNIQUE(tipo_vehiculo, cobertura, ambito)
);

CREATE TABLE IF NOT EXISTS ajustes_config (
    clave       TEXT PRIMARY KEY,
    valor       REAL NOT NULL DEFAULT 0,
    descripcion TEXT NOT NULL DEFAULT '',
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── AUDITORÍA ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL DEFAULT '',
    accion  TEXT NOT NULL DEFAULT '',
    detalle TEXT NOT NULL DEFAULT '',
    ip      TEXT NOT NULL DEFAULT '',
    ts      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_audit_ts      ON audit_log(ts DESC);
CREATE INDEX IF NOT EXISTS idx_audit_usuario ON audit_log(usuario);

-- ── SESIÓN SILVERDAT COMPARTIDA ──────────────────────────────────────────────
-- Una sola fila (id=1). Cookie compartida entre instancias PM2.
CREATE TABLE IF NOT EXISTS silverdat_session (
    id           INTEGER PRIMARY KEY CHECK (id = 1),
    cookie       TEXT NOT NULL DEFAULT '',
    dat_id       TEXT NOT NULL DEFAULT '',
    logged_in_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── MOTOR DE PRIMAS — ESTADÍSTICAS MMT ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS mmt_stats (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    tipologia    TEXT NOT NULL,
    id_garantia  TEXT NOT NULL,
    id_cobertura TEXT NOT NULL,
    fecha_foto   TEXT NOT NULL,
    prima        REAL NOT NULL DEFAULT 0,
    coste        REAL NOT NULL DEFAULT 0,
    exposicion   REAL NOT NULL DEFAULT 0,
    lr           REAL,
    fq           REAL,
    stros        INTEGER NOT NULL DEFAULT 0,
    importado_at TEXT NOT NULL DEFAULT (datetime('now')),
    importado_por TEXT NOT NULL DEFAULT '',
    UNIQUE(tipologia, id_garantia, id_cobertura, fecha_foto)
);

CREATE INDEX IF NOT EXISTS idx_mmt_stats_tipo ON mmt_stats(tipologia, fecha_foto);

-- ── MOTOR DE PRIMAS — MAPEO TIPOLOGÍAS ────────────────────────────────────────
-- Mapea tipo_vehiculo de ORION (normalizado) a nombre de tipología en mmt_stats
CREATE TABLE IF NOT EXISTS mmt_tipologia_map (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    orion_tipo    TEXT NOT NULL UNIQUE,
    mmt_tipologia TEXT NOT NULL,
    categoria     INTEGER NOT NULL DEFAULT 1,
    notas         TEXT NOT NULL DEFAULT ''
);

-- ── MOTOR DE PRIMAS — PARÁMETROS ECONÓMICOS ──────────────────────────────────
CREATE TABLE IF NOT EXISTS motor_params (
    clave       TEXT PRIMARY KEY,
    valor       REAL,
    descripcion TEXT NOT NULL DEFAULT '',
    updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_by  TEXT NOT NULL DEFAULT ''
);

-- ── MOTOR DE PRIMAS — CATÁLOGO DE VEHÍCULOS MMT ───────────────────────────────
CREATE TABLE IF NOT EXISTS mmt_catalogo_vehiculos (
    id_veh         TEXT PRIMARY KEY,
    id_veh_base7   TEXT NOT NULL DEFAULT '',
    marca          TEXT NOT NULL DEFAULT '',
    modelo         TEXT NOT NULL DEFAULT '',
    version        TEXT NOT NULL DEFAULT '',
    id_clase       TEXT NOT NULL DEFAULT '',
    motorizacion   TEXT NOT NULL DEFAULT '',
    combustible    TEXT NOT NULL DEFAULT '',
    num_puertas    INTEGER NOT NULL DEFAULT 0,
    fec_ini_comerc TEXT NOT NULL DEFAULT '',
    fec_fin_comerc TEXT NOT NULL DEFAULT '',
    pff            REAL NOT NULL DEFAULT 0,
    pvp            REAL NOT NULL DEFAULT 0,
    pma            REAL NOT NULL DEFAULT 0,
    num_velocidades INTEGER NOT NULL DEFAULT 0,
    transmision    TEXT NOT NULL DEFAULT '',
    selec_riesgo   INTEGER NOT NULL DEFAULT 0,
    num_plazas_min INTEGER NOT NULL DEFAULT 0,
    num_plazas_max INTEGER NOT NULL DEFAULT 0,
    tara           REAL NOT NULL DEFAULT 0,
    kw             REAL NOT NULL DEFAULT 0,
    fec_carga      TEXT NOT NULL DEFAULT '',
    ts_update      TEXT NOT NULL DEFAULT '',
    importado_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_cat_veh_marca  ON mmt_catalogo_vehiculos(marca);
CREATE INDEX IF NOT EXISTS idx_cat_veh_clase  ON mmt_catalogo_vehiculos(id_clase);
CREATE INDEX IF NOT EXISTS idx_cat_veh_modelo ON mmt_catalogo_vehiculos(marca, modelo);

-- ── MOTOR DE PRIMAS — CATÁLOGO COBERTURAS MMT ────────────────────────────────
CREATE TABLE IF NOT EXISTS mmt_coberturas_catalog (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria   TEXT NOT NULL DEFAULT '',
    codigo_tipo TEXT NOT NULL DEFAULT '',
    garantia    TEXT,
    cobertura   TEXT,
    subcobertura TEXT,
    franquicia  TEXT,
    nombre      TEXT NOT NULL DEFAULT '',
    indem_max   REAL,
    UNIQUE(categoria, garantia, cobertura, subcobertura, franquicia)
);
CREATE INDEX IF NOT EXISTS idx_cob_cat ON mmt_coberturas_catalog(categoria, garantia, cobertura);

-- ── MOTOR DE PRIMAS — PRIMAS MEDIAS MMT ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS mmt_primas_medias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tipologia   TEXT NOT NULL DEFAULT '',
    id_garantia TEXT NOT NULL DEFAULT '',
    id_cobertura TEXT NOT NULL DEFAULT '',
    fecha_foto  TEXT NOT NULL DEFAULT '',
    prima_media REAL NOT NULL DEFAULT 0,
    fuente      TEXT NOT NULL DEFAULT 'Primas_medias_todas_tarifas.xlsx',
    importado_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(tipologia, id_garantia, id_cobertura, fecha_foto)
);
CREATE INDEX IF NOT EXISTS idx_pm_tipologia ON mmt_primas_medias(tipologia, fecha_foto);

-- ── MEJORAS ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS mejoras (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario     TEXT NOT NULL DEFAULT '',
    titulo      TEXT NOT NULL DEFAULT '',
    descripcion TEXT NOT NULL DEFAULT '',
    estado      TEXT NOT NULL DEFAULT 'pendiente',
    ts          TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── FLOTAS HISTÓRICAS (pre-Orion) ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS flotas_historicas (
    id                TEXT PRIMARY KEY,
    nombre            TEXT NOT NULL DEFAULT '',
    estado            TEXT NOT NULL DEFAULT 'CONTRATADA',
    tomador           TEXT NOT NULL DEFAULT '',
    cif               TEXT NOT NULL DEFAULT '',
    actividad         TEXT NOT NULL DEFAULT '',
    corredor_nombre   TEXT NOT NULL DEFAULT '',
    comision          REAL NOT NULL DEFAULT 0,
    coberturas        TEXT NOT NULL DEFAULT '[]',
    prima_total       REAL NOT NULL DEFAULT 0,
    fecha_inicio      TEXT NOT NULL DEFAULT '',
    fecha_vencimiento TEXT NOT NULL DEFAULT '',
    periodicidad      TEXT NOT NULL DEFAULT 'anual',
    num_poliza        TEXT NOT NULL DEFAULT '',
    compania          TEXT NOT NULL DEFAULT '',
    total_vehiculos   INTEGER NOT NULL DEFAULT 0,
    categoria_flota   TEXT NOT NULL DEFAULT '',
    notas             TEXT NOT NULL DEFAULT '',
    created_by        TEXT NOT NULL DEFAULT '',
    created_at        TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_fh_estado ON flotas_historicas(estado);

-- Consultas de Vehículos (normales y masivas): cada estudio se guarda para no perderlo si se cierra la pantalla.
-- Aditiva: CREATE IF NOT EXISTS, no toca ninguna tabla existente. La matrícula va dentro de data (JSON).
CREATE TABLE IF NOT EXISTS consultas_vehiculos (
    id               TEXT PRIMARY KEY,
    tipo             TEXT NOT NULL DEFAULT 'normal',
    nombre           TEXT NOT NULL DEFAULT '',
    creado_por       TEXT NOT NULL DEFAULT '',
    n_vehiculos      INTEGER NOT NULL DEFAULT 0,
    n_identificados  INTEGER NOT NULL DEFAULT 0,
    created_at       TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at       TEXT NOT NULL DEFAULT (datetime('now')),
    data             TEXT NOT NULL DEFAULT '{{}}'
);
CREATE INDEX IF NOT EXISTS idx_consultas_veh_updated ON consultas_vehiculos(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_consultas_veh_tipo    ON consultas_vehiculos(tipo);

-- Ventanas de años que el sistema de emisión de MMT admite por idVehMMT (se aprenden de sus errores de validación
-- o se cargan en bloque). Aditiva: CREATE IF NOT EXISTS. Tiene prioridad sobre las fechas del catálogo.
CREATE TABLE IF NOT EXISTS ventanas_sistema (
    id_veh      TEXT PRIMARY KEY,
    fab_min     INTEGER NOT NULL DEFAULT 0,
    fab_max     INTEGER NOT NULL DEFAULT 0,
    mat_min     INTEGER,
    mat_max     INTEGER,
    fuente      TEXT NOT NULL DEFAULT '',
    updated_by  TEXT NOT NULL DEFAULT '',
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO usuarios (id, username, password_hash, rol) VALUES
  ('usr_titan',  'TITAN',  '{_HASH_DEFAULT}', 'usuario'),
  ('usr_carlos', 'CARLOS', '{_HASH_DEFAULT}', 'usuario'),
  ('usr_mmt',    'MMT',    '{_HASH_DEFAULT}', 'usuario'),
  ('usr_sergio', 'SERGIO', '{_HASH_DEFAULT}', 'admin');
"""

# ─── Datos iniciales de primas (se insertan solo si la tabla está vacía) ──────

PRIMAS_SEED = [
    # Cat.1 — solo nacional
    ('turismo',                   'terceros_ampliado', 'nacional', 395),
    ('turismo',                   'todo_riesgo',       'nacional', 395),
    ('furgoneta',                 'terceros_ampliado', 'nacional', 640),
    ('furgoneta',                 'todo_riesgo',       'nacional', 640),
    ('industrial_matriculado',    'terceros',          'nacional', 190),
    ('industrial_no_matriculado', 'terceros',          'nacional', 190),
    # Cat.2 nacional
    ('cabeza_tractora', 'terceros',           'nacional', 820),
    ('cabeza_tractora', 'terceros_con_luna',  'nacional', 970),
    ('cabeza_tractora', 'terceros_ampliado',  'nacional', 1500),
    ('cabeza_tractora', 'todo_riesgo',        'nacional', 2355),
    ('camion_rigido',   'terceros',           'nacional', 800),
    ('camion_rigido',   'terceros_con_luna',  'nacional', 950),
    ('camion_rigido',   'terceros_ampliado',  'nacional', 1400),
    ('camion_rigido',   'todo_riesgo',        'nacional', 2305),
    ('semirremolque',   'terceros',           'nacional', 270),
    ('semirremolque',   'terceros_ampliado',  'nacional', 1100),
    ('semirremolque',   'todo_riesgo',        'nacional', 1870),
    # Cat.2 internacional
    ('cabeza_tractora', 'terceros',           'internacional', 965),
    ('cabeza_tractora', 'terceros_con_luna',  'internacional', 1115),
    ('cabeza_tractora', 'terceros_ampliado',  'internacional', 1645),
    ('cabeza_tractora', 'todo_riesgo',        'internacional', 2500),
    ('camion_rigido',   'terceros',           'internacional', 945),
    ('camion_rigido',   'terceros_con_luna',  'internacional', 1095),
    ('camion_rigido',   'terceros_ampliado',  'internacional', 1545),
    ('camion_rigido',   'todo_riesgo',        'internacional', 2450),
    ('semirremolque',   'terceros',           'internacional', 300),
    ('semirremolque',   'terceros_ampliado',  'internacional', 1200),
    ('semirremolque',   'todo_riesgo',        'internacional', 1950),
]

MMT_TIPOLOGIA_SEED = [
    # (orion_tipo, mmt_tipologia, categoria, notas)
    ('cabeza tractora',   'TRACTOCAMION',       2, ''),
    ('semirremolque',     'REMOLQUE-SEMI',       2, ''),
    ('camion rigido',     'CAMION',              2, ''),
    ('furgoneta',         'FURGON',              1, ''),
    ('turismo',           'TRUISMOS -1000',      1, 'Turismo < 1000cc o categoría equivalente'),
    ('motocicleta',       'MOTOCICLETAS',        1, ''),
    ('furgon pesado',     'FURGON PESADO',       2, ''),
    ('camion ligero',     'CAMION LIGERO',       2, ''),
    ('derivado turismo',  'DERIVADO DE TURISMO', 1, ''),
    ('derivado tt',       'DERIVADO TT',         1, ''),
    ('vehiculo agricola', 'VH-AGRICOLA',         1, ''),
    ('vehiculo industrial','VEHICULO INDUSTRIAL', 2, 'Datos históricos 97% reducidos en 202512 — usar con precaución'),
]

MOTOR_PARAMS_SEED = [
    # Pendientes de definición autorizada — valor NULL hasta que se configuren
    ('gastos_fijos_por_vehiculo',  None, 'Gastos fijos por vehículo/año (EUR) — pendiente de definición'),
    ('gastos_variables_pct',       None, 'Porcentaje de gastos variables sobre prima (0-1) — pendiente'),
    ('comision_pct',               None, 'Porcentaje de comisión (0-1) — pendiente de definición'),
    ('margen_pct',                 None, 'Margen de rentabilidad objetivo (0-1) — pendiente'),
    ('carga_riesgo_pct',           None, 'Carga de riesgo o capital (0-1) — pendiente de definición'),
    ('foto_activa',                None, 'Fecha de foto MMT activa para cálculos (202609, 202512, 202412)'),
]

AJUSTES_SEED = [
    ('animales',                  25,   'Cobertura animales (fijo por vehículo)'),
    ('asistencia_particular',     110,  'Asistencia turismo (particular)'),
    ('asistencia_transportes',    110,  'Asistencia furgoneta (transportes propios)'),
    ('asistencia_servicio_pub',   160,  'Asistencia furgoneta (servicio público)'),
    ('asistencia_nacional',       221,  'Asistencia cat.2 ámbito nacional'),
    ('asistencia_internacional',  327,  'Asistencia cat.2 ámbito internacional'),
    ('isotermo_pct',              0.30, 'Recargo isotermo (porcentaje sobre base)'),
    ('perdida_total_pct',         0.12, 'Recargo pérdida total (porcentaje sobre base)'),
    ('ajuste_global_pct',         0,    'Ajuste global de primas (%) — positivo sube, negativo baja'),
]


def get_conn():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def _column_exists(conn, table: str, column: str) -> bool:
    cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(c['name'] == column for c in cols)


def _table_exists(conn, table: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table]
    ).fetchone()
    return row is not None


def migrate_db():
    conn = get_conn()
    try:
        # ── usuarios ──────────────────────────────────────────────────────────
        if _table_exists(conn, 'usuarios') and not _column_exists(conn, 'usuarios', 'rol'):
            conn.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'usuario'")
        if _table_exists(conn, 'usuarios'):
            conn.execute("DELETE FROM usuarios WHERE UPPER(username) = 'MMT'")
            conn.execute("UPDATE usuarios SET rol='admin' WHERE UPPER(username) = 'SERGIO'")
            conn.execute("UPDATE usuarios SET rol='usuario' WHERE UPPER(username) != 'SERGIO'")
        if _table_exists(conn, 'usuarios') and not _column_exists(conn, 'usuarios', 'salt'):
            conn.execute("ALTER TABLE usuarios ADD COLUMN salt TEXT DEFAULT NULL")

        # ── corredores ────────────────────────────────────────────────────────
        if _table_exists(conn, 'corredores'):
            new_cols = [
                ('codigo',       "TEXT NOT NULL DEFAULT ''"),
                ('cif',          "TEXT NOT NULL DEFAULT ''"),
                ('domicilio',    "TEXT NOT NULL DEFAULT ''"),
                ('comision',     "REAL NOT NULL DEFAULT 0"),
                ('periodicidad', "TEXT NOT NULL DEFAULT 'mensual'"),
                ('forma_pago',   "TEXT NOT NULL DEFAULT ''"),
                ('contacto',     "TEXT NOT NULL DEFAULT ''"),
                ('email',        "TEXT NOT NULL DEFAULT ''"),
                ('telefono',     "TEXT NOT NULL DEFAULT ''"),
                ('observaciones',"TEXT NOT NULL DEFAULT ''"),
                ('sucursal',      "TEXT NOT NULL DEFAULT ''"),
                ('comercial',    "TEXT NOT NULL DEFAULT ''"),
                ('id_perceptor', "TEXT NOT NULL DEFAULT ''"),
                ('created_at',   "TEXT NOT NULL DEFAULT '2000-01-01'"),
            ]
            for col, typedef in new_cols:
                if not _column_exists(conn, 'corredores', col):
                    conn.execute(f"ALTER TABLE corredores ADD COLUMN {col} {typedef}")
            if _column_exists(conn, 'corredores', 'data'):
                rows = conn.execute("SELECT id, data FROM corredores WHERE data IS NOT NULL AND data != '{}'").fetchall()
                for row in rows:
                    try:
                        d = json.loads(row['data'] or '{}')
                        comision = float(d.get('porcentajeComision') or d.get('comision') or 0)
                        conn.execute("""
                            UPDATE corredores SET
                                codigo=?, cif=?, domicilio=?, comision=?, periodicidad=?,
                                forma_pago=?, contacto=?, email=?, telefono=?,
                                observaciones=?, sucursal=?, comercial=?
                            WHERE id=?
                        """, [
                            d.get('codigo', ''), d.get('cif', ''), d.get('domicilio', ''),
                            comision, d.get('periodicidad', 'mensual'),
                            d.get('formaPago', ''), d.get('contacto', ''),
                            d.get('email', ''), d.get('telefono', ''),
                            d.get('observaciones', ''), d.get('sucursal', '') or '',
                            d.get('comercial', '') or '', row['id'],
                        ])
                    except Exception:
                        pass

        # ── carpetas ──────────────────────────────────────────────────────────
        if _table_exists(conn, 'carpetas'):
            new_cols = [
                ('estado',      "TEXT NOT NULL DEFAULT 'EN ESTUDIO'"),
                ('cif',         "TEXT NOT NULL DEFAULT ''"),
                ('tomador',     "TEXT NOT NULL DEFAULT ''"),
                ('actividad',   "TEXT NOT NULL DEFAULT ''"),
                ('corredor_id', "TEXT"),
                ('created_at',  "TEXT NOT NULL DEFAULT '2000-01-01'"),
            ]
            for col, typedef in new_cols:
                if not _column_exists(conn, 'carpetas', col):
                    conn.execute(f"ALTER TABLE carpetas ADD COLUMN {col} {typedef}")
            rows = conn.execute("SELECT id, data FROM carpetas WHERE data IS NOT NULL AND data != '{}'").fetchall()
            for row in rows:
                try:
                    d = json.loads(row['data'] or '{}')
                    h = d.get('header') or {}
                    conn.execute("""
                        UPDATE carpetas SET estado=?, cif=?, tomador=?, actividad=?, corredor_id=?
                        WHERE id=?
                    """, [
                        d.get('estado', 'EN ESTUDIO'),
                        h.get('cif') or d.get('cif', ''),
                        h.get('tomador') or d.get('tomador', ''),
                        h.get('actividad') or d.get('actividad', ''),
                        d.get('corredor_id') or None,
                        row['id'],
                    ])
                except Exception:
                    pass

        # ── silverdat ─────────────────────────────────────────────────────────
        if not _table_exists(conn, 'vehiculos_silverdat'):
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vehiculos_silverdat (
                    matricula TEXT PRIMARY KEY, datos TEXT NOT NULL,
                    fecha_consulta TEXT NOT NULL DEFAULT (datetime('now'))
                )
            """)
        if not _table_exists(conn, 'historial_silverdat'):
            conn.execute("""
                CREATE TABLE IF NOT EXISTS historial_silverdat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, matricula TEXT NOT NULL,
                    fecha_consulta TEXT NOT NULL DEFAULT (datetime('now')),
                    consultado_por TEXT NOT NULL DEFAULT '', carpeta_id TEXT NOT NULL DEFAULT '',
                    carpeta_nombre TEXT NOT NULL DEFAULT '', corredor_id TEXT NOT NULL DEFAULT ''
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_historial_sd_mat ON historial_silverdat(matricula)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_historial_sd_fecha ON historial_silverdat(fecha_consulta DESC)")

        # ── historial_silverdat: corredor_nombre column ────────────────────────
        if _table_exists(conn, 'historial_silverdat') and not _column_exists(conn, 'historial_silverdat', 'corredor_nombre'):
            conn.execute("ALTER TABLE historial_silverdat ADD COLUMN corredor_nombre TEXT NOT NULL DEFAULT ''")

        # ── silverdat_session (tabla compartida entre instancias PM2) ───────────
        if not _table_exists(conn, 'silverdat_session'):
            conn.execute("""
                CREATE TABLE IF NOT EXISTS silverdat_session (
                    id           INTEGER PRIMARY KEY CHECK (id = 1),
                    cookie       TEXT NOT NULL DEFAULT '',
                    dat_id       TEXT NOT NULL DEFAULT '',
                    logged_in_at TEXT NOT NULL DEFAULT (datetime('now')),
                    expires_at   TEXT NOT NULL DEFAULT (datetime('now'))
                )
            """)

        # ── primas_config: seed if empty ──────────────────────────────────────
        if _table_exists(conn, 'primas_config'):
            count = conn.execute("SELECT COUNT(*) FROM primas_config").fetchone()[0]
            if count == 0:
                conn.executemany("""
                    INSERT OR IGNORE INTO primas_config (tipo_vehiculo, cobertura, ambito, prima)
                    VALUES (?, ?, ?, ?)
                """, PRIMAS_SEED)

        # ── ajustes_config: seed if empty, add new keys to existing DBs ─────────
        if _table_exists(conn, 'ajustes_config'):
            count = conn.execute("SELECT COUNT(*) FROM ajustes_config").fetchone()[0]
            if count == 0:
                conn.executemany("""
                    INSERT OR IGNORE INTO ajustes_config (clave, valor, descripcion)
                    VALUES (?, ?, ?)
                """, AJUSTES_SEED)
            else:
                # Ensure new keys exist even on already-seeded DBs
                conn.executemany("""
                    INSERT OR IGNORE INTO ajustes_config (clave, valor, descripcion)
                    VALUES (?, ?, ?)
                """, AJUSTES_SEED)

        # ── mmt_tipologia_map: seed si vacío ─────────────────────────────────
        if _table_exists(conn, 'mmt_tipologia_map'):
            count = conn.execute("SELECT COUNT(*) FROM mmt_tipologia_map").fetchone()[0]
            if count == 0:
                conn.executemany("""
                    INSERT OR IGNORE INTO mmt_tipologia_map
                        (orion_tipo, mmt_tipologia, categoria, notas)
                    VALUES (?, ?, ?, ?)
                """, MMT_TIPOLOGIA_SEED)

        # ── motor_params: seed si vacío ───────────────────────────────────────
        if _table_exists(conn, 'motor_params'):
            count = conn.execute("SELECT COUNT(*) FROM motor_params").fetchone()[0]
            if count == 0:
                conn.executemany("""
                    INSERT OR IGNORE INTO motor_params (clave, valor, descripcion)
                    VALUES (?, ?, ?)
                """, MOTOR_PARAMS_SEED)
            else:
                # Asegurar que todas las claves del seed existen
                conn.executemany("""
                    INSERT OR IGNORE INTO motor_params (clave, valor, descripcion)
                    VALUES (?, ?, ?)
                """, MOTOR_PARAMS_SEED)

        # ── mmt_stats: limpiar registros corruptos ────────────────────────────
        if _table_exists(conn, 'mmt_stats'):
            deleted = conn.execute(
                "DELETE FROM mmt_stats WHERE id_cobertura = \"'-\""
            ).rowcount
            if deleted > 0:
                print(f"[db] Eliminados {deleted} registros corruptos de mmt_stats")

        conn.commit()
        print("[db] Migración completada")
    finally:
        conn.close()


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    migrate_db()
    print(f"[db] SQLite listo en {os.path.abspath(DB_PATH)}")
