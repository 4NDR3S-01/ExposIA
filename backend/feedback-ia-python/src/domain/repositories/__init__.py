# filepath: /src/domain/repositories/__init__.py
"""
Domain repository interfaces module.

This module contains all repository interfaces that define contracts for data access
following the Repository pattern and Dependency Inversion Principle.
"""

from .feedback_repository import FeedbackRepositoryInterface
from .grabacion_repository import GrabacionRepositoryInterface
from .metrica_repository import MetricaRepositoryInterface
from .parametro_repository import ParametroRepositoryInterface
from .tipo_metrica_repository import TipoMetricaRepositoryInterface

__all__ = [
    "FeedbackRepositoryInterface",
    "GrabacionRepositoryInterface",
    "MetricaRepositoryInterface", 
    "ParametroRepositoryInterface",
    "TipoMetricaRepositoryInterface"
]