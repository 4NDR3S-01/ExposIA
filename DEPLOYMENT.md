# Guía de Despliegue - ExposIA 🚀

## Arquitectura del Sistema

```
┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Microservicios │
│  (Consola)      │     │   (Docker)      │
│  Puerto 4000    │     │                 │
└─────────────────┘     └─────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    PHP      │         │ TypeScript  │         │   Python    │
│ Laravel     │         │   NestJS    │         │  FastAPI    │
│ Puerto 8001 │         │ Puerto 3000 │         │ Puerto 8000 │
└─────────────┘         └─────────────┘         └─────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ PostgreSQL  │         │ PostgreSQL  │         │ PostgreSQL  │
│ Puerto 5435 │         │ Puerto 5432 │         │ Puerto 5434 │
└─────────────┘         └─────────────┘         └─────────────┘
                                │
                                ▼
                        ┌─────────────┐
                        │    Java     │
                        │ Spring Boot │
                        │ Puerto 8080 │
                        └─────────────┘
                                │
                                ▼
                        ┌─────────────┐
                        │ PostgreSQL  │
                        │ Puerto 5433 │
                        └─────────────┘
```

## 🚀 Pasos para Levantar el Sistema Completo

### 1. Levantar Microservicios con Docker

Desde la raíz del proyecto:

```bash
# Levantar todos los microservicios y bases de datos
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f presentaciones_php
docker-compose logs -f practicas_ts
docker-compose logs -f feedback_ia_python
docker-compose logs -f springboot_modulo
```

### 2. Verificar que los Microservicios están Funcionando

```bash
# PHP (Presentaciones)
curl http://localhost:8001/api/test

# TypeScript (Prácticas)
curl http://localhost:3000

# Python (Feedback IA)
curl http://localhost:8000

# Java (Calificaciones)
curl http://localhost:8080/api/health
```

### 3. Ejecutar el API Gateway desde Consola

Abrir una nueva terminal y ejecutar:

```bash
cd infra/gateway-dummy
npm install
npm run dev
```

### 4. Verificar el Sistema Completo

Una vez que todo esté ejecutándose:

- **API Gateway**: http://localhost:4000 (GraphQL Playground)
- **PHP API**: http://localhost:8001/api
- **TypeScript API**: http://localhost:3000
- **Python API**: http://localhost:8000
- **Java API**: http://localhost:8080/api

## 🔧 Comandos Útiles

### Docker Compose
```bash
# Levantar servicios
docker-compose up -d

# Parar servicios
docker-compose down

# Rebuild y levantar
docker-compose up -d --build

# Ver estado de contenedores
docker-compose ps

# Limpiar volúmenes (CUIDADO: borra datos)
docker-compose down -v
```

### API Gateway
```bash
# Modo desarrollo (con hot reload)
npm run dev

# Modo producción
npm start

# Ejecutar tests
npm test

# Test con mutation
npm run test-mutation
```

## 🧪 Testing del Sistema

### 1. Test Rápido del Gateway
```bash
cd infra/gateway-dummy
npm test
```

### 2. Test Manual con GraphQL Playground
Ir a http://localhost:4000 y ejecutar:

```graphql
query TestConectividad {
  usuarios {
    id
    nombre
  }
  presentaciones {
    id
    titulo
  }
}
```

### 3. Test del Flujo Completo
```graphql
mutation TestFlujo {
  ejecutarFlujoCompleto(
    id_usuario: "1"
    id_presentacion: "1"
    archivo_audio: "test.mp3"
    navegaciones: [{
      numero_slide: 1
      tiempo_inicio: 0.0
      tiempo_fin: 30.0
    }]
    usar_ia_calificacion: false
  ) {
    estado
    usuario { nombre }
    presentacion { titulo }
  }
}
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Puerto ya en uso**
   ```bash
   # Ver qué proceso usa el puerto
   netstat -ano | findstr :8001
   
   # Matar proceso (reemplazar PID)
   taskkill /PID <PID> /F
   ```

2. **Microservicio no responde**
   ```bash
   # Ver logs del contenedor
   docker-compose logs <nombre_servicio>
   
   # Reiniciar servicio específico
   docker-compose restart <nombre_servicio>
   ```

3. **Gateway no conecta a microservicios**
   - Verificar que todos los contenedores estén ejecutándose
   - Verificar las URLs en el archivo `.env` del gateway
   - Revisar logs del gateway para errores específicos

4. **Error de base de datos**
   ```bash
   # Recrear volúmenes de BD
   docker-compose down -v
   docker-compose up -d
   ```

### Logs Útiles

```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs del gateway (desde su directorio)
npm run dev

# Logs específicos
docker-compose logs -f presentaciones_php
docker-compose logs -f practicas_ts
docker-compose logs -f feedback_ia_python
docker-compose logs -f springboot_modulo
```

## 📝 Orden de Inicio Recomendado

1. **Bases de datos** (se levantan automáticamente con docker-compose)
2. **Microservicios** (docker-compose up -d)
3. **Esperar 30-60 segundos** para que inicialicen
4. **API Gateway** (npm run dev desde consola)

## 🔍 Monitoreo

### URLs de Health Check
- PHP: http://localhost:8001/api/test
- TypeScript: http://localhost:3000/debug/resumen/1
- Python: http://localhost:8000/health
- Java: http://localhost:8080/api/health (si está implementado)

### Puertos Ocupados
- **4000**: API Gateway GraphQL
- **8001**: PHP Laravel API
- **3000**: TypeScript NestJS API
- **8000**: Python FastAPI
- **8080**: Java Spring Boot API
- **5432-5435**: Bases de datos PostgreSQL

## 🎯 Flujo de Desarrollo

1. **Desarrollo de microservicios**: Usar Docker Compose
2. **Desarrollo del gateway**: Usar consola con `npm run dev`
3. **Testing**: Usar GraphQL Playground y npm test
4. **Debugging**: Logs en tiempo real desde ambos entornos

---

**¡Sistema ExposIA listo para desarrollo!** 🚀
