# filepath: /src/application/use_cases/grabacion/create_grabacion.py
from datetime import datetime
from typing import Optional

from ...domain.entities.grabacion import Grabacion
from ...domain.value_objects.archivo_audio import ArchivoAudio
from ...domain.repositories.grabacion_repository import GrabacionRepositoryInterface
from ...domain.services.audio_analyzer_service import AudioAnalyzerService
from ...domain.exceptions.validation_exceptions import DomainValidationError
from ...infrastructure.exceptions.repository_exceptions import RepositoryError
from ..dtos.grabacion_dto import CreateGrabacionDTO, GrabacionResponseDTO


class CreateGrabacionUseCase:
    """
    Caso de uso para crear una nueva grabación.
    
    Este caso de uso orquesta la creación de grabaciones,
    incluyendo validaciones de archivo, análisis básico y persistencia.
    """
    
    def __init__(
        self, 
        grabacion_repository: GrabacionRepositoryInterface,
        audio_analyzer_service: AudioAnalyzerService
    ):
        self._repository = grabacion_repository
        self._audio_analyzer = audio_analyzer_service
    
    async def execute(self, dto: CreateGrabacionDTO) -> GrabacionResponseDTO:
        """
        Ejecuta el caso de uso de creación de grabación.
        
        Args:
            dto: DTO con los datos para crear la grabación
            
        Returns:
            GrabacionResponseDTO con la grabación creada
            
        Raises:
            DomainValidationError: Si los datos no son válidos
            RepositoryError: Si ocurre un error en la persistencia
        """
        # Verificar que la ruta del archivo no esté en uso
        if await self._repository.exists_by_ruta_archivo(dto.ruta_archivo):
            raise DomainValidationError(f"Ya existe una grabación con la ruta '{dto.ruta_archivo}'")
        
        # Crear el value object del archivo de audio
        try:
            archivo_audio = ArchivoAudio(
                nombre_archivo=dto.nombre_archivo,
                ruta_archivo=dto.ruta_archivo,
                formato=dto.formato,
                duracion=dto.duracion
            )
        except DomainValidationError as e:
            raise e
        
        # Crear la entidad de dominio
        try:
            grabacion = Grabacion(
                id=None,
                archivo_audio=archivo_audio,
                fecha_grabacion=dto.fecha_grabacion
            )
        except DomainValidationError as e:
            raise e
        
        # Validar que la grabación puede ser analizada
        if not self._audio_analyzer.is_grabacion_analyzable(grabacion):
            recomendaciones = self._audio_analyzer.recommend_preprocessing_steps(grabacion)
            raise DomainValidationError(
                f"La grabación no es válida para análisis. Recomendaciones: {', '.join(recomendaciones)}"
            )
        
        # Persistir en el repositorio
        try:
            grabacion_creada = await self._repository.create(grabacion)
        except RepositoryError as e:
            raise e
        
        # Convertir a DTO de respuesta
        response_dto = GrabacionResponseDTO.from_entity(grabacion_creada)
        
        # Agregar información de análisis básico
        if self._audio_analyzer.can_extract_advanced_metrics(grabacion_creada):
            response_dto.puede_analisis_avanzado = True
            response_dto.recomendaciones_preproceso = []
        else:
            response_dto.puede_analisis_avanzado = False
            response_dto.recomendaciones_preproceso = self._audio_analyzer.recommend_preprocessing_steps(grabacion_creada)
        
        return response_dto
