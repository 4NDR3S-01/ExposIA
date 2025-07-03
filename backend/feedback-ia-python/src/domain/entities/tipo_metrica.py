# filepath: /src/domain/entities/tipo_metrica.py
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from ..exceptions.validation_exceptions import DomainValidationError


@dataclass
class TipoMetrica:
    """
    Entidad de dominio que representa un tipo de métrica.
    
    Un tipo de métrica define una categoría de mediciones que se pueden
    realizar en las grabaciones (ej: "Velocidad", "Tono", "Claridad").
    """
    
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validación y normalización después de la inicialización."""
        self._validate()
        self._normalize()
    
    def _validate(self) -> None:
        """Valida la entidad según las reglas de negocio."""
        if not self.nombre or not self.nombre.strip():
            raise DomainValidationError("El nombre del tipo de métrica es obligatorio")
        
        if len(self.nombre.strip()) > 100:
            raise DomainValidationError("El nombre del tipo de métrica no puede exceder 100 caracteres")
        
        if self.descripcion and len(self.descripcion) > 1000:
            raise DomainValidationError("La descripción no puede exceder 1000 caracteres")
    
    def _normalize(self) -> None:
        """Normaliza los datos de la entidad."""
        self.nombre = self.nombre.strip().title()
        if self.descripcion:
            self.descripcion = self.descripcion.strip()
    
    def update_nombre(self, nuevo_nombre: str) -> None:
        """
        Actualiza el nombre del tipo de métrica.
        
        Args:
            nuevo_nombre: El nuevo nombre para el tipo de métrica
            
        Raises:
            DomainValidationError: Si el nuevo nombre no es válido
        """
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise DomainValidationError("El nombre del tipo de métrica es obligatorio")
        
        if len(nuevo_nombre.strip()) > 100:
            raise DomainValidationError("El nombre del tipo de métrica no puede exceder 100 caracteres")
        
        self.nombre = nuevo_nombre.strip().title()
        self.updated_at = datetime.utcnow()
    
    def update_descripcion(self, nueva_descripcion: Optional[str]) -> None:
        """
        Actualiza la descripción del tipo de métrica.
        
        Args:
            nueva_descripcion: La nueva descripción o None para eliminarla
            
        Raises:
            DomainValidationError: Si la nueva descripción no es válida
        """
        if nueva_descripcion and len(nueva_descripcion) > 1000:
            raise DomainValidationError("La descripción no puede exceder 1000 caracteres")
        
        self.descripcion = nueva_descripcion.strip() if nueva_descripcion else None
        self.updated_at = datetime.utcnow()
    
    def is_nombre_unique_candidate(self, existing_nombres: List[str]) -> bool:
        """
        Verifica si el nombre del tipo de métrica es único entre los existentes.
        
        Args:
            existing_nombres: Lista de nombres existentes en el sistema
            
        Returns:
            True si el nombre es único, False en caso contrario
        """
        return self.nombre.lower() not in [nombre.lower() for nombre in existing_nombres]
    
    def can_be_deleted(self, has_metricas: bool) -> bool:
        """
        Determina si el tipo de métrica puede ser eliminado.
        
        Args:
            has_metricas: True si tiene métricas asociadas
            
        Returns:
            True si puede ser eliminado, False en caso contrario
        """
        return not has_metricas
    
    def __str__(self) -> str:
        return f"TipoMetrica(id={self.id}, nombre='{self.nombre}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TipoMetrica):
            return False
        return self.id == other.id if self.id and other.id else self.nombre == other.nombre
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash(self.nombre)
