from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.schemas import schemas
from src.services.feedback_service import FeedbackService

router = APIRouter()

# Rutas para TipoMetrica
@router.post("/tipos-metrica/", response_model=schemas.TipoMetricaResponse, status_code=status.HTTP_201_CREATED)
def create_tipo_metrica(tipo_metrica: schemas.TipoMetricaCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_tipo_metrica(db, tipo_metrica)

@router.get("/tipos-metrica/", response_model=List[schemas.TipoMetricaResponse])
def get_tipos_metrica(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos_metrica = FeedbackService.get_tipos_metrica(db, skip=skip, limit=limit)
    return tipos_metrica

@router.get("/tipos-metrica/{tipo_metrica_id}", response_model=schemas.TipoMetricaResponse)
def get_tipo_metrica(tipo_metrica_id: int, db: Session = Depends(get_db)):
    tipo_metrica = FeedbackService.get_tipo_metrica_by_id(db, tipo_metrica_id)
    if tipo_metrica is None:
        raise HTTPException(status_code=404, detail="Tipo de métrica no encontrado")
    return tipo_metrica

# Rutas para Metrica
@router.post("/metricas/", response_model=schemas.MetricaResponse, status_code=status.HTTP_201_CREATED)
def create_metrica(metrica: schemas.MetricaCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_metrica(db, metrica)

@router.get("/metricas/", response_model=List[schemas.MetricaResponse])
def get_metricas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metricas = FeedbackService.get_metricas(db, skip=skip, limit=limit)
    return metricas

@router.get("/metricas/{metrica_id}", response_model=schemas.MetricaResponse)
def get_metrica(metrica_id: int, db: Session = Depends(get_db)):
    metrica = FeedbackService.get_metrica_by_id(db, metrica_id)
    if metrica is None:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    return metrica

# Rutas para Parametro
@router.post("/parametros/", response_model=schemas.ParametroResponse, status_code=status.HTTP_201_CREATED)
def create_parametro(parametro: schemas.ParametroCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_parametro(db, parametro)

@router.get("/parametros/", response_model=List[schemas.ParametroResponse])
def get_parametros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parametros = FeedbackService.get_parametros(db, skip=skip, limit=limit)
    return parametros

@router.get("/parametros/{parametro_id}", response_model=schemas.ParametroResponse)
def get_parametro(parametro_id: int, db: Session = Depends(get_db)):
    parametro = FeedbackService.get_parametro_by_id(db, parametro_id)
    if parametro is None:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    return parametro

# Rutas para Grabacion
@router.post("/grabaciones/", response_model=schemas.GrabacionResponse, status_code=status.HTTP_201_CREATED)
def create_grabacion(grabacion: schemas.GrabacionCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_grabacion(db, grabacion)

@router.get("/grabaciones/", response_model=List[schemas.GrabacionResponse])
def get_grabaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grabaciones = FeedbackService.get_grabaciones(db, skip=skip, limit=limit)
    return grabaciones

@router.get("/grabaciones/{grabacion_id}", response_model=schemas.GrabacionResponse)
def get_grabacion(grabacion_id: int, db: Session = Depends(get_db)):
    grabacion = FeedbackService.get_grabacion_by_id(db, grabacion_id)
    if grabacion is None:
        raise HTTPException(status_code=404, detail="Grabación no encontrada")
    return grabacion

# Rutas para Feedback
@router.post("/feedbacks/", response_model=schemas.FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_feedback(db, feedback)

@router.get("/feedbacks/", response_model=List[schemas.FeedbackResponse])
def get_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = FeedbackService.get_feedbacks(db, skip=skip, limit=limit)
    return feedbacks

@router.get("/feedbacks/{feedback_id}", response_model=schemas.FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = FeedbackService.get_feedback_by_id(db, feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback no encontrado")
    return feedback

@router.get("/grabaciones/{grabacion_id}/feedbacks", response_model=List[schemas.FeedbackResponse])
def get_feedbacks_by_grabacion(grabacion_id: int, db: Session = Depends(get_db)):
    feedbacks = FeedbackService.get_feedbacks_by_grabacion(db, grabacion_id)
    return feedbacks