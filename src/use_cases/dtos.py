# src/use_cases/dtos.py
from pydantic import BaseModel, Field
import uuid
import datetime
from typing import Optional, List
from src.domain.value_objects.enums import EstadoAnalisis, LetraPermitida

# DTO para la respuesta al crear una práctica
class CreatePracticeResponseDTO(BaseModel):
    practice_id: str
    user_id: str
    estado_analisis: EstadoAnalisis
    mensaje: str

# DTO para el análisis, usado en las respuestas
class AnalisisDetailDTO(BaseModel):
    puntuacion_general: int
    puntuacion_proporcion: int
    puntuacion_inclinacion: int
    puntuacion_espaciado: int
    puntuacion_consistencia: int
    fortalezas: str
    areas_mejora: str

# DTO para la petición de actualización del análisis (desde el servicio de IA)
class UpdateAnalysisRequestDTO(BaseModel):
    puntuacion_general: int = Field(..., ge=0, le=100)
    puntuacion_proporcion: int = Field(..., ge=0, le=100)
    puntuacion_inclinacion: int = Field(..., ge=0, le=100)
    puntuacion_espaciado: int = Field(..., ge=0, le=100)
    puntuacion_consistencia: int = Field(..., ge=0, le=100)
    fortalezas: str = Field(..., max_length=255)
    areas_mejora: str = Field(..., max_length=255)

# DTO para obtener el resultado de una práctica
class PracticeResultDTO(BaseModel):
    practice_id: str
    user_id: str
    letra_plantilla: LetraPermitida
    url_imagen: str
    fecha_carga: datetime.datetime
    estado_analisis: EstadoAnalisis
    analisis: Optional[AnalisisDetailDTO] = None

# DTO para la lista del historial
class PracticeHistoryDTO(BaseModel):
    practice_id: str
    letra_plantilla: LetraPermitida
    fecha_carga: datetime.datetime
    puntuacion_general: Optional[int]