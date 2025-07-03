# filepath: /src/application/dtos/metrica_dto.py
"""
Data Transfer Objects (DTOs) para Metrica.
Objetos para transferir datos entre capas de la aplicación.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ...domain.entities.metrica import Metrica


@dataclass
class CreateMetricaDTO:
    """DTO para crear una nueva métrica."""
    
    nombre: str
    descripcion: Optional[str] = None
    tipo_metrica_id: int
    unidad_medida: Optional[str] = None
    rango_min: Optional[float] = None
    rango_max: Optional[float] = None
    
    def validate(self) -> None:
        """Valida los datos del DTO."""
        if not self.nombre or self.nombre.strip() == "":
            raise ValueError("El nombre es requerido")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if self.tipo_metrica_id <= 0:
            raise ValueError("El ID de tipo de métrica debe ser mayor a 0")
        
        if self.descripcion and len(self.descripcion) > 500:
            raise ValueError("La descripción no puede exceder 500 caracteres")
        
        if self.rango_min is not None and self.rango_max is not None:
            if self.rango_min >= self.rango_max:
                raise ValueError("El rango mínimo debe ser menor que el máximo")


@dataclass
class UpdateMetricaDTO:
    """DTO para actualizar una métrica existente."""
    
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_metrica_id: Optional[int] = None
    unidad_medida: Optional[str] = None
    rango_min: Optional[float] = None
    rango_max: Optional[float] = None
    
    def has_changes(self) -> bool:
        """Verifica si hay cambios en el DTO."""
        return any([
            self.nombre is not None,
            self.descripcion is not None,
            self.tipo_metrica_id is not None,
            self.unidad_medida is not None,
            self.rango_min is not None,
            self.rango_max is not None
        ])
    
    def validate(self) -> None:
        """Valida los datos del DTO."""
        if self.nombre is not None:
            if not self.nombre or self.nombre.strip() == "":
                raise ValueError("El nombre no puede estar vacío")
            if len(self.nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if self.tipo_metrica_id is not None and self.tipo_metrica_id <= 0:
            raise ValueError("El ID de tipo de métrica debe ser mayor a 0")
        
        if self.descripcion is not None and len(self.descripcion) > 500:
            raise ValueError("La descripción no puede exceder 500 caracteres")


@dataclass
class MetricaResponseDTO:
    """DTO de respuesta para métrica."""
    
    id: int
    nombre: str
    descripcion: Optional[str]
    tipo_metrica_id: int
    tipo_metrica_nombre: Optional[str]
    unidad_medida: Optional[str]
    rango_min: Optional[float]
    rango_max: Optional[float]
    total_parametros: int
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, metrica: Metrica) -> 'MetricaResponseDTO':
        """Crea un DTO de respuesta desde una entidad de dominio."""
        return cls(
            id=metrica.id,
            nombre=metrica.nombre,
            descripcion=metrica.descripcion,
            tipo_metrica_id=metrica.tipo_metrica_id,
            tipo_metrica_nombre=metrica.tipo_metrica.nombre if metrica.tipo_metrica else None,
            unidad_medida=metrica.unidad_medida,
            rango_min=metrica.rango_min,
            rango_max=metrica.rango_max,
            total_parametros=len(metrica.parametros) if metrica.parametros else 0,
            created_at=metrica.created_at,
            updated_at=metrica.updated_at
        )
    
    def to_dict(self) -> dict:
        """Convierte el DTO a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo_metrica_id': self.tipo_metrica_id,
            'tipo_metrica_nombre': self.tipo_metrica_nombre,
            'unidad_medida': self.unidad_medida,
            'rango_min': self.rango_min,
            'rango_max': self.rango_max,
            'total_parametros': self.total_parametros,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class MetricaFilterDTO:
    """DTO para filtrar métricas."""
    
    tipo_metrica_id: Optional[int] = None
    nombre_like: Optional[str] = None
    con_parametros: Optional[bool] = None
    skip: int = 0
    limit: int = 100
    
    def validate(self) -> None:
        """Valida los filtros."""
        if self.skip < 0:
            raise ValueError("Skip debe ser mayor o igual a 0")
        
        if self.limit <= 0 or self.limit > 1000:
            raise ValueError("Limit debe estar entre 1 y 1000")
        
        if self.tipo_metrica_id is not None and self.tipo_metrica_id <= 0:
            raise ValueError("El ID de tipo de métrica debe ser mayor a 0")


@dataclass
class MetricaSummaryDTO:
    """DTO para resumen de métricas."""
    
    total_metricas: int
    metricas_por_tipo: dict[str, int]
    metricas_con_parametros: int
    metricas_sin_parametros: int
    promedio_parametros_por_metrica: float
