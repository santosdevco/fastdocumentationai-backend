"""
Esquemas Pydantic para Proyectos
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from ...models.project import ProjectStatus


# ============================================
# REQUEST SCHEMAS
# ============================================

class ProjectCreate(BaseModel):
    """Schema para crear un proyecto"""
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del proyecto")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción")
    created_by: str = Field(..., description="Email del creador")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata adicional")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sistema E-commerce",
                "description": "Plataforma de ventas online",
                "created_by": "analista@empresa.com",
                "metadata": {
                    "repository": "https://github.com/empresa/ecommerce",
                    "technology": "Python + FastAPI"
                }
            }
        }


class ProjectUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[ProjectStatus] = None
    metadata: Optional[Dict[str, Any]] = None


# ============================================
# RESPONSE SCHEMAS
# ============================================

class ProjectResponse(BaseModel):
    """Schema de respuesta de un proyecto"""
    id: str
    name: str
    description: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime
    status: ProjectStatus
    metadata: Dict[str, Any]
    
    class Config:
        from_attributes = True
