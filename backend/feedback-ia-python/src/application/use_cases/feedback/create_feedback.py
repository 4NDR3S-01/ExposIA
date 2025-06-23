"""
Caso de uso para crear un nuevo feedback.
Orquesta la lógica de negocio para la creación de feedbacks.
"""
from typing import Optional

from ...domain.entities.feedback import Feedback
from ...domain.repositories.feedback_repository import FeedbackRepositoryInterface
from ...domain.exceptions.validation_exceptions import DuplicateFeedbackError
from ..dtos.feedback_dto import CreateFeedbackDTO, FeedbackResponseDTO


class CreateFeedbackUseCase:
    """
    Caso de uso para crear un nuevo feedback.
    
    Orquesta la creación de feedback validando reglas de negocio
    y coordinando entre repositorios y servicios.
    """
    
    def __init__(
        self,
        feedback_repository: FeedbackRepositoryInterface,
        grabacion_repository: "GrabacionRepositoryInterface",
        parametro_repository: "ParametroRepositoryInterface"
    ):
        self._feedback_repository = feedback_repository
        self._grabacion_repository = grabacion_repository
        self._parametro_repository = parametro_repository
    
    async def execute(self, dto: CreateFeedbackDTO) -> FeedbackResponseDTO:
        """
        Ejecuta la creación de un nuevo feedback.
        
        Args:
            dto: Datos para crear el feedback
            
        Returns:
            DTO con los datos del feedback creado
            
        Raises:
            ValidationException: Si los datos no son válidos
            GrabacionNotFoundError: Si la grabación no existe
            ParametroNotFoundError: Si el parámetro no existe
            DuplicateFeedbackError: Si ya existe feedback para esta combinación
        """
        # Validar DTO
        dto.validate()
        
        # Verificar que la grabación existe
        grabacion = await self._grabacion_repository.get_by_id(dto.grabacion_id)
        if not grabacion:
            raise GrabacionNotFoundError(f"Grabación con ID {dto.grabacion_id} no encontrada")
        
        # Verificar que el parámetro existe
        parametro = await self._parametro_repository.get_by_id(dto.parametro_id)
        if not parametro:
            raise ParametroNotFoundError(f"Parámetro con ID {dto.parametro_id} no encontrado")
        
        # Verificar que no existe feedback duplicado
        existing_feedbacks = await self._feedback_repository.get_by_grabacion_and_parametro(
            dto.grabacion_id, dto.parametro_id
        )
        if existing_feedbacks and not dto.es_manual:
            raise DuplicateFeedbackError(
                f"Ya existe feedback automático para grabación {dto.grabacion_id} y parámetro {dto.parametro_id}"
            )
        
        # Crear entidad de dominio
        feedback = Feedback.create_new(
            grabacion_id=dto.grabacion_id,
            parametro_id=dto.parametro_id,
            valor=dto.valor,
            comentario=dto.comentario,
            es_manual=dto.es_manual
        )
        
        # Persistir en repositorio
        created_feedback = await self._feedback_repository.create(feedback)
        
        # Retornar DTO de respuesta
        return FeedbackResponseDTO.from_entity(created_feedback)
    """
    Caso de uso para crear un nuevo feedback.
    
    Responsabilidades:
    - Validar que no exista un feedback duplicado
    - Crear la entidad de dominio
    - Persistir el feedback
    - Retornar el resultado
    
    Principios aplicados:
    - Single Responsibility: Solo se encarga de crear feedbacks
    - Dependency Inversion: Depende de interfaces, no de implementaciones
    """
    
    def __init__(self, feedback_repository: FeedbackRepositoryInterface):
        self._feedback_repository = feedback_repository
    
    async def execute(self, create_dto: CreateFeedbackDTO) -> FeedbackResponseDTO:
        """
        Ejecuta el caso de uso de creación de feedback.
        
        Args:
            create_dto: DTO con los datos para crear el feedback
            
        Returns:
            FeedbackResponseDTO con el feedback creado
            
        Raises:
            DuplicateFeedbackError: Si ya existe un feedback para la grabación y parámetro
            InvalidFeedbackDataError: Si los datos son inválidos
        """
        # Verificar si ya existe un feedback para esta grabación y parámetro
        await self._validate_no_duplicate_feedback(
            create_dto.grabacion_id, 
            create_dto.parametro_id
        )
        
        # Crear la entidad de dominio
        feedback = self._create_feedback_entity(create_dto)
        
        # Persistir el feedback
        created_feedback = await self._feedback_repository.create(feedback)
        
        # Retornar el DTO de respuesta
        return FeedbackResponseDTO.from_entity(created_feedback)
    
    async def _validate_no_duplicate_feedback(
        self, 
        grabacion_id: int, 
        parametro_id: int
    ) -> None:
        """Valida que no exista un feedback duplicado."""
        exists = await self._feedback_repository.exists_by_grabacion_and_parametro(
            grabacion_id, parametro_id
        )
        
        if exists:
            raise DuplicateFeedbackError(grabacion_id, parametro_id)
    
    def _create_feedback_entity(self, create_dto: CreateFeedbackDTO) -> Feedback:
        """Crea la entidad de feedback basada en el DTO."""
        if create_dto.es_manual:
            return Feedback.create_manual_feedback(
                grabacion_id=create_dto.grabacion_id,
                parametro_id=create_dto.parametro_id,
                score_value=create_dto.valor,
                comentario=create_dto.comentario or ""
            )
        else:
            return Feedback.create_automatic_feedback(
                grabacion_id=create_dto.grabacion_id,
                parametro_id=create_dto.parametro_id,
                score_value=create_dto.valor,
                comentario=create_dto.comentario
            )
