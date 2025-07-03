# filepath: /src/domain/value_objects/archivo_audio.py
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from ..exceptions.validation_exceptions import DomainValidationError


@dataclass(frozen=True)
class ArchivoAudio:
    """
    Value object que representa las propiedades de un archivo de audio.
    
    Encapsula la lógica de negocio relacionada con archivos de audio,
    incluyendo validaciones de formato, ruta y propiedades físicas.
    """
    
    nombre_archivo: str
    ruta_archivo: str
    formato: Optional[str] = None
    duracion: Optional[float] = None  # en segundos
    
    # Formatos de audio soportados
    FORMATOS_SOPORTADOS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', 
        '.m4a', '.wma', '.opus', '.aiff'
    }
    
    def __post_init__(self):
        """Validación después de la inicialización."""
        self._validate()
    
    def _validate(self) -> None:
        """Valida las propiedades del archivo según las reglas de negocio."""
        # Validar nombre del archivo
        if not self.nombre_archivo or not self.nombre_archivo.strip():
            raise DomainValidationError("El nombre del archivo es obligatorio")
        
        if len(self.nombre_archivo) > 255:
            raise DomainValidationError("El nombre del archivo no puede exceder 255 caracteres")
        
        # Validar ruta del archivo
        if not self.ruta_archivo or not self.ruta_archivo.strip():
            raise DomainValidationError("La ruta del archivo es obligatoria")
        
        if len(self.ruta_archivo) > 500:
            raise DomainValidationError("La ruta del archivo no puede exceder 500 caracteres")
        
        # Validar formato si se proporciona
        if self.formato and not self._is_formato_soportado(self.formato):
            raise DomainValidationError(f"Formato '{self.formato}' no soportado")
        
        # Validar duración si se proporciona
        if self.duracion is not None:
            if not isinstance(self.duracion, (int, float)):
                raise DomainValidationError("La duración debe ser numérica")
            if self.duracion < 0:
                raise DomainValidationError("La duración no puede ser negativa")
            if self.duracion > 86400:  # 24 horas
                raise DomainValidationError("La duración no puede exceder 24 horas")
    
    def _is_formato_soportado(self, formato: str) -> bool:
        """Verifica si el formato está soportado."""
        formato_normalizado = formato.lower()
        if not formato_normalizado.startswith('.'):
            formato_normalizado = '.' + formato_normalizado
        return formato_normalizado in self.FORMATOS_SOPORTADOS
    
    @property
    def extension(self) -> Optional[str]:
        """Obtiene la extensión del archivo desde el nombre."""
        try:
            return Path(self.nombre_archivo).suffix.lower()
        except Exception:
            return None
    
    @property
    def nombre_sin_extension(self) -> str:
        """Obtiene el nombre del archivo sin la extensión."""
        try:
            return Path(self.nombre_archivo).stem
        except Exception:
            return self.nombre_archivo
    
    @property
    def es_formato_valido(self) -> bool:
        """Verifica si el formato del archivo es válido."""
        if self.formato:
            return self._is_formato_soportado(self.formato)
        
        # Si no hay formato explícito, verificar por extensión
        extension = self.extension
        return extension is not None and extension in self.FORMATOS_SOPORTADOS
    
    @property
    def duracion_formateada(self) -> str:
        """
        Retorna la duración formateada en formato HH:MM:SS.
        
        Returns:
            String con la duración formateada o "Desconocida" si no está disponible
        """
        if self.duracion is None:
            return "Desconocida"
        
        horas = int(self.duracion // 3600)
        minutos = int((self.duracion % 3600) // 60)
        segundos = int(self.duracion % 60)
        
        if horas > 0:
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        else:
            return f"{minutos:02d}:{segundos:02d}"
    
    @property
    def tamaño_estimado_mb(self) -> Optional[float]:
        """
        Estima el tamaño del archivo en MB basado en la duración y formato.
        Esto es una estimación aproximada.
        
        Returns:
            Tamaño estimado en MB o None si no se puede calcular
        """
        if self.duracion is None:
            return None
        
        # Bitrates aproximados por formato (kbps)
        bitrates = {
            '.mp3': 128,
            '.wav': 1411,
            '.flac': 800,
            '.aac': 128,
            '.ogg': 112,
            '.m4a': 128,
            '.wma': 128,
            '.opus': 64,
            '.aiff': 1411
        }
        
        formato_archivo = self.formato or self.extension
        if not formato_archivo:
            return None
        
        formato_normalizado = formato_archivo.lower()
        if not formato_normalizado.startswith('.'):
            formato_normalizado = '.' + formato_normalizado
        
        bitrate = bitrates.get(formato_normalizado, 128)  # Default a MP3
        
        # Cálculo: duración_segundos * bitrate_kbps / 8 / 1024
        return round((self.duracion * bitrate / 8 / 1024), 2)
    
    def es_archivo_largo(self, umbral_minutos: float = 10.0) -> bool:
        """
        Verifica si el archivo es considerado largo.
        
        Args:
            umbral_minutos: Umbral en minutos para considerar un archivo largo
            
        Returns:
            True si el archivo es largo, False en caso contrario o si no hay duración
        """
        if self.duracion is None:
            return False
        return self.duracion > (umbral_minutos * 60)
    
    def es_archivo_corto(self, umbral_segundos: float = 5.0) -> bool:
        """
        Verifica si el archivo es considerado muy corto.
        
        Args:
            umbral_segundos: Umbral en segundos para considerar un archivo corto
            
        Returns:
            True si el archivo es muy corto, False en caso contrario o si no hay duración
        """
        if self.duracion is None:
            return False
        return self.duracion < umbral_segundos
    
    def get_info_resumen(self) -> str:
        """
        Obtiene un resumen de la información del archivo.
        
        Returns:
            String con información resumida del archivo
        """
        info_parts = [f"Archivo: {self.nombre_archivo}"]
        
        if self.formato:
            info_parts.append(f"Formato: {self.formato.upper()}")
        elif self.extension:
            info_parts.append(f"Formato: {self.extension.upper()}")
        
        if self.duracion is not None:
            info_parts.append(f"Duración: {self.duracion_formateada}")
        
        tamaño = self.tamaño_estimado_mb
        if tamaño:
            info_parts.append(f"Tamaño estimado: {tamaño} MB")
        
        return " | ".join(info_parts)
    
    def __str__(self) -> str:
        return f"ArchivoAudio(nombre='{self.nombre_archivo}', formato='{self.formato}', duración={self.duracion}s)"
