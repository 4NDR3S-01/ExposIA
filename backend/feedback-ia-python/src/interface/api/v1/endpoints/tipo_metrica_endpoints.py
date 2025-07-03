# filepath: /src/interface/api/v1/endpoints/tipo_metrica_endpoints.py
"""
Endpoints REST para TipoMetrica.
Controladores de la capa de interfaz que manejan las peticiones HTTP.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....application.dtos.tipo_metrica_dto import (
    CreateTipoMetricaDTO, 
    TipoMetricaResponseDTO,
    TipoMetricaFilterDTO
)
from ....domain.exceptions.validation_exceptions import (
    DuplicateTipoMetricaError,
    InvalidTipoMetricaDataError,
    TipoMetricaNotFoundError
)
from ....infrastructure.database.connection import get_db
from ..dependencies import require_authentication
from ....services.feedback_service import FeedbackService


router = APIRouter(prefix="/tipos-metrica", tags=["tipos-metrica"])


@router.post(
    "/",
    response_model=TipoMetricaResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo tipo de métrica",
    description="Crea un nuevo tipo de métrica para clasificar métricas de análisis.",
    dependencies=[require_authentication()]
)
async def create_tipo_metrica(
    tipo_metrica_data: CreateTipoMetricaDTO,
    db: Session = Depends(get_db)
) -> TipoMetricaResponseDTO:
    """
    Crea un nuevo tipo de métrica.
    
    Args:
        tipo_metrica_data: Datos del tipo de métrica a crear
        db: Sesión de base de datos
        
    Returns:
        Tipo de métrica creado
        
    Raises:
        HTTPException: 409 si ya existe un tipo con ese nombre
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.create_tipo_metrica(db, tipo_metrica_data)
        return result
        
    except DuplicateTipoMetricaError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un tipo de métrica con ese nombre: {str(e)}"
        )
    except InvalidTipoMetricaDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de tipo de métrica inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[TipoMetricaResponseDTO],
    summary="Listar tipos de métrica",
    description="Obtiene una lista paginada de todos los tipos de métrica.",
    dependencies=[require_authentication()]
)
async def get_tipos_metrica(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[TipoMetricaResponseDTO]:
    """
    Obtiene lista de tipos de métrica.
    
    Args:
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        db: Sesión de base de datos
        
    Returns:
        Lista de tipos de métrica
    """
    try:
        return FeedbackService.get_tipos_metrica(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{tipo_metrica_id}",
    response_model=TipoMetricaResponseDTO,
    summary="Obtener tipo de métrica por ID",
    description="Obtiene un tipo de métrica específico por su ID.",
    dependencies=[require_authentication()]
)
async def get_tipo_metrica(
    tipo_metrica_id: int,
    db: Session = Depends(get_db)
) -> TipoMetricaResponseDTO:
    """
    Obtiene un tipo de métrica por su ID.
    
    Args:
        tipo_metrica_id: ID del tipo de métrica a obtener
        db: Sesión de base de datos
        
    Returns:
        Tipo de métrica encontrado
        
    Raises:
        HTTPException: 404 si el tipo de métrica no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.get_tipo_metrica_by_id(db, tipo_metrica_id)
        if not result:
            raise TipoMetricaNotFoundError(f"Tipo de métrica con ID {tipo_metrica_id} no encontrado")
        return result
        
    except TipoMetricaNotFoundError as e:
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
    "/{tipo_metrica_id}",
    response_model=TipoMetricaResponseDTO,
    summary="Actualizar tipo de métrica",
    description="Actualiza un tipo de métrica existente.",
    dependencies=[require_authentication()]
)
async def update_tipo_metrica(
    tipo_metrica_id: int,
    tipo_metrica_data: CreateTipoMetricaDTO,
    db: Session = Depends(get_db)
) -> TipoMetricaResponseDTO:
    """
    Actualiza un tipo de métrica existente.
    
    Args:
        tipo_metrica_id: ID del tipo de métrica a actualizar
        tipo_metrica_data: Nuevos datos del tipo de métrica
        db: Sesión de base de datos
        
    Returns:
        Tipo de métrica actualizado
        
    Raises:
        HTTPException: 404 si el tipo de métrica no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.update_tipo_metrica(db, tipo_metrica_id, tipo_metrica_data)
        if not result:
            raise TipoMetricaNotFoundError(f"Tipo de métrica con ID {tipo_metrica_id} no encontrado")
        return result
        
    except TipoMetricaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidTipoMetricaDataError as e:
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
    "/{tipo_metrica_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tipo de métrica",
    description="Elimina un tipo de métrica y todas sus métricas asociadas.",
    dependencies=[require_authentication()]
)
async def delete_tipo_metrica(
    tipo_metrica_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un tipo de métrica.
    
    Args:
        tipo_metrica_id: ID del tipo de métrica a eliminar
        db: Sesión de base de datos
        
    Raises:
        HTTPException: 404 si el tipo de métrica no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        success = FeedbackService.delete_tipo_metrica(db, tipo_metrica_id)
        if not success:
            raise TipoMetricaNotFoundError(f"Tipo de métrica con ID {tipo_metrica_id} no encontrado")
            
    except TipoMetricaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
