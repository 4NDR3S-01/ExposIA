# filepath: /src/domain/repositories/tipo_metrica_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.tipo_metrica import TipoMetrica


class TipoMetricaRepositoryInterface(ABC):
    """
    Interfaz del repositorio para la entidad TipoMetrica.
    
    Define las operaciones de persistencia para tipos de métrica
    siguiendo el patrón Repository y el principio de inversión de dependencias.
    """
    
    @abstractmethod
    async def create(self, tipo_metrica: TipoMetrica) -> TipoMetrica:
        """
        Crea un nuevo tipo de métrica en el repositorio.
        
        Args:
            tipo_metrica: Entidad TipoMetrica a crear
            
        Returns:
            TipoMetrica creado con ID asignado
            
        Raises:
            RepositoryError: Si ocurre un error en la persistencia
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[TipoMetrica]:
        """
        Obtiene un tipo de métrica por su ID.
        
        Args:
            id: ID del tipo de métrica a buscar
            
        Returns:
            TipoMetrica encontrado o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[TipoMetrica]:
        """
        Obtiene un tipo de métrica por su nombre.
        
        Args:
            nombre: Nombre del tipo de métrica a buscar
            
        Returns:
            TipoMetrica encontrado o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TipoMetrica]:
        """
        Obtiene todos los tipos de métrica con paginación.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de TipoMetrica
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def update(self, tipo_metrica: TipoMetrica) -> TipoMetrica:
        """
        Actualiza un tipo de métrica existente.
        
        Args:
            tipo_metrica: Entidad TipoMetrica con los datos actualizados
            
        Returns:
            TipoMetrica actualizado
            
        Raises:
            RepositoryError: Si ocurre un error en la actualización
            EntityNotFoundError: Si el tipo de métrica no existe
        """
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Elimina un tipo de métrica por su ID.
        
        Args:
            id: ID del tipo de métrica a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
            
        Raises:
            RepositoryError: Si ocurre un error en la eliminación
        """
        pass
    
    @abstractmethod
    async def exists_by_nombre(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un tipo de métrica con el nombre especificado.
        
        Args:
            nombre: Nombre a verificar
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
        Cuenta el total de tipos de métrica.
        
        Returns:
            Número total de tipos de métrica
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def has_metricas(self, id: int) -> bool:
        """
        Verifica si el tipo de métrica tiene métricas asociadas.
        
        Args:
            id: ID del tipo de métrica a verificar
            
        Returns:
            True si tiene métricas asociadas, False en caso contrario
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre(self, nombre_parcial: str, skip: int = 0, limit: int = 100) -> List[TipoMetrica]:
        """
        Busca tipos de métrica por nombre parcial.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de TipoMetrica que coinciden con la búsqueda
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
