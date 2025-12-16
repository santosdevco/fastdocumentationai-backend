"""
Aplicación Principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config.settings import settings
from .config.database import init_db, close_db
from .routes import projects, analysis, generated_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de vida de la aplicación
    Inicializa y cierra la conexión a MongoDB
    """
    # Startup
    print("🚀 Iniciando aplicación...")
    await init_db()
    yield
    # Shutdown
    print("🛑 Cerrando aplicación...")
    await close_db()


# Crear aplicación FastAPI
app = FastAPI(
    title="Documentation AI API",
    description="API Backend para sistema de documentación con IA",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(projects.router)
app.include_router(analysis.router)
app.include_router(generated_docs.router)


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "message": "Documentation AI API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


# ============================================
# ENDPOINTS DE INFORMACIÓN
# ============================================

@app.get("/api/analysis-types")
async def get_analysis_types():
    """Lista los tipos de análisis disponibles"""
    from .models.analysis_session import AnalysisType
    
    return {
        "analysis_types": [
            {"value": t.value, "label": t.value.replace("-", " ").title()}
            for t in AnalysisType
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
