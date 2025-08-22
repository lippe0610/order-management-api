# Arquitectura del Sistema

## Visión General

La Order Management API está diseñada siguiendo principios de arquitectura limpia y patrones de diseño modernos. El sistema utiliza una arquitectura en capas que separa claramente las responsabilidades y facilita el mantenimiento y escalabilidad.

## Arquitectura en Capas

### 1. Capa de Presentación (Routers)
- **Responsabilidad**: Manejo de requests HTTP y responses
- **Componentes**: 
  - `orders.py`: Endpoints relacionados con pedidos
  - `health.py`: Endpoints de salud y utilidades
- **Características**:
  - Validación de entrada usando Pydantic
  - Manejo de errores HTTP
  - Documentación automática con OpenAPI

### 2. Capa de Lógica de Negocio (Services)
- **Responsabilidad**: Implementación de reglas de negocio
- **Componentes**:
  - `OrderService`: Cálculos de pedidos, envíos y descuentos
- **Características**:
  - Lógica pura sin dependencias externas
  - Métodos estáticos para facilitar testing
  - Separación clara de responsabilidades

### 3. Capa de Modelos (Models)
- **Responsabilidad**: Definición de estructuras de datos
- **Componentes**:
  - `Product`: Modelo de producto
  - `OrderRequest/OrderResponse`: Modelos de pedido
  - `ErrorResponse/SuccessResponse`: Modelos de respuesta
- **Características**:
  - Validación automática con Pydantic
  - Serialización/deserialización automática
  - Documentación de esquemas

### 4. Capa de Configuración (Core)
- **Responsabilidad**: Configuración centralizada
- **Componentes**:
  - `config.py`: Configuración de la aplicación
- **Características**:
  - Configuración centralizada
  - Valores por defecto sensatos
  - Fácil modificación sin cambios de código

## Patrones de Diseño Implementados

### 1. Dependency Injection
- Uso de FastAPI para inyección de dependencias
- Facilita testing y modularidad

### 2. Repository Pattern (Preparado para futuras expansiones)
- Estructura preparada para abstracción de datos
- Facilita cambio de fuentes de datos

### 3. Service Layer Pattern
- Separación de lógica de negocio
- Reutilización de código
- Testing simplificado

### 4. Factory Pattern
- Creación de objetos de respuesta
- Configuración de aplicación

## Flujo de Datos

```
Request HTTP → Router → Service → Models → Response HTTP
     ↓           ↓        ↓        ↓         ↓
  Validación → Lógica → Cálculos → Datos → Serialización
```

### Flujo Detallado de Cálculo de Pedido

1. **Recepción del Request**
   - Router recibe POST `/orders/calculate`
   - Pydantic valida automáticamente el JSON

2. **Validación de Reglas de Negocio**
   - `OrderService.validate_order_business_rules()`
   - Verificación de reglas adicionales

3. **Cálculo de Subtotal**
   - `OrderService.calculate_subtotal()`
   - Suma de precio × cantidad por producto

4. **Cálculo de Envío**
   - `OrderService.calculate_shipping_cost()`
   - Basado en estrato socioeconómico

5. **Cálculo de Descuentos**
   - `OrderService.calculate_discount()`
   - Aplicación de descuentos según umbral

6. **Cálculo Total**
   - `OrderService.calculate_order_total()`
   - Orquestación de todos los cálculos

7. **Respuesta**
   - Creación de `OrderResponse`
   - Serialización automática a JSON

## Principios de Diseño

### SOLID Principles

#### Single Responsibility Principle (SRP)
- Cada clase tiene una única responsabilidad
- `OrderService` solo maneja cálculos
- `Product` solo representa datos de producto

#### Open/Closed Principle (OCP)
- Abierto para extensión, cerrado para modificación
- Nuevos tipos de descuento se pueden agregar sin modificar código existente

#### Liskov Substitution Principle (LSP)
- Los modelos Pydantic son intercambiables
- Interfaces consistentes

#### Interface Segregation Principle (ISP)
- Interfaces específicas y pequeñas
- Separación de concerns

#### Dependency Inversion Principle (DIP)
- Dependencias hacia abstracciones
- Configuración inyectable

### Clean Architecture

#### Independencia de Frameworks
- Lógica de negocio independiente de FastAPI
- Fácil migración a otros frameworks

#### Testabilidad
- Cada capa es testeable independientemente
- Mocks y stubs fáciles de implementar

#### Independencia de UI
- API puede servir múltiples interfaces
- Web, mobile, CLI, etc.

#### Independencia de Base de Datos
- Preparado para múltiples fuentes de datos
- Sin dependencias hard-coded

## Escalabilidad

### Escalabilidad Horizontal
- Stateless design
- Múltiples instancias sin problemas
- Load balancing friendly

### Escalabilidad Vertical
- Uso eficiente de recursos
- Operaciones O(n) lineales
- Memory footprint mínimo

### Puntos de Extensión

#### Nuevos Tipos de Productos
```python
class DigitalProduct(Product):
    download_url: str
    license_type: str
```

#### Nuevos Métodos de Descuento
```python
class VolumeDiscountService:
    @staticmethod
    def calculate_volume_discount(quantity: int) -> float:
        # Lógica de descuento por volumen
        pass
```

#### Nuevas Fuentes de Configuración
```python
class DatabaseConfig(Settings):
    # Configuración desde base de datos
    pass
```

## Seguridad

### Validación de Entrada
- Pydantic valida todos los inputs
- Prevención de inyección de datos
- Tipos seguros

### CORS
- Configuración flexible
- Restricción por dominio en producción

### Rate Limiting (Preparado)
- Estructura para implementar rate limiting
- Prevención de abuso

## Monitoreo y Observabilidad

### Health Checks
- Endpoint `/health` para monitoreo
- Verificación de estado del servicio

### Logging (Preparado)
- Estructura para logging estructurado
- Trazabilidad de requests

### Métricas (Preparado)
- Preparado para Prometheus
- Métricas de negocio y técnicas

## Consideraciones de Performance

### Optimizaciones Implementadas
- Operaciones matemáticas eficientes
- Validación temprana de datos
- Respuestas JSON optimizadas

### Optimizaciones Futuras
- Caché de configuración
- Pooling de conexiones
- Compresión de respuestas

## Testing Strategy

### Pirámide de Testing
- **Unit Tests**: Lógica de negocio aislada
- **Integration Tests**: Endpoints completos
- **Contract Tests**: Validación de esquemas

### Coverage
- Objetivo: >80% de cobertura
- Enfoque en lógica crítica de negocio
- Testing de casos límite

## Deployment Architecture

### Containerización
- Docker para consistencia
- Multi-stage builds para optimización
- Health checks integrados

### Orquestación
- Docker Compose para desarrollo
- Kubernetes ready para producción

### CI/CD Ready
- Testing automatizado
- Builds reproducibles
- Deployment automatizado

## Futuras Mejoras

### Persistencia
- Integración con bases de datos
- Audit trail de pedidos
- Histórico de configuraciones

### Microservicios
- Separación en servicios independientes
- Event-driven architecture
- Service mesh integration

### Machine Learning
- Predicción de descuentos personalizados
- Optimización de costos de envío
- Análisis de patrones de pedidos

