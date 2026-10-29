"""
Orion API — Python + Flask + SQLite
Puerto: 3001 (localhost solamente)
Auth:   header X-Api-Key
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, request, jsonify
from db import get_conn, init_db, hash_password, verify_password

# ─── Configuración ────────────────────────────────────────────────────────────

API_KEY = os.environ.get('ORION_API_KEY', 'dev_secret_local')

app = Flask(__name__)
init_db()

# ─── Helpers ──────────────────────────────────────────────────────────────────

def require_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('X-Api-Key') != API_KEY:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


# ─── AUTH ─────────────────────────────────────────────────────────────────────

@app.route('/auth/verify', methods=['POST'])
@require_key
def auth_verify():
    body = request.get_json(silent=True) or {}
    username = str(body.get('username', '')).strip().upper()
    password = str(body.get('password', ''))

    if not username or not password:
        return jsonify({'ok': False, 'error': 'Faltan credenciales'}), 400

    conn = get_conn()
    row = conn.execute(
        'SELECT id, username, password_hash, salt, rol FROM usuarios WHERE UPPER(username)=?',
        [username]
    ).fetchone()

    if not row or not verify_password(password, row['password_hash'], row['salt']):
        conn.close()
        return jsonify({'ok': False, 'error': 'Usuario o contraseña incorrectos'}), 401

    if row['salt'] is None:
        new_hash, new_salt = hash_password(password)
        conn.execute(
            'UPDATE usuarios SET password_hash=?, salt=? WHERE id=?',
            [new_hash, new_salt, row['id']]
        )
        conn.commit()

    conn.close()
    return jsonify({'ok': True, 'username': row['username'], 'rol': row['rol']})


# ─── CARPETAS ─────────────────────────────────────────────────────────────────

@app.route('/carpetas', methods=['GET'])
@require_key
def get_carpetas():
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.id, c.nombre, c.estado, c.cif, c.tomador, c.actividad,
               c.corredor_id, c.creado_por, c.updated_at, c.data,
               GROUP_CONCAT(sa.username) AS ep
        FROM carpetas c
        LEFT JOIN sesiones_activas sa
            ON sa.carpeta_id = c.id
           AND sa.last_seen > datetime('now', '-3 minutes')
        GROUP BY c.id
        ORDER BY c.updated_at DESC
    """).fetchall()
    conn.close()

    result = []
    for row in rows:
        data = json.loads(row['data']) if row['data'] else {}
        data['nombre']         = row['nombre'] or data.get('nombre', '')
        data['estado']         = row['estado'] or data.get('estado', 'EN ESTUDIO')
        data['corredor_id']    = row['corredor_id'] or data.get('corredor_id')
        data['creado_por']     = row['creado_por'] or data.get('creado_por', '')
        data['actualizadaEn']  = row['updated_at'] or data.get('actualizadaEn', '')
        data['estudiando_por'] = row['ep'].split(',') if row['ep'] else []
        if 'header' not in data:
            data['header'] = {}
        data['header']['cif']       = row['cif'] or data['header'].get('cif', '')
        data['header']['tomador']   = row['tomador'] or data['header'].get('tomador', '')
        data['header']['actividad'] = row['actividad'] or data['header'].get('actividad', '')
        result.append(data)
    return jsonify(result)


def _extract_carpeta_meta(c: dict) -> tuple:
    h = c.get('header') or {}
    nombre      = c.get('nombre', '')
    estado      = c.get('estado', 'EN ESTUDIO')
    cif         = h.get('cif') or c.get('cif', '')
    tomador     = h.get('tomador') or c.get('tomador', '')
    actividad   = h.get('actividad') or c.get('actividad', '')
    corredor_id = c.get('corredor_id') or None
    creado_por  = c.get('creado_por', '')
    return nombre, estado, cif, tomador, actividad, corredor_id, creado_por


@app.route('/carpetas', methods=['POST'])
@require_key
def post_carpetas():
    body   = request.get_json(silent=True) or {}
    action = body.get('action')
    conn   = get_conn()

    try:
        if action == 'upsert':
            c = body.get('carpeta', {})
            nombre, estado, cif, tomador, actividad, corredor_id, creado_por = _extract_carpeta_meta(c)
            conn.execute("""
                INSERT INTO carpetas
                    (id, nombre, estado, cif, tomador, actividad, corredor_id,
                     creado_por, updated_at, data)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET
                    nombre=excluded.nombre, estado=excluded.estado,
                    cif=excluded.cif, tomador=excluded.tomador,
                    actividad=excluded.actividad, corredor_id=excluded.corredor_id,
                    updated_at=excluded.updated_at, data=excluded.data
            """, [c['id'], nombre, estado, cif, tomador, actividad, corredor_id,
                  creado_por, now_iso(), json.dumps(c)])
            conn.commit()

        elif action == 'delete':
            cid = body.get('id')
            conn.execute("DELETE FROM sesiones_activas WHERE carpeta_id=?", [cid])
            conn.execute("DELETE FROM carpetas WHERE id=?", [cid])
            conn.commit()

        elif action == 'replaceAll':
            carpetas = body.get('carpetas', [])
            try:
                conn.execute("DELETE FROM carpetas")
                for c in carpetas:
                    nombre, estado, cif, tomador, actividad, corredor_id, creado_por = _extract_carpeta_meta(c)
                    conn.execute("""
                        INSERT INTO carpetas
                            (id, nombre, estado, cif, tomador, actividad, corredor_id,
                             creado_por, updated_at, data)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                        ON CONFLICT(id) DO UPDATE SET
                            nombre=excluded.nombre, estado=excluded.estado,
                            cif=excluded.cif, tomador=excluded.tomador,
                            actividad=excluded.actividad, corredor_id=excluded.corredor_id,
                            updated_at=excluded.updated_at, data=excluded.data
                    """, [c['id'], nombre, estado, cif, tomador, actividad, corredor_id,
                          creado_por, now_iso(), json.dumps(c)])
                conn.commit()
            except Exception:
                conn.rollback()
                raise
        else:
            return jsonify({'error': 'Acción desconocida'}), 400
    finally:
        conn.close()

    return jsonify({'ok': True})


# ─── CORREDORES ───────────────────────────────────────────────────────────────

@app.route('/corredores', methods=['GET'])
@require_key
def get_corredores():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM corredores ORDER BY nombre ASC").fetchall()
    conn.close()

    result = []
    for row in rows:
        r = dict(row)
        result.append({
            'id':                  r['id'],
            'codigo':              r.get('codigo', ''),
            'nombre':              r.get('nombre', ''),
            'cif':                 r.get('cif', ''),
            'domicilio':           r.get('domicilio', ''),
            'porcentajeComision':  r.get('comision', 0),
            'periodicidad':        r.get('periodicidad', 'mensual'),
            'formaPago':           r.get('forma_pago', ''),
            'contacto':            r.get('contacto', ''),
            'email':               r.get('email', ''),
            'telefono':            r.get('telefono', ''),
            'observaciones':       r.get('observaciones', ''),
            'sucursal':            r.get('sucursal') or None,
            'comercial':           r.get('comercial') or None,
            'idPerceptor':         r.get('id_perceptor', ''),
            'creado_por':          r.get('creado_por', ''),
            'creadoEn':            r.get('created_at', ''),
            'actualizadoEn':       r.get('updated_at', ''),
        })
    return jsonify(result)


