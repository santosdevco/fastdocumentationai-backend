"""
Modelo de Documentos Generados
"""
from beanie import Document, Link
from pydantic import Field
from typing import List, Dict, Any
from datetime import datetime

from .project import Project
from .analysis_session import AnalysisSession


class GeneratedFile(Document):
    """Representa un archivo .md generado"""
    
    path: str = Field(..., description="Ruta del archivo (ej: ai_docs/06-infraestructura/01-deployment.md)")
    content: str = Field(..., description="Contenido markdown del archivo")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        is_root = False  # Documento embebido


class GeneratedDoc(Document):
    """
    Modelo de Documentación Generada en MongoDB
    
    Almacena los archivos .md generados por Copilot en el paso final
    """
    
    # Relaciones
    project: Link[Project] = Field(..., description="Proyecto asociado")
    analysis_session: Link[AnalysisSession] = Field(..., description="Sesión de análisis que generó estos docs")
    
    # Archivos generados
    files: List[Dict[str, Any]] = Field(
        ...,
        description="Lista de archivos markdown generados"
    )
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: str = Field(..., description="Email de quien guardó los documentos")
    
    class Settings:
        name = "generated_docs"
        indexes = [
            "project",
            "analysis_session",
            "generated_at",
            "generated_by",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "files": [
                    {
                        "path": "ai_docs/06-infraestructura/01-deployment.md",
                        "content": "# Deployment\n\n...",
                        "generated_at": "2025-01-15T10:30:00Z"
                    },
                    {
                        "path": "ai_docs/06-infraestructura/02-ci-cd.md",
                        "content": "# CI/CD Pipeline\n\n...",
                        "generated_at": "2025-01-15T10:30:00Z"
                    }
                ],
                "generated_by": "analista@empresa.com"
            }
        }
    
    def __repr__(self):
        return f"<GeneratedDoc {len(self.files)} files>"
