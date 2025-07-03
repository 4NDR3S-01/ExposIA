"""
Interface para servicios de IA.
Define el contrato para servicios externos de inteligencia artificial.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class AIServiceInterface(ABC):
    """
    Interface que define las operaciones de servicios de IA.
    
    Esta interfaz pertenece a la capa de aplicación y define el contrato
    que deben implementar los servicios de IA en la capa de infraestructura.
    
    Principios aplicados:
    - Dependency Inversion: La aplicación define la interfaz, la infraestructura la implementa
    - Interface Segregation: Interfaz específica para operaciones de IA
    """
    
    @abstractmethod
    async def analyze_audio_basic(
        self, 
        grabacion_id: int, 
        audio_data: Dict
    ) -> Dict:
        """
        Realiza análisis básico de audio usando IA.
        
        Args:
            grabacion_id: ID de la grabación a analizar
            audio_data: Datos del archivo de audio
            
        Returns:
            Diccionario con métricas de análisis básico
            
        Raises:
            AIServiceError: Si ocurre un error en el análisis
        """
        pass
    
    @abstractmethod
    async def analyze_audio_advanced(
        self, 
        grabacion_id: int, 
        audio_data: Dict
    ) -> Dict:
        """
        Realiza análisis avanzado de audio usando IA.
        
        Args:
            grabacion_id: ID de la grabación a analizar
            audio_data: Datos del archivo de audio
            
        Returns:
            Diccionario con métricas de análisis avanzado
            
        Raises:
            AIServiceError: Si ocurre un error en el análisis
        """
        pass
    
    @abstractmethod
    async def generate_feedback_comment(
        self,
        analysis_results: Dict,
        parametro_type: str,
        score: float
    ) -> str:
        """
        Genera un comentario de feedback usando IA.
        
        Args:
            analysis_results: Resultados del análisis de audio
            parametro_type: Tipo de parámetro siendo evaluado
            score: Puntaje calculado
            
        Returns:
            Comentario generado por IA
            
        Raises:
            AIServiceError: Si ocurre un error en la generación
        """
        pass
    
    @abstractmethod
    async def extract_speech_metrics(
        self, 
        audio_file_path: str
    ) -> Dict:
        """
        Extrae métricas de habla del archivo de audio.
        
        Args:
            audio_file_path: Ruta al archivo de audio
            
        Returns:
            Diccionario con métricas extraídas:
            - speech_rate: Velocidad de habla (palabras por minuto)
            - pause_patterns: Patrones de pausas
            - volume_consistency: Consistencia del volumen
            - clarity_score: Puntaje de claridad
            - intonation_variety: Variedad de entonación
            
        Raises:
            AIServiceError: Si ocurre un error en la extracción
        """
        pass
    
    @abstractmethod
    async def detect_emotions(
        self, 
        audio_file_path: str
    ) -> Dict:
        """
        Detecta emociones en el audio.
        
        Args:
            audio_file_path: Ruta al archivo de audio
            
        Returns:
            Diccionario con emociones detectadas y sus intensidades
            
        Raises:
            AIServiceError: Si ocurre un error en la detección
        """
        pass
    
    @abstractmethod
    async def transcribe_audio(
        self, 
        audio_file_path: str,
        language: str = "es"
    ) -> Dict:
        """
        Transcribe el audio a texto.
        
        Args:
            audio_file_path: Ruta al archivo de audio
            language: Idioma para la transcripción
            
        Returns:
            Diccionario con transcripción y metadatos
            
        Raises:
            AIServiceError: Si ocurre un error en la transcripción
        """
        pass
    
    @abstractmethod
    async def analyze_presentation_structure(
        self, 
        transcript: str
    ) -> Dict:
        """
        Analiza la estructura de una presentación basada en la transcripción.
        
        Args:
            transcript: Texto transcrito de la presentación
            
        Returns:
            Diccionario con análisis de estructura:
            - introduction_quality: Calidad de la introducción
            - conclusion_quality: Calidad de la conclusión
            - content_organization: Organización del contenido
            - transition_quality: Calidad de las transiciones
            
        Raises:
            AIServiceError: Si ocurre un error en el análisis
        """
        pass
    
    @abstractmethod
    async def get_improvement_suggestions(
        self,
        analysis_results: Dict,
        weak_areas: List[str]
    ) -> List[str]:
        """
        Genera sugerencias de mejora basadas en el análisis.
        
        Args:
            analysis_results: Resultados completos del análisis
            weak_areas: Áreas que necesitan mejora
            
        Returns:
            Lista de sugerencias específicas de mejora
            
        Raises:
            AIServiceError: Si ocurre un error en la generación
        """
        pass
    
    @abstractmethod
    async def compare_with_benchmarks(
        self,
        analysis_results: Dict,
        presentation_type: str
    ) -> Dict:
        """
        Compara los resultados con benchmarks establecidos.
        
        Args:
            analysis_results: Resultados del análisis
            presentation_type: Tipo de presentación (académica, corporativa, etc.)
            
        Returns:
            Diccionario con comparación contra benchmarks
            
        Raises:
            AIServiceError: Si ocurre un error en la comparación
        """
        pass
