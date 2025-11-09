# src/adapters/repositories/base.py
from sqlalchemy.ext.declarative import declarative_base

# Base es una clase base para nuestros modelos ORM.
# Todos los modelos de la base de datos heredarán de esta clase.
Base = declarative_base()