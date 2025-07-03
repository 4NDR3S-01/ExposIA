# filepath: /src/domain/repositories/metrica_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.metrica import Metrica


class MetricaRepositoryInterface(ABC):
    """
    Interfaz del repositorio para la entidad Metrica.
    
    Define las operaciones de persistencia para métricas
    siguiendo el patrón Repository y el principio de inversión de dependencias.
    """
    
    @abstractmethod
    async def create(self, metrica: Metrica) -> Metrica:
        """
        Crea una nueva métrica en el repositorio.
        
        Args:
            metrica: Entidad Metrica a crear
            
        Returns:
            Metrica creada con ID asignado
            
        Raises:
            RepositoryError: Si ocurre un error en la persistencia
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Metrica]:
        """
        Obtiene una métrica por su ID.
        
        Args:
            id: ID de la métrica a buscar
            
        Returns:
            Metrica encontrada o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_nombre_and_tipo(self, nombre: str, tipo_metrica_id: int) -> Optional[Metrica]:
        """
        Obtiene una métrica por su nombre y tipo de métrica.
        
        Args:
            nombre: Nombre de la métrica a buscar
            tipo_metrica_id: ID del tipo de métrica
            
        Returns:
            Metrica encontrada o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Metrica]:
        """
        Obtiene todas las métricas con paginación.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Metrica
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_tipo_metrica(self, tipo_metrica_id: int, skip: int = 0, limit: int = 100) -> List[Metrica]:
        """
        Obtiene métricas por tipo de métrica.
        
        Args:
            tipo_metrica_id: ID del tipo de métrica
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Metrica del tipo especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def update(self, metrica: Metrica) -> Metrica:
        """
        Actualiza una métrica existente.
        
        Args:
            metrica: Entidad Metrica con los datos actualizados
            
        Returns:
            Metrica actualizada
            
        Raises:
            RepositoryError: Si ocurre un error en la actualización
            EntityNotFoundError: Si la métrica no existe
        """
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Elimina una métrica por su ID.
        
        Args:
            id: ID de la métrica a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
            
        Raises:
            RepositoryError: Si ocurre un error en la eliminación
        """
        pass
    
    @abstractmethod
    async def exists_by_nombre_in_tipo(
        self, 
        nombre: str, 
        tipo_metrica_id: int, 
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si existe una métrica con el nombre especificado en el tipo dado.
        
        Args:
            nombre: Nombre a verificar
            tipo_metrica_id: ID del tipo de métrica
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
        Cuenta el total de métricas.
        
        Returns:
            Número total de métricas
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def count_by_tipo_metrica(self, tipo_metrica_id: int) -> int:
        """
        Cuenta las métricas por tipo de métrica.
        
        Args:
            tipo_metrica_id: ID del tipo de métrica
            
        Returns:
            Número de métricas del tipo especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def has_parametros(self, id: int) -> bool:
        """
        Verifica si la métrica tiene parámetros asociados.
        
        Args:
            id: ID de la métrica a verificar
            
        Returns:
            True si tiene parámetros asociados, False en caso contrario
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre(self, nombre_parcial: str, skip: int = 0, limit: int = 100) -> List[Metrica]:
        """
        Busca métricas por nombre parcial.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Metrica que coinciden con la búsqueda
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre_in_tipo(
        self, 
        nombre_parcial: str, 
        tipo_metrica_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Metrica]:
        """
        Busca métricas por nombre parcial dentro de un tipo específico.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            tipo_metrica_id: ID del tipo de métrica
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Metrica que coinciden con la búsqueda en el tipo especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
