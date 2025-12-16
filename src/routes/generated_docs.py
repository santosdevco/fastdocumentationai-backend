"""
Rutas de Documentos Generados
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime

from ..controllers.generated_doc_controller import GeneratedDocController

router = APIRouter(prefix="/api", tags=["generated-docs"])


# ============================================
# SCHEMAS
# ============================================

class GeneratedFileSchema(BaseModel):
    """Schema de un archivo generado"""
    path: str = Field(..., description="Ruta del archivo")
    content: str = Field(..., description="Contenido markdown")
    
    class Config:
        json_schema_extra = {
            "example": {
                "path": "ai_docs/06-infraestructura/01-deployment.md",
                "content": "# Deployment\n\n..."
            }
        }


class GeneratedDocsCreate(BaseModel):
    """Schema para guardar documentos generados"""
    analysis_session_id: str = Field(..., description="ID de la sesión de análisis")
    files: List[GeneratedFileSchema] = Field(..., description="Archivos generados")
    generated_by: str = Field(..., description="Email de quien guardó")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_session_id": "507f1f77bcf86cd799439011",
                "files": [
                    {
                        "path": "ai_docs/06-infraestructura/01-deployment.md",
                        "content": "# Deployment\n\n..."
                    }
                ],
                "generated_by": "analista@empresa.com"
            }
        }


class GeneratedDocsResponse(BaseModel):
    """Schema de respuesta de documentos generados"""
    id: str
    project_id: str
    project_name: str
    analysis_session_id: str
    files: List[Dict[str, Any]]
    generated_at: datetime
    generated_by: str
    
    class Config:
        from_attributes = True


# ============================================
# ENDPOINTS
# ============================================

@router.post("/projects/{project_id}/generate-docs", response_model=GeneratedDocsResponse, status_code=status.HTTP_201_CREATED)
async def save_generated_docs(project_id: str, data: GeneratedDocsCreate):
    """
    Guarda los archivos .md generados por Copilot
    
    El analista copia y pega los archivos generados por Copilot en el paso final
    """
    try:
        # Convertir files a dict
        files_dict = [file.dict() for file in data.files]
        
        doc = await GeneratedDocController.save_generated_docs(
            project_id=PydanticObjectId(project_id),
            analysis_session_id=PydanticObjectId(data.analysis_session_id),
            files=files_dict,
            generated_by=data.generated_by
        )
        
        await doc.fetch_link(doc.project)
        
        return GeneratedDocsResponse(
            id=str(doc.id),
            project_id=str(doc.project.id),
            project_name=doc.project.name,
            analysis_session_id=str(doc.analysis_session.ref.id),
            files=doc.files,
            generated_at=doc.generated_at,
            generated_by=doc.generated_by
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/projects/{project_id}/docs", response_model=List[GeneratedDocsResponse])
async def get_project_docs(project_id: str):
    """Lista todos los documentos generados de un proyecto"""
    try:
        docs = await GeneratedDocController.get_project_docs(
            project_id=PydanticObjectId(project_id)
        )
        
        result = []
        for doc in docs:
            await doc.fetch_link(doc.project)
            result.append(GeneratedDocsResponse(
                id=str(doc.id),
                project_id=str(doc.project.id),
                project_name=doc.project.name,
                analysis_session_id=str(doc.analysis_session.ref.id),
                files=doc.files,
                generated_at=doc.generated_at,
                generated_by=doc.generated_by
            ))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/docs/{doc_id}", response_model=GeneratedDocsResponse)
async def get_doc(doc_id: str):
    """Obtiene un documento por ID"""
    try:
        doc = await GeneratedDocController.get_doc(PydanticObjectId(doc_id))
        await doc.fetch_link(doc.project)
        
        return GeneratedDocsResponse(
            id=str(doc.id),
            project_id=str(doc.project.id),
            project_name=doc.project.name,
            analysis_session_id=str(doc.analysis_session.ref.id),
            files=doc.files,
            generated_at=doc.generated_at,
            generated_by=doc.generated_by
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
