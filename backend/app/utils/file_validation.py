"""
Utilidades para validación de archivos.
"""

from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import get_settings

settings = get_settings()


def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """
    Valida la extensión de un archivo.
    
    Args:
        filename: Nombre del archivo
    
    Returns:
        Tupla (es_válido, extensión)
    """
    extension = Path(filename).suffix.lower()
    is_valid = extension in settings.ALLOWED_EXTENSIONS
    return is_valid, extension


def validate_file_size(file_size: int) -> bool:
    """
    Valida el tamaño de un archivo.
    
    Args:
        file_size: Tamaño en bytes
    
    Returns:
        True si es válido
    """
    return file_size <= settings.MAX_FILE_SIZE


async def validate_upload_file(file: UploadFile) -> Tuple[bool, str, str]:
    """
    Valida completamente un archivo subido.
    
    Args:
        file: UploadFile de FastAPI
    
    Returns:
        Tupla (es_válido, mensaje, extensión)
    
    Raises:
        HTTPException si el archivo no es válido
    """
    # Validar extensión
    is_valid_ext, extension = validate_file_extension(file.filename)
    if not is_valid_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {extension}. "
                   f"Extensiones permitidas: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Validar tamaño
    file.file.seek(0, 2)  # Ir al final del archivo
    file_size = file.file.tell()
    file.file.seek(0)  # Volver al inicio
    
    if not validate_file_size(file_size):
        max_size_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"Archivo demasiado grande. Tamaño máximo: {max_size_mb:.1f}MB"
        )
    
    return True, "Archivo válido", extension


def get_safe_filename(filename: str) -> str:
    """
    Limpia un nombre de archivo para hacerlo seguro.
    
    Args:
        filename: Nombre del archivo original
    
    Returns:
        Nombre de archivo seguro
    """
    import re
    import uuid
    
    # Obtener extensión
    path = Path(filename)
    extension = path.suffix
    name = path.stem
    
    # Limpiar el nombre (solo alfanuméricos, guiones y guiones bajos)
    safe_name = re.sub(r'[^\w\-]', '_', name)
    
    # Agregar un UUID corto para evitar colisiones
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{safe_name}_{unique_id}{extension}"
