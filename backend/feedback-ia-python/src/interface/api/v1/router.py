# filepath: /src/interface/api/v1/router.py
"""
Router principal de la API v1.
Incluye todos los endpoints de la aplicación organizados por módulos.
"""
from fastapi import APIRouter

from .endpoints.health_endpoints import router as health_router
from .endpoints.feedback_endpoints import router as feedback_router
from .endpoints.tipo_metrica_endpoints import router as tipo_metrica_router
from .endpoints.metrica_endpoints import router as metrica_router
from .endpoints.parametro_endpoints import router as parametro_router
from .endpoints.grabacion_endpoints import router as grabacion_router

# Router principal de la API v1
api_v1_router = APIRouter()

# Incluir todos los routers de endpoints
api_v1_router.include_router(
    health_router,
    tags=["health"]
)

api_v1_router.include_router(
    feedback_router,
    tags=["feedbacks"]
)

api_v1_router.include_router(
    tipo_metrica_router,
    tags=["tipos-metrica"]
)

api_v1_router.include_router(
    metrica_router,
    tags=["metricas"]
)

api_v1_router.include_router(
    parametro_router,
    tags=["parametros"]
)

api_v1_router.include_router(
    grabacion_router,
    tags=["grabaciones"]
)
