from sqlalchemy.orm import Session
from app.models.evento import Evento
from app.models.categoria import Categoria
from app.schemas.evento import EventoCreate, EventoUpdate
from fastapi import HTTPException
from datetime import datetime

def get_eventos(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    categoria_id: int = None,
    fecha_inicio: datetime = None,
    fecha_fin: datetime = None
):
    query = db.query(Evento)
    
    if categoria_id:
        query = query.filter(Evento.categoria_id == categoria_id)
    
    if fecha_inicio:
        query = query.filter(Evento.fecha >= fecha_inicio)
    
    if fecha_fin:
        query = query.filter(Evento.fecha <= fecha_fin)
    
    return query.offset(skip).limit(limit).all()

def get_evento(db: Session, evento_id: int):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

def create_evento(db: Session, evento: EventoCreate):
    categoria = db.query(Categoria).filter(Categoria.id == evento.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoria no encontrada")
    
    nuevo_evento = Evento(**evento.dict())
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento

def update_evento(db: Session, evento_id: int, evento: EventoUpdate):
    db_evento = get_evento(db, evento_id)
    
    if evento.categoria_id:
        categoria = db.query(Categoria).filter(Categoria.id == evento.categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=400, detail="Categoria no encontrada")
    
    for key, value in evento.dict(exclude_unset=True).items():
        setattr(db_evento, key, value)
    
    db.commit()
    db.refresh(db_evento)
    return db_evento

def delete_evento(db: Session, evento_id: int):
    db_evento = get_evento(db, evento_id)
    db.delete(db_evento)
    db.commit()
    return {"mensaje": "Evento eliminado"}