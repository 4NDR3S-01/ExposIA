const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
app.use(express.json());

const server = http.createServer(app);
const wss = new WebSocket.Server({ server, path: '/ws' });

wss.on('connection', () => console.log('🔗 Cliente WS conectado'));

app.post('/notify', (req, res) => {
  console.log('📣 EVENTO', req.body);
  wss.clients.forEach(c =>
    c.readyState === 1 && c.send(JSON.stringify(req.body)),
  );
  res.json({ ok: true });
});

server.listen(9000, () => console.log('🪵 WS logger en puerto 9000'));
