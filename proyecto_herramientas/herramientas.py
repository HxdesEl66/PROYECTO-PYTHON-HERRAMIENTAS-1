# herramientas.py

from typing import Dict, List, Optional
from storage import leer_json, guardar_json
from config import HERRAMIENTAS_JSON
from models import Herramienta
from logger import log_info, log_error

def listar_herramientas() -> List[Dict]:
    return leer_json(HERRAMIENTAS_JSON)

def buscar_herramienta_por_id(herr_id: str) -> Optional[Dict]:
    herramientas = listar_herramientas()
    for h in herramientas:
        if h["id"] == herr_id:
            return h
    return None

def crear_herramienta(data: Dict) -> bool:
    try:
        herramientas = listar_herramientas()
        if any(h["id"] == data["id"] for h in herramientas):
            log_error("ID de herramienta ya existe.")
            return False
        herramienta = Herramienta(**data)
        herramientas.append(herramienta.to_dict())
        ok = guardar_json(HERRAMIENTAS_JSON, herramientas)
        if ok:
            log_info(f"Herramienta creada: {herramienta.id}")
        return ok
    except Exception as e:
        log_error(f"Error creando herramienta: {e}")
        return False

def actualizar_herramienta(herr_id: str, cambios: Dict) -> bool:
    try:
        herramientas = listar_herramientas()
        for i, h in enumerate(herramientas):
            if h["id"] == herr_id:
                herramientas[i].update(cambios)
                ok = guardar_json(HERRAMIENTAS_JSON, herramientas)
                if ok:
                    log_info(f"Herramienta actualizada: {herr_id}")
                return ok
        log_error("Herramienta no encontrada para actualizar.")
        return False
    except Exception as e:
        log_error(f"Error actualizando herramienta: {e}")
        return False

def inactivar_herramienta(herr_id: str) -> bool:
    return actualizar_herramienta(herr_id, {"estado": "INACTIVA"})

def eliminar_herramienta(herr_id: str) -> bool:
    try:
        herramientas = listar_herramientas()
        nuevas = [h for h in herramientas if h["id"] != herr_id]
        if len(nuevas) == len(herramientas):
            log_error("Herramienta no encontrada para eliminar.")
            return False
        ok = guardar_json(HERRAMIENTAS_JSON, nuevas)
        if ok:
            log_info(f"Herramienta eliminada: {herr_id}")
        return ok
    except Exception as e:
        log_error(f"Error eliminando herramienta: {e}")
        return False
