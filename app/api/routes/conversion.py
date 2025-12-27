from fastapi import APIRouter, UploadFile, File, HTTPException, status, BackgroundTasks, Header, Request
from fastapi.responses import FileResponse
import os
from pathlib import Path
from typing import Optional
from app.services.conversion_service import ConversionService
from app.models.schemas import ConversionResponse
from app.core.security import MASTER_TOKEN, validate_token
from app.core.rate_limiting import limiter, CONVERSION_RATE_LIMIT

router = APIRouter()
conversion_service = ConversionService()


def delete_file(file_path: str):
    """Função para deletar arquivo em background"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo deletado: {file_path}")
    except Exception as e:
        print(f"Erro ao deletar arquivo {file_path}: {str(e)}")


@router.post("/docx-to-pdf", response_class=FileResponse)
@limiter.limit(CONVERSION_RATE_LIMIT)
async def convert_docx_to_pdf(
    request: Request,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    x_api_key: str = Header(...)
):
    """
    Converte arquivo DOCX para PDF
    
    **Autenticação:** Envie o token no header `x-api-key`
    
    **Rate limit:** 5 conversões por minuto
    
    - **file**: Arquivo DOCX a ser convertido
    - **x-api-key**: Token de autenticação (obrigatório)
    """
    try:
        # Validar token
        if not validate_token(x_api_key, MASTER_TOKEN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido"
            )
        
        # Validar extensão
        if not file.filename.lower().endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas arquivos .docx são permitidos"
            )
        
        # Ler arquivo
        contents = await file.read()
        
        # Converter
        pdf_path = await conversion_service.docx_to_pdf(contents, file.filename)
        
        # Agendar deleção após envio
        background_tasks.add_task(delete_file, pdf_path)
        
        return FileResponse(
            path=pdf_path,
            filename=file.filename.replace('.docx', '.pdf'),
            media_type='application/pdf'
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na conversão: {str(e)}"
        )


@router.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Verifica se o serviço de conversão está funcionando"""
    return {"status": "ok", "service": "conversion"}
