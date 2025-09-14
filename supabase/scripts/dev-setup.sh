#!/bin/bash

# ===================================================================
# SUPABASE DEVELOPMENT SETUP SCRIPT
# ===================================================================
# Descripción: Script automatizado para configurar entorno desarrollo
# Autor: Database Operations Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Uso: ./dev-setup.sh [--reset] [--with-data] [--skip-deps]
# ===================================================================

set -euo pipefail

# Configuración colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Variables globales
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Opciones
RESET_DB=false
WITH_SAMPLE_DATA=false
SKIP_DEPENDENCIES=false

# URLs y endpoints
SUPABASE_API_URL="http://127.0.0.1:54321"
SUPABASE_STUDIO_URL="http://127.0.0.1:54323"
SUPABASE_DB_URL="postgresql://postgres:postgres@127.0.0.1:54322/postgres"

# ===================================================================
# FUNCIONES AUXILIARES
# ===================================================================

print_header() {
    echo -e "\n${BOLD}${BLUE}============================================${NC}"
    echo -e "${BOLD}${BLUE} $1${NC}"
    echo -e "${BOLD}${BLUE}============================================${NC}\n"
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔄 $1${NC}"
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --reset)
                RESET_DB=true
                shift
                ;;
            --with-data)
                WITH_SAMPLE_DATA=true
                shift
                ;;
            --skip-deps)
                SKIP_DEPENDENCIES=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Opción desconocida: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    echo "Supabase Development Setup Script"
    echo ""
    echo "Usa este script para configurar rápidamente tu entorno de desarrollo."
    echo ""
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "OPCIONES:"
    echo "  --reset          Reset completo database (WARNING: borra datos)"
    echo "  --with-data      Cargar datos de ejemplo después del setup"
    echo "  --skip-deps      Saltear verificación de dependencias"
    echo "  -h, --help       Mostrar esta ayuda"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0                     # Setup básico"
    echo "  $0 --reset             # Reset y setup desde cero"
    echo "  $0 --with-data         # Setup con datos de ejemplo"
    echo "  $0 --reset --with-data # Reset completo + datos de ejemplo"
}

wait_for_user() {
    if [[ $RESET_DB == true ]]; then
        echo ""
        print_warning "⚠️  ADVERTENCIA: --reset borrará TODOS los datos actuales"
        print_warning "Esta operación es IRREVERSIBLE"
        echo ""
        read -p "¿Estás seguro? Escribe 'yes' para continuar: " confirm
        if [[ "$confirm" != "yes" ]]; then
            print_info "Operación cancelada por el usuario"
            exit 0
        fi
    fi
}

# ===================================================================
# VERIFICACIONES SISTEMA
# ===================================================================

check_system_requirements() {
    print_header "🔍 VERIFICANDO REQUISITOS SISTEMA"
    
    # Verificar OS
    local os_name
    os_name=$(uname -s)
    print_info "Sistema operativo: $os_name"
    
    # Verificar Docker si es necesario
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            print_success "Docker funcionando correctamente"
        else
            print_warning "Docker instalado pero no funcionando"
            print_info "Asegúrate de que Docker Desktop esté ejecutándose"
        fi
    else
        print_info "Docker no encontrado (puede no ser necesario)"
    fi
    
    # Verificar puertos disponibles
    local ports=(54321 54322 54323)
    for port in "${ports[@]}"; do
        if lsof -i :$port &> /dev/null; then
            print_warning "Puerto $port está en uso"
        else
            print_success "Puerto $port disponible"
        fi
    done
}

