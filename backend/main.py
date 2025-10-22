"""
Document Analyzer API - FastAPI Application
Análisis de documentos usando IA local (Ollama) con almacenamiento en Supabase.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time

from app.core.config import settings
from app.api import api_router
from app.models import ErrorResponse

# ==================== Crear aplicación ====================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)


# ==================== Middleware ====================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log todas las requests con tiempo de procesamiento"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    
    return response


# ==================== Exception Handlers ====================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Maneja excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail,
            detail=str(exc.detail)
        ).dict()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            error="Validation Error",
            detail=str(exc.errors())
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal Server Error",
            detail=str(exc) if not settings.is_production else "An error occurred"
        ).dict()
    )


# ==================== Rutas ====================

# Incluir router principal de API
app.include_router(api_router, prefix=settings.API_V1_STR)


# Ruta raíz
@app.get("/", tags=["root"])
async def root():
    """
    Ruta raíz de la API.
    Proporciona información básica del servicio.
    """
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc",
        "health": f"{settings.API_V1_STR}/system/health",
        "status": "running"
    }


# ==================== Eventos de inicio/cierre ====================

@app.on_event("startup")
async def startup_event():
    """
    Evento ejecutado al iniciar la aplicación.
    Inicializa servicios y verifica conexiones.
    """
    print("=" * 60)
    print(f"🚀 Iniciando {settings.PROJECT_NAME} v{settings.VERSION}")
    print("=" * 60)
    print(f"📊 API docs disponibles en: {settings.API_V1_STR}/docs")
    print(f"🔧 Configuración:")
    print(f"   - Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"   - Modelo: {settings.OLLAMA_MODEL}")
    print(f"   - Supabase: {'✓ Configurado' if settings.SUPABASE_URL else '✗ No configurado'}")
    print(f"   - Max file size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB")
    print(f"   - Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}")
    print("=" * 60)
    
    # Verificar disponibilidad de servicios
    from app.services import ollama_service, supabase_service
    
    try:
        ollama_available = await ollama_service.check_model_availability()
        print(f"🤖 Ollama: {'✓ Disponible' if ollama_available else '✗ No disponible'}")
    except:
        print("🤖 Ollama: ✗ No disponible")
    
    try:
        supabase_connected = supabase_service.test_connection()
        print(f"💾 Supabase: {'✓ Conectado' if supabase_connected else '✗ No conectado'}")
    except:
        print("💾 Supabase: ✗ No conectado")
    
    print("=" * 60)
    print("✅ Servidor listo para recibir requests")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento ejecutado al cerrar la aplicación.
    Limpia recursos y cierra conexiones.
    """
    print("\n" + "=" * 60)
    print("🛑 Cerrando aplicación...")
    print("=" * 60)


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
