# filepath: /src/domain/entities/parametro.py
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from ..exceptions.validation_exceptions import DomainValidationError
from ..value_objects.parametro_valor import ParametroValor


@dataclass
class Parametro:
    """
    Entidad de dominio que representa un parámetro específico de una métrica.
    
    Un parámetro define un valor específico que se puede medir dentro de una métrica
    (ej: "120" palabras por minuto para la métrica "Velocidad de habla").
    """
    
    id: Optional[int]
    metrica_id: int
    nombre: str
    valor: ParametroValor
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validación y normalización después de la inicialización."""
        self._validate()
        self._normalize()
    
    def _validate(self) -> None:
        """Valida la entidad según las reglas de negocio."""
        if not self.nombre or not self.nombre.strip():
            raise DomainValidationError("El nombre del parámetro es obligatorio")
        
        if len(self.nombre.strip()) > 100:
            raise DomainValidationError("El nombre del parámetro no puede exceder 100 caracteres")
        
        if not self.metrica_id or self.metrica_id <= 0:
            raise DomainValidationError("El ID de métrica es obligatorio y debe ser positivo")
        
        if not isinstance(self.valor, ParametroValor):
            raise DomainValidationError("El valor debe ser una instancia de ParametroValor")
    
    def _normalize(self) -> None:
        """Normaliza los datos de la entidad."""
        self.nombre = self.nombre.strip().title()
    
    def update_nombre(self, nuevo_nombre: str) -> None:
        """
        Actualiza el nombre del parámetro.
        
        Args:
            nuevo_nombre: El nuevo nombre para el parámetro
            
        Raises:
            DomainValidationError: Si el nuevo nombre no es válido
        """
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise DomainValidationError("El nombre del parámetro es obligatorio")
        
        if len(nuevo_nombre.strip()) > 100:
            raise DomainValidationError("El nombre del parámetro no puede exceder 100 caracteres")
        
        self.nombre = nuevo_nombre.strip().title()
        self.updated_at = datetime.utcnow()
    
    def update_valor(self, nuevo_valor: float, nueva_unidad: Optional[str] = None) -> None:
        """
        Actualiza el valor del parámetro.
        
        Args:
            nuevo_valor: El nuevo valor numérico
            nueva_unidad: La nueva unidad (opcional)
            
        Raises:
            DomainValidationError: Si el nuevo valor no es válido
        """
        try:
            if nueva_unidad is not None:
                nuevo_parametro_valor = ParametroValor(nuevo_valor, nueva_unidad)
            else:
                nuevo_parametro_valor = ParametroValor(nuevo_valor, self.valor.unidad)
            
            self.valor = nuevo_parametro_valor
            self.updated_at = datetime.utcnow()
        except DomainValidationError:
            raise
    
    def change_metrica(self, nueva_metrica_id: int) -> None:
        """
        Cambia la métrica a la que pertenece este parámetro.
        
        Args:
            nueva_metrica_id: ID de la nueva métrica
            
        Raises:
            DomainValidationError: Si el ID no es válido
        """
        if not nueva_metrica_id or nueva_metrica_id <= 0:
            raise DomainValidationError("El ID de métrica debe ser positivo")
        
        self.metrica_id = nueva_metrica_id
        self.updated_at = datetime.utcnow()
    
    def is_nombre_unique_in_metrica(self, existing_nombres_in_metrica: List[str]) -> bool:
        """
        Verifica si el nombre es único dentro de la misma métrica.
        
        Args:
            existing_nombres_in_metrica: Lista de nombres existentes en la misma métrica
            
        Returns:
            True si el nombre es único en la métrica, False en caso contrario
        """
        return self.nombre.lower() not in [nombre.lower() for nombre in existing_nombres_in_metrica]
    
    def can_be_deleted(self, has_feedbacks: bool) -> bool:
        """
        Determina si el parámetro puede ser eliminado.
        
        Args:
            has_feedbacks: True si tiene feedbacks asociados
            
        Returns:
            True si puede ser eliminado, False en caso contrario
        """
        return not has_feedbacks
    
    def is_related_to_metrica(self, metrica_id: int) -> bool:
        """
        Verifica si este parámetro pertenece a la métrica especificada.
        
        Args:
            metrica_id: ID de la métrica a verificar
            
        Returns:
            True si pertenece a la métrica especificada
        """
        return self.metrica_id == metrica_id
    
    def is_valor_in_range(self, minimo: float, maximo: float) -> bool:
        """
        Verifica si el valor del parámetro está dentro del rango especificado.
        
        Args:
            minimo: Valor mínimo del rango
            maximo: Valor máximo del rango
            
        Returns:
            True si está en el rango
        """
        return self.valor.esta_en_rango(minimo, maximo)
    
    def get_valor_formateado(self) -> str:
        """
        Obtiene el valor formateado con su unidad.
        
        Returns:
            String con el valor y unidad formateados
        """
        return self.valor.valor_formateado
    
    def round_valor(self, decimales: int = 2) -> None:
        """
        Redondea el valor del parámetro.
        
        Args:
            decimales: Número de decimales para redondear
        """
        self.valor = self.valor.redondear(decimales)
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"Parametro(id={self.id}, nombre='{self.nombre}', valor={self.valor}, metrica_id={self.metrica_id})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Parametro):
            return False
        return self.id == other.id if self.id and other.id else (
            self.nombre == other.nombre and self.metrica_id == other.metrica_id
        )
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash((self.nombre, self.metrica_id))
