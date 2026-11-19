"""
Amplía el schema V5 con sucursales + comerciales y columnas nuevas en flotas/estudios.
Idempotente: se puede correr múltiples veces sin romper nada.

Uso:
    python scripts/schema_v5_sucursal_comercial.py --apply
    python scripts/schema_v5_sucursal_comercial.py --dry-run
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
import time

DB_PATH = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')

SUCURSALES = ['TITAN', 'MEDIACION']
COMERCIALES = {
    'TITAN': ['AGUSTIN', 'IKER', 'RAQUEL'],
    'MEDIACION': ['MIGUEL', 'ROBERTO', 'JAVIER', 'ANTONIO'],
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}_{os.urandom(3).hex()}"


def crear_tablas(conn: sqlite3.Connection, dry: bool) -> list[str]:
    cur = conn.cursor()
    acciones = []
    for sql in [
        """CREATE TABLE IF NOT EXISTS sucursales (
            id     TEXT PRIMARY KEY,
            nombre TEXT UNIQUE NOT NULL,
            activa INTEGER NOT NULL DEFAULT 1,
            creado_en TEXT NOT NULL DEFAULT (datetime('now'))
        )""",
        """CREATE TABLE IF NOT EXISTS comerciales (
            id          TEXT PRIMARY KEY,
            nombre      TEXT NOT NULL,
            sucursal_id TEXT NOT NULL REFERENCES sucursales(id),
            activo      INTEGER NOT NULL DEFAULT 1,
            creado_en   TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(nombre, sucursal_id)
        )""",
        "CREATE INDEX IF NOT EXISTS idx_comerciales_sucursal ON comerciales(sucursal_id)",
    ]:
        if not dry:
            cur.execute(sql)
        acciones.append(sql.split('\n')[0][:80])

    # Columnas nuevas: ALTER TABLE ADD COLUMN sin IF NOT EXISTS → chequear antes
    def _tiene_col(tabla, col):
        rows = cur.execute(f"PRAGMA table_info({tabla})").fetchall()
        return any(r[1] == col for r in rows)

    for tabla, col, sql_alter in [
        ('flotas',   'comercial_traido_id', "ALTER TABLE flotas   ADD COLUMN comercial_traido_id TEXT REFERENCES comerciales(id)"),
        ('estudios', 'comercial_id',        "ALTER TABLE estudios ADD COLUMN comercial_id        TEXT REFERENCES comerciales(id)"),
    ]:
        if not _tiene_col(tabla, col):
            if not dry:
                cur.execute(sql_alter)
            acciones.append(sql_alter[:80])
        else:
            acciones.append(f"-- {tabla}.{col} ya existe")

    # Indices
    for sql in [
        "CREATE INDEX IF NOT EXISTS idx_flotas_comercial_traido ON flotas(comercial_traido_id)",
        "CREATE INDEX IF NOT EXISTS idx_estudios_comercial     ON estudios(comercial_id)",
    ]:
        if not dry:
            cur.execute(sql)
        acciones.append(sql[:80])

    if not dry:
        conn.commit()
    return acciones


def seed(conn: sqlite3.Connection, dry: bool) -> dict:
    cur = conn.cursor()
    resumen = {'sucursales_nuevas': 0, 'comerciales_nuevas': 0, 'ya_existentes': 0}

    # Sucursales
    suc_ids = {}
    for suc in SUCURSALES:
        row = cur.execute("SELECT id FROM sucursales WHERE nombre = ?", (suc,)).fetchone()
        if row:
            suc_ids[suc] = row[0]
            resumen['ya_existentes'] += 1
        else:
            sid = _uid('sucursal')
            if not dry:
                cur.execute("INSERT INTO sucursales (id, nombre) VALUES (?, ?)", (sid, suc))
            suc_ids[suc] = sid
            resumen['sucursales_nuevas'] += 1

    # Comerciales
    for suc, lista in COMERCIALES.items():
        sid = suc_ids.get(suc)
        if not sid:
            continue
        for nombre in lista:
            row = cur.execute(
                "SELECT id FROM comerciales WHERE nombre = ? AND sucursal_id = ?",
                (nombre, sid)
            ).fetchone()
            if row:
                resumen['ya_existentes'] += 1
            else:
                cid = _uid('comercial')
                if not dry:
                    cur.execute("""
                        INSERT INTO comerciales (id, nombre, sucursal_id)
                        VALUES (?, ?, ?)
                    """, (cid, nombre, sid))
                resumen['comerciales_nuevas'] += 1

    if not dry:
        conn.commit()
    return resumen


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--apply', action='store_true')
    g.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    print(f"BD: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] no existe BD", file=sys.stderr)
        return 1

    dry = args.dry_run
    conn = sqlite3.connect(DB_PATH)
    try:
        acciones = crear_tablas(conn, dry)
        print(f"\n[Schema] {'(dry-run)' if dry else '(APLICADO)'}")
        for a in acciones:
            print(f"  {a}")

        resumen = seed(conn, dry)
        print(f"\n[Seed] {'(dry-run)' if dry else '(APLICADO)'}")
        print(f"  Sucursales nuevas:    {resumen['sucursales_nuevas']}")
        print(f"  Comerciales nuevas:   {resumen['comerciales_nuevas']}")
        print(f"  Ya existentes:        {resumen['ya_existentes']}")

        # Verificar
        conn.row_factory = sqlite3.Row
        print("\n[Verificación]")
        for r in conn.execute("""
            SELECT s.nombre AS suc, GROUP_CONCAT(c.nombre, ', ') AS comerciales
            FROM sucursales s
            LEFT JOIN comerciales c ON c.sucursal_id = s.id
            GROUP BY s.id ORDER BY s.nombre
        """).fetchall():
            print(f"  {r['suc']}: {r['comerciales']}")
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
