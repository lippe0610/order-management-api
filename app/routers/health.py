"""
Router para endpoints de salud y utilidades del sistema.
Incluye health checks y información general de la API.
"""
from fastapi import APIRouter
from datetime import datetime
from app.models.responses import HealthResponse
from app.core.config import settings

# Crear router para health checks
router = APIRouter(
    tags=["health"],
    responses={
        200: {"description": "Servicio saludable"}
    }
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Endpoint para verificar el estado del servicio"
)
async def health_check() -> HealthResponse:
    """
    Endpoint de health check para verificar que el servicio esté funcionando.
    
    Returns:
        HealthResponse: Estado del servicio con timestamp
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@router.get(
    "/",
    summary="Información de la API",
    description="Endpoint raíz con información básica de la API"
)
async def root():
    """
    Endpoint raíz con información básica de la API.
    
    Returns:
        Dict con información de la API
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_url": "/health"
    }

