# filepath: /src/domain/repositories/grabacion_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities.grabacion import Grabacion


class GrabacionRepositoryInterface(ABC):
    """
    Interfaz del repositorio para la entidad Grabacion.
    
    Define las operaciones de persistencia para grabaciones
    siguiendo el patrón Repository y el principio de inversión de dependencias.
    """
    
    @abstractmethod
    async def create(self, grabacion: Grabacion) -> Grabacion:
        """
        Crea una nueva grabación en el repositorio.
        
        Args:
            grabacion: Entidad Grabacion a crear
            
        Returns:
            Grabacion creada con ID asignado
            
        Raises:
            RepositoryError: Si ocurre un error en la persistencia
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Grabacion]:
        """
        Obtiene una grabación por su ID.
        
        Args:
            id: ID de la grabación a buscar
            
        Returns:
            Grabacion encontrada o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_nombre_archivo(self, nombre_archivo: str) -> Optional[Grabacion]:
        """
        Obtiene una grabación por su nombre de archivo.
        
        Args:
            nombre_archivo: Nombre del archivo a buscar
            
        Returns:
            Grabacion encontrada o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_ruta_archivo(self, ruta_archivo: str) -> Optional[Grabacion]:
        """
        Obtiene una grabación por su ruta de archivo.
        
        Args:
            ruta_archivo: Ruta del archivo a buscar
            
        Returns:
            Grabacion encontrada o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Grabacion]:
        """
        Obtiene todas las grabaciones con paginación.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_formato(self, formato: str, skip: int = 0, limit: int = 100) -> List[Grabacion]:
        """
        Obtiene grabaciones por formato de archivo.
        
        Args:
            formato: Formato del archivo a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion con el formato especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_fecha_range(
        self, 
        fecha_inicio: datetime, 
        fecha_fin: datetime, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Grabacion]:
        """
        Obtiene grabaciones dentro de un rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion en el rango de fechas especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_duracion_range(
        self, 
        duracion_min: float, 
        duracion_max: float, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Grabacion]:
        """
        Obtiene grabaciones dentro de un rango de duración.
        
        Args:
            duracion_min: Duración mínima en segundos
            duracion_max: Duración máxima en segundos
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion en el rango de duración especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def update(self, grabacion: Grabacion) -> Grabacion:
        """
        Actualiza una grabación existente.
        
        Args:
            grabacion: Entidad Grabacion con los datos actualizados
            
        Returns:
            Grabacion actualizada
            
        Raises:
            RepositoryError: Si ocurre un error en la actualización
            EntityNotFoundError: Si la grabación no existe
        """
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Elimina una grabación por su ID.
        
        Args:
            id: ID de la grabación a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
            
        Raises:
            RepositoryError: Si ocurre un error en la eliminación
        """
        pass
    
    @abstractmethod
    async def exists_by_ruta_archivo(self, ruta_archivo: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una grabación con la ruta especificada.
        
        Args:
            ruta_archivo: Ruta del archivo a verificar
            exclude_id: ID a excluir de la verificación (para updates)
            
        Returns:
            True si existe, False en caso contrario
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        Cuenta el total de grabaciones.
        
        Returns:
            Número total de grabaciones
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def count_by_formato(self, formato: str) -> int:
        """
        Cuenta las grabaciones por formato.
        
        Args:
            formato: Formato del archivo
            
        Returns:
            Número de grabaciones del formato especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def has_feedbacks(self, id: int) -> bool:
        """
        Verifica si la grabación tiene feedbacks asociados.
        
        Args:
            id: ID de la grabación a verificar
            
        Returns:
            True si tiene feedbacks asociados, False en caso contrario
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre(self, nombre_parcial: str, skip: int = 0, limit: int = 100) -> List[Grabacion]:
        """
        Busca grabaciones por nombre parcial.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion que coinciden con la búsqueda
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_recent_grabaciones(self, days: int = 30, skip: int = 0, limit: int = 100) -> List[Grabacion]:
        """
        Obtiene grabaciones recientes.
        
        Args:
            days: Número de días hacia atrás para considerar "reciente"
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion recientes
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_grabaciones_sin_fecha(self, skip: int = 0, limit: int = 100) -> List[Grabacion]:
        """
        Obtiene grabaciones sin fecha de grabación especificada.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Grabacion sin fecha
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_total_duracion(self) -> float:
        """
        Calcula la duración total de todas las grabaciones.
        
        Returns:
            Duración total en segundos
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
