import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.connection import Base, get_db
from src.main import app

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_tipo_metrica():
    response = client.post(
        "/api/v1/tipos-metrica/",
        json={"nombre": "Audio", "descripcion": "Métricas relacionadas con audio"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Audio"
    assert "id" in data

def test_get_tipos_metrica():
    client.post(
        "/api/v1/tipos-metrica/",
        json={"nombre": "Video", "descripcion": "Métricas relacionadas con video"},
    )
    response = client.get("/api/v1/tipos-metrica/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_create_metrica():
    # Primero creamos un tipo de métrica
    tipo_response = client.post(
        "/api/v1/tipos-metrica/",
        json={"nombre": "Calidad", "descripcion": "Métricas de calidad"},
    )
    tipo_id = tipo_response.json()["id"]
    
    # Luego creamos una métrica asociada a ese tipo
    response = client.post(
        "/api/v1/metricas/",
        json={
            "nombre": "Claridad", 
            "descripcion": "Claridad del sonido", 
            "tipo_metrica_id": tipo_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Claridad"
    assert data["tipo_metrica_id"] == tipo_id

def test_create_grabacion():
    response = client.post(
        "/api/v1/grabaciones/",
        json={
            "nombre_archivo": "grabacion1.mp3",
            "ruta_archivo": "/storage/audios/grabacion1.mp3",
            "duracion": 120.5,
            "formato": "mp3"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_archivo"] == "grabacion1.mp3"
    assert "id" in data

def test_create_parametro_and_feedback():
    # Crear tipo de métrica
    tipo_response = client.post(
        "/api/v1/tipos-metrica/",
        json={"nombre": "Sonido", "descripcion": "Métricas de sonido"},
    )
    tipo_id = tipo_response.json()["id"]
    
    # Crear métrica
    metrica_response = client.post(
        "/api/v1/metricas/",
        json={
            "nombre": "Volumen", 
            "descripcion": "Nivel de volumen", 
            "tipo_metrica_id": tipo_id
        },
    )
    metrica_id = metrica_response.json()["id"]
    
    # Crear parámetro
    parametro_response = client.post(
        "/api/v1/parametros/",
        json={
            "nombre": "Nivel de dB",
            "valor": 60.0,
            "unidad": "dB",
            "metrica_id": metrica_id
        },
    )
    assert parametro_response.status_code == 201
    parametro_id = parametro_response.json()["id"]
    
    # Crear grabación
    grabacion_response = client.post(
        "/api/v1/grabaciones/",
        json={
            "nombre_archivo": "test.wav",
            "ruta_archivo": "/storage/audios/test.wav",
            "duracion": 45.2,
            "formato": "wav"
        },
    )
    grabacion_id = grabacion_response.json()["id"]
    
    # Crear feedback
    feedback_response = client.post(
        "/api/v1/feedbacks/",
        json={
            "grabacion_id": grabacion_id,
            "parametro_id": parametro_id,
            "valor": 58.7,
            "comentario": "Volumen ligeramente bajo",
            "es_manual": True
        },
    )
    assert feedback_response.status_code == 201
    data = feedback_response.json()
    assert data["grabacion_id"] == grabacion_id
    assert data["parametro_id"] == parametro_id
    assert abs(data["valor"] - 58.7) < 1e-6