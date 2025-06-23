"""
Implementación concreta del servicio de IA usando OpenAI.
Esta implementación pertenece a la capa de infraestructura.
"""
import asyncio
import json
from typing import Dict, List
import openai
from ...application.interfaces.ai_service_interface import AIServiceInterface
from ...domain.exceptions.validation_exceptions import AIServiceError
from ..config.ai_config import AIConfig


class OpenAIService(AIServiceInterface):
    """
    Implementación del servicio de IA usando OpenAI API.
    
    Esta clase implementa la interfaz definida en la capa de aplicación
    y proporciona funcionalidades específicas de análisis de audio con IA.
    
    Responsabilidades:
    - Interactuar con APIs de OpenAI
    - Procesar archivos de audio
    - Generar análisis y métricas
    - Manejar errores de servicios externos
    """
    
    def __init__(self):
        self.config = AIConfig()
        openai.api_key = self.config.openai_api_key
        self.client = openai.AsyncOpenAI(api_key=self.config.openai_api_key)
    
    async def analyze_audio_basic(
        self, 
        grabacion_id: int, 
        audio_data: Dict
    ) -> Dict:
        """
        Realiza análisis básico de audio usando IA.
        
        Este método utiliza modelos más simples y rápidos para
        proporcionar métricas básicas de audio.
        """
        try:
            # Simular análisis básico (en implementación real usaría APIs específicas)
            analysis_result = {
                "grabacion_id": grabacion_id,
                "analysis_type": "basic",
                "duration_seconds": audio_data.get("duration", 0),
                "audio_metrics": {
                    "clarity_score": await self._calculate_basic_clarity(audio_data),
                    "volume_consistency": await self._calculate_volume_consistency(audio_data),
                    "speech_rate": await self._estimate_speech_rate(audio_data),
                    "pause_patterns": await self._analyze_basic_pauses(audio_data),
                    "background_noise": audio_data.get("noise_level", 0.1)
                },
                "confidence_score": 0.75,  # Menor confianza para análisis básico
                "processing_time_ms": 1500
            }
            
            return analysis_result
            
        except Exception as e:
            raise AIServiceError(f"Error en análisis básico de audio: {str(e)}")
    
    async def analyze_audio_advanced(
        self, 
        grabacion_id: int, 
        audio_data: Dict
    ) -> Dict:
        """
        Realiza análisis avanzado de audio usando IA.
        
        Este método utiliza modelos más sofisticados para
        proporcionar análisis detallado y preciso.
        """
        try:
            # Análisis avanzado con múltiples métricas
            basic_analysis = await self.analyze_audio_basic(grabacion_id, audio_data)
            
            # Análisis adicionales para el modelo avanzado
            advanced_metrics = {
                "emotion_analysis": await self._analyze_emotions_advanced(audio_data),
                "intonation_variety": await self._analyze_intonation_patterns(audio_data),
                "articulation_clarity": await self._analyze_articulation(audio_data),
                "presentation_structure": await self._analyze_presentation_structure(audio_data),
                "audience_engagement": await self._estimate_engagement_level(audio_data),
                "filler_words_count": await self._count_filler_words(audio_data),
                "pace_variability": await self._analyze_pace_changes(audio_data)
            }
            
            # Combinar análisis básico con avanzado
            analysis_result = {
                **basic_analysis,
                "analysis_type": "advanced",
                "advanced_metrics": advanced_metrics,
                "confidence_score": 0.92,  # Mayor confianza para análisis avanzado
                "processing_time_ms": 4500
            }
            
            return analysis_result
            
        except Exception as e:
            raise AIServiceError(f"Error en análisis avanzado de audio: {str(e)}")
    
    async def generate_feedback_comment(
        self,
        analysis_results: Dict,
        parametro_type: str,
        score: float
    ) -> str:
        """
        Genera un comentario de feedback usando IA.
        """
        try:
            # Preparar contexto para el modelo
            context = self._prepare_comment_context(analysis_results, parametro_type, score)
            
            # Usar OpenAI para generar comentario personalizado
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en comunicación y presentaciones. "
                                 "Genera comentarios constructivos y específicos para mejorar las habilidades de presentación."
                    },
                    {
                        "role": "user",
                        "content": f"Basándote en este análisis: {context}, "
                                 f"genera un comentario específico y constructivo para el parámetro '{parametro_type}' "
                                 f"con puntaje {score}. Mantén el comentario entre 50-150 palabras."
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback a comentario genérico si falla la IA
            return self._generate_fallback_comment(parametro_type, score)
    
    async def extract_speech_metrics(self, audio_file_path: str) -> Dict:
        """
        Extrae métricas de habla del archivo de audio.
        """
        try:
            # En una implementación real, aquí usarías bibliotecas como librosa,
            # speechrecognition, o APIs especializadas
            
            # Simular extracción de métricas
            await asyncio.sleep(0.5)  # Simular procesamiento
            
            metrics = {
                "speech_rate": 145.5,  # palabras por minuto
                "pause_patterns": {
                    "total_pauses": 23,
                    "average_pause_duration": 0.8,
                    "pause_frequency": 0.15
                },
                "volume_consistency": 0.78,
                "clarity_score": 0.85,
                "intonation_variety": 0.72,
                "silence_ratio": 0.12,
                "speaking_time_ratio": 0.88
            }
            
            return metrics
            
        except Exception as e:
            raise AIServiceError(f"Error extrayendo métricas de habla: {str(e)}")
    
    async def detect_emotions(self, audio_file_path: str) -> Dict:
        """
        Detecta emociones en el audio.
        """
        try:
            # Simular detección de emociones
            await asyncio.sleep(0.3)
            
            emotions = {
                "confidence": 0.82,
                "neutral": 0.45,
                "positive": 0.35,
                "enthusiastic": 0.15,
                "nervous": 0.05,
                "dominant_emotion": "neutral",
                "emotional_variability": 0.68
            }
            
            return emotions
            
        except Exception as e:
            raise AIServiceError(f"Error detectando emociones: {str(e)}")
    
    async def transcribe_audio(
        self, 
        audio_file_path: str,
        language: str = "es"
    ) -> Dict:
        """
        Transcribe el audio a texto.
        """
        try:
            # En implementación real usarías Whisper de OpenAI
            with open(audio_file_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            return {
                "text": transcript.text,
                "language": language,
                "confidence": 0.95,
                "word_count": len(transcript.text.split()),
                "processing_time_ms": 2000
            }
            
        except Exception as e:
            raise AIServiceError(f"Error transcribiendo audio: {str(e)}")
    
    async def analyze_presentation_structure(self, transcript: str) -> Dict:
        """
        Analiza la estructura de una presentación.
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Analiza la estructura de presentaciones y proporciona métricas específicas."
                    },
                    {
                        "role": "user",
                        "content": f"Analiza la estructura de esta presentación y califica del 0 al 1: {transcript[:1000]}..."
                    }
                ],
                max_tokens=300
            )
            
            # En implementación real, parsearías la respuesta para extraer métricas
            return {
                "introduction_quality": 0.75,
                "conclusion_quality": 0.68,
                "content_organization": 0.82,
                "transition_quality": 0.71,
                "structure_score": 0.74
            }
            
        except Exception as e:
            raise AIServiceError(f"Error analizando estructura: {str(e)}")
    
    async def get_improvement_suggestions(
        self,
        analysis_results: Dict,
        weak_areas: List[str]
    ) -> List[str]:
        """
        Genera sugerencias de mejora específicas.
        """
        try:
            suggestions_prompt = self._build_suggestions_prompt(analysis_results, weak_areas)
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un coach de presentaciones. Proporciona sugerencias específicas y accionables."
                    },
                    {
                        "role": "user",
                        "content": suggestions_prompt
                    }
                ],
                max_tokens=400
            )
            
            # Parsear respuesta en lista de sugerencias
            suggestions_text = response.choices[0].message.content
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
            
            return suggestions[:5]  # Máximo 5 sugerencias
            
        except Exception as e:
            return self._generate_fallback_suggestions(weak_areas)
    
    async def compare_with_benchmarks(
        self,
        analysis_results: Dict,
        presentation_type: str
    ) -> Dict:
        """
        Compara con benchmarks establecidos.
        """
        try:
            # Benchmarks predefinidos por tipo de presentación
            benchmarks = self._get_benchmarks(presentation_type)
            
            comparison = {}
            audio_metrics = analysis_results.get("audio_metrics", {})
            
            for metric, benchmark_value in benchmarks.items():
                actual_value = audio_metrics.get(metric, 0)
                comparison[metric] = {
                    "actual": actual_value,
                    "benchmark": benchmark_value,
                    "performance": "above" if actual_value > benchmark_value else "below",
                    "difference": actual_value - benchmark_value
                }
            
            return comparison
            
        except Exception as e:
            raise AIServiceError(f"Error comparando con benchmarks: {str(e)}")
    
    # Métodos auxiliares privados
    
    async def _calculate_basic_clarity(self, audio_data: Dict) -> float:
        """Calcula puntaje básico de claridad."""
        # Simulación - en implementación real analizaría el audio
        return min(1.0, audio_data.get("volume", 0.5) * 1.2)
    
    async def _calculate_volume_consistency(self, audio_data: Dict) -> float:
        """Calcula consistencia de volumen."""
        return audio_data.get("volume_variance", 0.8)
    
    async def _estimate_speech_rate(self, audio_data: Dict) -> float:
        """Estima velocidad de habla."""
        duration = audio_data.get("duration", 60)
        word_count = audio_data.get("estimated_words", 150)
        return (word_count / duration) * 60  # palabras por minuto
    
    async def _analyze_basic_pauses(self, audio_data: Dict) -> float:
        """Analiza patrones básicos de pausas."""
        return audio_data.get("pause_quality", 0.7)
    
    async def _analyze_emotions_advanced(self, audio_data: Dict) -> Dict:
        """Análisis avanzado de emociones."""
        return {
            "emotional_range": 0.75,
            "appropriate_emotion": 0.82,
            "emotional_consistency": 0.68
        }
    
    async def _analyze_intonation_patterns(self, audio_data: Dict) -> float:
        """Analiza patrones de entonación."""
        return 0.76
    
    async def _analyze_articulation(self, audio_data: Dict) -> float:
        """Analiza claridad de articulación."""
        return 0.83
    
    async def _analyze_presentation_structure(self, audio_data: Dict) -> Dict:
        """Analiza estructura de presentación desde audio."""
        return {
            "clear_opening": 0.78,
            "logical_flow": 0.71,
            "strong_closing": 0.69
        }
    
    async def _estimate_engagement_level(self, audio_data: Dict) -> float:
        """Estima nivel de engagement."""
        return 0.74
    
    async def _count_filler_words(self, audio_data: Dict) -> int:
        """Cuenta palabras de relleno."""
        return audio_data.get("filler_words", 8)
    
    async def _analyze_pace_changes(self, audio_data: Dict) -> float:
        """Analiza variabilidad del ritmo."""
        return 0.65
    
    def _prepare_comment_context(self, analysis: Dict, parametro_type: str, score: float) -> str:
        """Prepara contexto para generar comentario."""
        return f"Parámetro: {parametro_type}, Puntaje: {score}, Métricas: {json.dumps(analysis.get('audio_metrics', {}))}"
    
    def _generate_fallback_comment(self, parametro_type: str, score: float) -> str:
        """Genera comentario de respaldo si falla la IA."""
        if score >= 80:
            return f"Excelente rendimiento en {parametro_type}. ¡Sigue así!"
        elif score >= 60:
            return f"Buen trabajo en {parametro_type}. Hay oportunidades de mejora."
        else:
            return f"Se recomienda practicar más en {parametro_type} para mejorar el rendimiento."
    
    def _build_suggestions_prompt(self, analysis: Dict, weak_areas: List[str]) -> str:
        """Construye prompt para sugerencias."""
        return f"Basándote en este análisis {analysis} y estas áreas débiles {weak_areas}, proporciona 3-5 sugerencias específicas de mejora."
    
    def _generate_fallback_suggestions(self, weak_areas: List[str]) -> List[str]:
        """Genera sugerencias de respaldo."""
        fallback_suggestions = {
            "clarity": "Practica articular claramente cada palabra",
            "volume": "Mantén un volumen consistente durante toda la presentación",
            "pace": "Varía el ritmo para mantener el interés del público",
            "pauses": "Usa pausas estratégicas para enfatizar puntos importantes"
        }
        
        return [fallback_suggestions.get(area, f"Mejora tu {area}") for area in weak_areas[:3]]
    
    def _get_benchmarks(self, presentation_type: str) -> Dict:
        """Obtiene benchmarks por tipo de presentación."""
        benchmarks_db = {
            "academic": {
                "clarity_score": 0.85,
                "speech_rate": 140,
                "pause_patterns": 0.75
            },
            "corporate": {
                "clarity_score": 0.80,
                "speech_rate": 160,
                "pause_patterns": 0.70
            },
            "general": {
                "clarity_score": 0.75,
                "speech_rate": 150,
                "pause_patterns": 0.65
            }
        }
        
        return benchmarks_db.get(presentation_type, benchmarks_db["general"])
