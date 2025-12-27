import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# API
API_V1_STR = "/api/v1"

# Arquivos
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {"docx"}

# Conversão
CONVERSION_TIMEOUT = 300  # 5 minutos
