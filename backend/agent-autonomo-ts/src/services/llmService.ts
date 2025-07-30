import { OpenAI } from '@langchain/openai';

// Procesa los datos usando un LLM (OpenAI)
export async function analyzeWithLLM(feedbackData: any): Promise<string> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('OPENAI_API_KEY no definido');

  const llm = new OpenAI({ openAIApiKey: apiKey });
  const prompt = `Resume y analiza el siguiente feedback: ${JSON.stringify(feedbackData)}`;
  const result = await llm.call(prompt);
  return result;
}
