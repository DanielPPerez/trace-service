# src/use_cases/delete_practice.py
import uuid
from src.ports.repositories.practice_repository import IPracticeRepository

class DeletePracticeUseCase:
    """
    Caso de uso para eliminar una práctica.
    """
    def __init__(self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository

    def execute(self, practice_id: uuid.UUID) -> None:
        """
        Ejecuta el caso de uso.

        Args:
            practice_id: El ID de la práctica a eliminar.

        Raises:
            FileNotFoundError: Si la práctica no se encuentra (la capa del repositorio podría manejar esto,
                             pero es buena práctica que el caso de uso sea explícito).
        """
        # 1. (Opcional pero recomendado) Verificar que la práctica existe antes de intentar borrarla.
        #    Esto permite devolver un error más significativo que una simple falla de base de datos.
        practice_to_delete = self.practice_repository.find_by_id(practice_id)
        if not practice_to_delete:
            raise FileNotFoundError("Práctica no encontrada para eliminar.")

        # 2. Llamar al método de eliminación del repositorio
        self.practice_repository.delete(practice_id)

        # No se retorna nada en una operación de eliminación exitosa.
        return