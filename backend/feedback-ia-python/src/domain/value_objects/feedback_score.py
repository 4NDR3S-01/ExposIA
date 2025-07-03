"""
Value Object para el puntaje de feedback.
Encapsula la lógica relacionada con la validación y categorización de puntajes.
"""
from dataclasses import dataclass
from typing import Union

from ..exceptions.validation_exceptions import InvalidScoreError


@dataclass(frozen=True)
class FeedbackScore:
    """
    Value Object inmutable que representa un puntaje de feedback.
    
    Los value objects son inmutables y contienen lógica específica
    del dominio relacionada con su valor.
    """
    
    value: float
    
    def __post_init__(self):
        """Valida el puntaje al crear la instancia."""
        if not self._is_valid_score(self.value):
            raise InvalidScoreError(f"El puntaje debe estar entre 0 y 100, recibido: {self.value}")
    
    @staticmethod
    def _is_valid_score(score: Union[int, float]) -> bool:
        """Valida que el puntaje esté en el rango correcto."""
        return isinstance(score, (int, float)) and 0 <= score <= 100
    
    def is_high(self, threshold: float = 80.0) -> bool:
        """Determina si es un puntaje alto."""
        return self.value >= threshold
    
    def is_low(self, threshold: float = 40.0) -> bool:
        """Determina si es un puntaje bajo."""
        return self.value <= threshold
    
    def is_medium(self, low_threshold: float = 40.0, high_threshold: float = 80.0) -> bool:
        """Determina si es un puntaje medio."""
        return low_threshold < self.value < high_threshold
    
    def get_performance_level(self) -> str:
        """Obtiene el nivel de rendimiento basado en el puntaje."""
        if self.is_high(90):
            return "Excelente"
        elif self.is_high(80):
            return "Muy Bueno"
        elif self.is_high(60):
            return "Bueno"
        elif self.is_low(40):
            return "Necesita Mejora"
        else:
            return "Regular"
    
    def get_category(self) -> str:
        """Obtiene la categoría del puntaje."""
        if self.is_high():
            return "ALTO"
        elif self.is_low():
            return "BAJO"
        else:
            return "MEDIO"
    
    def to_percentage_string(self) -> str:
        """Convierte el puntaje a string con formato de porcentaje."""
        return f"{self.value:.1f}%"
    
    def compare_with(self, other: 'FeedbackScore') -> str:
        """Compara este puntaje con otro."""
        if self.value > other.value:
            return "MEJOR"
        elif self.value < other.value:
            return "PEOR"
        else:
            return "IGUAL"
    
    def difference_with(self, other: 'FeedbackScore') -> float:
        """Calcula la diferencia con otro puntaje."""
        return abs(self.value - other.value)
    
    def __str__(self) -> str:
        return f"{self.value:.1f}"
    
    def __float__(self) -> float:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, FeedbackScore):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        return False
    
    def __lt__(self, other) -> bool:
        if isinstance(other, FeedbackScore):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented
    
    def __le__(self, other) -> bool:
        return self < other or self == other
    
    def __gt__(self, other) -> bool:
        if isinstance(other, FeedbackScore):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        return self > other or self == other
