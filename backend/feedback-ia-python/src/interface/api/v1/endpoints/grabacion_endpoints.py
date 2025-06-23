# filepath: /src/interface/api/v1/endpoints/grabacion_endpoints.py
"""
Endpoints REST para Grabacion.
Controladores de la capa de interfaz que manejan las peticiones HTTP.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from ....application.dtos.grabacion_dto import (
    CreateGrabacionDTO, 
    GrabacionResponseDTO,
    GrabacionFilterDTO
)
from ....domain.exceptions.validation_exceptions import (
    DuplicateGrabacionError,
    InvalidGrabacionDataError,
    GrabacionNotFoundError,
    InvalidAudioFileError
)
from ....infrastructure.database.connection import get_db
from ..dependencies import require_authentication
from ....services.feedback_service import FeedbackService


router = APIRouter(prefix="/grabaciones", tags=["grabaciones"])


@router.post(
    "/",
    response_model=GrabacionResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva grabación",
    description="Crea una nueva grabación de audio para análisis.",
    dependencies=[require_authentication()]
)
async def create_grabacion(
    grabacion_data: CreateGrabacionDTO,
    db: Session = Depends(get_db)
) -> GrabacionResponseDTO:
    """
    Crea una nueva grabación.
    
    Args:
        grabacion_data: Datos de la grabación a crear
        db: Sesión de base de datos
        
    Returns:
        Grabación creada
        
    Raises:
        HTTPException: 409 si ya existe una grabación con ese nombre
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.create_grabacion(db, grabacion_data)
        return result
        
    except DuplicateGrabacionError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una grabación con ese nombre: {str(e)}"
        )
    except InvalidGrabacionDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de grabación inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post(
    "/upload",
    response_model=GrabacionResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Subir archivo de audio",
    description="Sube un archivo de audio y crea una grabación.",
    dependencies=[require_authentication()]
)
async def upload_audio_file(
    file: UploadFile = File(...),
    descripcion: str = None,
    db: Session = Depends(get_db)
) -> GrabacionResponseDTO:
    """
    Sube un archivo de audio y crea la grabación.
    
    Args:
        file: Archivo de audio a subir
        descripcion: Descripción opcional de la grabación
        db: Sesión de base de datos
        
    Returns:
        Grabación creada con el archivo subido
        
    Raises:
        HTTPException: 400 si el archivo no es válido
        HTTPException: 500 si ocurre un error interno
    """
    try:
        # Validar tipo de archivo
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise InvalidAudioFileError("El archivo debe ser de tipo audio")
            
        # Aquí iría la lógica real de guardado del archivo
        # Por ahora simulamos el proceso
        file_path = f"/uploads/audio/{file.filename}"
        
        grabacion_data = CreateGrabacionDTO(
            nombre_archivo=file.filename,
            ruta_archivo=file_path,
            formato=file.content_type.split('/')[-1],
            descripcion=descripcion
        )
        
        result = FeedbackService.create_grabacion(db, grabacion_data)
        return result
        
    except InvalidAudioFileError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[GrabacionResponseDTO],
    summary="Listar grabaciones",
    description="Obtiene una lista paginada de todas las grabaciones.",
    dependencies=[require_authentication()]
)
async def get_grabaciones(
    skip: int = 0,
    limit: int = 100,
    formato: str = None,
    db: Session = Depends(get_db)
) -> List[GrabacionResponseDTO]:
    """
    Obtiene lista de grabaciones.
    
    Args:
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        formato: Filtrar por formato de audio (opcional)
        db: Sesión de base de datos
        
    Returns:
        Lista de grabaciones
    """
    try:
        if formato:
            return FeedbackService.get_grabaciones_by_formato(db, formato, skip=skip, limit=limit)
        else:
            return FeedbackService.get_grabaciones(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "/{grabacion_id}",
    response_model=GrabacionResponseDTO,
    summary="Obtener grabación por ID",
    description="Obtiene una grabación específica por su ID.",
    dependencies=[require_authentication()]
)
async def get_grabacion(
    grabacion_id: int,
    db: Session = Depends(get_db)
) -> GrabacionResponseDTO:
    """
    Obtiene una grabación por su ID.
    
    Args:
        grabacion_id: ID de la grabación a obtener
        db: Sesión de base de datos
        
    Returns:
        Grabación encontrada
        
    Raises:
        HTTPException: 404 si la grabación no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.get_grabacion_by_id(db, grabacion_id)
        if not result:
            raise GrabacionNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
        return result
        
    except GrabacionNotFoundError as e:
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
    "/{grabacion_id}",
    response_model=GrabacionResponseDTO,
    summary="Actualizar grabación",
    description="Actualiza una grabación existente.",
    dependencies=[require_authentication()]
)
async def update_grabacion(
    grabacion_id: int,
    grabacion_data: CreateGrabacionDTO,
    db: Session = Depends(get_db)
) -> GrabacionResponseDTO:
    """
    Actualiza una grabación existente.
    
    Args:
        grabacion_id: ID de la grabación a actualizar
        grabacion_data: Nuevos datos de la grabación
        db: Sesión de base de datos
        
    Returns:
        Grabación actualizada
        
    Raises:
        HTTPException: 404 si la grabación no existe
        HTTPException: 400 si los datos son inválidos
        HTTPException: 500 si ocurre un error interno
    """
    try:
        result = FeedbackService.update_grabacion(db, grabacion_id, grabacion_data)
        if not result:
            raise GrabacionNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
        return result
        
    except GrabacionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidGrabacionDataError as e:
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
    "/{grabacion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar grabación",
    description="Elimina una grabación y todos sus feedbacks asociados.",
    dependencies=[require_authentication()]
)
async def delete_grabacion(
    grabacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una grabación.
    
    Args:
        grabacion_id: ID de la grabación a eliminar
        db: Sesión de base de datos
        
    Raises:
        HTTPException: 404 si la grabación no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        success = FeedbackService.delete_grabacion(db, grabacion_id)
        if not success:
            raise GrabacionNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
            
    except GrabacionNotFoundError as e:
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
    "/{grabacion_id}/feedbacks",
    response_model=List,
    summary="Obtener feedbacks de grabación",
    description="Obtiene todos los feedbacks asociados a una grabación.",
    dependencies=[require_authentication()]
)
async def get_feedbacks_by_grabacion(
    grabacion_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene feedbacks de una grabación específica.
    
    Args:
        grabacion_id: ID de la grabación
        skip: Número de registros a omitir
        limit: Número máximo de registros a retornar
        db: Sesión de base de datos
        
    Returns:
        Lista de feedbacks de la grabación
        
    Raises:
        HTTPException: 404 si la grabación no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        # Verificar que la grabación existe
        grabacion = FeedbackService.get_grabacion_by_id(db, grabacion_id)
        if not grabacion:
            raise GrabacionNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
            
        return FeedbackService.get_feedbacks_by_grabacion(db, grabacion_id, skip=skip, limit=limit)
        
    except GrabacionNotFoundError as e:
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
    "/{grabacion_id}/analizar",
    summary="Analizar calidad de audio",
    description="Analiza la calidad técnica del archivo de audio.",
    dependencies=[require_authentication()]
)
async def analizar_calidad_audio(
    grabacion_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Analiza la calidad del audio de una grabación.
    
    Args:
        grabacion_id: ID de la grabación a analizar
        db: Sesión de base de datos
        
    Returns:
        Análisis de calidad del audio
        
    Raises:
        HTTPException: 404 si la grabación no existe
        HTTPException: 500 si ocurre un error interno
    """
    try:
        grabacion = FeedbackService.get_grabacion_by_id(db, grabacion_id)
        if not grabacion:
            raise GrabacionNotFoundError(f"Grabación con ID {grabacion_id} no encontrada")
            
        # Aquí iría la lógica real de análisis de audio
        # Por ahora retornamos datos simulados
        analisis = {
            "grabacion_id": grabacion_id,
            "calidad_general": "Buena",
            "nivel_ruido": "Bajo",
            "claridad": 8.5,
            "volumen_promedio": 75.2,
            "duracion_analizada": grabacion.duracion or 0,
            "recomendaciones": [
                "El audio tiene buena calidad general",
                "Nivel de ruido aceptable",
                "No se requieren ajustes adicionales"
            ]
        }
        
        return analisis
        
    except GrabacionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
