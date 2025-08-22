# Order Management API

Una API RESTful robusta y escalable para la gestión de pedidos con cálculo automático de costos, envío y descuentos, diseñada específicamente para el sistema de estratos socioeconómicos de Colombia.

## 🚀 Características Principales

- **Cálculo Automático de Costos**: Procesamiento inteligente de precios y cantidades de productos
- **Sistema de Estratos Socioeconómicos**: Integración completa con el sistema colombiano de estratificación (1-6)
- **Gestión de Envíos Diferenciados**: Costos de envío variables según el estrato del cliente
- **Sistema de Descuentos Automáticos**: Aplicación automática de descuentos basados en el monto total
- **Validación Robusta**: Validación exhaustiva de datos con Pydantic
- **Documentación Automática**: Documentación interactiva generada automáticamente con FastAPI
- **Cobertura de Pruebas Completa**: Suite de pruebas unitarias y de integración
- **Código Limpio y Mantenible**: Arquitectura modular siguiendo mejores prácticas

## 📋 Tabla de Contenidos

- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Documentación de la API](#documentación-de-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 🛠️ Instalación

### Prerrequisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd order-management-api

# 2. Crear y activar entorno virtual
python -m venv venv

# En Linux/macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación ejecutando pruebas
pytest tests/ -v
```

### Instalación con Docker

```bash
# Construir imagen
docker build -t order-management-api .

# Ejecutar contenedor
docker run -p 8000:8000 order-management-api
```

## 🚀 Uso Rápido

### Iniciar el Servidor

```bash
# Modo desarrollo (con recarga automática)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

La API estará disponible en: `http://localhost:8000`

### Ejemplo de Uso

```bash
# Calcular costo de pedido
curl -X POST "http://localhost:8000/orders/calculate" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

**Respuesta esperada:**
```json
{
  "subtotal": 2590000.00,
  "shipping_cost": 6000.00,
  "discount_applied": 259000.00,
  "total_cost": 2337000.00,
  "customer_stratum": 3,
  "discount_percentage": 10.0
}
```

## 📚 Documentación de la API

### Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principales

#### POST `/orders/calculate`
Calcula el costo total de un pedido incluyendo productos, envío y descuentos.

**Parámetros de entrada:**
- `products`: Lista de productos con precio y cantidad
- `customer_stratum`: Estrato socioeconómico del cliente (1-6)
- `customer_address`: Dirección de entrega (opcional)

**Respuesta:**
- `subtotal`: Suma total de productos
- `shipping_cost`: Costo de envío según estrato
- `discount_applied`: Monto del descuento aplicado
- `total_cost`: Costo final del pedido
- `customer_stratum`: Estrato del cliente
- `discount_percentage`: Porcentaje de descuento aplicado

#### GET `/orders/shipping-costs`
Consulta los costos de envío por estrato socioeconómico.

#### GET `/orders/discount-info`
Obtiene información sobre la configuración de descuentos.

#### GET `/health`
Health check del servicio.

### Sistema de Estratos y Costos de Envío

| Estrato | Descripción | Costo de Envío |
|---------|-------------|----------------|
| 1 | Bajo-bajo | $8,000 COP |
| 2 | Bajo | $8,000 COP |
| 3 | Medio-bajo | $6,000 COP |
| 4 | Medio | $5,000 COP |
| 5 | Medio-alto | Gratis |
| 6 | Alto | Gratis |

### Sistema de Descuentos

- **Umbral de descuento**: $100,000 COP
- **Porcentaje de descuento**: 10%
- **Aplicación**: Solo sobre el subtotal de productos (no incluye envío)

## 🏗️ Estructura del Proyecto

```
order-management-api/
├── app/                          # Código fuente principal
│   ├── core/                     # Configuración y utilidades centrales
│   │   └── config.py            # Configuración de la aplicación
│   ├── models/                   # Modelos Pydantic
│   │   ├── product.py           # Modelo de producto
│   │   ├── order.py             # Modelos de pedido (request/response)
│   │   └── responses.py         # Modelos de respuesta estándar
│   ├── services/                 # Lógica de negocio
│   │   └── order_service.py     # Servicio de cálculo de pedidos
│   ├── routers/                  # Endpoints de la API
│   │   ├── orders.py            # Endpoints de pedidos
│   │   └── health.py            # Endpoints de salud
│   └── main.py                   # Aplicación principal FastAPI
├── tests/                        # Pruebas unitarias e integración
│   ├── conftest.py              # Configuración de pytest
│   ├── test_order_service.py    # Pruebas de lógica de negocio
│   ├── test_api_endpoints.py    # Pruebas de endpoints
│   └── test_models.py           # Pruebas de modelos
├── docs/                         # Documentación adicional
├── requirements.txt              # Dependencias de Python
├── pytest.ini                   # Configuración de pytest
├── Dockerfile                    # Configuración de Docker
├── docker-compose.yml           # Orquestación con Docker Compose
└── README.md                     # Este archivo
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de la aplicación
APP_NAME="Order Management API"
VERSION="1.0.0"
DEBUG=true

# Configuración de CORS
ALLOWED_ORIGINS=["*"]

# Configuración de costos (opcional - usa valores por defecto)
DISCOUNT_THRESHOLD=100000
DISCOUNT_RATE=0.10
DEFAULT_SHIPPING_COST=6000
```

### Configuración Personalizada

Modifica `app/core/config.py` para ajustar:

- Costos de envío por estrato
- Umbrales y porcentajes de descuento
- Configuración de CORS
- Otros parámetros de la aplicación

## 🧪 Pruebas

### Ejecutar Todas las Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=app --cov-report=html

# Ejecutar solo pruebas unitarias
pytest -m unit

# Ejecutar solo pruebas de integración
pytest -m integration

# Ejecutar con salida detallada
pytest -v
```

### Cobertura de Pruebas

El proyecto mantiene una cobertura de pruebas superior al 80%. El reporte de cobertura se genera en `htmlcov/index.html`.

### Tipos de Pruebas

- **Pruebas Unitarias**: Verifican la lógica de negocio aislada
- **Pruebas de Integración**: Verifican el comportamiento de los endpoints
- **Pruebas de Validación**: Verifican las validaciones de Pydantic
- **Pruebas de Casos Límite**: Verifican comportamiento en situaciones extremas

## 🚀 Despliegue

### Despliegue Local

```bash
# Usando uvicorn directamente
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Usando gunicorn (recomendado para producción)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Despliegue con Docker

```bash
# Construir imagen
docker build -t order-management-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name order-api order-management-api

# Usando Docker Compose
docker-compose up -d
```

### Despliegue en la Nube

#### Heroku

```bash
# Instalar Heroku CLI y hacer login
heroku login

# Crear aplicación
heroku create your-app-name

# Configurar variables de entorno
heroku config:set DEBUG=false

# Desplegar
git push heroku main
```

#### AWS/GCP/Azure

Consulta la documentación específica en `docs/deployment/` para instrucciones detalladas de despliegue en cada plataforma.

## 🔧 Desarrollo

### Configuración del Entorno de Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install

# Ejecutar linters
flake8 app/
black app/
isort app/
```

### Contribuir al Proyecto

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y añade pruebas
4. Ejecuta las pruebas (`pytest`)
5. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
6. Push a la rama (`git push origin feature/nueva-funcionalidad`)
7. Crea un Pull Request

### Estándares de Código

- **Estilo**: PEP 8 con Black formatter
- **Imports**: Organizados con isort
- **Documentación**: Docstrings en formato Google
- **Pruebas**: Cobertura mínima del 80%
- **Commits**: Mensajes descriptivos en español

## 📖 Documentación Adicional

- [Guía de Arquitectura](docs/architecture.md)
- [Manual de Despliegue](docs/deployment.md)
- [Guía de Contribución](docs/contributing.md)
- [Changelog](docs/changelog.md)

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor:

1. Verifica que no esté ya reportado en los issues
2. Crea un nuevo issue con:
   - Descripción detallada del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Información del entorno (OS, Python version, etc.)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Manus AI** - Desarrollo inicial y mantenimiento

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Pydantic por las validaciones robustas
- La comunidad de Python por las herramientas y librerías

---

**¿Necesitas ayuda?** Abre un issue o contacta al equipo de desarrollo.

**¿Te gusta el proyecto?** ¡Dale una estrella ⭐ en GitHub!

