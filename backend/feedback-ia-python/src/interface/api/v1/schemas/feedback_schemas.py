"""
Esquemas Pydantic para validación de datos de Feedback en la API.
Definen la estructura y validaciones para las peticiones HTTP.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class FeedbackCreateSchema(BaseModel):
    """Esquema para crear un nuevo feedback."""
    
    grabacion_id: int = Field(..., gt=0, description="ID de la grabación")
    parametro_id: int = Field(..., gt=0, description="ID del parámetro")
    valor: float = Field(..., ge=0, le=100, description="Valor del feedback (0-100)")
    comentario: Optional[str] = Field(None, max_length=1000, description="Comentario opcional")
    es_manual: bool = Field(False, description="Indica si es feedback manual")
    
    @validator('comentario')
    def validate_comentario(cls, v, values):
        """Valida que el comentario sea requerido para feedbacks manuales."""
        if values.get('es_manual') and not v:
            raise ValueError('El comentario es requerido para feedbacks manuales')
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El comentario no puede estar vacío')
        return v.strip() if v else v
    
    class Config:
        json_schema_extra = {
            "example": {
                "grabacion_id": 1,
                "parametro_id": 2,
                "valor": 85.5,
                "comentario": "Excelente claridad en la presentación",
                "es_manual": True
            }
        }


class FeedbackUpdateSchema(BaseModel):
    """Esquema para actualizar un feedback existente."""
    
    valor: Optional[float] = Field(None, ge=0, le=100, description="Nuevo valor del feedback")
    comentario: Optional[str] = Field(None, max_length=1000, description="Nuevo comentario")
    es_manual: Optional[bool] = Field(None, description="Cambiar tipo de feedback")
    
    @validator('comentario')
    def validate_comentario(cls, v):
        """Valida el comentario si se proporciona."""
        if v is not None and len(v.strip()) == 0:
            raise ValueError('El comentario no puede estar vacío')
        return v.strip() if v else v
    
    class Config:
        json_schema_extra = {
            "example": {
                "valor": 90.0,
                "comentario": "Actualización: Mejora significativa en el ritmo"
            }
        }


class FeedbackResponseSchema(BaseModel):
    """Esquema de respuesta para feedback."""
    
    id: int = Field(..., description="ID único del feedback")
    grabacion_id: int = Field(..., description="ID de la grabación")
    parametro_id: int = Field(..., description="ID del parámetro")
    valor: float = Field(..., description="Valor del feedback (0-100)")
    comentario: Optional[str] = Field(None, description="Comentario del feedback")
    es_manual: bool = Field(..., description="Indica si es feedback manual")
    performance_level: str = Field(..., description="Nivel de rendimiento")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "grabacion_id": 1,
                "parametro_id": 2,
                "valor": 85.5,
                "comentario": "Excelente claridad en la presentación",
                "es_manual": True,
                "performance_level": "Muy Bueno",
                "created_at": "2025-06-09T10:30:00Z",
                "updated_at": "2025-06-09T10:30:00Z"
            }
        }


class GenerateAIFeedbackSchema(BaseModel):
    """Esquema para generar feedback automático con IA."""
    
    grabacion_id: int = Field(..., gt=0, description="ID de la grabación a analizar")
    parametros_ids: List[int] = Field(..., min_items=1, description="Lista de IDs de parámetros")
    audio_analysis_data: dict = Field(..., description="Datos del análisis de audio")
    use_advanced_model: bool = Field(False, description="Usar modelo avanzado de IA")
    
    @validator('parametros_ids')
    def validate_parametros_ids(cls, v):
        """Valida que todos los IDs de parámetros sean válidos."""
        if not all(param_id > 0 for param_id in v):
            raise ValueError('Todos los IDs de parámetros deben ser mayores a 0')
        if len(set(v)) != len(v):
            raise ValueError('No puede haber IDs de parámetros duplicados')
        return v
    
    @validator('audio_analysis_data')
    def validate_audio_analysis_data(cls, v):
        """Valida la estructura básica de los datos de análisis."""
        if not isinstance(v, dict):
            raise ValueError('audio_analysis_data debe ser un objeto')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "grabacion_id": 1,
                "parametros_ids": [1, 2, 3],
                "audio_analysis_data": {
                    "duration_seconds": 120,
                    "audio_metrics": {
                        "clarity_score": 0.85,
                        "volume_consistency": 0.78,
                        "speech_rate": 145
                    }
                },
                "use_advanced_model": True
            }
        }


class FeedbackFilterSchema(BaseModel):
    """Esquema para filtrar feedbacks."""
    
    grabacion_id: Optional[int] = Field(None, gt=0, description="Filtrar por grabación")
    parametro_id: Optional[int] = Field(None, gt=0, description="Filtrar por parámetro")
    es_manual: Optional[bool] = Field(None, description="Filtrar por tipo manual/automático")
    min_valor: Optional[float] = Field(None, ge=0, le=100, description="Valor mínimo")
    max_valor: Optional[float] = Field(None, ge=0, le=100, description="Valor máximo")
    
    @validator('max_valor')
    def validate_valor_range(cls, v, values):
        """Valida que max_valor sea mayor que min_valor."""
        min_valor = values.get('min_valor')
        if min_valor is not None and v is not None and v < min_valor:
            raise ValueError('max_valor debe ser mayor o igual que min_valor')
        return v


class FeedbackListResponseSchema(BaseModel):
    """Esquema de respuesta para lista de feedbacks."""
    
    feedbacks: List[FeedbackResponseSchema] = Field(..., description="Lista de feedbacks")
    total: int = Field(..., description="Total de feedbacks encontrados")
    skip: int = Field(..., description="Elementos omitidos")
    limit: int = Field(..., description="Límite de elementos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feedbacks": [
                    {
                        "id": 1,
                        "grabacion_id": 1,
                        "parametro_id": 2,
                        "valor": 85.5,
                        "comentario": "Excelente claridad",
                        "es_manual": True,
                        "performance_level": "Muy Bueno",
                        "created_at": "2025-06-09T10:30:00Z",
                        "updated_at": "2025-06-09T10:30:00Z"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100
            }
        }


class FeedbackSummarySchema(BaseModel):
    """Esquema para resumen estadístico de feedbacks."""
    
    total_feedbacks: int = Field(..., description="Total de feedbacks")
    feedbacks_automaticos: int = Field(..., description="Feedbacks automáticos")
    feedbacks_manuales: int = Field(..., description="Feedbacks manuales")
    promedio_general: float = Field(..., description="Promedio general")
    promedio_automaticos: float = Field(..., description="Promedio de automáticos")
    promedio_manuales: float = Field(..., description="Promedio de manuales")
    feedbacks_altos: int = Field(..., description="Feedbacks con puntaje alto (>80)")
    feedbacks_medios: int = Field(..., description="Feedbacks con puntaje medio (40-80)")
    feedbacks_bajos: int = Field(..., description="Feedbacks con puntaje bajo (<40)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_feedbacks": 50,
                "feedbacks_automaticos": 35,
                "feedbacks_manuales": 15,
                "promedio_general": 75.8,
                "promedio_automaticos": 72.3,
                "promedio_manuales": 83.1,
                "feedbacks_altos": 25,
                "feedbacks_medios": 20,
                "feedbacks_bajos": 5
            }
        }


class ErrorResponseSchema(BaseModel):
    """Esquema para respuestas de error."""
    
    detail: str = Field(..., description="Descripción del error")
    error_code: Optional[str] = Field(None, description="Código de error específico")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp del error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Feedback con ID 123 no encontrado",
                "error_code": "FEEDBACK_NOT_FOUND",
                "timestamp": "2025-06-09T10:30:00Z"
            }
        }
