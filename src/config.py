# src/config.py
from typing import Optional
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    # Database
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int

    # JWT Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External Services
    analysis_service_base_url: Optional[str] = None
    analysis_service_timeout: int = 30

    def get_db_url(self) -> str:
        """Genera la URL de conexión para SQLAlchemy."""
        # Codificamos usuario y contraseña para manejar caracteres especiales
        encoded_user = quote_plus(self.db_user)
        encoded_password = quote_plus(self.db_password)
        return f"mysql+pymysql://{encoded_user}:{encoded_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"


settings = Settings()