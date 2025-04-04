import smtplib
from email.message import EmailMessage
from app.core.config import settings
from app.models.evento import Evento
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from typing import Optional

class NotificacionRequest(BaseModel):
    email: EmailStr
    evento_id: Optional[int] = None
    dias: Optional[int] = None

def enviar_notificaciones(request: NotificacionRequest, db: Session):
    try:
        eventos = []
        
        if request.evento_id:
            evento = db.query(Evento).filter(Evento.id == request.evento_id).first()
            if not evento:
                return {"message": "Evento no encontrado", "status": "not_found"}
            eventos.append(evento)
        elif request.dias:
            fecha_limite = datetime.now() + timedelta(days=request.dias)
            eventos = db.query(Evento).filter(
                Evento.fecha_inicio <= fecha_limite,
                Evento.fecha_inicio >= datetime.now(),
                Evento.notificacion_enviada == False
            ).all()

            if not eventos:
                return {"message": "No hay eventos próximos", "status": "no_events"}

        if not request.evento_id and not request.dias:
            return {"message": "Debe especificar evento_id o días", "status": "bad_request"}

        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD

        for evento in eventos:
            msg = EmailMessage()
            msg.set_content(f"Recordatorio para el evento: {evento.titulo}\n"
                            f"Fecha: {evento.fecha_inicio}\n"
                            f"Ubicación: {evento.ubicacion or 'No especificada'}")

            msg["Subject"] = f"Recordatorio: {evento.titulo}"
            msg["From"] = smtp_username
            msg["To"] = request.email

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            evento.notificacion_enviada = True

        return {"message": "Notificaciones enviadas exitosamente.", "status": "success"}

    except Exception as e:
        db.rollback()
        return {"message": f"Error al enviar notificaciones: {str(e)}", "status": "error"}
