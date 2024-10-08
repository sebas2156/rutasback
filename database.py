from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:123456@localhost:5432/rutas'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importa los modelos para asegurarte de que se creen las tablas
from models.historial_rutas import HistorialRutas
from models.rutas import Rutas
from models.usuarios import Usuarios
