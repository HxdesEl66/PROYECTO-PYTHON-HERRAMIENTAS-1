# reportes.py

from typing import Dict, List
from storage import leer_json
from config import HERRAMIENTAS_JSON, PRESTAMOS_JSON, USUARIOS_JSON, STOCK_BAJO_UMBRAL
from logger import log_error

def herramientas_stock_bajo() -> List[Dict]:
    try:
        herramientas = leer_json(HERRAMIENTAS_JSON)
        return [h for h in herramientas if h["cantidad_disponible"] <= STOCK_BAJO_UMBRAL]
    except Exception as e:
        log_error(f"Error reporte stock bajo: {e}")
        return []

def prestamos_activos_y_vencidos() -> Dict[str, List[Dict]]:
    try:
        prestamos = leer_json(PRESTAMOS_JSON)
        activos = [p for p in prestamos if p["estado"] == "ACTIVO"]
        vencidos = [p for p in prestamos if p["estado"] == "VENCIDO"]
        return {"ACTIVOS": activos, "VENCIDOS": vencidos}
    except Exception as e:
        log_error(f"Error reporte préstamos: {e}")
        return {"ACTIVOS": [], "VENCIDOS": []}

def historial_prestamos_por_usuario(usuario_id: str) -> List[Dict]:
    try:
        prestamos = leer_json(PRESTAMOS_JSON)
        return [p for p in prestamos if p["usuario_id"] == usuario_id]
    except Exception as e:
        log_error(f"Error historial usuario: {e}")
        return []

def herramientas_mas_cotizadas(top: int = 5) -> List[Dict]:
    """Cuenta cuántas veces se prestó cada herramienta y ordena desc."""
    try:
        prestamos = leer_json(PRESTAMOS_JSON)
        conteo = {}
        for p in prestamos:
            hid = p["herramienta_id"]
            conteo[hid] = conteo.get(hid, 0) + 1
        ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top]
        return [{"herramienta_id": hid, "prestamos": cnt} for hid, cnt in ordenado]
    except Exception as e:
        log_error(f"Error herramientas más cotizadas: {e}")
        return []

def usuarios_que_mas_piden(top: int = 5) -> List[Dict]:
    try:
        prestamos = leer_json(PRESTAMOS_JSON)
        conteo = {}
        for p in prestamos:
            uid = p["usuario_id"]
            conteo[uid] = conteo.get(uid, 0) + 1
        ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top]
        return [{"usuario_id": uid, "prestamos": cnt} for uid, cnt in ordenado]
    except Exception as e:
        log_error(f"Error usuarios que más piden: {e}")
        return []
