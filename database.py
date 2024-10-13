from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://ruatas_back_user:HapjBbI6jGWqvkTB1xaAu0EjKkAAnakR@dpg-cs64kgqj1k6c739vv6v0-a.oregon-postgres.render.com:5432/ruatas_back'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importa los modelos para asegurarte de que se creen las tablas
from models.historial_rutas import HistorialRutas
from models.rutas import Rutas
from models.usuarios import Usuarios
