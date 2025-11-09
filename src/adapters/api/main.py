# src/adapters/api/main.py
from fastapi import FastAPI, status

# Importamos el router que contiene todos nuestros endpoints de prácticas
from src.adapters.api import practice_routes

# Importamos lo necesario de SQLAlchemy para la creación inicial de las tablas
from src.adapters.repositories.database import engine
from src.adapters.repositories.base import Base

# Es crucial importar los modelos de la base de datos aquí.
# Aunque no los usemos directamente en este archivo, al importarlos,
# se registran en los metadatos de `Base`, permitiendo que `create_all` los encuentre.
from src.adapters.repositories import db_models

# --- Creación de Tablas en la Base de Datos ---
# Esta línea es la que crea las tablas "practices" y "analyses" en tu base de datos MySQL
# (específicamente en el schema 'scriptoria_trace') la primera vez que se ejecuta la aplicación.
# Si las tablas ya existen, no hace nada.
def init_db():
    """Inicializa las tablas de la base de datos."""
    try:
        print("Creando tablas en la base de datos si no existen...")
        Base.metadata.create_all(bind=engine)
        print("Tablas verificadas/creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        print("Asegúrate de que la base de datos esté configurada correctamente.")

# Ejecutamos la inicialización de la base de datos
init_db()


# --- Creación de la Aplicación Principal FastAPI ---
app = FastAPI(
    title="Servicio de Trazos - Scriptoria AI",
    description="Microservicio para gestionar las prácticas de caligrafía de los usuarios y sus análisis.",
    version="1.0.0"
)


# --- Inclusión de Rutas ---
# Aquí es donde le decimos a nuestra aplicación principal que use
# todos los endpoints que definimos en el archivo practice_routes.py.
# Todos los endpoints de ese archivo ahora estarán disponibles bajo la aplicación principal.
app.include_router(practice_routes.router)


# --- Endpoints de Nivel de Aplicación ---
# Es un buen lugar para mantener endpoints que son para el servicio
# en general, como una verificación de estado (health check).
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoring"])
def health_check():
    """
    Verifica que el servicio esté funcionando correctamente.
    Es útil para sistemas de monitoreo, balanceadores de carga o Kubernetes.
    """
    return {"status": "ok", "service": "TraceService"}