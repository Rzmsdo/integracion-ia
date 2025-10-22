"""
Inicialización de rutas de API.
"""

from fastapi import APIRouter
from app.api.routes import documents, system

api_router = APIRouter()

# Incluir routers de diferentes módulos
api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"]
)

api_router.include_router(
    system.router,
    prefix="/system",
    tags=["system"]
)