check_dependencies() {
    if [[ $SKIP_DEPENDENCIES == true ]]; then
        print_info "Saltando verificación de dependencias..."
        return 0
    fi
    
    print_header "📦 VERIFICANDO DEPENDENCIAS"
    
    local missing_deps=()
    
    # Supabase CLI (crítico)
    if ! command -v supabase &> /dev/null; then
        missing_deps+=("supabase-cli")
    else
        local supabase_version
        supabase_version=$(supabase --version 2>/dev/null | head -n1 || echo "unknown")
        print_success "Supabase CLI: $supabase_version"
    fi
    
    # PostgreSQL client (crítico)
    if ! command -v psql &> /dev/null; then
        missing_deps+=("postgresql-client")
    else
        local psql_version
        psql_version=$(psql --version | head -n1)
        print_success "PostgreSQL client: $psql_version"
    fi
    
    # Git (crítico)
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    else
        print_success "Git disponible"
    fi
    
    # Node.js (para frontend)
    if ! command -v node &> /dev/null; then
        print_warning "Node.js no encontrado (necesario para frontend)"
    else
        local node_version
        node_version=$(node --version)
        print_success "Node.js: $node_version"
    fi
    
    # Python (para backend)
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 no encontrado (necesario para backend)"
    else
        local python_version
        python_version=$(python3 --version)
        print_success "Python: $python_version"
    fi
    
    # Reportar dependencias faltantes
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Dependencias críticas faltantes:"
        printf '  - %s\n' "${missing_deps[@]}"
        echo ""
        print_info "Instrucciones de instalación:"
        
        for dep in "${missing_deps[@]}"; do
            case $dep in
                "supabase-cli")
                    echo "  - Supabase CLI: https://supabase.com/docs/guides/cli"
                    ;;
                "postgresql-client")
                    echo "  - PostgreSQL: brew install postgresql (macOS) o apt-get install postgresql-client (Ubuntu)"
                    ;;
                "git")
                    echo "  - Git: https://git-scm.com/downloads"
                    ;;
            esac
        done
        
        echo ""
        print_warning "Instala las dependencias y vuelve a ejecutar el script"
        exit 1
    fi
    
    print_success "Todas las dependencias críticas están disponibles"
}

# ===================================================================
# CONFIGURACIÓN SUPABASE
# ===================================================================

setup_supabase_services() {
    print_header "🚀 CONFIGURANDO SERVICIOS SUPABASE"
    
    # Verificar si Supabase ya está ejecutándose
    if supabase status &>/dev/null; then
        print_info "Supabase ya está ejecutándose"
        
        if [[ $RESET_DB == true ]]; then
            print_step "Deteniendo servicios para reset..."
            supabase stop
        else
            print_success "Servicios Supabase OK"
            return 0
        fi
    fi
    
    # Iniciar servicios Supabase
    print_step "Iniciando servicios Supabase..."
    if supabase start; then
        print_success "Servicios Supabase iniciados exitosamente"
    else
        print_error "Error iniciando servicios Supabase"
        print_info "Intenta ejecutar manualmente: supabase start"
        exit 1
    fi
    
    # Esperar a que los servicios estén completamente listos
    print_step "Esperando que los servicios estén listos..."
    sleep 5
    
    # Verificar conectividad
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s "$SUPABASE_API_URL/health" &>/dev/null; then
            print_success "API Server respondiendo"
            break
        fi
        
        print_info "Esperando API Server... (intento $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        print_error "API Server no respondió después de $max_attempts intentos"
        exit 1
    fi
}

apply_migrations() {
    print_header "📋 APLICANDO MIGRACIONES DATABASE"
    
    if [[ $RESET_DB == true ]]; then
        print_step "Reseteando database (aplicando todas las migraciones)..."
        
        if supabase db reset; then
            print_success "Database reseteada y migraciones aplicadas"
        else
            print_error "Error durante reset de database"
            exit 1
        fi
    else
        # Verificar si hay migraciones pendientes
        local diff_output
        diff_output=$(supabase db diff 2>/dev/null || echo "Error checking diff")
        
        if [[ "$diff_output" == *"No differences found"* ]]; then
            print_success "Database sincronizada (no hay migraciones pendientes)"
        else
            print_warning "Hay diferencias de schema detectadas"
            print_info "Considera ejecutar: supabase db reset"
        fi
    fi
    
    # Verificar estado final migraciones
    print_step "Verificando estado migraciones..."
    local migration_count
    migration_count=$(supabase migration list 2>/dev/null | grep -c "Applied" || echo "0")
    print_success "$migration_count migraciones aplicadas"
}

