from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String, nullable=True)

    eventos = relationship("Evento", back_populates="categoria")