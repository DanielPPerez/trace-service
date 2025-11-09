import uuid
import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .analisis import Analisis
from ..value_objects.enums import EstadoAnalisis, LetraPermitida

class Practica(BaseModel):
    practice_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    letra_plantilla: LetraPermitida
    url_imagen: str
    fecha_carga: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    estado_analisis: EstadoAnalisis = EstadoAnalisis.PENDIENTE
    analisis: Optional[Analisis] = None

    def marcar_como_completada(self, analisis_resultado: Analisis):
        if self.estado_analisis != EstadoAnalisis.PENDIENTE:
            raise ValueError("Solo se puede completar una práctica pendiente.")
        self.analisis = analisis_resultado
        self.estado_analisis = EstadoAnalisis.COMPLETADO