# filepath: /src/interface/api/v1/endpoints/health_endpoints.py
"""
Endpoints de salud del sistema.
Estos endpoints no requieren autenticación y proporcionan información básica del estado del sistema.
"""
from fastapi import APIRouter, status
from typing import Dict
import os
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Estado de salud del sistema",
    description="Verifica que el sistema esté funcionando correctamente. No requiere autenticación."
)
async def health_check() -> Dict[str, str]:
    """
    Endpoint de health check que no requiere autenticación.
    
    Returns:
        Diccionario con el estado del sistema
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "feedback-ia-python",
        "version": "1.0.0"
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Información básica del servicio",
    description="Proporciona información básica sobre el servicio. No requiere autenticación."
)
async def root() -> Dict[str, str]:
    """
    Endpoint raíz con información básica del servicio.
    
    Returns:
        Diccionario con información del servicio
    """
    return {
        "message": "Feedback IA Python Service",
        "description": "API para gestión de feedbacks con análisis de IA",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    summary="Información detallada del sistema",
    description="Proporciona información detallada sobre la configuración del sistema."
)
async def system_info() -> Dict[str, str]:
    """
    Información detallada del sistema y configuración.
    
    Returns:
        Diccionario con información del sistema
    """
    return {
        "service_name": "feedback-ia-python",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug_mode": os.getenv("DEBUG", "false"),
        "database_type": "SQLite/PostgreSQL",
        "auth_method": "Bearer Token",
        "timestamp": datetime.utcnow().isoformat()
    }
