import express from 'express';
import dotenv from 'dotenv';
import { agentRouter } from './routes/agent';
import { persistRouter } from './routes/persist';

// Cargar variables de entorno
dotenv.config();

const app = express();
app.use(express.json());

// Rutas del agente
app.use('/api/v1', agentRouter);
app.use('/api/v1', persistRouter);

const PORT = process.env.PORT || 3005;
app.listen(PORT, () => {
  console.log(`Agente autónomo escuchando en puerto ${PORT}`);
});
