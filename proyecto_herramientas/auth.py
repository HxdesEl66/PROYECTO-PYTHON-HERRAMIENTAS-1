# auth.py

from typing import Dict
from config import ROLES_VALIDOS
from logger import log_error

def validar_rol(rol: str) -> bool:
    return rol in ROLES_VALIDOS

def puede_administrar(usuario: Dict) -> bool:
    try:
        return usuario.get("tipo_usuario") == "ADMINISTRADOR"
    except Exception as e:
        log_error(f"Error validando permisos: {e}")
        return False

def puede_residente(usuario: Dict) -> bool:
    try:
        return usuario.get("tipo_usuario") == "RESIDENTE"
    except Exception as e:
        log_error(f"Error validando permisos: {e}")
        return False
