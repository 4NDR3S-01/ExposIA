# filepath: /src/infrastructure/security/auth_middleware.py
"""
Middleware de autenticación para el módulo feedback-ia-python.
Implementa verificación de token Bearer para proteger endpoints.
"""
import os
from typing import Optional
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class AuthMiddleware:
    """
    Middleware de autenticación que verifica tokens Bearer.
    """
    
    def __init__(self):
        self.security = HTTPBearer()
        self.api_key = os.getenv("API_KEY", "default-api-key-12345")
        self.debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials) -> bool:
        """
        Verifica si el token proporcionado es válido.
        
        Args:
            credentials: Credenciales HTTP con el token Bearer
            
        Returns:
            True si el token es válido, False en caso contrario
        """
        if not credentials:
            return False
        
        # En modo debug, aceptar cualquier token que empiece con "test-"
        if self.debug_mode and credentials.credentials.startswith("test-"):
            return True
        
        # Verificar token contra API_KEY configurada
        return credentials.credentials == self.api_key
    
    async def authenticate_request(self, request: Request) -> None:
        """
        Autentica una solicitud HTTP verificando el token Bearer.
        
        Args:
            request: Objeto Request de FastAPI
            
        Raises:
            HTTPException: Si la autenticación falla
        """
        # Extraer token del header Authorization
        auth_header = request.headers.get("authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorización requerido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Formato de token inválido. Use: Bearer <token>",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = auth_header.split(" ")[1]
        
        # Crear credenciales para verificación
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=token
        )
        
        if not await self.verify_token(credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Instancia global del middleware
auth_middleware = AuthMiddleware()


async def verify_api_key(credentials: HTTPAuthorizationCredentials = None) -> str:
    """
    Función de dependencia para verificar API key en endpoints.
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        Token válido
        
    Raises:
        HTTPException: Si la autenticación falla
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not await auth_middleware.verify_token(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


def get_current_token() -> HTTPBearer:
    """
    Función helper para obtener el esquema de seguridad Bearer.
    
    Returns:
        Instancia de HTTPBearer para dependencias
    """
    return HTTPBearer()
