"""
Backup diario de la BD de Orion.
Uso:  python backup.py
Cron: 0 3 * * * cd /opt/orion-api && ORION_DB_PATH=/opt/orion/data/orion.db python backup.py >> /opt/orion/logs/backup.log 2>&1
"""
import os
import shutil
import glob
import sqlite3
from datetime import datetime

DB_PATH    = os.environ.get('ORION_DB_PATH', '/opt/orion/data/orion.db')
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(DB_PATH)), 'backups')
KEEP_DAYS  = 30


def get_stats(db_path: str) -> dict:
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        hoy = datetime.now().strftime('%Y-%m-%d')
        mes = datetime.now().strftime('%Y-%m')
        stats = {
            'carpetas':   conn.execute("SELECT COUNT(*) FROM carpetas").fetchone()[0],
            'corredores': conn.execute("SELECT COUNT(*) FROM corredores").fetchone()[0],
            'usuarios':   conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
            'sd_cache':   conn.execute("SELECT COUNT(*) FROM vehiculos_silverdat").fetchone()[0],
            'sd_hoy':     conn.execute("SELECT COUNT(*) FROM historial_silverdat WHERE fecha_consulta LIKE ?", [f"{hoy}%"]).fetchone()[0],
            'sd_mes':     conn.execute("SELECT COUNT(*) FROM historial_silverdat WHERE fecha_consulta LIKE ?", [f"{mes}%"]).fetchone()[0],
            'mejoras':    0,
            'audit_hoy':  0,
        }
        try:
            stats['mejoras']   = conn.execute("SELECT COUNT(*) FROM mejoras WHERE estado='pendiente'").fetchone()[0]
            stats['audit_hoy'] = conn.execute("SELECT COUNT(*) FROM audit_log WHERE ts LIKE ?", [f"{hoy}%"]).fetchone()[0]
        except Exception:
            pass
        conn.close()
        return stats
    except Exception as e:
        return {'error': str(e)}


def backup():
    if not os.path.exists(DB_PATH):
        print(f'[backup] ERROR: BD no encontrada en {DB_PATH}')
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d_%H%M')
    dest = os.path.join(BACKUP_DIR, f'orion_{date_str}.db')

    shutil.copy2(DB_PATH, dest)
    size_kb = os.path.getsize(dest) // 1024
    print(f'[backup] Guardado: {dest} ({size_kb} KB)')

    # Mantener solo los últimos KEEP_DAYS backups
    backups = sorted(glob.glob(os.path.join(BACKUP_DIR, 'orion_*.db')))
    to_delete = backups[:-KEEP_DAYS] if len(backups) > KEEP_DAYS else []
    for f in to_delete:
        os.remove(f)
        print(f'[backup] Eliminado antiguo: {os.path.basename(f)}')

    remaining = len(backups) - len(to_delete)
    print(f'[backup] OK — {remaining}/{KEEP_DAYS} copias guardadas')

    # Imprimir stats del día para el log
    stats = get_stats(DB_PATH)
    if 'error' not in stats:
        print(f"[backup] Stats — carpetas:{stats['carpetas']} corredores:{stats['corredores']} "
              f"SD_cache:{stats['sd_cache']} SD_hoy:{stats['sd_hoy']} SD_mes:{stats['sd_mes']} "
              f"mejoras_pend:{stats['mejoras']} acciones_hoy:{stats['audit_hoy']}")
    else:
        print(f"[backup] Stats error: {stats['error']}")


if __name__ == '__main__':
    backup()
