"""
Esquemas Pydantic para Análisis
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from ...models.analysis_session import AnalysisType, AnalysisStatus


# ============================================
# REQUEST SCHEMAS
# ============================================

class AnalysisCreate(BaseModel):
    """Schema para crear una sesión de análisis"""
    project_id: str = Field(..., description="ID del proyecto")
    analysis_type: AnalysisType = Field(..., description="Tipo de análisis")
    yaml_config: Dict[str, Any] = Field(..., description="YAML con preguntas")
    created_by: str = Field(..., description="Email del creador")
    assigned_to: Optional[str] = Field(None, description="Email del asignado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "507f1f77bcf86cd799439011",
                "analysis_type": "deployment",
                "yaml_config": {
                    "title": "🚀 Deployment - E-commerce",
                    "description": "Completa este formulario...",
                    "sections": []
                },
                "created_by": "analista@empresa.com",
                "assigned_to": "devops@empresa.com"
            }
        }


class AnswersUpdate(BaseModel):
    """Schema para actualizar respuestas"""
    answers: Dict[str, Any] = Field(..., description="Respuestas del formulario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answers": {
                    "projectName": "E-commerce API",
                    "cloudProvider": ["aws", "gcp"],
                    "hasDocker": "si"
                }
            }
        }


class IterationCreate(BaseModel):
    """Schema para agregar una iteración"""
    yaml_config: Dict[str, Any] = Field(..., description="Nuevo YAML de Copilot")
    needs_more_info: bool = Field(default=True, description="¿Necesita más info?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "yaml_config": {
                    "title": "🚀 Deployment - Iteración 2",
                    "sections": []
                },
                "needs_more_info": True
            }
        }


# ============================================
# RESPONSE SCHEMAS
# ============================================

class AnalysisResponse(BaseModel):
    """Schema de respuesta de una sesión de análisis"""
    id: str
    project_id: str
    project_name: str
    analysis_type: AnalysisType
    status: AnalysisStatus
    yaml_config: Dict[str, Any]
    answers: Dict[str, Any]
    iteration: int
    needs_more_info: bool
    share_token: str
    share_url: str
    created_by: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PublicAnalysisResponse(BaseModel):
    """Schema de respuesta para URL pública (sin info sensible)"""
    project_name: str
    analysis_type: AnalysisType
    yaml_config: Dict[str, Any]
    answers: Dict[str, Any]
    iteration: int
    
    class Config:
        from_attributes = True
