from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db_conection import get_db
from app.services.notificaciones_service import enviar_notificaciones
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(
    prefix="/notificaciones",
    tags=["notificaciones"]
)

class NotificacionRequest(BaseModel):
    email: EmailStr
    dias: Optional[int] = 1
    evento_id: Optional[int] = None

@router.post("/eventos/proximos")
def notificar_eventos_proximos(
    request: NotificacionRequest,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    background_tasks.add_task(enviar_notificaciones, request, db)
    
    return {
        "mensaje": f"Se ha programado la notificación para los eventos próximos a {request.email}."
    }
