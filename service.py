from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import uvicorn
from app.api.routes import api_router
from app.core.config import API_V1_STR
from app.core.rate_limiting import limiter

app = FastAPI(
    title="Docs Vert API",
    description="API de conversão de documentos - DOCX para PDF",
    version="0.1.0",
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(api_router, prefix=API_V1_STR)

@app.get('/')
async def read_root():
    return {
        "message": "Service is up and running!",
        "docs": "/docs",
        "version": "0.1.0",
        "endpoints": {
            "convert_docx_to_pdf": "POST /api/v1/conversion/docx-to-pdf",
            "health": "GET /api/v1/conversion/health"
        },
        "authentication": "Envie o token no header 'x-api-key'"
    }


@app.get('/health')
async def health():
    return {"status": "ok"}


def run():
    uvicorn.run('service:app', host='0.0.0.0', port=8000, reload=True)
