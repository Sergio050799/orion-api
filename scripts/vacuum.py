"""Compacta la BD de ORION.

Pensado para cron semanal del VPS. Libera espacio fragmentado tras muchas
inserciones/borrados. En una BD de ~20 MB tarda <1s y puede liberar la mitad.

Uso:
    python scripts/vacuum.py

En cron del VPS (semanal, domingos a las 4am):
    0 4 * * 0 cd /opt/orion-api && /usr/bin/python3 scripts/vacuum.py >> /var/log/orion-vacuum.log 2>&1
"""
import os
import sys
from datetime import datetime

# Permite ejecutar desde la raíz del repo o desde scripts/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import vacuum_db  # noqa: E402

if __name__ == '__main__':
    ts = datetime.now().isoformat(timespec='seconds')
    print(f"[{ts}] Iniciando VACUUM…")
    before, after = vacuum_db()
    print(f"[{ts}] Hecho.")
