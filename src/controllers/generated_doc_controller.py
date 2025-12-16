"""
Controlador de Documentos Generados
"""
from typing import List, Dict, Any
from beanie import PydanticObjectId
from datetime import datetime

from ..models.generated_doc import GeneratedDoc
from ..models.analysis_session import AnalysisSession
from ..models.project import Project


class GeneratedDocController:
    """Lógica de negocio para Documentos Generados"""
    
    @staticmethod
    async def save_generated_docs(
        project_id: PydanticObjectId,
        analysis_session_id: PydanticObjectId,
        files: List[Dict[str, Any]],
        generated_by: str
    ) -> GeneratedDoc:
        """Guarda los archivos .md generados por Copilot"""
        
        # Validar que el proyecto existe
        project = await Project.get(project_id)
        if not project:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        # Validar que la sesión existe
        session = await AnalysisSession.get(analysis_session_id)
        if not session:
            raise ValueError(f"Sesión {analysis_session_id} no encontrada")
        
        # Agregar timestamp a cada archivo
        for file in files:
            if "generated_at" not in file:
                file["generated_at"] = datetime.utcnow()
        
        # Crear documento
        doc = GeneratedDoc(
            project=project,
            analysis_session=session,
            files=files,
            generated_by=generated_by
        )
        
        await doc.insert()
        return doc
    
    @staticmethod
    async def get_project_docs(
        project_id: PydanticObjectId
    ) -> List[GeneratedDoc]:
        """Lista todos los documentos generados de un proyecto"""
        docs = await GeneratedDoc.find(
            {"project.$id": project_id},
            fetch_links=True
        ).sort("-generated_at").to_list()
        
        return docs
    
    @staticmethod
    async def get_analysis_docs(
        analysis_session_id: PydanticObjectId
    ) -> GeneratedDoc:
        """Obtiene los documentos de una sesión específica"""
        doc = await GeneratedDoc.find_one(
            {"analysis_session.$id": analysis_session_id},
            fetch_links=True
        )
        return doc
    
    @staticmethod
    async def get_doc(doc_id: PydanticObjectId) -> GeneratedDoc:
        """Obtiene un documento por ID"""
        doc = await GeneratedDoc.get(doc_id, fetch_links=True)
        if not doc:
            raise ValueError(f"Documento {doc_id} no encontrado")
        return doc
