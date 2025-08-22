"""
Pruebas unitarias para el servicio de cálculo de pedidos.
Verifica toda la lógica de negocio relacionada con cálculos de costos.
"""
import pytest
from pydantic import ValidationError
from app.services.order_service import OrderService
from app.models.order import OrderRequest
from app.models.product import Product
from app.core.config import settings


class TestOrderService:
    """Pruebas para la clase OrderService."""
    
    @pytest.mark.unit
    def test_calculate_subtotal_single_product(self, simple_order_request):
        """Prueba el cálculo de subtotal con un solo producto."""
        subtotal = OrderService.calculate_subtotal(simple_order_request)
        expected = 50000.00  # 50000 * 1
        assert subtotal == expected
    
    @pytest.mark.unit
    def test_calculate_subtotal_multiple_products(self, sample_order_request):
        """Prueba el cálculo de subtotal con múltiples productos."""
        subtotal = OrderService.calculate_subtotal(sample_order_request)
        # 2500000*1 + 45000*2 + 150000*1 = 2740000
        expected = 2740000.00
        assert subtotal == expected
    
    @pytest.mark.unit
    def test_calculate_subtotal_with_decimals(self):
        """Prueba el cálculo de subtotal con precios decimales."""
        order = OrderRequest(
            products=[
                Product(name="Test", price=99.99, quantity=3)
            ],
            customer_stratum=3
        )
        subtotal = OrderService.calculate_subtotal(order)
        expected = 299.97  # 99.99 * 3
        assert subtotal == expected
    
    @pytest.mark.unit
    @pytest.mark.parametrize("stratum,expected_cost", [
        (1, 8000),
        (2, 8000),
        (3, 6000),
        (4, 5000),
        (5, 0),
        (6, 0)
    ])
    def test_calculate_shipping_cost_by_stratum(self, stratum, expected_cost):
        """Prueba el cálculo de costo de envío por estrato."""
        shipping_cost = OrderService.calculate_shipping_cost(stratum)
        assert shipping_cost == expected_cost
    
    @pytest.mark.unit
    def test_calculate_shipping_cost_invalid_stratum(self):
        """Prueba el costo de envío para estrato inválido."""
        shipping_cost = OrderService.calculate_shipping_cost(99)
        assert shipping_cost == settings.DEFAULT_SHIPPING_COST
    
    @pytest.mark.unit
    def test_calculate_discount_no_discount(self):
        """Prueba que no se aplique descuento para montos bajos."""
        subtotal = 50000.00  # Menor al umbral
        discount_info = OrderService.calculate_discount(subtotal)
        
        assert discount_info['amount'] == 0.0
        assert discount_info['percentage'] == 0.0
    
    @pytest.mark.unit
    def test_calculate_discount_with_discount(self):
        """Prueba que se aplique descuento para montos altos."""
        subtotal = 150000.00  # Mayor al umbral
        discount_info = OrderService.calculate_discount(subtotal)
        
        expected_amount = 15000.00  # 150000 * 0.10
        assert discount_info['amount'] == expected_amount
        assert discount_info['percentage'] == 10.0
    
    @pytest.mark.unit
    def test_calculate_discount_exact_threshold(self):
        """Prueba el descuento en el umbral exacto."""
        subtotal = float(settings.DISCOUNT_THRESHOLD)
        discount_info = OrderService.calculate_discount(subtotal)
        
        # En el umbral exacto no debe aplicar descuento
        assert discount_info['amount'] == 0.0
        assert discount_info['percentage'] == 0.0
    
    @pytest.mark.unit
    def test_calculate_discount_just_above_threshold(self):
        """Prueba el descuento justo por encima del umbral."""
        subtotal = float(settings.DISCOUNT_THRESHOLD + 1)
        discount_info = OrderService.calculate_discount(subtotal)
        
        expected_amount = subtotal * settings.DISCOUNT_RATE
        assert discount_info['amount'] == expected_amount
        assert discount_info['percentage'] == settings.DISCOUNT_RATE * 100
    
    @pytest.mark.unit
    def test_calculate_order_total_simple(self, simple_order_request):
        """Prueba el cálculo completo de un pedido simple."""
        result = OrderService.calculate_order_total(simple_order_request)
        
        # Verificar todos los campos
        assert result.subtotal == 50000.00
        assert result.shipping_cost == 5000.00  # Estrato 4
        assert result.discount_applied == 0.0    # No califica para descuento
        assert result.total_cost == 55000.00     # 50000 + 5000 - 0
        assert result.customer_stratum == 4
        assert result.discount_percentage == 0.0
    
    @pytest.mark.unit
    def test_calculate_order_total_with_discount(self, high_value_order_request):
        """Prueba el cálculo completo de un pedido con descuento."""
        result = OrderService.calculate_order_total(high_value_order_request)
        
        # Verificar cálculos
        assert result.subtotal == 150000.00
        assert result.shipping_cost == 8000.00   # Estrato 2
        assert result.discount_applied == 15000.00  # 10% de 150000
        assert result.total_cost == 143000.00    # 150000 - 15000 + 8000
        assert result.customer_stratum == 2
        assert result.discount_percentage == 10.0
    
    @pytest.mark.unit
    def test_calculate_order_total_premium_customer(self, premium_customer_order):
        """Prueba el cálculo para cliente premium (envío gratis)."""
        result = OrderService.calculate_order_total(premium_customer_order)
        
        # Verificar envío gratis para estrato 6
        assert result.subtotal == 200000.00
        assert result.shipping_cost == 0.0       # Estrato 6 - envío gratis
        assert result.discount_applied == 20000.00  # 10% de 200000
        assert result.total_cost == 180000.00    # 200000 - 20000 + 0
        assert result.customer_stratum == 6
        assert result.discount_percentage == 10.0
    
    @pytest.mark.unit
    def test_validate_order_business_rules_valid(self, sample_order_request):
        """Prueba la validación de reglas de negocio para pedido válido."""
        validation = OrderService.validate_order_business_rules(sample_order_request)
        
        assert validation['valid'] is True
        assert len(validation['errors']) == 0
    
    @pytest.mark.unit
    def test_validate_order_business_rules_invalid_price(self):
        """Prueba la validación con precio inválido."""
        # Esta validación la maneja Pydantic, así que probamos que falle en la creación
        with pytest.raises(ValidationError):
            Product(name="Test", price=-100, quantity=1)
    
    @pytest.mark.unit
    def test_validate_order_business_rules_invalid_stratum(self):
        """Prueba la validación con estrato inválido."""
        # Esta validación la maneja Pydantic, así que probamos que falle en la creación
        with pytest.raises(ValidationError):
            OrderRequest(
                products=[
                    Product(name="Test", price=100, quantity=1)
                ],
                customer_stratum=10  # Estrato inválido
            )
    
    @pytest.mark.unit
    def test_rounding_precision(self):
        """Prueba que los cálculos mantengan la precisión correcta."""
        order = OrderRequest(
            products=[
                Product(name="Test", price=33.33, quantity=3)
            ],
            customer_stratum=3
        )
        
        result = OrderService.calculate_order_total(order)
        
        # Verificar que los valores estén redondeados correctamente
        assert isinstance(result.subtotal, float)
        assert isinstance(result.total_cost, float)
        assert result.subtotal == 99.99  # 33.33 * 3
        
    @pytest.mark.unit
    def test_large_order_calculation(self):
        """Prueba el cálculo con un pedido grande."""
        products = [
            Product(name=f"Producto {i}", price=10000.00, quantity=5)
            for i in range(20)  # 20 productos
        ]
        
        order = OrderRequest(
            products=products,
            customer_stratum=1
        )
        
        result = OrderService.calculate_order_total(order)
        
        expected_subtotal = 1000000.00  # 20 * 10000 * 5
        expected_discount = 100000.00   # 10% de 1000000
        expected_shipping = 8000.00     # Estrato 1
        expected_total = 908000.00      # 1000000 - 100000 + 8000
        
        assert result.subtotal == expected_subtotal
        assert result.discount_applied == expected_discount
        assert result.shipping_cost == expected_shipping
        assert result.total_cost == expected_total

