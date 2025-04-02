from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventoBase(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    ubicacion: Optional[str] = None
    categoria_id: Optional[int] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    ubicacion: Optional[str] = None
    categoria_id: Optional[int] = None

    class EventoResponse(EventoBase):
        id: int
        notificacion_enviada: bool

        class Config:
            orm_mode = True
