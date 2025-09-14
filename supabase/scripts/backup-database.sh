#!/bin/bash

# ===================================================================
# SUPABASE DATABASE BACKUP SCRIPT
# ===================================================================
# Descripción: Script completo backup database con múltiples estrategias
# Autor: Database Operations Team - IPS Santa Helena del Valle  
# Fecha: 14 septiembre 2025
# Uso: ./backup-database.sh [--type=TYPE] [--compress] [--upload]
# ===================================================================

set -euo pipefail

# Configuración colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
BOLD='\033[1m'

# Variables globales
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="${SCRIPT_DIR}/../backups"
TEMP_DIR="/tmp/supabase_backup_${TIMESTAMP}"

# Opciones por defecto
BACKUP_TYPE="full"
COMPRESS=false
UPLOAD=false
RETENTION_DAYS=30

# Configuración database (ajustar según ambiente)
DB_HOST="127.0.0.1"
DB_PORT="54322"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="postgres"

# Configuración cloud storage (opcional)
CLOUD_PROVIDER=""  # "aws", "gcp", "azure"
CLOUD_BUCKET=""
CLOUD_REGION=""

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

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --type=*)
                BACKUP_TYPE="${1#*=}"
                shift
                ;;
            --compress)
                COMPRESS=true
                shift
                ;;
            --upload)
                UPLOAD=true
                shift
                ;;
            --retention=*)
                RETENTION_DAYS="${1#*=}"
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
    echo "Supabase Database Backup Script"
    echo ""
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "OPCIONES:"
    echo "  --type=TYPE         Tipo de backup (full|schema|data|incremental)"
    echo "  --compress          Comprimir backup con gzip"
    echo "  --upload            Subir backup a cloud storage"
    echo "  --retention=DAYS    Días de retención (default: 30)"
    echo "  -h, --help          Mostrar esta ayuda"
    echo ""
    echo "TIPOS DE BACKUP:"
    echo "  full               Backup completo (schema + data)"
    echo "  schema             Solo estructura (tablas, índices, funciones)"
    echo "  data               Solo datos (sin estructura)"
    echo "  incremental        Backup incremental (requiere backup base)"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0                              # Backup completo básico"
    echo "  $0 --type=schema --compress     # Backup schema comprimido"
    echo "  $0 --type=full --compress --upload  # Backup completo a cloud"
}

check_dependencies() {
    local missing_deps=()
    
    if ! command -v pg_dump &> /dev/null; then
        missing_deps+=("pg_dump (PostgreSQL client)")
    fi
    
    if ! command -v psql &> /dev/null; then
        missing_deps+=("psql (PostgreSQL client)")
    fi
    
    if [[ $COMPRESS == true ]] && ! command -v gzip &> /dev/null; then
        missing_deps+=("gzip (compression tool)")
    fi
    
    if [[ $UPLOAD == true ]] && [[ -z "$CLOUD_PROVIDER" ]]; then
        print_warning "Upload habilitado pero cloud provider no configurado"
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Dependencias faltantes:"
        printf '%s\n' "${missing_deps[@]}"
        exit 1
    fi
}

setup_directories() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$TEMP_DIR"
    print_info "Directorios de backup configurados"
}

cleanup() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
        print_info "Limpieza temporal completada"
    fi
}

# ===================================================================
# FUNCIONES DE BACKUP
# ===================================================================

test_database_connection() {
    print_info "Verificando conexión a database..."
    
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" &>/dev/null; then
        print_success "Conexión database exitosa"
    else
        print_error "No se puede conectar a la database"
        exit 1
    fi
    
    # Obtener información básica
    local db_size
    db_size=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" | xargs)
    print_info "Tamaño actual database: $db_size"
}

