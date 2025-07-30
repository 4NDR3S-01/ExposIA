import { Router, Request, Response } from 'express';
import { saveResult } from '../services/dbService';

export const persistRouter = Router();

// Endpoint para guardar resultados manualmente (opcional, para pruebas)
persistRouter.post('/save-result', async (req: Request, res: Response) => {
  try {
    const { content } = req.body;
    if (!content) return res.status(400).json({ error: 'Falta el campo content' });
    const saved = await saveResult(content);
    res.status(201).json({ success: true, saved });
  } catch (error: any) {
    res.status(500).json({ success: false, error: error.message });
  }
});
