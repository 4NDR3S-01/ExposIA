# filepath: /src/infrastructure/middleware/auth_middleware.py
"""
Middleware de autenticación para validar tokens de acceso.
"""
import os
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

# Configuración del token
security = HTTPBearer()

class AuthMiddleware:
    """
    Middleware para validar autenticación por token Bearer.
    """
    
    def __init__(self):
        self.expected_token = os.getenv("API_KEY")
        if not self.expected_token:
            raise ValueError("API_KEY no configurado en variables de entorno")
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """
        Verifica que el token proporcionado sea válido.
        
        Args:
            credentials: Credenciales de autorización Bearer
            
        Returns:
            Token válido
            
        Raises:
            HTTPException: Si el token es inválido o faltante
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorización requerido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if credentials.credentials != self.expected_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return credentials.credentials


# Instancia global del middleware
auth_middleware = AuthMiddleware()

# Dependencia para usar en los endpoints
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependencia de FastAPI para verificar el token de API.
    
    Args:
        credentials: Credenciales Bearer del header Authorization
        
    Returns:
        Token válido
        
    Raises:
        HTTPException: Si el token es inválido
    """
    return auth_middleware.verify_token(credentials)


def get_optional_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[str]:
    """
    Dependencia opcional para endpoints que pueden funcionar con o sin token.
    
    Args:
        credentials: Credenciales Bearer opcionales
        
    Returns:
        Token si es válido, None si no se proporciona
        
    Raises:
        HTTPException: Si se proporciona un token pero es inválido
    """
    if not credentials:
        return None
    
    return auth_middleware.verify_token(credentials)
