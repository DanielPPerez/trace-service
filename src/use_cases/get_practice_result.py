# src/use_cases/get_practice_result.py
import uuid
from src.ports.repositories.practice_repository import IPracticeRepository
from src.use_cases.dtos import PracticeResultDTO, AnalisisDetailDTO

class GetPracticeResultUseCase:
    """
    Caso de uso para obtener el resultado detallado de una práctica específica.
    """
    def __init__(self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository

    def execute(self, practice_id: uuid.UUID) -> PracticeResultDTO:
        """
        Ejecuta el caso de uso.

        Args:
            practice_id: El ID de la práctica a buscar.

        Raises:
            FileNotFoundError: Si la práctica con el ID dado no se encuentra.

        Returns:
            Un DTO con los detalles completos de la práctica.
        """
        # 1. Obtener la entidad de dominio desde el repositorio
        practice_entity = self.practice_repository.find_by_id(practice_id)

        # 2. Validar que la práctica exista
        if not practice_entity:
            raise FileNotFoundError("La práctica no fue encontrada.")

        # 3. Mapear la entidad de dominio a un DTO de respuesta
        analisis_dto = None
        if practice_entity.analisis:
            analisis_dto = AnalisisDetailDTO(
                puntuacion_general=practice_entity.analisis.puntuacion_general,
                puntuacion_proporcion=practice_entity.analisis.puntuacion_proporcion,
                puntuacion_inclinacion=practice_entity.analisis.puntuacion_inclinacion,
                puntuacion_espaciado=practice_entity.analisis.puntuacion_espaciado,
                puntuacion_consistencia=practice_entity.analisis.puntuacion_consistencia,
                fortalezas=practice_entity.analisis.fortalezas,
                areas_mejora=practice_entity.analisis.areas_mejora,
            )

        return PracticeResultDTO(
            practice_id=str(practice_entity.practice_id),
            user_id=str(practice_entity.user_id),
            letra_plantilla=practice_entity.letra_plantilla,
            url_imagen=practice_entity.url_imagen,
            fecha_carga=practice_entity.fecha_carga,
            estado_analisis=practice_entity.estado_analisis,
            analisis=analisis_dto
        )