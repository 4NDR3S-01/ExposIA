# Propuesta de Clean Architecture para feedback-ia-python

## 📁 Estructura de Carpetas Propuesta

```
src/
├── domain/                     # Capa de Dominio (Lógica de Negocio Pura)
│   ├── entities/               # Entidades del dominio
│   │   ├── __init__.py
│   │   ├── tipo_metrica.py
│   │   ├── metrica.py
│   │   ├── parametro.py
│   │   ├── grabacion.py
│   │   └── feedback.py
│   ├── value_objects/          # Objetos de valor
│   │   ├── __init__.py
│   │   ├── metrica_value.py
│   │   └── feedback_score.py
│   ├── repositories/           # Interfaces de repositorios (abstracciones)
│   │   ├── __init__.py
│   │   ├── tipo_metrica_repository.py
│   │   ├── metrica_repository.py
│   │   ├── parametro_repository.py
│   │   ├── grabacion_repository.py
│   │   └── feedback_repository.py
│   ├── services/               # Servicios de dominio
│   │   ├── __init__.py
│   │   ├── feedback_analyzer.py
│   │   └── metrica_calculator.py
│   └── exceptions/             # Excepciones del dominio
│       ├── __init__.py
│       ├── domain_exceptions.py
│       └── validation_exceptions.py
├── application/                # Capa de Aplicación (Casos de Uso)
│   ├── use_cases/              # Casos de uso
│   │   ├── __init__.py
│   │   ├── tipo_metrica/
│   │   │   ├── __init__.py
│   │   │   ├── create_tipo_metrica.py
│   │   │   ├── get_tipo_metrica.py
│   │   │   ├── get_tipos_metrica.py
│   │   │   └── delete_tipo_metrica.py
│   │   ├── metrica/
│   │   │   ├── __init__.py
│   │   │   ├── create_metrica.py
│   │   │   ├── get_metrica.py
│   │   │   ├── get_metricas.py
│   │   │   └── update_metrica.py
│   │   ├── parametro/
│   │   │   ├── __init__.py
│   │   │   ├── create_parametro.py
│   │   │   ├── get_parametro.py
│   │   │   ├── get_parametros.py
│   │   │   └── update_parametro.py
│   │   ├── grabacion/
│   │   │   ├── __init__.py
│   │   │   ├── create_grabacion.py
│   │   │   ├── get_grabacion.py
│   │   │   ├── get_grabaciones.py
│   │   │   └── analyze_grabacion.py
│   │   └── feedback/
│   │       ├── __init__.py
│   │       ├── create_feedback.py
│   │       ├── get_feedback.py
│   │       ├── get_feedbacks.py
│   │       ├── get_feedbacks_by_grabacion.py
│   │       └── generate_ai_feedback.py
│   ├── dtos/                   # DTOs de la aplicación
│   │   ├── __init__.py
│   │   ├── tipo_metrica_dto.py
│   │   ├── metrica_dto.py
│   │   ├── parametro_dto.py
│   │   ├── grabacion_dto.py
│   │   └── feedback_dto.py
│   └── interfaces/             # Interfaces de servicios externos
│       ├── __init__.py
│       ├── ai_service_interface.py
│       └── audio_analyzer_interface.py
├── infrastructure/             # Capa de Infraestructura (Implementaciones)
│   ├── database/               # Persistencia de datos
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── models/             # Modelos SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── tipo_metrica_model.py
│   │   │   ├── metrica_model.py
│   │   │   ├── parametro_model.py
│   │   │   ├── grabacion_model.py
│   │   │   └── feedback_model.py
│   │   └── repositories/       # Implementaciones de repositorios
│   │       ├── __init__.py
│   │       ├── sqlalchemy_tipo_metrica_repository.py
│   │       ├── sqlalchemy_metrica_repository.py
│   │       ├── sqlalchemy_parametro_repository.py
│   │       ├── sqlalchemy_grabacion_repository.py
│   │       └── sqlalchemy_feedback_repository.py
│   ├── external_services/      # Servicios externos
│   │   ├── __init__.py
│   │   ├── openai_service.py
│   │   ├── audio_analysis_service.py
│   │   └── ml_feedback_service.py
│   └── config/                 # Configuraciones
│       ├── __init__.py
│       ├── database_config.py
│       ├── ai_config.py
│       └── settings.py
├── interface/                  # Capa de Interfaz (Controladores y APIs)
│   ├── api/                    # API REST
│   │   ├── __init__.py
│   │   ├── v1/                 # Versionado de API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tipo_metrica_endpoints.py
│   │   │   │   ├── metrica_endpoints.py
│   │   │   │   ├── parametro_endpoints.py
│   │   │   │   ├── grabacion_endpoints.py
│   │   │   │   └── feedback_endpoints.py
│   │   │   ├── schemas/        # Esquemas Pydantic para validación
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tipo_metrica_schemas.py
│   │   │   │   ├── metrica_schemas.py
│   │   │   │   ├── parametro_schemas.py
│   │   │   │   ├── grabacion_schemas.py
│   │   │   │   └── feedback_schemas.py
│   │   │   └── dependencies.py # Dependencias de FastAPI
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── error_handler.py
│   │       └── logging_middleware.py
│   └── cli/                    # Interfaz de línea de comandos (opcional)
│       ├── __init__.py
│       └── commands.py
├── shared/                     # Capa Compartida
│   ├── __init__.py
│   ├── utils/                  # Utilidades compartidas
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   └── constants.py
│   └── types/                  # Tipos compartidos
│       ├── __init__.py
│       └── common_types.py
├── tests/                      # Tests organizados por capas
│   ├── __init__.py
│   ├── unit/                   # Tests unitarios
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/            # Tests de integración
│   │   ├── api/
│   │   └── database/
│   └── e2e/                    # Tests end-to-end
│       └── test_feedback_flow.py
└── main.py                     # Punto de entrada principal
```

## 🔧 Componentes Clave

### 1. Domain Layer (Dominio)
- **Entidades**: Lógica de negocio pura sin dependencias externas
- **Value Objects**: Objetos inmutables que representan conceptos del dominio
- **Repositories (Interfaces)**: Contratos para persistencia
- **Domain Services**: Lógica compleja que no pertenece a una entidad específica

### 2. Application Layer (Aplicación)
- **Use Cases**: Orquestación de la lógica de negocio
- **DTOs**: Objetos de transferencia de datos
- **Interfaces**: Contratos para servicios externos

### 3. Infrastructure Layer (Infraestructura)
- **Database**: Implementaciones concretas de persistencia
- **External Services**: Integraciones con servicios externos (IA, ML)
- **Configuration**: Configuraciones y settings

### 4. Interface Layer (Interfaz)
- **API**: Controladores REST y esquemas de validación
- **CLI**: Interfaz de línea de comandos (opcional)
