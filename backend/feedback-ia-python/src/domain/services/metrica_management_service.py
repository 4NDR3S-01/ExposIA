# filepath: /src/domain/services/metrica_management_service.py
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from ..entities.metrica import Metrica
from ..entities.parametro import Parametro
from ..entities.tipo_metrica import TipoMetrica
from ..value_objects.parametro_valor import ParametroValor
from ..exceptions.validation_exceptions import DomainValidationError


@dataclass
class MetricaAnalysisResult:
    """
    Resultado del análisis de una métrica con sus parámetros.
    """
    metrica: Metrica
    parametros_count: int
    valor_promedio: Optional[float]
    valor_minimo: Optional[float]
    valor_maximo: Optional[float]
    unidades_utilizadas: List[str]
    es_metrica_completa: bool
    recomendaciones: List[str]


class MetricaManagementService:
    """
    Servicio de dominio para gestión y análisis de métricas.
    
    Este servicio encapsula la lógica de negocio compleja relacionada con
    la gestión de métricas, parámetros y sus relaciones.
    """
    
    # Constantes para análisis de métricas
    MIN_PARAMETROS_METRICA_COMPLETA = 3
    MAX_PARAMETROS_POR_METRICA = 20
    
    def analyze_metrica_completeness(
        self, 
        metrica: Metrica, 
        parametros: List[Parametro]
    ) -> MetricaAnalysisResult:
        """
        Analiza la completitud y calidad de una métrica con sus parámetros.
        
        Args:
            metrica: Métrica a analizar
            parametros: Lista de parámetros asociados a la métrica
            
        Returns:
            MetricaAnalysisResult con el análisis completo
        """
        # Verificar que los parámetros pertenecen a la métrica
        parametros_validos = [p for p in parametros if p.is_related_to_metrica(metrica.id)]
        
        # Calcular estadísticas de valores
        valores = [p.valor.valor for p in parametros_validos]
        valor_promedio = sum(valores) / len(valores) if valores else None
        valor_minimo = min(valores) if valores else None
        valor_maximo = max(valores) if valores else None
        
        # Obtener unidades utilizadas
        unidades = list(set(
            p.valor.unidad for p in parametros_validos 
            if p.valor.unidad is not None
        ))
        
        # Determinar si es una métrica completa
        es_completa = self._is_metrica_completa(parametros_validos)
        
        # Generar recomendaciones
        recomendaciones = self._generate_metrica_recommendations(metrica, parametros_validos)
        
        return MetricaAnalysisResult(
            metrica=metrica,
            parametros_count=len(parametros_validos),
            valor_promedio=valor_promedio,
            valor_minimo=valor_minimo,
            valor_maximo=valor_maximo,
            unidades_utilizadas=unidades,
            es_metrica_completa=es_completa,
            recomendaciones=recomendaciones
        )
    
    def validate_parametro_for_metrica(
        self, 
        parametro: Parametro, 
        metrica: Metrica,
        existing_parametros: List[Parametro]
    ) -> Tuple[bool, List[str]]:
        """
        Valida si un parámetro es apropiado para una métrica específica.
        
        Args:
            parametro: Parámetro a validar
            metrica: Métrica objetivo
            existing_parametros: Parámetros existentes en la métrica
            
        Returns:
            Tupla (es_valido, lista_de_errores)
        """
        errores = []
        
        # Verificar relación con la métrica
        if not parametro.is_related_to_metrica(metrica.id):
            errores.append("El parámetro no está asociado a la métrica especificada")
        
        # Verificar unicidad del nombre en la métrica
        nombres_existentes = [p.nombre for p in existing_parametros if p.id != parametro.id]
        if not parametro.is_nombre_unique_in_metrica(nombres_existentes):
            errores.append(f"Ya existe un parámetro con el nombre '{parametro.nombre}' en esta métrica")
        
        # Verificar límite de parámetros por métrica
        if len(existing_parametros) >= self.MAX_PARAMETROS_POR_METRICA:
            errores.append(f"La métrica no puede tener más de {self.MAX_PARAMETROS_POR_METRICA} parámetros")
        
        # Validar consistencia de unidades si aplica
        unidades_existentes = list(set(
            p.valor.unidad for p in existing_parametros 
            if p.valor.unidad is not None
        ))
        
        if (len(unidades_existentes) > 0 and 
            parametro.valor.unidad and 
            parametro.valor.unidad not in unidades_existentes):
            # Advertencia, no error - diferentes unidades pueden ser válidas
            errores.append(f"ADVERTENCIA: Unidad '{parametro.valor.unidad}' difiere de las existentes: {unidades_existentes}")
        
        return len(errores) == 0, errores
    
    def suggest_parametros_ideales(
        self, 
        metrica: Metrica, 
        tipo_metrica: TipoMetrica
    ) -> List[Dict[str, any]]:
        """
        Sugiere parámetros ideales basados en el tipo de métrica.
        
        Args:
            metrica: Métrica para la cual sugerir parámetros
            tipo_metrica: Tipo de métrica al que pertenece
            
        Returns:
            Lista de diccionarios con sugerencias de parámetros
        """
        sugerencias = []
        
        # Sugerencias basadas en tipos comunes de métricas
        tipo_nombre = tipo_metrica.nombre.lower()
        
        if "velocidad" in tipo_nombre or "rapidez" in tipo_nombre:
            sugerencias.extend([
                {"nombre": "Velocidad Promedio", "unidad": "palabras/min", "valor_ejemplo": 120.0},
                {"nombre": "Velocidad Máxima", "unidad": "palabras/min", "valor_ejemplo": 150.0},
                {"nombre": "Velocidad Mínima", "unidad": "palabras/min", "valor_ejemplo": 90.0}
            ])
        
        elif "tono" in tipo_nombre or "frecuencia" in tipo_nombre:
            sugerencias.extend([
                {"nombre": "Frecuencia Fundamental", "unidad": "Hz", "valor_ejemplo": 120.0},
                {"nombre": "Rango Tonal", "unidad": "Hz", "valor_ejemplo": 50.0},
                {"nombre": "Variabilidad Tonal", "unidad": "%", "valor_ejemplo": 15.0}
            ])
        
        elif "volumen" in tipo_nombre or "intensidad" in tipo_nombre:
            sugerencias.extend([
                {"nombre": "Nivel Promedio", "unidad": "dB", "valor_ejemplo": 65.0},
                {"nombre": "Picos de Volumen", "unidad": "dB", "valor_ejemplo": 80.0},
                {"nombre": "Consistencia", "unidad": "%", "valor_ejemplo": 85.0}
            ])
        
        elif "pausa" in tipo_nombre or "silencio" in tipo_nombre:
            sugerencias.extend([
                {"nombre": "Duración Promedio Pausas", "unidad": "segundos", "valor_ejemplo": 0.5},
                {"nombre": "Frecuencia Pausas", "unidad": "pausas/min", "valor_ejemplo": 8.0},
                {"nombre": "Pausas Apropiadas", "unidad": "%", "valor_ejemplo": 75.0}
            ])
        
        elif "claridad" in tipo_nombre or "articulación" in tipo_nombre:
            sugerencias.extend([
                {"nombre": "Índice Claridad", "unidad": "puntos", "valor_ejemplo": 8.5},
                {"nombre": "Consonantes Claras", "unidad": "%", "valor_ejemplo": 90.0},
                {"nombre": "Vocales Definidas", "unidad": "%", "valor_ejemplo": 95.0}
            ])
        
        else:
            # Sugerencias genéricas
            sugerencias.extend([
                {"nombre": "Valor Principal", "unidad": "unidad", "valor_ejemplo": 100.0},
                {"nombre": "Calidad", "unidad": "puntos", "valor_ejemplo": 8.0},
                {"nombre": "Consistencia", "unidad": "%", "valor_ejemplo": 80.0}
            ])
        
        return sugerencias
    
    def calculate_metrica_score(
        self, 
        metrica: Metrica, 
        parametros: List[Parametro],
        parametros_ideales: Optional[List[Parametro]] = None
    ) -> Dict[str, float]:
        """
        Calcula un score general para la métrica basado en sus parámetros.
        
        Args:
            metrica: Métrica a evaluar
            parametros: Parámetros actuales de la métrica
            parametros_ideales: Parámetros ideales para comparación (opcional)
            
        Returns:
            Diccionario con diferentes scores calculados
        """
        if not parametros:
            return {
                "score_completitud": 0.0,
                "score_consistencia": 0.0,
                "score_general": 0.0
            }
        
        # Score de completitud (basado en número de parámetros)
        score_completitud = min(
            len(parametros) / self.MIN_PARAMETROS_METRICA_COMPLETA, 
            1.0
        )
        
        # Score de consistencia (basado en variabilidad de valores)
        valores = [p.valor.valor for p in parametros]
        if len(valores) > 1:
            promedio = sum(valores) / len(valores)
            varianza = sum((v - promedio) ** 2 for v in valores) / len(valores)
            coef_variacion = (varianza ** 0.5) / promedio if promedio != 0 else 1.0
            score_consistencia = max(0.0, 1.0 - min(coef_variacion, 1.0))
        else:
            score_consistencia = 1.0
        
        # Score general (promedio ponderado)
        score_general = (score_completitud * 0.6) + (score_consistencia * 0.4)
        
        resultado = {
            "score_completitud": round(score_completitud, 3),
            "score_consistencia": round(score_consistencia, 3),
            "score_general": round(score_general, 3)
        }
        
        # Si hay parámetros ideales, calcular score de cercanía
        if parametros_ideales:
            score_cercanía = self._calculate_closeness_score(parametros, parametros_ideales)
            resultado["score_cercanía_ideal"] = round(score_cercanía, 3)
        
        return resultado
    
    def detect_parametros_outliers(
        self, 
        parametros: List[Parametro]
    ) -> List[Tuple[Parametro, str]]:
        """
        Detecta parámetros que son outliers o anómalos.
        
        Args:
            parametros: Lista de parámetros a analizar
            
        Returns:
            Lista de tuplas (parametro, razon_outlier)
        """
        if len(parametros) < 3:
            return []  # No se pueden detectar outliers con pocos datos
        
        outliers = []
        valores = [p.valor.valor for p in parametros]
        
        # Calcular estadísticas
        promedio = sum(valores) / len(valores)
        desviacion = (sum((v - promedio) ** 2 for v in valores) / len(valores)) ** 0.5
        
        # Detectar outliers usando regla de 2 desviaciones estándar
        umbral_outlier = 2 * desviacion
        
        for parametro in parametros:
            diferencia = abs(parametro.valor.valor - promedio)
            
            if diferencia > umbral_outlier:
                if parametro.valor.valor > promedio:
                    razon = f"Valor excepcionalmente alto ({parametro.valor.valor:.2f} vs promedio {promedio:.2f})"
                else:
                    razon = f"Valor excepcionalmente bajo ({parametro.valor.valor:.2f} vs promedio {promedio:.2f})"
                outliers.append((parametro, razon))
        
        return outliers
    
    def _is_metrica_completa(self, parametros: List[Parametro]) -> bool:
        """Determina si una métrica está completa basada en sus parámetros."""
        return len(parametros) >= self.MIN_PARAMETROS_METRICA_COMPLETA
    
    def _generate_metrica_recommendations(
        self, 
        metrica: Metrica, 
        parametros: List[Parametro]
    ) -> List[str]:
        """Genera recomendaciones para mejorar una métrica."""
        recomendaciones = []
        
        # Recomendaciones basadas en número de parámetros
        if len(parametros) == 0:
            recomendaciones.append("Agregar parámetros para que la métrica sea útil")
        elif len(parametros) < self.MIN_PARAMETROS_METRICA_COMPLETA:
            recomendaciones.append(f"Agregar más parámetros (mínimo {self.MIN_PARAMETROS_METRICA_COMPLETA} recomendado)")
        elif len(parametros) > self.MAX_PARAMETROS_POR_METRICA:
            recomendaciones.append("Considerar dividir en múltiples métricas - demasiados parámetros")
        
        # Recomendaciones basadas en unidades
        unidades = list(set(p.valor.unidad for p in parametros if p.valor.unidad))
        if len(unidades) > 3:
            recomendaciones.append("Múltiples unidades detectadas - considerar estandarizar")
        
        # Recomendaciones basadas en valores
        if parametros:
            valores = [p.valor.valor for p in parametros]
            if all(v == valores[0] for v in valores):
                recomendaciones.append("Todos los parámetros tienen el mismo valor - verificar variabilidad")
        
        return recomendaciones
    
    def _calculate_closeness_score(
        self, 
        parametros_actuales: List[Parametro], 
        parametros_ideales: List[Parametro]
    ) -> float:
        """Calcula qué tan cerca están los parámetros actuales de los ideales."""
        if not parametros_ideales:
            return 1.0
        
        # Implementación simplificada - comparar valores promedio
        valores_actuales = [p.valor.valor for p in parametros_actuales]
        valores_ideales = [p.valor.valor for p in parametros_ideales]
        
        if not valores_actuales or not valores_ideales:
            return 0.0
        
        promedio_actual = sum(valores_actuales) / len(valores_actuales)
        promedio_ideal = sum(valores_ideales) / len(valores_ideales)
        
        if promedio_ideal == 0:
            return 1.0 if promedio_actual == 0 else 0.0
        
        # Score basado en la diferencia porcentual
        diferencia_porcentual = abs(promedio_actual - promedio_ideal) / promedio_ideal
        return max(0.0, 1.0 - diferencia_porcentual)
