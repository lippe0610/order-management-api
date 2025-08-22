"""
Modelos Pydantic para productos.
Define la estructura y validaciones para los productos en los pedidos.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class Product(BaseModel):
    """
    Modelo para un producto individual en un pedido.
    
    Attributes:
        name: Nombre del producto (opcional para el cálculo)
        price: Precio unitario del producto en pesos colombianos
        quantity: Cantidad de unidades del producto
    """
    name: Optional[str] = Field(None, description="Nombre del producto")
    price: float = Field(..., gt=0, description="Precio unitario en COP")
    quantity: int = Field(..., gt=0, description="Cantidad de unidades")
    
    @validator('price')
    def validate_price(cls, v):
        """Valida que el precio sea un número positivo."""
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2)  # Redondear a 2 decimales
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Valida que la cantidad sea un entero positivo."""
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v
    
    class Config:
        """Configuración del modelo."""
        schema_extra = {
            "example": {
                "name": "Laptop Dell Inspiron",
                "price": 2500000.00,
                "quantity": 1
            }
        }

