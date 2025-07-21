"""
Tests para el servicio de WebSocket
"""
import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from fastapi import WebSocket
import websockets
from main import app, manager

client = TestClient(app)

class TestWebSocketService:
    
    def test_health_endpoint(self):
        """Test del endpoint de salud"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "connections" in data

    def test_root_endpoint(self):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "ExposIA WebSocket Notifications"
        assert "endpoints" in data

    def test_stats_endpoint(self):
        """Test del endpoint de estadísticas"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_connections" in data
        assert "rooms" in data
        assert "clients" in data

    def test_notify_endpoint_without_token(self):
        """Test del endpoint notify sin token"""
        notification_data = {
            "event": "test.event",
            "payload": {"message": "test"}
        }
        response = client.post("/notify", json=notification_data)
        assert response.status_code == 401

    def test_notify_endpoint_with_token(self):
        """Test del endpoint notify con token válido"""
        notification_data = {
            "event": "test.event",
            "payload": {"message": "test"}
        }
        response = client.post(
            "/notify?token=dev", 
            json=notification_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["event"] == "test.event"

    def test_test_notification_endpoint(self):
        """Test del endpoint de notificación de prueba"""
        response = client.post("/test-notification")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "connections" in data

    def test_history_endpoint(self):
        """Test del endpoint de historial"""
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert "total" in data

@pytest.mark.asyncio
class TestConnectionManager:
    
    async def test_connection_manager_stats(self):
        """Test de estadísticas del gestor de conexiones"""
        stats = manager.get_stats()
        assert "total_connections" in stats
        assert "rooms" in stats
        assert "clients" in stats
        assert "recent_notifications" in stats

    async def test_notification_routing(self):
        """Test del enrutamiento de notificaciones"""
        from main import NotificationPayload
        
        # Test notificación global
        notification = NotificationPayload(
            event="presentacion.creada",
            payload={"id": 1, "titulo": "Test Presentation"}
        )
        
        # Esto debería ejecutarse sin errores
        await manager.send_notification(notification)
        
        # Verificar que se agregó al historial
        assert len(manager.notification_history) > 0
        last_notification = manager.notification_history[-1]
        assert last_notification["event"] == "presentacion.creada"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])