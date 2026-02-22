import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://proyecto06:proyecto06@database-service:5432/proyecto06_db"
    )
    
    # API
    API_TITLE: str = "Proyecto06 API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Backend FastAPI para Proyecto06 - Arquitectura 3 capas"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # App
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    class Config:
        case_sensitive = True

settings = Settings()
