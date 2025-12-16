"""
Modelo de Sesión de Análisis (Preguntas y Respuestas)
"""
from beanie import Document, Link
from pydantic import Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from .project import Project


class AnalysisStatus(str, Enum):
    """Estados de la sesión de análisis"""
    PENDING_ANSWERS = "pending_answers"  # Esperando que alguien responda
    COMPLETED = "completed"              # Copilot confirmó "todo ok"
    IN_REVIEW = "in_review"              # En revisión por el analista


class AnalysisType(str, Enum):
    """Tipos de análisis disponibles"""
    DEPLOYMENT = "deployment"
    API = "api"
    ARQUITECTURA = "arquitectura"
    REQUERIMIENTOS = "requerimientos"
    VISTA_EJECUTIVA = "vista-ejecutiva"
    TECNICA = "tecnica"
    PROCESOS_NEGOCIO = "procesos-negocio"
    ADR = "adr"
    SWAGGER = "swagger"


class IterationHistory(Document):
    """Historial de una iteración de preguntas/respuestas"""
    
    iteration: int = Field(..., description="Número de iteración")
    yaml_generated: Dict[str, Any] = Field(..., description="YAML generado por Copilot")
    answers_provided: Optional[Dict[str, Any]] = Field(None, description="Respuestas del usuario")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "iteration_history"
        is_root = False  # Documento embebido


class AnalysisSession(Document):
    """
    Modelo de Sesión de Análisis en MongoDB
    
    Representa un análisis específico (deployment, API, etc.) de un proyecto.
    Maneja el flujo iterativo de preguntas/respuestas con Copilot.
    """
    
    # Relación con el proyecto
    project: Link[Project] = Field(..., description="Proyecto asociado")
    
    # Tipo de análisis
    analysis_type: AnalysisType = Field(..., description="Tipo de documentación a generar")
    
    # Estado
    status: AnalysisStatus = Field(
        default=AnalysisStatus.PENDING_ANSWERS,
        description="Estado actual del análisis"
    )
    
    # Configuración YAML generada por Copilot
    yaml_config: Dict[str, Any] = Field(
        ...,
        description="YAML con preguntas generado por Copilot"
    )
    
    # Respuestas del usuario
    answers: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Respuestas del formulario"
    )
    
    # Control de iteraciones
    iteration: int = Field(default=1, description="Número de iteración actual")
    needs_more_info: bool = Field(
        default=True,
        description="True si Copilot necesita más información"
    )
    
    # Token único para compartir
    share_token: str = Field(..., description="Token único para URL pública")
    
    # Usuarios involucrados
    created_by: str = Field(..., description="Email del analista que creó el análisis")
    assigned_to: Optional[str] = Field(
        None,
        description="Email del experto asignado para responder"
    )
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Historial de iteraciones
    iteration_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Historial de todas las iteraciones"
    )
    
    class Settings:
        name = "analysis_sessions"
        indexes = [
            "project",
            "analysis_type",
            "status",
            "share_token",
            "created_by",
            "assigned_to",
            "created_at",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "deployment",
                "status": "pending_answers",
                "yaml_config": {
                    "title": "🚀 Deployment - E-commerce",
                    "sections": []
                },
                "answers": {
                    "projectName": "E-commerce API",
                    "cloudProvider": ["aws"]
                },
                "iteration": 1,
                "needs_more_info": True,
                "share_token": "abc123def456",
                "created_by": "analista@empresa.com",
                "assigned_to": "devops@empresa.com"
            }
        }
    
    def __repr__(self):
        return f"<AnalysisSession {self.analysis_type} - Iteration {self.iteration}>"
    
    def get_share_url(self, frontend_url: str) -> str:
        """Genera la URL pública para responder preguntas"""
        return f"{frontend_url}/answer/?token={self.share_token}"
