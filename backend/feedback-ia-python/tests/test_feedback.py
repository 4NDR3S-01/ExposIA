import pytest
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

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

# Crear las tablas de prueba
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override de la función get_db para usar la BD de prueba."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Configurar variables de entorno para pruebas
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["DEBUG"] = "true"

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAuthentication:
    """Tests de autenticación."""
    
    def test_health_endpoint_no_auth_required(self):
        """El endpoint de salud no requiere autenticación."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint_no_auth_required(self):
        """El endpoint raíz no requiere autenticación."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_protected_endpoint_without_token(self):
        """Los endpoints protegidos requieren token."""
        response = client.get("/api/v1/tipos-metrica/")
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]
    
    def test_protected_endpoint_with_invalid_token(self):
        """Token inválido debe retornar 401."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/tipos-metrica/", headers=headers)
        assert response.status_code == 401
        assert "Token inválido" in response.json()["detail"]
    
    def test_protected_endpoint_with_valid_token(self):
        """Token válido debe permitir acceso."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        response = client.get("/api/v1/tipos-metrica/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestTipoMetrica:
    """Tests para TipoMetrica con autenticación."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def test_create_tipo_metrica(self):
        """Test crear tipo de métrica."""
        data = {
            "nombre": "Velocidad",
            "descripcion": "Métrica de velocidad de habla"
        }
        response = client.post("/api/v1/tipos-metrica/", json=data, headers=self.auth_headers)
        assert response.status_code == 201
        assert response.json()["nombre"] == "Velocidad"
        assert "id" in response.json()
    
    def test_get_tipos_metrica(self):
        """Test obtener tipos de métrica."""
        response = client.get("/api/v1/tipos-metrica/", headers=self.auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_tipo_metrica_by_id(self):
        """Test obtener tipo de métrica por ID."""
        # Primero crear uno
        data = {"nombre": "Tono", "descripcion": "Métrica de tono"}
        create_response = client.post("/api/v1/tipos-metrica/", json=data, headers=self.auth_headers)
        created_id = create_response.json()["id"]
        
        # Luego obtenerlo
        response = client.get(f"/api/v1/tipos-metrica/{created_id}", headers=self.auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == created_id
        assert response.json()["nombre"] == "Tono"
    
    def test_get_tipo_metrica_not_found(self):
        """Test tipo de métrica no encontrado."""
        response = client.get("/api/v1/tipos-metrica/9999", headers=self.auth_headers)
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]


class TestMetrica:
    """Tests para Metrica con autenticación."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def setup_method(self):
        """Setup para cada test - crear tipo de métrica."""
        data = {"nombre": "Test Tipo", "descripcion": "Para pruebas"}
        response = client.post("/api/v1/tipos-metrica/", json=data, headers=self.auth_headers)
        self.tipo_metrica_id = response.json()["id"]
    
    def test_create_metrica(self):
        """Test crear métrica."""
        data = {
            "nombre": "Palabras por minuto",
            "descripcion": "Velocidad de habla en palabras por minuto",
            "tipo_metrica_id": self.tipo_metrica_id
        }
        response = client.post("/api/v1/metricas/", json=data, headers=self.auth_headers)
        assert response.status_code == 201
        assert response.json()["nombre"] == "Palabras por minuto"
        assert response.json()["tipo_metrica_id"] == self.tipo_metrica_id
    
    def test_get_metricas(self):
        """Test obtener métricas."""
        response = client.get("/api/v1/metricas/", headers=self.auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestParametro:
    """Tests para Parametro con autenticación."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def setup_method(self):
        """Setup para cada test."""
        # Crear tipo de métrica
        tipo_data = {"nombre": "Test Tipo Param", "descripcion": "Para pruebas param"}
        tipo_response = client.post("/api/v1/tipos-metrica/", json=tipo_data, headers=self.auth_headers)
        self.tipo_metrica_id = tipo_response.json()["id"]
        
        # Crear métrica
        metrica_data = {
            "nombre": "Test Metrica",
            "descripcion": "Para pruebas",
            "tipo_metrica_id": self.tipo_metrica_id
        }
        metrica_response = client.post("/api/v1/metricas/", json=metrica_data, headers=self.auth_headers)
        self.metrica_id = metrica_response.json()["id"]
    
    def test_create_parametro(self):
        """Test crear parámetro."""
        data = {
            "nombre": "Velocidad ideal",
            "valor": 150.0,
            "unidad": "palabras/min",
            "metrica_id": self.metrica_id
        }
        response = client.post("/api/v1/parametros/", json=data, headers=self.auth_headers)
        assert response.status_code == 201
        assert response.json()["nombre"] == "Velocidad ideal"
        assert response.json()["valor"] == 150.0
        assert response.json()["metrica_id"] == self.metrica_id


class TestGrabacion:
    """Tests para Grabacion con autenticación."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def test_create_grabacion(self):
        """Test crear grabación."""
        data = {
            "nombre_archivo": "test_audio.mp3",
            "ruta_archivo": "/uploads/test_audio.mp3",
            "duracion": 120.5,
            "formato": "mp3"
        }
        response = client.post("/api/v1/grabaciones/", json=data, headers=self.auth_headers)
        assert response.status_code == 201
        assert response.json()["nombre_archivo"] == "test_audio.mp3"
        assert response.json()["duracion"] == 120.5


class TestFeedback:
    """Tests para Feedback con autenticación."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def setup_method(self):
        """Setup completo para feedback."""
        # Crear grabación
        grabacion_data = {
            "nombre_archivo": "feedback_test.mp3",
            "ruta_archivo": "/uploads/feedback_test.mp3",
            "duracion": 60.0,
            "formato": "mp3"
        }
        grabacion_response = client.post("/api/v1/grabaciones/", json=grabacion_data, headers=self.auth_headers)
        self.grabacion_id = grabacion_response.json()["id"]
        
        # Crear tipo, métrica y parámetro
        tipo_data = {"nombre": "Feedback Tipo", "descripcion": "Para feedback"}
        tipo_response = client.post("/api/v1/tipos-metrica/", json=tipo_data, headers=self.auth_headers)
        tipo_id = tipo_response.json()["id"]
        
        metrica_data = {"nombre": "Feedback Metrica", "tipo_metrica_id": tipo_id}
        metrica_response = client.post("/api/v1/metricas/", json=metrica_data, headers=self.auth_headers)
        metrica_id = metrica_response.json()["id"]
        
        parametro_data = {"nombre": "Feedback Param", "valor": 100.0, "metrica_id": metrica_id}
        parametro_response = client.post("/api/v1/parametros/", json=parametro_data, headers=self.auth_headers)
        self.parametro_id = parametro_response.json()["id"]
    
    def test_create_feedback(self):
        """Test crear feedback."""
        data = {
            "grabacion_id": self.grabacion_id,
            "parametro_id": self.parametro_id,
            "valor": 85.0,
            "comentario": "Buen rendimiento",
            "es_manual": True
        }
        response = client.post("/api/v1/feedbacks/", json=data, headers=self.auth_headers)
        assert response.status_code == 201
        assert response.json()["valor"] == 85.0
        assert response.json()["grabacion_id"] == self.grabacion_id
        assert response.json()["parametro_id"] == self.parametro_id
    
    def test_get_feedbacks_by_grabacion(self):
        """Test obtener feedbacks por grabación."""
        # Crear feedback primero
        data = {
            "grabacion_id": self.grabacion_id,
            "parametro_id": self.parametro_id,
            "valor": 90.0,
            "es_manual": False
        }
        client.post("/api/v1/feedbacks/", json=data, headers=self.auth_headers)
        
        # Obtener feedbacks de la grabación
        response = client.get(f"/api/v1/feedbacks/grabacion/{self.grabacion_id}", headers=self.auth_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1
        assert response.json()[0]["grabacion_id"] == self.grabacion_id


class TestIntegrationFlow:
    """Tests de flujo completo de integración."""
    
    @property
    def auth_headers(self):
        return {"Authorization": "Bearer test-api-key-12345"}
    
    def test_complete_flow(self):
        """Test del flujo completo de creación."""
        # 1. Crear tipo de métrica
        tipo_data = {"nombre": "Flow Tipo", "descripcion": "Test completo"}
        tipo_response = client.post("/api/v1/tipos-metrica/", json=tipo_data, headers=self.auth_headers)
        assert tipo_response.status_code == 201
        tipo_id = tipo_response.json()["id"]
        
        # 2. Crear métrica
        metrica_data = {"nombre": "Flow Metrica", "tipo_metrica_id": tipo_id}
        metrica_response = client.post("/api/v1/metricas/", json=metrica_data, headers=self.auth_headers)
        assert metrica_response.status_code == 201
        metrica_id = metrica_response.json()["id"]
        
        # 3. Crear parámetro
        param_data = {"nombre": "Flow Param", "valor": 120.0, "metrica_id": metrica_id}
        param_response = client.post("/api/v1/parametros/", json=param_data, headers=self.auth_headers)
        assert param_response.status_code == 201
        param_id = param_response.json()["id"]
        
        # 4. Crear grabación
        grab_data = {"nombre_archivo": "flow.mp3", "ruta_archivo": "/flow.mp3"}
        grab_response = client.post("/api/v1/grabaciones/", json=grab_data, headers=self.auth_headers)
        assert grab_response.status_code == 201
        grab_id = grab_response.json()["id"]
        
        # 5. Crear feedback
        feedback_data = {
            "grabacion_id": grab_id,
            "parametro_id": param_id,
            "valor": 88.5,
            "comentario": "Excelente flujo completo"
        }
        feedback_response = client.post("/api/v1/feedbacks/", json=feedback_data, headers=self.auth_headers)
        assert feedback_response.status_code == 201
        assert feedback_response.json()["comentario"] == "Excelente flujo completo"
        
        # 6. Verificar relaciones
        feedbacks_by_grab = client.get(f"/api/v1/feedbacks/grabacion/{grab_id}", headers=self.auth_headers)
        assert feedbacks_by_grab.status_code == 200
        assert len(feedbacks_by_grab.json()) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

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