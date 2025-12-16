"""
Validador de estructura YAML para formularios
"""
import yaml
from typing import Dict, Any, List
from pydantic import BaseModel, Field, validator


class YAMLQuestion(BaseModel):
    """Estructura de una pregunta en el YAML"""
    id: str
    type: str
    label: str
    placeholder: str = ""
    required: bool = False
    help: str = ""
    rows: int = 3
    options: List[Dict[str, str]] = []
    default: str = ""
    showOther: bool = False
    otherPlaceholder: str = ""
    
    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['text', 'textarea', 'select', 'radio', 'checkbox']
        if v not in allowed_types:
            raise ValueError(f'type debe ser uno de: {allowed_types}')
        return v


class YAMLSection(BaseModel):
    """Estructura de una sección en el YAML"""
    icon: str
    title: str
    description: str = ""
    questions: List[Dict[str, Any]]


class YAMLConfig(BaseModel):
    """Estructura completa del YAML"""
    title: str
    description: str
    warning: Dict[str, Any] = None
    sections: List[Dict[str, Any]]
    
    @validator('sections')
    def validate_sections(cls, v):
        if not v or len(v) == 0:
            raise ValueError('sections no puede estar vacío')
        return v


def validate_yaml_structure(yaml_dict: Dict[str, Any]) -> bool:
    """
    Valida que un diccionario tenga la estructura correcta de YAML
    
    Args:
        yaml_dict: Diccionario a validar
    
    Returns:
        True si es válido
    
    Raises:
        ValueError: Si la estructura no es válida
    """
    try:
        YAMLConfig(**yaml_dict)
        return True
    except Exception as e:
        raise ValueError(f"YAML inválido: {str(e)}")


def parse_yaml_string(yaml_str: str) -> Dict[str, Any]:
    """
    Parsea un string YAML y lo valida
    
    Args:
        yaml_str: String YAML
    
    Returns:
        Diccionario con el YAML parseado
    
    Raises:
        ValueError: Si el YAML es inválido
    """
    try:
        yaml_dict = yaml.safe_load(yaml_str)
        validate_yaml_structure(yaml_dict)
        return yaml_dict
    except yaml.YAMLError as e:
        raise ValueError(f"Error parseando YAML: {str(e)}")
    except Exception as e:
        raise ValueError(f"YAML inválido: {str(e)}")
