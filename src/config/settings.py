"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración global de la aplicación"""
    
    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "documentation_ai"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # CORS
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    
    # Frontend
    frontend_url: str = "http://localhost:8000"
    
    # Environment
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte el string de CORS origins a lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Instancia global de settings
settings = Settings()
