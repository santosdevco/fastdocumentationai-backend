"""
Rutas de Análisis (Sesiones de Preguntas/Respuestas)
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from ..controllers.analysis_controller import AnalysisController
from .schemas.analysis_schemas import (
    AnalysisCreate,
    AnswersUpdate,
    IterationCreate,
    AnalysisResponse,
    PublicAnalysisResponse
)
from ..config.settings import settings
from ..models.analysis_session import AnalysisType

router = APIRouter(prefix="/api", tags=["analysis"])


# ============================================
# RUTAS PRIVADAS (para el analista)
# ============================================

@router.post("/projects/{project_id}/analysis", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(project_id: str, data: AnalysisCreate):
    """
    Crea una nueva sesión de análisis
    
    El analista pega el YAML generado por Copilot y obtiene una URL para compartir
    """
    try:
        session = await AnalysisController.create_analysis(
            project_id=PydanticObjectId(data.project_id),
            analysis_type=data.analysis_type,
            yaml_config=data.yaml_config,
            created_by=data.created_by,
            assigned_to=data.assigned_to
        )
        
        # Obtener nombre del proyecto
        await session.fetch_link('project')
        
        return AnalysisResponse(
            id=str(session.id),
            project_id=str(session.project.id),
            project_name=session.project.name,
            analysis_type=session.analysis_type,
            status=session.status,
            yaml_config=session.yaml_config,
            answers=session.answers,
            iteration=session.iteration,
            needs_more_info=session.needs_more_info,
            share_token=session.share_token,
            share_url=session.get_share_url(settings.frontend_url),
            created_by=session.created_by,
            assigned_to=session.assigned_to,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """Obtiene una sesión de análisis (para el analista)"""
    try:
        session = await AnalysisController.get_analysis(PydanticObjectId(analysis_id))
        await session.fetch_link('project')
        
        return AnalysisResponse(
            id=str(session.id),
            project_id=str(session.project.id),
            project_name=session.project.name,
            analysis_type=session.analysis_type,
            status=session.status,
            yaml_config=session.yaml_config,
            answers=session.answers,
            iteration=session.iteration,
            needs_more_info=session.needs_more_info,
            share_token=session.share_token,
            share_url=session.get_share_url(settings.frontend_url),
            created_by=session.created_by,
            assigned_to=session.assigned_to,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/analysis/{analysis_id}/iteration", response_model=AnalysisResponse)
async def add_iteration(analysis_id: str, data: IterationCreate):
    """
    Agrega una nueva iteración (Copilot generó nuevo YAML)
    
    El analista pega el nuevo YAML y obtiene una nueva URL para compartir
    """
    try:
        session = await AnalysisController.add_iteration(
            analysis_id=PydanticObjectId(analysis_id),
            yaml_config=data.yaml_config,
            needs_more_info=data.needs_more_info
        )
        
        await session.fetch_link('project')
        
        return AnalysisResponse(
            id=str(session.id),
            project_id=str(session.project.id),
            project_name=session.project.name,
            analysis_type=session.analysis_type,
            status=session.status,
            yaml_config=session.yaml_config,
            answers=session.answers,
            iteration=session.iteration,
            needs_more_info=session.needs_more_info,
            share_token=session.share_token,
            share_url=session.get_share_url(settings.frontend_url),
            created_by=session.created_by,
            assigned_to=session.assigned_to,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/analysis/{analysis_id}/complete", response_model=AnalysisResponse)
async def complete_analysis(analysis_id: str):
    """Marca el análisis como completo (Copilot dijo 'todo ok')"""
    try:
        session = await AnalysisController.complete_analysis(PydanticObjectId(analysis_id))
        await session.fetch_link('project')
        
        return AnalysisResponse(
            id=str(session.id),
            project_id=str(session.project.id),
            project_name=session.project.name,
            analysis_type=session.analysis_type,
            status=session.status,
            yaml_config=session.yaml_config,
            answers=session.answers,
            iteration=session.iteration,
            needs_more_info=session.needs_more_info,
            share_token=session.share_token,
            share_url=session.get_share_url(settings.frontend_url),
            created_by=session.created_by,
            assigned_to=session.assigned_to,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/projects/{project_id}/analyses", response_model=List[AnalysisResponse])
async def list_project_analyses(
    project_id: str,
    analysis_type: AnalysisType = None
):
    """Lista todas las sesiones de análisis de un proyecto"""
    try:
        sessions = await AnalysisController.list_project_analyses(
            project_id=PydanticObjectId(project_id),
            analysis_type=analysis_type
        )
        
        result = []
        for session in sessions:
            await session.fetch_link('project')
            result.append(AnalysisResponse(
                id=str(session.id),
                project_id=str(session.project.id),
                project_name=session.project.name,
                analysis_type=session.analysis_type,
                status=session.status,
                yaml_config=session.yaml_config,
                answers=session.answers,
                iteration=session.iteration,
                needs_more_info=session.needs_more_info,
                share_token=session.share_token,
                share_url=session.get_share_url(settings.frontend_url),
                created_by=session.created_by,
                assigned_to=session.assigned_to,
                created_at=session.created_at,
                updated_at=session.updated_at
            ))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================
# RUTAS PÚBLICAS (para responder preguntas)
# ============================================

@router.get("/answer/{share_token}", response_model=PublicAnalysisResponse)
async def get_public_analysis(share_token: str):
    """
    Obtiene una sesión de análisis por token (URL pública)
    
    Esta ruta NO requiere autenticación y se usa para que el experto
    pueda ver y responder las preguntas
    """
    try:
        session = await AnalysisController.get_analysis_by_token(share_token)
        await session.fetch_link('project')
        
        return PublicAnalysisResponse(
            project_name=session.project.name,
            analysis_type=session.analysis_type,
            yaml_config=session.yaml_config,
            answers=session.answers,
            iteration=session.iteration
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token inválido o expirado"
        )


@router.post("/answer/{share_token}", status_code=status.HTTP_200_OK)
async def update_public_answers(share_token: str, data: AnswersUpdate):
    """
    Guarda/actualiza respuestas del formulario (endpoint público)
    
    El experto completa el formulario y envía las respuestas
    """
    try:
        await AnalysisController.update_answers(
            share_token=share_token,
            answers=data.answers
        )
        
        return {
            "success": True,
            "message": "Respuestas guardadas correctamente"
        }
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


@router.get("/search/analyses", response_model=List[AnalysisResponse])
async def search_analyses(
    q: str,
    project_id: str = None,
    analysis_type: AnalysisType = None,
    limit: int = 50
):
    """
    Busca sesiones de análisis por texto en:
    - Título del YAML
    - Descripción del YAML
    - Preguntas del YAML
    - Respuestas del experto
    """
    try:
        sessions = await AnalysisController.search_analyses(
            query=q,
            project_id=PydanticObjectId(project_id) if project_id else None,
            analysis_type=analysis_type,
            limit=limit
        )
        
        result = []
        for session in sessions:
            await session.fetch_link('project')
            result.append(AnalysisResponse(
                id=str(session.id),
                project_id=str(session.project.id),
                project_name=session.project.name,
                analysis_type=session.analysis_type,
                status=session.status,
                yaml_config=session.yaml_config,
                answers=session.answers,
                iteration=session.iteration,
                needs_more_info=session.needs_more_info,
                share_token=session.share_token,
                share_url=session.get_share_url(settings.frontend_url),
                created_by=session.created_by,
                assigned_to=session.assigned_to,
                created_at=session.created_at,
                updated_at=session.updated_at
            ))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
