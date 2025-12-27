from pydantic import BaseModel
from typing import Optional


class ConversionResponse(BaseModel):
    """Resposta de conversão bem-sucedida"""
    message: str
    filename: str
    format: str = "pdf"
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Conversão realizada com sucesso",
                "filename": "documento.pdf",
                "format": "pdf"
            }
        }


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Erro na conversão"
            }
        }
