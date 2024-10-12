from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuarios import UsuariosCreate, UsuariosResponse
from models.usuarios import Usuarios
from pydantic import BaseModel

router = APIRouter()


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear un nuevo usuario
@router.post("/usuarios", response_model=UsuariosResponse, tags=["Usuarios"])
def crear_usuario(usuario: UsuariosCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuarios(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# Listar todos los usuarios
@router.get("/usuarios", response_model=list[UsuariosResponse], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuarios).all()
    return usuarios


# Obtener un usuario por ID
@router.get("/usuarios/{usuario_id}", response_model=UsuariosResponse, tags=["Usuarios"])
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Editar un usuario
@router.put("/usuarios/{usuario_id}", response_model=UsuariosResponse, tags=["Usuarios"])
def editar_usuario(usuario_id: int, usuario: UsuariosCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in usuario.dict().items():
        setattr(usuario_db, key, value)

    db.commit()
    db.refresh(usuario_db)
    return usuario_db


# Eliminar un usuario
@router.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario_db)
    db.commit()
    return {"detail": "Usuario eliminado"}


class Credenciales(BaseModel):
    nombre: str
    contraseña: str


# Verificar nombre y contraseña
@router.post("/usuarios/validar", tags=["Usuarios"])
def validar_usuario(credenciales: Credenciales, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(
        Usuarios.nombre == credenciales.nombre,
        Usuarios.contraseña == credenciales.contraseña
    ).first()

    if usuario:
        return {"detail": "Credenciales válidas"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")