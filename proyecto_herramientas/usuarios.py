# usuarios.py

from typing import Dict, List, Optional
from storage import leer_json, guardar_json
from config import USUARIOS_JSON
from models import Usuario
from logger import log_info, log_error
from auth import validar_rol

def listar_usuarios() -> List[Dict]:
    return leer_json(USUARIOS_JSON)

def buscar_usuario_por_id(usuario_id: str) -> Optional[Dict]:
    usuarios = listar_usuarios()
    for u in usuarios:
        if u["id"] == usuario_id:
            return u
    return None

def crear_usuario(data: Dict) -> bool:
    try:
        if not validar_rol(data.get("tipo_usuario", "")):
            log_error("Tipo de usuario inválido al crear usuario.")
            return False

        usuarios = listar_usuarios()
        if any(u["id"] == data["id"] for u in usuarios):
            log_error("ID de usuario ya existe.")
            return False

        usuario = Usuario(**data)
        usuarios.append(usuario.to_dict())
        ok = guardar_json(USUARIOS_JSON, usuarios)
        if ok:
            log_info(f"Usuario creado: {usuario.id}")
        return ok
    except Exception as e:
        log_error(f"Error creando usuario: {e}")
        return False

def actualizar_usuario(usuario_id: str, cambios: Dict) -> bool:
    try:
        usuarios = listar_usuarios()
        for i, u in enumerate(usuarios):
            if u["id"] == usuario_id:
                usuarios[i].update(cambios)
                ok = guardar_json(USUARIOS_JSON, usuarios)
                if ok:
                    log_info(f"Usuario actualizado: {usuario_id}")
                return ok
        log_error("Usuario no encontrado para actualizar.")
        return False
    except Exception as e:
        log_error(f"Error actualizando usuario: {e}")
        return False

def eliminar_usuario(usuario_id: str) -> bool:
    try:
        usuarios = listar_usuarios()
        nuevos = [u for u in usuarios if u["id"] != usuario_id]
        if len(nuevos) == len(usuarios):
            log_error("Usuario no encontrado para eliminar.")
            return False
        ok = guardar_json(USUARIOS_JSON, nuevos)
        if ok:
            log_info(f"Usuario eliminado: {usuario_id}")
        return ok
    except Exception as e:
        log_error(f"Error eliminando usuario: {e}")
        return False
