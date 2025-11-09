# src/adapters/repositories/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Importamos la Base desde nuestro nuevo archivo centralizado.
from .base import Base 

# Creamos el "motor" que conecta SQLAlchemy con la base de datos
engine = create_engine(settings.get_db_url())

# SessionLocal es una fábrica de sesiones. Cada instancia será una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependencia de FastAPI para obtener una sesión de BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()