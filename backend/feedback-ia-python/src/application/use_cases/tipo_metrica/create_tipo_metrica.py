# filepath: /src/application/use_cases/tipo_metrica/create_tipo_metrica.py
from typing import Optional

from ...domain.entities.tipo_metrica import TipoMetrica
from ...domain.repositories.tipo_metrica_repository import TipoMetricaRepositoryInterface
from ...domain.exceptions.validation_exceptions import DomainValidationError
from ...infrastructure.exceptions.repository_exceptions import RepositoryError
from ..dtos.tipo_metrica_dto import CreateTipoMetricaDTO, TipoMetricaResponseDTO


class CreateTipoMetricaUseCase:
    """
    Caso de uso para crear un nuevo tipo de métrica.
    
    Este caso de uso orquesta la creación de tipos de métrica,
    incluyendo validaciones de negocio y persistencia.
    """
    
    def __init__(self, tipo_metrica_repository: TipoMetricaRepositoryInterface):
        self._repository = tipo_metrica_repository
    
    async def execute(self, dto: CreateTipoMetricaDTO) -> TipoMetricaResponseDTO:
        """
        Ejecuta el caso de uso de creación de tipo de métrica.
        
        Args:
            dto: DTO con los datos para crear el tipo de métrica
            
        Returns:
            TipoMetricaResponseDTO con el tipo de métrica creado
            
        Raises:
            DomainValidationError: Si los datos no son válidos
            RepositoryError: Si ocurre un error en la persistencia
        """
        # Verificar que el nombre no esté en uso
        if await self._repository.exists_by_nombre(dto.nombre):
            raise DomainValidationError(f"Ya existe un tipo de métrica con el nombre '{dto.nombre}'")
        
        # Crear la entidad de dominio
        try:
            tipo_metrica = TipoMetrica(
                id=None,
                nombre=dto.nombre,
                descripcion=dto.descripcion
            )
        except DomainValidationError as e:
            raise e
        
        # Persistir en el repositorio
        try:
            tipo_metrica_creado = await self._repository.create(tipo_metrica)
        except RepositoryError as e:
            raise e
        
        # Convertir a DTO de respuesta
        return TipoMetricaResponseDTO.from_entity(tipo_metrica_creado)
