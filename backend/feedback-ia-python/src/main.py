from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from src.api.endpoints import router as public_router
from src.api.secure_endpoints import router as secure_router
from src.database.connection import Base, engine
from src.infrastructure.config.settings import settings

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app.title,
    description=settings.app.description,
    version=settings.app.version,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores de excepciones personalizados
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Maneja excepciones HTTP con formato consistente."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": getattr(exc, 'error_code', None),
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic."""
    # Si el input recibido es bytes, conviértelo a string para mostrarlo en el error
    input_data = None
    try:
        if exc.body:
            if isinstance(exc.body, bytes):
                input_data = exc.body.decode("utf-8", errors="replace")
            else:
                input_data = exc.body
    except Exception:
        input_data = None
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación",
            "errors": exc.errors(),
            "input": input_data,
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
            "path": str(request.url),
            "method": request.method
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales no capturadas."""
    if settings.is_development:
        # En desarrollo, mostrar el error completo
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Error interno del servidor",
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "path": str(request.url),
                "method": request.method
            }
        )
    else:
        # En producción, ocultar detalles del error
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Error interno del servidor",
                "path": str(request.url),
                "method": request.method
            }
        )

# Incluir routers
app.include_router(public_router, prefix="/api/v1/public", tags=["public"])
app.include_router(secure_router, prefix="/api/v1", tags=["authenticated"])

@app.get("/")
def root():
    """Endpoint raíz con información de la API."""
    return {
        "message": "Módulo de Feedback API",
        "version": settings.app.version,
        "status": "operational",
        "documentation": "/docs" if settings.is_development else "Disabled in production",
        "authentication": "Bearer token required for most endpoints"
    }

@app.get("/health")
def health_check():
    """Endpoint de verificación de salud."""
    return {
        "status": "healthy",
        "service": "feedback-ia-python",
        "version": settings.app.version,
        "environment": "development" if settings.is_development else "production"
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.is_development,
        log_level="debug" if settings.is_development else "info"
    )