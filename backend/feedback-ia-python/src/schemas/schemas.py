from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Esquemas para TipoMetrica
class TipoMetricaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoMetricaCreate(TipoMetricaBase):
    pass

class TipoMetricaResponse(TipoMetricaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Esquemas para Metrica
class MetricaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_metrica_id: int

class MetricaCreate(MetricaBase):
    pass

class MetricaResponse(MetricaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Esquemas para Parametro
class ParametroBase(BaseModel):
    nombre: str
    valor: float
    unidad: Optional[str] = None
    metrica_id: int

class ParametroCreate(ParametroBase):
    pass

class ParametroResponse(ParametroBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Esquemas para Grabacion
class GrabacionBase(BaseModel):
    nombre_archivo: str
    ruta_archivo: str
    duracion: Optional[float] = None
    formato: Optional[str] = None
    fecha_grabacion: Optional[datetime] = None

class GrabacionCreate(GrabacionBase):
    pass

class GrabacionResponse(GrabacionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Esquemas para Feedback
class FeedbackBase(BaseModel):
    grabacion_id: int
    parametro_id: int
    valor: float
    comentario: Optional[str] = None
    es_manual: Optional[bool] = False

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Esquemas avanzados con relaciones
class FeedbackDetailResponse(FeedbackResponse):
    grabacion: GrabacionResponse
    parametro: ParametroResponse

    model_config = {"from_attributes": True}