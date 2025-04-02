from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    ubicacion = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    notificacion_enviada = Column(Boolean, default=False)

    categoria = relationship("Categoria", back_populates="eventos")