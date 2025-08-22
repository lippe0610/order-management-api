"""
Servicio de lógica de negocio para el cálculo de pedidos.
Contiene toda la lógica para calcular costos, envíos y descuentos.
"""
from typing import Dict, Any
from app.models.order import OrderRequest, OrderResponse
from app.core.config import settings


class OrderService:
    """
    Servicio para el cálculo de pedidos.
    
    Centraliza toda la lógica de negocio relacionada con el cálculo
    de costos, envíos y descuentos de pedidos.
    """
    
    @staticmethod
    def calculate_subtotal(order: OrderRequest) -> float:
        """
        Calcula el subtotal del pedido (suma de precio * cantidad de todos los productos).
        
        Args:
            order: Request del pedido con la lista de productos
            
        Returns:
            float: Subtotal del pedido en pesos colombianos
        """
        subtotal = sum(product.price * product.quantity for product in order.products)
        return round(subtotal, 2)
    
    @staticmethod
    def calculate_shipping_cost(customer_stratum: int) -> float:
        """
        Calcula el costo de envío basado en el estrato socioeconómico del cliente.
        
        En Colombia, los estratos más altos (5 y 6) tienen envío gratuito,
        mientras que los estratos más bajos tienen costos de envío más altos.
        
        Args:
            customer_stratum: Estrato socioeconómico del cliente (1-6)
            
        Returns:
            float: Costo de envío en pesos colombianos
        """
        shipping_cost = settings.SHIPPING_COSTS_BY_STRATUM.get(
            customer_stratum, 
            settings.DEFAULT_SHIPPING_COST
        )
        return float(shipping_cost)
    
    @staticmethod
    def calculate_discount(subtotal: float) -> Dict[str, float]:
        """
        Calcula el descuento aplicable basado en el subtotal del pedido.
        
        Se aplica un descuento del 10% si el subtotal supera el umbral definido.
        El descuento se aplica solo sobre el subtotal, no sobre el costo de envío.
        
        Args:
            subtotal: Subtotal del pedido
            
        Returns:
            Dict con 'amount' (monto del descuento) y 'percentage' (porcentaje aplicado)
        """
        if subtotal > settings.DISCOUNT_THRESHOLD:
            discount_amount = subtotal * settings.DISCOUNT_RATE
            return {
                'amount': round(discount_amount, 2),
                'percentage': settings.DISCOUNT_RATE * 100
            }
        return {
            'amount': 0.0,
            'percentage': 0.0
        }
    
    @classmethod
    def calculate_order_total(cls, order: OrderRequest) -> OrderResponse:
        """
        Calcula el costo total de un pedido incluyendo todos los componentes.
        
        Este es el método principal que orquesta todos los cálculos:
        1. Calcula el subtotal de productos
        2. Determina el costo de envío según el estrato
        3. Aplica descuentos si corresponde
        4. Calcula el total final
        
        Args:
            order: Request del pedido con productos y datos del cliente
            
        Returns:
            OrderResponse: Respuesta con todos los cálculos detallados
        """
        # Calcular subtotal
        subtotal = cls.calculate_subtotal(order)
        
        # Calcular costo de envío
        shipping_cost = cls.calculate_shipping_cost(order.customer_stratum)
        
        # Calcular descuento
        discount_info = cls.calculate_discount(subtotal)
        discount_applied = discount_info['amount']
        discount_percentage = discount_info['percentage']
        
        # Calcular total final
        # Nota: El descuento se aplica sobre el subtotal, luego se suma el envío
        total_cost = (subtotal - discount_applied) + shipping_cost
        total_cost = round(total_cost, 2)
        
        return OrderResponse(
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount_applied=discount_applied,
            total_cost=total_cost,
            customer_stratum=order.customer_stratum,
            discount_percentage=discount_percentage
        )
    
    @staticmethod
    def validate_order_business_rules(order: OrderRequest) -> Dict[str, Any]:
        """
        Valida reglas de negocio adicionales para el pedido.
        
        Args:
            order: Request del pedido a validar
            
        Returns:
            Dict con 'valid' (bool) y 'errors' (list) si hay errores
        """
        errors = []
        
        # Validar que todos los productos tengan precios válidos
        for i, product in enumerate(order.products):
            if product.price <= 0:
                errors.append(f"Producto {i+1}: El precio debe ser mayor a 0")
            
            if product.quantity <= 0:
                errors.append(f"Producto {i+1}: La cantidad debe ser mayor a 0")
        
        # Validar estrato
        if order.customer_stratum < 1 or order.customer_stratum > 6:
            errors.append("El estrato debe estar entre 1 y 6")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