verify_database_structure() {
    print_header "🏗️ VERIFICANDO ESTRUCTURA DATABASE"
    
    # Contar tablas principales
    local table_count
    table_count=$(PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs || echo "0")
    print_info "Tablas en schema público: $table_count"
    
    # Verificar tablas críticas
    local critical_tables=("pacientes" "medicos" "atenciones" "atencion_materno_perinatal")
    local missing_tables=()
    
    for table in "${critical_tables[@]}"; do
        local table_exists
        table_exists=$(PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '$table');" 2>/dev/null | xargs || echo "f")
        
        if [[ "$table_exists" == "t" ]]; then
            print_success "Tabla $table existe"
        else
            missing_tables+=("$table")
        fi
    done
    
    if [[ ${#missing_tables[@]} -gt 0 ]]; then
        print_warning "Tablas críticas faltantes: ${missing_tables[*]}"
        print_info "Considera ejecutar migraciones: supabase db reset"
    fi
    
    # Verificar RLS
    local rls_count
    rls_count=$(PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -t -c "SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relrowsecurity = true;" 2>/dev/null | xargs || echo "0")
    print_info "Tablas con RLS habilitado: $rls_count"
}

# ===================================================================
# DATOS DE EJEMPLO
# ===================================================================

load_sample_data() {
    if [[ $WITH_SAMPLE_DATA != true ]]; then
        return 0
    fi
    
    print_header "📊 CARGANDO DATOS DE EJEMPLO"
    
    print_step "Generando datos de ejemplo..."
    
    # Crear datos de ejemplo básicos
    local sample_sql="${SCRIPT_DIR}/../temp/sample_data_${TIMESTAMP}.sql"
    mkdir -p "$(dirname "$sample_sql")"
    
    cat > "$sample_sql" << 'EOF'
-- Datos de ejemplo para desarrollo
-- IMPORTANTE: Solo usar en desarrollo, nunca en producción

BEGIN;

-- Insertar médicos de ejemplo
INSERT INTO medicos (id, nombre, especialidad, numero_licencia) VALUES
(gen_random_uuid(), 'Dr. María González', 'ginecologia_obstetricia', 'MED-001'),
(gen_random_uuid(), 'Dr. Carlos Rodríguez', 'medicina_general', 'MED-002'),
(gen_random_uuid(), 'Dra. Ana Martínez', 'pediatria', 'MED-003')
ON CONFLICT (numero_licencia) DO NOTHING;

-- Insertar pacientes de ejemplo
DO $$
DECLARE
    medico_id_1 UUID;
    medico_id_2 UUID;
    paciente_id_1 UUID;
    paciente_id_2 UUID;
BEGIN
    -- Obtener IDs de médicos
    SELECT id INTO medico_id_1 FROM medicos WHERE numero_licencia = 'MED-001' LIMIT 1;
    SELECT id INTO medico_id_2 FROM medicos WHERE numero_licencia = 'MED-002' LIMIT 1;
    
    -- Insertar pacientes
    INSERT INTO pacientes (id, tipo_documento, numero_documento, primer_nombre, primer_apellido, fecha_nacimiento, genero) VALUES
    (gen_random_uuid(), 'CC', '12345678', 'Laura', 'Silva', '1995-03-15', 'F'),
    (gen_random_uuid(), 'CC', '87654321', 'Carmen', 'Torres', '1988-07-22', 'F'),
    (gen_random_uuid(), 'CC', '11223344', 'José', 'Hernández', '1990-12-10', 'M')
    ON CONFLICT (numero_documento) DO NOTHING;
    
    -- Obtener ID de paciente para atenciones
    SELECT id INTO paciente_id_1 FROM pacientes WHERE numero_documento = '12345678' LIMIT 1;
    SELECT id INTO paciente_id_2 FROM pacientes WHERE numero_documento = '87654321' LIMIT 1;
    
    -- Insertar algunas atenciones de ejemplo si los pacientes existen
    IF paciente_id_1 IS NOT NULL AND medico_id_1 IS NOT NULL THEN
        -- Atención materno-perinatal
        INSERT INTO atenciones (id, paciente_id, medico_id, tipo_atencion, detalle_id, fecha_atencion)
        SELECT 
            gen_random_uuid(),
            paciente_id_1,
            medico_id_1,
            'materno_perinatal',
            gen_random_uuid(), -- Se actualizará con el ID real de la tabla de detalle
            NOW() - INTERVAL '7 days'
        ON CONFLICT DO NOTHING;
    END IF;
    
    RAISE NOTICE 'Datos de ejemplo insertados correctamente';
END $$;

COMMIT;
EOF
    
    # Aplicar datos de ejemplo
    print_step "Aplicando datos de ejemplo a database..."
    if PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -f "$sample_sql"; then
        print_success "Datos de ejemplo cargados exitosamente"
        
        # Verificar datos cargados
        local patient_count
        patient_count=$(PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -t -c "SELECT count(*) FROM pacientes;" 2>/dev/null | xargs || echo "0")
        print_info "Pacientes de ejemplo: $patient_count"
        
        local doctor_count
        doctor_count=$(PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -t -c "SELECT count(*) FROM medicos;" 2>/dev/null | xargs || echo "0")
        print_info "Médicos de ejemplo: $doctor_count"
    else
        print_warning "Error cargando datos de ejemplo (puede ser normal si las tablas no existen)"
    fi
    
    # Limpiar archivo temporal
    rm -f "$sample_sql"
}

# ===================================================================
# CONFIGURACIÓN AMBIENTE DESARROLLO
# ===================================================================

setup_environment_files() {
    print_header "📝 CONFIGURANDO ARCHIVOS AMBIENTE"
    
    # Crear .env para backend si no existe
    local backend_env="${PROJECT_ROOT}/../backend/.env"
    if [[ ! -f "$backend_env" ]]; then
        print_step "Creando .env para backend..."
        cat > "$backend_env" << EOF
# Supabase Configuration (Development)
SUPABASE_URL=${SUPABASE_API_URL}
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

# Database Direct Connection (Development)
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres

# Development Settings
ENVIRONMENT=development
DEBUG=true
EOF
        print_success "Archivo .env creado para backend"
    else
        print_info "Archivo .env ya existe para backend"
    fi
    
    # Crear .env.local para frontend si no existe
    local frontend_env="${PROJECT_ROOT}/../frontend/.env.local"
    if [[ ! -f "$frontend_env" ]]; then
        print_step "Creando .env.local para frontend..."
        cat > "$frontend_env" << EOF
# Supabase Configuration (Development)
REACT_APP_SUPABASE_URL=${SUPABASE_API_URL}
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0

# Development Settings
REACT_APP_ENVIRONMENT=development
EOF
        print_success "Archivo .env.local creado para frontend"
    else
        print_info "Archivo .env.local ya existe para frontend"
    fi
}

create_development_shortcuts() {
    print_header "⚡ CREANDO SHORTCUTS DESARROLLO"
    
    local shortcuts_dir="${PROJECT_ROOT}/shortcuts"
    mkdir -p "$shortcuts_dir"
    
    # Script para iniciar todo el stack
    cat > "${shortcuts_dir}/start-all.sh" << 'EOF'
#!/bin/bash
echo "🚀 Iniciando stack completo de desarrollo..."

# Iniciar Supabase
echo "Iniciando Supabase..."
supabase start

# Iniciar backend (en background)
echo "Iniciando backend FastAPI..."
(cd ../backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000) &
BACKEND_PID=$!

# Iniciar frontend (en background)
echo "Iniciando frontend React..."
(cd ../frontend && npm start) &
FRONTEND_PID=$!

echo ""
echo "✅ Stack completo iniciado:"
echo "  - Supabase Studio: http://127.0.0.1:54323"
echo "  - Backend API: http://127.0.0.1:8000"
echo "  - Frontend: http://localhost:3000"
echo ""
echo "Para detener todo, presiona Ctrl+C"

# Esperar y limpiar al salir
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; supabase stop" EXIT
wait
EOF
    
    # Script para reset rápido database
    cat > "${shortcuts_dir}/reset-db.sh" << 'EOF'
#!/bin/bash
echo "🔄 Reseteando database..."
supabase db reset
echo "✅ Database reseteada"
EOF
    
    # Script para backup rápido
    cat > "${shortcuts_dir}/quick-backup.sh" << 'EOF'
#!/bin/bash
echo "💾 Creando backup rápido..."
../scripts/backup-database.sh --type=full --compress
echo "✅ Backup completado"
EOF
    
    # Script para health check
    cat > "${shortcuts_dir}/health-check.sh" << 'EOF'
#!/bin/bash
echo "🏥 Ejecutando health check..."
../scripts/health-check.sh --detailed
EOF
    
    # Hacer ejecutables
    chmod +x "${shortcuts_dir}"/*.sh
    
    print_success "Shortcuts creados en: $shortcuts_dir/"
    print_info "  - start-all.sh: Iniciar stack completo"
    print_info "  - reset-db.sh: Reset rápido database"
    print_info "  - quick-backup.sh: Backup rápido"
    print_info "  - health-check.sh: Health check detallado"
}

# ===================================================================
# RESUMEN Y FINALIZACIÓN
# ===================================================================

print_final_summary() {
    print_header "🎉 SETUP COMPLETADO EXITOSAMENTE"
    
    print_success "Entorno de desarrollo configurado correctamente"
    echo ""
    
    print_info "📍 URLS IMPORTANTES:"
    echo "   • Supabase Studio: $SUPABASE_STUDIO_URL"
    echo "   • API URL: $SUPABASE_API_URL"
    echo "   • Database: $SUPABASE_DB_URL"
    echo ""
    
    print_info "🛠️ PRÓXIMOS PASOS:"
    echo "   1. Backend: cd ../backend && python -m uvicorn main:app --reload"
    echo "   2. Frontend: cd ../frontend && npm start"
    echo "   3. O usar shortcut: ./shortcuts/start-all.sh"
    echo ""
    
    print_info "📚 RECURSOS ÚTILES:"
    echo "   • Health Check: ./scripts/health-check.sh"
    echo "   • Backup: ./scripts/backup-database.sh"
    echo "   • Documentation: ./docs/01-overview/database-overview.md"
    echo ""
    
    if [[ $WITH_SAMPLE_DATA == true ]]; then
        print_info "📊 DATOS DE EJEMPLO CARGADOS:"
        echo "   • Revisa pacientes y médicos de ejemplo en Studio"
        echo "   • Credentials para testing disponibles en database"
    fi
    
    print_success "🚀 ¡Listo para desarrollar!"
}

# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

main() {
    local start_time
    start_time=$(date +%s)
    
    parse_args "$@"
    
    print_header "🏥 SUPABASE DEV SETUP - IPS SANTA HELENA DEL VALLE"
    print_info "Configurando entorno de desarrollo..."
    
    if [[ $RESET_DB == true ]]; then
        print_warning "Modo RESET activado - se borrarán todos los datos"
    fi
    
    if [[ $WITH_SAMPLE_DATA == true ]]; then
        print_info "Datos de ejemplo serán cargados"
    fi
    
    # Confirmación usuario
    wait_for_user
    
    # Ejecutar setup
    check_system_requirements
    check_dependencies
    setup_supabase_services
    apply_migrations
    verify_database_structure
    load_sample_data
    setup_environment_files
    create_development_shortcuts
    
    # Finalización
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    print_final_summary
    print_success "Setup completado en ${duration} segundos"
}

# Ejecutar solo si es invocado directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi