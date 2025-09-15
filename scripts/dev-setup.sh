#!/bin/bash
# =============================================================================
# Setup de Desarrollo - IPS Santa Helena del Valle
# Configuración completa del entorno de desarrollo local
# =============================================================================

set -e  # Salir en cualquier error

echo "🚀 Configurando entorno de desarrollo para IPS Santa Helena del Valle..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar dependencias del sistema
print_step "Verificando dependencias del sistema..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.10" ]]; then
    print_error "Se requiere Python 3.10+, versión actual: $PYTHON_VERSION"
    exit 1
fi
print_success "Python $PYTHON_VERSION ✓"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_warning "Node.js no está instalado (requerido para frontend)"
else
    NODE_VERSION=$(node -v)
    print_success "Node.js $NODE_VERSION ✓"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    print_warning "Docker no está instalado (opcional para containerización)"
else
    print_success "Docker ✓"
fi

# Check Supabase CLI
if ! command -v supabase &> /dev/null; then
    print_warning "Supabase CLI no está instalado"
    echo "  Instalación: npm install -g supabase"
else
    print_success "Supabase CLI ✓"
fi

# Configurar backend
print_step "Configurando backend Python..."

cd backend

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    print_step "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
print_step "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
print_step "Instalando dependencias de Python..."
pip install -r requirements.txt
print_success "Dependencias de Python instaladas"

# Verificar instalación con test básico
print_step "Verificando configuración del backend..."
if python -c "import fastapi, supabase, pydantic" 2>/dev/null; then
    print_success "Importaciones básicas exitosas"
else
    print_error "Error en dependencias básicas del backend"
    exit 1
fi

cd ..

# Configurar frontend (si existe)
if [ -d "frontend" ]; then
    print_step "Configurando frontend React..."
    cd frontend
    
    if [ -f "package.json" ]; then
        print_step "Instalando dependencias de Node.js..."
        npm install
        print_success "Dependencias de Node.js instaladas"
    fi
    
    cd ..
fi

# Configurar Supabase local
if command -v supabase &> /dev/null; then
    print_step "Configurando Supabase local..."
    
    cd supabase
    
    # Iniciar servicios de Supabase
    if ! supabase status &> /dev/null; then
        print_step "Iniciando servicios de Supabase..."
        supabase start
        print_success "Servicios de Supabase iniciados"
    else
        print_success "Servicios de Supabase ya están corriendo"
    fi
    
    # Mostrar información de conexión
    echo ""
    print_step "Información de Supabase local:"
    supabase status
    
    cd ..
fi

# Crear archivo .env de ejemplo si no existe
print_step "Configurando variables de entorno..."

if [ ! -f ".env" ]; then
    cat > .env << EOF
# =============================================================================
# Variables de Entorno - IPS Santa Helena del Valle
# Configuración de desarrollo local
# =============================================================================

# Supabase Configuration
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=debug
API_PREFIX=/api/v1

# Security
SECRET_KEY=your-secret-key-here-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# APM and Monitoring
APM_ENABLED=true
METRICS_ENABLED=true
SECURITY_AUDIT_ENABLED=true

# Frontend (React)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
EOF
    print_success "Archivo .env creado con configuración de desarrollo"
else
    print_warning "Archivo .env ya existe, no se sobreescribió"
fi

# Ejecutar tests para verificar configuración
print_step "Ejecutando tests de verificación..."

cd backend
source venv/bin/activate

if pytest tests/ -v --tb=short -q; then
    print_success "Tests de verificación pasaron correctamente"
else
    print_warning "Algunos tests fallaron, revisa la configuración"
fi

cd ..

# Resumen final
echo ""
echo "════════════════════════════════════════════════════════════════════════"
print_success "🎉 Configuración de desarrollo completada!"
echo ""
echo "📋 Próximos pasos:"
echo "  1. Revisar y ajustar .env con tus configuraciones"
echo "  2. Para iniciar el backend:"
echo "     cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  3. Para iniciar el frontend:"
echo "     cd frontend && npm start"
echo "  4. Para iniciar con Docker:"
echo "     docker-compose up --build"
echo ""
echo "🔗 URLs útiles:"
echo "  • Backend API: http://localhost:8000"
echo "  • Frontend: http://localhost:3000"
echo "  • Supabase Studio: http://127.0.0.1:54323"
echo "  • API Docs: http://localhost:8000/docs"
echo ""
echo "📚 Documentación:"
echo "  • Backend: backend/CLAUDE.md"
echo "  • Frontend: frontend/CLAUDE.md"
echo "  • Base de datos: supabase/CLAUDE.md"
echo "════════════════════════════════════════════════════════════════════════"