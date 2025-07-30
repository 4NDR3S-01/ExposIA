import axios from 'axios';
import { analyzeWithLLM } from './llmService';
import { saveResult } from './dbService';

// Flujo principal del agente autónomo
export async function startAgentFlow(): Promise<any> {
  // Paso 1: Llamar a microservicio externo (feedback)
  const feedbackUrl = process.env.MICROSERVICE_FEEDBACK_URL || 'http://localhost:8000/api/feedback';
  const feedbackResponse = await axios.get(feedbackUrl);
  const feedbackData = feedbackResponse.data;

  // Paso 2: Procesar datos con LLM
  const llmResult = await analyzeWithLLM(feedbackData);

  // Paso 3: Persistir resultado
  const saved = await saveResult(llmResult);

  return { llmResult, saved };
}
