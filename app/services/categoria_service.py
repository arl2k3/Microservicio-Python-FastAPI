from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate
from fastapi import HTTPException

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Categoria).offset(skip).limit(limit).all()

def get_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if db_categoria:
        raise HTTPException(status_code=400, detail="Esta categoria ya existe")
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria: CategoriaCreate):
    db_categoria = get_categoria(db, categoria_id)
    db_categoria.nombre = categoria.nombre
    db_categoria.descripcion = categoria.descripcion
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria(db, categoria_id)
    
    from app.models.evento import Evento
    eventos_asociados = db.query(Evento).filter(Evento.categoria_id == categoria_id).count()
    if eventos_asociados > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar la categoria porque tiene eventos asociados")
    
    db.delete(db_categoria)
    db.commit()
    return {"mensaje": "Categoria eliminada"}