# src/adapters/api/practice_routes.py
from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, status
import uuid
from typing import Any, Dict, List, Optional

# DTOs
from src.use_cases.dtos import (
    PracticeResultDTO, PracticeHistoryDTO, UpdateAnalysisRequestDTO
)
# Casos de Uso
from src.use_cases.create_practice import CreatePracticeUseCase
from src.use_cases.get_practice_result import GetPracticeResultUseCase
from src.use_cases.list_user_practices import ListUserPracticesUseCase
from src.use_cases.update_practice_analysis import UpdatePracticeAnalysisUseCase
from src.use_cases.delete_practice import DeletePracticeUseCase

# Seguridad y dependencias
from sqlalchemy.orm import Session
from src.adapters.api.security import get_current_user_id
from src.adapters.repositories.database import get_db
from src.adapters.repositories.mysql_practice_repository import MySQLPracticeRepository
from src.domain.value_objects.enums import LetraPermitida
from src.adapters.clients import AnalysisServiceClient, AnalysisServiceError
from src.config import settings

router = APIRouter(prefix="/practices", tags=["Prácticas de Caligrafía"])

# --- Inyección de Dependencias ---
def get_practice_repository(db: Session = Depends(get_db)) -> MySQLPracticeRepository:
    return MySQLPracticeRepository(db=db)


def _clamp_score(value: Any) -> int:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(100, int(round(numeric))))


def _short_text(value: Optional[str]) -> str:
    text = value or "Sin información disponible"
    return text[:255]


def _build_analysis_request_dto(payload: Dict[str, Any]) -> UpdateAnalysisRequestDTO:
    metrics = payload.get("metricas_detalle", {}) or {}
    feedback = payload.get("feedback_final", {}) or {}
    fortalezas_candidate = metrics.get("fortalezas_base")
    areas_candidate = metrics.get("areas_mejora_base")

    if not fortalezas_candidate:
        analisis_reglas = feedback.get("analisis_reglas")
        if isinstance(analisis_reglas, dict):
            fortalezas_candidate = analisis_reglas.get("fortalezas")
        else:
            fortalezas_candidate = feedback.get("fortalezas")

    if not areas_candidate:
        analisis_reglas = feedback.get("analisis_reglas")
        if isinstance(analisis_reglas, dict):
            areas_candidate = analisis_reglas.get("areas_mejora")
        else:
            areas_candidate = feedback.get("areas_mejora")

    return UpdateAnalysisRequestDTO(
        puntuacion_general=_clamp_score(metrics.get("score_global")),
        puntuacion_proporcion=_clamp_score(metrics.get("puntuacion_proporcion")),
        puntuacion_inclinacion=_clamp_score(metrics.get("puntuacion_inclinacion")),
        puntuacion_espaciado=_clamp_score(metrics.get("puntuacion_espaciado")),
        puntuacion_consistencia=_clamp_score(metrics.get("puntuacion_consistencia")),
        fortalezas=_short_text(fortalezas_candidate),
        areas_mejora=_short_text(areas_candidate),
    )


# --- Endpoints ---

@router.post("/", response_model=PracticeResultDTO, status_code=status.HTTP_201_CREATED)
async def create_practice(
    user_id: uuid.UUID = Depends(get_current_user_id),
    letra: LetraPermitida = Form(...),
    imagen: UploadFile = File(...),
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """Sube una nueva práctica y coordina el análisis con el microservicio externo."""
    # Leer los bytes para reenviarlos al servicio de análisis
    image_bytes = await imagen.read()
    imagen.file.seek(0)  # Permite reusar el archivo en otras capas si es necesario

    use_case = CreatePracticeUseCase(repo)
    creation_response = use_case.execute(user_id=user_id, letra=letra, imagen=imagen)
    practice_id = uuid.UUID(creation_response.practice_id)

    # Intentar conectarse al servicio de análisis
    try:
        analysis_client = AnalysisServiceClient(
            base_url=settings.analysis_service_base_url,
            timeout=settings.analysis_service_timeout,
        )
    except AnalysisServiceError as exc:
        print(f"[AnalysisService] configuración incompleta: {exc}")
        analysis_client = None

    if analysis_client and image_bytes:
        try:
            analysis_payload = await analysis_client.analyze_letter(
                letter_char=letra.value,
                image_bytes=image_bytes,
                filename=imagen.filename,
                content_type=imagen.content_type,
            )
            analysis_dto = _build_analysis_request_dto(analysis_payload)
            update_uc = UpdatePracticeAnalysisUseCase(repo)
            update_uc.execute(practice_id=practice_id, analysis_data=analysis_dto)
        except AnalysisServiceError as exc:
            print(f"[AnalysisService] Error de negocio: {exc}")
        except Exception as exc:  # noqa: BLE001
            print(f"[AnalysisService] Error inesperado al actualizar análisis: {exc}")

    # Devolver el resultado actualizado (o pendiente si falló el análisis)
    result_uc = GetPracticeResultUseCase(repo)
    return result_uc.execute(practice_id)

@router.get("/history", response_model=List[PracticeHistoryDTO])
def get_user_history(
    user_id: uuid.UUID = Depends(get_current_user_id),
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """Obtiene el historial de prácticas de un usuario."""
    use_case = ListUserPracticesUseCase(repo)
    return use_case.execute(user_id=user_id)

@router.get("/{practice_id}", response_model=PracticeResultDTO)
def get_practice_result(
    practice_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """Obtiene el resultado detallado de una práctica específica."""
    use_case = GetPracticeResultUseCase(repo)
    try:
        practice = use_case.execute(practice_id)
        # Valida que el usuario solo pueda ver sus propias prácticas
        if practice.user_id != str(user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado a esta práctica.")
        return practice
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Práctica no encontrada.")

@router.put("/{practice_id}/analysis", response_model=PracticeResultDTO)
def update_practice_analysis(
    practice_id: uuid.UUID,
    request: UpdateAnalysisRequestDTO,
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """
    ENDPOINT INTERNO: Usado por el servicio de IA para registrar los resultados de un análisis.
    En producción, este endpoint debería estar protegido por un método de autenticación de servicio a servicio.
    """
    use_case = UpdatePracticeAnalysisUseCase(repo)
    try:
        return use_case.execute(practice_id=practice_id, analysis_data=request)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Práctica no encontrada.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{practice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_practice(
    practice_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """Elimina una práctica del historial."""
    # Primero, verifica que la práctica pertenece al usuario
    practice_repo_check = GetPracticeResultUseCase(repo)
    try:
        practice = practice_repo_check.execute(practice_id)
        if practice.user_id != str(user_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar esta práctica.")
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Práctica no encontrada.")

    # Si todo está bien, procede a eliminar
    use_case = DeletePracticeUseCase(repo)
    use_case.execute(practice_id)