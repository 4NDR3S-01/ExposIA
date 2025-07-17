# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Expone el puerto de la app
EXPOSE 8000

# Comando por defecto para iniciar la app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] 