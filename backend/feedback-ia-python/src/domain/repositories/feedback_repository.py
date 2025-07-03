"""
Interface del repositorio de Feedback.
Define el contrato que deben cumplir las implementaciones concretas.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.feedback import Feedback


class FeedbackRepositoryInterface(ABC):
    """
    Interface que define las operaciones de persistencia para Feedback.
    
    Esta interfaz pertenece a la capa de dominio y define el contrato
    que deben implementar los repositorios concretos en la capa de infraestructura.
    
    Principios aplicados:
    - Dependency Inversion: El dominio define la interfaz, la infraestructura la implementa
    - Interface Segregation: Interfaz específica para operaciones de Feedback
    """
    
    @abstractmethod
    async def create(self, feedback: Feedback) -> Feedback:
        """
        Crea un nuevo feedback en el sistema.
        
        Args:
            feedback: Entidad de feedback a crear
            
        Returns:
            Feedback creado con su ID asignado
            
        Raises:
            DuplicateFeedbackError: Si ya existe un feedback para la misma grabación y parámetro
            RepositoryError: Si ocurre un error durante la creación
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """
        Obtiene un feedback por su ID.
        
        Args:
            feedback_id: ID del feedback a buscar
            
        Returns:
            Feedback encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """
        Obtiene todos los feedbacks con paginación.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de feedbacks
        """
        pass
    
    @abstractmethod
    async def get_by_grabacion_id(self, grabacion_id: int) -> List[Feedback]:
        """
        Obtiene todos los feedbacks de una grabación específica.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Lista de feedbacks de la grabación
        """
        pass
    
    @abstractmethod
    async def get_by_parametro_id(self, parametro_id: int) -> List[Feedback]:
        """
        Obtiene todos los feedbacks de un parámetro específico.
        
        Args:
            parametro_id: ID del parámetro
            
        Returns:
            Lista de feedbacks del parámetro
        """
        pass
    
    @abstractmethod
    async def get_automatic_feedbacks(self, grabacion_id: int) -> List[Feedback]:
        """
        Obtiene todos los feedbacks automáticos de una grabación.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Lista de feedbacks automáticos
        """
        pass
    
    @abstractmethod
    async def get_manual_feedbacks(self, grabacion_id: int) -> List[Feedback]:
        """
        Obtiene todos los feedbacks manuales de una grabación.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Lista de feedbacks manuales
        """
        pass
    
    @abstractmethod
    async def update(self, feedback: Feedback) -> Feedback:
        """
        Actualiza un feedback existente.
        
        Args:
            feedback: Entidad de feedback con los datos actualizados
            
        Returns:
            Feedback actualizado
            
        Raises:
            FeedbackNotFoundError: Si el feedback no existe
            RepositoryError: Si ocurre un error durante la actualización
        """
        pass
    
    @abstractmethod
    async def delete(self, feedback_id: int) -> bool:
        """
        Elimina un feedback por su ID.
        
        Args:
            feedback_id: ID del feedback a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no se encontró
            
        Raises:
            RepositoryError: Si ocurre un error durante la eliminación
        """
        pass
    
    @abstractmethod
    async def exists_by_grabacion_and_parametro(
        self, 
        grabacion_id: int, 
        parametro_id: int
    ) -> bool:
        """
        Verifica si existe un feedback para una grabación y parámetro específicos.
        
        Args:
            grabacion_id: ID de la grabación
            parametro_id: ID del parámetro
            
        Returns:
            True si existe, False si no
        """
        pass
    
    @abstractmethod
    async def get_by_grabacion_and_parametro(
        self, 
        grabacion_id: int, 
        parametro_id: int
    ) -> Optional[Feedback]:
        """
        Obtiene un feedback específico por grabación y parámetro.
        
        Args:
            grabacion_id: ID de la grabación
            parametro_id: ID del parámetro
            
        Returns:
            Feedback encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    async def get_feedbacks_with_low_scores(
        self, 
        threshold: float = 40.0,
        skip: int = 0,
        limit: int = 100
    ) -> List[Feedback]:
        """
        Obtiene feedbacks con puntajes bajos.
        
        Args:
            threshold: Umbral para considerar un puntaje como bajo
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de feedbacks con puntajes bajos
        """
        pass
    
    @abstractmethod
    async def get_average_score_by_grabacion(self, grabacion_id: int) -> Optional[float]:
        """
        Calcula el puntaje promedio de todos los feedbacks de una grabación.
        
        Args:
            grabacion_id: ID de la grabación
            
        Returns:
            Puntaje promedio o None si no hay feedbacks
        """
        pass
