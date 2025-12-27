from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from app.core.security import api_key_manager
from app.core.rate_limiting import limiter, API_KEY_RATE_LIMIT

router = APIRouter()


class APIKeyRequest(BaseModel):
    """Requisição para gerar API key"""
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Minha aplicação"
            }
        }


class APIKeyResponse(BaseModel):
    """Resposta com API key gerada"""
    api_key: str
    name: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "api_key": "docs-vert-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "name": "Minha aplicação",
                "message": "Guarde esta chave com segurança. Você não poderá recuperá-la depois."
            }
        }


@router.post("/generate", response_model=APIKeyResponse)
@limiter.limit(API_KEY_RATE_LIMIT)
async def generate_api_key(request: APIKeyRequest, request_=None):
    """
    Gera uma nova API key
    
    **Rate limit:** 3 por hora
    
    - **name**: Nome/descrição da chave
    """
    if not request.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome da API key não pode estar vazio"
        )
    
    api_key = api_key_manager.generate_key(request.name)
    
    return APIKeyResponse(
        api_key=api_key,
        name=request.name,
        message="Guarde esta chave com segurança. Você não poderá recuperá-la depois."
    )


@router.get("/list")
@limiter.limit("5/minute")
async def list_api_keys(request_=None):
    """
    Lista todas as API keys (apenas preview)
    
    **Rate limit:** 5 por minuto
    """
    return {"keys": api_key_manager.list_keys()}


@router.delete("/{api_key}")
@limiter.limit("5/minute")
async def revoke_api_key(api_key: str, request_=None):
    """
    Revoga uma API key
    
    **Rate limit:** 5 por minuto
    
    - **api_key**: A chave a revogar
    """
    if api_key_manager.revoke_key(api_key):
        return {"message": "API key revogada com sucesso"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key não encontrada"
        )
