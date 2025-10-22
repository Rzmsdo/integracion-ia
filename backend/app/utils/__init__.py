"""
Inicialización del módulo de utilidades.
"""

from app.utils.text_extraction import (
    extract_text,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    get_text_statistics,
    truncate_text,
    clean_text
)

from app.utils.file_validation import (
    validate_file_extension,
    validate_file_size,
    validate_upload_file,
    get_safe_filename
)

__all__ = [
    # Text extraction
    "extract_text",
    "extract_text_from_pdf",
    "extract_text_from_docx",
    "extract_text_from_txt",
    "get_text_statistics",
    "truncate_text",
    "clean_text",
    # File validation
    "validate_file_extension",
    "validate_file_size",
    "validate_upload_file",
    "get_safe_filename"
]
