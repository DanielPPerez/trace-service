import uuid
from fastapi import UploadFile
from src.ports.repositories.practice_repository import IPracticeRepository
# Más adelante añadiremos puertos para guardar archivos y publicar eventos
from src.domain.entities.practica import Practica
from src.domain.value_objects.enums import LetraPermitida
from .dtos import CreatePracticeResponseDTO

class CreatePracticeUseCase:
    def __init__(self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository
        # self.file_storage = file_storage
        # self.event_publisher = event_publisher

    def execute(self, user_id: uuid.UUID, letra: LetraPermitida, imagen: UploadFile) -> CreatePracticeResponseDTO:
        # 1. Lógica para guardar la imagen en un bucket S3 (o localmente)
        # Por ahora, simularemos la URL
        image_url = f"https://s3.bucket.name/images/{user_id}/{uuid.uuid4()}.jpg"
        
        # 2. Crear la entidad de dominio
        nueva_practica = Practica(
            user_id=user_id,
            letra_plantilla=letra,
            url_imagen=image_url
        )

        # 3. Guardar en la base de datos a través del repositorio
        self.practice_repository.save(nueva_practica)

        # 4. Lógica para publicar un evento al servicio de IA
        # self.event_publisher.publish("practica_creada", nueva_practica.dict())
        print(f"EVENTO: Publicar 'practica_creada' para practice_id: {nueva_practica.practice_id}")
        
        # 5. Devolver una respuesta
        return CreatePracticeResponseDTO(
            practice_id=str(nueva_practica.practice_id),
            user_id=str(user_id),
            estado_analisis=nueva_practica.estado_analisis,
            mensaje="Práctica recibida y en cola para análisis."
        )