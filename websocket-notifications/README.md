# 🔌 ExposIA WebSocket Notifications

Servicio de notificaciones en tiempo real desarrollado en Python para la arquitectura de microservicios de ExposIA.

## 🎯 Funcionalidades

- **WebSocket Server** para conexiones en tiempo real
- **REST API** para recibir notificaciones de microservicios
- **Gestión de salas** para organizar clientes
- **Historial de notificaciones** (últimas 100)
- **Estadísticas en tiempo real** de conexiones
- **Cliente de prueba** incluido para testing

## 🚀 Inicio Rápido

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Iniciar servidor
python src/main.py

# El servidor estará disponible en:
# WebSocket: ws://localhost:9000/ws/{client_id}
# REST API: http://localhost:9000
```

### Docker

```bash
# Construir imagen
docker build -t exposia-websocket .

# Ejecutar contenedor
docker run -p 9000:9000 exposia-websocket
```

## 📡 API Reference

### WebSocket Endpoints

#### Conectar Cliente

```javascript
// Conexión básica
const ws = new WebSocket('ws://localhost:9000/ws/client-123');

// Conexión con parámetros
const ws = new WebSocket('ws://localhost:9000/ws/client-123?user_id=456&room=general');
```

#### Mensajes del Cliente

```javascript
// Ping/Pong
ws.send(JSON.stringify({
  type: 'ping'
}));

// Mensaje de chat
ws.send(JSON.stringify({
  type: 'chat_message',
  message: 'Hola a todos!'
}));

// Cambiar de sala
ws.send(JSON.stringify({
  type: 'join_room',
  room: 'tema_1'
}));
```

#### Mensajes del Servidor

```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'connection_established':
      console.log('Conectado exitosamente');
      break;
      
    case 'system_notification':
      console.log('Notificación del sistema:', data.payload);
      break;
      
    case 'chat_message':
      console.log(`${data.client_id}: ${data.message}`);
      break;
      
    case 'user_joined':
    case 'user_left':
      console.log(data.message);
      break;
  }
};
```

### REST API Endpoints

#### Enviar Notificación

```bash
POST /notify?token=dev
Content-Type: application/json

{
  "event": "presentacion.creada",
  "payload": {
    "id": 123,
    "titulo": "Mi Presentación",
    "usuarioId": 456
  }
}
```

#### Estadísticas

```bash
GET /stats

# Respuesta:
{
  "total_connections": 5,
  "rooms": {
    "general": 3,
    "tema_1": 2
  },
  "clients": [
    {
      "client_id": "client-123",
      "user_id": "456",
      "room": "general",
      "connected_at": "2025-01-09T10:30:00"
    }
  ],
  "total_notifications_sent": 42
}
```

#### Health Check

```bash
GET /health

# Respuesta:
{
  "status": "healthy",
  "service": "websocket-notifications",
  "timestamp": "2025-01-09T10:30:00",
  "connections": 5
}
```

#### Historial de Notificaciones

```bash
GET /history

# Respuesta:
{
  "history": [
    {
      "type": "system_notification",
      "event": "presentacion.creada",
      "payload": {...},
      "timestamp": "2025-01-09T10:30:00"
    }
  ],
  "total": 15
}
```

## 🏗️ Arquitectura

### Gestor de Conexiones

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.client_info: Dict[str, ConnectionInfo] = {}
        self.rooms: Dict[str, Set[str]] = {"general": set()}
        self.notification_history: List[Dict] = []
```

### Enrutamiento de Notificaciones

Las notificaciones se enrutan automáticamente según el evento:

```python
# Notificaciones específicas por usuario
if event.startswith('user.') and 'usuarioId' in payload:
    # Enviar solo al usuario específico

# Notificaciones globales del sistema  
if event in ['presentacion.creada', 'grabacion.creada']:
    # Broadcast a todos los clientes

# Notificaciones por tema/sala
if 'temaId' in payload:
    # Enviar a sala específica del tema
```

### Tipos de Eventos Soportados

| Evento | Origen | Descripción |
|--------|--------|-------------|
| `presentacion.creada` | PHP | Nueva presentación creada |
| `presentacion.eliminada` | PHP | Presentación eliminada |
| `grabacion.creada` | TypeScript | Nueva grabación de práctica |
| `feedback.creado` | Python | Nuevo feedback de IA |
| `metrica.creada` | Python | Nueva métrica definida |
| `calificacion.creada` | Java | Nueva calificación asignada |
| `calificacion.ia.aplicada` | Java | IA aplicada a calificación |
| `user.{id}.{evento}` | Cualquiera | Notificación específica de usuario |

## 🧪 Testing

### Tests Automatizados

```bash
# Ejecutar todos los tests
python -m pytest src/test_websocket.py -v

# Tests específicos
python -m pytest src/test_websocket.py::TestWebSocketService::test_notify_endpoint_with_token -v

# Coverage
python -m pytest --cov=src src/test_websocket.py
```

### Cliente de Prueba HTML

Abrir en navegador: `src/client_test.html`

Funcionalidades del cliente:
- ✅ Conectar/desconectar WebSocket
- ✅ Enviar mensajes de chat
- ✅ Cambiar de sala
- ✅ Enviar notificaciones via REST
- ✅ Ver estadísticas en tiempo real
- ✅ Ping/pong testing

### Testing Manual

```bash
# Terminal 1: Iniciar servidor
python src/main.py

# Terminal 2: Conectar cliente WebSocket
wscat -c "ws://localhost:9000/ws/test-client"

# Terminal 3: Enviar notificación
curl -X POST "http://localhost:9000/notify?token=dev" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "test.notification",
    "payload": {"message": "Hola mundo"}
  }'
```

## 🔧 Configuración

### Variables de Entorno

```env
# Puerto del servicio
PORT=9000

# Token de autenticación
WS_TOKEN=dev

# Configuración de Redis (futuro)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Entorno
ENVIRONMENT=development
```

### Configuración de Salas

Las salas se crean automáticamente cuando los clientes se conectan:

- **general**: Sala por defecto
- **tema_{id}**: Salas por tema de presentación
- **admin**: Sala para administradores
- **user_{id}**: Salas privadas por usuario

## 🔄 Integración con Microservicios

### Desde PHP (Laravel)

```php
use Illuminate\Support\Facades\Http;

// En un controlador o servicio
private function enviarNotificacion(string $evento, array $payload): void
{
    try {
        $wsUrl = env('WS_NOTIFICATION_URL', 'http://localhost:9000');
        $token = env('WS_NOTIFICATION_TOKEN', 'dev');

        Http::timeout(5)->post("{$wsUrl}/notify", [
            'event' => $evento,
            'payload' => array_merge($payload, [
                'timestamp' => now()->toISOString(),
                'source' => 'presentaciones-php'
            ])
        ], [
            'token' => $token
        ]);
    } catch (\Exception $e) {
        \Log::error("Error enviando notificación: " . $e->getMessage());
    }
}
```

### Desde TypeScript (NestJS)

```typescript
import axios from 'axios';

private async enviarNotificacion(evento: string, payload: any): Promise<void> {
  try {
    const wsUrl = process.env.WS_NOTIFICATION_URL || 'http://localhost:9000';
    const token = process.env.WS_NOTIFICATION_TOKEN || 'dev';

    await axios.post(`${wsUrl}/notify`, {
      event: evento,
      payload: {
        ...payload,
        timestamp: new Date().toISOString(),
        source: 'practicas-ts'
      }
    }, {
      params: { token },
      timeout: 5000
    });
  } catch (error) {
    console.error(`Error enviando notificación:`, error.message);
  }
}
```

### Desde Java (Spring Boot)

```java
@Service
public class NotificationService {
    
    @Value("${ws.notification.url:http://localhost:9000}")
    private String wsNotificationUrl;
    
    @Value("${ws.notification.token:dev}")
    private String wsNotificationToken;
    
    private final RestTemplate restTemplate;
    
    public void enviarNotificacion(String evento, Map<String, Object> payload) {
        try {
            String url = wsNotificationUrl + "/notify?token=" + wsNotificationToken;
            
            Map<String, Object> notificationData = new HashMap<>();
            notificationData.put("event", evento);
            notificationData.put("payload", payload);
            
            restTemplate.postForObject(url, notificationData, String.class);
        } catch (Exception e) {
            System.err.println("Error enviando notificación: " + e.getMessage());
        }
    }
}
```

### Desde Python (FastAPI)

```python
import requests
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.ws_url = os.getenv('WS_NOTIFICATION_URL', 'http://localhost:9000')
        self.token = os.getenv('WS_NOTIFICATION_TOKEN', 'dev')

    def send_notification(self, event: str, payload: dict) -> bool:
        try:
            response = requests.post(
                f"{self.ws_url}/notify",
                json={
                    'event': event,
                    'payload': {
                        **payload,
                        'timestamp': datetime.utcnow().isoformat(),
                        'source': 'feedback-ia-python'
                    }
                },
                params={'token': self.token},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando notificación: {e}")
            return False
```

## 📊 Monitoreo y Logs

### Logs del Servidor

```bash
# Ver logs en tiempo real
docker-compose logs -f websocket_notifications

# Logs específicos
python src/main.py  # Modo desarrollo con logs detallados
```

### Métricas Disponibles

- **Conexiones activas**: Número total de clientes conectados
- **Distribución por salas**: Clientes por sala
- **Notificaciones enviadas**: Total histórico
- **Tiempo de actividad**: Uptime del servicio
- **Errores de conexión**: Fallos y reconexiones

### Debugging

```python
# Habilitar logs debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Ver todas las conexiones activas
GET /stats

# Ver historial completo
GET /history
```

## 🚀 Deployment

### Desarrollo

```bash
python src/main.py
```

### Producción con Docker

```bash
docker build -t exposia-websocket .
docker run -p 9000:9000 -e WS_TOKEN=production-token exposia-websocket
```

### Docker Compose

```yaml
websocket_notifications:
  build: ./websocket-notifications
  ports:
    - "9000:9000"
  environment:
    PORT: 9000
    WS_TOKEN: dev
    ENVIRONMENT: production
```

## 🔮 Roadmap

### Implementado ✅
- [x] WebSocket server básico
- [x] REST API para notificaciones
- [x] Gestión de salas
- [x] Cliente de prueba HTML
- [x] Testing automatizado
- [x] Integración con microservicios

### Próximas Funcionalidades 🔄
- [ ] Persistencia con Redis
- [ ] Autenticación JWT
- [ ] Rate limiting
- [ ] Métricas con Prometheus
- [ ] Clustering para escalabilidad
- [ ] Push notifications móviles

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Convenciones

- **Naming**: snake_case para Python
- **Events**: formato `entidad.accion`
- **Tests**: Cobertura mínima del 80%
- **Docs**: Documentar nuevos endpoints