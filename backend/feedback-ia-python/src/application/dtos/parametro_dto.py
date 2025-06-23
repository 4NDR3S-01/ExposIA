# filepath: /src/application/dtos/parametro_dto.py
"""
Data Transfer Objects (DTOs) para Parametro.
Objetos para transferir datos entre capas de la aplicación.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ...domain.entities.parametro import Parametro


@dataclass
class CreateParametroDTO:
    """DTO para crear un nuevo parámetro."""
    
    nombre: str
    valor: float
    unidad: Optional[str] = None
    metrica_id: int
    descripcion: Optional[str] = None
    rango_min: Optional[float] = None
    rango_max: Optional[float] = None
    
    def validate(self) -> None:
        """Valida los datos del DTO."""
        if not self.nombre or self.nombre.strip() == "":
            raise ValueError("El nombre es requerido")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        if self.metrica_id <= 0:
            raise ValueError("El ID de métrica debe ser mayor a 0")
        
        if self.descripcion and len(self.descripcion) > 500:
            raise ValueError("La descripción no puede exceder 500 caracteres")
        
        if self.unidad and len(self.unidad) > 50:
            raise ValueError("La unidad no puede exceder 50 caracteres")
        
        if self.rango_min is not None and self.rango_max is not None:
            if self.rango_min >= self.rango_max:
                raise ValueError("El rango mínimo debe ser menor que el máximo")
            
            if not (self.rango_min <= self.valor <= self.rango_max):
                raise ValueError("El valor debe estar dentro del rango especificado")


@dataclass
class UpdateParametroDTO:
    """DTO para actualizar un parámetro existente."""
    
    nombre: Optional[str] = None
    valor: Optional[float] = None
    unidad: Optional[str] = None
    metrica_id: Optional[int] = None
    descripcion: Optional[str] = None
    rango_min: Optional[float] = None
    rango_max: Optional[float] = None
    
    def has_changes(self) -> bool:
        """Verifica si hay cambios en el DTO."""
        return any([
            self.nombre is not None,
            self.valor is not None,
            self.unidad is not None,
            self.metrica_id is not None,
            self.descripcion is not None,
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
        
        if self.metrica_id is not None and self.metrica_id <= 0:
            raise ValueError("El ID de métrica debe ser mayor a 0")
        
        if self.descripcion is not None and len(self.descripcion) > 500:
            raise ValueError("La descripción no puede exceder 500 caracteres")
        
        if self.unidad is not None and len(self.unidad) > 50:
            raise ValueError("La unidad no puede exceder 50 caracteres")


@dataclass
class ParametroResponseDTO:
    """DTO de respuesta para parámetro."""
    
    id: int
    nombre: str
    valor: float
    unidad: Optional[str]
    metrica_id: int
    metrica_nombre: Optional[str]
    descripcion: Optional[str]
    rango_min: Optional[float]
    rango_max: Optional[float]
    total_feedbacks: int
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, parametro: Parametro) -> 'ParametroResponseDTO':
        """Crea un DTO de respuesta desde una entidad de dominio."""
        return cls(
            id=parametro.id,
            nombre=parametro.nombre,
            valor=parametro.valor.value,
            unidad=parametro.valor.unidad,
            metrica_id=parametro.metrica_id,
            metrica_nombre=parametro.metrica.nombre if parametro.metrica else None,
            descripcion=parametro.descripcion,
            rango_min=parametro.rango_min,
            rango_max=parametro.rango_max,
            total_feedbacks=len(parametro.feedbacks) if parametro.feedbacks else 0,
            created_at=parametro.created_at,
            updated_at=parametro.updated_at
        )
    
    def to_dict(self) -> dict:
        """Convierte el DTO a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'valor': self.valor,
            'unidad': self.unidad,
            'metrica_id': self.metrica_id,
            'metrica_nombre': self.metrica_nombre,
            'descripcion': self.descripcion,
            'rango_min': self.rango_min,
            'rango_max': self.rango_max,
            'total_feedbacks': self.total_feedbacks,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@dataclass
class ParametroFilterDTO:
    """DTO para filtrar parámetros."""
    
    metrica_id: Optional[int] = None
    nombre_like: Optional[str] = None
    unidad: Optional[str] = None
    valor_min: Optional[float] = None
    valor_max: Optional[float] = None
    con_feedbacks: Optional[bool] = None
    skip: int = 0
    limit: int = 100
    
    def validate(self) -> None:
        """Valida los filtros."""
        if self.skip < 0:
            raise ValueError("Skip debe ser mayor o igual a 0")
        
        if self.limit <= 0 or self.limit > 1000:
            raise ValueError("Limit debe estar entre 1 y 1000")
        
        if self.metrica_id is not None and self.metrica_id <= 0:
            raise ValueError("El ID de métrica debe ser mayor a 0")
        
        if (self.valor_min is not None and 
            self.valor_max is not None and 
            self.valor_min > self.valor_max):
            raise ValueError("valor_min no puede ser mayor que valor_max")


@dataclass
class ParametroSummaryDTO:
    """DTO para resumen de parámetros."""
    
    total_parametros: int
    parametros_por_metrica: dict[str, int]
    parametros_con_feedbacks: int
    parametros_sin_feedbacks: int
    valor_promedio: float
    unidades_utilizadas: list[str]


@dataclass
class ValidarParametroDTO:
    """DTO para validar un valor contra un parámetro."""
    
    parametro_id: int
    valor_propuesto: float
    
    def validate(self) -> None:
        """Valida los datos del DTO."""
        if self.parametro_id <= 0:
            raise ValueError("El ID de parámetro debe ser mayor a 0")


@dataclass
class ValidacionResultadoDTO:
    """DTO de resultado de validación de parámetro."""
    
    parametro_id: int
    valor_propuesto: float
    es_valido: bool
    mensaje: str
    valor_sugerido: Optional[float] = None
    porcentaje_desviacion: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convierte el DTO a diccionario."""
        return {
            'parametro_id': self.parametro_id,
            'valor_propuesto': self.valor_propuesto,
            'es_valido': self.es_valido,
            'mensaje': self.mensaje,
            'valor_sugerido': self.valor_sugerido,
            'porcentaje_desviacion': self.porcentaje_desviacion
        }
