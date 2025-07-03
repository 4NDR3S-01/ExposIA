# filepath: /tests/test_auth_integration.py
"""
Pruebas de integración para autenticación y endpoints protegidos.
"""
import pytest
import os
import sys

# Añadir el directorio src al path
sys.path.insert(0, '/home/andres/Documentos/ExposIA/backend/feedback-ia-python/src')

# Configurar variables de entorno para pruebas
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["DEBUG"] = "true"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.database.connection import Base, get_db
from main_updated import app

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override de la función get_db para usar la BD de prueba."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAuthentication:
    """Pruebas del sistema de autenticación."""
    
    def test_health_endpoint_no_auth_required(self):
        """El endpoint de salud no requiere autenticación."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint_no_auth_required(self):
        """El endpoint raíz no requiere autenticación."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Feedback IA Python Service" in response.json()["message"]
    
    def test_info_endpoint_no_auth_required(self):
        """El endpoint de información no requiere autenticación."""
        response = client.get("/info")
        assert response.status_code == 200
        assert response.json()["service_name"] == "feedback-ia-python"
    
    def test_protected_endpoint_without_token(self):
        """Endpoint protegido sin token debe retornar 401."""
        response = client.post("/api/v1/feedbacks/", json={
            "grabacion_id": 1,
            "parametro_id": 1,
            "score_value": 85.0,
            "comentario": "Test feedback",
            "es_manual": True
        })
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]
    
    def test_protected_endpoint_with_invalid_token(self):
        """Endpoint protegido con token inválido debe retornar 401."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.post("/api/v1/feedbacks/", json={
            "grabacion_id": 1,
            "parametro_id": 1,
            "score_value": 85.0,
            "comentario": "Test feedback",
            "es_manual": True
        }, headers=headers)
        assert response.status_code == 401
        assert "Token inválido" in response.json()["detail"]
    
    def test_protected_endpoint_with_malformed_token(self):
        """Endpoint protegido con token mal formateado debe retornar 401."""
        headers = {"Authorization": "InvalidFormat token"}
        response = client.post("/api/v1/feedbacks/", json={
            "grabacion_id": 1,
            "parametro_id": 1,
            "score_value": 85.0,
            "comentario": "Test feedback",
            "es_manual": True
        }, headers=headers)
        assert response.status_code == 401
        assert "Formato de token inválido" in response.json()["detail"]
    
    def test_protected_endpoint_with_valid_token(self):
        """Endpoint protegido con token válido debe funcionar."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        response = client.post("/api/v1/feedbacks/", json={
            "grabacion_id": 1,
            "parametro_id": 1,
            "score_value": 85.0,
            "comentario": "Test feedback",
            "es_manual": True
        }, headers=headers)
        # Puede retornar 201 (creado) o error de validación de negocio, pero no 401
        assert response.status_code != 401
    
    def test_debug_mode_accepts_test_tokens(self):
        """En modo debug, debe aceptar tokens que empiecen con 'test-'."""
        headers = {"Authorization": "Bearer test-debug-token-123"}
        response = client.get("/api/v1/feedbacks/", headers=headers)
        # Debe aceptar el token (no retornar 401)
        assert response.status_code != 401


class TestSecurityHeaders:
    """Pruebas de headers de seguridad."""
    
    def test_security_headers_present(self):
        """Verificar que los headers de seguridad estén presentes."""
        response = client.get("/health")
        
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        
        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"
        
        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-XSS-Protection"] == "1; mode=block"


class TestErrorHandling:
    """Pruebas del manejo de errores."""
    
    def test_404_error_format(self):
        """Verificar formato de error 404."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        json_response = response.json()
        assert "detail" in json_response
        assert "error_type" in json_response
        assert "path" in json_response
        assert "method" in json_response
    
    def test_validation_error_format(self):
        """Verificar formato de errores de validación."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        response = client.post("/api/v1/feedbacks/", json={
            "invalid_field": "invalid_value"
        }, headers=headers)
        
        # Debe ser error de validación (422)
        assert response.status_code == 422
        
        json_response = response.json()
        assert "detail" in json_response
        assert "error_type" in json_response
        assert "errors" in json_response
        assert json_response["error_type"] == "ValidationError"


class TestEndpointAccess:
    """Pruebas de acceso a endpoints específicos."""
    
    def test_feedback_endpoints_require_auth(self):
        """Todos los endpoints de feedback deben requerir autenticación."""
        endpoints_to_test = [
            ("GET", "/api/v1/feedbacks/"),
            ("POST", "/api/v1/feedbacks/"),
            ("GET", "/api/v1/feedbacks/1"),
            ("PUT", "/api/v1/feedbacks/1"),
            ("DELETE", "/api/v1/feedbacks/1"),
        ]
        
        for method, endpoint in endpoints_to_test:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            elif method == "PUT":
                response = client.put(endpoint, json={})
            elif method == "DELETE":
                response = client.delete(endpoint)
            
            # Todos deben retornar 401 sin autenticación
            assert response.status_code == 401, f"Endpoint {method} {endpoint} no requiere auth"
    
    def test_feedback_endpoints_work_with_auth(self):
        """Los endpoints de feedback deben funcionar con autenticación válida."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        
        # Test GET feedbacks (debe funcionar)
        response = client.get("/api/v1/feedbacks/", headers=headers)
        assert response.status_code in [200, 404], "GET feedbacks debe funcionar con auth"
        
        # Test POST feedback (puede fallar por validación de negocio, pero no por auth)
        response = client.post("/api/v1/feedbacks/", json={
            "grabacion_id": 1,
            "parametro_id": 1,
            "score_value": 85.0,
            "comentario": "Test feedback",
            "es_manual": True
        }, headers=headers)
        assert response.status_code != 401, "POST feedback no debe fallar por auth"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