backup_full() {
    print_header "📦 BACKUP COMPLETO (SCHEMA + DATA)"
    
    local backup_file="${TEMP_DIR}/full_backup_${TIMESTAMP}.sql"
    local final_file="${BACKUP_DIR}/full_backup_${TIMESTAMP}.sql"
    
    print_info "Iniciando backup completo..."
    
    # Backup completo con opciones optimizadas
    PGPASSWORD=$DB_PASSWORD pg_dump \
        -h $DB_HOST \
        -p $DB_PORT \
        -U $DB_USER \
        -d $DB_NAME \
        --format=custom \
        --compress=6 \
        --verbose \
        --no-owner \
        --no-privileges \
        --exclude-schema=information_schema \
        --exclude-schema=pg_* \
        --file="$backup_file" \
        2>/dev/null
    
    if [[ $? -eq 0 ]]; then
        print_success "Backup completo generado exitosamente"
        
        # Convertir a SQL si se requiere compresión adicional
        if [[ $COMPRESS == true ]]; then
            local sql_file="${backup_file}.sql"
            PGPASSWORD=$DB_PASSWORD pg_restore --no-owner --no-privileges -f "$sql_file" "$backup_file"
            gzip "$sql_file"
            final_file="${BACKUP_DIR}/full_backup_${TIMESTAMP}.sql.gz"
            mv "${sql_file}.gz" "$final_file"
            rm "$backup_file"
            print_success "Backup comprimido: $(basename "$final_file")"
        else
            mv "$backup_file" "$final_file"
        fi
        
        print_backup_info "$final_file"
    else
        print_error "Error durante backup completo"
        exit 1
    fi
}

backup_schema_only() {
    print_header "🏗️ BACKUP SCHEMA (SOLO ESTRUCTURA)"
    
    local backup_file="${TEMP_DIR}/schema_backup_${TIMESTAMP}.sql"
    local final_file="${BACKUP_DIR}/schema_backup_${TIMESTAMP}.sql"
    
    print_info "Iniciando backup de schema..."
    
    PGPASSWORD=$DB_PASSWORD pg_dump \
        -h $DB_HOST \
        -p $DB_PORT \
        -U $DB_USER \
        -d $DB_NAME \
        --schema-only \
        --no-owner \
        --no-privileges \
        --exclude-schema=information_schema \
        --exclude-schema=pg_* \
        --file="$backup_file"
    
    if [[ $? -eq 0 ]]; then
        print_success "Backup de schema generado exitosamente"
        
        if [[ $COMPRESS == true ]]; then
            gzip "$backup_file"
            final_file="${BACKUP_DIR}/schema_backup_${TIMESTAMP}.sql.gz"
            mv "${backup_file}.gz" "$final_file"
        else
            mv "$backup_file" "$final_file"
        fi
        
        print_backup_info "$final_file"
    else
        print_error "Error durante backup de schema"
        exit 1
    fi
}

backup_data_only() {
    print_header "📊 BACKUP DATA (SOLO DATOS)"
    
    local backup_file="${TEMP_DIR}/data_backup_${TIMESTAMP}.sql"
    local final_file="${BACKUP_DIR}/data_backup_${TIMESTAMP}.sql"
    
    print_info "Iniciando backup de datos..."
    
    PGPASSWORD=$DB_PASSWORD pg_dump \
        -h $DB_HOST \
        -p $DB_PORT \
        -U $DB_USER \
        -d $DB_NAME \
        --data-only \
        --no-owner \
        --no-privileges \
        --exclude-schema=information_schema \
        --exclude-schema=pg_* \
        --exclude-table-data=audit_log \
        --exclude-table-data=pg_stat_statements \
        --file="$backup_file"
    
    if [[ $? -eq 0 ]]; then
        print_success "Backup de datos generado exitosamente"
        
        if [[ $COMPRESS == true ]]; then
            gzip "$backup_file"
            final_file="${BACKUP_DIR}/data_backup_${TIMESTAMP}.sql.gz"
            mv "${backup_file}.gz" "$final_file"
        else
            mv "$backup_file" "$final_file"
        fi
        
        print_backup_info "$final_file"
    else
        print_error "Error durante backup de datos"
        exit 1
    fi
}

