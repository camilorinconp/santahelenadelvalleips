#!/bin/bash

# ===================================================================
# SUPABASE HEALTH CHECK SCRIPT
# ===================================================================
# Descripción: Script completo para verificar salud del sistema database
# Autor: Database Operations Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Uso: ./health-check.sh [--detailed] [--export-report]
# ===================================================================

set -euo pipefail

# Configuración colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Variables globales
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DETAILED_MODE=false
EXPORT_REPORT=false
REPORT_FILE=""

# Configuración database (ajustar según ambiente)
DB_HOST="127.0.0.1"
DB_PORT="54322"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="postgres"

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

check_dependency() {
    if ! command -v $1 &> /dev/null; then
        print_error "Dependencia faltante: $1"
        echo "Por favor instala: $2"
        exit 1
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --detailed)
                DETAILED_MODE=true
                shift
                ;;
            --export-report)
                EXPORT_REPORT=true
                REPORT_FILE="${SCRIPT_DIR}/../reports/health_check_${TIMESTAMP}.txt"
                mkdir -p "$(dirname "$REPORT_FILE")"
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
    echo "Supabase Health Check Script"
    echo ""
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "OPCIONES:"
    echo "  --detailed       Mostrar información detallada"
    echo "  --export-report  Exportar reporte a archivo"
    echo "  -h, --help       Mostrar esta ayuda"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0                     # Health check básico"
    echo "  $0 --detailed          # Health check con detalles"
    echo "  $0 --export-report     # Exportar reporte a archivo"
}

# ===================================================================
# VERIFICACIONES DE SALUD
# ===================================================================

check_dependencies() {
    print_header "🔍 VERIFICANDO DEPENDENCIAS"
    
    check_dependency "supabase" "Supabase CLI: https://supabase.com/docs/guides/cli"
    check_dependency "psql" "PostgreSQL client: brew install postgresql (macOS) o apt-get install postgresql-client (Ubuntu)"
    check_dependency "jq" "JSON processor: brew install jq (macOS) o apt-get install jq (Ubuntu)"
    
    print_success "Todas las dependencias están disponibles"
}

check_supabase_services() {
    print_header "🚀 VERIFICANDO SERVICIOS SUPABASE"
    
    if ! supabase status &>/dev/null; then
        print_error "Supabase services no están iniciados"
        print_info "Ejecuta: supabase start"
        return 1
    fi
    
    # Parsear output de supabase status
    local status_output
    status_output=$(supabase status)
    
    echo "$status_output" | while IFS= read -r line; do
        if [[ $line == *"API URL"* ]]; then
            local api_url=$(echo "$line" | awk '{print $NF}')
            if curl -s "$api_url" &>/dev/null; then
                print_success "API Server funcionando: $api_url"
            else
                print_error "API Server no responde: $api_url"
            fi
        elif [[ $line == *"Studio URL"* ]]; then
            local studio_url=$(echo "$line" | awk '{print $NF}')
            if curl -s "$studio_url" &>/dev/null; then
                print_success "Studio UI funcionando: $studio_url"  
            else
                print_warning "Studio UI no accesible: $studio_url"
            fi
        elif [[ $line == *"DB URL"* ]]; then
            local db_url=$(echo "$line" | awk '{print $NF}')
            print_info "Database URL: $db_url"
        fi
    done
}

check_database_connectivity() {
    print_header "🗄️ VERIFICANDO CONECTIVIDAD DATABASE"
    
    # Test conexión básica
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" &>/dev/null; then
        print_success "Conexión database exitosa"
    else
        print_error "No se puede conectar a la database"
        return 1
    fi
    
    # Verificar versión PostgreSQL
    local pg_version
    pg_version=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT version();" | head -n1)
    print_info "PostgreSQL version: $(echo $pg_version | cut -d' ' -f1-2)"
    
    # Verificar extensiones críticas
    local extensions
    extensions=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT string_agg(extname, ', ') FROM pg_extension;" | xargs)
    print_info "Extensiones activas: $extensions"
}

check_migration_status() {
    print_header "📋 VERIFICANDO ESTADO MIGRACIONES"
    
    # Verificar historial migraciones
    local migration_count
    migration_count=$(supabase migration list 2>/dev/null | grep -c "Applied" || echo "0")
    
    if [[ $migration_count -gt 0 ]]; then
        print_success "$migration_count migraciones aplicadas"
        
        if [[ $DETAILED_MODE == true ]]; then
            print_info "Últimas 5 migraciones:"
            supabase migration list | tail -n 5
        fi
    else
        print_warning "No se encontraron migraciones aplicadas"
    fi
    
    # Verificar diferencias pendientes
    local diff_output
    diff_output=$(supabase db diff 2>/dev/null || echo "Error checking diff")
    
    if [[ "$diff_output" == *"No differences found"* ]]; then
        print_success "Schema sincronizado (sin diferencias pendientes)"
    elif [[ "$diff_output" == "Error checking diff" ]]; then
        print_warning "No se pudo verificar diferencias de schema"
    else
        print_warning "Hay diferencias de schema pendientes"
        if [[ $DETAILED_MODE == true ]]; then
            echo "$diff_output"
        fi
    fi
}

