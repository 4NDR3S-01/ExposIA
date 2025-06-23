"""
Caso de uso para generar feedback automático usando IA.
Orquesta el análisis de audio y generación de feedback inteligente.
"""
from typing import List

from ...domain.entities.feedback import Feedback
from ...domain.repositories.feedback_repository import FeedbackRepositoryInterface
from ...domain.services.feedback_analyzer import FeedbackAnalyzerService
from ...domain.exceptions.validation_exceptions import (
    GrabacionNotFoundError,
    ParametroNotFoundError,
    AIServiceError
)
from ..interfaces.ai_service_interface import AIServiceInterface
from ..dtos.feedback_dto import GenerateAIFeedbackDTO, FeedbackResponseDTO


class GenerateAIFeedbackUseCase:
    """
    Caso de uso para generar feedback automático con IA.
    
    Responsabilidades:
    - Validar la existencia de grabación y parámetros
    - Analizar el audio con IA
    - Generar feedbacks para cada parámetro
    - Persistir los feedbacks generados
    
    Principios aplicados:
    - Single Responsibility: Solo se encarga de generar feedback con IA
    - Dependency Inversion: Depende de interfaces de servicios
    - Open/Closed: Fácil de extender con nuevos modelos de IA
    """
    
    def __init__(
        self,
        feedback_repository: FeedbackRepositoryInterface,
        ai_service: AIServiceInterface,
        feedback_analyzer: FeedbackAnalyzerService
    ):
        self._feedback_repository = feedback_repository
        self._ai_service = ai_service
        self._feedback_analyzer = feedback_analyzer
    
    async def execute(self, generate_dto: GenerateAIFeedbackDTO) -> List[FeedbackResponseDTO]:
        """
        Ejecuta la generación de feedback con IA.
        
        Args:
            generate_dto: DTO con los datos para generar feedback
            
        Returns:
            Lista de FeedbackResponseDTO generados
            
        Raises:
            GrabacionNotFoundError: Si la grabación no existe
            ParametroNotFoundError: Si algún parámetro no existe
            AIServiceError: Si falla el servicio de IA
        """
        # Validar entrada
        generate_dto.validate()
        
        # Analizar audio con IA
        ai_analysis = await self._analyze_audio_with_ai(
            generate_dto.grabacion_id,
            generate_dto.audio_analysis_data,
            generate_dto.use_advanced_model
        )
        
        # Generar feedbacks para cada parámetro
        feedbacks = await self._generate_feedbacks_for_parameters(
            generate_dto.grabacion_id,
            generate_dto.parametros_ids,
            ai_analysis
        )
        
        # Persistir los feedbacks
        created_feedbacks = await self._persist_feedbacks(feedbacks)
        
        # Retornar DTOs de respuesta
        return [
            FeedbackResponseDTO.from_entity(feedback) 
            for feedback in created_feedbacks
        ]
    
    async def _analyze_audio_with_ai(
        self,
        grabacion_id: int,
        audio_data: dict,
        use_advanced_model: bool
    ) -> dict:
        """Analiza el audio usando servicios de IA."""
        try:
            if use_advanced_model:
                return await self._ai_service.analyze_audio_advanced(
                    grabacion_id, audio_data
                )
            else:
                return await self._ai_service.analyze_audio_basic(
                    grabacion_id, audio_data
                )
        except Exception as e:
            raise AIServiceError(f"Error en análisis de IA: {str(e)}")
    
    async def _generate_feedbacks_for_parameters(
        self,
        grabacion_id: int,
        parametros_ids: List[int],
        ai_analysis: dict
    ) -> List[Feedback]:
        """Genera feedbacks para cada parámetro basado en el análisis de IA."""
        feedbacks = []
        
        for parametro_id in parametros_ids:
            # Verificar que no exista ya un feedback para este parámetro
            existing_feedback = await self._feedback_repository.get_by_grabacion_and_parametro(
                grabacion_id, parametro_id
            )
            
            if existing_feedback is None:
                # Calcular puntaje usando el analizador de feedback
                score = await self._feedback_analyzer.calculate_score_for_parameter(
                    parametro_id, ai_analysis
                )
                
                # Generar comentario automático
                comentario = await self._feedback_analyzer.generate_comment_for_parameter(
                    parametro_id, ai_analysis, score
                )
                
                # Crear feedback automático
                feedback = Feedback.create_automatic_feedback(
                    grabacion_id=grabacion_id,
                    parametro_id=parametro_id,
                    score_value=score,
                    comentario=comentario
                )
                
                feedbacks.append(feedback)
        
        return feedbacks
    
    async def _persist_feedbacks(self, feedbacks: List[Feedback]) -> List[Feedback]:
        """Persiste todos los feedbacks generados."""
        created_feedbacks = []
        
        for feedback in feedbacks:
            try:
                created_feedback = await self._feedback_repository.create(feedback)
                created_feedbacks.append(created_feedback)
            except Exception as e:
                # Log el error pero continúa con los otros feedbacks
                print(f"Error al crear feedback: {str(e)}")
                continue
        
        return created_feedbacks
