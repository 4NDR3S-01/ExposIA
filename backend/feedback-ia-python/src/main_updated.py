# filepath: /src/main_updated.py
"""
Aplicación principal de FastAPI para el módulo feedback-ia-python.
Incluye configuración de seguridad, manejo de errores y rutas con autenticación.
"""
import os
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

# Importar endpoints
from interface.api.v1.endpoints.health_endpoints import router as health_router
from interface.api.v1.endpoints.feedback_endpoints import router as feedback_router

# Importar configuración de base de datos
from infrastructure.database.connection import Base, engine

# Configurar variables de entorno por defecto
os.environ.setdefault("API_KEY", "default-api-key-12345")
os.environ.setdefault("DEBUG", "true")

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configuración de la aplicación
app = FastAPI(
    title="Feedback IA Python Service",
    description="API para gestión de feedbacks con análisis de IA siguiendo Clean Architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Endpoints de salud del sistema (sin autenticación)"
        },
        {
            "name": "feedbacks", 
            "description": "Gestión de feedbacks (requiere autenticación)"
        }
    ]
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MANEJADORES DE EXCEPCIONES ===

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Maneja excepciones HTTP con formato consistente."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_type": "HTTPException",
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación de datos",
            "error_type": "ValidationError",
            "errors": exc.errors(),
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    """Maneja excepciones HTTP de Starlette."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_type": "StarletteHTTPException",
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales no capturadas."""
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    if debug_mode:
        # En desarrollo, mostrar detalles del error
        import traceback
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "path": str(request.url),
                "method": request.method
            }
        )
    else:
        # En producción, ocultar detalles del error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor",
                "error_type": "InternalServerError",
                "path": str(request.url),
                "method": request.method
            }
        )

# === MIDDLEWARE DE INICIO ===

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Añade headers de seguridad a todas las respuestas."""
    response = await call_next(request)
    
    # Headers de seguridad básicos
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response

# === INCLUIR ROUTERS ===

# Endpoints sin autenticación (health checks)
app.include_router(health_router)

# Endpoints con autenticación (funcionalidad principal)
app.include_router(
    feedback_router, 
    prefix="/api/v1"
)

# === EVENTOS DE INICIO Y PARADA ===

@app.on_event("startup")
async def startup_event():
    """Eventos que se ejecutan al iniciar la aplicación."""
    print("🚀 Iniciando Feedback IA Python Service...")
    print(f"📊 Modo debug: {os.getenv('DEBUG', 'false')}")
    print(f"🔐 API Key configurada: {'✅' if os.getenv('API_KEY') else '❌'}")
    print("✅ Servicio iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos que se ejecutan al parar la aplicación."""
    print("🛑 Cerrando Feedback IA Python Service...")
    print("✅ Servicio cerrado correctamente")

# === FUNCIÓN PRINCIPAL ===

if __name__ == "__main__":
    # Configuración para desarrollo
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        "main_updated:app",
        host="0.0.0.0",
        port=8000,
        reload=debug_mode,
        log_level="debug" if debug_mode else "info",
        access_log=debug_mode
    )
