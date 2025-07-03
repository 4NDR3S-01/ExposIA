"""
Entidad de dominio para Feedback.
Contiene únicamente lógica de negocio pura, sin dependencias externas.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ..value_objects.feedback_score import FeedbackScore
from ..exceptions.validation_exceptions import InvalidFeedbackDataError


@dataclass
class Feedback:
    """
    Entidad de dominio que representa un feedback de una grabación.
    
    Esta clase contiene únicamente lógica de negocio pura y no tiene
    dependencias de frameworks o bibliotecas externas.
    """
    
    id: Optional[int]
    grabacion_id: int
    parametro_id: int
    score: FeedbackScore
    comentario: Optional[str]
    es_manual: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de dominio que se ejecutan después de la creación."""
        self._validate()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def _validate(self) -> None:
        """Valida las reglas de negocio de la entidad."""
        if self.grabacion_id <= 0:
            raise InvalidFeedbackDataError("El ID de grabación debe ser mayor a 0")
        
        if self.parametro_id <= 0:
            raise InvalidFeedbackDataError("El ID de parámetro debe ser mayor a 0")
        
        if self.comentario is not None and len(self.comentario.strip()) == 0:
            raise InvalidFeedbackDataError("El comentario no puede estar vacío si se proporciona")
    
    def is_automatic(self) -> bool:
        """Determina si el feedback fue generado automáticamente."""
        return not self.es_manual
    
    def is_high_performance(self) -> bool:
        """Determina si el feedback indica alto rendimiento."""
        return self.score.is_high()
    
    def is_low_performance(self) -> bool:
        """Determina si el feedback indica bajo rendimiento."""
        return self.score.is_low()
    
    def get_performance_level(self) -> str:
        """Obtiene el nivel de rendimiento basado en el score."""
        return self.score.get_performance_level()
    
    def update_score(self, new_value: float) -> None:
        """Actualiza el score del feedback con validación."""
        self.score = FeedbackScore(new_value)
        self.updated_at = datetime.utcnow()
    
    def add_comentario(self, comentario: str) -> None:
        """Añade o actualiza el comentario del feedback."""
        if not comentario or len(comentario.strip()) == 0:
            raise InvalidFeedbackDataError("El comentario no puede estar vacío")
        
        self.comentario = comentario.strip()
        self.updated_at = datetime.utcnow()
    
    def mark_as_manual(self) -> None:
        """Marca el feedback como manual."""
        self.es_manual = True
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización."""
        return {
            'id': self.id,
            'grabacion_id': self.grabacion_id,
            'parametro_id': self.parametro_id,
            'valor': self.score.value,
            'comentario': self.comentario,
            'es_manual': self.es_manual,
            'performance_level': self.get_performance_level(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create_automatic_feedback(
        cls,
        grabacion_id: int,
        parametro_id: int,
        score_value: float,
        comentario: Optional[str] = None
    ) -> 'Feedback':
        """Factory method para crear feedback automático."""
        return cls(
            id=None,
            grabacion_id=grabacion_id,
            parametro_id=parametro_id,
            score=FeedbackScore(score_value),
            comentario=comentario,
            es_manual=False,
        )
    
    @classmethod
    def create_manual_feedback(
        cls,
        grabacion_id: int,
        parametro_id: int,
        score_value: float,
        comentario: str
    ) -> 'Feedback':
        """Factory method para crear feedback manual."""
        return cls(
            id=None,
            grabacion_id=grabacion_id,
            parametro_id=parametro_id,
            score=FeedbackScore(score_value),
            comentario=comentario,
            es_manual=True,
        )
