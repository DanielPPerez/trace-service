# src/adapters/repositories/mysql_practice_repository.py
from typing import Optional, List
import uuid
from sqlalchemy.orm import Session, joinedload
from src.ports.repositories.practice_repository import IPracticeRepository

# Modelos del dominio
from src.domain.entities.practica import Practica
from src.domain.entities.analisis import Analisis

# Modelos de la base de datos (SQLAlchemy)
from .db_models import PracticeDB, AnalisisDB

class MySQLPracticeRepository(IPracticeRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def save(self, practica: Practica) -> None:
        practice_db = self._map_entity_to_db_model(practica)
        self.db.add(practice_db)
        self.db.commit()

    def find_by_id(self, practice_id: uuid.UUID) -> Optional[Practica]:
        practice_db = (
            self.db.query(PracticeDB)
            .options(joinedload(PracticeDB.analisis)) # Carga ansiosa para incluir el análisis
            .filter(PracticeDB.practice_id == str(practice_id))
            .first()
        )
        return self._map_db_model_to_entity(practice_db) if practice_db else None

    def find_by_user_id(self, user_id: uuid.UUID) -> List[Practica]:
        practices_db = (
            self.db.query(PracticeDB)
            .options(joinedload(PracticeDB.analisis))
            .filter(PracticeDB.user_id == str(user_id))
            .order_by(PracticeDB.fecha_carga.desc())
            .all()
        )
        return [self._map_db_model_to_entity(p) for p in practices_db if p]

    def update(self, practica: Practica) -> None:
        practice_db = (
            self.db.query(PracticeDB)
            .options(joinedload(PracticeDB.analisis))
            .filter(PracticeDB.practice_id == str(practica.practice_id))
            .first()
        )
        if practice_db:
            # Actualiza los campos de la práctica
            practice_db.estado_analisis = practica.estado_analisis
            
            # Si hay un análisis, créalo o actualízalo
            if practica.analisis:
                if practice_db.analisis:
                    # Actualiza el análisis existente
                    practice_db.analisis.puntuacion_general = practica.analisis.puntuacion_general
                    practice_db.analisis.puntuacion_proporcion = practica.analisis.puntuacion_proporcion
                    practice_db.analisis.puntuacion_inclinacion = practica.analisis.puntuacion_inclinacion
                    practice_db.analisis.puntuacion_espaciado = practica.analisis.puntuacion_espaciado
                    practice_db.analisis.puntuacion_consistencia = practica.analisis.puntuacion_consistencia
                    practice_db.analisis.fortalezas = practica.analisis.fortalezas
                    practice_db.analisis.areas_mejora = practica.analisis.areas_mejora
                else:
                    # Crea un nuevo análisis
                    practice_db.analisis = AnalisisDB(
                        analisis_id=str(practica.analisis.analisis_id),
                        practice_id=str(practica.practice_id),
                        puntuacion_general=practica.analisis.puntuacion_general,
                        puntuacion_proporcion=practica.analisis.puntuacion_proporcion,
                        puntuacion_inclinacion=practica.analisis.puntuacion_inclinacion,
                        puntuacion_espaciado=practica.analisis.puntuacion_espaciado,
                        puntuacion_consistencia=practica.analisis.puntuacion_consistencia,
                        fortalezas=practica.analisis.fortalezas,
                        areas_mejora=practica.analisis.areas_mejora,
                    )
            
            self.db.commit()

    def delete(self, practice_id: uuid.UUID) -> None:
        practice_db = self.db.query(PracticeDB).filter(PracticeDB.practice_id == str(practice_id)).first()
        if practice_db:
            self.db.delete(practice_db)
            self.db.commit()
            
    # --- MÉTODOS PRIVADOS DE MAPEO ---

    def _map_db_model_to_entity(self, practice_db: PracticeDB) -> Optional[Practica]:
        if not practice_db:
            return None
            
        analisis_entity = None
        if practice_db.analisis:
            analisis_db = practice_db.analisis
            analisis_entity = Analisis(
                analisis_id=uuid.UUID(analisis_db.analisis_id),
                puntuacion_general=analisis_db.puntuacion_general,
                puntuacion_proporcion=analisis_db.puntuacion_proporcion,
                puntuacion_inclinacion=analisis_db.puntuacion_inclinacion,
                puntuacion_espaciado=analisis_db.puntuacion_espaciado,
                puntuacion_consistencia=analisis_db.puntuacion_consistencia,
                fortalezas=analisis_db.fortalezas,
                areas_mejora=analisis_db.areas_mejora,
            )
            
        return Practica(
            practice_id=uuid.UUID(practice_db.practice_id),
            user_id=uuid.UUID(practice_db.user_id),
            letra_plantilla=practice_db.letra_plantilla,
            url_imagen=practice_db.url_imagen,
            fecha_carga=practice_db.fecha_carga,
            estado_analisis=practice_db.estado_analisis,
            analisis=analisis_entity,
        )

    def _map_entity_to_db_model(self, practica: Practica) -> PracticeDB:
        return PracticeDB(
            practice_id=str(practica.practice_id),
            user_id=str(practica.user_id),
            letra_plantilla=practica.letra_plantilla,
            url_imagen=practica.url_imagen,
            fecha_carga=practica.fecha_carga,
            estado_analisis=practica.estado_analisis,
        )