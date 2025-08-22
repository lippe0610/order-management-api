# Order Management API

## Descripción General

Este proyecto implementa una API RESTful para la gestión de pedidos, desarrollada con **FastAPI** y **Python**. La API permite calcular el costo total de un pedido, aplicando lógica de negocio específica para descuentos y cargos de envío basados en el sistema de estratos socioeconómicos de Colombia.

## Características Principales

*   **Cálculo de Costo Total**: Determina el costo final de un pedido, incluyendo el subtotal de productos, cargos de envío y descuentos aplicables.
*   **Sistema de Descuentos**: Aplica un descuento del 10% sobre el subtotal para pedidos que superen un umbral predefinido.
*   **Cargos de Envío por Estrato**: Los costos de envío varían según el estrato socioeconómico del cliente, reflejando las condiciones de Colombia.
*   **Validación de Datos**: Utiliza Pydantic para una validación robusta de los payloads JSON de entrada.
*   **API Documentada**: Generación automática de documentación interactiva (Swagger UI) y esquemas OpenAPI.
*   **Pruebas Unitarias**: Cobertura de pruebas exhaustiva para asegurar la fiabilidad de la lógica de negocio y los endpoints.
*   **Containerización**: Soporte para Docker y Docker Compose (opcional) para facilitar el despliegue y la portabilidad.

## Estructura del Proyecto

order-management-api/
├── app/
│   ├── core/                 # Configuración de la aplicación
│   ├── models/               # Definiciones de modelos de datos (Pydantic)
│   ├── services/             # Lógica de negocio y cálculos
│   ├── routers/              # Endpoints de la API (FastAPI)
│   └── main.py               # Aplicación principal de FastAPI
├── tests/                    # Pruebas unitarias y de integración
├── docs/                     # Documentación adicional (arquitectura)
├── Dockerfile                # Definición del contenedor Docker
├── docker-compose.yml        # Orquestación de servicios Docker
├── requirements.txt          # Dependencias del proyecto
├── pytest.ini                # Configuración de Pytest
└── README.md                 # Documentación del proyecto
Plain Text

## Requisitos

*   Python 3.9+
*   pip (administrador de paquetes de Python)
*   Docker y Docker Compose (opcional, para despliegue containerizado)

## Configuración e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/lippe0610/order-management-api.git
    cd order-management-api
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución de la API

Para iniciar la API localmente:

La API estará disponible en http://localhost:8000.
Documentación de la API
La documentación interactiva (Swagger UI ) está disponible en:
http://localhost:8000/docs

