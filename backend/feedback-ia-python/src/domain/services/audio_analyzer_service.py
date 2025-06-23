# filepath: /src/domain/services/audio_analyzer_service.py
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ..entities.grabacion import Grabacion
from ..entities.parametro import Parametro
from ..value_objects.archivo_audio import ArchivoAudio
from ..exceptions.validation_exceptions import DomainValidationError


@dataclass
class AudioAnalysisResult:
    """
    Resultado del análisis de audio que contiene métricas extraídas.
    """
    duracion_segundos: float
    formato_detectado: str
    calidad_audio: str  # 'alta', 'media', 'baja'
    metricas_extraidas: Dict[str, float]
    problemas_detectados: List[str]
    confiabilidad_analisis: float  # 0.0 a 1.0


class AudioAnalyzerService:
    """
    Servicio de dominio para análisis de archivos de audio.
    
    Este servicio encapsula la lógica de negocio compleja relacionada con
    el análisis de grabaciones de audio y extracción de métricas.
    """
    
    # Umbrales de calidad de audio
    CALIDAD_ALTA_BITRATE = 256  # kbps
    CALIDAD_MEDIA_BITRATE = 128  # kbps
    
    # Duración mínima y máxima para análisis válido
    DURACION_MINIMA_SEGUNDOS = 1.0
    DURACION_MAXIMA_SEGUNDOS = 7200.0  # 2 horas
    
    def analyze_grabacion(self, grabacion: Grabacion) -> AudioAnalysisResult:
        """
        Realiza un análisis completo de una grabación.
        
        Args:
            grabacion: Entidad Grabacion a analizar
            
        Returns:
            AudioAnalysisResult con los resultados del análisis
            
        Raises:
            DomainValidationError: Si la grabación no es válida para análisis
        """
        if not self.is_grabacion_analyzable(grabacion):
            raise DomainValidationError("La grabación no es válida para análisis")
        
        # Análisis básico del archivo
        problemas = self._detect_audio_problems(grabacion.archivo_audio)
        calidad = self._determine_audio_quality(grabacion.archivo_audio)
        
        # Extracción de métricas básicas
        metricas_basicas = self._extract_basic_metrics(grabacion.archivo_audio)
        
        # Calcular confiabilidad basada en calidad y problemas
        confiabilidad = self._calculate_analysis_reliability(calidad, problemas)
        
        return AudioAnalysisResult(
            duracion_segundos=grabacion.archivo_audio.duracion or 0.0,
            formato_detectado=grabacion.archivo_audio.formato or "desconocido",
            calidad_audio=calidad,
            metricas_extraidas=metricas_basicas,
            problemas_detectados=problemas,
            confiabilidad_analisis=confiabilidad
        )
    
    def is_grabacion_analyzable(self, grabacion: Grabacion) -> bool:
        """
        Determina si una grabación puede ser analizada.
        
        Args:
            grabacion: Grabación a evaluar
            
        Returns:
            True si puede ser analizada, False en caso contrario
        """
        archivo = grabacion.archivo_audio
        
        # Verificar formato válido
        if not archivo.es_formato_valido:
            return False
        
        # Verificar duración
        if archivo.duracion is None:
            return False
        
        if (archivo.duracion < self.DURACION_MINIMA_SEGUNDOS or 
            archivo.duracion > self.DURACION_MAXIMA_SEGUNDOS):
            return False
        
        return True
    
    def can_extract_advanced_metrics(self, grabacion: Grabacion) -> bool:
        """
        Determina si se pueden extraer métricas avanzadas de la grabación.
        
        Args:
            grabacion: Grabación a evaluar
            
        Returns:
            True si permite análisis avanzado
        """
        if not self.is_grabacion_analyzable(grabacion):
            return False
        
        archivo = grabacion.archivo_audio
        
        # Requiere duración mínima para análisis avanzado
        if archivo.duracion and archivo.duracion < 5.0:
            return False
        
        # Preferir formatos sin compresión para análisis avanzado
        if archivo.es_formato_valido and not grabacion.is_formato_comprimido():
            return True
        
        # Los formatos comprimidos también pueden analizarse pero con menor precisión
        return True
    
    def recommend_preprocessing_steps(self, grabacion: Grabacion) -> List[str]:
        """
        Recomienda pasos de preprocesamiento para mejorar el análisis.
        
        Args:
            grabacion: Grabación a evaluar
            
        Returns:
            Lista de recomendaciones de preprocesamiento
        """
        recomendaciones = []
        archivo = grabacion.archivo_audio
        
        # Conversión de formato si es necesario
        if grabacion.requires_conversion():
            recomendaciones.append("Convertir a formato WAV para mejor análisis")
        
        # Verificar duración
        if archivo.duracion and archivo.es_archivo_largo(1800):  # 30 minutos
            recomendaciones.append("Considerar segmentar archivo largo en partes más pequeñas")
        
        if archivo.duracion and archivo.es_archivo_corto(3.0):
            recomendaciones.append("Archivo muy corto, resultados pueden ser limitados")
        
        # Calidad de audio
        calidad = self._determine_audio_quality(archivo)
        if calidad == "baja":
            recomendaciones.append("Mejorar calidad de audio para análisis más preciso")
        
        return recomendaciones
    
    def estimate_processing_cost(self, grabacion: Grabacion) -> Dict[str, float]:
        """
        Estima el costo computacional del procesamiento.
        
        Args:
            grabacion: Grabación a evaluar
            
        Returns:
            Diccionario con estimaciones de costo
        """
        archivo = grabacion.archivo_audio
        duracion = archivo.duracion or 0.0
        
        # Factores de costo basados en características del archivo
        factor_duracion = min(duracion / 60, 10.0)  # Máximo factor de 10
        factor_formato = 1.5 if grabacion.is_formato_comprimido() else 1.0
        factor_calidad = {
            "alta": 1.2,
            "media": 1.0, 
            "baja": 0.8
        }.get(self._determine_audio_quality(archivo), 1.0)
        
        costo_base = factor_duracion * factor_formato * factor_calidad
        
        return {
            "tiempo_estimado_segundos": costo_base * 2,  # Aprox 2 segundos por unidad
            "memoria_estimada_mb": costo_base * 50,  # Aprox 50MB por unidad
            "cpu_intensivo": costo_base > 5.0,
            "factor_costo_total": costo_base
        }
    
    def _detect_audio_problems(self, archivo: ArchivoAudio) -> List[str]:
        """Detecta problemas potenciales en el archivo de audio."""
        problemas = []
        
        if archivo.duracion is None:
            problemas.append("Duración desconocida")
        elif archivo.es_archivo_corto(2.0):
            problemas.append("Archivo muy corto para análisis robusto")
        elif archivo.es_archivo_largo(3600):  # 1 hora
            problemas.append("Archivo muy largo, puede afectar rendimiento")
        
        if not archivo.es_formato_valido:
            problemas.append("Formato de archivo no soportado")
        
        return problemas
    
    def _determine_audio_quality(self, archivo: ArchivoAudio) -> str:
        """Determina la calidad del audio basada en características del archivo."""
        # Estimación básica basada en formato y tamaño estimado
        if not archivo.es_formato_valido:
            return "baja"
        
        formato = archivo.formato or archivo.extension or ""
        formato_lower = formato.lower()
        
        # Formatos sin pérdida se consideran alta calidad
        if formato_lower in ['.wav', '.flac', '.aiff']:
            return "alta"
        
        # Formatos comprimidos modernos de buena calidad
        if formato_lower in ['.opus', '.aac']:
            return "media"
        
        # Formatos comprimidos comunes
        if formato_lower in ['.mp3', '.ogg']:
            # Podríamos estimar basado en el tamaño del archivo
            tamaño_mb = archivo.tamaño_estimado_mb
            if tamaño_mb and archivo.duracion:
                bitrate_estimado = (tamaño_mb * 8 * 1024) / archivo.duracion
                if bitrate_estimado > self.CALIDAD_ALTA_BITRATE:
                    return "alta"
                elif bitrate_estimado > self.CALIDAD_MEDIA_BITRATE:
                    return "media"
            return "media"
        
        return "media"  # Default para formatos desconocidos
    
    def _extract_basic_metrics(self, archivo: ArchivoAudio) -> Dict[str, float]:
        """Extrae métricas básicas del archivo de audio."""
        metricas = {}
        
        if archivo.duracion:
            metricas["duracion_segundos"] = archivo.duracion
            metricas["duracion_minutos"] = archivo.duracion / 60
        
        # Estimación de tamaño
        tamaño_mb = archivo.tamaño_estimado_mb
        if tamaño_mb:
            metricas["tamaño_mb"] = tamaño_mb
            if archivo.duracion:
                metricas["bitrate_estimado_kbps"] = (tamaño_mb * 8 * 1024) / archivo.duracion
        
        # Métricas derivadas
        if archivo.duracion:
            metricas["es_archivo_largo"] = float(archivo.es_archivo_largo(600))  # 10 min
            metricas["es_archivo_corto"] = float(archivo.es_archivo_corto(5))
        
        return metricas
    
    def _calculate_analysis_reliability(self, calidad: str, problemas: List[str]) -> float:
        """Calcula la confiabilidad del análisis basada en factores de calidad."""
        base_reliability = {
            "alta": 0.95,
            "media": 0.80,
            "baja": 0.60
        }.get(calidad, 0.50)
        
        # Reducir confiabilidad por cada problema detectado
        penalty_per_problem = 0.10
        final_reliability = base_reliability - (len(problemas) * penalty_per_problem)
        
        # Asegurar que esté en el rango [0.0, 1.0]
        return max(0.0, min(1.0, final_reliability))
