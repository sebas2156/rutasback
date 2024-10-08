from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.rutas import RutasCreate, RutasResponse
from models.rutas import Rutas  # Importa el modelo SQLAlchemy

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rutas", response_model=RutasResponse, tags=["Rutas"])
def crear_ruta(ruta: RutasCreate, db: Session = Depends(get_db)):
    nueva_ruta = Rutas(**ruta.dict())
    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)
    return nueva_ruta

@router.get("/rutas", response_model=list[RutasResponse], tags=["Rutas"])
def listar_rutas(db: Session = Depends(get_db)):
    rutas = db.query(Rutas).all()
    return rutas

@router.get("/rutas/{ruta_id}", response_model=RutasResponse, tags=["Rutas"])
def obtener_ruta(ruta_id: int, db: Session = Depends(get_db)):
    ruta = db.query(Rutas).filter(Rutas.id == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return ruta


@router.put("/rutas/{ruta_id}", response_model=RutasResponse, tags=["Rutas"])
def editar_ruta(ruta_id: int, ruta: RutasCreate, db: Session = Depends(get_db)):
    ruta_db = db.query(Rutas).filter(Rutas.id == ruta_id).first()
    if not ruta_db:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    for key, value in ruta.dict().items():
        setattr(ruta_db, key, value)

    db.commit()
    db.refresh(ruta_db)
    return ruta_db


@router.delete("/rutas/{ruta_id}", tags=["Rutas"])
def eliminar_ruta(ruta_id: int, db: Session = Depends(get_db)):
    ruta_db = db.query(Rutas).filter(Rutas.id == ruta_id).first()
    if not ruta_db:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    db.delete(ruta_db)
    db.commit()
    return {"detail": "Ruta eliminada"}