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
                ('sucursal',     "TEXT NOT NULL DEFAULT ''"),
                ('comercial',    "TEXT NOT NULL DEFAULT ''"),
                ('created_at',   "TEXT NOT NULL DEFAULT (datetime('now'))"),
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
                ('created_at',  "TEXT NOT NULL DEFAULT (datetime('now'))"),
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
