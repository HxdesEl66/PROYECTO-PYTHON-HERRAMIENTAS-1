# prestamos.py

from typing import Dict, List, Optional
from storage import leer_json, guardar_json
from config import PRESTAMOS_JSON, HERRAMIENTAS_JSON
from models import Prestamo
from logger import log_info, log_error
from herramientas import buscar_herramienta_por_id, actualizar_herramienta

def listar_prestamos() -> List[Dict]:
    return leer_json(PRESTAMOS_JSON)

def buscar_prestamo_por_id(prestamo_id: str) -> Optional[Dict]:
    prestamos = listar_prestamos()
    for p in prestamos:
        if p["id"] == prestamo_id:
            return p
    return None

def disponibilidad_herramienta(herr_id: str, cantidad: int) -> bool:
    h = buscar_herramienta_por_id(herr_id)
    if not h:
        return False
    return h["cantidad_disponible"] >= cantidad and h["estado"] == "ACTIVA"

def crear_prestamo(data: Dict) -> bool:
    try:
        # Verificar disponibilidad
        if not disponibilidad_herramienta(data["herramienta_id"], data["cantidad"]):
            log_error("Herramienta no disponible o stock insuficiente.")
            return False

        prestamos = listar_prestamos()
        if any(p["id"] == data["id"] for p in prestamos):
            log_error("ID de préstamo ya existe.")
            return False

        # Actualizar stock
        h = buscar_herramienta_por_id(data["herramienta_id"])
        nuevo_stock = h["cantidad_disponible"] - data["cantidad"]
        if not actualizar_herramienta(h["id"], {"cantidad_disponible": nuevo_stock}):
            log_error("No se pudo actualizar stock al crear préstamo.")
            return False

        prestamo = Prestamo(**data)
        prestamos.append(prestamo.to_dict())
        ok = guardar_json(PRESTAMOS_JSON, prestamos)
        if ok:
            log_info(f"Préstamo creado: {prestamo.id}")
        return ok
    except Exception as e:
        log_error(f"Error creando préstamo: {e}")
        return False

def devolver_prestamo(prestamo_id: str, observaciones: str = "") -> bool:
    try:
        prestamos = listar_prestamos()
        for i, p in enumerate(prestamos):
            if p["id"] == prestamo_id:
                if p["estado"] == "DEVUELTO":
                    log_error("Préstamo ya estaba devuelto.")
                    return False
                # Actualizar estado del préstamo
                prestamos[i]["estado"] = "DEVUELTO"
                prestamos[i]["observaciones"] = observaciones

                # Actualizar stock de herramienta
                h = buscar_herramienta_por_id(p["herramienta_id"])
                nuevo_stock = h["cantidad_disponible"] + p["cantidad"]
                if not actualizar_herramienta(h["id"], {"cantidad_disponible": nuevo_stock}):
                    log_error("No se pudo actualizar stock al devolver.")
                    return False

                ok = guardar_json(PRESTAMOS_JSON, prestamos)
                if ok:
                    log_info(f"Préstamo devuelto: {prestamo_id}")
                return ok
        log_error("Préstamo no encontrado para devolución.")
        return False
    except Exception as e:
        log_error(f"Error devolviendo préstamo: {e}")
        return False

def marcar_vencidos(fecha_hoy: str) -> int:
    """Marca préstamos como VENCIDO si fecha_devolucion_estimada < fecha_hoy y estado == ACTIVO."""
    try:
        prestamos = listar_prestamos()
        cambios = 0
        for i, p in enumerate(prestamos):
            if p["estado"] == "ACTIVO" and p["fecha_devolucion_estimada"] < fecha_hoy:
                prestamos[i]["estado"] = "VENCIDO"
                cambios += 1
        if cambios > 0:
            guardar_json(PRESTAMOS_JSON, prestamos)
            log_info(f"Préstamos vencidos marcados: {cambios}")
        return cambios
    except Exception as e:
        log_error(f"Error marcando vencidos: {e}")
        return 0
