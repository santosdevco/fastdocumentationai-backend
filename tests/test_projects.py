"""
Tests para el controlador de proyectos
"""
import pytest
from beanie import PydanticObjectId

from src.models.project import Project, ProjectStatus
from src.controllers.project_controller import ProjectController


@pytest.mark.asyncio
async def test_create_project():
    """Test de creación de proyecto"""
    project = await ProjectController.create_project(
        name="Test Project",
        description="Test Description",
        created_by="test@example.com",
        metadata={"tech": "Python"}
    )
    
    assert project.name == "Test Project"
    assert project.description == "Test Description"
    assert project.created_by == "test@example.com"
    assert project.status == ProjectStatus.ACTIVE
    assert project.metadata["tech"] == "Python"


@pytest.mark.asyncio
async def test_list_projects():
    """Test de listado de proyectos"""
    # Crear algunos proyectos de prueba
    await ProjectController.create_project(
        name="Project 1",
        description="Desc 1",
        created_by="test@example.com"
    )
    
    await ProjectController.create_project(
        name="Project 2",
        description="Desc 2",
        created_by="test@example.com"
    )
    
    # Listar proyectos
    projects = await ProjectController.list_projects()
    
    assert len(projects) >= 2
