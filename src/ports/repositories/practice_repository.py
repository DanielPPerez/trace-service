from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from src.domain.entities.practica import Practica

class IPracticeRepository(ABC):
    @abstractmethod
    def save(self, practica: Practica) -> None:
        pass

    @abstractmethod
    def find_by_id(self, practice_id: uuid.UUID) -> Optional[Practica]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: uuid.UUID) -> List[Practica]:
        pass
    
    @abstractmethod
    def update(self, practica: Practica) -> None:
        pass