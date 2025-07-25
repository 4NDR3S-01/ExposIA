# ExposIA API Gateway 🚀

API Gateway con GraphQL que orquesta 4 microservicios REST para el sistema ExposIA.

## Arquitectura de Microservicios

```
                    ┌─────────────────┐
                    │   GraphQL       │
                    │   Gateway       │
                    │   (Puerto 4000) │
                    └─────────┬───────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                │             │             │
    ┌───────────▼─┐  ┌───────▼─┐  ┌───────▼─┐  ┌───────▼─┐
    │   PHP       │  │TypeScript│  │ Python  │  │  Java   │
    │Presentaciones│  │Prácticas │  │Feedback │  │Calific. │
    │(Puerto 8001)│  │(Puerto   │  │IA       │  │(Puerto  │
    │             │  │ 3000)    │  │(Puerto  │  │ 8080)   │
    │             │  │          │  │ 8000)   │  │         │
    └─────────────┘  └──────────┘  └─────────┘  └─────────┘
```

## Flujo de Trabajo Principal

### 1. PHP (Presentaciones) - Puerto 8001
- Gestión de usuarios y presentaciones
- Autenticación y autorización
- Almacenamiento de archivos PDF

### 2. TypeScript/NestJS (Prácticas) - Puerto 3000
- Grabación de audio de prácticas
- Navegación por slides
- Fragmentación de audio
- Notas y observaciones

### 3. Python/FastAPI (Feedback IA) - Puerto 8000
- Análisis de métricas con IA
- Generación de feedback inteligente
- Evaluación de parámetros de presentación

### 4. Java/Spring Boot (Calificaciones) - Puerto 8080
- Calificación final de presentaciones
- Criterios de evaluación
- Integración con IA para calificación automática

## Instalación y Configuración

### 1. Instalar dependencias
```bash
cd infra/gateway-dummy
npm install
```

### 2. Configurar variables de entorno
Edita el archivo `.env`:
```env
PHP_API_URL=http://localhost:8001/api
NEST_API_URL=http://localhost:3000
PYTHON_API_URL=http://localhost:8000/api/v1
JAVA_API_URL=http://localhost:8080/api
PORT=4000
```

### 3. Ejecutar el gateway
```bash
# Modo desarrollo
npm run dev

# Modo producción
npm start
```

## Uso del API Gateway

### GraphQL Playground
Una vez iniciado, puedes acceder a GraphQL Playground en:
```
http://localhost:4000
```

### Queries Principales

#### 1. Obtener Flujo Completo de una Presentación
```graphql
query FlujoCompleto {
  flujoCompleto(id_presentacion: "1", id_usuario: "1") {
    usuario {
      id
      nombre
      email
    }
    presentacion {
      id
      titulo
      archivo_pdf
    }
    practica {
      grabacion {
        archivo_audio
        duracion
      }
      navegaciones {
        numero_slide
        tiempo_inicio
        tiempo_fin
      }
    }
    feedback {
      feedback_texto
      puntuacion_general
      metricas {
        valor
        descripcion
      }
    }
    calificacion {
      puntaje_total
      comentario_general
      detalles {
        criterio
        puntaje
        comentario
      }
    }
    estado
    timestamp
  }
}
```

#### 2. Ejecutar Flujo Completo del Sistema
```graphql
mutation EjecutarFlujoCompleto {
  ejecutarFlujoCompleto(
    id_usuario: "1"
    id_presentacion: "1"
    archivo_audio: "presentacion_audio.mp3"
    navegaciones: [
      {
        numero_slide: 1
        tiempo_inicio: 0.0
        tiempo_fin: 30.5
      }
      {
        numero_slide: 2
        tiempo_inicio: 30.5
        tiempo_fin: 65.2
      }
    ]
    notas: [
      {
        numero_slide: 1
        nota: "Introducción clara y concisa"
      }
    ]
    usar_ia_calificacion: true
  ) {
    usuario {
      nombre
    }
    presentacion {
      titulo
    }
    practica {
      grabacion {
        duracion
      }
    }
    feedback {
      puntuacion_general
    }
    calificacion {
      puntaje_total
    }
    estado
  }
}
```

### Queries por Módulo

