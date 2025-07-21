# 🌐 ExposIA Gateway GraphQL

API Gateway unificado desarrollado en TypeScript que centraliza el acceso a todos los microservicios de ExposIA.

## 🎯 Funcionalidades

- **Punto único de entrada** para todos los microservicios
- **Schema GraphQL unificado** con todas las entidades del sistema
- **Consultas complejas** que combinan datos de múltiples servicios
- **Notificaciones automáticas** a través de WebSocket
- **Estadísticas del sistema** en tiempo real
- **Testing automatizado** con Jest

## 🚀 Inicio Rápido

### Desarrollo Local

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Iniciar en modo desarrollo
npm run dev

# El servidor estará disponible en:
# http://localhost:4000/graphql
```

### Docker

```bash
# Construir imagen
docker build -t exposia-gateway .

# Ejecutar contenedor
docker run -p 4000:4000 exposia-gateway
```

## 📊 Schema GraphQL

### Consultas Principales

```graphql
# Obtener todas las presentaciones con relaciones
query ObtenerPresentaciones {
  presentaciones {
    id
    titulo
    usuario {
      id
      nombre
      email
    }
    tema {
      id
      nombre
    }
    slides {
      id
      numeroSlide
      textoSlide
    }
    grabaciones {
      id
      fechaGrabacion
      calificaciones {
        puntajeGlobal
        observacionGlobal
      }
      feedbacks {
        valor
        comentario
        parametro {
          nombre
          unidad
        }
      }
    }
  }
}

# Estadísticas del sistema
query EstadisticasGenerales {
  estadisticasGenerales {
    totalUsuarios
    totalPresentaciones
    totalGrabaciones
    totalCalificaciones
    promedioCalificaciones
    presentacionesPorTema {
      tema {
        nombre
      }
      cantidad
      promedioCalificacion
    }
    actividadReciente {
      tipo
      descripcion
      fecha
    }
  }
}

# Datos específicos de un usuario
query DatosUsuario($usuarioId: ID!) {
  usuario(id: $usuarioId) {
    id
    nombre
    email
    presentaciones {
      id
      titulo
      tema { nombre }
    }
    grabaciones {
      id
      fechaGrabacion
      presentacion { titulo }
      calificaciones {
        puntajeGlobal
      }
    }
    calificaciones {
      puntajeGlobal
      observacionGlobal
      fecha
    }
  }
}
```

### Mutaciones

```graphql
# Crear nuevo usuario
mutation CrearUsuario($input: CrearUsuarioInput!) {
  crearUsuario(input: $input) {
    id
    nombre
    email
  }
}

# Crear presentación
mutation CrearPresentacion($input: CrearPresentacionInput!) {
  crearPresentacion(input: $input) {
    id
    titulo
    usuario { nombre }
    tema { nombre }
  }
}

# Crear feedback
mutation CrearFeedback($input: CrearFeedbackInput!) {
  crearFeedback(input: $input) {
    id
    valor
    comentario
    grabacion { id }
    parametro { nombre }
  }
}

# Enviar notificación de prueba
mutation EnviarNotificacionPrueba($mensaje: String!) {
  enviarNotificacionPrueba(mensaje: $mensaje)
}
```

## 🔧 Configuración

### Variables de Entorno

```env
# Puerto del servidor
PORT=4000

# URLs de microservicios
PRESENTACIONES_API_URL=http://localhost:8001/api
PRACTICAS_API_URL=http://localhost:3000
FEEDBACK_API_URL=http://localhost:8000/api/v1
CALIFICACION_API_URL=http://localhost:8080/api

# Autenticación para microservicios
PRESENTACIONES_JWT_TOKEN=your-jwt-token-here
PRACTICAS_API_KEY=mi-token-seguro
FEEDBACK_API_KEY=test-api-key-12345
CALIFICACION_API_USER=admin
CALIFICACION_API_PASS=admin123

# WebSocket para notificaciones
WS_NOTIFICATION_URL=http://localhost:9000
WS_NOTIFICATION_TOKEN=dev

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## 🏗️ Arquitectura

### Data Sources

El Gateway utiliza el patrón **Data Source** para comunicarse con cada microservicio:

