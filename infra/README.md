# 🛠️ Infraestructura de ExposIA (stubs de desarrollo)

Guía rápida para levantar y extender el **Gateway GraphQL dummy** y el **WebSocket Logger**.  
Permite que cada alumno pruebe su micro-servicio REST sin depender de los demás.

---

## Requisitos

| Herramienta | Versión |
|-------------|---------|
| Docker Desktop | 4.x+ |
| Git | — |
| VS Code (recomendado) | — |
| Node 18+ (opcional, para correr stubs fuera de Docker) | — |

---

## Estructura

```
infra/
├─ docker-compose.yml
├─ gateway-dummy/
│   └─ index.js
└─ ws-logger/
    └─ index.js
```

---

## Levantar todo

```bash
cd infra
docker compose up --build   # primera vez
docker compose up           # siguientes arranques
```

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Gateway stub | http://localhost:4000/graphql | Responde `ping` y la query del módulo activo |
| WS-logger | ws://localhost:9000/ws  \|  POST http://localhost:9000/notify | Imprime y reenvía eventos en tiempo real |

> `host.docker.internal` ya está configurado para que el contenedor alcance tu servidor local (Herd, Nest, etc.).

---

## Probar tu micro-servicio REST

1. **Arranca** los contenedores (`docker compose up`).  
2. **Levanta** tu servicio (ej. `php artisan serve`, `npm run start`, etc.).  
3. **Edita** `gateway-dummy/index.js` y agrega tu resolver:

   ```js
   const REST_URL = 'http://host.docker.internal';

   const typeDefs = gql\`
     type Presentation { id: ID! titulo: String! }
     type Query { presentations: [Presentation!]! }
   \`;

   const resolvers = {
     Query: {
       presentations: () =>
         fetch(\`\${REST_URL}/api/presentaciones\`).then(r => r.json()),
     },
   };
   ```

4. Consulta en GraphQL:

   ```graphql
   query { presentations { id titulo } }
   ```

---

## Enviar eventos (Notifier)

1. En tu `.env`:

   ```
   WS_URL=http://localhost:9000
   WS_TOKEN=dev
   ```

2. Código de ejemplo (Laravel):

   ```php
   Http::withToken(env('WS_TOKEN'))->post(env('WS_URL').'/notify', [
       'event' => 'presentation.created',
       'payload' => ['id' => $id, 'titulo' => $titulo],
   ]);
   ```

3. Escucha en el navegador:

   ```js
   const ws = new WebSocket("ws://localhost:9000/ws");
   ws.onmessage = e => console.log(e.data);
   ```

---

## Checklist antes de hacer commit

- [ ] Resolver GraphQL añadido en `gateway-dummy/index.js`.
- [ ] Evento enviado con `POST /notify` y visible en WS-logger.
- [ ] README de tu micro-servicio actualizado con endpoint de login y ejemplo de evento.

---

## FAQ

| Pregunta | Respuesta |
|----------|-----------|
| ¿Puedo correr los stubs sin Docker? | `node gateway-dummy/index.js` y `node ws-logger/index.js` |
| ¿Por qué “host.docker.internal”? | Hace que Docker vea tu localhost sin tocar `/etc/hosts`. |
| Mi REST usa otro puerto | Cambia la variable `REST_MISERVICIO_URL` en `docker-compose.yml`. |
| ¿Tengo que subir `node_modules`? | No: el contenedor corre `npm install` en cada arranque. |
| ¿Qué pasa al pasar al Gateway real? | Se reemplaza `gateway-dummy/` por `gateway/`; tus resolvers ya migrados funcionarán sin cambios. |

---