#### PHP - Usuarios y Presentaciones
```graphql
query {
  usuarios {
    id
    nombre
    email
    presentaciones {
      id
      titulo
    }
  }
}
```

#### TypeScript - Prácticas
```graphql
query {
  practicas(id_usuario: "1") {
    id
    grabacion {
      archivo_audio
      duracion
    }
    navegaciones {
      numero_slide
      tiempo_inicio
      tiempo_fin
    }
  }
}
```

#### Python - Feedback IA
```graphql
query {
  feedbacks(id_usuario: "1") {
    id
    feedback_texto
    puntuacion_general
    metricas {
      valor
      descripcion
      tipo {
        nombre
        peso
      }
    }
  }
}
```

#### Java - Calificaciones
```graphql
query {
  calificaciones(id_usuario: "1") {
    id
    puntaje_total
    comentario_general
    detalles {
      criterio
      puntaje
      comentario
    }
  }
}
```

## Características del Gateway

### ✅ Funcionalidades Implementadas
- **Orquestación de 4 microservicios** REST diferentes
- **Flujo completo** PHP → TS → Python → Java
- **Manejo de errores** robusto con reintentos
- **Timeouts configurables** para cada servicio
- **Logging detallado** para debugging
- **Consultas anidadas** automáticas entre servicios
- **Mutations complejas** que involucran múltiples servicios

### 🔧 Configuración de Desarrollo
- **GraphQL Playground** habilitado para pruebas
- **Hot reload** con nodemon
- **Variables de entorno** para URLs de servicios
- **Error handling** personalizado

### 🛡️ Manejo de Errores
- **Reintentos automáticos** con exponential backoff
- **Timeouts configurables** por servicio
- **Mensajes de error** descriptivos
- **Logging de errores** detallado

## Endpoints de Microservicios

### PHP (Laravel) - Puerto 8001
- `GET /api/usuarios` - Lista de usuarios
- `GET /api/presentaciones` - Lista de presentaciones
- `POST /api/presentaciones` - Crear presentación

### TypeScript (NestJS) - Puerto 3000
- `GET /grabaciones` - Lista de grabaciones
- `POST /grabaciones` - Crear grabación
- `POST /navegacion-slides` - Guardar navegación
- `POST /fragmentar-desde-navegacion/{id}` - Fragmentar audio

### Python (FastAPI) - Puerto 8000
- `GET /api/v1/feedbacks` - Lista de feedbacks
- `POST /api/v1/generar-feedback` - Generar feedback con IA
- `GET /api/v1/tipos-metrica` - Tipos de métricas

### Java (Spring Boot) - Puerto 8080
- `GET /api/calificaciones` - Lista de calificaciones
- `POST /api/calificaciones` - Crear calificación manual
- `POST /api/calificaciones/ai` - Crear calificación con IA

## Desarrollo y Testing

### Ejecutar en modo desarrollo
```bash
npm run dev
```

### Testing con curl
```bash
# Test de salud del gateway
curl -X POST http://localhost:4000 \
  -H "Content-Type: application/json" \
  -d '{"query": "{ usuarios { id nombre } }"}'
```

### Docker Compose
Para ejecutar todo el sistema:
```bash
# Desde la raíz del proyecto
docker-compose up -d
```

## Troubleshooting

### Errores Comunes

1. **Servicio no responde**
   - Verificar que todos los microservicios estén ejecutándose
   - Revisar las URLs en el archivo `.env`

2. **Timeout en consultas**
   - Aumentar el timeout en `resolvers.js`
   - Verificar la conectividad de red

3. **Error de CORS**
   - Configurar CORS en cada microservicio
   - Verificar headers de las peticiones

### Logs y Debugging
El gateway proporciona logs detallados:
- ✅ Peticiones exitosas
- ⚠️ Reintentos automáticos
- ❌ Errores finales
- 📡 Estado de cada microservicio

## Roadmap

### Próximas Mejoras
- [ ] Autenticación centralizada con JWT
- [ ] Cache de consultas frecuentes
- [ ] Rate limiting por usuario
- [ ] Métricas y monitoring
- [ ] Tests automatizados
- [ ] Documentación Swagger/OpenAPI

---

**Desarrollado para ExposIA** - Sistema de gestión de presentaciones con IA
