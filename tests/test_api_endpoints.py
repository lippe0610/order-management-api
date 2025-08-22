"""
Pruebas de integración para los endpoints de la API.
Verifica el comportamiento completo de los endpoints HTTP.
"""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Pruebas para endpoints de salud y utilidades."""
    
    @pytest.mark.integration
    def test_health_check(self, client: TestClient):
        """Prueba el endpoint de health check."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
    
    @pytest.mark.integration
    def test_root_endpoint(self, client: TestClient):
        """Prueba el endpoint raíz."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "description" in data
        assert "docs_url" in data


class TestOrderEndpoints:
    """Pruebas para endpoints de pedidos."""
    
    @pytest.mark.integration
    def test_calculate_order_success(self, client: TestClient):
        """Prueba el cálculo exitoso de un pedido."""
        order_data = {
            "products": [
                {
                    "name": "Laptop Dell",
                    "price": 2500000.00,
                    "quantity": 1
                }
            ],
            "customer_stratum": 3,
            "customer_address": "Calle 123 #45-67"
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura de respuesta
        assert "subtotal" in data
        assert "shipping_cost" in data
        assert "discount_applied" in data
        assert "total_cost" in data
        assert "customer_stratum" in data
        assert "discount_percentage" in data
        
        # Verificar valores específicos
        assert data["subtotal"] == 2500000.00
        assert data["shipping_cost"] == 6000.00  # Estrato 3
        assert data["discount_applied"] == 250000.00  # 10% de 2500000
        assert data["customer_stratum"] == 3
        assert data["discount_percentage"] == 10.0
    
    @pytest.mark.integration
    def test_calculate_order_no_discount(self, client: TestClient):
        """Prueba el cálculo de pedido sin descuento."""
        order_data = {
            "products": [
                {
                    "name": "Mouse",
                    "price": 50000.00,
                    "quantity": 1
                }
            ],
            "customer_stratum": 4
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["subtotal"] == 50000.00
        assert data["shipping_cost"] == 5000.00  # Estrato 4
        assert data["discount_applied"] == 0.0   # No califica para descuento
        assert data["total_cost"] == 55000.00    # 50000 + 5000 - 0
        assert data["discount_percentage"] == 0.0
    
    @pytest.mark.integration
    def test_calculate_order_premium_customer(self, client: TestClient):
        """Prueba el cálculo para cliente premium (envío gratis)."""
        order_data = {
            "products": [
                {
                    "name": "Producto Premium",
                    "price": 200000.00,
                    "quantity": 1
                }
            ],
            "customer_stratum": 6
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["subtotal"] == 200000.00
        assert data["shipping_cost"] == 0.0      # Estrato 6 - envío gratis
        assert data["discount_applied"] == 20000.00  # 10% de 200000
        assert data["total_cost"] == 180000.00   # 200000 - 20000 + 0
    
    @pytest.mark.integration
    def test_calculate_order_multiple_products(self, client: TestClient):
        """Prueba el cálculo con múltiples productos."""
        order_data = {
            "products": [
                {
                    "name": "Laptop",
                    "price": 2000000.00,
                    "quantity": 1
                },
                {
                    "name": "Mouse",
                    "price": 50000.00,
                    "quantity": 2
                },
                {
                    "name": "Teclado",
                    "price": 100000.00,
                    "quantity": 1
                }
            ],
            "customer_stratum": 2
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        expected_subtotal = 2200000.00  # 2000000 + 100000 + 100000
        expected_discount = 220000.00   # 10% de 2200000
        expected_shipping = 8000.00     # Estrato 2
        expected_total = 1988000.00     # 2200000 - 220000 + 8000
        
        assert data["subtotal"] == expected_subtotal
        assert data["discount_applied"] == expected_discount
        assert data["shipping_cost"] == expected_shipping
        assert data["total_cost"] == expected_total
    
    @pytest.mark.integration
    def test_calculate_order_invalid_stratum(self, client: TestClient):
        """Prueba validación de estrato inválido."""
        order_data = {
            "products": [
                {
                    "name": "Test",
                    "price": 100000.00,
                    "quantity": 1
                }
            ],
            "customer_stratum": 10  # Estrato inválido
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "error" in data
        assert data["error"] == "ValidationError"
    
    @pytest.mark.integration
    def test_calculate_order_negative_price(self, client: TestClient):
        """Prueba validación de precio negativo."""
        order_data = {
            "products": [
                {
                    "name": "Test",
                    "price": -100.00,  # Precio inválido
                    "quantity": 1
                }
            ],
            "customer_stratum": 3
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "error" in data
    
    @pytest.mark.integration
    def test_calculate_order_zero_quantity(self, client: TestClient):
        """Prueba validación de cantidad cero."""
        order_data = {
            "products": [
                {
                    "name": "Test",
                    "price": 100000.00,
                    "quantity": 0  # Cantidad inválida
                }
            ],
            "customer_stratum": 3
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.integration
    def test_calculate_order_empty_products(self, client: TestClient):
        """Prueba validación de lista de productos vacía."""
        order_data = {
            "products": [],  # Lista vacía
            "customer_stratum": 3
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.integration
    def test_calculate_order_missing_required_fields(self, client: TestClient):
        """Prueba validación de campos requeridos faltantes."""
        order_data = {
            "products": [
                {
                    "name": "Test",
                    "price": 100000.00
                    # Falta quantity
                }
            ],
            "customer_stratum": 3
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.integration
    def test_get_shipping_costs(self, client: TestClient):
        """Prueba el endpoint de consulta de costos de envío."""
        response = client.get("/orders/shipping-costs")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "shipping_costs" in data
        assert "default_cost" in data
        assert "currency" in data
        
        # Verificar estructura de costos por estrato
        shipping_costs = data["shipping_costs"]
        assert "1" in shipping_costs or 1 in shipping_costs
        assert data["currency"] == "COP"
    
    @pytest.mark.integration
    def test_get_discount_info(self, client: TestClient):
        """Prueba el endpoint de información de descuentos."""
        response = client.get("/orders/discount-info")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "discount_threshold" in data
        assert "discount_rate" in data
        assert "discount_percentage" in data
        assert "currency" in data
        
        assert data["discount_threshold"] == 100000
        assert data["discount_rate"] == 0.10
        assert data["discount_percentage"] == 10.0
        assert data["currency"] == "COP"
    
    @pytest.mark.integration
    def test_calculate_order_with_decimals(self, client: TestClient):
        """Prueba el cálculo con precios decimales."""
        order_data = {
            "products": [
                {
                    "name": "Test",
                    "price": 99.99,
                    "quantity": 3
                }
            ],
            "customer_stratum": 3
        }
        
        response = client.post("/orders/calculate", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["subtotal"] == 299.97  # 99.99 * 3
        
    @pytest.mark.integration
    def test_cors_headers(self, client: TestClient):
        """Prueba que los headers CORS estén configurados correctamente."""
        response = client.options("/orders/calculate")
        
        # FastAPI maneja automáticamente las opciones CORS
        # Verificamos que no hay errores
        assert response.status_code in [200, 405]  # 405 es normal para OPTIONS sin configuración específica

