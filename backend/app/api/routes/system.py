"""
Rutas de API para health checks y información del sistema.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models import HealthCheckResponse
from app.services import ollama_service, supabase_service
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Verifica el estado del sistema y sus dependencias"
)
async def health_check():
    """
    Endpoint de health check.
    Verifica la disponibilidad de Ollama y Supabase.
    """
    
    try:
        # Verificar Ollama
        ollama_available = await ollama_service.check_model_availability()
        
        # Verificar Supabase
        supabase_connected = supabase_service.test_connection()
        
        return HealthCheckResponse(
            status="healthy" if (ollama_available and supabase_connected) else "degraded",
            ollama_available=ollama_available,
            supabase_connected=supabase_connected,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en health check: {str(e)}"
        )


@router.get(
    "/models",
    summary="Listar modelos disponibles",
    description="Obtiene la lista de modelos de IA disponibles en Ollama"
)
async def list_available_models():
    """
    Lista todos los modelos disponibles en Ollama.
    """
    
    try:
        models = await ollama_service.get_available_models()
        
        return {
            "success": True,
            "current_model": settings.OLLAMA_MODEL,
            "available_models": models,
            "total": len(models)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo modelos: {str(e)}"
        )


@router.get(
    "/info",
    summary="Información del sistema",
    description="Obtiene información general sobre la API y su configuración"
)
async def get_system_info():
    """
    Retorna información general del sistema.
    """
    
    return {
        "success": True,
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "api_version": settings.API_V1_STR,
        "ollama": {
            "base_url": settings.OLLAMA_BASE_URL,
            "model": settings.OLLAMA_MODEL,
            "timeout": settings.OLLAMA_TIMEOUT
        },
        "file_upload": {
            "max_size_bytes": settings.MAX_FILE_SIZE,
            "max_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024),
            "allowed_extensions": list(settings.ALLOWED_EXTENSIONS)
        },
        "rate_limiting": {
            "requests_per_minute": settings.RATE_LIMIT_PER_MINUTE
        }
    }
