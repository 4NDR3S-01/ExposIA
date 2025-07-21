"""
Servicio de Notificaciones WebSocket para ExposIA
Desarrollado en Python para el segundo parcial
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class NotificationPayload(BaseModel):
    event: str
    payload: Dict
    timestamp: str = None
    source: str = None

class ConnectionInfo(BaseModel):
    client_id: str
    connected_at: str
    user_id: str = None
    room: str = "general"

# Gestor de conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        # Conexiones activas: {client_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Información de clientes: {client_id: ConnectionInfo}
        self.client_info: Dict[str, ConnectionInfo] = {}
        # Salas de chat: {room_name: set(client_ids)}
        self.rooms: Dict[str, Set[str]] = {"general": set()}
        # Historial de notificaciones (últimas 100)
        self.notification_history: List[Dict] = []

    async def connect(self, websocket: WebSocket, client_id: str, user_id: str = None, room: str = "general"):
        """Conectar un nuevo cliente WebSocket"""
        await websocket.accept()
        
        # Si ya existe una conexión con este client_id, cerrarla
        if client_id in self.active_connections:
            await self.disconnect(client_id)
        
        self.active_connections[client_id] = websocket
        self.client_info[client_id] = ConnectionInfo(
            client_id=client_id,
            connected_at=datetime.now().isoformat(),
            user_id=user_id,
            room=room
        )
        
        # Agregar a la sala
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(client_id)
        
        logger.info(f"Cliente {client_id} conectado a la sala {room}")
        
        # Enviar mensaje de bienvenida
        await self.send_personal_message({
            "type": "connection_established",
            "message": f"Conectado exitosamente como {client_id}",
            "room": room,
            "timestamp": datetime.now().isoformat()
        }, client_id)
        
        # Notificar a otros en la sala
        await self.broadcast_to_room({
            "type": "user_joined",
            "message": f"Usuario {client_id} se unió a la sala",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }, room, exclude_client=client_id)

    async def disconnect(self, client_id: str):
        """Desconectar un cliente"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            client_info = self.client_info.get(client_id)
            room = client_info.room if client_info else "general"
            
            # Remover de estructuras de datos
            del self.active_connections[client_id]
            if client_id in self.client_info:
                del self.client_info[client_id]
            
            # Remover de la sala
            if room in self.rooms and client_id in self.rooms[room]:
                self.rooms[room].remove(client_id)
            
            logger.info(f"Cliente {client_id} desconectado de la sala {room}")
            
            # Notificar a otros en la sala
            await self.broadcast_to_room({
                "type": "user_left",
                "message": f"Usuario {client_id} salió de la sala",
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }, room)

    async def send_personal_message(self, message: Dict, client_id: str):
        """Enviar mensaje a un cliente específico"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error enviando mensaje a {client_id}: {e}")
                await self.disconnect(client_id)

    async def broadcast_to_room(self, message: Dict, room: str, exclude_client: str = None):
        """Enviar mensaje a todos los clientes de una sala"""
        if room in self.rooms:
            clients_to_notify = self.rooms[room].copy()
            if exclude_client:
                clients_to_notify.discard(exclude_client)
            
            for client_id in clients_to_notify:
                await self.send_personal_message(message, client_id)

    async def broadcast_to_all(self, message: Dict):
        """Enviar mensaje a todos los clientes conectados"""
        for client_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, client_id)

    async def send_notification(self, notification: NotificationPayload):
        """Procesar y enviar notificación del sistema"""
        # Agregar timestamp si no existe
        if not notification.timestamp:
            notification.timestamp = datetime.now().isoformat()
        
        # Preparar mensaje
        message = {
            "type": "system_notification",
            "event": notification.event,
            "payload": notification.payload,
            "timestamp": notification.timestamp,
            "source": notification.source or "unknown"
        }
        
        # Agregar al historial
        self.notification_history.append(message)
        if len(self.notification_history) > 100:
            self.notification_history.pop(0)
        
        # Determinar a quién enviar la notificación
        await self._route_notification(message, notification)
        
        logger.info(f"Notificación procesada: {notification.event}")

    async def _route_notification(self, message: Dict, notification: NotificationPayload):
        """Enrutar notificación según el tipo de evento"""
        event = notification.event
        payload = notification.payload
        
        # Notificaciones específicas por usuario
        if event.startswith('user.') and 'usuarioId' in payload:
            user_id = str(payload['usuarioId'])
            # Buscar conexiones de este usuario
            for client_id, info in self.client_info.items():
                if info.user_id == user_id:
                    await self.send_personal_message(message, client_id)
            return
        
        # Notificaciones globales del sistema
        if event in ['presentacion.creada', 'grabacion.creada', 'calificacion.creada', 'feedback.creado']:
            await self.broadcast_to_all(message)
            return
        
        # Notificaciones por sala/tema
        if 'temaId' in payload:
            room = f"tema_{payload['temaId']}"
            await self.broadcast_to_room(message, room)
            return
        
        # Por defecto, enviar a sala general
        await self.broadcast_to_room(message, "general")

    def get_stats(self) -> Dict:
        """Obtener estadísticas del servicio"""
        return {
            "total_connections": len(self.active_connections),
            "rooms": {room: len(clients) for room, clients in self.rooms.items()},
            "clients": [
                {
                    "client_id": client_id,
                    "user_id": info.user_id,
                    "room": info.room,
                    "connected_at": info.connected_at
                }
                for client_id, info in self.client_info.items()
            ],
            "recent_notifications": self.notification_history[-10:],
            "total_notifications_sent": len(self.notification_history)
        }

# Instancia global del gestor de conexiones
manager = ConnectionManager()

# Crear aplicación FastAPI
app = FastAPI(
    title="ExposIA WebSocket Notifications",
    description="Servicio de notificaciones en tiempo real para ExposIA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de autenticación simple
def verify_token(token: str = None):
    """Verificar token de autenticación"""
    expected_token = os.getenv("WS_TOKEN", "dev")
    if token != expected_token:
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

# Endpoints REST

@app.get("/")
async def root():
    """Endpoint raíz con información del servicio"""
    return {
        "service": "ExposIA WebSocket Notifications",
        "version": "1.0.0",
        "description": "Servicio de notificaciones en tiempo real",
        "endpoints": {
            "websocket": "/ws/{client_id}",
            "notify": "POST /notify",
            "stats": "GET /stats",
            "health": "GET /health"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check del servicio"""
    return {
        "status": "healthy",
        "service": "websocket-notifications",
        "timestamp": datetime.now().isoformat(),
        "connections": len(manager.active_connections)
    }

