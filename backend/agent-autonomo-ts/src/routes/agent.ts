import { Router } from 'express';
import { startAgentFlow } from '../services/agentService';

export const agentRouter = Router();

// Endpoint de activación del agente autónomo
agentRouter.post('/start-analysis-agent', async (req, res) => {
  try {
    const result = await startAgentFlow();
    res.status(200).json({ success: true, result });
  } catch (error: any) {
    res.status(500).json({ success: false, error: error.message });
  }
});
