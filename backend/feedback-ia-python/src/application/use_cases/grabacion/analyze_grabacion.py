# filepath: /src/application/use_cases/grabacion/analyze_grabacion.py
from typing import Dict, Any

from ...domain.entities.grabacion import Grabacion
from ...domain.repositories.grabacion_repository import GrabacionRepositoryInterface
from ...domain.services.audio_analyzer_service import AudioAnalyzerService, AudioAnalysisResult
from ...infrastructure.exceptions.repository_exceptions import EntityNotFoundError
from ...domain.exceptions.validation_exceptions import DomainValidationError
from ..dtos.grabacion_dto import GrabacionAnalysisResponseDTO


class AnalyzeGrabacionUseCase:
    """
    Caso de uso para analizar una grabación existente.
    
    Este caso de uso orquesta el análisis completo de grabaciones,
    incluyendo extracción de métricas y evaluación de calidad.
    """
    
    def __init__(
        self, 
        grabacion_repository: GrabacionRepositoryInterface,
        audio_analyzer_service: AudioAnalyzerService
    ):
        self._repository = grabacion_repository
        self._audio_analyzer = audio_analyzer_service
    
    async def execute(self, grabacion_id: int) -> GrabacionAnalysisResponseDTO:
        """
        Ejecuta el análisis completo de una grabación.
        
        Args:
            grabacion_id: ID de la grabación a analizar
            
        Returns:
            GrabacionAnalysisResponseDTO con los resultados del análisis
            
        Raises:
            EntityNotFoundError: Si la grabación no existe
            DomainValidationError: Si la grabación no puede ser analizada
        """
        # Obtener la grabación
        grabacion = await self._repository.get_by_id(grabacion_id)
        if not grabacion:
            raise EntityNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
        
        # Verificar que puede ser analizada
        if not self._audio_analyzer.is_grabacion_analyzable(grabacion):
            recomendaciones = self._audio_analyzer.recommend_preprocessing_steps(grabacion)
            raise DomainValidationError(
                f"La grabación no puede ser analizada. Recomendaciones: {', '.join(recomendaciones)}"
            )
        
        # Realizar el análisis
        try:
            analysis_result = self._audio_analyzer.analyze_grabacion(grabacion)
        except Exception as e:
            raise DomainValidationError(f"Error durante el análisis: {str(e)}")
        
        # Obtener estimaciones de costo
        costo_estimado = self._audio_analyzer.estimate_processing_cost(grabacion)
        
        # Obtener recomendaciones adicionales
        recomendaciones = self._audio_analyzer.recommend_preprocessing_steps(grabacion)
        
        # Crear el DTO de respuesta
        return GrabacionAnalysisResponseDTO(
            grabacion_id=grabacion.id,
            duracion_segundos=analysis_result.duracion_segundos,
            formato_detectado=analysis_result.formato_detectado,
            calidad_audio=analysis_result.calidad_audio,
            metricas_extraidas=analysis_result.metricas_extraidas,
            problemas_detectados=analysis_result.problemas_detectados,
            confiabilidad_analisis=analysis_result.confiabilidad_analisis,
            puede_analisis_avanzado=self._audio_analyzer.can_extract_advanced_metrics(grabacion),
            recomendaciones_preproceso=recomendaciones,
            estimacion_costo=costo_estimado,
            info_archivo=grabacion.get_info_archivo()
        )
    
    async def get_preprocessing_recommendations(self, grabacion_id: int) -> Dict[str, Any]:
        """
        Obtiene recomendaciones de preprocesamiento para una grabación.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Diccionario con recomendaciones detalladas
            
        Raises:
            EntityNotFoundError: Si la grabación no existe
        """
        # Obtener la grabación
        grabacion = await self._repository.get_by_id(grabacion_id)
        if not grabacion:
            raise EntityNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
        
        # Generar recomendaciones
        recomendaciones = self._audio_analyzer.recommend_preprocessing_steps(grabacion)
        costo_estimado = self._audio_analyzer.estimate_processing_cost(grabacion)
        
        return {
            "grabacion_id": grabacion_id,
            "es_analizable": self._audio_analyzer.is_grabacion_analyzable(grabacion),
            "permite_analisis_avanzado": self._audio_analyzer.can_extract_advanced_metrics(grabacion),
            "recomendaciones": recomendaciones,
            "estimacion_procesamiento": costo_estimado,
            "requiere_conversion": grabacion.requires_conversion(),
            "formato_actual": grabacion.archivo_audio.formato or "desconocido",
            "duracion_minutos": grabacion.get_duracion_minutos(),
            "info_archivo": grabacion.get_info_archivo()
        }
    
    async def validate_for_analysis(self, grabacion_id: int) -> Dict[str, Any]:
        """
        Valida si una grabación está lista para análisis.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Diccionario con información de validación
            
        Raises:
            EntityNotFoundError: Si la grabación no existe
        """
        # Obtener la grabación
        grabacion = await self._repository.get_by_id(grabacion_id)
        if not grabacion:
            raise EntityNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
        
        # Realizar validaciones
        es_valida = grabacion.is_archivo_valido()
        es_analizable = self._audio_analyzer.is_grabacion_analyzable(grabacion)
        permite_avanzado = self._audio_analyzer.can_extract_advanced_metrics(grabacion)
        
        # Identificar problemas
        problemas = []
        if not es_valida:
            problemas.append("Archivo no válido para procesamiento")
        if not es_analizable:
            problemas.append("No cumple requisitos mínimos para análisis")
        
        # Obtener recomendaciones
        recomendaciones = self._audio_analyzer.recommend_preprocessing_steps(grabacion)
        
        return {
            "grabacion_id": grabacion_id,
            "es_archivo_valido": es_valida,
            "es_analizable": es_analizable,
            "permite_analisis_avanzado": permite_avanzado,
            "problemas_detectados": problemas,
            "recomendaciones": recomendaciones,
            "estado_general": "válido" if es_analizable else "requiere_preproceso"
        }
