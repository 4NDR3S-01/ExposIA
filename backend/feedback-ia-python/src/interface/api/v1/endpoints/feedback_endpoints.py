"""
Endpoints REST para Feedback.
Controladores de la capa de interfaz que manejan las peticiones HTTP.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....application.use_cases.feedback.create_feedback import CreateFeedbackUseCase
from ....application.use_cases.feedback.generate_ai_feedback import GenerateAIFeedbackUseCase
from ....application.dtos.feedback_dto import (
    CreateFeedbackDTO, 
    FeedbackResponseDTO,
    GenerateAIFeedbackDTO,
    FeedbackFilterDTO
)
from ....domain.exceptions.validation_exceptions import (
    DuplicateFeedbackError,
    InvalidFeedbackDataError,
    FeedbackNotFoundError,
    AIServiceError
)
from ....infrastructure.database.connection import get_db
from ..dependencies import get_feedback_use_cases, require_authentication


router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])


@router.post(
    "/",
    response_model=FeedbackResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo feedback",
    description="Crea un nuevo feedback manual o automático para una grabación y parámetro específicos.",
    dependencies=[require_authentication()]
)
async def create_feedback(
    feedback_data: CreateFeedbackDTO,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> FeedbackResponseDTO:
    """
    Crea un nuevo feedback.
    
    Args:
        feedback_data: Datos del feedback a crear
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Feedback creado
        
    Raises:
        HTTPException: 400 si los datos son inválidos o hay duplicados
        HTTPException: 500 si ocurre un error interno
    """
    try:
        create_use_case: CreateFeedbackUseCase = use_cases["create_feedback"]
        result = await create_use_case.execute(feedback_data)
        return result
        
    except DuplicateFeedbackError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un feedback para esta grabación y parámetro: {str(e)}"
        )
    except InvalidFeedbackDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de feedback inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post(
    "/generate-ai",
    response_model=List[FeedbackResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Generar feedback con IA",
    description="Genera feedback automáticamente usando análisis de IA para una grabación.",
    dependencies=[require_authentication()]
)
async def generate_ai_feedback(
    generate_data: GenerateAIFeedbackDTO,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> List[FeedbackResponseDTO]:
    """
    Genera feedback automático usando IA.
    
    Args:
        generate_data: Datos para la generación de feedback
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Lista de feedbacks generados
        
    Raises:
        HTTPException: 400 si los datos son inválidos
        HTTPException: 502 si falla el servicio de IA
        HTTPException: 500 si ocurre un error interno
    """
    try:
        generate_use_case: GenerateAIFeedbackUseCase = use_cases["generate_ai_feedback"]
        results = await generate_use_case.execute(generate_data)
        return results
        
    except InvalidFeedbackDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos inválidos: {str(e)}"
        )
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en servicio de IA: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponseDTO,
    summary="Obtener feedback por ID",
    description="Obtiene un feedback específico por su ID.",
    dependencies=[require_authentication()]
)
async def get_feedback(
    feedback_id: int,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> FeedbackResponseDTO:
    """
    Obtiene un feedback por su ID.
    
    Args:
        feedback_id: ID del feedback a obtener
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Feedback encontrado
        
    Raises:
        HTTPException: 404 si el feedback no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        get_use_case = use_cases["get_feedback"]
        result = await get_use_case.execute(feedback_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback con ID {feedback_id} no encontrado"
            )
        
        return result
        
    except FeedbackNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback con ID {feedback_id} no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[FeedbackResponseDTO],
    summary="Listar feedbacks",
    description="Obtiene una lista de feedbacks con filtros opcionales y paginación.",
    dependencies=[require_authentication()]
)
async def list_feedbacks(
    grabacion_id: int = None,
    parametro_id: int = None,
    es_manual: bool = None,
    skip: int = 0,
    limit: int = 100,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> List[FeedbackResponseDTO]:
    """
    Lista feedbacks con filtros opcionales.
    
    Args:
        grabacion_id: Filtrar por ID de grabación (opcional)
        parametro_id: Filtrar por ID de parámetro (opcional)
        es_manual: Filtrar por tipo manual/automático (opcional)
        skip: Número de elementos a saltar para paginación
        limit: Número máximo de elementos a retornar
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Lista de feedbacks que cumplen los filtros
        
    Raises:
        HTTPException: 400 si los parámetros son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        # Validar parámetros
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="skip debe ser mayor o igual a 0"
            )
        
        if limit <= 0 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit debe estar entre 1 y 1000"
            )
        
        # Crear DTO de filtros
        filter_dto = FeedbackFilterDTO(
            grabacion_id=grabacion_id,
            parametro_id=parametro_id,
            es_manual=es_manual,
            skip=skip,
            limit=limit
        )
        
        list_use_case = use_cases["list_feedbacks"]
        results = await list_use_case.execute(filter_dto)
        return results
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parámetros inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put(
    "/{feedback_id}",
    response_model=FeedbackResponseDTO,
    summary="Actualizar feedback",
    description="Actualiza un feedback existente.",
    dependencies=[require_authentication()]
)
async def update_feedback(
    feedback_id: int,
    feedback_data: CreateFeedbackDTO,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> FeedbackResponseDTO:
    """
    Actualiza un feedback existente.
    
    Args:
        feedback_id: ID del feedback a actualizar
        feedback_data: Nuevos datos del feedback
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Feedback actualizado
        
    Raises:
        HTTPException: 404 si el feedback no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        update_use_case = use_cases["update_feedback"]
        result = await update_use_case.execute(feedback_id, feedback_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback con ID {feedback_id} no encontrado"
            )
        
        return result
        
    except FeedbackNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback con ID {feedback_id} no encontrado"
        )
    except InvalidFeedbackDataError as e:
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
    "/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar feedback",
    description="Elimina un feedback específico.",
    dependencies=[require_authentication()]
)
async def delete_feedback(
    feedback_id: int,
    use_cases: dict = Depends(get_feedback_use_cases)
):
    """
    Elimina un feedback.
    
    Args:
        feedback_id: ID del feedback a eliminar
        use_cases: Casos de uso inyectados por dependencia
        
    Raises:
        HTTPException: 404 si el feedback no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        delete_use_case = use_cases["delete_feedback"]
        success = await delete_use_case.execute(feedback_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback con ID {feedback_id} no encontrado"
            )
        
    except FeedbackNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback con ID {feedback_id} no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/grabacion/{grabacion_id}",
    response_model=List[FeedbackResponseDTO],
    summary="Obtener feedbacks por grabación",
    description="Obtiene todos los feedbacks asociados a una grabación específica.",
    dependencies=[require_authentication()]
)
async def get_feedbacks_by_grabacion(
    grabacion_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> List[FeedbackResponseDTO]:
    """
    Obtiene feedbacks de una grabación específica.
    
    Args:
        grabacion_id: ID de la grabación
        skip: Número de elementos a saltar para paginación
        limit: Número máximo de elementos a retornar
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Lista de feedbacks de la grabación
        
    Raises:
        HTTPException: 500 si ocurre un error interno
    """
    try:
        get_by_grabacion_use_case = use_cases["get_feedbacks_by_grabacion"]
        return await get_by_grabacion_use_case.execute(grabacion_id, skip, limit)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/parametro/{parametro_id}",
    response_model=List[FeedbackResponseDTO],
    summary="Obtener feedbacks por parámetro",
    description="Obtiene todos los feedbacks asociados a un parámetro específico.",
    dependencies=[require_authentication()]
)
async def get_feedbacks_by_parametro(
    parametro_id: int,
    skip: int = 0,
    limit: int = 100,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> List[FeedbackResponseDTO]:
    """
    Obtiene feedbacks de un parámetro específico.
    
    Args:
        parametro_id: ID del parámetro
        skip: Número de elementos a saltar para paginación
        limit: Número máximo de elementos a retornar
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Lista de feedbacks del parámetro
        
    Raises:
        HTTPException: 500 si ocurre un error interno
    """
    try:
        get_by_parametro_use_case = use_cases["get_feedbacks_by_parametro"]
        return await get_by_parametro_use_case.execute(parametro_id, skip, limit)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post(
    "/analizar-tendencias",
    summary="Analizar tendencias de feedback",
    description="Analiza tendencias y patrones en los feedbacks.",
    dependencies=[require_authentication()]
)
async def analizar_tendencias_feedback(
    filtros: FeedbackFilterDTO,
    use_cases: dict = Depends(get_feedback_use_cases)
) -> dict:
    """
    Analiza tendencias en los feedbacks.
    
    Args:
        filtros: Filtros para el análisis
        use_cases: Casos de uso inyectados por dependencia
        
    Returns:
        Análisis de tendencias
        
    Raises:
        HTTPException: 500 si ocurre un error interno
    """
    try:
        analizar_use_case = use_cases["analizar_tendencias"]
        return await analizar_use_case.execute(filtros)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
