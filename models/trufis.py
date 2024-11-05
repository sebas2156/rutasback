# app/models/trufi.py
from sqlalchemy import Column, Integer, String, Float, Sequence, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
import datetime

Base = declarative_base()

class Trufi(Base):
    __tablename__ = 'trufis'

    id = Column(Integer, Sequence('trufis_id_seq'), primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    ruta = Column(ARRAY(String), nullable=False)  # Lista de coordenadas lat,lng
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Esquema base para la ruta del trufi
class TrufiBase(BaseModel):
    nombre: str
    descripcion: str
    ruta: List[str]  # Lista de coordenadas como strings en el formato 'lat,lng'
    created_at: datetime.datetime

# Esquema para la creación de un nuevo trufi
class TrufiCreate(TrufiBase):
    pass

# Esquema de respuesta para mostrar un trufi (incluyendo el ID)
class TrufiResponse(TrufiBase):
    id: int

    class Config:
        orm_mode = True  # Permite la conversión de objetos SQLAlchemy a Pydantic (necesario para FastAPI)

