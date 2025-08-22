"""
Configuración compartida para las pruebas con pytest.
Define fixtures y configuraciones comunes para todas las pruebas.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.order import OrderRequest
from app.models.product import Product


@pytest.fixture
def client():
    """
    Fixture que proporciona un cliente de prueba para FastAPI.
    
    Returns:
        TestClient: Cliente para realizar requests a la API
    """
    return TestClient(app)


@pytest.fixture
def sample_product():
    """
    Fixture que proporciona un producto de ejemplo para las pruebas.
    
    Returns:
        Product: Producto de ejemplo
    """
    return Product(
        name="Laptop Dell Inspiron",
        price=2500000.00,
        quantity=1
    )


@pytest.fixture
def sample_products():
    """
    Fixture que proporciona una lista de productos de ejemplo.
    
    Returns:
        List[Product]: Lista de productos de ejemplo
    """
    return [
        Product(name="Laptop Dell Inspiron", price=2500000.00, quantity=1),
        Product(name="Mouse inalámbrico", price=45000.00, quantity=2),
        Product(name="Teclado mecánico", price=150000.00, quantity=1)
    ]


@pytest.fixture
def sample_order_request(sample_products):
    """
    Fixture que proporciona un pedido de ejemplo para las pruebas.
    
    Args:
        sample_products: Lista de productos de ejemplo
        
    Returns:
        OrderRequest: Pedido de ejemplo
    """
    return OrderRequest(
        products=sample_products,
        customer_stratum=3,
        customer_address="Calle 123 #45-67, Bogotá"
    )


@pytest.fixture
def simple_order_request():
    """
    Fixture que proporciona un pedido simple sin descuento.
    
    Returns:
        OrderRequest: Pedido simple
    """
    return OrderRequest(
        products=[
            Product(name="Producto simple", price=50000.00, quantity=1)
        ],
        customer_stratum=4
    )


@pytest.fixture
def high_value_order_request():
    """
    Fixture que proporciona un pedido de alto valor que califica para descuento.
    
    Returns:
        OrderRequest: Pedido de alto valor
    """
    return OrderRequest(
        products=[
            Product(name="Producto caro", price=150000.00, quantity=1)
        ],
        customer_stratum=2
    )


@pytest.fixture
def premium_customer_order():
    """
    Fixture que proporciona un pedido de cliente premium (estrato alto).
    
    Returns:
        OrderRequest: Pedido de cliente premium
    """
    return OrderRequest(
        products=[
            Product(name="Producto premium", price=200000.00, quantity=1)
        ],
        customer_stratum=6
    )

