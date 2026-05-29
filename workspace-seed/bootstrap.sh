#!/usr/bin/env bash
# bootstrap.sh — Ejecutado por el wrapper de OpenClaw (server.js línea ~1416)
# al arrancar el container. Sirve para instalar deps persistentes en /data
# y preparar el entorno antes de que la gateway esté lista.

set -euo pipefail

echo "[bootstrap] starting at $(date)"

# 1. Asegurar directorios persistentes
mkdir -p /data/workspace/data
mkdir -p /data/workspace/nutricion

# 2. Crear venv Python persistente si no existe
if [ ! -d /data/venv ]; then
  echo "[bootstrap] creating persistent python venv at /data/venv"
  python3 -m venv /data/venv
fi

# 3. Instalar dependencias Python para los scripts de sheets + análisis financiero
/data/venv/bin/pip install --quiet --upgrade pip
/data/venv/bin/pip install --quiet \
  google-api-python-client \
  google-auth \
  google-auth-httplib2 \
  google-auth-oauthlib \
  yfinance \
  pandas \
  numpy

# 4. Symlink python3 del venv para que los scripts lo encuentren primero
ln -sf /data/venv/bin/python3 /data/bin/python3 2>/dev/null || mkdir -p /data/bin && ln -sf /data/venv/bin/python3 /data/bin/python3

echo "[bootstrap] done at $(date)"