@app.route('/corredores', methods=['POST'])
@require_key
def post_corredores():
    body   = request.get_json(silent=True) or {}
    action = body.get('action')
    conn   = get_conn()

    try:
        if action == 'upsert':
            c = body.get('corredor', {})
            comision = float(c.get('porcentajeComision') or c.get('comision') or 0)
            conn.execute("""
                INSERT INTO corredores
                    (id, codigo, nombre, cif, domicilio, comision, periodicidad,
                     forma_pago, contacto, email, telefono, observaciones,
                     sucursal, comercial, id_perceptor, creado_por, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET
                    codigo=excluded.codigo, nombre=excluded.nombre,
                    cif=excluded.cif, domicilio=excluded.domicilio,
                    comision=excluded.comision, periodicidad=excluded.periodicidad,
                    forma_pago=excluded.forma_pago, contacto=excluded.contacto,
                    email=excluded.email, telefono=excluded.telefono,
                    observaciones=excluded.observaciones, sucursal=excluded.sucursal,
                    comercial=excluded.comercial, id_perceptor=excluded.id_perceptor,
                    updated_at=excluded.updated_at
            """, [
                c['id'], c.get('codigo', ''), c.get('nombre', ''), c.get('cif', ''),
                c.get('domicilio', ''), comision, c.get('periodicidad', 'mensual'),
                c.get('formaPago', ''), c.get('contacto', ''), c.get('email', ''),
                c.get('telefono', ''), c.get('observaciones', ''),
                c.get('sucursal') or '', c.get('comercial') or '',
                c.get('idPerceptor', ''),
                c.get('creado_por', ''), now_iso(),
            ])
            conn.commit()

        elif action == 'delete':
            conn.execute("DELETE FROM corredores WHERE id=?", [body.get('id')])
            conn.commit()

        elif action == 'upsertBatch':
            lista = body.get('corredores', [])
            if not lista:
                return jsonify({'error': 'Sin corredores'}), 400
            try:
                for c in lista:
                    comision = float(c.get('porcentajeComision') or c.get('comision') or 0)
                    conn.execute("""
                        INSERT INTO corredores
                            (id, codigo, nombre, cif, domicilio, comision, periodicidad,
                             forma_pago, contacto, email, telefono, observaciones,
                             sucursal, comercial, id_perceptor, creado_por, updated_at)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ON CONFLICT(id) DO UPDATE SET
                            codigo=excluded.codigo, nombre=excluded.nombre,
                            cif=excluded.cif, domicilio=excluded.domicilio,
                            comision=excluded.comision, periodicidad=excluded.periodicidad,
                            forma_pago=excluded.forma_pago, contacto=excluded.contacto,
                            email=excluded.email, telefono=excluded.telefono,
                            observaciones=excluded.observaciones, sucursal=excluded.sucursal,
                            comercial=excluded.comercial,
                            id_perceptor=excluded.id_perceptor,
                            updated_at=excluded.updated_at
                    """, [
                        c['id'], c.get('codigo', ''), c.get('nombre', ''), c.get('cif', ''),
                        c.get('domicilio', ''), comision, c.get('periodicidad', 'mensual'),
                        c.get('formaPago', ''), c.get('contacto', ''), c.get('email', ''),
                        c.get('telefono', ''), c.get('observaciones', ''),
                        c.get('sucursal') or '', c.get('comercial') or '',
                        c.get('idPerceptor', ''),
                        c.get('creado_por', ''), now_iso(),
                    ])
                conn.commit()
            except Exception:
                conn.rollback()
                raise

        elif action == 'deleteAll':
            conn.execute("DELETE FROM corredores")
            conn.commit()

        else:
            return jsonify({'error': 'Acción desconocida'}), 400
    finally:
        conn.close()

    return jsonify({'ok': True})


# ─── SESIONES ─────────────────────────────────────────────────────────────────

@app.route('/sesion', methods=['POST'])
@require_key
def post_sesion():
    body       = request.get_json(silent=True) or {}
    action     = body.get('action')
    carpeta_id = body.get('carpeta_id')
    username   = body.get('username')

    if not carpeta_id or not username:
        return jsonify({'error': 'carpeta_id y username requeridos'}), 400

    conn = get_conn()
    try:
        if action in ('join', 'heartbeat'):
            conn.execute("""
                INSERT INTO sesiones_activas (carpeta_id, username, last_seen)
                VALUES (?, ?, ?)
                ON CONFLICT(carpeta_id, username) DO UPDATE SET last_seen=excluded.last_seen
            """, [carpeta_id, username, now_iso()])
            conn.commit()
        elif action == 'leave':
            conn.execute(
                "DELETE FROM sesiones_activas WHERE carpeta_id=? AND username=?",
                [carpeta_id, username]
            )
            conn.commit()
        else:
            return jsonify({'error': 'Acción desconocida'}), 400
    finally:
        conn.close()

    return jsonify({'ok': True})


# ─── USUARIOS ─────────────────────────────────────────────────────────────────

@app.route('/usuarios', methods=['GET'])
@require_key
def get_usuarios():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, username, rol, created_at FROM usuarios ORDER BY username"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ─── SILVERDAT CACHE ──────────────────────────────────────────────────────────

