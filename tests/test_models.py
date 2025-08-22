"""
Pruebas unitarias para los modelos Pydantic.
Verifica las validaciones y comportamiento de los modelos de datos.
"""
import pytest
from pydantic import ValidationError
from app.models.product import Product
from app.models.order import OrderRequest, OrderResponse


class TestProductModel:
    """Pruebas para el modelo Product."""
    
    @pytest.mark.unit
    def test_product_creation_valid(self):
        """Prueba la creación de un producto válido."""
        product = Product(
            name="Laptop Dell",
            price=2500000.00,
            quantity=1
        )
        
        assert product.name == "Laptop Dell"
        assert product.price == 2500000.00
        assert product.quantity == 1
    
    @pytest.mark.unit
    def test_product_creation_without_name(self):
        """Prueba la creación de producto sin nombre (opcional)."""
        product = Product(
            price=100000.00,
            quantity=2
        )
        
        assert product.name is None
        assert product.price == 100000.00
        assert product.quantity == 2
    
    @pytest.mark.unit
    def test_product_price_validation_negative(self):
        """Prueba validación de precio negativo."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=-100.00,
                quantity=1
            )
        
        errors = exc_info.value.errors()
        assert any("price" in str(error) for error in errors)
    
    @pytest.mark.unit
    def test_product_price_validation_zero(self):
        """Prueba validación de precio cero."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=0.00,
                quantity=1
            )
        
        errors = exc_info.value.errors()
        assert any("price" in str(error) for error in errors)
    
    @pytest.mark.unit
    def test_product_quantity_validation_negative(self):
        """Prueba validación de cantidad negativa."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=100.00,
                quantity=-1
            )
        
        errors = exc_info.value.errors()
        assert any("quantity" in str(error) for error in errors)
    
    @pytest.mark.unit
    def test_product_quantity_validation_zero(self):
        """Prueba validación de cantidad cero."""
        with pytest.raises(ValidationError) as exc_info:
            Product(
                name="Test",
                price=100.00,
                quantity=0
            )
        
        errors = exc_info.value.errors()
        assert any("quantity" in str(error) for error in errors)
    
    @pytest.mark.unit
    def test_product_price_rounding(self):
        """Prueba el redondeo de precios a 2 decimales."""
        product = Product(
            name="Test",
            price=99.999,  # Debería redondearse a 100.00
            quantity=1
        )
        
        assert product.price == 100.00


class TestOrderRequestModel:
    """Pruebas para el modelo OrderRequest."""
    
    @pytest.mark.unit
    def test_order_request_creation_valid(self, sample_products):
        """Prueba la creación de un pedido válido."""
        order = OrderRequest(
            products=sample_products,
            customer_stratum=3,
            customer_address="Calle 123 #45-67"
        )
        
        assert len(order.products) == 3
        assert order.customer_stratum == 3
        assert order.customer_address == "Calle 123 #45-67"
    
    @pytest.mark.unit
    def test_order_request_without_address(self, sample_products):
        """Prueba la creación de pedido sin dirección (opcional)."""
        order = OrderRequest(
            products=sample_products,
            customer_stratum=4
        )
        
        assert len(order.products) == 3
        assert order.customer_stratum == 4
        assert order.customer_address is None
    
    @pytest.mark.unit
    def test_order_request_empty_products(self):
        """Prueba validación de lista de productos vacía."""
        with pytest.raises(ValidationError) as exc_info:
            OrderRequest(
                products=[],
                customer_stratum=3
            )
        
        errors = exc_info.value.errors()
        assert any("products" in str(error) for error in errors)
    
    @pytest.mark.unit
    @pytest.mark.parametrize("invalid_stratum", [0, -1, 7, 10, 100])
    def test_order_request_invalid_stratum(self, sample_products, invalid_stratum):
        """Prueba validación de estrato inválido."""
        with pytest.raises(ValidationError) as exc_info:
            OrderRequest(
                products=sample_products,
                customer_stratum=invalid_stratum
            )
        
        errors = exc_info.value.errors()
        assert any("customer_stratum" in str(error) for error in errors)
    
    @pytest.mark.unit
    @pytest.mark.parametrize("valid_stratum", [1, 2, 3, 4, 5, 6])
    def test_order_request_valid_stratum(self, sample_products, valid_stratum):
        """Prueba validación de estratos válidos."""
        order = OrderRequest(
            products=sample_products,
            customer_stratum=valid_stratum
        )
        
        assert order.customer_stratum == valid_stratum
    
    @pytest.mark.unit
    def test_order_request_missing_required_fields(self):
        """Prueba validación de campos requeridos faltantes."""
        with pytest.raises(ValidationError):
            OrderRequest()  # Sin productos ni estrato
    
    @pytest.mark.unit
    def test_order_request_with_invalid_product(self):
        """Prueba validación con producto inválido en la lista."""
        with pytest.raises(ValidationError):
            OrderRequest(
                products=[
                    Product(name="Valid", price=100.00, quantity=1),
                    # Producto inválido con precio negativo
                    {"name": "Invalid", "price": -50.00, "quantity": 1}
                ],
                customer_stratum=3
            )


class TestOrderResponseModel:
    """Pruebas para el modelo OrderResponse."""
    
    @pytest.mark.unit
    def test_order_response_creation(self):
        """Prueba la creación de una respuesta de pedido."""
        response = OrderResponse(
            subtotal=100000.00,
            shipping_cost=5000.00,
            discount_applied=10000.00,
            total_cost=95000.00,
            customer_stratum=4,
            discount_percentage=10.0
        )
        
        assert response.subtotal == 100000.00
        assert response.shipping_cost == 5000.00
        assert response.discount_applied == 10000.00
        assert response.total_cost == 95000.00
        assert response.customer_stratum == 4
        assert response.discount_percentage == 10.0
    
    @pytest.mark.unit
    def test_order_response_missing_fields(self):
        """Prueba validación de campos requeridos en respuesta."""
        with pytest.raises(ValidationError):
            OrderResponse(
                subtotal=100000.00,
                # Faltan campos requeridos
            )
    
    @pytest.mark.unit
    def test_order_response_serialization(self):
        """Prueba la serialización de la respuesta a dict."""
        response = OrderResponse(
            subtotal=100000.00,
            shipping_cost=5000.00,
            discount_applied=10000.00,
            total_cost=95000.00,
            customer_stratum=4,
            discount_percentage=10.0
        )
        
        data = response.dict()
        
        assert isinstance(data, dict)
        assert "subtotal" in data
        assert "shipping_cost" in data
        assert "discount_applied" in data
        assert "total_cost" in data
        assert "customer_stratum" in data
        assert "discount_percentage" in data
    
    @pytest.mark.unit
    def test_order_response_json_serialization(self):
        """Prueba la serialización de la respuesta a JSON."""
        response = OrderResponse(
            subtotal=100000.00,
            shipping_cost=5000.00,
            discount_applied=10000.00,
            total_cost=95000.00,
            customer_stratum=4,
            discount_percentage=10.0
        )
        
        json_str = response.json()
        
        assert isinstance(json_str, str)
        assert "subtotal" in json_str
        assert "100000.0" in json_str


class TestModelIntegration:
    """Pruebas de integración entre modelos."""
    
    @pytest.mark.unit
    def test_product_in_order_request(self):
        """Prueba la integración de productos en pedidos."""
        products = [
            Product(name="Laptop", price=2000000.00, quantity=1),
            Product(name="Mouse", price=50000.00, quantity=2)
        ]
        
        order = OrderRequest(
            products=products,
            customer_stratum=3
        )
        
        assert len(order.products) == 2
        assert order.products[0].name == "Laptop"
        assert order.products[1].quantity == 2
    
    @pytest.mark.unit
    def test_model_validation_chain(self):
        """Prueba la cadena de validación desde request hasta response."""
        # Crear productos válidos
        products = [
            Product(name="Test Product", price=150000.00, quantity=1)
        ]
        
        # Crear pedido válido
        order_request = OrderRequest(
            products=products,
            customer_stratum=2
        )
        
        # Simular respuesta válida
        order_response = OrderResponse(
            subtotal=150000.00,
            shipping_cost=8000.00,
            discount_applied=15000.00,
            total_cost=143000.00,
            customer_stratum=2,
            discount_percentage=10.0
        )
        
        # Verificar que todos los modelos son válidos
        assert order_request.customer_stratum == order_response.customer_stratum
        assert len(order_request.products) == 1
        assert order_response.total_cost > 0