@app.post("/notify")
async def notify_clients(notification: NotificationPayload, token: str = Depends(verify_token)):
    """Endpoint para que otros servicios envíen notificaciones"""
    try:
        await manager.send_notification(notification)
        return {
            "success": True,
            "message": "Notificación enviada exitosamente",
            "event": notification.event,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error procesando notificación: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando notificación: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Obtener estadísticas del servicio"""
    return manager.get_stats()

@app.get("/history")
async def get_notification_history():
    """Obtener historial de notificaciones"""
    return {
        "history": manager.notification_history,
        "total": len(manager.notification_history)
    }

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, user_id: str = None, room: str = "general"):
    """Endpoint principal de WebSocket"""
    await manager.connect(websocket, client_id, user_id, room)
    
    try:
        while True:
            # Escuchar mensajes del cliente
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Procesar diferentes tipos de mensajes del cliente
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }, client_id)
                
                elif message.get("type") == "join_room":
                    new_room = message.get("room", "general")
                    # Cambiar de sala
                    old_room = manager.client_info[client_id].room
                    if old_room in manager.rooms:
                        manager.rooms[old_room].discard(client_id)
                    
                    if new_room not in manager.rooms:
                        manager.rooms[new_room] = set()
                    manager.rooms[new_room].add(client_id)
                    manager.client_info[client_id].room = new_room
                    
                    await manager.send_personal_message({
                        "type": "room_changed",
                        "message": f"Te uniste a la sala {new_room}",
                        "room": new_room,
                        "timestamp": datetime.now().isoformat()
                    }, client_id)
                
                elif message.get("type") == "chat_message":
                    # Reenviar mensaje de chat a la sala
                    chat_message = {
                        "type": "chat_message",
                        "client_id": client_id,
                        "message": message.get("message", ""),
                        "room": manager.client_info[client_id].room,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast_to_room(
                        chat_message, 
                        manager.client_info[client_id].room,
                        exclude_client=client_id
                    )
                
                else:
                    # Mensaje no reconocido
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Tipo de mensaje no reconocido: {message.get('type')}",
                        "timestamp": datetime.now().isoformat()
                    }, client_id)
                    
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Formato de mensaje inválido. Debe ser JSON válido.",
                    "timestamp": datetime.now().isoformat()
                }, client_id)
                
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error en WebSocket para cliente {client_id}: {e}")
        await manager.disconnect(client_id)

# Endpoint para testing
@app.post("/test-notification")
async def send_test_notification():
    """Enviar notificación de prueba"""
    test_notification = NotificationPayload(
        event="test.notification",
        payload={
            "message": "Esta es una notificación de prueba",
            "timestamp": datetime.now().isoformat(),
            "test": True
        },
        source="test-endpoint"
    )
    
    await manager.send_notification(test_notification)
    
    return {
        "success": True,
        "message": "Notificación de prueba enviada",
        "connections": len(manager.active_connections)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 9000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )