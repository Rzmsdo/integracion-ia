"""
Servicio de inicialización.
Permite acceso centralizado a todos los servicios.
"""

from app.services.ollama_service import ollama_service
from app.services.supabase_service import supabase_service

__all__ = ["ollama_service", "supabase_service"]
