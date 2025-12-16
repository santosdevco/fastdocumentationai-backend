"""
Modelo de Proyecto
"""
from beanie import Document
from pydantic import Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    """Estados del proyecto"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Document):
    """
    Modelo de Proyecto en MongoDB
    
    Representa un sistema/aplicación que será documentado
    """
    
    name: str = Field(..., description="Nombre del proyecto")
    description: Optional[str] = Field(None, description="Descripción del proyecto")
    
    created_by: str = Field(..., description="Email del creador")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    status: ProjectStatus = Field(
        default=ProjectStatus.ACTIVE,
        description="Estado del proyecto"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Información adicional (repository, technology, etc.)"
    )
    
    class Settings:
        name = "projects"
        indexes = [
            "name",
            "created_by",
            "status",
            "created_at",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sistema E-commerce",
                "description": "Plataforma de ventas online",
                "created_by": "analista@empresa.com",
                "status": "active",
                "metadata": {
                    "repository": "https://github.com/empresa/ecommerce",
                    "technology": "Python + FastAPI + React"
                }
            }
        }
    
    def __repr__(self):
        return f"<Project {self.name}>"
    
    def __str__(self):
        return self.name
