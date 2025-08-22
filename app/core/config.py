"""
Configuración de la aplicación.
Centraliza todas las constantes y configuraciones del sistema.
"""
from typing import Dict

class Settings:
    """Configuración principal de la aplicación."""
    
    # Información de la aplicación
    APP_NAME: str = "Order Management API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API RESTful para gestión de pedidos con cálculo de costos y descuentos"
    
    # Configuración de CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Configuración de costos de envío por estrato socioeconómico
    # En Colombia, los estratos van del 1 al 6
    SHIPPING_COSTS_BY_STRATUM: Dict[int, int] = {
        1: 8000,  # Estrato bajo - mayor costo de envío
        2: 8000,  # Estrato bajo - mayor costo de envío
        3: 6000,  # Estrato medio-bajo
        4: 5000,  # Estrato medio
        5: 0,     # Estrato alto - envío gratis
        6: 0      # Estrato alto - envío gratis
    }
    
    # Configuración de descuentos
    DISCOUNT_THRESHOLD: int = 100000  # Monto mínimo para aplicar descuento (COP)
    DISCOUNT_RATE: float = 0.10       # 10% de descuento
    
    # Costo de envío por defecto para estratos no definidos
    DEFAULT_SHIPPING_COST: int = 6000

settings = Settings()

