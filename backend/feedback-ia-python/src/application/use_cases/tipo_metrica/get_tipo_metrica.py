# filepath: /src/application/use_cases/tipo_metrica/get_tipo_metrica.py
from typing import Optional, List

from ...domain.entities.tipo_metrica import TipoMetrica
from ...domain.repositories.tipo_metrica_repository import TipoMetricaRepositoryInterface
from ...infrastructure.exceptions.repository_exceptions import EntityNotFoundError
from ..dtos.tipo_metrica_dto import TipoMetricaResponseDTO


class GetTipoMetricaUseCase:
    """
    Caso de uso para obtener tipos de métrica.
    
    Proporciona diferentes métodos para consultar tipos de métrica
    con la lógica de negocio aplicada.
    """
    
    def __init__(self, tipo_metrica_repository: TipoMetricaRepositoryInterface):
        self._repository = tipo_metrica_repository
    
    async def get_by_id(self, id: int) -> TipoMetricaResponseDTO:
        """
        Obtiene un tipo de métrica por su ID.
        
        Args:
            id: ID del tipo de métrica
            
        Returns:
            TipoMetricaResponseDTO con los datos del tipo de métrica
            
        Raises:
            EntityNotFoundError: Si el tipo de métrica no existe
        """
        tipo_metrica = await self._repository.get_by_id(id)
        
        if not tipo_metrica:
            raise EntityNotFoundError(f"Tipo de métrica con ID {id} no encontrado")
        
        return TipoMetricaResponseDTO.from_entity(tipo_metrica)
    
    async def get_by_nombre(self, nombre: str) -> Optional[TipoMetricaResponseDTO]:
        """
        Obtiene un tipo de métrica por su nombre.
        
        Args:
            nombre: Nombre del tipo de métrica
            
        Returns:
            TipoMetricaResponseDTO si existe, None en caso contrario
        """
        tipo_metrica = await self._repository.get_by_nombre(nombre)
        
        if not tipo_metrica:
            return None
        
        return TipoMetricaResponseDTO.from_entity(tipo_metrica)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TipoMetricaResponseDTO]:
        """
        Obtiene todos los tipos de métrica con paginación.
        
        Args:
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de TipoMetricaResponseDTO
        """
        tipos_metrica = await self._repository.get_all(skip=skip, limit=limit)
        
        return [TipoMetricaResponseDTO.from_entity(tm) for tm in tipos_metrica]
    
    async def search_by_nombre(self, nombre_parcial: str, skip: int = 0, limit: int = 100) -> List[TipoMetricaResponseDTO]:
        """
        Busca tipos de métrica por nombre parcial.
        
        Args:
            nombre_parcial: Parte del nombre a buscar
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de TipoMetricaResponseDTO que coinciden con la búsqueda
        """
        tipos_metrica = await self._repository.search_by_nombre(
            nombre_parcial=nombre_parcial,
            skip=skip,
            limit=limit
        )
        
        return [TipoMetricaResponseDTO.from_entity(tm) for tm in tipos_metrica]
    
    async def count_total(self) -> int:
        """
        Cuenta el total de tipos de métrica.
        
        Returns:
            Número total de tipos de métrica
        """
        return await self._repository.count()