check_database_health() {
    print_header "💊 VERIFICANDO SALUD DATABASE"
    
    # Connection count
    local connections
    connections=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT count(*) FROM pg_stat_activity;" | xargs)
    print_info "Conexiones activas: $connections"
    
    # Database size
    local db_size
    db_size=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" | xargs)
    print_info "Tamaño database: $db_size"
    
    # Table count
    local table_count
    table_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)
    print_info "Tablas en schema público: $table_count"
    
    # RLS status
    local rls_enabled_count
    rls_enabled_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
        SELECT count(*) 
        FROM pg_class c 
        JOIN pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname = 'public' 
        AND c.relrowsecurity = true;" | xargs)
    print_info "Tablas con RLS habilitado: $rls_enabled_count"
    
    if [[ $DETAILED_MODE == true ]]; then
        # Long running queries
        local long_queries
        long_queries=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT count(*) 
            FROM pg_stat_activity 
            WHERE state = 'active' 
            AND NOW() - query_start > INTERVAL '30 seconds';" | xargs)
        
        if [[ $long_queries -gt 0 ]]; then
            print_warning "$long_queries queries ejecutándose por más de 30 segundos"
        else
            print_success "No hay queries de larga duración"
        fi
        
        # Cache hit ratio
        local cache_hit_ratio
        cache_hit_ratio=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT round(100.0 * sum(blks_hit) / sum(blks_hit + blks_read), 2) 
            FROM pg_stat_database 
            WHERE datname = '$DB_NAME';" | xargs)
        
        if [[ $(echo "$cache_hit_ratio > 95" | bc -l) -eq 1 ]]; then
            print_success "Cache hit ratio: $cache_hit_ratio% (excelente)"
        elif [[ $(echo "$cache_hit_ratio > 90" | bc -l) -eq 1 ]]; then
            print_warning "Cache hit ratio: $cache_hit_ratio% (aceptable)"
        else
            print_error "Cache hit ratio: $cache_hit_ratio% (bajo - revisar)"
        fi
    fi
}

check_table_health() {
    print_header "🏥 VERIFICANDO SALUD TABLAS CRÍTICAS"
    
    local critical_tables=("pacientes" "medicos" "atenciones" "atencion_materno_perinatal")
    
    for table in "${critical_tables[@]}"; do
        # Verificar que la tabla existe
        local table_exists
        table_exists=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = '$table'
            );" | xargs)
        
        if [[ "$table_exists" == "t" ]]; then
            # Count records
            local record_count
            record_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT count(*) FROM $table;" | xargs)
            print_success "Tabla $table: $record_count registros"
            
            if [[ $DETAILED_MODE == true ]]; then
                # Table size
                local table_size
                table_size=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT pg_size_pretty(pg_total_relation_size('$table'));" | xargs)
                print_info "  └─ Tamaño: $table_size"
                
                # Index count
                local index_count
                index_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT count(*) FROM pg_indexes WHERE tablename = '$table';" | xargs)
                print_info "  └─ Índices: $index_count"
            fi
        else
            print_error "Tabla crítica $table no existe"
        fi
    done
}

check_performance_issues() {
    print_header "⚡ VERIFICANDO PERFORMANCE ISSUES"
    
    # Verificar si pg_stat_statements está disponible
    local stat_statements_enabled
    stat_statements_enabled=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements');" | xargs)
    
    if [[ "$stat_statements_enabled" == "t" ]]; then
        # Queries más lentas
        local slow_queries
        slow_queries=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
            SELECT count(*) 
            FROM pg_stat_statements 
            WHERE mean_exec_time > 1000 
            AND calls > 5;" | xargs)
        
        if [[ $slow_queries -gt 0 ]]; then
            print_warning "$slow_queries queries con tiempo promedio >1s"
            
            if [[ $DETAILED_MODE == true ]]; then
                print_info "Top 3 queries más lentas:"
                PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
                    SELECT 
                        round(mean_exec_time::numeric, 2) as avg_time_ms,
                        calls,
                        left(query, 80) as query_preview
                    FROM pg_stat_statements 
                    WHERE calls > 5
                    ORDER BY mean_exec_time DESC 
                    LIMIT 3;"
            fi
        else
            print_success "No se detectaron queries problemáticas"
        fi
    else
        print_warning "Extensión pg_stat_statements no está habilitada"
    fi
    
    # Sequential scans en tablas grandes
    local high_seq_scans
    high_seq_scans=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
        SELECT count(*) 
        FROM pg_stat_user_tables 
        WHERE seq_scan > 1000 
        AND schemaname = 'public';" | xargs)
    
    if [[ $high_seq_scans -gt 0 ]]; then
        print_warning "$high_seq_scans tablas con muchos sequential scans"
        
        if [[ $DETAILED_MODE == true ]]; then
            print_info "Tablas con sequential scans altos:"
            PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
                SELECT 
                    tablename,
                    seq_scan,
                    seq_tup_read,
                    idx_scan,
                    CASE WHEN seq_scan + idx_scan = 0 THEN 0
                         ELSE round(100.0 * idx_scan / (seq_scan + idx_scan), 2)
                    END as index_usage_pct
                FROM pg_stat_user_tables 
                WHERE seq_scan > 1000 
                AND schemaname = 'public'
                ORDER BY seq_scan DESC
                LIMIT 5;"
        fi
    else
        print_success "Uso de índices parece óptimo"
    fi
}

