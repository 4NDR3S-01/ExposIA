# filepath: /src/domain/value_objects/__init__.py
"""
Domain value objects module.

This module contains immutable value objects that encapsulate business logic
and represent concepts that are defined by their value rather than identity.
"""

from .archivo_audio import ArchivoAudio
from .feedback_score import FeedbackScore
from .parametro_valor import ParametroValor

__all__ = [
    "ArchivoAudio",
    "FeedbackScore",
    "ParametroValor"
]