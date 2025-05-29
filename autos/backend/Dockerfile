# autos/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalación de librerías necesarias (libpq para PostgreSQL, gcc para compilar dependencias)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la app
COPY . .

# Comando de inicio (espera a DB y lanza el servidor)
CMD ["bash", "-c", "python -m app.wait_for_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