backup_incremental() {
    print_header "🔄 BACKUP INCREMENTAL"
    
    # Buscar último backup completo
    local last_full_backup
    last_full_backup=$(find "$BACKUP_DIR" -name "full_backup_*.sql*" -type f | sort -r | head -n1)
    
    if [[ -z "$last_full_backup" ]]; then
        print_error "No se encontró backup completo base para incremental"
        print_info "Ejecuta primero: $0 --type=full"
        exit 1
    fi
    
    print_info "Backup base encontrado: $(basename "$last_full_backup")"
    
    # Para simplificar, backup incremental = backup de tablas modificadas recientement
    local backup_file="${TEMP_DIR}/incremental_backup_${TIMESTAMP}.sql"
    local final_file="${BACKUP_DIR}/incremental_backup_${TIMESTAMP}.sql"
    
    print_info "Iniciando backup incremental..."
    
    # Backup de tablas con modificaciones recientes (último día)
    PGPASSWORD=$DB_PASSWORD pg_dump \
        -h $DB_HOST \
        -p $DB_PORT \
        -U $DB_USER \
        -d $DB_NAME \
        --data-only \
        --no-owner \
        --no-privileges \
        --where="actualizado_en >= NOW() - INTERVAL '1 day' OR creado_en >= NOW() - INTERVAL '1 day'" \
        --table=pacientes \
        --table=atenciones \
        --table=atencion_materno_perinatal \
        --file="$backup_file" \
        2>/dev/null
    
    # Agregar metadatos del incremental
    echo "-- INCREMENTAL BACKUP METADATA" >> "$backup_file"
    echo "-- Base backup: $(basename "$last_full_backup")" >> "$backup_file"
    echo "-- Incremental date: $(date)" >> "$backup_file"
    echo "-- Records since: $(date -d '1 day ago')" >> "$backup_file"
    
    if [[ $COMPRESS == true ]]; then
        gzip "$backup_file"
        final_file="${BACKUP_DIR}/incremental_backup_${TIMESTAMP}.sql.gz"
        mv "${backup_file}.gz" "$final_file"
    else
        mv "$backup_file" "$final_file"
    fi
    
    print_success "Backup incremental completado"
    print_backup_info "$final_file"
}

# ===================================================================
# UTILIDADES BACKUP
# ===================================================================

print_backup_info() {
    local backup_file="$1"
    local file_size
    
    if [[ -f "$backup_file" ]]; then
        file_size=$(du -h "$backup_file" | cut -f1)
        print_info "Archivo generado: $(basename "$backup_file")"
        print_info "Tamaño: $file_size"
        print_info "Ubicación: $backup_file"
        
        # Verificar integridad (si es SQL)
        if [[ "$backup_file" == *.sql ]]; then
            local line_count
            line_count=$(wc -l < "$backup_file")
            print_info "Líneas SQL: $line_count"
        fi
    else
        print_error "Archivo de backup no encontrado: $backup_file"
    fi
}

upload_to_cloud() {
    if [[ $UPLOAD != true ]]; then
        return 0
    fi
    
    print_header "☁️ SUBIENDO BACKUP A CLOUD STORAGE"
    
    if [[ -z "$CLOUD_PROVIDER" ]]; then
        print_error "Cloud provider no configurado"
        return 1
    fi
    
    case "$CLOUD_PROVIDER" in
        "aws")
            upload_to_aws
            ;;
        "gcp")
            upload_to_gcp
            ;;
        "azure")
            upload_to_azure
            ;;
        *)
            print_error "Cloud provider no soportado: $CLOUD_PROVIDER"
            return 1
            ;;
    esac
}

upload_to_aws() {
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI no está instalado"
        return 1
    fi
    
    local backup_files
    backup_files=$(find "$BACKUP_DIR" -name "*_${TIMESTAMP}.*" -type f)
    
    for file in $backup_files; do
        local s3_path="s3://$CLOUD_BUCKET/database-backups/$(basename "$file")"
        print_info "Subiendo $(basename "$file") a S3..."
        
        if aws s3 cp "$file" "$s3_path" --region "$CLOUD_REGION"; then
            print_success "Subido exitosamente: $s3_path"
        else
            print_error "Error subiendo: $(basename "$file")"
        fi
    done
}

upload_to_gcp() {
    if ! command -v gsutil &> /dev/null; then
        print_error "Google Cloud SDK no está instalado"
        return 1
    fi
    
    local backup_files
    backup_files=$(find "$BACKUP_DIR" -name "*_${TIMESTAMP}.*" -type f)
    
    for file in $backup_files; do
        local gcs_path="gs://$CLOUD_BUCKET/database-backups/$(basename "$file")"
        print_info "Subiendo $(basename "$file") a GCS..."
        
        if gsutil cp "$file" "$gcs_path"; then
            print_success "Subido exitosamente: $gcs_path"
        else
            print_error "Error subiendo: $(basename "$file")"
        fi
    done
}

