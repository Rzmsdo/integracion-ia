"""
Inicialización de modelos.
"""

from app.models.schemas import (
    # Enums
    AnalysisType,
    FileType,
    # Request Models
    AnalysisRequest,
    DocumentAnalysisConfig,
    # Response Models
    TextStatistics,
    AnalysisMetadata,
    AnalysisResult,
    DocumentAnalysisResponse,
    AnalysisListItem,
    AnalysisListResponse,
    AnalysisDetailResponse,
    DeleteAnalysisResponse,
    StatisticsResponse,
    HealthCheckResponse,
    ErrorResponse,
    # Database Models
    AnalysisDB
)

__all__ = [
    # Enums
    "AnalysisType",
    "FileType",
    # Request Models
    "AnalysisRequest",
    "DocumentAnalysisConfig",
    # Response Models
    "TextStatistics",
    "AnalysisMetadata",
    "AnalysisResult",
    "DocumentAnalysisResponse",
    "AnalysisListItem",
    "AnalysisListResponse",
    "AnalysisDetailResponse",
    "DeleteAnalysisResponse",
    "StatisticsResponse",
    "HealthCheckResponse",
    "ErrorResponse",
    # Database Models
    "AnalysisDB"
]
