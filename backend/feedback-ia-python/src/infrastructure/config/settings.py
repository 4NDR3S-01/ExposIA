# filepath: /src/infrastructure/config/settings.py
"""
Configuración de la aplicación.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig(BaseSettings):
    """Configuración de base de datos."""
    
    url: str = Field(default="sqlite:///./feedback.db", env="DATABASE_URL")
    echo_sql: bool = Field(default=False, env="DATABASE_ECHO")
    pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")


class AuthConfig(BaseSettings):
    """Configuración de autenticación."""
    
    api_key: str = Field(..., env="API_KEY")
    token_algorithm: str = Field(default="HS256", env="TOKEN_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")


class AIConfig(BaseSettings):
    """Configuración de servicios de IA."""
    
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    max_tokens: int = Field(default=1000, env="AI_MAX_TOKENS")
    temperature: float = Field(default=0.7, env="AI_TEMPERATURE")


class AppConfig(BaseSettings):
    """Configuración general de la aplicación."""
    
    title: str = Field(default="Feedback IA API", env="APP_TITLE")
    description: str = Field(default="API para gestión de feedbacks con IA", env="APP_DESCRIPTION")
    version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    
    # Configuraciones de archivo
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    allowed_audio_formats: list = Field(
        default=[".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        env="ALLOWED_AUDIO_FORMATS"
    )
    
    # Rutas de almacenamiento
    upload_directory: str = Field(default="./uploads", env="UPLOAD_DIRECTORY")
    temp_directory: str = Field(default="./temp", env="TEMP_DIRECTORY")


class Settings:
    """Clase principal de configuración que agrupa todas las configuraciones."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.auth = AuthConfig()
        self.ai = AIConfig()
        self.app = AppConfig()
    
    @property
    def is_development(self) -> bool:
        """Verifica si está en modo desarrollo."""
        return self.app.debug
    
    @property
    def is_production(self) -> bool:
        """Verifica si está en modo producción."""
        return not self.app.debug


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """
    Función para obtener las configuraciones.
    Útil para inyección de dependencias.
    """
    return settings
