# src/use_cases/update_practice_analysis.py
import uuid
from src.ports.repositories.practice_repository import IPracticeRepository
from src.use_cases.dtos import PracticeResultDTO, AnalisisDetailDTO, UpdateAnalysisRequestDTO
from src.domain.entities.analisis import Analisis

class UpdatePracticeAnalysisUseCase:
    """
    Caso de uso para actualizar el análisis de una práctica.
    Usado por el servicio de IA para registrar los resultados del análisis.
    """
    def __init__(self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository

    def execute(self, practice_id: uuid.UUID, analysis_data: UpdateAnalysisRequestDTO) -> PracticeResultDTO:
        """
        Ejecuta el caso de uso.

        Args:
            practice_id: El ID de la práctica a actualizar.
            analysis_data: Los datos del análisis a registrar.

        Raises:
            FileNotFoundError: Si la práctica con el ID dado no se encuentra.
            ValueError: Si la práctica no está en estado PENDIENTE (ya fue completada).

        Returns:
            Un DTO con los detalles completos de la práctica actualizada.
        """
        # 1. Obtener la entidad de dominio desde el repositorio
        practice_entity = self.practice_repository.find_by_id(practice_id)

        # 2. Validar que la práctica exista
        if not practice_entity:
            raise FileNotFoundError("La práctica no fue encontrada.")

        # 3. Crear la entidad de análisis a partir del DTO
        analisis_entity = Analisis(
            puntuacion_general=analysis_data.puntuacion_general,
            puntuacion_proporcion=analysis_data.puntuacion_proporcion,
            puntuacion_inclinacion=analysis_data.puntuacion_inclinacion,
            puntuacion_espaciado=analysis_data.puntuacion_espaciado,
            puntuacion_consistencia=analysis_data.puntuacion_consistencia,
            fortalezas=analysis_data.fortalezas,
            areas_mejora=analysis_data.areas_mejora,
        )

        # 4. Marcar la práctica como completada (esto valida el estado y lanza ValueError si ya está completada)
        practice_entity.marcar_como_completada(analisis_entity)

        # 5. Actualizar en el repositorio
        self.practice_repository.update(practice_entity)

        # 6. Obtener la práctica actualizada para retornar el DTO completo
        updated_practice = self.practice_repository.find_by_id(practice_id)
        if not updated_practice:
            raise FileNotFoundError("Error al recuperar la práctica actualizada.")

        # 7. Mapear la entidad de dominio a un DTO de respuesta
        analisis_dto = None
        if updated_practice.analisis:
            analisis_dto = AnalisisDetailDTO(
                puntuacion_general=updated_practice.analisis.puntuacion_general,
                puntuacion_proporcion=updated_practice.analisis.puntuacion_proporcion,
                puntuacion_inclinacion=updated_practice.analisis.puntuacion_inclinacion,
                puntuacion_espaciado=updated_practice.analisis.puntuacion_espaciado,
                puntuacion_consistencia=updated_practice.analisis.puntuacion_consistencia,
                fortalezas=updated_practice.analisis.fortalezas,
                areas_mejora=updated_practice.analisis.areas_mejora,
            )

        return PracticeResultDTO(
            practice_id=str(updated_practice.practice_id),
            user_id=str(updated_practice.user_id),
            letra_plantilla=updated_practice.letra_plantilla,
            url_imagen=updated_practice.url_imagen,
            fecha_carga=updated_practice.fecha_carga,
            estado_analisis=updated_practice.estado_analisis,
            analisis=analisis_dto
        )

