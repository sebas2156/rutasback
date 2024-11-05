# app/routers/trufi_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.trufis import TrufiCreate, TrufiResponse, Trufi  # Importa el modelo y esquemas

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo trufi
@router.post("/trufi", response_model=TrufiResponse, tags=["Trufis"])
def crear_trufi(trufi: TrufiCreate, db: Session = Depends(get_db)):
    nuevo_trufi = Trufi(**trufi.dict())
    db.add(nuevo_trufi)
    db.commit()
    db.refresh(nuevo_trufi)
    return nuevo_trufi

# Listar todos los trufis
@router.get("/trufi", response_model=list[TrufiResponse], tags=["Trufis"])
def listar_trufis(db: Session = Depends(get_db)):
    trufis = db.query(Trufi).all()
    return trufis

# Obtener un trufi por su ID
@router.get("/trufi/{trufi_id}", response_model=TrufiResponse, tags=["Trufis"])
def obtener_trufi(trufi_id: int, db: Session = Depends(get_db)):
    trufi = db.query(Trufi).filter(Trufi.id == trufi_id).first()
    if not trufi:
        raise HTTPException(status_code=404, detail="Trufi no encontrado")
    return trufi

# Editar un trufi existente
@router.put("/trufi/{trufi_id}", response_model=TrufiResponse, tags=["Trufis"])
def editar_trufi(trufi_id: int, trufi: TrufiCreate, db: Session = Depends(get_db)):
    trufi_db = db.query(Trufi).filter(Trufi.id == trufi_id).first()
    if not trufi_db:
        raise HTTPException(status_code=404, detail="Trufi no encontrado")

    # Actualizamos los campos con los datos proporcionados
    for key, value in trufi.dict().items():
        setattr(trufi_db, key, value)

    db.commit()
    db.refresh(trufi_db)
    return trufi_db

# Eliminar un trufi por su ID
@router.delete("/trufi/{trufi_id}", tags=["Trufis"])
def eliminar_trufi(trufi_id: int, db: Session = Depends(get_db)):
    trufi_db = db.query(Trufi).filter(Trufi.id == trufi_id).first()
    if not trufi_db:
        raise HTTPException(status_code=404, detail="Trufi no encontrado")

    db.delete(trufi_db)
    db.commit()
    return {"detail": "Trufi eliminado"}
