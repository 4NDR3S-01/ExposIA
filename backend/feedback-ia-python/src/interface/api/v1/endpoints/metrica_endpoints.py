# filepath: /src/interface/api/v1/endpoints/metrica_endpoints.py
"""
Endpoints REST para Metrica.
Controladores de la capa de interfaz que manejan las peticiones HTTP.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....application.dtos.metrica_dto import (
    CreateMetricaDTO, 
    MetricaResponseDTO,
    MetricaFilterDTO
)
from ....domain.exceptions.validation_exceptions import (
    DuplicateMetricaError,
    InvalidMetricaDataError,
    MetricaNotFoundError
)
from ....infrastructure.database.connection import get_db
from ..dependencies import require_authentication
from ....services.feedback_service import FeedbackService


router = APIRouter(prefix="/metricas", tags=["metricas"])


@router.post(
    "/",
    response_model=MetricaResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva métrica",
    description="Crea una nueva métrica asociada a un tipo de métrica.",
    dependencies=[require_authentication()]
)
async def create_metrica(
    metrica_data: CreateMetricaDTO,
    db: Session = Depends(get_db)
) -> MetricaResponseDTO:
    """
    Crea una nueva métrica.
    
    Args:
        metrica_data: Datos de la métrica a crear
        db: Sesión de base de datos
        
    Returns:
        Métrica creada
        
    Raises:
        HTTPException: 409 si ya existe una métrica con ese nombre
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.create_metrica(db, metrica_data)
        return result
        
    except DuplicateMetricaError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una métrica con ese nombre: {str(e)}"
        )
    except InvalidMetricaDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de métrica inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[MetricaResponseDTO],
    summary="Listar métricas",
    description="Obtiene una lista paginada de todas las métricas.",
    dependencies=[require_authentication()]
)
async def get_metricas(
    skip: int = 0,
    limit: int = 100,
    tipo_metrica_id: int = None,
    db: Session = Depends(get_db)
) -> List[MetricaResponseDTO]:
    """
    Obtiene lista de métricas.
    
    Args:
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        tipo_metrica_id: Filtrar por tipo de métrica (opcional)
        db: Sesión de base de datos
        
    Returns:
        Lista de métricas
    """
    try:
        if tipo_metrica_id:
            return FeedbackService.get_metricas_by_tipo(db, tipo_metrica_id, skip=skip, limit=limit)
        else:
            return FeedbackService.get_metricas(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{metrica_id}",
    response_model=MetricaResponseDTO,
    summary="Obtener métrica por ID",
    description="Obtiene una métrica específica por su ID.",
    dependencies=[require_authentication()]
)
async def get_metrica(
    metrica_id: int,
    db: Session = Depends(get_db)
) -> MetricaResponseDTO:
    """
    Obtiene una métrica por su ID.
    
    Args:
        metrica_id: ID de la métrica a obtener
        db: Sesión de base de datos
        
    Returns:
        Métrica encontrada
        
    Raises:
        HTTPException: 404 si la métrica no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.get_metrica_by_id(db, metrica_id)
        if not result:
            raise MetricaNotFoundError(f"Métrica con ID {metrica_id} no encontrada")
        return result
        
    except MetricaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put(
    "/{metrica_id}",
    response_model=MetricaResponseDTO,
    summary="Actualizar métrica",
    description="Actualiza una métrica existente.",
    dependencies=[require_authentication()]
)
async def update_metrica(
    metrica_id: int,
    metrica_data: CreateMetricaDTO,
    db: Session = Depends(get_db)
) -> MetricaResponseDTO:
    """
    Actualiza una métrica existente.
    
    Args:
        metrica_id: ID de la métrica a actualizar
        metrica_data: Nuevos datos de la métrica
        db: Sesión de base de datos
        
    Returns:
        Métrica actualizada
        
    Raises:
        HTTPException: 404 si la métrica no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.update_metrica(db, metrica_id, metrica_data)
        if not result:
            raise MetricaNotFoundError(f"Métrica con ID {metrica_id} no encontrada")
        return result
        
    except MetricaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidMetricaDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete(
    "/{metrica_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar métrica",
    description="Elimina una métrica y todos sus parámetros asociados.",
    dependencies=[require_authentication()]
)
async def delete_metrica(
    metrica_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una métrica.
    
    Args:
        metrica_id: ID de la métrica a eliminar
        db: Sesión de base de datos
        
    Raises:
        HTTPException: 404 si la métrica no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        success = FeedbackService.delete_metrica(db, metrica_id)
        if not success:
            raise MetricaNotFoundError(f"Métrica con ID {metrica_id} no encontrada")
            
    except MetricaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/tipo/{tipo_metrica_id}",
    response_model=List[MetricaResponseDTO],
    summary="Obtener métricas por tipo",
    description="Obtiene todas las métricas de un tipo específico.",
    dependencies=[require_authentication()]
)
async def get_metricas_by_tipo(
    tipo_metrica_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[MetricaResponseDTO]:
    """
    Obtiene métricas por tipo de métrica.
    
    Args:
        tipo_metrica_id: ID del tipo de métrica
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        db: Sesión de base de datos
        
    Returns:
        Lista de métricas del tipo especificado
    """
    try:
        return FeedbackService.get_metricas_by_tipo(db, tipo_metrica_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
