"""
Rutas de Proyectos
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from ..controllers.project_controller import ProjectController
from .schemas.project_schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from ..models.project import ProjectStatus

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate):
    """
    Crea un nuevo proyecto
    
    - **name**: Nombre del proyecto
    - **description**: Descripción opcional
    - **created_by**: Email del creador
    - **metadata**: Información adicional (repository, technology, etc.)
    """
    try:
        project = await ProjectController.create_project(
            name=data.name,
            description=data.description,
            created_by=data.created_by,
            metadata=data.metadata
        )
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at,
            status=project.status,
            metadata=project.metadata
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: ProjectStatus = None,
    created_by: str = None,
    limit: int = 100,
    skip: int = 0
):
    """
    Lista todos los proyectos con filtros opcionales
    
    - **status**: Filtrar por estado (active, completed, archived)
    - **created_by**: Filtrar por creador
    - **limit**: Límite de resultados
    - **skip**: Cantidad a omitir (paginación)
    """
    projects = await ProjectController.list_projects(
        status=status,
        created_by=created_by,
        limit=limit,
        skip=skip
    )
    
    return [
        ProjectResponse(
            id=str(p.id),
            name=p.name,
            description=p.description,
            created_by=p.created_by,
            created_at=p.created_at,
            updated_at=p.updated_at,
            status=p.status,
            metadata=p.metadata
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Obtiene un proyecto por ID"""
    try:
        project = await ProjectController.get_project(PydanticObjectId(project_id))
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at,
            status=project.status,
            metadata=project.metadata
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


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, data: ProjectUpdate):
    """Actualiza un proyecto"""
    try:
        project = await ProjectController.update_project(
            project_id=PydanticObjectId(project_id),
            name=data.name,
            description=data.description,
            status=data.status,
            metadata=data.metadata
        )
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            created_by=project.created_by,
            created_at=project.created_at,
            updated_at=project.updated_at,
            status=project.status,
            metadata=project.metadata
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


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str):
    """Elimina un proyecto (soft delete)"""
    try:
        await ProjectController.delete_project(PydanticObjectId(project_id))
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
