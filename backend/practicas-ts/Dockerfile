# Usa una imagen oficial de Node.js como base
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código fuente
COPY . .

# Construye la app (si aplica)
RUN npm run build

# Expone el puerto de la app
EXPOSE 3000

# Comando por defecto para iniciar la app
CMD ["npm", "run", "start:prod"] 