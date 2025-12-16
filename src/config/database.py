"""
Configuración de la conexión a MongoDB usando Beanie
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional

from .settings import settings
from ..models.project import Project
from ..models.analysis_session import AnalysisSession
from ..models.generated_doc import GeneratedDoc


class Database:
    """Gestor de conexión a MongoDB"""
    
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Conecta a MongoDB e inicializa Beanie"""
        try:
            # Crear cliente de MongoDB
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            
            # Inicializar Beanie con los modelos
            await init_beanie(
                database=cls.client[settings.database_name],
                document_models=[
                    Project,
                    AnalysisSession,
                    GeneratedDoc,
                ]
            )
            
            print(f"✅ Conectado a MongoDB: {settings.database_name}")
            
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Cierra la conexión a MongoDB"""
        if cls.client:
            cls.client.close()
            print("🔌 Desconectado de MongoDB")


# Funciones para FastAPI lifespan
async def init_db():
    """Inicializa la base de datos al arrancar la app"""
    await Database.connect_db()


async def close_db():
    """Cierra la conexión al apagar la app"""
    await Database.close_db()
