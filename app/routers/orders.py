"""
Router para endpoints relacionados con pedidos.
Maneja las rutas de cálculo de pedidos y operaciones relacionadas.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any

from app.models.order import OrderRequest, OrderResponse
from app.models.responses import ErrorResponse
from app.services.order_service import OrderService

# Crear router con prefijo y tags para documentación
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={
        404: {"description": "No encontrado"},
        422: {"description": "Error de validación"},
        500: {"description": "Error interno del servidor"}
    }
)


@router.post(
    "/calculate",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcular costo total de pedido",
    description="""
    Calcula el costo total de un pedido incluyendo:
    - Subtotal de productos (precio × cantidad)
    - Costo de envío basado en estrato socioeconómico
    - Descuentos aplicables según el monto total
    
    **Estratos y costos de envío:**
    - Estrato 1-2: $8,000 COP
    - Estrato 3: $6,000 COP  
    - Estrato 4: $5,000 COP
    - Estrato 5-6: Envío gratis
    
    **Descuentos:**
    - 10% de descuento para pedidos superiores a $100,000 COP
    """
)
async def calculate_order(order: OrderRequest) -> OrderResponse:
    """
    Endpoint principal para calcular el costo total de un pedido.
    
    Args:
        order: Datos del pedido con productos y estrato del cliente
        
    Returns:
        OrderResponse: Cálculo detallado del pedido
        
    Raises:
        HTTPException: Si hay errores en la validación o cálculo
    """
    try:
        # Validar reglas de negocio adicionales
        validation_result = OrderService.validate_order_business_rules(order)
        
        if not validation_result['valid']:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "ValidationError",
                    "message": "Los datos del pedido no cumplen las reglas de negocio",
                    "details": validation_result['errors']
                }
            )
        
        # Calcular el pedido
        result = OrderService.calculate_order_total(order)
        
        return result
        
    except HTTPException:
        # Re-lanzar HTTPExceptions
        raise
    except Exception as e:
        # Manejar errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Error interno al procesar el pedido",
                "details": str(e)
            }
        )


@router.get(
    "/shipping-costs",
    response_model=Dict[str, Any],
    summary="Obtener costos de envío por estrato",
    description="Retorna la tabla de costos de envío según el estrato socioeconómico"
)
async def get_shipping_costs() -> Dict[str, Any]:
    """
    Endpoint para consultar los costos de envío por estrato.
    
    Returns:
        Dict con los costos de envío por estrato
    """
    from app.core.config import settings
    
    return {
        "shipping_costs": settings.SHIPPING_COSTS_BY_STRATUM,
        "default_cost": settings.DEFAULT_SHIPPING_COST,
        "currency": "COP"
    }


@router.get(
    "/discount-info",
    response_model=Dict[str, Any],
    summary="Obtener información de descuentos",
    description="Retorna la configuración actual de descuentos"
)
async def get_discount_info() -> Dict[str, Any]:
    """
    Endpoint para consultar la configuración de descuentos.
    
    Returns:
        Dict con la información de descuentos
    """
    from app.core.config import settings
    
    return {
        "discount_threshold": settings.DISCOUNT_THRESHOLD,
        "discount_rate": settings.DISCOUNT_RATE,
        "discount_percentage": settings.DISCOUNT_RATE * 100,
        "currency": "COP"
    }

