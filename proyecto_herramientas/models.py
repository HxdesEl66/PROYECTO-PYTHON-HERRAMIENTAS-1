# models.py

from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Usuario:
    id: str
    primer_nombre: str
    primer_apellido: str
    telefono: str
    direccion: str
    tipo_usuario: str  # ADMINISTRADOR o RESIDENTE

    def to_dict(self):
        return asdict(self)

@dataclass
class Herramienta:
    id: str
    nombre: str
    categoria: str
    cantidad_disponible: int
    estado: str  # ACTIVA / INACTIVA / MANTENIMIENTO
    valor_estimado: float

    def to_dict(self):
        return asdict(self)

@dataclass
class Prestamo:
    id: str
    usuario_id: str
    herramienta_id: str
    cantidad: int
    fecha_inicio: str
    fecha_devolucion_estimada: str
    estado: str  # ACTIVO / DEVUELTO / VENCIDO
    observaciones: Optional[str] = ""

    def to_dict(self):
        return asdict(self)
