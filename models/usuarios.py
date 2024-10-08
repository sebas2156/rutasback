from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, Sequence('usuarios_id_seq'), primary_key=True)
    nombre = Column(String, nullable=False)
    contraseña = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    fecha_creacion = Column(String, nullable=False)


# Modelos de Pydantic
class UsuariosBase(BaseModel):
    nombre: str
    contraseña: str
    correo: str
    fecha_creacion: str


class UsuariosCreate(UsuariosBase):
    pass


class UsuariosResponse(UsuariosBase):
    id: int

    class Config:
        from_attributes = True
