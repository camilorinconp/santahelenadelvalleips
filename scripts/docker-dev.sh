#!/bin/bash
# =============================================================================
# Docker Development Helper - IPS Santa Helena del Valle
# Scripts para manejo de contenedores en desarrollo
# =============================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() { echo -e "${BLUE}📋 $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado"
    exit 1
fi

# Función para mostrar ayuda
show_help() {
    echo "🐳 Docker Development Helper - IPS Santa Helena del Valle"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start         Iniciar todos los servicios"
    echo "  stop          Detener todos los servicios"
    echo "  restart       Reiniciar todos los servicios"
    echo "  build         Construir imágenes"
    echo "  rebuild       Reconstruir imágenes forzando"
    echo "  logs          Mostrar logs de todos los servicios"
    echo "  logs-backend  Mostrar logs solo del backend"
    echo "  logs-frontend Mostrar logs solo del frontend"
    echo "  shell-backend Abrir shell en contenedor backend"
    echo "  test          Ejecutar tests en contenedor"
    echo "  clean         Limpiar contenedores e imágenes"
    echo "  status        Mostrar estado de contenedores"
    echo "  help          Mostrar esta ayuda"
    echo ""
    echo "Perfiles disponibles:"
    echo "  full-stack    Incluir frontend React"
    echo "  production    Configuración con nginx"
    echo "  cache         Incluir Redis para cache"
}

# Función para verificar si .env existe
check_env() {
    if [ ! -f ".env" ]; then
        print_warning "Archivo .env no encontrado"
        print_step "Creando .env de ejemplo..."
        
        cat > .env << EOF
# Docker Development Environment
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
SECRET_KEY=docker-dev-secret-key
ENVIRONMENT=development
EOF
        print_success "Archivo .env creado"
    fi
}

# Comandos principales
case "$1" in
    "start")
        check_env
        print_step "Iniciando servicios Docker..."
        docker-compose up -d
        print_success "Servicios iniciados"
        print_step "Esperando que los servicios estén listos..."
        sleep 10
        docker-compose ps
        echo ""
        print_success "Backend disponible en: http://localhost:8000"
        print_success "Health check: http://localhost:8000/health/"
        ;;
        
    "stop")
        print_step "Deteniendo servicios Docker..."
        docker-compose down
        print_success "Servicios detenidos"
        ;;
        
    "restart")
        print_step "Reiniciando servicios Docker..."
        docker-compose down
        docker-compose up -d
        print_success "Servicios reiniciados"
        ;;
        
    "build")
        print_step "Construyendo imágenes Docker..."
        docker-compose build
        print_success "Imágenes construidas"
        ;;
        
    "rebuild")
        print_step "Reconstruyendo imágenes Docker (sin cache)..."
        docker-compose build --no-cache
        print_success "Imágenes reconstruidas"
        ;;
        
    "logs")
        print_step "Mostrando logs de todos los servicios..."
        docker-compose logs -f --tail=100
        ;;
        
    "logs-backend")
        print_step "Mostrando logs del backend..."
        docker-compose logs -f --tail=100 backend
        ;;
        
    "logs-frontend")
        print_step "Mostrando logs del frontend..."
        docker-compose logs -f --tail=100 frontend
        ;;
        
    "shell-backend")
        print_step "Abriendo shell en contenedor backend..."
        docker-compose exec backend /bin/bash
        ;;
        
    "test")
        check_env
        print_step "Ejecutando tests en contenedor..."
        docker-compose run --rm backend pytest -v
        ;;
        
    "clean")
        print_step "Limpiando contenedores e imágenes..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "Limpieza completada"
        ;;
        
    "status")
        print_step "Estado de contenedores..."
        docker-compose ps
        echo ""
        print_step "Uso de recursos..."
        docker stats --no-stream
        ;;
        
    "full-stack")
        check_env
        print_step "Iniciando con frontend React..."
        docker-compose --profile full-stack up -d
        print_success "Full-stack iniciado"
        print_success "Frontend disponible en: http://localhost:3000"
        ;;
        
    "production")
        check_env
        print_step "Iniciando configuración de producción..."
        docker-compose --profile production up -d
        print_success "Configuración de producción iniciada"
        print_success "Nginx disponible en: http://localhost:80"
        ;;
        
    "help"|"--help"|"-h"|"")
        show_help
        ;;
        
    *)
        print_error "Comando no reconocido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac