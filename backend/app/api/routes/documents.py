"""
Rutas de API para gestión de documentos y análisis.
Endpoints principales de la aplicación.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Path as PathParam
from typing import Optional
import uuid
from pathlib import Path
import os

from app.models import (
    DocumentAnalysisResponse,
    AnalysisListResponse,
    AnalysisDetailResponse,
    DeleteAnalysisResponse,
    StatisticsResponse,
    AnalysisRequest,
    DocumentAnalysisConfig,
    ErrorResponse
)
from app.services import ollama_service, supabase_service
from app.utils import (
    extract_text,
    validate_upload_file,
    get_safe_filename,
    get_text_statistics,
    truncate_text
)
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()

# Directorio para uploads temporales
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "/upload",
    response_model=DocumentAnalysisResponse,
    summary="Subir y analizar documento",
    description="Sube un documento (PDF, DOCX, TXT, MD) y recibe un análisis completo del contenido"
)
async def upload_and_analyze_document(
    file: UploadFile = File(..., description="Archivo a analizar"),
    user_id: str = Query(default="demo_user", description="ID del usuario"),
    analysis_type: str = Query(
        default="comprehensive",
        description="Tipo de análisis: general, summary, key_points, sentiment, comprehensive"
    ),
    save_to_db: bool = Query(default=True, description="Guardar resultado en base de datos")
):
    """
    Endpoint principal para subir y analizar documentos.
    
    Proceso:
    1. Validar archivo (tamaño, extensión)
    2. Extraer texto del documento
    3. Analizar con Ollama
    4. Guardar resultado en Supabase (opcional)
    5. Retornar resultado
    """
    
    file_path = None
    
    try:
        # 1. Validar archivo
        is_valid, message, extension = await validate_upload_file(file)
        
        # Obtener tamaño del archivo
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        # 2. Guardar temporalmente
        safe_filename = get_safe_filename(file.filename)
        file_path = UPLOAD_DIR / safe_filename
        
        with file_path.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 3. Extraer texto
        text = await extract_text(str(file_path), extension)
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer texto del documento o el contenido es demasiado corto"
            )
        
        # 4. Analizar con Ollama
        if analysis_type == "comprehensive":
            analysis = await ollama_service.analyze_comprehensive(text)
        else:
            result = await ollama_service.analyze_document(text, analysis_type)
            analysis = {
                "type": analysis_type,
                analysis_type: result,
                "metadata": {
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "char_count": len(text),
                    "model_used": ollama_service.model,
                    "file_size": file_size,
                    "file_type": extension
                }
            }
        
        # 5. Calcular estadísticas
        statistics = get_text_statistics(text)
        
        # 6. Guardar en Supabase (si se solicita)
        analysis_id = None
        if save_to_db:
            try:
                db_result = await supabase_service.save_analysis(
                    user_id=user_id,
                    document_name=file.filename,
                    analysis=analysis,
                    file_size=file_size,
                    file_type=extension,
                    original_text=text
                )
                analysis_id = db_result.get("id")
            except Exception as e:
                print(f"Warning: Could not save to database: {str(e)}")
                # No fallar si no se puede guardar en BD
        
        # 7. Preparar respuesta
        return DocumentAnalysisResponse(
            success=True,
            message="Documento analizado exitosamente",
            filename=file.filename,
            file_size=file_size,
            file_type=extension,
            analysis=analysis,
            analysis_id=analysis_id,
            statistics=statistics
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando documento: {str(e)}"
        )
    
    finally:
        # Limpiar archivo temporal
        if file_path and file_path.exists():
            try:
                os.remove(file_path)
            except:
                pass


@router.post(
    "/analyze-text",
    response_model=DocumentAnalysisResponse,
    summary="Analizar texto directo",
    description="Analiza texto enviado directamente sin subir archivo"
)
async def analyze_text(
    request: AnalysisRequest,
    save_to_db: bool = Query(default=False, description="Guardar en base de datos")
):
    """
    Analiza texto enviado directamente (sin archivo).
    """
    
    try:
        # Analizar con Ollama
        if request.analysis_type.value == "comprehensive":
            analysis = await ollama_service.analyze_comprehensive(request.text)
        else:
            result = await ollama_service.analyze_document(request.text, request.analysis_type.value)
            analysis = {
                "type": request.analysis_type.value,
                request.analysis_type.value: result,
                "metadata": {
                    "text_length": len(request.text),
                    "word_count": len(request.text.split()),
                    "char_count": len(request.text),
                    "model_used": ollama_service.model
                }
            }
        
        # Calcular estadísticas
        statistics = get_text_statistics(request.text)
        
        # Guardar en Supabase (si se solicita)
        analysis_id = None
        if save_to_db:
            try:
                db_result = await supabase_service.save_analysis(
                    user_id=request.user_id,
                    document_name="Text Analysis",
                    analysis=analysis
                )
                analysis_id = db_result.get("id")
            except Exception as e:
                print(f"Warning: Could not save to database: {str(e)}")
        
        return DocumentAnalysisResponse(
            success=True,
            message="Texto analizado exitosamente",
            filename="direct_text.txt",
            file_size=len(request.text.encode('utf-8')),
            file_type=".txt",
            analysis=analysis,
            analysis_id=analysis_id,
            statistics=statistics
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando texto: {str(e)}"
        )


@router.get(
    "/analyses",
    response_model=AnalysisListResponse,
    summary="Listar análisis",
    description="Obtiene la lista de análisis del usuario"
)
async def list_analyses(
    user_id: str = Query(default="demo_user", description="ID del usuario"),
    limit: int = Query(default=10, ge=1, le=100, description="Número de resultados"),
    offset: int = Query(default=0, ge=0, description="Offset para paginación")
):
    """
    Lista todos los análisis de un usuario con paginación.
    """
    
    try:
        analyses = await supabase_service.get_user_analyses(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        return AnalysisListResponse(
            success=True,
            total=len(analyses),
            analyses=analyses
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo análisis: {str(e)}"
        )


@router.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisDetailResponse,
    summary="Obtener análisis específico",
    description="Obtiene los detalles completos de un análisis"
)
async def get_analysis(
    analysis_id: str = PathParam(..., description="ID del análisis"),
    user_id: str = Query(default="demo_user", description="ID del usuario")
):
    """
    Obtiene un análisis específico por ID.
    """
    
    try:
        analysis = await supabase_service.get_analysis_by_id(analysis_id, user_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"Análisis no encontrado: {analysis_id}"
            )
        
        return AnalysisDetailResponse(
            success=True,
            **analysis
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo análisis: {str(e)}"
        )


@router.delete(
    "/analyses/{analysis_id}",
    response_model=DeleteAnalysisResponse,
    summary="Eliminar análisis",
    description="Elimina un análisis específico"
)
async def delete_analysis(
    analysis_id: str = PathParam(..., description="ID del análisis"),
    user_id: str = Query(default="demo_user", description="ID del usuario")
):
    """
    Elimina un análisis por ID.
    """
    
    try:
        success = await supabase_service.delete_analysis(analysis_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Análisis no encontrado: {analysis_id}"
            )
        
        return DeleteAnalysisResponse(
            success=True,
            message="Análisis eliminado exitosamente",
            deleted_id=analysis_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando análisis: {str(e)}"
        )


@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    summary="Estadísticas de usuario",
    description="Obtiene estadísticas de uso del usuario"
)
async def get_statistics(
    user_id: str = Query(default="demo_user", description="ID del usuario")
):
    """
    Obtiene estadísticas de análisis del usuario.
    """
    
    try:
        stats = await supabase_service.get_user_statistics(user_id)
        
        return StatisticsResponse(
            success=True,
            user_id=user_id,
            **stats
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )


@router.get(
    "/search",
    response_model=AnalysisListResponse,
    summary="Buscar análisis",
    description="Busca análisis por término de búsqueda"
)
async def search_analyses(
    user_id: str = Query(default="demo_user", description="ID del usuario"),
    query: str = Query(..., min_length=2, description="Término de búsqueda"),
    limit: int = Query(default=20, ge=1, le=100, description="Número de resultados")
):
    """
    Busca análisis por término en nombre de documento, resumen o puntos clave.
    """
    
    try:
        analyses = await supabase_service.search_analyses(
            user_id=user_id,
            search_term=query,
            limit=limit
        )
        
        return AnalysisListResponse(
            success=True,
            total=len(analyses),
            analyses=analyses
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error buscando análisis: {str(e)}"
        )
