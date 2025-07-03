# filepath: /src/domain/entities/grabacion.py
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from ..exceptions.validation_exceptions import DomainValidationError
from ..value_objects.archivo_audio import ArchivoAudio


@dataclass
class Grabacion:
    """
    Entidad de dominio que representa una grabación de audio.
    
    Una grabación contiene información sobre un archivo de audio
    que será analizado para generar feedbacks.
    """
    
    id: Optional[int]
    archivo_audio: ArchivoAudio
    fecha_grabacion: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validación después de la inicialización."""
        self._validate()
    
    def _validate(self) -> None:
        """Valida la entidad según las reglas de negocio."""
        if not isinstance(self.archivo_audio, ArchivoAudio):
            raise DomainValidationError("El archivo de audio debe ser una instancia de ArchivoAudio")
        
        if self.fecha_grabacion and self.fecha_grabacion > datetime.now():
            raise DomainValidationError("La fecha de grabación no puede ser futura")
    
    def update_archivo_audio(
        self, 
        nuevo_nombre: str, 
        nueva_ruta: str, 
        nuevo_formato: Optional[str] = None,
        nueva_duracion: Optional[float] = None
    ) -> None:
        """
        Actualiza la información del archivo de audio.
        
        Args:
            nuevo_nombre: Nuevo nombre del archivo
            nueva_ruta: Nueva ruta del archivo
            nuevo_formato: Nuevo formato del archivo (opcional)
            nueva_duracion: Nueva duración en segundos (opcional)
            
        Raises:
            DomainValidationError: Si los nuevos datos no son válidos
        """
        try:
            nuevo_archivo = ArchivoAudio(
                nombre_archivo=nuevo_nombre,
                ruta_archivo=nueva_ruta,
                formato=nuevo_formato,
                duracion=nueva_duracion
            )
            self.archivo_audio = nuevo_archivo
            self.updated_at = datetime.utcnow()
        except DomainValidationError:
            raise
    
    def update_fecha_grabacion(self, nueva_fecha: Optional[datetime]) -> None:
        """
        Actualiza la fecha de grabación.
        
        Args:
            nueva_fecha: Nueva fecha de grabación o None
            
        Raises:
            DomainValidationError: Si la fecha no es válida
        """
        if nueva_fecha and nueva_fecha > datetime.now():
            raise DomainValidationError("La fecha de grabación no puede ser futura")
        
        self.fecha_grabacion = nueva_fecha
        self.updated_at = datetime.utcnow()
    
    def can_be_deleted(self, has_feedbacks: bool) -> bool:
        """
        Determina si la grabación puede ser eliminada.
        
        Args:
            has_feedbacks: True si tiene feedbacks asociados
            
        Returns:
            True si puede ser eliminada, False en caso contrario
        """
        return not has_feedbacks
    
    def is_archivo_valido(self) -> bool:
        """
        Verifica si el archivo de audio es válido para procesamiento.
        
        Returns:
            True si el archivo es válido para análisis
        """
        return (
            self.archivo_audio.es_formato_valido and
            not self.archivo_audio.es_archivo_corto(5.0) and  # Mínimo 5 segundos
            not self.archivo_audio.es_archivo_largo(3600.0)   # Máximo 1 hora
        )
    
    def get_duracion_minutos(self) -> Optional[float]:
        """
        Obtiene la duración en minutos.
        
        Returns:
            Duración en minutos o None si no está disponible
        """
        if self.archivo_audio.duracion is None:
            return None
        return round(self.archivo_audio.duracion / 60, 2)
    
    def is_grabacion_reciente(self, dias_umbral: int = 30) -> bool:
        """
        Verifica si la grabación es reciente.
        
        Args:
            dias_umbral: Número de días para considerar una grabación como reciente
            
        Returns:
            True si es reciente, False en caso contrario
        """
        if not self.fecha_grabacion:
            return False
        
        diferencia = datetime.now() - self.fecha_grabacion
        return diferencia.days <= dias_umbral
    
    def get_info_archivo(self) -> str:
        """
        Obtiene información resumida del archivo.
        
        Returns:
            String con información del archivo
        """
        return self.archivo_audio.get_info_resumen()
    
    def get_nombre_archivo_sanitizado(self) -> str:
        """
        Obtiene el nombre del archivo sin caracteres especiales.
        
        Returns:
            Nombre del archivo sanitizado
        """
        import re
        nombre = self.archivo_audio.nombre_sin_extension
        # Remover caracteres especiales y espacios
        nombre_sanitizado = re.sub(r'[^\w\-_.]', '_', nombre)
        return nombre_sanitizado
    
    def is_formato_comprimido(self) -> bool:
        """
        Verifica si el formato del archivo es comprimido.
        
        Returns:
            True si es un formato comprimido
        """
        formatos_comprimidos = {'.mp3', '.aac', '.ogg', '.m4a', '.wma', '.opus'}
        formato = self.archivo_audio.formato or self.archivo_audio.extension
        
        if not formato:
            return False
        
        formato_normalizado = formato.lower()
        if not formato_normalizado.startswith('.'):
            formato_normalizado = '.' + formato_normalizado
        
        return formato_normalizado in formatos_comprimidos
    
    def requires_conversion(self) -> bool:
        """
        Determina si el archivo requiere conversión para procesamiento.
        
        Returns:
            True si requiere conversión
        """
        # Formatos preferidos para procesamiento
        formatos_preferidos = {'.wav', '.flac'}
        formato = self.archivo_audio.formato or self.archivo_audio.extension
        
        if not formato:
            return True
        
        formato_normalizado = formato.lower()
        if not formato_normalizado.startswith('.'):
            formato_normalizado = '.' + formato_normalizado
        
        return formato_normalizado not in formatos_preferidos
    
    def estimate_processing_time(self) -> Optional[float]:
        """
        Estima el tiempo de procesamiento en segundos.
        Esto es una estimación basada en la duración del archivo.
        
        Returns:
            Tiempo estimado en segundos o None si no se puede calcular
        """
        if self.archivo_audio.duracion is None:
            return None
        
        # Factor de procesamiento (aproximadamente 0.1x la duración real)
        factor_procesamiento = 0.1
        
        if self.is_formato_comprimido():
            # Los formatos comprimidos requieren más tiempo para decodificar
            factor_procesamiento *= 1.5
        
        return self.archivo_audio.duracion * factor_procesamiento
    
    def __str__(self) -> str:
        return f"Grabacion(id={self.id}, archivo='{self.archivo_audio.nombre_archivo}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Grabacion):
            return False
        return self.id == other.id if self.id and other.id else (
            self.archivo_audio.nombre_archivo == other.archivo_audio.nombre_archivo and
            self.archivo_audio.ruta_archivo == other.archivo_audio.ruta_archivo
        )
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash((
            self.archivo_audio.nombre_archivo, 
            self.archivo_audio.ruta_archivo
        ))
