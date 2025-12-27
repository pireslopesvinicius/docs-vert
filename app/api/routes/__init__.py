from fastapi import APIRouter
from .conversion import router as conversion_router

api_router = APIRouter()
api_router.include_router(conversion_router, prefix="/conversion", tags=["conversion"])

__all__ = ["api_router"]
