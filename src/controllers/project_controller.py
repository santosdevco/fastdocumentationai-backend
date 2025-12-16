"""
Controlador de Proyectos
"""
from typing import List
from beanie import PydanticObjectId
from datetime import datetime

from ..models.project import Project, ProjectStatus


class ProjectController:
    """Lógica de negocio para Proyectos"""
    
    @staticmethod
    async def create_project(
        name: str,
        description: str,
        created_by: str,
        metadata: dict = None
    ) -> Project:
        """Crea un nuevo proyecto"""
        project = Project(
            name=name,
            description=description,
            created_by=created_by,
            metadata=metadata or {},
            status=ProjectStatus.ACTIVE
        )
        await project.insert()
        return project
    
    @staticmethod
    async def get_project(project_id: PydanticObjectId) -> Project:
        """Obtiene un proyecto por ID"""
        project = await Project.get(project_id)
        if not project:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        return project
    
    @staticmethod
    async def list_projects(
        status: ProjectStatus = None,
        created_by: str = None,
        limit: int = 100,
        skip: int = 0
    ) -> List[Project]:
        """Lista proyectos con filtros opcionales"""
        query = {}
        
        if status:
            query['status'] = status
        if created_by:
            query['created_by'] = created_by
        
        projects = await Project.find(query)\
            .sort("-created_at")\
            .skip(skip)\
            .limit(limit)\
            .to_list()
        
        return projects
    
    @staticmethod
    async def update_project(
        project_id: PydanticObjectId,
        name: str = None,
        description: str = None,
        status: ProjectStatus = None,
        metadata: dict = None
    ) -> Project:
        """Actualiza un proyecto"""
        project = await ProjectController.get_project(project_id)
        
        if name:
            project.name = name
        if description:
            project.description = description
        if status:
            project.status = status
        if metadata:
            project.metadata.update(metadata)
        
        project.updated_at = datetime.utcnow()
        await project.save()
        
        return project
    
    @staticmethod
    async def delete_project(project_id: PydanticObjectId) -> bool:
        """Elimina un proyecto (soft delete)"""
        project = await ProjectController.get_project(project_id)
        project.status = ProjectStatus.ARCHIVED
        project.updated_at = datetime.utcnow()
        await project.save()
        return True
