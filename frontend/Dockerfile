# =============================================================================
# Dockerfile Frontend - IPS Santa Helena del Valle
# React + TypeScript para perfiles duales (Clínico + Call Center)
# =============================================================================

FROM node:18-alpine AS build

# Metadatos
LABEL maintainer="IPS Santa Helena del Valle"
LABEL description="Frontend React para sistema RIAS"

# Variables de entorno para build
ARG REACT_APP_API_URL=http://localhost:8000
ARG REACT_APP_ENVIRONMENT=production

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY . .

# Build para producción
RUN npm run build

# =============================================================================
# STAGE 2: Nginx para servir archivos estáticos
# =============================================================================
FROM nginx:alpine

# Copiar archivos build al contenedor nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copiar configuración nginx personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]