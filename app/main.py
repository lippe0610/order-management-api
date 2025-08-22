"""
Aplicación principal de FastAPI para la API de gestión de pedidos.
Configura la aplicación, middlewares, CORS y registra todos los routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.core.config import settings
from app.routers import orders_router, health_router

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requests desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejador de errores de validación personalizado
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejador personalizado para errores de validación de Pydantic.
    
    Args:
        request: Request que causó el error
        exc: Excepción de validación
        
    Returns:
        JSONResponse con formato de error estándar
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Los datos proporcionados no son válidos",
            "details": exc.errors()
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """
    Manejador para errores de validación de Pydantic.
    
    Args:
        request: Request que causó el error
        exc: Excepción de validación de Pydantic
        
    Returns:
        JSONResponse con formato de error estándar
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Error de validación en los datos",
            "details": exc.errors()
        }
    )


# Registrar routers
app.include_router(health_router)
app.include_router(orders_router)


# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Útil para inicialización de recursos, conexiones a BD, etc.
    """
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION} iniciado")
    print(f"📚 Documentación disponible en: /docs")
    print(f"🔍 Health check disponible en: /health")


# Evento de cierre de la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    Útil para limpieza de recursos, cierre de conexiones, etc.
    """
    print(f"🛑 {settings.APP_NAME} detenido")


if __name__ == "__main__":
    import uvicorn
    
    # Configuración para desarrollo
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

