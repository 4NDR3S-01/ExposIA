// WS Logger mejorado: logs con timestamp, métricas, health, ping/pong, cierre limpio, configuración por env
const express = require('express');
const http = require('http');
const WebSocket = require('ws');

// Configuración por variables de entorno
const PORT = process.env.WS_LOGGER_PORT || 9000;
const WS_PATH = process.env.WS_LOGGER_PATH || '/ws';
const MAX_MSG_SIZE = parseInt(process.env.WS_LOGGER_MAX_MSG_SIZE || '4096', 10); // bytes

const app = express();
app.use(express.json());

// Métricas básicas
let metricas = {
  conexiones: 0,
  desconexiones: 0,
  mensajesEnviados: 0,
  mensajesRecibidos: 0,
  errores: 0,
};

function log(level, ...args) {
  const ts = new Date().toISOString();
  console[level](`[${ts}]`, ...args);
}

const server = http.createServer(app);
const wss = new WebSocket.Server({ server, path: WS_PATH });

wss.on('connection', (ws, req) => {
  const ip = req.socket.remoteAddress;
  metricas.conexiones++;
  log('info', `🔗 Cliente WS conectado desde ${ip}`);

  ws.on('message', (msg) => {
    metricas.mensajesRecibidos++;
    if (msg.length > MAX_MSG_SIZE) {
      log('warn', `Mensaje demasiado grande (${msg.length} bytes)`);
      ws.send(JSON.stringify({ error: 'Mensaje demasiado grande' }));
      return;
    }
    // Responder a ping manual
    try {
      const data = JSON.parse(msg);
      if (data && data.type === 'ping') {
        ws.send(JSON.stringify({ type: 'pong', ts: Date.now() }));
      }
    } catch {}
  });

  ws.on('error', err => {
    metricas.errores++;
    log('error', '❌ Error en cliente WS:', err.message);
  });

  ws.on('close', (code, reason) => {
    metricas.desconexiones++;
    log('info', `🔌 Cliente WS desconectado (${code}): ${reason}`);
  });
});

// Endpoint para enviar notificaciones a todos los clientes WS
app.post('/notify', (req, res) => {
  try {
    if (!req.body || Object.keys(req.body).length === 0) {
      return res.status(400).json({ ok: false, error: 'Body vacío o inválido' });
    }
    log('info', '📣 EVENTO', req.body);
    let enviados = 0;
    wss.clients.forEach(c => {
      if (c.readyState === WebSocket.OPEN) {
        try {
          c.send(JSON.stringify(req.body));
          enviados++;
          metricas.mensajesEnviados++;
        } catch (err) {
          metricas.errores++;
          log('error', '❌ Error enviando a cliente WS:', err.message);
        }
      }
    });
    res.json({ ok: true, enviados });
  } catch (err) {
    metricas.errores++;
    log('error', '❌ Error en /notify:', err.message);
    res.status(500).json({ ok: false, error: 'Error interno del servidor' });
  }
});

// Endpoint de healthcheck
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    wsPath: WS_PATH,
    port: PORT,
    metricas,
    clientesActivos: wss.clients.size,
    timestamp: new Date().toISOString(),
  });
});

server.on('error', err => {
  metricas.errores++;
  log('error', '❌ Error en el servidor HTTP:', err.message);
  process.exit(1);
});

// Cierre limpio con señales
['SIGINT', 'SIGTERM'].forEach(sig => {
  process.on(sig, () => {
    log('info', `Recibida señal ${sig}, cerrando...`);
    server.close(() => {
      log('info', 'Servidor HTTP cerrado');
      process.exit(0);
    });
    wss.close(() => {
      log('info', 'Servidor WS cerrado');
    });
    setTimeout(() => process.exit(0), 3000); // Forzar salida si tarda
  });
});

server.listen(PORT, () => log('info', `🪵 WS logger en puerto ${PORT} (path: ${WS_PATH})`));

// Uso:
// - Conéctate por WS a ws://localhost:9000/ws (o el puerto/path configurado)
// - POST a /notify para enviar mensajes a todos los clientes
// - GET /health para ver estado y métricas
