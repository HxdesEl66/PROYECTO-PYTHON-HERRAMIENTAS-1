# storage.py

import json
from typing import Any, Dict, List
from logger import log_error, log_info

def leer_json(ruta: str) -> List[Dict[str, Any]]:
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        log_info(f"Archivo no encontrado, se crea vacío: {ruta}")
        guardar_json(ruta, [])
        return []
    except Exception as e:
        log_error(f"Error leyendo {ruta}: {e}")
        return []

def guardar_json(ruta: str, data: List[Dict[str, Any]]) -> bool:
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log_error(f"Error guardando {ruta}: {e}")
        return False
