const WebSocket = require('ws');

// Cliente WebSocket para probar el sistema ExposIA
class ExposiaWebSocketClient {
  constructor(url = 'ws://localhost:4001/ws') {
    this.url = url;
    this.ws = null;
    this.isConnected = false;
  }

  // Conectar al WebSocket Server
  connect() {
    return new Promise((resolve, reject) => {
      console.log(`🔌 Conectando a ${this.url}...`);
      
      this.ws = new WebSocket(this.url);

      this.ws.on('open', () => {
        this.isConnected = true;
        console.log('✅ Conectado al WebSocket Server');
        resolve();
      });

      this.ws.on('message', (data) => {
        try {
          const message = JSON.parse(data);
          this.handleMessage(message);
        } catch (error) {
          console.log('📨 Mensaje raw:', data.toString());
        }
      });

      this.ws.on('close', () => {
        this.isConnected = false;
        console.log('🔌 Conexión WebSocket cerrada');
      });

      this.ws.on('error', (error) => {
        console.error('❌ Error WebSocket:', error);
        reject(error);
      });
    });
  }

  // Manejar mensajes del servidor
  handleMessage(message) {
    const { type } = message;

    switch (type) {
      case 'connection':
        console.log('🎉 Bienvenida del servidor:');
        console.log(`   Cliente ID: ${message.clientId}`);
        console.log(`   Comandos disponibles: ${message.availableCommands.join(', ')}`);
        break;

      case 'pong':
        console.log(`🏓 Pong recibido: ${message.timestamp}`);
        break;

      case 'status':
        console.log('📊 Estado del sistema:');
        console.log(`   Gateway: ${message.gateway}`);
        console.log(`   Clientes conectados: ${message.connectedClients}`);
        console.log(`   Uptime: ${Math.round(message.uptime)}s`);
        break;

      case 'gateway-test':
        if (message.success) {
          console.log(`✅ Gateway Test: ${message.message}`);
        } else {
          console.log(`❌ Gateway Test Error: ${message.error}`);
        }
        break;

      case 'live-demo-start':
        console.log('\n🎬 === DEMO EN TIEMPO REAL INICIADA ===');
        break;

      case 'live-step':
        if (message.completed) {
          console.log(`✅ Paso ${message.step} completado`);
          if (message.data) {
            console.log(`   Datos: ${JSON.stringify(message.data)}`);
          }
        } else {
          console.log(`🔄 Paso ${message.step}: ${message.message}`);
        }
        break;

      case 'live-progress':
        process.stdout.write(`\r🤖 ${message.message}   `);
        if (message.progress === 100) {
          console.log(''); // Nueva línea
        }
        break;

      case 'live-demo-complete':
        console.log('\n🎉 === DEMO COMPLETADA ===');
        console.log(`   Feedback ID: ${message.feedback.id}`);
        console.log(`   Puntuación: ${message.feedback.valor}/10`);
        console.log(`   Comentario: "${message.feedback.comentario}"`);
        break;

      case 'graphql-start':
        console.log('🔄 Ejecutando GraphQL...');
        break;

      case 'graphql-result':
        if (message.success) {
          console.log('✅ GraphQL ejecutado exitosamente:');
          console.log(JSON.stringify(message.data, null, 2));
        } else {
          console.log('❌ GraphQL con errores:');
          console.log(message.errors);
        }
        break;

      case 'heartbeat':
        // Silencioso - solo para mantener conexión
        break;

      default:
        console.log(`📨 Mensaje recibido:`, message);
    }
  }

  // Enviar mensaje al servidor
  send(message) {
    if (this.isConnected) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.log('❌ No conectado al WebSocket');
    }
  }

  // Comandos de prueba
  ping() {
    this.send({ type: 'ping' });
  }

  getStatus() {
    this.send({ type: 'status' });
  }

  testGateway() {
    this.send({ type: 'test-gateway' });
  }

  runLiveFeedbackDemo() {
    this.send({ type: 'live-feedback' });
  }

  executeGraphQL(query, variables = {}) {
    this.send({
      type: 'graphql',
      payload: { query, variables }
    });
  }

  // Desconectar
  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Demo interactivo
async function runDemo() {
  const client = new ExposiaWebSocketClient();

  try {
    await client.connect();

    console.log('\n🎮 === DEMO INTERACTIVO EXPOSIA WEBSOCKET ===\n');

    // Test 1: Ping
    console.log('1️⃣ Probando ping...');
    client.ping();
    await sleep(1000);

    // Test 2: Estado del sistema
    console.log('\n2️⃣ Consultando estado del sistema...');
    client.getStatus();
    await sleep(1000);

    // Test 3: Probar Gateway
    console.log('\n3️⃣ Probando conexión con Gateway...');
    client.testGateway();
    await sleep(2000);

    // Test 4: Consulta GraphQL
    console.log('\n4️⃣ Ejecutando consulta GraphQL...');
    client.executeGraphQL(`
      query {
        presentaciones {
          id
          titulo
          id_usuario
        }
      }
    `);
    await sleep(2000);

    // Test 5: Demo en tiempo real
    console.log('\n5️⃣ Iniciando demo de feedback en tiempo real...');
    client.runLiveFeedbackDemo();
    await sleep(10000);

    console.log('\n✅ Demo completada. Cerrando conexión...');
    client.disconnect();

  } catch (error) {
    console.error('❌ Error en demo:', error);
  }
}

// Función helper
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Ejecutar demo si el script se ejecuta directamente
if (require.main === module) {
  runDemo();
}

module.exports = ExposiaWebSocketClient;
