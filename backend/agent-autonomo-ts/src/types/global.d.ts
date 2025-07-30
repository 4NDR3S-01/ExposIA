// Tipos globales para Express y Node
import 'express';
declare namespace NodeJS {
  interface ProcessEnv {
    PORT?: string;
    OPENAI_API_KEY?: string;
    MICROSERVICE_FEEDBACK_URL?: string;
  }
}
