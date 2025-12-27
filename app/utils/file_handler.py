import os
from pathlib import Path
from app.core.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from app.core.exceptions import InvalidFileTypeException, FileTooLargeException


def validate_file(filename: str, file_size: int) -> bool:
    """
    Valida arquivo enviado
    
    Args:
        filename: Nome do arquivo
        file_size: Tamanho do arquivo em bytes
        
    Returns:
        True se válido
        
    Raises:
        InvalidFileTypeException: Se extensão não permitida
        FileTooLargeException: Se arquivo muito grande
    """
    # Verificar extensão
    extension = filename.rsplit('.', 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidFileTypeException(
            f"Extensão '{extension}' não permitida. Permitidas: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Verificar tamanho
    if file_size > MAX_FILE_SIZE:
        raise FileTooLargeException(
            f"Arquivo maior que {MAX_FILE_SIZE / (1024*1024):.0f}MB"
        )
    
    return True


def get_safe_filename(filename: str) -> str:
    """Remove caracteres perigosos do nome do arquivo"""
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename[:255]
