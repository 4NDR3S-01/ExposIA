"""
Sistema de inyección de dependencias para la aplicación.
Configura e inyecta las dependencias necesarias para cada capa.
"""
from typing import Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ...application.use_cases.feedback.create_feedback import CreateFeedbackUseCase
from ...application.use_cases.feedback.generate_ai_feedback import GenerateAIFeedbackUseCase
from ...domain.services.feedback_analyzer import FeedbackAnalyzerService
from ...infrastructure.database.repositories.sqlalchemy_feedback_repository import SQLAlchemyFeedbackRepository
from ...infrastructure.external_services.openai_service import OpenAIService
from ...infrastructure.database.connection import get_db
from ...infrastructure.security import verify_api_key, get_current_token


def get_feedback_repository(db: Session = Depends(get_db)) -> SQLAlchemyFeedbackRepository:
    """
    Inyecta el repositorio de feedback.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        Instancia del repositorio de feedback
    """
    return SQLAlchemyFeedbackRepository(db)


def get_feedback_analyzer() -> FeedbackAnalyzerService:
    """
    Inyecta el servicio analizador de feedback.
    
    Returns:
        Instancia del analizador de feedback
    """
    return FeedbackAnalyzerService()


def get_ai_service() -> OpenAIService:
    """
    Inyecta el servicio de IA.
    
    Returns:
        Instancia del servicio de IA
    """
    return OpenAIService()


def get_create_feedback_use_case(
    repository: SQLAlchemyFeedbackRepository = Depends(get_feedback_repository)
) -> CreateFeedbackUseCase:
    """
    Inyecta el caso de uso para crear feedback.
    
    Args:
        repository: Repositorio de feedback
        
    Returns:
        Instancia del caso de uso
    """
    return CreateFeedbackUseCase(repository)


def get_generate_ai_feedback_use_case(
    repository: SQLAlchemyFeedbackRepository = Depends(get_feedback_repository),
    ai_service: OpenAIService = Depends(get_ai_service),
    analyzer: FeedbackAnalyzerService = Depends(get_feedback_analyzer)
) -> GenerateAIFeedbackUseCase:
    """
    Inyecta el caso de uso para generar feedback con IA.
    
    Args:
        repository: Repositorio de feedback
        ai_service: Servicio de IA
        analyzer: Analizador de feedback
        
    Returns:
        Instancia del caso de uso
    """
    return GenerateAIFeedbackUseCase(repository, ai_service, analyzer)


def get_feedback_use_cases(
    create_use_case: CreateFeedbackUseCase = Depends(get_create_feedback_use_case),
    generate_ai_use_case: GenerateAIFeedbackUseCase = Depends(get_generate_ai_feedback_use_case)
) -> Dict:
    """
    Inyecta todos los casos de uso de feedback.
    
    Args:
        create_use_case: Caso de uso para crear feedback
        generate_ai_use_case: Caso de uso para generar feedback con IA
        
    Returns:
        Diccionario con todos los casos de uso
    """
    return {
        "create_feedback": create_use_case,
        "generate_ai_feedback": generate_ai_use_case,
        # Aquí se pueden agregar más casos de uso según se implementen
        # "get_feedback": get_feedback_use_case,
        # "list_feedbacks": list_feedbacks_use_case,
        # "get_feedbacks_by_grabacion": get_feedbacks_by_grabacion_use_case,
        # "delete_feedback": delete_feedback_use_case,
    }


# === Dependencias de Autenticación ===
security = HTTPBearer()

async def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependencia para obtener el usuario autenticado.
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        Token del usuario autenticado
        
    Raises:
        HTTPException: Si la autenticación falla
    """
    return await verify_api_key(credentials)


def require_authentication():
    """
    Dependencia simple para requerir autenticación.
    Útil para endpoints que solo necesitan verificar autenticación.
    
    Returns:
        Dependencia que requiere autenticación válida
    """
    return Depends(get_authenticated_user)
