"""
Configuración centralizada de la aplicación.
Maneja todas las variables de entorno y settings del proyecto.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings.
    Lee automáticamente desde variables de entorno o archivo .env
    """
    
    # ============== API Configuration ==============
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Document Analyzer API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para análisis de documentos usando IA local (Ollama)"
    
    # ============== Supabase Configuration ==============
    SUPABASE_URL: str = ""  # Opcional hasta configurar
    SUPABASE_KEY: str = ""  # Anon key para operaciones del cliente
    SUPABASE_SERVICE_KEY: str = ""  # Service key para operaciones administrativas
    
    # ============== Ollama Configuration ==============
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_TIMEOUT: int = 120  # Timeout en segundos para requests a Ollama
    
    # ============== Security Configuration ==============
    SECRET_KEY: str = "45b7b9dec975758ae5aaf3dc43c6d65da153431b39f6c46319ac09a8889b26d9"  # Cambiar en producción
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ============== File Upload Configuration ==============
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB por defecto
    UPLOAD_DIR: str = "uploads"
    
    # Extensiones permitidas (se define como propiedad para evitar problemas con .env)
    @property
    def ALLOWED_EXTENSIONS(self) -> set:
        return {".pdf", ".txt", ".docx", ".md", ".doc"}
    
    # ============== CORS Configuration ==============
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
        ]
    
    # ============== Server Configuration ==============
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    LOG_LEVEL: str = "INFO"
    
    # ============== Rate Limiting ==============
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # ============== Database Configuration (si usas SQL local) ==============
    DATABASE_URL: str = "sqlite:///./document_analyzer.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorar campos extra del .env
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Crear directorio de uploads si no existe
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
    
    @property
    def is_production(self) -> bool:
        """Detecta si estamos en producción"""
        return not self.RELOAD
    
    def get_allowed_extensions_list(self) -> List[str]:
        """Retorna las extensiones permitidas como lista"""
        return list(self.ALLOWED_EXTENSIONS)


@lru_cache()
def get_settings() -> Settings:
    """
    Función cacheada para obtener settings.
    El decorador @lru_cache() asegura que Settings se instancie una sola vez.
    """
    return Settings()


# Instancia global de settings (opcional, para acceso directo)
settings = get_settings()
