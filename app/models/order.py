"""
Modelos Pydantic para pedidos.
Define la estructura para requests y responses de pedidos.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from .product import Product


class OrderRequest(BaseModel):
    """
    Modelo para el request de cálculo de pedido.
    
    Attributes:
        products: Lista de productos en el pedido
        customer_stratum: Estrato socioeconómico del cliente (1-6)
        customer_address: Dirección del cliente (opcional)
    """
    products: List[Product] = Field(..., min_items=1, description="Lista de productos")
    customer_stratum: int = Field(..., ge=1, le=6, description="Estrato socioeconómico (1-6)")
    customer_address: Optional[str] = Field(None, description="Dirección de entrega")
    
    @validator('products')
    def validate_products_not_empty(cls, v):
        """Valida que la lista de productos no esté vacía."""
        if not v:
            raise ValueError('Debe incluir al menos un producto')
        return v
    
    @validator('customer_stratum')
    def validate_stratum(cls, v):
        """Valida que el estrato esté en el rango válido para Colombia."""
        if v < 1 or v > 6:
            raise ValueError('El estrato debe estar entre 1 y 6')
        return v
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "products": [
                    {
                        "name": "Laptop Dell Inspiron",
                        "price": 2500000.00,
                        "quantity": 1
                    },
                    {
                        "name": "Mouse inalámbrico",
                        "price": 45000.00,
                        "quantity": 2
                    }
                ],
                "customer_stratum": 3,
                "customer_address": "Calle 123 #45-67, Bogotá"
            }
        }


class OrderResponse(BaseModel):
    """
    Modelo para la respuesta del cálculo de pedido.
    
    Attributes:
        subtotal: Suma de todos los productos (precio * cantidad)
        shipping_cost: Costo de envío basado en el estrato
        discount_applied: Monto del descuento aplicado
        total_cost: Costo total final del pedido
        customer_stratum: Estrato del cliente
        discount_percentage: Porcentaje de descuento aplicado
    """
    subtotal: float = Field(..., description="Subtotal de productos en COP")
    shipping_cost: float = Field(..., description="Costo de envío en COP")
    discount_applied: float = Field(..., description="Descuento aplicado en COP")
    total_cost: float = Field(..., description="Costo total final en COP")
    customer_stratum: int = Field(..., description="Estrato del cliente")
    discount_percentage: float = Field(..., description="Porcentaje de descuento aplicado")
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "subtotal": 2590000.00,
                "shipping_cost": 6000.00,
                "discount_applied": 259000.00,
                "total_cost": 2337000.00,
                "customer_stratum": 3,
                "discount_percentage": 10.0
            }
        }

