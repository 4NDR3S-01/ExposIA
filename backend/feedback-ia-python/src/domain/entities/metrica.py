# filepath: /src/domain/entities/metrica.py
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from ..exceptions.validation_exceptions import DomainValidationError


@dataclass
class Metrica:
    """
    Entidad de dominio que representa una métrica específica.
    
    Una métrica es una medición específica dentro de un tipo de métrica
    (ej: "Palabras por minuto" del tipo "Velocidad").
    """
    
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    tipo_metrica_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validación y normalización después de la inicialización."""
        self._validate()
        self._normalize()
    
    def _validate(self) -> None:
        """Valida la entidad según las reglas de negocio."""
        if not self.nombre or not self.nombre.strip():
            raise DomainValidationError("El nombre de la métrica es obligatorio")
        
        if len(self.nombre.strip()) > 100:
            raise DomainValidationError("El nombre de la métrica no puede exceder 100 caracteres")
        
        if self.descripcion and len(self.descripcion) > 1000:
            raise DomainValidationError("La descripción no puede exceder 1000 caracteres")
        
        if not self.tipo_metrica_id or self.tipo_metrica_id <= 0:
            raise DomainValidationError("El tipo de métrica ID es obligatorio y debe ser positivo")
    
    def _normalize(self) -> None:
        """Normaliza los datos de la entidad."""
        self.nombre = self.nombre.strip().title()
        if self.descripcion:
            self.descripcion = self.descripcion.strip()
    
    def update_nombre(self, nuevo_nombre: str) -> None:
        """
        Actualiza el nombre de la métrica.
        
        Args:
            nuevo_nombre: El nuevo nombre para la métrica
            
        Raises:
            DomainValidationError: Si el nuevo nombre no es válido
        """
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise DomainValidationError("El nombre de la métrica es obligatorio")
        
        if len(nuevo_nombre.strip()) > 100:
            raise DomainValidationError("El nombre de la métrica no puede exceder 100 caracteres")
        
        self.nombre = nuevo_nombre.strip().title()
        self.updated_at = datetime.utcnow()
    
    def update_descripcion(self, nueva_descripcion: Optional[str]) -> None:
        """
        Actualiza la descripción de la métrica.
        
        Args:
            nueva_descripcion: La nueva descripción o None para eliminarla
            
        Raises:
            DomainValidationError: Si la nueva descripción no es válida
        """
        if nueva_descripcion and len(nueva_descripcion) > 1000:
            raise DomainValidationError("La descripción no puede exceder 1000 caracteres")
        
        self.descripcion = nueva_descripcion.strip() if nueva_descripcion else None
        self.updated_at = datetime.utcnow()
    
    def change_tipo_metrica(self, nuevo_tipo_metrica_id: int) -> None:
        """
        Cambia el tipo de métrica al que pertenece esta métrica.
        
        Args:
            nuevo_tipo_metrica_id: ID del nuevo tipo de métrica
            
        Raises:
            DomainValidationError: Si el ID no es válido
        """
        if not nuevo_tipo_metrica_id or nuevo_tipo_metrica_id <= 0:
            raise DomainValidationError("El tipo de métrica ID debe ser positivo")
        
        self.tipo_metrica_id = nuevo_tipo_metrica_id
        self.updated_at = datetime.utcnow()
    
    def is_nombre_unique_in_tipo(self, existing_nombres_in_tipo: List[str]) -> bool:
        """
        Verifica si el nombre es único dentro del mismo tipo de métrica.
        
        Args:
            existing_nombres_in_tipo: Lista de nombres existentes en el mismo tipo
            
        Returns:
            True si el nombre es único en el tipo, False en caso contrario
        """
        return self.nombre.lower() not in [nombre.lower() for nombre in existing_nombres_in_tipo]
    
    def can_be_deleted(self, has_parametros: bool) -> bool:
        """
        Determina si la métrica puede ser eliminada.
        
        Args:
            has_parametros: True si tiene parámetros asociados
            
        Returns:
            True si puede ser eliminada, False en caso contrario
        """
        return not has_parametros
    
    def is_related_to_tipo_metrica(self, tipo_metrica_id: int) -> bool:
        """
        Verifica si esta métrica pertenece al tipo de métrica especificado.
        
        Args:
            tipo_metrica_id: ID del tipo de métrica a verificar
            
        Returns:
            True si pertenece al tipo especificado
        """
        return self.tipo_metrica_id == tipo_metrica_id
    
    def __str__(self) -> str:
        return f"Metrica(id={self.id}, nombre='{self.nombre}', tipo_metrica_id={self.tipo_metrica_id})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Metrica):
            return False
        return self.id == other.id if self.id and other.id else (
            self.nombre == other.nombre and self.tipo_metrica_id == other.tipo_metrica_id
        )
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash((self.nombre, self.tipo_metrica_id))
