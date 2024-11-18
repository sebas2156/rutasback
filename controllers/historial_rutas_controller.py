from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.historial_rutas import HistorialRutasCreate, HistorialRutasResponse, HistorialRutas
from models.trufis import Trufi
import math
from geopy.distance import geodesic
from typing import Tuple, List

router = APIRouter()


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Función para calcular la distancia entre dos puntos usando la fórmula de Haversine
def haversine(coord1, coord2):
    R = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# Crear un nuevo historial de rutas
@router.post("/historial", response_model=HistorialRutasResponse, tags=["Historial de Rutas"])
def crear_historial(historial: HistorialRutasCreate, db: Session = Depends(get_db)):
    coordenadas = historial.camino  # Asumimos que es una lista de cadenas "lat,lng"

    total_distancia = 0.0
    for i in range(len(coordenadas) - 1):
        lat1, lon1 = map(float, coordenadas[i].split(","))
        lat2, lon2 = map(float, coordenadas[i + 1].split(","))
        total_distancia += haversine((lat1, lon1), (lat2, lon2))

    # Excluimos 'distanciakm' al crear el nuevo historial
    nuevo_historial = HistorialRutas(**{**historial.dict(), "distanciakm": total_distancia})
    print(historial)
    print(total_distancia)
    db.add(nuevo_historial)
    db.commit()
    db.refresh(nuevo_historial)
    return nuevo_historial


# Función para calcular la distancia entre dos puntos
def calcular_distancia(punto1: Tuple[float, float], punto2: Tuple[float, float]) -> float:
    return geodesic(punto1, punto2).meters



# Ruta para obtener la ruta real con la tolerancia calculada
@router.post("/ruta_con_tolerancia", response_model=HistorialRutasResponse, tags=["Ruta Real con Tolerancia"])
def calcular_ruta_con_tolerancia(historial: HistorialRutasCreate, db: Session = Depends(get_db)):
    margen_tolerancia = 10
    # Verificar si el medio_usado existe en los nombres de los trufis
    trufi = db.query(Trufi).filter(Trufi.nombre == historial.medio_usado).first()
    if not trufi:
        coordenadas = historial.camino  # Asumimos que es una lista de cadenas "lat,lng"

        total_distancia = 0.0
        for i in range(len(coordenadas) - 1):
            lat1, lon1 = map(float, coordenadas[i].split(","))
            lat2, lon2 = map(float, coordenadas[i + 1].split(","))
            total_distancia += haversine((lat1, lon1), (lat2, lon2))

        # Excluimos 'distanciakm' al crear el nuevo historial
        nuevo_historial = HistorialRutas(**{**historial.dict(), "distanciakm": total_distancia})
        print(historial)
        print(total_distancia)
        db.add(nuevo_historial)
        db.commit()
        db.refresh(nuevo_historial)
        return nuevo_historial

    # Obtener las rutas de la base de datos
    ruta_ideal = trufi.ruta
    ruta_real = historial.camino

    if not ruta_ideal or not ruta_real:
        return []  # Si no se encuentran rutas, retornar lista vacía

    # Lista para almacenar las coordenadas con el valor de tolerancia
    ruta_real_con_tolerancia = []

    # Procesar cada punto de la ruta real
    total_distancia = 0.0
    for i in range(len(ruta_real) - 1):
        lat, lon = map(float, ruta_real[i].split(","))
        lat2, lon2 = map(float, ruta_real[i + 1].split(","))
        # Encontrar la distancia mínima a cualquier punto de la ruta ideal
        distancias = [calcular_distancia((lat, lon), punto_ideal) for punto_ideal in ruta_ideal]
        distancia_minima = min(distancias)

        # Determinar si está dentro o fuera del margen de tolerancia
        dentro_tolerancia = 0 if distancia_minima <= margen_tolerancia else 1

        # Agregar el punto con su valor de tolerancia
        total_distancia += haversine((lat, lon), (lat2, lon2))
        ruta_real_con_tolerancia.append(
            f"{lat}, {lon}, {dentro_tolerancia}")
    historial.camino = ruta_real_con_tolerancia
    db_historial = HistorialRutas(**{**historial.dict(), "distanciakm": total_distancia})

    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    # Devolver la ruta con el tercer valor indicando dentro o fuera del margen de tolerancia
    return db_historial


# Listar todos los historiales de rutas
@router.get("/historial", response_model=list[HistorialRutasResponse], tags=["Historial de Rutas"])
def listar_historial(db: Session = Depends(get_db)):
    historiales = db.query(HistorialRutas).all()
    return historiales


# Obtener un historial de rutas por ID
@router.get("/historial/{historial_id}", response_model=HistorialRutasResponse, tags=["Historial de Rutas"])
def obtener_historial(historial_id: int, db: Session = Depends(get_db)):
    historial = db.query(HistorialRutas).filter(HistorialRutas.id == historial_id).first()
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial


# Editar un historial de rutas
@router.put("/historial/{historial_id}", response_model=HistorialRutasResponse, tags=["Historial de Rutas"])
def editar_historial(historial_id: int, historial: HistorialRutasCreate, db: Session = Depends(get_db)):
    historial_db = db.query(HistorialRutas).filter(HistorialRutas.id == historial_id).first()
    if not historial_db:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    for key, value in historial.dict().items():
        setattr(historial_db, key, value)

    db.commit()
    db.refresh(historial_db)
    return historial_db


# Eliminar un historial de rutas
@router.delete("/historial/{historial_id}", tags=["Historial de Rutas"])
def eliminar_historial(historial_id: int, db: Session = Depends(get_db)):
    historial_db = db.query(HistorialRutas).filter(HistorialRutas.id == historial_id).first()
    if not historial_db:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    db.delete(historial_db)
    db.commit()
    return {"detail": "Historial eliminado"}
