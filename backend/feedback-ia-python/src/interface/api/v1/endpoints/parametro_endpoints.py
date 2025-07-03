# filepath: /src/interface/api/v1/endpoints/parametro_endpoints.py
"""
Endpoints REST para Parametro.
Controladores de la capa de interfaz que manejan las peticiones HTTP.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....application.dtos.parametro_dto import (
    CreateParametroDTO, 
    ParametroResponseDTO,
    ParametroFilterDTO
)
from ....domain.exceptions.validation_exceptions import (
    DuplicateParametroError,
    InvalidParametroDataError,
    ParametroNotFoundError
)
from ....infrastructure.database.connection import get_db
from ..dependencies import require_authentication
from ....services.feedback_service import FeedbackService


router = APIRouter(prefix="/parametros", tags=["parametros"])


@router.post(
    "/",
    response_model=ParametroResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo parámetro",
    description="Crea un nuevo parámetro asociado a una métrica.",
    dependencies=[require_authentication()]
)
async def create_parametro(
    parametro_data: CreateParametroDTO,
    db: Session = Depends(get_db)
) -> ParametroResponseDTO:
    """
    Crea un nuevo parámetro.
    
    Args:
        parametro_data: Datos del parámetro a crear
        db: Sesión de base de datos
        
    Returns:
        Parámetro creado
        
    Raises:
        HTTPException: 409 si ya existe un parámetro con ese nombre para la métrica
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.create_parametro(db, parametro_data)
        return result
        
    except DuplicateParametroError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un parámetro con ese nombre para esta métrica: {str(e)}"
        )
    except InvalidParametroDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de parámetro inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[ParametroResponseDTO],
    summary="Listar parámetros",
    description="Obtiene una lista paginada de todos los parámetros.",
    dependencies=[require_authentication()]
)
async def get_parametros(
    skip: int = 0,
    limit: int = 100,
    metrica_id: int = None,
    db: Session = Depends(get_db)
) -> List[ParametroResponseDTO]:
    """
    Obtiene lista de parámetros.
    
    Args:
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        metrica_id: Filtrar por métrica (opcional)
        db: Sesión de base de datos
        
    Returns:
        Lista de parámetros
    """
    try:
        if metrica_id:
            return FeedbackService.get_parametros_by_metrica(db, metrica_id, skip=skip, limit=limit)
        else:
            return FeedbackService.get_parametros(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{parametro_id}",
    response_model=ParametroResponseDTO,
    summary="Obtener parámetro por ID",
    description="Obtiene un parámetro específico por su ID.",
    dependencies=[require_authentication()]
)
async def get_parametro(
    parametro_id: int,
    db: Session = Depends(get_db)
) -> ParametroResponseDTO:
    """
    Obtiene un parámetro por su ID.
    
    Args:
        parametro_id: ID del parámetro a obtener
        db: Sesión de base de datos
        
    Returns:
        Parámetro encontrado
        
    Raises:
        HTTPException: 404 si el parámetro no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.get_parametro_by_id(db, parametro_id)
        if not result:
            raise ParametroNotFoundError(f"Parámetro con ID {parametro_id} no encontrado")
        return result
        
    except ParametroNotFoundError as e:
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
    "/{parametro_id}",
    response_model=ParametroResponseDTO,
    summary="Actualizar parámetro",
    description="Actualiza un parámetro existente.",
    dependencies=[require_authentication()]
)
async def update_parametro(
    parametro_id: int,
    parametro_data: CreateParametroDTO,
    db: Session = Depends(get_db)
) -> ParametroResponseDTO:
    """
    Actualiza un parámetro existente.
    
    Args:
        parametro_id: ID del parámetro a actualizar
        parametro_data: Nuevos datos del parámetro
        db: Sesión de base de datos
        
    Returns:
        Parámetro actualizado
        
    Raises:
        HTTPException: 404 si el parámetro no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.update_parametro(db, parametro_id, parametro_data)
        if not result:
            raise ParametroNotFoundError(f"Parámetro con ID {parametro_id} no encontrado")
        return result
        
    except ParametroNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidParametroDataError as e:
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
    "/{parametro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar parámetro",
    description="Elimina un parámetro y todos sus feedbacks asociados.",
    dependencies=[require_authentication()]
)
async def delete_parametro(
    parametro_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un parámetro.
    
    Args:
        parametro_id: ID del parámetro a eliminar
        db: Sesión de base de datos
        
    Raises:
        HTTPException: 404 si el parámetro no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        success = FeedbackService.delete_parametro(db, parametro_id)
        if not success:
            raise ParametroNotFoundError(f"Parámetro con ID {parametro_id} no encontrado")
            
    except ParametroNotFoundError as e:
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
    "/metrica/{metrica_id}",
    response_model=List[ParametroResponseDTO],
    summary="Obtener parámetros por métrica",
    description="Obtiene todos los parámetros de una métrica específica.",
    dependencies=[require_authentication()]
)
async def get_parametros_by_metrica(
    metrica_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[ParametroResponseDTO]:
    """
    Obtiene parámetros por métrica.
    
    Args:
        metrica_id: ID de la métrica
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        db: Sesión de base de datos
        
    Returns:
        Lista de parámetros de la métrica especificada
    """
    try:
        return FeedbackService.get_parametros_by_metrica(db, metrica_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{parametro_id}/validar-valor",
    summary="Validar valor para parámetro",
    description="Valida si un valor está dentro del rango permitido para el parámetro.",
    dependencies=[require_authentication()]
)
async def validar_valor_parametro(
    parametro_id: int,
    valor: float,
    db: Session = Depends(get_db)
) -> dict:
    """
    Valida un valor para un parámetro específico.
    
    Args:
        parametro_id: ID del parámetro
        valor: Valor a validar
        db: Sesión de base de datos
        
    Returns:
        Resultado de la validación
        
    Raises:
        HTTPException: 404 si el parámetro no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        parametro = FeedbackService.get_parametro_by_id(db, parametro_id)
        if not parametro:
            raise ParametroNotFoundError(f"Parámetro con ID {parametro_id} no encontrado")
            
        # Aquí podríamos implementar lógica de validación específica
        es_valido = True  # Implementar lógica real
        mensaje = "Valor válido" if es_valido else "Valor fuera de rango"
        
        return {
            "parametro_id": parametro_id,
            "valor": valor,
            "es_valido": es_valido,
            "mensaje": mensaje,
            "unidad": parametro.unidad
        }
        
    except ParametroNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
