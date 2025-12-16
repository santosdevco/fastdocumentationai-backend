FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/
COPY run.py .

# Crear directorio para .env si no existe
RUN mkdir -p /app

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto (se sobrescriben con docker-compose)
ENV MONGODB_URL=mongodb://mongodb:27017
ENV DATABASE_NAME=documentation_ai
ENV HOST=0.0.0.0
ENV PORT=8000
ENV ENVIRONMENT=production

# Comando de inicio
CMD ["python", "run.py"]
