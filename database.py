from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://rutas_gppr_user:0V43gOHLxybEeV7wpK3RtbxVM3W0vfhR@dpg-csq0ahl2ng1s7397ptvg-a.oregon-postgres.render.com/rutas_gppr'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importa los modelos para asegurarte de que se creen las tablas
from models.historial_rutas import HistorialRutas
from models.rutas import Rutas
from models.usuarios import Usuarios
