# Docker Configuration - IPS Santa Helena del Valle

## Overview

Configuración **Growth Tier** de Docker para desarrollo y producción de la IPS Santa Helena del Valle. Esta configuración balancea simplicidad con funcionalidad empresarial.

## Arquitectura Docker

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Frontend      │   │    Backend      │   │   Supabase      │
│   (React)       │   │   (FastAPI)     │   │ (External SaaS) │
│   Port: 3000    │   │   Port: 8000    │   │                 │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx Proxy   │
                    │   Port: 80/443  │
                    └─────────────────┘
```

## Quick Start

### 1. Desarrollo Local (Solo Backend)
```bash
# Método 1: Docker directo
docker build -t ips-backend .
docker run -p 8000:8000 --env-file .env ips-backend

# Método 2: Docker Compose
docker-compose up backend

# Método 3: Makefile
make docker-dev

# Método 4: Script helper
./scripts/docker-dev.sh start
```

### 2. Desarrollo Full-Stack
```bash
# Incluir frontend React
docker-compose --profile full-stack up

# Usando script helper
./scripts/docker-dev.sh full-stack
```

### 3. Producción con Nginx
```bash
# Configuración de producción
docker-compose --profile production up

# Usando script helper
./scripts/docker-dev.sh production
```

## Perfiles de Docker Compose

| Perfil | Servicios | Uso |
|--------|-----------|-----|
| **default** | backend | Desarrollo básico |
| **full-stack** | backend + frontend | Desarrollo completo |
| **production** | backend + frontend + nginx | Despliegue |
| **cache** | + redis | Performance avanzada |

## Configuración de Entorno

### Variables de Entorno (.env)
```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Aplicación
ENVIRONMENT=development
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# APM y Monitoreo
APM_ENABLED=true
METRICS_ENABLED=true
SECURITY_AUDIT_ENABLED=true
```

### Secrets para CI/CD
```bash
# GitHub Actions Secrets
DOCKER_USERNAME=your_docker_hub_username
DOCKER_PASSWORD=your_docker_hub_token
SUPABASE_TEST_URL=your_test_supabase_url
SUPABASE_TEST_KEY=your_test_key
STAGING_HOST=your_staging_server_ip
STAGING_SSH_KEY=your_ssh_private_key
```

## Comandos Útiles

### Desarrollo
```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Acceder al contenedor
docker-compose exec backend /bin/bash

# Reiniciar servicios
docker-compose restart

# Reconstruir imagen
docker-compose build --no-cache backend
```

### Testing
```bash
# Ejecutar tests en contenedor
docker-compose run --rm backend pytest -v

# Health check manual
curl http://localhost:8000/health/

# Performance básico
docker stats --no-stream
```

### Limpieza
```bash
# Detener y limpiar
docker-compose down -v --remove-orphans

# Limpiar imágenes no utilizadas
docker system prune -f

# Limpiar volúmenes
docker volume prune -f
```

## Health Checks

Todos los contenedores incluyen health checks automáticos:

- **Backend**: `GET /health/` cada 30s
- **Frontend**: `GET /` cada 30s  
- **Nginx**: Verificación de puerto cada 30s

## Volúmenes y Persistencia

```yaml
volumes:
  frontend_node_modules:  # Cache de dependencias Node.js
  redis_data:            # Datos de Redis (perfil cache)
```

## Networking

- **Red personalizada**: `ips-santa-helena-network`
- **Comunicación interna**: Por nombres de servicio
- **Puertos expuestos**: 80, 443, 3000, 8000

## Seguridad

### Buenas Prácticas Implementadas
- ✅ Usuario no-root en contenedores
- ✅ Imagen base slim para reducir superficie de ataque
- ✅ .dockerignore para excluir archivos sensibles
- ✅ Health checks para monitoreo
- ✅ Variables de entorno para configuración
- ✅ Rate limiting en Nginx
- ✅ Headers de seguridad

### Configuración SSL (Producción)
```bash
# Generar certificados SSL
mkdir -p docker/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout docker/nginx/ssl/key.pem \
  -out docker/nginx/ssl/cert.pem
```

## Performance

### Optimizaciones Implementadas
- **Multi-stage builds** para imágenes optimizadas
- **Layer caching** en GitHub Actions
- **Gzip compression** en Nginx
- **Static asset caching** con headers apropiados
- **Connection pooling** y keep-alive

### Monitoreo
- APM integrado con métricas detalladas
- Health checks automáticos
- Logs estructurados
- Métricas de sistema disponibles

## Troubleshooting

### Problemas Comunes

#### 1. Puerto ocupado
```bash
# Verificar qué proceso usa el puerto
lsof -i :8000

# Matar proceso si es necesario
kill -9 <PID>
```

#### 2. Problemas de permisos
```bash
# Reconstruir con usuario correcto
docker-compose build --no-cache

# Verificar permisos de archivos
ls -la /path/to/files
```

#### 3. Falta .env
```bash
# Crear .env desde ejemplo
cp .env.example .env

# Usar script de setup
./scripts/dev-setup.sh
```

#### 4. Conectividad con Supabase
```bash
# Verificar variables de entorno
docker-compose exec backend env | grep SUPABASE

# Test de conectividad
curl -H "apikey: $SUPABASE_KEY" $SUPABASE_URL/rest/v1/
```

### Logs de Debug
```bash
# Logs detallados del backend
docker-compose logs --follow --tail=100 backend

# Logs de todos los servicios
docker-compose logs --follow

# Logs con timestamps
docker-compose logs --timestamps backend
```

## CI/CD Integration

### GitHub Actions
- ✅ Tests automatizados en cada push
- ✅ Build de imagen Docker en main
- ✅ Deploy automático a staging
- ✅ Performance testing con k6
- ✅ Security scanning con bandit

### Flujo de Deploy
1. **Push** → Tests automáticos
2. **Tests OK** → Build de imagen Docker
3. **Build OK** → Deploy a staging
4. **Staging OK** → Performance tests
5. **Manual approval** → Deploy a producción

## Comandos de Makefile

```bash
make docker-build     # Construir imágenes
make docker-dev       # Iniciar desarrollo
make docker-prod      # Iniciar producción
make docker-clean     # Limpiar contenedores
make docker-logs      # Ver logs
```

## Recursos

- **Dockerfile**: Configuración del contenedor backend
- **docker-compose.yml**: Orquestación de servicios
- **nginx.conf**: Configuración del proxy reverso
- **Scripts**: `./scripts/docker-dev.sh` para operaciones comunes

## Support

Para problemas específicos de Docker:
1. Revisar logs: `docker-compose logs`
2. Verificar health checks: `docker-compose ps`
3. Ejecutar script de diagnóstico: `./scripts/health-check.sh`
4. Consultar documentación: `backend/CLAUDE.md`