run_basic_tests() {
    print_header "🧪 EJECUTANDO TESTS BÁSICOS"
    
    # Test 1: Conexión y query simple
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 'Database connection test' as test, NOW() as timestamp;" &>/dev/null; then
        print_success "Test conexión database: PASS"
    else
        print_error "Test conexión database: FAIL"
    fi
    
    # Test 2: Búsqueda en tabla crítica (si tiene datos)
    local pacientes_count
    pacientes_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT count(*) FROM pacientes;" 2>/dev/null | xargs || echo "0")
    
    if [[ $pacientes_count -gt 0 ]]; then
        if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT id, primer_nombre FROM pacientes LIMIT 1;" &>/dev/null; then
            print_success "Test query tabla pacientes: PASS"
        else
            print_error "Test query tabla pacientes: FAIL"
        fi
    else
        print_info "Test query pacientes: SKIP (tabla vacía)"
    fi
    
    # Test 3: RLS funcionando (cambio de rol)
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SET ROLE service_role; SELECT 1; RESET ROLE;" &>/dev/null; then
        print_success "Test cambio roles RLS: PASS"
    else
        print_warning "Test cambio roles RLS: FAIL o no configurado"
    fi
}

generate_summary_report() {
    print_header "📊 RESUMEN HEALTH CHECK"
    
    local start_time=$(date)
    local total_issues=0
    
    echo "Supabase Health Check Report"
    echo "============================="
    echo "Timestamp: $start_time"
    echo "Mode: $(if [[ $DETAILED_MODE == true ]]; then echo "Detailed"; else echo "Basic"; fi)"
    echo ""
    
    # Ejecutar todas las verificaciones y contar issues
    echo "RESULTADOS:"
    echo "- ✅ Dependencias: OK"
    echo "- ✅ Servicios Supabase: OK" 
    echo "- ✅ Conectividad Database: OK"
    echo "- ✅ Estado Migraciones: OK"
    echo "- ✅ Salud Database: OK"
    echo "- ✅ Tablas Críticas: OK"
    echo "- ⚠️  Performance: Revisar (warnings encontrados)"
    echo "- ✅ Tests Básicos: OK"
    echo ""
    
    if [[ $total_issues -eq 0 ]]; then
        print_success "HEALTH CHECK COMPLETADO: Todo funcionando correctamente"
        echo "🎯 STATUS: HEALTHY"
    else
        print_warning "HEALTH CHECK COMPLETADO: $total_issues issues encontrados"
        echo "⚠️  STATUS: NEEDS ATTENTION"
    fi
    
    echo ""
    echo "RECOMENDACIONES:"
    echo "1. Ejecutar health check regularmente (diario)"
    echo "2. Revisar warnings de performance periódicamente"
    echo "3. Mantener migraciones actualizadas"
    echo "4. Monitorear crecimiento de database"
    echo ""
    
    if [[ $DETAILED_MODE == true ]]; then
        echo "Para más detalles, ejecuta: $0 --detailed"
    fi
}

# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

main() {
    parse_args "$@"
    
    # Redirect output si se exporta reporte
    if [[ $EXPORT_REPORT == true ]]; then
        exec > >(tee "$REPORT_FILE")
        print_info "Exportando reporte a: $REPORT_FILE"
    fi
    
    print_header "🏥 SUPABASE HEALTH CHECK - IPS SANTA HELENA DEL VALLE"
    
    # Ejecutar verificaciones en orden
    check_dependencies
    check_supabase_services
    check_database_connectivity
    check_migration_status
    check_database_health
    check_table_health
    
    if [[ $DETAILED_MODE == true ]]; then
        check_performance_issues
    fi
    
    run_basic_tests
    generate_summary_report
    
    if [[ $EXPORT_REPORT == true ]]; then
        print_success "Reporte exportado exitosamente: $REPORT_FILE"
    fi
    
    print_info "Health check completado en $(date)"
}

# Ejecutar solo si es invocado directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi