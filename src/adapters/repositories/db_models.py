from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from src.domain.value_objects.enums import EstadoAnalisis, LetraPermitida
from src.adapters.repositories.base import Base
import datetime

class PracticeDB(Base):
    __tablename__ = "practices"
    
    # Configuración para distinguir mayúsculas/minúsculas ('a' vs 'A')
    __table_args__ = {'mysql_collate': 'utf8mb4_bin'}

    practice_id = Column(CHAR(36), primary_key=True)
<<<<<<< HEAD
    user_id = Column(CHAR(36), index=True, nullable=False)
    letra_plantilla = Column(SQLAlchemyEnum(LetraPermitida), nullable=False)
=======
    user_id = Column(CHAR(36), index=True, nullable=False) # Referencia lógica, no clave foránea
    letra_plantilla = Column(
        SQLAlchemyEnum(LetraPermitida, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
>>>>>>> 5f4b543eaf0d401ba70980e1c0a3dba2d98f3b20
    url_imagen = Column(String(255), nullable=False)
    fecha_carga = Column(DateTime, default=datetime.datetime.utcnow)
    estado_analisis = Column(
        SQLAlchemyEnum(EstadoAnalisis, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        default=EstadoAnalisis.PENDIENTE
    )
    
    analisis = relationship("AnalisisDB", back_populates="practice", uselist=False, cascade="all, delete-orphan")

class AnalisisDB(Base):
    __tablename__ = "analyses"

    # --- CORRECCIÓN IMPRESCINDIBLE ---
    # La tabla hija TAMBIÉN debe ser 'utf8mb4_bin' para poder conectarse con la madre.
    __table_args__ = {'mysql_collate': 'utf8mb4_bin'}
    # ---------------------------------

    analisis_id = Column(CHAR(36), primary_key=True)
    
    # Ahora esta columna coincidirá perfectamente con practices.practice_id
    practice_id = Column(CHAR(36), ForeignKey("practices.practice_id"), nullable=False)
    
    puntuacion_general = Column(Integer)
    puntuacion_proporcion = Column(Integer)
    puntuacion_inclinacion = Column(Integer)
    puntuacion_espaciado = Column(Integer)
    puntuacion_consistencia = Column(Integer)
    fortalezas = Column(String(255))
    areas_mejora = Column(String(255))
    
    practice = relationship("PracticeDB", back_populates="analisis")