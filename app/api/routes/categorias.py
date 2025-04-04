from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.db_conection import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.services import categoria_service

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"],
)

@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva categoria.
    """
    return categoria_service.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Listar todas las categorias.
    """
    return categoria_service.get_categorias(db=db, skip=skip, limit=limit)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Obtener una categoria por su ID.
    """
    categoria = categoria_service.get_categoria(db=db, categoria_id=categoria_id)
    return categoria_service.get_categoria(db=db, categoria_id=categoria_id)

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """
    Actualizar una categoria por su ID.
    """
    return categoria_service.update_categoria(db=db, categoria_id=categoria_id, categoria=categoria)

@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una categoria por su ID.
    """
    return categoria_service.delete_categoria(db=db, categoria_id=categoria_id)