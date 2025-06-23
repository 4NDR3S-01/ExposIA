# filepath: /tests/test_auth_simple.py
"""
Pruebas simplificadas de autenticación.
"""
import pytest
import os
import sys

# Configurar variables de entorno
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["DEBUG"] = "true"

# Añadir el directorio src al path
sys.path.insert(0, '/home/andres/Documentos/ExposIA/backend/feedback-ia-python/src')

from fastapi.testclient import TestClient
from test_app_simple import app

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
        response = client.get("/api/v1/feedbacks/")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token(self):
        """Endpoint protegido con token inválido debe retornar 401."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/feedbacks/", headers=headers)
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token(self):
        """Endpoint protegido con token válido debe funcionar."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        response = client.get("/api/v1/feedbacks/", headers=headers)
        assert response.status_code == 200
        assert "feedbacks" in response.json()
    
    def test_debug_mode_accepts_test_tokens(self):
        """En modo debug, debe aceptar tokens que empiecen con 'test-'."""
        headers = {"Authorization": "Bearer test-debug-token-123"}
        response = client.get("/api/v1/feedbacks/", headers=headers)
        assert response.status_code == 200
    
    def test_post_endpoint_with_auth(self):
        """Endpoint POST protegido debe funcionar con autenticación."""
        headers = {"Authorization": "Bearer test-api-key-12345"}
        data = {"test": "data"}
        response = client.post("/api/v1/feedbacks/", json=data, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Feedback created"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
