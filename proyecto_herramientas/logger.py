# logger.py

import logging
from config import LOG_DIR
import os

LOG_FILE = os.path.join(LOG_DIR, "eventos.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_info(mensaje: str):
    logging.info(mensaje)

def log_error(mensaje: str):
    logging.error(mensaje)
