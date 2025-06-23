"""
Data Transfer Objects (DTOs) para Feedback.
Objetos para transferir datos entre capas de la aplicación.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ...domain.entities.feedback import Feedback


@dataclass
class CreateFeedbackDTO:
    """DTO para crear un nuevo feedback."""
    
    grabacion_id: int
    parametro_id: int
    valor: float
    comentario: Optional[str] = None
    es_manual: bool = False
    
    def validate(self) -> None:
        """Valida los datos del DTO."""
        if self.grabacion_id <= 0:
            raise ValueError("El ID de grabación debe ser mayor a 0")
        
        if self.parametro_id <= 0:
            raise ValueError("El ID de parámetro debe ser mayor a 0")
        
        if not (0 <= self.valor <= 100):
            raise ValueError("El valor debe estar entre 0 y 100")
        
        if self.es_manual and not self.comentario:
            raise ValueError("El comentario es requerido para feedbacks manuales")


@dataclass
class UpdateFeedbackDTO:
    """DTO para actualizar un feedback existente."""
    
    valor: Optional[float] = None
    comentario: Optional[str] = None
    es_manual: Optional[bool] = None
    
    def has_changes(self) -> bool:
        """Verifica si hay cambios en el DTO."""
        return any([
            self.valor is not None,
            self.comentario is not None,
            self.es_manual is not None
        ])


@dataclass
class FeedbackResponseDTO:
    """DTO de respuesta para feedback."""
    
    id: int
    grabacion_id: int
    parametro_id: int
    valor: float
    comentario: Optional[str]
    es_manual: bool
    performance_level: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, feedback: Feedback) -> 'FeedbackResponseDTO':
        """Crea un DTO de respuesta desde una entidad de dominio."""
        return cls(
            id=feedback.id,
            grabacion_id=feedback.grabacion_id,
            parametro_id=feedback.parametro_id,
            valor=feedback.score.value,
            comentario=feedback.comentario,
            es_manual=feedback.es_manual,
            performance_level=feedback.get_performance_level(),
            created_at=feedback.created_at,
            updated_at=feedback.updated_at
        )
    
    def to_dict(self) -> dict:
        """Convierte el DTO a diccionario."""
        return {
            'id': self.id,
            'grabacion_id': self.grabacion_id,
            'parametro_id': self.parametro_id,
            'valor': self.valor,
            'comentario': self.comentario,
            'es_manual': self.es_manual,
            'performance_level': self.performance_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class FeedbackFilterDTO:
    """DTO para filtrar feedbacks."""
    
    grabacion_id: Optional[int] = None
    parametro_id: Optional[int] = None
    es_manual: Optional[bool] = None
    min_valor: Optional[float] = None
    max_valor: Optional[float] = None
    skip: int = 0
    limit: int = 100
    
    def validate(self) -> None:
        """Valida los filtros."""
        if self.skip < 0:
            raise ValueError("Skip debe ser mayor o igual a 0")
        
        if self.limit <= 0 or self.limit > 1000:
            raise ValueError("Limit debe estar entre 1 y 1000")
        
        if self.min_valor is not None and not (0 <= self.min_valor <= 100):
            raise ValueError("min_valor debe estar entre 0 y 100")
        
        if self.max_valor is not None and not (0 <= self.max_valor <= 100):
            raise ValueError("max_valor debe estar entre 0 y 100")
        
        if (self.min_valor is not None and 
            self.max_valor is not None and 
            self.min_valor > self.max_valor):
            raise ValueError("min_valor no puede ser mayor que max_valor")


@dataclass
class GenerateAIFeedbackDTO:
    """DTO para generar feedback automático con IA."""
    
    grabacion_id: int
    parametros_ids: list[int]
    audio_analysis_data: dict
    use_advanced_model: bool = False
    
    def validate(self) -> None:
        """Valida los datos para generación de feedback con IA."""
        if self.grabacion_id <= 0:
            raise ValueError("El ID de grabación debe ser mayor a 0")
        
        if not self.parametros_ids:
            raise ValueError("Debe especificar al menos un parámetro")
        
        if not all(param_id > 0 for param_id in self.parametros_ids):
            raise ValueError("Todos los IDs de parámetros deben ser mayores a 0")
        
        if not isinstance(self.audio_analysis_data, dict):
            raise ValueError("audio_analysis_data debe ser un diccionario")


@dataclass
class FeedbackSummaryDTO:
    """DTO para resumen de feedbacks."""
    
    total_feedbacks: int
    feedbacks_automaticos: int
    feedbacks_manuales: int
    promedio_general: float
    promedio_automaticos: float
    promedio_manuales: float
    feedbacks_altos: int  # > 80
    feedbacks_medios: int  # 40-80
    feedbacks_bajos: int  # < 40
