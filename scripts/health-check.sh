#!/bin/bash
# =============================================================================
# Health Check Script - IPS Santa Helena del Valle
# Verificación completa del estado del sistema
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

# Variables de configuración
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
SUPABASE_URL="http://127.0.0.1:54321"
TIMEOUT=10

# Función para verificar URL
check_url() {
    local url=$1
    local name=$2
    local timeout=${3:-$TIMEOUT}
    
    if curl -sSf --max-time $timeout "$url" >/dev/null 2>&1; then
        print_success "$name está disponible ($url)"
        return 0
    else
        print_error "$name no está disponible ($url)"
        return 1
    fi
}

# Función para verificar URL con respuesta JSON
check_json_endpoint() {
    local url=$1
    local name=$2
    local timeout=${3:-$TIMEOUT}
    
    response=$(curl -sSf --max-time $timeout "$url" 2>/dev/null) || {
        print_error "$name no responde ($url)"
        return 1
    }
    
    if echo "$response" | jq . >/dev/null 2>&1; then
        print_success "$name responde con JSON válido ($url)"
        return 0
    else
        print_warning "$name responde pero no es JSON válido ($url)"
        return 1
    fi
}

# Header
echo "🏥 Health Check - IPS Santa Helena del Valle"
echo "$(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════════════════════════════════════"

# Verificar dependencias
print_step "Verificando dependencias..."

if ! command -v curl &> /dev/null; then
    print_error "curl no está instalado"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    print_warning "jq no está instalado (recomendado para verificación JSON)"
fi

# Verificar servicios principales
print_step "Verificando servicios principales..."

backend_ok=false
frontend_ok=false
supabase_ok=false

# Backend API
if check_url "$BACKEND_URL" "Backend API"; then
    backend_ok=true
    
    # Verificar endpoints específicos
    print_step "Verificando endpoints del backend..."
    
    # Health check
    if check_json_endpoint "$BACKEND_URL/health/" "Health Check"; then
        # Obtener datos del health check
        health_data=$(curl -sSf "$BACKEND_URL/health/" 2>/dev/null)
        status=$(echo "$health_data" | jq -r '.status' 2>/dev/null || echo "unknown")
        
        if [ "$status" = "healthy" ]; then
            print_success "Sistema reporta estado: $status"
        else
            print_warning "Sistema reporta estado: $status"
        fi
    fi
    
    # API docs
    if check_url "$BACKEND_URL/docs" "API Documentation"; then
        print_success "Documentación de API disponible"
    fi
    
    # Root endpoint
    if check_json_endpoint "$BACKEND_URL/" "Root Endpoint"; then
        version=$(curl -sSf "$BACKEND_URL/" 2>/dev/null | jq -r '.version' 2>/dev/null || echo "unknown")
        print_success "Versión de API: $version"
    fi
    
    # Endpoints críticos
    check_json_endpoint "$BACKEND_URL/health/quick" "Quick Health Check"
    check_json_endpoint "$BACKEND_URL/health/metrics" "Metrics Endpoint"
else
    print_error "Backend no está disponible - verificar si está ejecutándose"
fi

# Frontend (si está corriendo)
print_step "Verificando frontend..."
if check_url "$FRONTEND_URL" "Frontend React"; then
    frontend_ok=true
else
    print_warning "Frontend no está corriendo (normal en modo solo-backend)"
fi

# Supabase local
print_step "Verificando Supabase local..."
if check_url "$SUPABASE_URL" "Supabase Local"; then
    supabase_ok=true
    
    # Verificar API REST
    if check_url "$SUPABASE_URL/rest/v1/" "Supabase REST API"; then
        print_success "API REST de Supabase disponible"
    fi
else
    print_warning "Supabase local no está corriendo (usar 'supabase start')"
fi

# Verificar base de datos (a través del backend)
if [ "$backend_ok" = true ]; then
    print_step "Verificando conectividad de base de datos..."
    
    if check_json_endpoint "$BACKEND_URL/health/database" "Database Health"; then
        db_data=$(curl -sSf "$BACKEND_URL/health/database" 2>/dev/null)
        db_status=$(echo "$db_data" | jq -r '.status' 2>/dev/null || echo "unknown")
        db_time=$(echo "$db_data" | jq -r '.response_time_ms' 2>/dev/null || echo "unknown")
        
        if [ "$db_status" = "healthy" ]; then
            print_success "Base de datos: $db_status (${db_time}ms)"
        else
            print_error "Base de datos: $db_status"
        fi
    fi
fi

# Verificar Docker (si está siendo usado)
print_step "Verificando contenedores Docker..."
if command -v docker &> /dev/null; then
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(backend|frontend|nginx)" >/dev/null 2>&1; then
        print_success "Contenedores Docker detectados:"
        docker ps --format "  • {{.Names}}: {{.Status}}" | grep -E "(backend|frontend|nginx)" || true
    else
        print_warning "No se detectaron contenedores Docker corriendo"
    fi
else
    print_warning "Docker no está disponible"
fi

# Tests de conectividad avanzados
if [ "$backend_ok" = true ]; then
    print_step "Ejecutando tests de conectividad avanzados..."
    
    # Test de endpoints CRUD básicos
    if check_url "$BACKEND_URL/pacientes/" "Endpoint Pacientes"; then
        print_success "Endpoints CRUD accesibles"
    fi
    
    # Test de autenticación (si está configurada)
    auth_response=$(curl -sSf -o /dev/null -w "%{http_code}" "$BACKEND_URL/health/security/access-levels" 2>/dev/null || echo "000")
    if [ "$auth_response" = "200" ]; then
        print_success "Sistema de seguridad respondiendo"
    elif [ "$auth_response" = "401" ] || [ "$auth_response" = "403" ]; then
        print_success "Sistema de seguridad activo (requiere autenticación)"
    else
        print_warning "Sistema de seguridad no responde correctamente"
    fi
fi

# Resumen final
echo ""
echo "════════════════════════════════════════════════════════════════════════"
print_step "Resumen del Health Check:"

total_checks=0
passed_checks=0

if [ "$backend_ok" = true ]; then
    print_success "Backend API: Operacional"
    ((passed_checks++))
else
    print_error "Backend API: No disponible"
fi
((total_checks++))

if [ "$supabase_ok" = true ]; then
    print_success "Supabase Local: Operacional"
    ((passed_checks++))
else
    print_warning "Supabase Local: No disponible"
fi
((total_checks++))

if [ "$frontend_ok" = true ]; then
    print_success "Frontend React: Operacional"
    ((passed_checks++))
else
    print_warning "Frontend React: No disponible"
fi
((total_checks++))

echo ""
echo "📊 Estado general: $passed_checks/$total_checks servicios operacionales"

if [ $passed_checks -eq $total_checks ]; then
    print_success "🎉 Todos los servicios están funcionando correctamente"
    exit 0
elif [ $passed_checks -gt 0 ]; then
    print_warning "⚠️  Algunos servicios necesitan atención"
    exit 1
else
    print_error "💥 Servicios críticos no están disponibles"
    exit 2
fi