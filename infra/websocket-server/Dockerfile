FROM node:18-alpine

LABEL maintainer="ExposIA Team"
LABEL description="WebSocket Server for ExposIA Real-time Communication"

# Crear directorio de la aplicación
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production && npm cache clean --force

# Copiar código fuente
COPY . .

# Crear usuario no-root para seguridad
RUN addgroup -g 1001 -S nodejs && \
    adduser -S websocket -u 1001

# Cambiar ownership del directorio
RUN chown -R websocket:nodejs /app

# Cambiar a usuario no-root
USER websocket

# Exponer puerto
EXPOSE 4001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "const WebSocket = require('ws'); const ws = new WebSocket('ws://localhost:4001/ws'); ws.on('open', () => { ws.close(); process.exit(0); }); ws.on('error', () => process.exit(1));"

# Comando por defecto
CMD ["node", "websocket-server.js"]
