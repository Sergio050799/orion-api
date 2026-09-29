#!/bin/bash
# Deploy orion-api al VPS
# Ejecutar en el VPS como root: bash deploy_vps.sh

set -e

DEPLOY_DIR="/opt/orion-api"
APP_DIR="/opt/orion-app"

echo "=== orion-api deploy ==="

# 1. Crear directorio y copiar archivos
mkdir -p "$DEPLOY_DIR/data"
# Los archivos ya deben estar copiados via scp o git pull antes de este script

# 2. Instalar dependencias Python
cd "$DEPLOY_DIR"
pip3 install flask waitress

# 3. Verificar que las variables de entorno están definidas
if [ -z "$ORION_API_KEY" ]; then
    echo "ERROR: ORION_API_KEY no definida. Definela con:"
    echo "  export ORION_API_KEY=<clave_segura>"
    exit 1
fi

export ORION_DB_PATH="$DEPLOY_DIR/data/orion.db"
export PORT=3001

# 4. Arrancar con PM2
pm2 delete orion-api 2>/dev/null || true
pm2 start "python3 app.py" --name orion-api
pm2 save

echo "=== orion-api corriendo en localhost:3001 ==="

# 5. Verificar que NO está expuesto al exterior
echo "Verificando que port 3001 NO es accesible desde fuera..."
if curl -s --max-time 2 "http://0.0.0.0:3001/ping" | grep -q "orion-api" 2>/dev/null; then
    echo "ADVERTENCIA: port 3001 podria estar expuesto. Verificar nginx."
fi

# 6. Actualizar .env.production y rebuild Orion_APP
cd "$APP_DIR"
if [ -f ".env.production" ]; then
    # Actualizar ORION_API_URL y ORION_API_KEY
    sed -i "s|ORION_API_URL=.*|ORION_API_URL=http://localhost:3001|" .env.production
    sed -i "s|ORION_API_KEY=.*|ORION_API_KEY=$ORION_API_KEY|" .env.production
    echo "ORION_API_URL actualizado en .env.production"
else
    echo "ORION_API_URL=http://localhost:3001" >> .env.production
    echo "ORION_API_KEY=$ORION_API_KEY" >> .env.production
    echo "Creado .env.production"
fi

# 7. Rebuild y restart
npm run build
pm2 restart orion-app

echo ""
echo "=== Smoke test ==="
sleep 3
RESULT=$(curl -s --max-time 5 "https://myorion.online/api/flotas/carpetas")
if echo "$RESULT" | grep -q "\["; then
    echo "OK — /api/flotas/carpetas responde correctamente"
else
    echo "ERROR — Respuesta inesperada: $RESULT"
fi
