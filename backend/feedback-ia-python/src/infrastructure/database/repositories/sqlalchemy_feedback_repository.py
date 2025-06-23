"""
Implementación concreta del repositorio de Feedback usando SQLAlchemy.
Esta implementación pertenece a la capa de infraestructura.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from ...domain.entities.feedback import Feedback
from ...domain.repositories.feedback_repository import FeedbackRepositoryInterface
from ...domain.value_objects.feedback_score import FeedbackScore
from ...domain.exceptions.validation_exceptions import (
    FeedbackNotFoundError,
    DuplicateFeedbackError
)
from ..models.feedback_model import FeedbackModel


class SQLAlchemyFeedbackRepository(FeedbackRepositoryInterface):
    """
    Implementación concreta del repositorio de Feedback usando SQLAlchemy.
    
    Esta clase implementa la interfaz definida en el dominio y maneja
    la persistencia específica usando SQLAlchemy como ORM.
    
    Responsabilidades:
    - Convertir entre entidades de dominio y modelos de SQLAlchemy
    - Implementar todas las operaciones de persistencia
    - Manejar errores de base de datos
    - Mantener la integridad de los datos
    """
    
    def __init__(self, db_session: Session):
        self._db = db_session
    
    async def create(self, feedback: Feedback) -> Feedback:
        """Crea un nuevo feedback en la base de datos."""
        # Verificar duplicados
        existing = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == feedback.grabacion_id,
                FeedbackModel.parametro_id == feedback.parametro_id
            )
        ).first()
        
        if existing:
            raise DuplicateFeedbackError(feedback.grabacion_id, feedback.parametro_id)
        
        # Convertir entidad a modelo SQLAlchemy
        db_feedback = self._entity_to_model(feedback)
        
        # Persistir
        self._db.add(db_feedback)
        self._db.commit()
        self._db.refresh(db_feedback)
        
        # Convertir de vuelta a entidad
        return self._model_to_entity(db_feedback)
    
    async def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """Obtiene un feedback por su ID."""
        db_feedback = self._db.query(FeedbackModel).filter(
            FeedbackModel.id == feedback_id
        ).first()
        
        if db_feedback:
            return self._model_to_entity(db_feedback)
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """Obtiene todos los feedbacks con paginación."""
        db_feedbacks = self._db.query(FeedbackModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def get_by_grabacion_id(self, grabacion_id: int) -> List[Feedback]:
        """Obtiene todos los feedbacks de una grabación."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            FeedbackModel.grabacion_id == grabacion_id
        ).all()
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def get_by_parametro_id(self, parametro_id: int) -> List[Feedback]:
        """Obtiene todos los feedbacks de un parámetro específico."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            FeedbackModel.parametro_id == parametro_id
        ).all()
        
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def get_automatic_feedbacks(self, grabacion_id: int) -> List[Feedback]:
        """Obtiene todos los feedbacks automáticos de una grabación."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == grabacion_id,
                FeedbackModel.es_manual == False
            )
        ).all()
        
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def get_manual_feedbacks(self, grabacion_id: int) -> List[Feedback]:
        """Obtiene todos los feedbacks manuales de una grabación."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == grabacion_id,
                FeedbackModel.es_manual == True
            )
        ).all()
        
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def update(self, feedback: Feedback) -> Feedback:
        """Actualiza un feedback existente."""
        db_feedback = self._db.query(FeedbackModel).filter(
            FeedbackModel.id == feedback.id
        ).first()
        
        if not db_feedback:
            raise FeedbackNotFoundError(feedback.id)
        
        # Actualizar campos
        db_feedback.valor = feedback.score.value
        db_feedback.comentario = feedback.comentario
        db_feedback.es_manual = feedback.es_manual
        db_feedback.updated_at = feedback.updated_at
        
        self._db.commit()
        self._db.refresh(db_feedback)
        
        return self._model_to_entity(db_feedback)
    
    async def delete(self, feedback_id: int) -> bool:
        """Elimina un feedback por su ID."""
        db_feedback = self._db.query(FeedbackModel).filter(
            FeedbackModel.id == feedback_id
        ).first()
        
        if db_feedback:
            self._db.delete(db_feedback)
            self._db.commit()
            return True
        return False
    
    async def exists_by_grabacion_and_parametro(
        self, 
        grabacion_id: int, 
        parametro_id: int
    ) -> bool:
        """Verifica si existe un feedback para grabación y parámetro específicos."""
        exists = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == grabacion_id,
                FeedbackModel.parametro_id == parametro_id
            )
        ).first() is not None
        return exists
    
    async def get_by_grabacion_and_parametro(
        self, 
        grabacion_id: int, 
        parametro_id: int
    ) -> Optional[Feedback]:
        """Obtiene feedback específico por grabación y parámetro."""
        db_feedback = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == grabacion_id,
                FeedbackModel.parametro_id == parametro_id
            )
        ).first()
        
        if db_feedback:
            return self._model_to_entity(db_feedback)
        return None
    
    async def get_feedbacks_with_low_scores(
        self, 
        threshold: float = 40.0,
        skip: int = 0,
        limit: int = 100
    ) -> List[Feedback]:
        """Obtiene feedbacks con puntajes bajos."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            FeedbackModel.valor <= threshold
        ).offset(skip).limit(limit).all()
        
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    async def get_average_score_by_grabacion(self, grabacion_id: int) -> Optional[float]:
        """Calcula el puntaje promedio de una grabación."""
        result = self._db.query(func.avg(FeedbackModel.valor)).filter(
            FeedbackModel.grabacion_id == grabacion_id
        ).scalar()
        
        return float(result) if result is not None else None
    
    async def count_by_grabacion(self, grabacion_id: int) -> int:
        """Cuenta el número de feedbacks de una grabación."""
        return self._db.query(FeedbackModel).filter(
            FeedbackModel.grabacion_id == grabacion_id
        ).count()
    
    async def get_feedbacks_by_score_range(
        self, 
        grabacion_id: int, 
        min_score: float, 
        max_score: float
    ) -> List[Feedback]:
        """Obtiene feedbacks dentro de un rango de scores específico."""
        db_feedbacks = self._db.query(FeedbackModel).filter(
            and_(
                FeedbackModel.grabacion_id == grabacion_id,
                FeedbackModel.valor >= min_score,
                FeedbackModel.valor <= max_score
            )
        ).all()
        
        return [self._model_to_entity(db_feedback) for db_feedback in db_feedbacks]
    
    def _entity_to_model(self, feedback: Feedback) -> FeedbackModel:
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        return FeedbackModel(
            id=feedback.id,
            grabacion_id=feedback.grabacion_id,
            parametro_id=feedback.parametro_id,
            valor=feedback.score.value,
            comentario=feedback.comentario,
            es_manual=feedback.es_manual,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at
        )
    
    def _model_to_entity(self, db_feedback: FeedbackModel) -> Feedback:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        return Feedback(
            id=db_feedback.id,
            grabacion_id=db_feedback.grabacion_id,
            parametro_id=db_feedback.parametro_id,
            score=FeedbackScore(db_feedback.valor),
            comentario=db_feedback.comentario,
            es_manual=db_feedback.es_manual,
            created_at=db_feedback.created_at,
            updated_at=db_feedback.updated_at
        )
