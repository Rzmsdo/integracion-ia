"""
Modelos Pydantic para validación de datos.
Define la estructura de las peticiones y respuestas de la API.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


# ==================== Enums ====================

class AnalysisType(str, Enum):
    """Tipos de análisis disponibles"""
    GENERAL = "general"
    SUMMARY = "summary"
    KEY_POINTS = "key_points"
    SENTIMENT = "sentiment"
    COMPREHENSIVE = "comprehensive"
    ENTITIES = "entities"
    QUESTIONS = "questions"


class FileType(str, Enum):
    """Tipos de archivo soportados"""
    PDF = ".pdf"
    DOCX = ".docx"
    DOC = ".doc"
    TXT = ".txt"
    MD = ".md"
    MARKDOWN = ".markdown"


# ==================== Request Models ====================

class AnalysisRequest(BaseModel):
    """Request para análisis de texto directo"""
    text: str = Field(..., description="Texto a analizar", min_length=10)
    analysis_type: AnalysisType = Field(
        default=AnalysisType.GENERAL,
        description="Tipo de análisis a realizar"
    )
    user_id: Optional[str] = Field(
        default="demo_user",
        description="ID del usuario (temporal hasta implementar auth)"
    )
    
    @validator('text')
    def validate_text_length(cls, v):
        if len(v) > 100000:  # 100k caracteres max
            raise ValueError("Texto demasiado largo. Máximo 100,000 caracteres.")
        return v


class DocumentAnalysisConfig(BaseModel):
    """Configuración para análisis de documento"""
    analysis_type: AnalysisType = Field(
        default=AnalysisType.COMPREHENSIVE,
        description="Tipo de análisis"
    )
    save_to_db: bool = Field(
        default=True,
        description="Guardar resultado en base de datos"
    )
    max_text_length: Optional[int] = Field(
        default=None,
        description="Longitud máxima de texto a procesar (trunca si es mayor)"
    )


# ==================== Response Models ====================

class TextStatistics(BaseModel):
    """Estadísticas de un texto"""
    character_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    average_word_length: float
    average_sentence_length: float


class AnalysisMetadata(BaseModel):
    """Metadata del análisis"""
    text_length: int
    word_count: int
    char_count: int
    model_used: str
    analyzed_at: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None


class AnalysisResult(BaseModel):
    """Resultado de un análisis"""
    type: str
    summary: Optional[str] = None
    key_points: Optional[str] = None
    sentiment: Optional[str] = None
    entities: Optional[str] = None
    questions: Optional[str] = None
    metadata: AnalysisMetadata


class DocumentAnalysisResponse(BaseModel):
    """Respuesta completa de análisis de documento"""
    success: bool = True
    message: str
    filename: str
    file_size: int
    file_type: str
    analysis: AnalysisResult
    analysis_id: Optional[str] = None
    statistics: Optional[TextStatistics] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Documento analizado exitosamente",
                "filename": "documento.pdf",
                "file_size": 245678,
                "file_type": ".pdf",
                "analysis": {
                    "type": "comprehensive",
                    "summary": "Este documento trata sobre...",
                    "key_points": "1. Punto principal...",
                    "sentiment": "El sentimiento general es positivo...",
                    "metadata": {
                        "text_length": 5000,
                        "word_count": 800,
                        "char_count": 5000,
                        "model_used": "llama3.2"
                    }
                },
                "analysis_id": "abc-123-def-456"
            }
        }


class AnalysisListItem(BaseModel):
    """Item de lista de análisis"""
    id: str
    user_id: str
    document_name: str
    analysis_type: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


class AnalysisListResponse(BaseModel):
    """Respuesta de lista de análisis"""
    success: bool = True
    total: int
    analyses: List[AnalysisListItem]


class AnalysisDetailResponse(BaseModel):
    """Respuesta detallada de un análisis"""
    success: bool = True
    id: str
    user_id: str
    document_name: str
    analysis_type: str
    summary: Optional[str] = None
    key_points: Optional[str] = None
    sentiment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: Optional[str] = None


class DeleteAnalysisResponse(BaseModel):
    """Respuesta de eliminación de análisis"""
    success: bool = True
    message: str
    deleted_id: str


class StatisticsResponse(BaseModel):
    """Respuesta de estadísticas de usuario"""
    success: bool = True
    user_id: str
    total_analyses: int
    analyses_by_type: Dict[str, int]
    total_documents: int


class HealthCheckResponse(BaseModel):
    """Respuesta del health check"""
    status: str
    ollama_available: bool
    supabase_connected: bool
    timestamp: str


class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Validation Error",
                "detail": "El archivo es demasiado grande"
            }
        }


# ==================== Database Models ====================

class AnalysisDB(BaseModel):
    """Modelo de análisis en la base de datos"""
    id: Optional[str] = None
    user_id: str
    document_name: str
    analysis_type: str
    summary: Optional[str] = None
    key_points: Optional[str] = None
    sentiment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True
