# src/adapters/api/practice_routes.py
from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, status
import uuid
from typing import List

# DTOs
from src.use_cases.dtos import (
    CreatePracticeResponseDTO, PracticeResultDTO, PracticeHistoryDTO, UpdateAnalysisRequestDTO
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

router = APIRouter(prefix="/practices", tags=["Prácticas de Caligrafía"])

# --- Inyección de Dependencias ---
def get_practice_repository(db: Session = Depends(get_db)) -> MySQLPracticeRepository:
    return MySQLPracticeRepository(db=db)

# --- Endpoints ---

@router.post("/", response_model=CreatePracticeResponseDTO, status_code=status.HTTP_202_ACCEPTED)
def create_practice(
    user_id: uuid.UUID = Depends(get_current_user_id),
    letra: LetraPermitida = Form(...),
    imagen: UploadFile = File(...),
    repo: MySQLPracticeRepository = Depends(get_practice_repository)
):
    """Sube una nueva práctica para ser analizada."""
    use_case = CreatePracticeUseCase(repo)
    return use_case.execute(user_id=user_id, letra=letra, imagen=imagen)

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