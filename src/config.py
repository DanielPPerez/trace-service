# src/config.py
from pydantic_settings import BaseSettings

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

    def get_db_url(self) -> str:
        """Genera la URL de conexión para SQLAlchemy."""
        # Cambiamos 'mysqlclient' por 'pymysql'
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env" 

settings = Settings()