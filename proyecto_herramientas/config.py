# config.py

import os

# Rutas de persistencia
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

USUARIOS_JSON = os.path.join(DATA_DIR, "usuarios.json")
HERRAMIENTAS_JSON = os.path.join(DATA_DIR, "herramientas.json")
PRESTAMOS_JSON = os.path.join(DATA_DIR, "prestamos.json")

# Parámetros de negocio
STOCK_BAJO_UMBRAL = 3  # 3 unidades o menos
ROLES_VALIDOS = {"ADMINISTRADOR", "RESIDENTE"}

# Asegurar carpetas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
