# filepath: /src/application/dtos/tipo_metrica_dto.py
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ...domain.entities.tipo_metrica import TipoMetrica


@dataclass
class CreateTipoMetricaDTO:
    """
    DTO para la creación de tipos de métrica.
    
    Contiene los datos necesarios para crear un nuevo tipo de métrica
    desde la capa de interfaz hacia la aplicación.
    """
    nombre: str
    descripcion: Optional[str] = None
    
    def validate(self) -> None:
        """
        Valida los datos del DTO.
        
        Raises:
            ValueError: Si los datos no son válidos
        """
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre es obligatorio")
        
        if len(self.nombre.strip()) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if self.descripcion and len(self.descripcion) > 1000:
            raise ValueError("La descripción no puede exceder 1000 caracteres")


@dataclass
class UpdateTipoMetricaDTO:
    """
    DTO para la actualización de tipos de métrica.
    
    Contiene los datos que se pueden actualizar en un tipo de métrica existente.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    
    def validate(self) -> None:
        """
        Valida los datos del DTO.
        
        Raises:
            ValueError: Si los datos no son válidos
        """
        if self.nombre is not None:
            if not self.nombre.strip():
                raise ValueError("El nombre no puede estar vacío")
            
            if len(self.nombre.strip()) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if self.descripcion is not None and len(self.descripcion) > 1000:
            raise ValueError("La descripción no puede exceder 1000 caracteres")
    
    def has_changes(self) -> bool:
        """
        Verifica si el DTO contiene cambios.
        
        Returns:
            True si hay cambios para aplicar
        """
        return self.nombre is not None or self.descripcion is not None


@dataclass
class TipoMetricaResponseDTO:
    """
    DTO para las respuestas de tipos de métrica.
    
    Representa los datos de un tipo de métrica que se envían como respuesta
    desde la aplicación hacia la capa de interfaz.
    """
    id: int
    nombre: str
    descripcion: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, tipo_metrica: TipoMetrica) -> 'TipoMetricaResponseDTO':
        """
        Crea un DTO desde una entidad de dominio.
        
        Args:
            tipo_metrica: Entidad TipoMetrica de dominio
            
        Returns:
            TipoMetricaResponseDTO con los datos de la entidad
        """
        return cls(
            id=tipo_metrica.id,
            nombre=tipo_metrica.nombre,
            descripcion=tipo_metrica.descripcion,
            created_at=tipo_metrica.created_at,
            updated_at=tipo_metrica.updated_at
        )


@dataclass
class TipoMetricaListResponseDTO:
    """
    DTO para respuestas de listas de tipos de métrica con metadatos.
    
    Incluye información de paginación y total de elementos.
    """
    items: list[TipoMetricaResponseDTO]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool
    
    @classmethod
    def create(
        cls,
        items: list[TipoMetricaResponseDTO],
        total: int,
        skip: int,
        limit: int
    ) -> 'TipoMetricaListResponseDTO':
        """
        Crea un DTO de lista con metadatos calculados.
        
        Args:
            items: Lista de tipos de métrica
            total: Total de elementos disponibles
            skip: Elementos omitidos
            limit: Límite de elementos por página
            
        Returns:
            TipoMetricaListResponseDTO con metadatos
        """
        has_next = (skip + limit) < total
        has_previous = skip > 0
        
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_next=has_next,
            has_previous=has_previous
        )


@dataclass
class TipoMetricaStatsDTO:
    """
    DTO para estadísticas de tipos de métrica.
    
    Contiene información estadística útil sobre los tipos de métrica.
    """
    total_tipos: int
    tipos_con_metricas: int
    tipos_sin_metricas: int
    promedio_metricas_por_tipo: float
    tipo_mas_utilizado: Optional[str]
    
    @property
    def porcentaje_utilizados(self) -> float:
        """
        Calcula el porcentaje de tipos de métrica que tienen métricas asociadas.
        
        Returns:
            Porcentaje de utilización (0.0 - 100.0)
        """
        if self.total_tipos == 0:
            return 0.0
        return (self.tipos_con_metricas / self.total_tipos) * 100
