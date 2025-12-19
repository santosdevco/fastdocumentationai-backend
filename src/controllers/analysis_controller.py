"""
Controlador de Sesiones de Análisis
"""
from typing import List, Dict, Any, Optional
from beanie import PydanticObjectId
from datetime import datetime

from ..models.analysis_session import (
    AnalysisSession,
    AnalysisType,
    AnalysisStatus
)
from ..models.project import Project
from ..utils.token_generator import generate_share_token
from ..utils.yaml_validator import validate_yaml_structure
from ..config.settings import settings


class AnalysisController:
    """Lógica de negocio para Sesiones de Análisis"""
    
    @staticmethod
    async def create_analysis(
        project_id: PydanticObjectId,
        analysis_type: AnalysisType,
        yaml_config: Dict[str, Any],
        created_by: str,
        assigned_to: str = None
    ) -> AnalysisSession:
        """Crea una nueva sesión de análisis"""
        
        # Validar que el proyecto existe
        project = await Project.get(project_id)
        if not project:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        # Validar estructura del YAML
        validate_yaml_structure(yaml_config)
        
        # Generar token único
        share_token = generate_share_token()
        
        # Crear sesión
        session = AnalysisSession(
            project=project,
            analysis_type=analysis_type,
            yaml_config=yaml_config,
            share_token=share_token,
            created_by=created_by,
            assigned_to=assigned_to,
            iteration=1,
            needs_more_info=True,
            status=AnalysisStatus.PENDING_ANSWERS
        )
        
        await session.insert()
        return session
    
    @staticmethod
    async def get_analysis(analysis_id: PydanticObjectId) -> AnalysisSession:
        """Obtiene una sesión de análisis por ID"""
        session = await AnalysisSession.get(analysis_id, fetch_links=True)
        if not session:
            raise ValueError(f"Análisis {analysis_id} no encontrado")
        return session
    
    @staticmethod
    async def get_analysis_by_token(share_token: str) -> AnalysisSession:
        """Obtiene una sesión de análisis por token (para URL pública)"""
        session = await AnalysisSession.find_one(
            AnalysisSession.share_token == share_token,
            fetch_links=True
        )
        if not session:
            raise ValueError(f"Token {share_token} inválido o expirado")
        return session
    
    @staticmethod
    async def update_answers(
        share_token: str,
        answers: Dict[str, Any]
    ) -> AnalysisSession:
        """Actualiza las respuestas de una sesión (endpoint público)"""
        session = await AnalysisController.get_analysis_by_token(share_token)
        
        # Actualizar respuestas
        session.answers.update(answers)
        session.updated_at = datetime.utcnow()
        
        await session.save()
        return session
    
    @staticmethod
    async def add_iteration(
        analysis_id: PydanticObjectId,
        yaml_config: Dict[str, Any],
        needs_more_info: bool = True
    ) -> AnalysisSession:
        """Agrega una nueva iteración (nuevo YAML de Copilot)"""
        session = await AnalysisController.get_analysis(analysis_id)
        
        # Validar YAML
        validate_yaml_structure(yaml_config)
        
        # Guardar iteración anterior en historial
        iteration_record = {
            "iteration": session.iteration,
            "yaml_generated": session.yaml_config,
            "answers_provided": session.answers,
            "timestamp": datetime.utcnow()
        }
        session.iteration_history.append(iteration_record)
        
        # Actualizar a nueva iteración
        session.iteration += 1
        session.yaml_config = yaml_config
        session.needs_more_info = needs_more_info
        session.answers = {}  # Reset answers para nueva iteración
        
        # Generar nuevo token
        session.share_token = generate_share_token()
        session.updated_at = datetime.utcnow()
        
        await session.save()
        return session
    
    @staticmethod
    async def complete_analysis(analysis_id: PydanticObjectId) -> AnalysisSession:
        """Marca el análisis como completo (Copilot dijo 'todo ok')"""
        session = await AnalysisController.get_analysis(analysis_id)
        
        session.status = AnalysisStatus.COMPLETED
        session.needs_more_info = False
        session.updated_at = datetime.utcnow()
        
        await session.save()
        return session
    
    @staticmethod
    async def list_project_analyses(
        project_id: PydanticObjectId,
        analysis_type: AnalysisType = None
    ) -> List[AnalysisSession]:
        """Lista todas las sesiones de análisis de un proyecto"""
        query = {"project.$id": project_id}
        
        if analysis_type:
            query["analysis_type"] = analysis_type
        
        sessions = await AnalysisSession.find(query)\
            .sort("-created_at")\
            .to_list()
        
        return sessions

    @staticmethod
    async def search_analyses(
        query: str,
        project_id: Optional[PydanticObjectId] = None,
        analysis_type: Optional[AnalysisType] = None,
        limit: int = 50
    ) -> List[AnalysisSession]:
        """
        Busca sesiones de análisis en TODO el contenido del YAML y respuestas.
        Convierte el YAML completo a string para búsqueda universal.
        """
        import json
        
        # Construir filtro base
        base_filter = {}
        if project_id:
            base_filter["project"] = project_id
        if analysis_type:
            base_filter["analysis_type"] = analysis_type
        
        # Obtener todas las sesiones que cumplan filtros base
        all_sessions = await AnalysisSession.find(base_filter).to_list()
        
        # Filtrar en Python buscando en todo el contenido
        query_lower = query.lower()
        matching_sessions = []
        
        for session in all_sessions:
            # Convertir YAML config completo a JSON string
            yaml_str = json.dumps(session.yaml_config, ensure_ascii=False).lower()
            
            # Convertir answers completo a JSON string
            answers_str = json.dumps(session.answers or {}, ensure_ascii=False).lower()
            
            # Buscar en ambos strings
            if query_lower in yaml_str or query_lower in answers_str:
                matching_sessions.append(session)
                
                # Limitar resultados
                if len(matching_sessions) >= limit:
                    break
        
        # Ordenar por fecha (más recientes primero)
        matching_sessions.sort(key=lambda x: x.created_at, reverse=True)
        
        return matching_sessions[:limit]
