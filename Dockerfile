# =============================================================================
# Dockerfile - IPS Santa Helena del Valle Backend
# Configuración Growth Tier - Balance simplicidad/funcionalidad
# =============================================================================

FROM python:3.12-slim

# Metadatos del contenedor
LABEL maintainer="IPS Santa Helena del Valle"
LABEL description="API REST para RIAS según Resolución 3280 de 2018"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero (optimización de cache)
COPY backend/requirements.txt /app/backend/
COPY backend/requirements-lock.txt /app/backend/

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copiar código fuente
COPY backend/ /app/backend/
COPY conftest.py /app/

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Comando por defecto
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]