@app.route('/silverdat-cache/<matricula>', methods=['GET'])
@require_key
def get_silverdat_cache(matricula):
    conn = get_conn()
    row = conn.execute(
        'SELECT datos, fecha_consulta FROM vehiculos_silverdat WHERE matricula=?',
        [matricula.strip().upper()]
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({'ok': False}), 404
    return jsonify({'ok': True, 'datos': row['datos'], 'fecha_consulta': row['fecha_consulta']})


@app.route('/silverdat-cache', methods=['POST'])
@require_key
def post_silverdat_cache():
    body = request.get_json(silent=True) or {}
    matricula      = str(body.get('matricula', '')).strip().upper()
    datos          = body.get('datos', '')
    consultado_por = str(body.get('consultado_por', '')).strip()
    carpeta_id     = str(body.get('carpeta_id', '')).strip()
    carpeta_nombre = str(body.get('carpeta_nombre', '')).strip()
    corredor_id    = str(body.get('corredor_id', '')).strip()

    if not matricula or not datos:
        return jsonify({'ok': False, 'error': 'Faltan datos'}), 400

    ts = now_iso()
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO vehiculos_silverdat (matricula, datos, fecha_consulta)
            VALUES (?, ?, ?)
            ON CONFLICT(matricula) DO UPDATE SET datos=excluded.datos, fecha_consulta=excluded.fecha_consulta
        """, [matricula, datos, ts])
        conn.execute("""
            INSERT INTO historial_silverdat
                (matricula, fecha_consulta, consultado_por, carpeta_id, carpeta_nombre, corredor_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [matricula, ts, consultado_por, carpeta_id, carpeta_nombre, corredor_id])
        conn.commit()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        conn.close()


# ─── SILVERDAT SESSION (compartida entre instancias PM2) ─────────────────────

@app.route('/silverdat-session', methods=['GET', 'POST'])
@require_key
def silverdat_session_endpoint():
    conn = get_conn()
    try:
        if request.method == 'GET':
            row = conn.execute("SELECT * FROM silverdat_session WHERE id=1").fetchone()
            if not row:
                return jsonify({'ok': False})
            expires = datetime.fromisoformat(row['expires_at'])
            if datetime.now(timezone.utc) > expires.replace(tzinfo=timezone.utc) if expires.tzinfo is None else datetime.now(timezone.utc) > expires:
                conn.execute("DELETE FROM silverdat_session WHERE id=1")
                conn.commit()
                return jsonify({'ok': False})
            return jsonify({
                'ok': True,
                'cookie': row['cookie'],
                'dat_id': row['dat_id'],
                'logged_in_at': row['logged_in_at'],
                'expires_at': row['expires_at'],
            })
        else:
            body = request.get_json(silent=True) or {}
            if body.get('clear'):
                conn.execute("DELETE FROM silverdat_session WHERE id=1")
                conn.commit()
                return jsonify({'ok': True})
            cookie = body.get('cookie', '')
            if not cookie:
                return jsonify({'ok': False, 'error': 'cookie requerida'}), 400
            conn.execute("""
                INSERT OR REPLACE INTO silverdat_session (id, cookie, dat_id, logged_in_at, expires_at)
                VALUES (1, ?, ?, ?, ?)
            """, [cookie, body.get('dat_id', ''), body.get('logged_in_at', now_iso()), body.get('expires_at', now_iso())])
            conn.commit()
            return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/silverdat-historial', methods=['GET'])
@require_key
def get_silverdat_historial():
    conn = get_conn()
    rows = conn.execute("""
        SELECT h.id, h.matricula, h.fecha_consulta, h.consultado_por,
               h.carpeta_id, h.carpeta_nombre, h.corredor_id,
               COALESCE(c.nombre, '') AS corredor_nombre
        FROM historial_silverdat h
        LEFT JOIN corredores c ON c.id = h.corredor_id
        ORDER BY h.fecha_consulta DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/silverdat-historial/check', methods=['POST'])
@require_key
def check_silverdat_historial():
    body = request.get_json(silent=True) or {}
    matriculas = [str(m).strip().upper() for m in body.get('matriculas', []) if str(m).strip()]
    if not matriculas:
        return jsonify({'ok': True, 'conocidas': []})

    placeholders = ','.join('?' * len(matriculas))
    conn = get_conn()
    rows = conn.execute(f"""
        SELECT h.matricula, MAX(h.fecha_consulta) AS fecha_consulta,
               h.consultado_por, h.carpeta_nombre, h.corredor_id,
               COALESCE(c.nombre, '') AS corredor_nombre
        FROM historial_silverdat h
        LEFT JOIN corredores c ON c.id = h.corredor_id
        WHERE h.matricula IN ({placeholders})
        GROUP BY h.matricula
    """, matriculas).fetchall()
    conn.close()
    return jsonify({'ok': True, 'conocidas': [dict(r) for r in rows]})


# ─── ADMIN — PRIMAS ───────────────────────────────────────────────────────────

@app.route('/admin/primas', methods=['GET'])
@require_key
def get_primas():
    conn = get_conn()
    rows = conn.execute(
        "SELECT tipo_vehiculo, cobertura, ambito, prima, updated_at, updated_by FROM primas_config ORDER BY tipo_vehiculo, ambito, cobertura"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/admin/primas', methods=['PUT'])
@require_key
def put_primas():
    body    = request.get_json(silent=True) or {}
    updates = body.get('updates', [])  # [{tipo_vehiculo, cobertura, ambito, prima}]
    by      = str(body.get('updated_by', '')).strip()
    if not updates:
        return jsonify({'error': 'Sin datos'}), 400

    ts = now_iso()
    conn = get_conn()
    try:
        for u in updates:
            conn.execute("""
                INSERT INTO primas_config (tipo_vehiculo, cobertura, ambito, prima, updated_at, updated_by)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(tipo_vehiculo, cobertura, ambito)
                DO UPDATE SET prima=excluded.prima, updated_at=excluded.updated_at, updated_by=excluded.updated_by
            """, [u['tipo_vehiculo'], u['cobertura'], u['ambito'], float(u['prima']), ts, by])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True, 'updated': len(updates)})


# ─── ADMIN — AJUSTES ──────────────────────────────────────────────────────────

@app.route('/admin/ajustes', methods=['GET'])
@require_key
def get_ajustes():
    conn = get_conn()
    rows = conn.execute("SELECT clave, valor, descripcion, updated_at FROM ajustes_config ORDER BY clave").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/admin/ajustes', methods=['PUT'])
@require_key
def put_ajustes():
    body    = request.get_json(silent=True) or {}
    updates = body.get('updates', [])  # [{clave, valor}]
    if not updates:
        return jsonify({'error': 'Sin datos'}), 400

    ts = now_iso()
    conn = get_conn()
    try:
        for u in updates:
            conn.execute("""
                UPDATE ajustes_config SET valor=?, updated_at=? WHERE clave=?
            """, [float(u['valor']), ts, u['clave']])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


# ─── ADMIN — AUDITORÍA ────────────────────────────────────────────────────────

@app.route('/admin/audit', methods=['POST'])
@require_key
def post_audit():
    body    = request.get_json(silent=True) or {}
    usuario = str(body.get('usuario', '')).strip()
    accion  = str(body.get('accion', '')).strip()
    detalle = str(body.get('detalle', '')).strip()
    ip      = str(body.get('ip', '')).strip()

    if not accion:
        return jsonify({'error': 'accion requerida'}), 400

    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO audit_log (usuario, accion, detalle, ip, ts) VALUES (?, ?, ?, ?, ?)",
            [usuario, accion, detalle, ip, now_iso()]
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


@app.route('/admin/audit', methods=['GET'])
@require_key
def get_audit():
    limit  = min(int(request.args.get('limit', 100)), 500)
    offset = int(request.args.get('offset', 0))
    user   = request.args.get('usuario', '')
    date   = request.args.get('fecha', '')

    query  = "SELECT id, usuario, accion, detalle, ip, ts FROM audit_log WHERE 1=1"
    params = []
    if user:
        query += " AND UPPER(usuario)=?"
        params.append(user.upper())
    if date:
        query += " AND ts LIKE ?"
        params.append(f"{date}%")
    query += " ORDER BY ts DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    conn = get_conn()
    rows = conn.execute(query, params).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    conn.close()
    return jsonify({'rows': [dict(r) for r in rows], 'total': total})


# ─── ADMIN — MEJORAS ──────────────────────────────────────────────────────────

@app.route('/admin/mejoras', methods=['GET'])
@require_key
def get_mejoras():
    estado = request.args.get('estado', '')
    query  = "SELECT id, usuario, titulo, descripcion, estado, ts FROM mejoras"
    params = []
    if estado:
        query += " WHERE estado=?"
        params.append(estado)
    query += " ORDER BY ts DESC"

    conn = get_conn()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/admin/mejoras', methods=['POST'])
@require_key
def post_mejora():
    body = request.get_json(silent=True) or {}
    usuario     = str(body.get('usuario', '')).strip()
    titulo      = str(body.get('titulo', '')).strip()
    descripcion = str(body.get('descripcion', '')).strip()

    if not titulo or not descripcion:
        return jsonify({'error': 'titulo y descripcion requeridos'}), 400

    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO mejoras (usuario, titulo, descripcion, estado, ts) VALUES (?, ?, ?, 'pendiente', ?)",
            [usuario, titulo, descripcion, now_iso()]
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


@app.route('/admin/mejoras/<int:mejora_id>', methods=['PUT'])
@require_key
def put_mejora(mejora_id):
    body   = request.get_json(silent=True) or {}
    estado = str(body.get('estado', '')).strip()
    if estado not in ('pendiente', 'revisando', 'aprobada', 'descartada'):
        return jsonify({'error': 'Estado inválido'}), 400

    conn = get_conn()
    try:
        conn.execute("UPDATE mejoras SET estado=? WHERE id=?", [estado, mejora_id])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


# ─── ADMIN — ESTADÍSTICAS ─────────────────────────────────────────────────────

@app.route('/admin/stats', methods=['GET'])
@require_key
def get_stats():
    conn = get_conn()
    try:
        hoy   = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        mes   = datetime.now(timezone.utc).strftime('%Y-%m')

        total_carpetas   = conn.execute("SELECT COUNT(*) FROM carpetas").fetchone()[0]
        carpetas_estudio = conn.execute("SELECT COUNT(*) FROM carpetas WHERE estado='EN ESTUDIO'").fetchone()[0]
        carpetas_contrat = conn.execute("SELECT COUNT(*) FROM carpetas WHERE estado='CONTRATADA'").fetchone()[0]
        total_corredores = conn.execute("SELECT COUNT(*) FROM corredores").fetchone()[0]
        total_usuarios   = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        sd_hoy           = conn.execute("SELECT COUNT(*) FROM historial_silverdat WHERE fecha_consulta LIKE ?", [f"{hoy}%"]).fetchone()[0]
        sd_mes           = conn.execute("SELECT COUNT(*) FROM historial_silverdat WHERE fecha_consulta LIKE ?", [f"{mes}%"]).fetchone()[0]
        sd_total         = conn.execute("SELECT COUNT(*) FROM vehiculos_silverdat").fetchone()[0]
        mejoras_pend     = conn.execute("SELECT COUNT(*) FROM mejoras WHERE estado='pendiente'").fetchone()[0]
        acciones_hoy     = conn.execute("SELECT COUNT(*) FROM audit_log WHERE ts LIKE ?", [f"{hoy}%"]).fetchone()[0]

        ultimas_acciones = conn.execute("""
            SELECT usuario, accion, detalle, ts FROM audit_log
            ORDER BY ts DESC LIMIT 10
        """).fetchall()

    finally:
        conn.close()

    return jsonify({
        'carpetas': {
            'total': total_carpetas,
            'en_estudio': carpetas_estudio,
            'contratadas': carpetas_contrat,
        },
        'corredores': total_corredores,
        'usuarios': total_usuarios,
        'silverdat': {
            'hoy': sd_hoy,
            'mes': sd_mes,
            'cache_total': sd_total,
        },
        'mejoras_pendientes': mejoras_pend,
        'acciones_hoy': acciones_hoy,
        'ultimas_acciones': [dict(r) for r in ultimas_acciones],
    })


# ─── FLOTAS HISTÓRICAS ────────────────────────────────────────────────────────

import uuid as _uuid

@app.route('/flotas-historicas', methods=['GET'])
@require_key
def get_flotas_historicas():
    estado = request.args.get('estado', '').strip()
    cif    = request.args.get('cif',    '').strip()
    q      = request.args.get('q',      '').strip()
    conn   = get_conn()

    if cif:
        rows = conn.execute(
            "SELECT * FROM flotas_historicas WHERE upper(trim(cif)) = upper(?) ORDER BY nombre",
            (cif,)
        ).fetchall()
    elif q:
        words = [w for w in q.upper().split() if len(w) >= 2]
        if words:
            conds  = ' AND '.join(['(upper(nombre) LIKE ? OR upper(tomador) LIKE ?)'] * len(words))
            params = []
            for w in words:
                params.extend([f'%{w}%', f'%{w}%'])
            rows = conn.execute(
                f"SELECT * FROM flotas_historicas WHERE {conds} ORDER BY nombre LIMIT 30",
                params
            ).fetchall()
        else:
            rows = []
    elif estado:
        rows = conn.execute(
            "SELECT * FROM flotas_historicas WHERE estado=? ORDER BY updated_at DESC",
            (estado.upper(),)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM flotas_historicas ORDER BY updated_at DESC"
        ).fetchall()

    conn.close()
    result = []
    for row in rows:
        r = dict(row)
        try:
            r['coberturas'] = json.loads(r['coberturas'])
        except Exception:
            r['coberturas'] = []
        result.append(r)
    return jsonify(result)


@app.route('/flotas-historicas', methods=['POST'])
@require_key
def post_flotas_historicas():
    body = request.get_json(silent=True) or {}
    fid  = str(_uuid.uuid4())
    ts   = now_iso()
    coberturas = json.dumps(body.get('coberturas', []))
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO flotas_historicas
              (id, nombre, estado, tomador, cif, actividad,
               corredor_nombre, comision, coberturas, prima_total,
               fecha_inicio, fecha_vencimiento, periodicidad,
               num_poliza, compania, total_vehiculos, categoria_flota,
               notas, created_by, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            fid,
            str(body.get('nombre', '')).strip(),
            str(body.get('estado', 'CONTRATADA')).upper().strip(),
            str(body.get('tomador', '')).strip(),
            str(body.get('cif', '')).strip(),
            str(body.get('actividad', '')).strip(),
            str(body.get('corredor_nombre', '')).strip(),
            float(body.get('comision', 0) or 0),
            coberturas,
            float(body.get('prima_total', 0) or 0),
            str(body.get('fecha_inicio', '')).strip(),
            str(body.get('fecha_vencimiento', '')).strip(),
            str(body.get('periodicidad', 'anual')).strip(),
            str(body.get('num_poliza', '')).strip(),
            str(body.get('compania', '')).strip(),
            int(body.get('total_vehiculos', 0) or 0),
            str(body.get('categoria_flota', '')).strip(),
            str(body.get('notas', '')).strip(),
            str(body.get('created_by', '')).strip(),
            ts, ts,
        ])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True, 'id': fid}), 201


@app.route('/flotas-historicas/<fid>', methods=['PUT'])
@require_key
def put_flota_historica(fid):
    body = request.get_json(silent=True) or {}
    ts   = now_iso()
    coberturas = json.dumps(body.get('coberturas', []))
    conn = get_conn()
    try:
        conn.execute("""
            UPDATE flotas_historicas SET
              nombre=?, estado=?, tomador=?, cif=?, actividad=?,
              corredor_nombre=?, comision=?, coberturas=?, prima_total=?,
              fecha_inicio=?, fecha_vencimiento=?, periodicidad=?,
              num_poliza=?, compania=?, total_vehiculos=?, categoria_flota=?,
              notas=?, updated_at=?
            WHERE id=?
        """, [
            str(body.get('nombre', '')).strip(),
            str(body.get('estado', 'CONTRATADA')).upper().strip(),
            str(body.get('tomador', '')).strip(),
            str(body.get('cif', '')).strip(),
            str(body.get('actividad', '')).strip(),
            str(body.get('corredor_nombre', '')).strip(),
            float(body.get('comision', 0) or 0),
            coberturas,
            float(body.get('prima_total', 0) or 0),
            str(body.get('fecha_inicio', '')).strip(),
            str(body.get('fecha_vencimiento', '')).strip(),
            str(body.get('periodicidad', 'anual')).strip(),
            str(body.get('num_poliza', '')).strip(),
            str(body.get('compania', '')).strip(),
            int(body.get('total_vehiculos', 0) or 0),
            str(body.get('categoria_flota', '')).strip(),
            str(body.get('notas', '')).strip(),
            ts, fid,
        ])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


@app.route('/flotas-historicas/<fid>', methods=['DELETE'])
@require_key
def delete_flota_historica(fid):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM flotas_historicas WHERE id=?", [fid])
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


# ─── Motor de primas ──────────────────────────────────────────────────────────

@app.route('/motor/stats', methods=['GET'])
@require_key
def get_motor_stats():
    """Devuelve estadísticas MMT para una tipología y foto dada."""
    tipologia  = request.args.get('tipologia', '').strip()
    fecha_foto = request.args.get('fecha_foto', '').strip()
    if not tipologia:
        return jsonify({'error': 'tipologia requerida'}), 400
    conn = get_conn()
    try:
        q = "SELECT * FROM mmt_stats WHERE tipologia=?"
        params = [tipologia]
        if fecha_foto:
            q += " AND fecha_foto=?"
            params.append(fecha_foto)
        q += " ORDER BY id_garantia, id_cobertura, fecha_foto"
        rows = conn.execute(q, params).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route('/motor/tipologias', methods=['GET'])
@require_key
def get_motor_tipologias():
    """Devuelve el mapeo ORION tipo_vehiculo → MMT tipología."""
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM mmt_tipologia_map ORDER BY orion_tipo").fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route('/motor/params', methods=['GET'])
@require_key
def get_motor_params():
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM motor_params ORDER BY clave").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            # foto_activa puede llegar como int/float; normalizarla siempre a string
            if d.get('clave') == 'foto_activa' and d.get('valor') is not None:
                raw = d['valor']
                d['valor'] = str(int(raw)) if isinstance(raw, (int, float)) else str(raw).strip()
            result.append(d)
        return jsonify({'params': result})
    finally:
        conn.close()


@app.route('/motor/params', methods=['PUT'])
@require_key
def put_motor_params():
    """Actualiza parámetros económicos del motor. Body: {clave: valor, ...}"""
    data = request.get_json(force=True) or {}
    usuario = request.headers.get('X-Username', 'sistema')
    conn = get_conn()
    try:
        for clave, valor in data.items():
            # foto_activa se trata como entero (p.ej. 202609) para evitar ambigüedad REAL vs TEXT
            if clave == 'foto_activa' and valor is not None:
                try: valor = int(str(valor).strip())
                except (ValueError, TypeError): pass
            conn.execute("""
                INSERT INTO motor_params (clave, valor, updated_at, updated_by)
                VALUES (?, ?, datetime('now'), ?)
                ON CONFLICT(clave) DO UPDATE SET
                    valor=excluded.valor,
                    updated_at=excluded.updated_at,
                    updated_by=excluded.updated_by
            """, [clave, valor, usuario])
        conn.commit()
        return jsonify({'ok': True})
    finally:
        conn.close()


@app.route('/motor/catalogo', methods=['GET'])
@require_key
def get_motor_catalogo():
    """Busca vehículos en mmt_catalogo_vehiculos. Params: marca, modelo, id_clase, q (búsqueda libre)."""
    marca    = request.args.get('marca', '').strip().upper()
    modelo   = request.args.get('modelo', '').strip().upper()
    id_clase = request.args.get('id_clase', '').strip().upper()
    q        = request.args.get('q', '').strip().upper()
    limit    = min(int(request.args.get('limit', 50)), 200)

    filters, params = [], []
    if marca:    filters.append("UPPER(marca) LIKE ?");   params.append(f'%{marca}%')
    if modelo:   filters.append("UPPER(modelo) LIKE ?");  params.append(f'%{modelo}%')
    if id_clase: filters.append("UPPER(id_clase) = ?");   params.append(id_clase)
    if q:
        filters.append("(UPPER(marca) LIKE ? OR UPPER(modelo) LIKE ? OR UPPER(version) LIKE ?)")
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%'])
    if not filters:
        return jsonify({'error': 'Se requiere al menos un parámetro de búsqueda'}), 400

    sql = f"SELECT * FROM mmt_catalogo_vehiculos WHERE {' AND '.join(filters)} ORDER BY marca, modelo LIMIT ?"
    params.append(limit)
    conn = get_conn()
    try:
        rows = conn.execute(sql, params).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route('/motor/coberturas', methods=['GET'])
@require_key
def get_motor_coberturas():
    """Devuelve el catálogo de coberturas. Params: categoria (1a_categoria|2a_categoria|motos)."""
    categoria = request.args.get('categoria', '').strip()
    conn = get_conn()
    try:
        if categoria:
            rows = conn.execute(
                "SELECT * FROM mmt_coberturas_catalog WHERE categoria=? ORDER BY id",
                [categoria]
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM mmt_coberturas_catalog ORDER BY categoria, id"
            ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route('/motor/primas-medias', methods=['GET'])
@require_key
def get_motor_primas_medias():
    """Devuelve primas medias MMT. Params: tipologia, fecha_foto, id_cobertura."""
    tipologia    = request.args.get('tipologia', '').strip()
    fecha_foto   = request.args.get('fecha_foto', '').strip()
    id_cobertura = request.args.get('id_cobertura', '').strip()
    conn = get_conn()
    try:
        filters, params = [], []
        if tipologia:    filters.append("tipologia=?");    params.append(tipologia)
        if fecha_foto:   filters.append("fecha_foto=?");   params.append(fecha_foto)
        if id_cobertura: filters.append("id_cobertura=?"); params.append(id_cobertura)
        where = f"WHERE {' AND '.join(filters)}" if filters else ''
        rows = conn.execute(
            f"SELECT * FROM mmt_primas_medias {where} ORDER BY tipologia, id_garantia, id_cobertura, fecha_foto",
            params
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route('/motor/import', methods=['POST'])
@require_key
def post_motor_import():
    """
    Importa estadísticas desde TARIFAS.zip.
    Body JSON: { "zip_path": "/ruta/a/TARIFAS.zip" }
    Solo accesible con API key válida (uso interno / admin).
    """
    from motor_import import import_zip, verify_import
    data = request.get_json(force=True) or {}
    zip_path = data.get('zip_path', '').strip()
    usuario  = request.headers.get('X-Username', 'sistema')
    if not zip_path:
        return jsonify({'error': 'zip_path requerido'}), 400
    if not os.path.isfile(zip_path):
        return jsonify({'error': f'Archivo no encontrado: {zip_path}'}), 404

    result = import_zip(zip_path, usuario=usuario)
    if not result['ok']:
        return jsonify({'error': result['error']}), 500

    verification = verify_import()
    result['verificacion'] = verification
    return jsonify(result)


@app.route('/motor/diagnostico', methods=['POST'])
@require_key
def post_motor_diagnostico():
    """
    Calcula el diagnóstico de coste para un grupo de vehículos.

    Body JSON:
    {
      "tipologia_mmt": "TRACTOCAMION",      # nombre exacto en mmt_stats
      "n_vehiculos": 20,
      "sinco_freq": 0.16,                   # frecuencia RC SINCO del grupo (null si no disponible)
      "coberturas": ["RCO_1","RCO_2","DEFC_1"],  # garantías hija contratadas
      "fecha_foto": "202609"                # snapshot a usar
    }

    Respuesta: coste por garantía, escenarios RC, estado, advertencias.
    """
    data = request.get_json(force=True) or {}
    tipologia   = data.get('tipologia_mmt', '').strip()
    n_veh       = data.get('n_vehiculos', 0)
    sinco_freq  = data.get('sinco_freq')        # puede ser null
    coberturas  = data.get('coberturas', [])    # lista de id_cobertura
    fecha_foto  = (data.get('fecha_foto') or '').strip()

    if not fecha_foto:
        conn_p = get_conn()
        try:
            fp = conn_p.execute("SELECT valor FROM motor_params WHERE clave='foto_activa'").fetchone()
            if fp and fp['valor'] is not None:
                # valor puede ser int/float cuando SQLite convierte el texto '202609'
                raw = fp['valor']
                fecha_foto = str(int(raw)) if isinstance(raw, (int, float)) else str(raw).strip()
        finally:
            conn_p.close()
    if not fecha_foto:
        fecha_foto = '202609'

    if not tipologia or n_veh <= 0:
        return jsonify({'error': 'tipologia_mmt y n_vehiculos > 0 requeridos'}), 400

    conn = get_conn()
    try:
        # Cargar todos los registros de esta tipología y foto
        rows = conn.execute(
            "SELECT * FROM mmt_stats WHERE tipologia=? AND fecha_foto=?",
            [tipologia, fecha_foto]
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return jsonify({
            'estado': 'no_calculable',
            'advertencias': [f'Sin datos MMT para {tipologia} / {fecha_foto}'],
            'grupos': [],
        })

    stats_by_cob = {r['id_cobertura']: dict(r) for r in rows}
    advertencias = []
    grupos = []

    # LCE_1 = "Subsidio por Paralización del vehículo" — no equivale al producto
    # AV completo. Se usa como proxy cuando la tipología no tiene AV_1 en mmt_stats.
    if 'LCE_1' in coberturas:
        advertencias.append(
            'LCE_1 (Subsidio por Paralización del vehículo) utilizado como referencia '
            'de Asistencia en Viaje — equivalencia con el producto AV completo no '
            'verificada documentalmente. La prima de esta cobertura es orientativa.'
        )

    # ── RC historial multi-foto (contexto comparativo) ────────────────────────
    conn2 = get_conn()
    try:
        rc_hist_rows = conn2.execute(
            "SELECT fecha_foto, prima, coste, exposicion, stros, lr FROM mmt_stats "
            "WHERE tipologia=? AND id_cobertura='RCO_1' ORDER BY fecha_foto",
            [tipologia]
        ).fetchall()
        rco2_hist = {r['fecha_foto']: dict(r) for r in conn2.execute(
            "SELECT fecha_foto, prima, coste, exposicion FROM mmt_stats "
            "WHERE tipologia=? AND id_cobertura='RCO_2' ORDER BY fecha_foto",
            [tipologia]
        ).fetchall()}
    finally:
        conn2.close()

    rc_historial_fotos = []
    for rh in rc_hist_rows:
        f = rh['fecha_foto']
        r2h = rco2_hist.get(f)
        exp1 = rh['exposicion'] or 0
        cp1  = rh['coste']  / exp1 if exp1 > 0 else 0
        pm1  = (rh['prima'] / exp1) if (rh['prima'] is not None and exp1 > 0) else 0
        exp2 = (r2h['exposicion'] or 0) if r2h else 0
        cp2  = (r2h['coste'] / exp2) if (r2h and exp2 > 0) else 0
        pm2  = (r2h['prima'] / exp2) if (r2h and r2h['prima'] is not None and exp2 > 0) else 0
        rc_historial_fotos.append({
            'fecha_foto':      f,
            'coste_rc_veh':    round(cp1 + cp2, 2),
            'prima_mmt_rc_veh': round(pm1 + pm2, 2),
            'lr_rco1':         round(rh['lr'], 4) if rh['lr'] is not None else None,
            'stros':           rh['stros'],
        })

    # ── RC: RCO_1 y RCO_2 con ajuste SINCO ───────────────────────────────────
    rco1 = stats_by_cob.get('RCO_1')
    rco2 = stats_by_cob.get('RCO_2')
    rc_diagnostico = None

    if rco1 and rco1['exposicion'] > 0 and rco1['stros'] > 0:
        mmt_freq_rco1    = rco1['stros'] / rco1['exposicion']
        coste_puro_rco1  = rco1['coste'] / rco1['exposicion']
        coste_puro_rco2  = (rco2['coste'] / rco2['exposicion']) if (rco2 and rco2['exposicion'] > 0) else 0
        coste_puro_rc_mmt = coste_puro_rco1 + coste_puro_rco2
        lr_rco1 = rco1.get('lr')  # ratio de pérdida de la foto activa
        # prima media MMT por veh (prima/exposicion) — dato estadístico comercial real
        prima_mmt_rco1_veh = (rco1['prima'] / rco1['exposicion']) if (rco1['prima'] is not None and rco1['exposicion'] > 0) else None
        prima_mmt_rco2_veh = (rco2['prima'] / rco2['exposicion']) if (rco2 and rco2['prima'] is not None and rco2['exposicion'] > 0) else 0
        prima_mmt_rc_veh   = round((prima_mmt_rco1_veh or 0) + prima_mmt_rco2_veh, 4)

        # Advertir si el período captura siniestralidad excepcionalmente alta
        lr_excepcional = lr_rco1 is not None and lr_rco1 > 1.5
        if lr_excepcional:
            advertencias.append(
                f'Foto {fecha_foto}: ratio de pérdida RC = {lr_rco1:.2%} — '
                f'período con siniestros de coste excepcional (coste > prima MMT). '
                f'La referencia técnica RC de esta foto puede estar distorsionada; '
                f'contrastar con períodos anteriores antes de aceptar.'
            )

        if sinco_freq is not None and sinco_freq > 0:
            ratio_sinco = sinco_freq / mmt_freq_rco1 if mmt_freq_rco1 > 0 else None

            if ratio_sinco is not None:
                coste_rc_por_veh = coste_puro_rc_mmt * ratio_sinco
                coste_rc_grupo   = n_veh * coste_rc_por_veh

                # Escenario alto: denominador RCO_1 stros (solapamiento total RCO_2 en RCO_1)
                sev_alto = (rco1['coste'] + (rco2['coste'] if rco2 else 0)) / rco1['stros']
                esc_alto = n_veh * sinco_freq * sev_alto

                # Escenario bajo: denominador RCO_1+RCO_2 stros (sin solapamiento)
                stros_bajo = rco1['stros'] + (rco2['stros'] if rco2 else 0)
                sev_bajo   = (rco1['coste'] + (rco2['coste'] if rco2 else 0)) / stros_bajo
                esc_bajo   = n_veh * sinco_freq * sev_bajo

                if ratio_sinco > 1.5:
                    advertencias.append(f'ratio_SINCO={ratio_sinco:.3f} — flota con siniestralidad superior a media MMT')

                rc_diagnostico = {
                    'tipo': 'rc_con_sinco',
                    'mmt_freq_rco1':       round(mmt_freq_rco1, 6),
                    'lr_rco1':             round(lr_rco1, 4) if lr_rco1 is not None else None,
                    'prima_mmt_veh':       prima_mmt_rc_veh,
                    'sinco_freq':          sinco_freq,
                    'ratio_sinco':         round(ratio_sinco, 4),
                    'coste_puro_rco1_veh': round(coste_puro_rco1, 4),
                    'coste_puro_rco2_veh': round(coste_puro_rco2, 4),
                    'coste_rc_por_veh':    round(coste_rc_por_veh, 2),
                    'coste_rc_grupo':      round(coste_rc_grupo, 2),
                    'escenario_alto_grupo': round(esc_alto, 2),
                    'escenario_bajo_grupo': round(esc_bajo, 2),
                    'nota': 'Escenarios condicionales — solapamiento RCO1/RCO2 no confirmado',
                    'rc_historial_fotos':  rc_historial_fotos,
                }
            else:
                advertencias.append('mmt_freq_rco1 = 0 — ratio SINCO no calculable')
                rc_diagnostico = {
                    'tipo': 'rc_sin_ratio',
                    'coste_puro_rc_mmt_veh': round(coste_puro_rc_mmt, 4),
                    'mmt_freq_rco1': round(mmt_freq_rco1, 6),
                    'lr_rco1': round(lr_rco1, 4) if lr_rco1 is not None else None,
                    'prima_mmt_veh': prima_mmt_rc_veh,
                    'rc_historial_fotos': rc_historial_fotos,
                }
        elif sinco_freq is not None and sinco_freq == 0:
            # freq=0 no implica coste futuro 0 — usar diagnóstico base MMT con aviso
            advertencias.append('Frecuencia SINCO = 0 — sin modelo de credibilidad autorizado, se muestra diagnóstico base MMT')
            rc_diagnostico = {
                'tipo': 'rc_sin_sinco',
                'coste_puro_rc_mmt_veh': round(coste_puro_rc_mmt, 4),
                'coste_rc_grupo_base':   round(n_veh * coste_puro_rc_mmt, 2),
                'mmt_freq_rco1':         round(mmt_freq_rco1, 6),
                'lr_rco1':               round(lr_rco1, 4) if lr_rco1 is not None else None,
                'prima_mmt_veh':         prima_mmt_rc_veh,
                'rc_historial_fotos':    rc_historial_fotos,
            }
        else:
            # Sin SINCO (None): coste histórico MMT directo como referencia
            advertencias.append('Sin frecuencia SINCO para este grupo — coste RC = diagnóstico MMT base')
            rc_diagnostico = {
                'tipo': 'rc_sin_sinco',
                'coste_puro_rc_mmt_veh': round(coste_puro_rc_mmt, 4),
                'coste_rc_grupo_base':   round(n_veh * coste_puro_rc_mmt, 2),
                'mmt_freq_rco1':         round(mmt_freq_rco1, 6),
                'lr_rco1':               round(lr_rco1, 4) if lr_rco1 is not None else None,
                'prima_mmt_veh':         prima_mmt_rc_veh,
                'rc_historial_fotos':    rc_historial_fotos,
            }
    else:
        lr_excepcional = False
        advertencias.append('Sin datos RCO_1 válidos para RC')

    grupos.append({'garantia': 'RC', 'detalle': rc_diagnostico})

    # ── Otras garantías (sin ajuste SINCO) ────────────────────────────────────
    coberturas_no_rc = [c for c in coberturas if c not in ('RCO_1', 'RCO_2')]
    for cob_id in coberturas_no_rc:
        g = stats_by_cob.get(cob_id)
        if not g:
            advertencias.append(f'{cob_id}: sin datos en {tipologia}/{fecha_foto}')
            grupos.append({'garantia': cob_id, 'detalle': {'tipo': 'no_calculable', 'razon': 'sin datos'}})
            continue

        if g['exposicion'] <= 0:
            advertencias.append(f'{cob_id}: exposición = 0')
            grupos.append({'garantia': cob_id, 'detalle': {'tipo': 'no_calculable', 'razon': 'exposicion = 0'}})
            continue

        coste_puro_veh = g['coste'] / g['exposicion']
        coste_grupo    = n_veh * coste_puro_veh
        # prima media MMT para esta cobertura (dato comercial real, independiente del coste técnico)
        prima_mmt_veh_cob = round(g['prima'] / g['exposicion'], 4) if (g['prima'] is not None and g['exposicion'] > 0) else None

        detalle = {
            'tipo': 'coste_historico_mmt',
            'coste_puro_veh': round(coste_puro_veh, 4),
            'coste_grupo':    round(coste_grupo, 2),
            'stros':          g['stros'],
            'exposicion':     round(g['exposicion'], 4),
            'prima_mmt_veh':  prima_mmt_veh_cob,
        }

        if g['stros'] == 0:
            advertencias.append(f'{cob_id}: cero siniestros observados en {fecha_foto} — estadística insuficiente para este período, coste MMT = 0')
            detalle['tipo'] = 'cero_siniestros'

        grupos.append({'garantia': cob_id, 'detalle': detalle})

    # ── Totales y estado ──────────────────────────────────────────────────────
    coste_total_grupo = 0.0
    prima_orientativa_mmt_total = 0.0
    prima_mmt_incompleta = False  # True si alguna cobertura no tiene prima_mmt_veh
    estado = 'calculado'

    for grp in grupos:
        d = grp.get('detalle') or {}
        tipo = d.get('tipo')
        # Coste técnico (Option A)
        if tipo == 'rc_con_sinco':
            coste_total_grupo += d.get('escenario_alto_grupo', 0)
        elif tipo == 'rc_sin_sinco':
            coste_total_grupo += d.get('coste_rc_grupo_base', 0)
            estado = 'revisar'
        elif tipo in ('coste_historico_mmt', 'cero_siniestros'):
            coste_total_grupo += d.get('coste_grupo', 0)
            if tipo == 'cero_siniestros':
                estado = 'revisar'
        elif tipo == 'no_calculable':
            estado = 'revisar'
        # Prima media MMT (Option B) — suma de prima/exposicion de cada cobertura
        pmv = d.get('prima_mmt_veh')
        if pmv is not None:
            prima_orientativa_mmt_total += pmv
        else:
            prima_mmt_incompleta = True

    prima_orientativa_mmt_veh = round(prima_orientativa_mmt_total, 2) if prima_orientativa_mmt_total > 0 else None

    # ── Prima técnica ORION (ajuste de riesgo sobre primas medias MMT) ──────────
    # RC: prima_mmt_rc × (sinco_freq / mmt_freq_rco1) si SINCO válido; prima_mmt directa si no
    # Otras garantías: prima_mmt directa sin ajuste individual
    sinco_n_exposicion  = data.get('sinco_n_exposicion')   # veh·años aprox en SINCO (opcional)

    prima_tecnica_total    = 0.0
    prima_tecnica_parcial  = False
    prima_tecnica_detalle  = []
    prima_tecnica_sin_datos = []

    rc_grp = next((g for g in grupos if g['garantia'] == 'RC'), None)
    if rc_grp:
        d_rc    = rc_grp['detalle'] or {}
        pm_rc   = d_rc.get('prima_mmt_veh')
        freq_mmt = d_rc.get('mmt_freq_rco1')
        if pm_rc is not None and pm_rc > 0:
            if sinco_freq is not None and sinco_freq > 0 and freq_mmt and freq_mmt > 0:
                ratio = sinco_freq / freq_mmt
                prima_rc_tecnica = round(pm_rc * ratio, 2)
                tipo_rc  = 'rc_ajustado_sinco'
                nota_rc  = (f'Prima MMT RC {pm_rc:.2f} × ratio {ratio:.3f} '
                            f'(freq. flota {sinco_freq:.4f} / freq. MMT {freq_mmt:.4f})')
                if ratio > 3.0:
                    advertencias.append(
                        f'Ratio SINCO/MMT RC = {ratio:.2f} (>3.0) — siniestralidad muy superior '
                        f'a la media de mercado; ajuste de RC puede ser poco fiable')
                elif ratio < 0.2:
                    advertencias.append(
                        f'Ratio SINCO/MMT RC = {ratio:.2f} (<0.2) — siniestralidad muy inferior '
                        f'a la media de mercado; ajuste de RC puede ser poco fiable')
                if sinco_n_exposicion is not None and sinco_n_exposicion < 10:
                    advertencias.append(
                        f'Exposición SINCO reducida (~{sinco_n_exposicion:.0f} veh·años) — '
                        f'ajuste de frecuencia con baja credibilidad estadística')
                prima_tecnica_detalle.append({
                    'garantia': 'RC', 'prima_tecnica_veh': prima_rc_tecnica,
                    'tipo': tipo_rc, 'ratio_sinco': round(ratio, 4), 'nota': nota_rc,
                })
            else:
                prima_rc_tecnica = round(pm_rc, 2)
                tipo_rc = 'rc_referencia_mmt'
                nota_rc = 'Sin exposición SINCO válida — prima media MMT sin ajuste individual'
                prima_tecnica_detalle.append({
                    'garantia': 'RC', 'prima_tecnica_veh': prima_rc_tecnica,
                    'tipo': tipo_rc, 'ratio_sinco': None, 'nota': nota_rc,
                })
            prima_tecnica_total += prima_rc_tecnica
        else:
            prima_tecnica_parcial = True
            prima_tecnica_sin_datos.append('RC — sin prima_mmt calculable')
    else:
        prima_tecnica_parcial = True
        prima_tecnica_sin_datos.append('RC — sin datos en mmt_stats')

    for grp in grupos:
        if grp['garantia'] == 'RC':
            continue
        d_g  = grp['detalle'] or {}
        pm_g = d_g.get('prima_mmt_veh')
        gar  = grp['garantia']
        if pm_g is not None:
            prima_tecnica_total += pm_g
            prima_tecnica_detalle.append({
                'garantia': gar, 'prima_tecnica_veh': round(pm_g, 4),
                'tipo': 'prima_mmt_referencia', 'ratio_sinco': None,
                'nota': 'Prima media comercial MMT — sin ajuste individual',
            })
        else:
            prima_tecnica_parcial = True
            prima_tecnica_sin_datos.append(f'{gar} — sin prima_mmt en mmt_stats para {tipologia}')

    prima_tecnica_orion_veh = round(prima_tecnica_total, 2) if prima_tecnica_total > 0 else None

    # ── Verificar parámetros económicos para prima rentable (Option C) ────────
    conn = get_conn()
    try:
        params = {r['clave']: r['valor'] for r in conn.execute("SELECT clave, valor FROM motor_params").fetchall()}
    finally:
        conn.close()

    params_requeridos = ('gastos_variables_pct', 'comision_pct', 'margen_pct')
    params_faltantes = [k for k in params_requeridos if params.get(k) is None]
    params_ok = len(params_faltantes) == 0

    prima_orion = None
    if params_ok:
        gv  = params.get('gastos_variables_pct', 0) or 0
        com = params.get('comision_pct', 0) or 0
        mar = params.get('margen_pct', 0) or 0
        gf_veh = params.get('gastos_fijos_por_vehiculo') or 0
        denominador = 1 - gv - com - mar
        if denominador > 0:
            prima_orion = round((coste_total_grupo + n_veh * gf_veh) / denominador, 2)
    else:
        # Mensaje específico: lista exacta de parámetros que faltan
        advertencias.append(
            f'Prima rentable ORION bloqueada — faltan en ADMIN→Motor: '
            f'{", ".join(params_faltantes)}'
        )

    return jsonify({
        'tipologia':                    tipologia,
        'fecha_foto':                   fecha_foto,
        'n_vehiculos':                  n_veh,
        'sinco_freq':                   sinco_freq,
        'coste_total_grupo':            round(coste_total_grupo, 2),
        'coste_por_vehiculo':           round(coste_total_grupo / n_veh, 2) if n_veh > 0 else None,
        'prima_orientativa_mmt_grupo':  round(prima_orientativa_mmt_total * n_veh, 2) if prima_orientativa_mmt_veh else None,
        'prima_orientativa_mmt_veh':    prima_orientativa_mmt_veh,
        'prima_mmt_parcial':            prima_mmt_incompleta,
        'prima_tecnica_orion_veh':      prima_tecnica_orion_veh,
        'prima_tecnica_orion_grupo':    round(prima_tecnica_total * n_veh, 2) if prima_tecnica_orion_veh else None,
        'prima_tecnica_parcial':        prima_tecnica_parcial,
        'prima_tecnica_sin_datos':      prima_tecnica_sin_datos,
        'prima_tecnica_detalle':        prima_tecnica_detalle,
        'prima_orion_grupo':            prima_orion,
        'prima_orion_veh':              round(prima_orion / n_veh, 2) if (prima_orion and n_veh > 0) else None,
        'estado':                       estado,
        'advertencias':                 advertencias,
        'grupos':                       grupos,
    })


# ─── CONSULTAS DE VEHÍCULOS (normales y masivas) ─────────────────────────────

@app.route('/consultas-vehiculos', methods=['GET'])
@require_key
def get_consultas_vehiculos():
    """Lista sin el contenido (data): para el directorio de consultas guardadas."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, tipo, nombre, creado_por, n_vehiculos, n_identificados, created_at, updated_at
        FROM consultas_vehiculos ORDER BY updated_at DESC LIMIT 500
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/consultas-vehiculos/<cid>', methods=['GET'])
@require_key
def get_consulta_vehiculos(cid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM consultas_vehiculos WHERE id=?", [cid]).fetchone()
    conn.close()
    if not row:
        return jsonify({'ok': False, 'error': 'No existe'}), 404
    d = dict(row)
    try:
        d['data'] = json.loads(d.get('data') or '{}')
    except Exception:
        d['data'] = {}
    return jsonify({'ok': True, 'consulta': d})


@app.route('/consultas-vehiculos', methods=['POST'])
@require_key
def post_consultas_vehiculos():
    body   = request.get_json(silent=True) or {}
    action = body.get('action')
    conn   = get_conn()
    try:
        if action == 'upsert':
            c  = body.get('consulta') or {}
            cid = str(c.get('id', '')).strip()
            if not cid:
                return jsonify({'ok': False, 'error': 'Falta id'}), 400
            tipo = 'masiva' if c.get('tipo') == 'masiva' else 'normal'
            conn.execute("""
                INSERT INTO consultas_vehiculos
                    (id, tipo, nombre, creado_por, n_vehiculos, n_identificados, created_at, updated_at, data)
                VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET
                    nombre=excluded.nombre, n_vehiculos=excluded.n_vehiculos,
                    n_identificados=excluded.n_identificados,
                    updated_at=excluded.updated_at, data=excluded.data
            """, [cid, tipo, str(c.get('nombre', ''))[:200], str(c.get('creado_por', ''))[:80],
                  int(c.get('n_vehiculos') or 0), int(c.get('n_identificados') or 0),
                  now_iso(), now_iso(), json.dumps(c.get('data') or {})])
            conn.commit()
        elif action == 'delete':
            conn.execute("DELETE FROM consultas_vehiculos WHERE id=?", [str(body.get('id', ''))])
            conn.commit()
        else:
            return jsonify({'ok': False, 'error': 'Acción desconocida'}), 400
    finally:
        conn.close()
    return jsonify({'ok': True})


# ─── VENTANAS DE AÑOS DEL SISTEMA DE EMISIÓN ─────────────────────────────────

@app.route('/ventanas-sistema', methods=['GET'])
@require_key
def get_ventanas_sistema():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM ventanas_sistema ORDER BY id_veh").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/ventanas-sistema', methods=['POST'])
@require_key
def post_ventanas_sistema():
    """{ ventanas: [{id, fabMin, fabMax, matMin?, matMax?, fuente?}], usuario? }  Fusiona sobre lo que ya hay."""
    body = request.get_json(silent=True) or {}
    lista = body.get('ventanas') or []
    usuario = str(body.get('usuario', ''))[:80]
    conn = get_conn()
    n = 0
    try:
        for v in lista[:2000]:
            vid = str(v.get('id', '')).strip()
            if not vid.isdigit():
                continue
            def ent(k):
                try:
                    x = int(v.get(k) or 0)
                    return x if 1900 < x < 2100 else None
                except Exception:
                    return None
            fmin, fmax, mmin, mmax = ent('fabMin'), ent('fabMax'), ent('matMin'), ent('matMax')
            if not (fmin and fmax) and not (mmin and mmax):
                continue
            conn.execute("""
                INSERT INTO ventanas_sistema (id_veh, fab_min, fab_max, mat_min, mat_max, fuente, updated_by, updated_at)
                VALUES (?,?,?,?,?,?,?,?)
                ON CONFLICT(id_veh) DO UPDATE SET
                    fab_min = CASE WHEN excluded.fab_min > 0 THEN excluded.fab_min ELSE fab_min END,
                    fab_max = CASE WHEN excluded.fab_max > 0 THEN excluded.fab_max ELSE fab_max END,
                    mat_min = COALESCE(excluded.mat_min, mat_min),
                    mat_max = COALESCE(excluded.mat_max, mat_max),
                    fuente = CASE WHEN excluded.fuente <> '' THEN excluded.fuente ELSE fuente END, updated_by = excluded.updated_by, updated_at = excluded.updated_at
            """, [vid, fmin or 0, fmax or 0, mmin, mmax, str(v.get('fuente', ''))[:120], usuario, now_iso()])
            n += 1
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True, 'guardadas': n})


# ─── Ping ─────────────────────────────────────────────────────────────────────

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'service': 'orion-api'})


# ─── Arranque ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        from waitress import serve
        port = int(os.environ.get('PORT', 3001))
        print(f"[orion-api] Iniciando en http://127.0.0.1:{port}")
        serve(app, host='127.0.0.1', port=port, threads=12)
    except ImportError:
        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 3001)), debug=False, threaded=True)