cleanup_old_backups() {
    print_header "🧹 LIMPIEZA BACKUPS ANTIGUOS"
    
    print_info "Eliminando backups mayores a $RETENTION_DAYS días..."
    
    local deleted_count=0
    while IFS= read -r -d '' file; do
        rm "$file"
        print_info "Eliminado: $(basename "$file")"
        ((deleted_count++))
    done < <(find "$BACKUP_DIR" -type f -name "*.sql*" -mtime +$RETENTION_DAYS -print0)
    
    if [[ $deleted_count -gt 0 ]]; then
        print_success "$deleted_count backups antiguos eliminados"
    else
        print_info "No hay backups antiguos para eliminar"
    fi
}

create_backup_manifest() {
    local manifest_file="${BACKUP_DIR}/backup_manifest_${TIMESTAMP}.json"
    
    cat > "$manifest_file" << EOF
{
    "backup_session": {
        "timestamp": "$TIMESTAMP",
        "date": "$(date -Iseconds)",
        "type": "$BACKUP_TYPE",
        "compressed": $COMPRESS,
        "uploaded": $UPLOAD,
        "database": {
            "host": "$DB_HOST",
            "port": "$DB_PORT",
            "name": "$DB_NAME",
            "size": "$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" | xargs)"
        },
        "files": [
EOF
    
    # Agregar archivos generados en esta sesión
    local first=true
    for file in $(find "$BACKUP_DIR" -name "*_${TIMESTAMP}.*" -type f); do
        if [[ $first == false ]]; then
            echo "," >> "$manifest_file"
        fi
        echo "            {" >> "$manifest_file"
        echo "                \"name\": \"$(basename "$file")\"," >> "$manifest_file"
        echo "                \"path\": \"$file\"," >> "$manifest_file"  
        echo "                \"size\": \"$(du -h "$file" | cut -f1)\"," >> "$manifest_file"
        echo "                \"checksum\": \"$(shasum -a 256 "$file" | cut -d' ' -f1)\"" >> "$manifest_file"
        echo "            }" >> "$manifest_file"
        first=false
    done
    
    cat >> "$manifest_file" << EOF
        ]
    }
}
EOF
    
    print_info "Manifest creado: $(basename "$manifest_file")"
}

# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

main() {
    parse_args "$@"
    
    print_header "💾 SUPABASE DATABASE BACKUP - IPS SANTA HELENA DEL VALLE"
    print_info "Tipo de backup: $BACKUP_TYPE"
    print_info "Compresión: $(if [[ $COMPRESS == true ]]; then echo "Habilitada"; else echo "Deshabilitada"; fi)"
    print_info "Upload cloud: $(if [[ $UPLOAD == true ]]; then echo "Habilitado"; else echo "Deshabilitado"; fi)"
    
    # Setup
    trap cleanup EXIT
    check_dependencies
    setup_directories
    test_database_connection
    
    # Ejecutar backup según tipo
    case "$BACKUP_TYPE" in
        "full")
            backup_full
            ;;
        "schema")
            backup_schema_only
            ;;
        "data")
            backup_data_only
            ;;
        "incremental")
            backup_incremental
            ;;
        *)
            print_error "Tipo de backup no válido: $BACKUP_TYPE"
            show_help
            exit 1
            ;;
    esac
    
    # Post-procesamiento
    create_backup_manifest
    upload_to_cloud
    cleanup_old_backups
    
    print_header "✅ BACKUP COMPLETADO EXITOSAMENTE"
    print_success "Backup session: $TIMESTAMP"
    print_info "Archivos disponibles en: $BACKUP_DIR"
    
    # Mostrar resumen final
    local backup_count
    backup_count=$(find "$BACKUP_DIR" -name "*_${TIMESTAMP}.*" -type f | wc -l)
    print_info "Archivos generados en esta sesión: $backup_count"
    
    local total_size
    total_size=$(find "$BACKUP_DIR" -name "*_${TIMESTAMP}.*" -type f -exec du -ch {} + | tail -n1 | cut -f1)
    print_info "Tamaño total backup session: $total_size"
}

# Ejecutar solo si es invocado directamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi