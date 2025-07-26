# 🔌 ExposIA WebSocket Integration

## 📋 Descripción
Sistema de comunicación en tiempo real para ExposIA que complementa el API Gateway GraphQL con capacidades WebSocket.

## 🏗️ Arquitectura

```
Cliente (Browser/Test) 
    ↓ WebSocket
WebSocket Server (Puerto 4001)
    ↓ HTTP/GraphQL
API Gateway GraphQL (Puerto 4000)
    ↓ REST APIs
Microservicios (PHP, TypeScript, Python, Java)
```

## 🚀 Características

### ✅ Implementado
- **WebSocket Server** en puerto 4001
- **Comunicación bidireccional** en tiempo real
- **Integración con GraphQL Gateway** (puerto 4000)
- **Demo de feedback IA** en vivo
- **Cliente de prueba** interactivo
- **Gestión de múltiples clientes**
- **Heartbeat automático**

### 🔧 Funcionalidades

1. **Comandos disponibles:**
   - `ping` - Test de conectividad
   - `status` - Estado del sistema
   - `test-gateway` - Probar conexión con Gateway
   - `live-feedback` - Demo de feedback IA en tiempo real
   - `graphql` - Ejecutar consultas/mutaciones GraphQL

2. **Eventos en tiempo real:**
   - Notificaciones de operaciones
   - Progreso de procesos largos
   - Resultados de feedback IA
   - Estado de microservicios

## 🛠️ Uso

### Iniciar WebSocket Server
```bash
npm run ws-server
```

### Probar cliente WebSocket
```bash
npm run ws-client
```

### Prueba completa del flujo
```bash
npm run ws-test
```

### Sistema completo (Gateway + WebSocket)
```bash
npm run full-system
```

## 📡 Protocolo de Mensajes

### Mensajes del Cliente → Servidor
```json
{
  "type": "ping | status | test-gateway | live-feedback | graphql",
  "payload": { /* datos opcionales */ }
}
```

### Mensajes del Servidor → Cliente
```json
{
  "type": "connection | pong | status | gateway-test | live-demo-start | live-step | live-progress | live-demo-complete | graphql-result",
  "clientId": "uuid",
  "timestamp": "ISO string",
  "data": { /* datos del mensaje */ }
}
```

## 🧪 Casos de Uso

### 1. Feedback en Tiempo Real
El usuario puede ver el progreso del análisis de IA:
```
🎬 Demo iniciada
🔄 Conectando con IA...
🤖 Analizando presentación... 25%
🤖 Procesando texto... 50%
🤖 Generando feedback... 75%
✅ Feedback completado: 8.5/10
```

### 2. Operaciones GraphQL Asíncronas
Ejecutar mutaciones complejas y recibir notificaciones:
```javascript
client.executeGraphQL(`
  mutation {
    createPresentacion(titulo: "Demo", descripcion: "Test", id_usuario: 1) {
      id titulo descripcion
    }
  }
`);
```

### 3. Monitoreo del Sistema
Estado en tiempo real de todos los microservicios:
```
📊 Estado del sistema:
   Gateway: ✅ Activo
   Clientes conectados: 3
   Uptime: 120s
```

## 🔗 Integración con GraphQL

El WebSocket Server actúa como **proxy inteligente**:

1. **Recibe comandos** vía WebSocket
2. **Traduce a GraphQL** cuando es necesario
3. **Ejecuta en Gateway** (puerto 4000)
4. **Retorna resultados** en tiempo real

## 📁 Archivos Clave

- `websocket-server.js` - Servidor WebSocket principal
- `websocket-client.js` - Cliente de prueba
- `test-complete-flow.js` - Test completo del flujo
- `package.json` - Scripts npm actualizados

## 🐛 Debugging

### Logs del servidor
```bash
npm run ws-server
# Ver logs en consola del servidor
```

### Test de conectividad
```bash
npm run ws-client
# Cliente interactivo con múltiples pruebas
```

### Test completo
```bash
npm run ws-test
# Flujo completo: WebSocket → GraphQL → Microservicios
```

## 🔄 Flujo de Datos

1. **Cliente conecta** → WebSocket Server (4001)
2. **Envía comando** → Servidor procesa
3. **Si es GraphQL** → Proxy a Gateway (4000)
4. **Gateway orquesta** → Microservicios (8001, 3000, 8000, 8080)
5. **Respuesta regresa** → Cliente vía WebSocket
6. **Notificaciones en tiempo real** → Todos los clientes conectados

## 🎯 Ventajas

- ✅ **Tiempo real** sin polling
- ✅ **Notificaciones push** instantáneas
- ✅ **Múltiples clientes** simultáneos
- ✅ **Integración transparente** con GraphQL
- ✅ **Fallback a REST** si es necesario
- ✅ **Demos interactivos** del sistema IA

---

*Este sistema complementa perfectamente el API Gateway GraphQL existente, añadiendo capacidades de tiempo real sin modificar la arquitectura base.*
