# filepath: /src/domain/value_objects/parametro_valor.py
from dataclasses import dataclass
from typing import Optional

from ..exceptions.validation_exceptions import DomainValidationError


@dataclass(frozen=True)
class ParametroValor:
    """
    Value object que representa el valor de un parámetro con su unidad.
    
    Este value object encapsula la lógica de negocio relacionada con
    los valores de parámetros y sus unidades de medida.
    """
    
    valor: float
    unidad: Optional[str] = None
    
    def __post_init__(self):
        """Validación después de la inicialización."""
        self._validate()
    
    def _validate(self) -> None:
        """Valida el valor según las reglas de negocio."""
        if self.valor is None:
            raise DomainValidationError("El valor del parámetro es obligatorio")
        
        if not isinstance(self.valor, (int, float)):
            raise DomainValidationError("El valor del parámetro debe ser numérico")
        
        if self.unidad and len(self.unidad.strip()) > 50:
            raise DomainValidationError("La unidad no puede exceder 50 caracteres")
    
    @property
    def valor_formateado(self) -> str:
        """
        Retorna el valor formateado con su unidad.
        
        Returns:
            String con el valor y unidad formateados
        """
        if self.unidad:
            return f"{self.valor} {self.unidad}"
        return str(self.valor)
    
    @property
    def es_entero(self) -> bool:
        """Verifica si el valor es un número entero."""
        return float(self.valor).is_integer()
    
    @property
    def es_positivo(self) -> bool:
        """Verifica si el valor es positivo."""
        return self.valor > 0
    
    @property
    def es_negativo(self) -> bool:
        """Verifica si el valor es negativo."""
        return self.valor < 0
    
    @property
    def es_cero(self) -> bool:
        """Verifica si el valor es cero."""
        return self.valor == 0
    
    def esta_en_rango(self, minimo: float, maximo: float) -> bool:
        """
        Verifica si el valor está dentro del rango especificado.
        
        Args:
            minimo: Valor mínimo del rango (inclusivo)
            maximo: Valor máximo del rango (inclusivo)
            
        Returns:
            True si está en el rango, False en caso contrario
        """
        return minimo <= self.valor <= maximo
    
    def es_aproximadamente_igual(self, otro_valor: float, tolerancia: float = 0.001) -> bool:
        """
        Compara si el valor es aproximadamente igual a otro valor.
        
        Args:
            otro_valor: Valor a comparar
            tolerancia: Tolerancia para la comparación
            
        Returns:
            True si son aproximadamente iguales
        """
        return abs(self.valor - otro_valor) <= tolerancia
    
    def redondear(self, decimales: int = 2) -> 'ParametroValor':
        """
        Crea un nuevo ParametroValor con el valor redondeado.
        
        Args:
            decimales: Número de decimales para redondear
            
        Returns:
            Nuevo ParametroValor con el valor redondeado
        """
        valor_redondeado = round(self.valor, decimales)
        return ParametroValor(valor_redondeado, self.unidad)
    
    def convertir_unidad(self, nueva_unidad: str) -> 'ParametroValor':
        """
        Crea un nuevo ParametroValor con una nueva unidad.
        Nota: Esta implementación básica solo cambia la unidad,
        no realiza conversión matemática entre unidades.
        
        Args:
            nueva_unidad: Nueva unidad para el valor
            
        Returns:
            Nuevo ParametroValor con la nueva unidad
        """
        if not nueva_unidad or len(nueva_unidad.strip()) > 50:
            raise DomainValidationError("La unidad debe ser válida y no exceder 50 caracteres")
        
        return ParametroValor(self.valor, nueva_unidad.strip())
    
    def __str__(self) -> str:
        return self.valor_formateado
    
    def __lt__(self, other) -> bool:
        if isinstance(other, ParametroValor):
            return self.valor < other.valor
        return self.valor < other
    
    def __le__(self, other) -> bool:
        if isinstance(other, ParametroValor):
            return self.valor <= other.valor
        return self.valor <= other
    
    def __gt__(self, other) -> bool:
        if isinstance(other, ParametroValor):
            return self.valor > other.valor
        return self.valor > other
    
    def __ge__(self, other) -> bool:
        if isinstance(other, ParametroValor):
            return self.valor >= other.valor
        return self.valor >= other
