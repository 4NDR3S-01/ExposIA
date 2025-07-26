const WebSocket = require('ws');
const axios = require('axios');

// Configuración
const WS_PORT = 4001;
const GATEWAY_URL = 'http://localhost:4000/';

// Crear servidor WebSocket
const wss = new WebSocket.Server({ 
  port: WS_PORT,
  path: '/ws'
});

console.log(`🔌 ExposIA WebSocket Server iniciado en puerto ${WS_PORT}`);
console.log(`📡 Conectar a: ws://localhost:${WS_PORT}/ws`);

// Almacenar conexiones activas
const clients = new Map();
let clientCounter = 0;

wss.on('connection', (ws, req) => {
  // Asignar ID único al cliente
  const clientId = ++clientCounter;
  clients.set(clientId, {
    ws: ws,
    id: clientId,
    connected: new Date(),
    ip: req.socket.remoteAddress
  });

  console.log(`🔗 Cliente ${clientId} conectado (${clients.size} conexiones activas)`);

  // Enviar mensaje de bienvenida
  ws.send(JSON.stringify({
    type: 'connection',
    message: 'Conectado al WebSocket Server de ExposIA',
    clientId: clientId,
    availableCommands: [
      'ping',
      'status',
      'test-gateway',
      'live-feedback',
      'mutation:iniciarPractica',
      'mutation:generarFeedback',
      'query:usuarios',
      'query:presentaciones'
    ]
  }));

  // Manejar mensajes entrantes
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);
      console.log(`📨 Cliente ${clientId} envió:`, data);

      await handleMessage(ws, clientId, data);
    } catch (error) {
      console.error(`❌ Error procesando mensaje de cliente ${clientId}:`, error);
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Error procesando mensaje',
        error: error.message
      }));
    }
  });

  // Manejar desconexión
  ws.on('close', () => {
    clients.delete(clientId);
    console.log(`🔌 Cliente ${clientId} desconectado (${clients.size} conexiones activas)`);
  });

  // Manejar errores
  ws.on('error', (error) => {
    console.error(`❌ Error WebSocket cliente ${clientId}:`, error);
  });
});

// Función para manejar mensajes
async function handleMessage(ws, clientId, data) {
  const { type, command, payload } = data;

  switch (type) {
    case 'ping':
      ws.send(JSON.stringify({
        type: 'pong',
        timestamp: new Date().toISOString(),
        clientId: clientId
      }));
      break;

    case 'status':
      ws.send(JSON.stringify({
        type: 'status',
        gateway: 'http://localhost:4000/',
        connectedClients: clients.size,
        uptime: process.uptime(),
        memory: process.memoryUsage()
      }));
      break;

    case 'test-gateway':
      await testGatewayConnection(ws, clientId);
      break;

    case 'graphql':
      await executeGraphQL(ws, clientId, payload);
      break;

    case 'live-feedback':
      await startLiveFeedbackDemo(ws, clientId, payload);
      break;

    default:
      ws.send(JSON.stringify({
        type: 'error',
        message: `Comando desconocido: ${type}`
      }));
  }
}

// Probar conexión con el Gateway
async function testGatewayConnection(ws, clientId) {
  try {
    // Test simple de conexión
    const response = await axios.post(GATEWAY_URL, {
      query: `
        query {
          usuarios {
            id
            nombre
            email
          }
        }
      `
    });

    ws.send(JSON.stringify({
      type: 'gateway-test',
      success: true,
      usuarios: response.data.data.usuarios.length,
      message: `Gateway conectado: ${response.data.data.usuarios.length} usuarios encontrados`
    }));

  } catch (error) {
    ws.send(JSON.stringify({
      type: 'gateway-test',
      success: false,
      error: error.message
    }));
  }
}

// Ejecutar consulta GraphQL
async function executeGraphQL(ws, clientId, payload) {
  try {
    const { query, variables } = payload;
    
    // Notificar inicio
    ws.send(JSON.stringify({
      type: 'graphql-start',
      message: 'Ejecutando consulta GraphQL...'
    }));

    const response = await axios.post(GATEWAY_URL, {
      query,
      variables
    });

    // Enviar resultado
    ws.send(JSON.stringify({
      type: 'graphql-result',
      success: !response.data.errors,
      data: response.data.data,
      errors: response.data.errors
    }));

  } catch (error) {
    ws.send(JSON.stringify({
      type: 'graphql-error',
      error: error.message
    }));
  }
}

// Demo de feedback en tiempo real
async function startLiveFeedbackDemo(ws, clientId, payload) {
  try {
    ws.send(JSON.stringify({
      type: 'live-demo-start',
      message: 'Iniciando demo de feedback en tiempo real...'
    }));

    // Paso 1: Crear práctica
    ws.send(JSON.stringify({
      type: 'live-step',
      step: 1,
      message: 'Creando práctica...'
    }));

    const practicaResponse = await axios.post(GATEWAY_URL, {
      query: `
        mutation {
          iniciarPractica(input: {
            id_usuario: "1"
            id_presentacion: "36"
            archivo_audio: "websocket-demo.mp3"
          }) {
            id
            id_usuario
            id_presentacion
          }
        }
      `
    });

    const practicaId = practicaResponse.data.data.iniciarPractica.id;

    ws.send(JSON.stringify({
      type: 'live-step',
      step: 1,
      completed: true,
      data: { practicaId }
    }));

    // Paso 2: Simular procesamiento
    for (let i = 0; i <= 100; i += 20) {
      ws.send(JSON.stringify({
        type: 'live-progress',
        step: 2,
        progress: i,
        message: `Procesando audio con IA... ${i}%`
      }));
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Paso 3: Generar feedback
    ws.send(JSON.stringify({
      type: 'live-step',
      step: 3,
      message: 'Generando feedback con IA...'
    }));

    const feedbackResponse = await axios.post(GATEWAY_URL, {
      query: `
        mutation {
          generarFeedback(input: {
            grabacion_id: ${practicaId}
            parametro_id: 1
            valor: 9.1
            comentario: "Feedback generado via WebSocket en tiempo real"
          }) {
            id
            valor
            comentario
            created_at
          }
        }
      `
    });

    ws.send(JSON.stringify({
      type: 'live-demo-complete',
      success: true,
      feedback: feedbackResponse.data.data.generarFeedback,
      message: '¡Demo completa! Feedback generado exitosamente'
    }));

  } catch (error) {
    ws.send(JSON.stringify({
      type: 'live-demo-error',
      error: error.message
    }));
  }
}

// Función para broadcast a todos los clientes
function broadcast(message) {
  const data = JSON.stringify(message);
  clients.forEach((client) => {
    if (client.ws.readyState === WebSocket.OPEN) {
      client.ws.send(data);
    }
  });
}

// Enviar notificaciones periódicas
setInterval(() => {
  if (clients.size > 0) {
    broadcast({
      type: 'heartbeat',
      timestamp: new Date().toISOString(),
      connectedClients: clients.size
    });
  }
}, 30000);

// Manejar cierre graceful
process.on('SIGTERM', () => {
  console.log('🔌 Cerrando WebSocket Server...');
  wss.close();
  process.exit(0);
});
