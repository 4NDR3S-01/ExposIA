# filepath: /src/infrastructure/database/connection.py
"""
Configuración de la conexión a la base de datos.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./feedback_db.sqlite")

# Crear el engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear la sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db():
    """
    Función de dependencia para obtener la sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
