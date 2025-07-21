from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.models import TipoMetrica, Metrica, Parametro, Grabacion, Feedback
from src.schemas import schemas

class FeedbackService:
    @staticmethod
    def create_tipo_metrica(db: Session, tipo_metrica: schemas.TipoMetricaCreate):
        db_tipo_metrica = TipoMetrica(**tipo_metrica.model_dump())
        db.add(db_tipo_metrica)
        db.commit()
        db.refresh(db_tipo_metrica)
        return db_tipo_metrica
    
    @staticmethod
    def get_tipos_metrica(db: Session, skip: int = 0, limit: int = 100):
        return db.query(TipoMetrica).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tipo_metrica_by_id(db: Session, tipo_metrica_id: int):
        return db.query(TipoMetrica).filter(TipoMetrica.id == tipo_metrica_id).first()
    
    @staticmethod
    def create_metrica(db: Session, metrica: schemas.MetricaCreate):
        db_metrica = Metrica(**metrica.model_dump())
        db.add(db_metrica)
        db.commit()
        db.refresh(db_metrica)
        return db_metrica
    
    @staticmethod
    def get_metricas(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Metrica).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_metrica_by_id(db: Session, metrica_id: int):
        return db.query(Metrica).filter(Metrica.id == metrica_id).first()
    
    @staticmethod
    def create_parametro(db: Session, parametro: schemas.ParametroCreate):
        db_parametro = Parametro(**parametro.model_dump())
        db.add(db_parametro)
        db.commit()
        db.refresh(db_parametro)
        return db_parametro
    
    @staticmethod
    def get_parametros(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Parametro).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_parametro_by_id(db: Session, parametro_id: int):
        return db.query(Parametro).filter(Parametro.id == parametro_id).first()
    
    @staticmethod
    def create_grabacion(db: Session, grabacion: schemas.GrabacionCreate):
        db_grabacion = Grabacion(**grabacion.model_dump())
        db.add(db_grabacion)
        db.commit()
        db.refresh(db_grabacion)
        return db_grabacion
    
    @staticmethod
    def get_grabaciones(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Grabacion).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_grabacion_by_id(db: Session, grabacion_id: int):
        return db.query(Grabacion).filter(Grabacion.id == grabacion_id).first()
    
    @staticmethod
    def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
        db_feedback = Feedback(**feedback.model_dump())
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    
    @staticmethod
    def get_feedbacks(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Feedback).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_feedback_by_id(db: Session, feedback_id: int):
        return db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    @staticmethod
    def get_feedbacks_by_grabacion(db: Session, grabacion_id: int):
        return db.query(Feedback).filter(Feedback.grabacion_id == grabacion_id).all()