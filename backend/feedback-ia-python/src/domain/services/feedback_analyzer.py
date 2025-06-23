"""
Servicio de dominio para análisis de feedback.
Contiene lógica compleja de negocio que no pertenece a una entidad específica.
"""
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

from ..entities.feedback import Feedback
from ..value_objects.feedback_score import FeedbackScore


class FeedbackAnalyzerService:
    """
    Servicio de dominio que encapsula la lógica compleja de análisis de feedback.
    
    Este servicio contiene lógica de negocio que:
    - No pertenece a una entidad específica
    - Requiere conocimiento de múltiples entidades
    - Implementa reglas de negocio complejas
    
    Responsabilidades:
    - Calcular puntajes basados en análisis de IA
    - Generar comentarios automáticos
    - Evaluar patrones de rendimiento
    - Aplicar reglas de negocio complejas
    """
    
    # Configuración de pesos para diferentes métricas
    METRIC_WEIGHTS = {
        'claridad': 0.25,
        'volumen': 0.20,
        'velocidad': 0.20,
        'pausas': 0.15,
        'entonacion': 0.20
    }
    
    # Umbrales para categorización de puntajes
    THRESHOLDS = {
        'excelente': 90,
        'muy_bueno': 80,
        'bueno': 70,
        'regular': 50,
        'necesita_mejora': 40
    }
    
    async def calculate_score_for_parameter(
        self,
        parametro_id: int,
        ai_analysis: Dict
    ) -> float:
        """
        Calcula el puntaje para un parámetro específico basado en el análisis de IA.
        
        Args:
            parametro_id: ID del parámetro a evaluar
            ai_analysis: Datos del análisis de IA
            
        Returns:
            Puntaje calculado (0-100)
        """
        # Obtener métricas relevantes para el parámetro
        relevant_metrics = self._get_relevant_metrics_for_parameter(parametro_id, ai_analysis)
        
        if not relevant_metrics:
            return 50.0  # Puntaje neutral si no hay métricas
        
        # Calcular puntaje ponderado
        weighted_score = 0.0
        total_weight = 0.0
        
        for metric_name, metric_value in relevant_metrics.items():
            weight = self.METRIC_WEIGHTS.get(metric_name, 0.1)
            normalized_score = self._normalize_metric_value(metric_name, metric_value)
            
            weighted_score += normalized_score * weight
            total_weight += weight
        
        # Calcular puntaje final
        if total_weight > 0:
            final_score = (weighted_score / total_weight) * 100
        else:
            final_score = 50.0
        
        # Aplicar ajustes basados en reglas de negocio
        final_score = self._apply_business_rules(parametro_id, final_score, ai_analysis)
        
        # Asegurar que el puntaje esté en el rango válido
        return max(0.0, min(100.0, final_score))
    
    async def generate_comment_for_parameter(
        self,
        parametro_id: int,
        ai_analysis: Dict,
        score: float
    ) -> str:
        """
        Genera un comentario automático para un parámetro basado en su puntaje y análisis.
        
        Args:
            parametro_id: ID del parámetro
            ai_analysis: Datos del análisis de IA
            score: Puntaje calculado
            
        Returns:
            Comentario generado automáticamente
        """
        score_obj = FeedbackScore(score)
        performance_level = score_obj.get_performance_level()
        
        # Obtener métricas específicas para el comentario
        metrics = self._get_relevant_metrics_for_parameter(parametro_id, ai_analysis)
        
        # Generar comentario basado en el nivel de rendimiento
        if performance_level == "Excelente":
            return self._generate_excellent_comment(metrics)
        elif performance_level in ["Muy Bueno", "Bueno"]:
            return self._generate_good_comment(metrics, score)
        elif performance_level == "Regular":
            return self._generate_regular_comment(metrics)
        else:  # Necesita Mejora
            return self._generate_improvement_comment(metrics)
    
    def analyze_feedback_patterns(self, feedbacks: List[Feedback]) -> Dict:
        """
        Analiza patrones en una lista de feedbacks.
        
        Args:
            feedbacks: Lista de feedbacks a analizar
            
        Returns:
            Diccionario con análisis de patrones
        """
        if not feedbacks:
            return {'error': 'No hay feedbacks para analizar'}
        
        scores = [feedback.score.value for feedback in feedbacks]
        
        analysis = {
            'total_feedbacks': len(feedbacks),
            'promedio': sum(scores) / len(scores),
            'score_maximo': max(scores),
            'score_minimo': min(scores),
            'feedbacks_altos': len([s for s in scores if s >= 80]),
            'feedbacks_medios': len([s for s in scores if 40 <= s < 80]),
            'feedbacks_bajos': len([s for s in scores if s < 40]),
            'feedbacks_automaticos': len([f for f in feedbacks if not f.es_manual]),
            'feedbacks_manuales': len([f for f in feedbacks if f.es_manual]),
            'tendencia': self._calculate_trend(scores),
            'consistencia': self._calculate_consistency(scores)
        }
        
        return analysis
    
    def _get_relevant_metrics_for_parameter(
        self,
        parametro_id: int,
        ai_analysis: Dict
    ) -> Dict:
        """Obtiene las métricas relevantes para un parámetro específico."""
        # Esta lógica dependería de la configuración de parámetros
        # Por ahora, retornamos todas las métricas disponibles
        metrics = {}
        
        if 'audio_metrics' in ai_analysis:
            audio_metrics = ai_analysis['audio_metrics']
            
            # Mapear métricas según el tipo de parámetro
            if parametro_id in [1, 2]:  # Parámetros de claridad
                metrics['claridad'] = audio_metrics.get('clarity_score', 0.5)
                metrics['volumen'] = audio_metrics.get('volume_consistency', 0.5)
            elif parametro_id in [3, 4]:  # Parámetros de ritmo
                metrics['velocidad'] = audio_metrics.get('speech_rate', 0.5)
                metrics['pausas'] = audio_metrics.get('pause_patterns', 0.5)
            else:  # Otros parámetros
                metrics['entonacion'] = audio_metrics.get('intonation_variety', 0.5)
        
        return metrics
    
    def _normalize_metric_value(self, metric_name: str, value: float) -> float:
        """Normaliza un valor de métrica a un rango 0-1."""
        # Diferentes métricas pueden tener diferentes rangos
        if metric_name in ['claridad', 'volumen', 'entonacion']:
            # Estas métricas ya vienen normalizadas (0-1)
            return max(0.0, min(1.0, value))
        elif metric_name == 'velocidad':
            # Velocidad óptima está alrededor de 150 palabras por minuto
            optimal_speed = 150
            if value <= 0:
                return 0.0
            # Calcular qué tan cerca está del óptimo
            deviation = abs(value - optimal_speed) / optimal_speed
            return max(0.0, 1.0 - deviation)
        elif metric_name == 'pausas':
            # Pausas apropiadas mejoran la comprensión
            return max(0.0, min(1.0, value))
        else:
            return 0.5  # Valor neutral para métricas desconocidas
    
    def _apply_business_rules(
        self,
        parametro_id: int,
        score: float,
        ai_analysis: Dict
    ) -> float:
        """Aplica reglas de negocio específicas para ajustar el puntaje."""
        adjusted_score = score
        
        # Regla: Si la grabación es muy corta, penalizar ligeramente
        duration = ai_analysis.get('duration_seconds', 0)
        if duration < 30:  # Menos de 30 segundos
            adjusted_score *= 0.95
        
        # Regla: Si hay mucho ruido de fondo, penalizar
        noise_level = ai_analysis.get('background_noise', 0)
        if noise_level > 0.3:  # Alto nivel de ruido
            adjusted_score *= 0.9
        
        # Regla: Bonificar consistencia en el rendimiento
        consistency = ai_analysis.get('consistency_score', 0.5)
        if consistency > 0.8:
            adjusted_score *= 1.05  # Bonificación del 5%
        
        return adjusted_score
    
    def _generate_excellent_comment(self, metrics: Dict) -> str:
        """Genera comentario para rendimiento excelente."""
        strong_metrics = [name for name, value in metrics.items() if value > 0.8]
        
        if strong_metrics:
            return f"Excelente rendimiento. Destacas especialmente en: {', '.join(strong_metrics)}. ¡Sigue así!"
        else:
            return "Excelente rendimiento general. Tu presentación es muy profesional."
    
    def _generate_good_comment(self, metrics: Dict, score: float) -> str:
        """Genera comentario para buen rendimiento."""
        return f"Buen trabajo (puntaje: {score:.1f}). Mantén este nivel de calidad."
    
    def _generate_regular_comment(self, metrics: Dict) -> str:
        """Genera comentario para rendimiento regular."""
        weak_metrics = [name for name, value in metrics.items() if value < 0.5]
        
        if weak_metrics:
            return f"Rendimiento aceptable. Considera mejorar: {', '.join(weak_metrics)}."
        else:
            return "Rendimiento aceptable. Hay oportunidades de mejora."
    
    def _generate_improvement_comment(self, metrics: Dict) -> str:
        """Genera comentario para rendimiento que necesita mejora."""
        weak_metrics = [name for name, value in metrics.items() if value < 0.4]
        
        if weak_metrics:
            return f"Necesita mejora en: {', '.join(weak_metrics)}. Te recomendamos practicar estos aspectos."
        else:
            return "Necesita mejora. Te sugerimos revisar los fundamentos de presentación."
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calcula la tendencia de los puntajes."""
        if len(scores) < 2:
            return "insuficiente_data"
        
        # Comparar primera y segunda mitad
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid if mid > 0 else 0
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)
        
        diff = second_half_avg - first_half_avg
        
        if diff > 5:
            return "mejorando"
        elif diff < -5:
            return "empeorando"
        else:
            return "estable"
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calcula la consistencia de los puntajes (0-1, donde 1 es muy consistente)."""
        if len(scores) < 2:
            return 1.0
        
        avg = sum(scores) / len(scores)
        variance = sum((score - avg) ** 2 for score in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Normalizar la desviación estándar a un rango 0-1
        # Una desviación estándar de 0 = consistencia perfecta (1.0)
        # Una desviación estándar de 25 o más = inconsistencia alta (0.0)
        consistency = max(0.0, 1.0 - (std_dev / 25.0))
        
        return consistency
