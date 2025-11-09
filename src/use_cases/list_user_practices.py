# src/use_cases/list_user_practices.py
import uuid
from typing import List
from src.ports.repositories.practice_repository import IPracticeRepository
from src.use_cases.dtos import PracticeHistoryDTO

class ListUserPracticesUseCase:
    """
    Caso de uso para listar el historial de prácticas de un usuario.
    """
    def __init__(self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository

    def execute(self, user_id: uuid.UUID) -> List[PracticeHistoryDTO]:
        """
        Ejecuta el caso de uso.

        Args:
            user_id: El ID del usuario cuyo historial se quiere obtener.

        Returns:
            Una lista de DTOs simplificados para mostrar en el historial.
        """
        # 1. Obtener todas las entidades de práctica para el usuario
        user_practices = self.practice_repository.find_by_user_id(user_id)

        # 2. Mapear cada entidad a su DTO correspondiente
        history_list = []
        for practice in user_practices:
            puntuacion = practice.analisis.puntuacion_general if practice.analisis else None
            
            history_dto = PracticeHistoryDTO(
                practice_id=str(practice.practice_id),
                letra_plantilla=practice.letra_plantilla,
                fecha_carga=practice.fecha_carga,
                puntuacion_general=puntuacion
            )
            history_list.append(history_dto)
            
        return history_list