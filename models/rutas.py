from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Rutas(Base):
    __tablename__ = 'rutas'

    id = Column(Integer, Sequence('rutas_id_seq'), primary_key=True)
    id_usuario = Column(Integer, nullable=False)
    ubicacion_inicial = Column(String, nullable=False)
    ubicacion_final = Column(String, nullable=False)
    duracion_estimada_minutos = Column(Integer, default=None)
    fecha_creacion = Column(String, nullable=False)
    medio_esperado = Column(String, nullable=False)
    dias = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    hora = Column(String)


# Modelos de Pydantic
class RutasBase(BaseModel):
    id_usuario: int
    ubicacion_inicial: str
    ubicacion_final: str
    duracion_estimada_minutos: int
    fecha_creacion: str
    medio_esperado: str
    dias: str
    nombre: str
    hora: str


class RutasCreate(RutasBase):
    pass


class RutasResponse(RutasBase):
    id: int

    class Config:
        from_attributes = True