- **PresentacionesAPI**: Gestión de usuarios, temas, presentaciones y slides
- **PracticasAPI**: Grabaciones, navegación, fragmentos y notas
- **FeedbackAPI**: Análisis de IA, métricas y parámetros
- **CalificacionAPI**: Calificaciones y evaluaciones

### Resolvers

Los resolvers están organizados por entidad:

- **usuarioResolvers**: Consultas y mutaciones de usuarios
- **presentacionResolvers**: Gestión de presentaciones y temas
- **grabacionResolvers**: Datos de prácticas y grabaciones
- **feedbackResolvers**: Feedback y métricas de IA
- **calificacionResolvers**: Sistema de calificación
- **estadisticasResolvers**: Métricas del sistema

### Notificaciones

Cada mutación importante envía notificaciones automáticas:

```typescript
// Ejemplo en resolver
const usuario = await dataSources.presentacionesAPI.crearUsuario(input);

// Enviar notificación automática
await notificationService.enviarNotificacion('usuario.creado', {
  id: usuario.id,
  nombre: usuario.nombre,
  email: usuario.email
});
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests unitarios
npm test

# Tests con coverage
npm run test:coverage

# Tests en modo watch
npm run test:watch
```

### Estructura de Tests

```
src/__tests__/
├── resolvers.test.ts      # Tests de resolvers principales
├── dataSources.test.ts    # Tests de data sources
├── integration.test.ts    # Tests de integración
└── schema.test.ts         # Validación de schema
```

### Ejemplo de Test

```typescript
describe('Usuario Resolvers', () => {
  test('debe crear usuario y enviar notificación', async () => {
    const input = {
      nombre: 'Test User',
      email: 'test@example.com',
      password: 'password123'
    };

    const result = await resolvers.Mutation.crearUsuario(
      null, 
      { input }, 
      mockContext
    );
    
    expect(result).toHaveProperty('nombre', 'Test User');
    expect(mockNotificationService.enviarNotificacion)
      .toHaveBeenCalledWith('usuario.creado', expect.any(Object));
  });
});
```

## 📈 Monitoreo

### Health Check

```bash
curl http://localhost:4000/health
```

### Métricas GraphQL

El playground de GraphQL incluye métricas automáticas:
- Tiempo de respuesta por query
- Errores y warnings
- Uso de cache
- Estadísticas de resolvers

### Logs

```bash
# Ver logs en desarrollo
npm run dev

# Logs en producción
docker-compose logs gateway_graphql
```

## 🔄 Integración con Microservicios

### Flujo de Datos

1. **Cliente** envía query GraphQL al Gateway
2. **Gateway** parsea la query y determina qué data sources necesita
3. **Data Sources** hacen llamadas HTTP a los microservicios correspondientes
4. **Resolvers** combinan y transforman los datos
5. **Gateway** retorna respuesta unificada al cliente

### Manejo de Errores

```typescript
// Los data sources manejan errores gracefully
async getUsuarios() {
  try {
    const response = await this.api.get('/usuarios');
    return response.data.data || response.data;
  } catch (error) {
    console.error('Error obteniendo usuarios:', error);
    return []; // Retorna array vacío en lugar de fallar
  }
}
```

### Cache y Performance

- **Timeout configurado** en todas las llamadas HTTP (10s)
- **Retry logic** para servicios temporalmente no disponibles
- **Parallel queries** cuando es posible
- **Error boundaries** para evitar fallos en cascada

## 🚀 Deployment

### Desarrollo

```bash
npm run dev
```

### Producción

```bash
npm run build
npm start
```

### Docker Compose

```yaml
gateway_graphql:
  build: ./gateway-graphql
  ports:
    - "4000:4000"
  environment:
    NODE_ENV: production
    # ... otras variables
```

## 📚 Recursos

- **GraphQL Playground**: http://localhost:4000/graphql
- **Documentación Apollo**: https://www.apollographql.com/docs/
- **TypeScript**: https://www.typescriptlang.org/docs/
- **Schema Design**: https://graphql.org/learn/schema/

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Convenciones

- **Naming**: camelCase para campos GraphQL
- **Resolvers**: Un archivo por entidad principal
- **Tests**: Cobertura mínima del 80%
- **Docs**: Documentar schema con descripciones GraphQL