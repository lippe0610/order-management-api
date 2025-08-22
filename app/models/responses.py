"""
Modelos Pydantic para respuestas de la API.
Define estructuras estándar para respuestas de error y éxito.
"""
from pydantic import BaseModel, Field
from typing import Optional, Any


class ErrorResponse(BaseModel):
    """
    Modelo estándar para respuestas de error.
    
    Attributes:
        error: Tipo de error
        message: Mensaje descriptivo del error
        details: Detalles adicionales del error (opcional)
    """
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: Optional[Any] = Field(None, description="Detalles adicionales del error")
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Los datos proporcionados no son válidos",
                "details": {
                    "field": "customer_stratum",
                    "issue": "El estrato debe estar entre 1 y 6"
                }
            }
        }


class SuccessResponse(BaseModel):
    """
    Modelo estándar para respuestas exitosas.
    
    Attributes:
        success: Indica si la operación fue exitosa
        message: Mensaje descriptivo
        data: Datos de la respuesta
    """
    success: bool = Field(True, description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[Any] = Field(None, description="Datos de la respuesta")
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "success": True,
                "message": "Pedido calculado exitosamente",
                "data": {
                    "subtotal": 2590000.00,
                    "shipping_cost": 6000.00,
                    "discount_applied": 259000.00,
                    "total_cost": 2337000.00
                }
            }
        }


class HealthResponse(BaseModel):
    """
    Modelo para respuesta de health check.
    
    Attributes:
        status: Estado del servicio
        version: Versión de la API
        timestamp: Timestamp de la respuesta
    """
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión de la API")
    timestamp: str = Field(..., description="Timestamp de la respuesta")
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

