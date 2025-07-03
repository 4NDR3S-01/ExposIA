"""
Modelo SQLAlchemy para Feedback.
Representa la estructura de datos en la capa de infraestructura.
"""
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..connection import Base


class FeedbackModel(Base):
    """
    Modelo SQLAlchemy para la tabla feedbacks.
    
    Esta clase pertenece a la capa de infraestructura y define
    la estructura de datos para persistencia en base de datos.
    
    Separada de la entidad de dominio para mantener la independencia
    del dominio respecto a frameworks específicos.
    """
    
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    grabacion_id = Column(Integer, ForeignKey("grabaciones.id"), nullable=False, index=True)
    parametro_id = Column(Integer, ForeignKey("parametros.id"), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    es_manual = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    grabacion = relationship("GrabacionModel", back_populates="feedbacks")
    parametro = relationship("ParametroModel", back_populates="feedbacks")
    
    # Índices compuestos para mejorar performance
    __table_args__ = (
        # Índice único para evitar feedbacks duplicados
        {'sqlite_autoincrement': True}  # Para SQLite
    )
    
    def __repr__(self):
        return f"<FeedbackModel(id={self.id}, grabacion_id={self.grabacion_id}, parametro_id={self.parametro_id}, valor={self.valor})>"
