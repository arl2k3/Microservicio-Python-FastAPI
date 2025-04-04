from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.dependencies.db_conection import get_db
from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse
from app.services import evento_service

router = APIRouter(
    prefix="/eventos",
    tags=["eventos"],
)

@router.post("/", response_model=EventoResponse)
def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo evento.
    """
    return evento_service.create_evento(db=db, evento=evento)

@router.get("/", response_model=List[EventoResponse])
def listar_eventos(
    skip: int = 0,
    limit: int = 10,
    categoria_id: int = None,
    fecha_inicio: datetime = None,
    fecha_fin: datetime = None,
    db: Session = Depends(get_db)
):
    """
    Listar todos los eventos.
    """
    eventos = evento_service.get_eventos(
        db=db,
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    return eventos

@router.get("/{evento_id}", response_model=EventoResponse)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    """
    Obtener un evento por su ID.
    """
    return evento_service.get_evento(db=db, evento_id=evento_id)

@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(evento_id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
    """
    Actualizar un evento por su ID.
    """
    return evento_service.update_evento(db=db, evento_id=evento_id, evento=evento)

@router.delete("/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un evento por su ID.
    """
    return evento_service.delete_evento(db=db, evento_id=evento_id)