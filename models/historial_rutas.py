from sqlalchemy import Column, Integer, Float, String, Sequence
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class HistorialRutas(Base):
    __tablename__ = 'historial_rutas'

    id = Column(Integer, Sequence('historial_rutas_id_seq'), primary_key=True)
    id_ruta = Column(Integer, nullable=False)
    id_usuario = Column(Integer, nullable=False)
    hora_inicio = Column(String, nullable=False)
    hora_fin = Column(String, nullable=False)
    distanciakm = Column(Float, nullable=False)
    camino = Column(ARRAY(String), nullable=False)  # Cambiado a ARRAY(String)
    medio_usado = Column(String, nullable=False)

# Modelos de Pydantic
class HistorialRutasBase(BaseModel):
    id_ruta: int
    id_usuario: int
    hora_inicio: str
    hora_fin: str
    distanciakm: float
    camino: list[str]  # Cambiado a list[str]
    medio_usado: str

class HistorialRutasCreate(HistorialRutasBase):
    pass

class HistorialRutasResponse(HistorialRutasBase):
    id: int

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes
