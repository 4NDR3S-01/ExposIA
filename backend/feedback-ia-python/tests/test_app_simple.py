# filepath: /tests/test_app_simple.py
"""
Aplicación de prueba simplificada para testing.
"""
import os
import sys

# Configurar variables de entorno
os.environ["API_KEY"] = "test-api-key-12345"
os.environ["DEBUG"] = "true"

# Añadir el directorio src al path
sys.path.insert(0, '/home/andres/Documentos/ExposIA/backend/feedback-ia-python/src')

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from infrastructure.security.auth_middleware import verify_api_key

app = FastAPI(title="Test App")
security = HTTPBearer()

@app.get("/health")
async def health_check():
    """Endpoint de salud sin autenticación."""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """Endpoint raíz sin autenticación."""
    return {"message": "Feedback IA Python Service"}

@app.get("/info")
async def info():
    """Endpoint de información sin autenticación."""
    return {"service_name": "feedback-ia-python"}

@app.get("/api/v1/feedbacks/")
async def get_feedbacks(token: str = Depends(verify_api_key)):
    """Endpoint protegido que requiere autenticación."""
    return {"feedbacks": []}

@app.post("/api/v1/feedbacks/")
async def create_feedback(
    feedback_data: dict,
    token: str = Depends(verify_api_key)
):
    """Endpoint protegido para crear feedback."""
    return {"message": "Feedback created", "data": feedback_data}
