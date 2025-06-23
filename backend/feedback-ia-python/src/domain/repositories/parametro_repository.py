# filepath: /src/domain/repositories/parametro_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.parametro import Parametro


class ParametroRepositoryInterface(ABC):
    """
    Interfaz del repositorio para la entidad Parametro.
    
    Define las operaciones de persistencia para parámetros
    siguiendo el patrón Repository y el principio de inversión de dependencias.
    """
    
    @abstractmethod
    async def create(self, parametro: Parametro) -> Parametro:
        """
        Crea un nuevo parámetro en el repositorio.
        
        Args:
            parametro: Entidad Parametro a crear
            
        Returns:
            Parametro creado con ID asignado
            
        Raises:
            RepositoryError: Si ocurre un error en la persistencia
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Parametro]:
        """
        Obtiene un parámetro por su ID.
        
        Args:
            id: ID del parámetro a buscar
            
        Returns:
            Parametro encontrado o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_nombre_and_metrica(self, nombre: str, metrica_id: int) -> Optional[Parametro]:
        """
        Obtiene un parámetro por su nombre y métrica.
        
        Args:
            nombre: Nombre del parámetro a buscar
            metrica_id: ID de la métrica
            
        Returns:
            Parametro encontrado o None si no existe
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Parametro]:
        """
        Obtiene todos los parámetros con paginación.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_metrica(self, metrica_id: int, skip: int = 0, limit: int = 100) -> List[Parametro]:
        """
        Obtiene parámetros por métrica.
        
        Args:
            metrica_id: ID de la métrica
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro de la métrica especificada
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_valor_range(
        self, 
        valor_min: float, 
        valor_max: float, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Parametro]:
        """
        Obtiene parámetros dentro de un rango de valores.
        
        Args:
            valor_min: Valor mínimo del rango
            valor_max: Valor máximo del rango
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro en el rango especificado
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def update(self, parametro: Parametro) -> Parametro:
        """
        Actualiza un parámetro existente.
        
        Args:
            parametro: Entidad Parametro con los datos actualizados
            
        Returns:
            Parametro actualizado
            
        Raises:
            RepositoryError: Si ocurre un error en la actualización
            EntityNotFoundError: Si el parámetro no existe
        """
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """
        Elimina un parámetro por su ID.
        
        Args:
            id: ID del parámetro a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
            
        Raises:
            RepositoryError: Si ocurre un error en la eliminación
        """
        pass
    
    @abstractmethod
    async def exists_by_nombre_in_metrica(
        self, 
        nombre: str, 
        metrica_id: int, 
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si existe un parámetro con el nombre especificado en la métrica dada.
        
        Args:
            nombre: Nombre a verificar
            metrica_id: ID de la métrica
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
        Cuenta el total de parámetros.
        
        Returns:
            Número total de parámetros
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def count_by_metrica(self, metrica_id: int) -> int:
        """
        Cuenta los parámetros por métrica.
        
        Args:
            metrica_id: ID de la métrica
            
        Returns:
            Número de parámetros de la métrica especificada
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def has_feedbacks(self, id: int) -> bool:
        """
        Verifica si el parámetro tiene feedbacks asociados.
        
        Args:
            id: ID del parámetro a verificar
            
        Returns:
            True si tiene feedbacks asociados, False en caso contrario
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre(self, nombre_parcial: str, skip: int = 0, limit: int = 100) -> List[Parametro]:
        """
        Busca parámetros por nombre parcial.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro que coinciden con la búsqueda
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def search_by_nombre_in_metrica(
        self, 
        nombre_parcial: str, 
        metrica_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Parametro]:
        """
        Busca parámetros por nombre parcial dentro de una métrica específica.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            metrica_id: ID de la métrica
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro que coinciden con la búsqueda en la métrica especificada
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
    
    @abstractmethod
    async def get_by_unidad(self, unidad: str, skip: int = 0, limit: int = 100) -> List[Parametro]:
        """
        Obtiene parámetros por unidad de medida.
        
        Args:
            unidad: Unidad de medida a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de Parametro con la unidad especificada
            
        Raises:
            RepositoryError: Si ocurre un error en la consulta
        """
        pass
