import uuid
from pydantic import BaseModel, Field, conint

class Analisis(BaseModel):
    analisis_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    puntuacion_general: conint(ge=0, le=100)
    puntuacion_proporcion: conint(ge=0, le=100)
    puntuacion_inclinacion: conint(ge=0, le=100)
    puntuacion_espaciado: conint(ge=0, le=100)
    puntuacion_consistencia: conint(ge=0, le=100)
    fortalezas: str
    areas_mejora: str