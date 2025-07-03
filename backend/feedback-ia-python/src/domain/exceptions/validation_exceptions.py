"""
Excepciones específicas del dominio.
Estas excepciones representan violaciones de reglas de negocio.
"""


class DomainException(Exception):
    """Excepción base para todas las excepciones del dominio."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationException(DomainException):
    """Excepción base para errores de validación."""
    pass


class InvalidScoreError(ValidationException):
    """Se lanza cuando un puntaje no está en el rango válido."""
    
    def __init__(self, message: str = "Puntaje inválido"):
        super().__init__(message, "INVALID_SCORE")


class InvalidFeedbackDataError(ValidationException):
    """Se lanza cuando los datos de feedback son inválidos."""
    
    def __init__(self, message: str = "Datos de feedback inválidos"):
        super().__init__(message, "INVALID_FEEDBACK_DATA")


class FeedbackNotFoundError(DomainException):
    """Se lanza cuando no se encuentra un feedback."""
    
    def __init__(self, feedback_id: int):
        message = f"Feedback con ID {feedback_id} no encontrado"
        super().__init__(message, "FEEDBACK_NOT_FOUND")


class GrabacionNotFoundError(DomainException):
    """Se lanza cuando no se encuentra una grabación."""
    
    def __init__(self, grabacion_id: int):
        message = f"Grabación con ID {grabacion_id} no encontrada"
        super().__init__(message, "GRABACION_NOT_FOUND")


class ParametroNotFoundError(DomainException):
    """Se lanza cuando no se encuentra un parámetro."""
    
    def __init__(self, parametro_id: int):
        message = f"Parámetro con ID {parametro_id} no encontrado"
        super().__init__(message, "PARAMETRO_NOT_FOUND")


class MetricaNotFoundError(DomainException):
    """Se lanza cuando no se encuentra una métrica."""
    
    def __init__(self, metrica_id: int):
        message = f"Métrica con ID {metrica_id} no encontrada"
        super().__init__(message, "METRICA_NOT_FOUND")


class TipoMetricaNotFoundError(DomainException):
    """Se lanza cuando no se encuentra un tipo de métrica."""
    
    def __init__(self, tipo_metrica_id: int):
        message = f"Tipo de métrica con ID {tipo_metrica_id} no encontrado"
        super().__init__(message, "TIPO_METRICA_NOT_FOUND")


class DuplicateFeedbackError(DomainException):
    """Se lanza cuando se intenta crear un feedback duplicado."""
    
    def __init__(self, grabacion_id: int, parametro_id: int):
        message = f"Ya existe un feedback para la grabación {grabacion_id} y parámetro {parametro_id}"
        super().__init__(message, "DUPLICATE_FEEDBACK")


class InvalidAudioFileError(DomainException):
    """Se lanza cuando un archivo de audio es inválido."""
    
    def __init__(self, filename: str, reason: str = "Formato no soportado"):
        message = f"Archivo de audio inválido '{filename}': {reason}"
        super().__init__(message, "INVALID_AUDIO_FILE")


class AudioAnalysisError(DomainException):
    """Se lanza cuando falla el análisis de audio."""
    
    def __init__(self, message: str = "Error en el análisis de audio"):
        super().__init__(message, "AUDIO_ANALYSIS_ERROR")


class AIServiceError(DomainException):
    """Se lanza cuando falla el servicio de IA."""
    
    def __init__(self, message: str = "Error en el servicio de IA"):
        super().__init__(message, "AI_SERVICE_ERROR")


class DomainValidationError(ValidationException):
    """Excepción para errores de validación de dominio."""
    
    def __init__(self, message: str = "Error de validación de dominio"):
        super().__init__(message, "DOMAIN_VALIDATION_ERROR")


class RepositoryError(DomainException):
    """Excepción para errores en operaciones de repositorio."""
    
    def __init__(self, message: str = "Error en operación de repositorio"):
        super().__init__(message, "REPOSITORY_ERROR")


class EntityNotFoundError(DomainException):
    """Excepción cuando una entidad no se encuentra."""
    
    def __init__(self, message: str = "Entidad no encontrada"):
        super().__init__(message, "ENTITY_NOT_FOUND")
