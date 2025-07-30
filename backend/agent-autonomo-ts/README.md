# Módulo de Agente Autónomo con Flujos (TypeScript)

Este módulo implementa un agente inteligente autónomo que orquesta un flujo de trabajo usando LangChain y un LLM, integrándose con otros microservicios del proyecto ExposIA.

## Características
- Endpoint de activación: `POST /api/v1/start-analysis-agent`
- Orquestación de flujo con LangChain (no if/else)
- Llama a un microservicio externo (por ejemplo, feedback-ia-python)
- Usa un LLM (OpenAI/HuggingFace) para análisis/generación
- Persiste el resultado en una base de datos SQLite

## Instalación
```bash
cd backend/agent-autonomo-ts
npm install
```

## Variables de entorno
Crea un archivo `.env` con:
```
PORT=3005
OPENAI_API_KEY=tu_api_key
MICROSERVICE_FEEDBACK_URL=http://localhost:8000/api/feedback
```

## Ejecución
```bash
npm run dev
```

## Endpoint
- `POST /api/v1/start-analysis-agent`  
  Inicia el flujo del agente autónomo.

## Estructura del flujo
1. Recibe la petición de activación.
2. Llama a un endpoint de otro microservicio.
3. Usa un LLM para analizar/generar un resumen.
4. Persiste el resultado en la base de datos.

## Autor
Andrés (proyecto extra)
