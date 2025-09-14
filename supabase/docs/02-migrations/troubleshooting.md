# 🔧 Migration Troubleshooting - Resolución Problemas CLI

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía resolución rápida problemas comunes Supabase CLI  
**📍 Audiencia:** Database Developers, DevOps Engineers, Backend Developers  

---

## 🚨 **Problemas Críticos y Soluciones**

### **🔥 CRITICAL: CLI Connection Failures**

#### **Síntomas:**
- `supabase db diff` no responde o timeout
- "connection refused" errors persistentes
- `supabase start` servicios no levantan correctamente
- Commands se cuelgan indefinidamente

#### **Diagnóstico:**
```bash
# Step 1: Verificar status servicios
supabase status

# Expected output si está sano:
# ✅ API URL: http://127.0.0.1:54321
# ✅ Studio URL: http://127.0.0.1:54323  
# ✅ DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres

# Step 2: Si servicios down o partially running
supabase logs -t api
supabase logs -t db
# Revisar logs para errores específicos
```

#### **Solución LEVEL 1: Reset Completo (90% efectividad)**
```bash
# 1. Stop all services
supabase stop

# 2. Clean state (si persisten problemas)
rm -rf .supabase/  # ⚠️ Elimina estado local, no migraciones

# 3. Restart fresh
supabase start

# 4. Reconstruir database desde migraciones
supabase db reset

# 5. Verificar que funciona
supabase db diff  # Debe mostrar "No differences found"
```

#### **Solución LEVEL 2: Port Conflicts**
```bash
# Verificar puertos ocupados
lsof -i :54321  # API
lsof -i :54322  # Database  
lsof -i :54323  # Studio

# Si hay conflictos, matar procesos
kill -9 [PID]

# Reiniciar Supabase
supabase start
```

#### **Solución LEVEL 3: Docker Issues**
```bash
# Si usa Docker backend
docker ps | grep supabase

# Stop containers si están stuck
docker stop $(docker ps -q --filter "name=supabase")

# Remove containers si están corrupted
docker rm $(docker ps -aq --filter "name=supabase")

# Restart Supabase (recrea containers)
supabase start
```

---

### **💥 CRITICAL: Migration Fails Midway**

#### **Síntomas:**
- Migration se aplica parcialmente
- Algunas tablas creadas, otras con error
- Estado database inconsistente
- `supabase db reset` falla

#### **Diagnóstico:**
```bash
# Verificar última migración aplicada
supabase migration list

# Expected output:
#     LOCAL      REMOTE     STATUS
# 0  20250913... 20250913... Applied
# 1  20250914... 20250914... Failed ❌  

# Verificar logs de error específico
supabase logs -t db | grep ERROR
```

#### **Solución LEVEL 1: Migration Repair**
```bash
# Marcar migración problemática como applied manualmente
supabase migration repair --status applied [timestamp_failed_migration]

# Ejemplo:
supabase migration repair --status applied 20250914143000

# Verificar reparación
supabase migration list

# Reset para validar consistency
supabase db reset
```

#### **Solución LEVEL 2: Manual SQL Fix**
```bash
# 1. Conectar directamente a database
supabase db connect

# 2. En psql, verificar estado actual
\dt  -- List todas las tablas
SELECT * FROM supabase_migrations.schema_migrations ORDER BY version;

# 3. Identificar qué se creó y qué falta
# Compare con migration file esperado

# 4. Ejecutar SQL faltante manualmente
\i supabase/migrations/[failed_migration_file].sql

# 5. Exit psql y reset para validar
\q
supabase db reset
```

#### **Solución LEVEL 3: Reset + Manual Recovery**
```bash
# ⚠️ CUIDADO: Solo si tienes backup de datos importantes

# 1. Backup datos críticos si existen
pg_dump -h 127.0.0.1 -p 54322 -U postgres postgres > backup_pre_reset.sql

# 2. Reset completo database  
supabase db reset

# 3. Si reset también falla, nuclear option:
supabase stop
rm -rf .supabase/
supabase start
supabase db reset

# 4. Restaurar datos críticos si era necesario
psql -h 127.0.0.1 -p 54322 -U postgres postgres < backup_pre_reset.sql
```

---

### **⚖️ MEDIUM: Schema Drift (Local ≠ Remote)**

#### **Síntomas:**
- `supabase db diff --linked` muestra diferencias inesperadas
- Local database no sincronizado con remote  
- Push/pull operations inconsistentes
- Backend API recibe schema errors

#### **Diagnóstico:**
```bash
# Verificar diferencias específicas
supabase db diff --linked > schema_differences.sql

# Revisar archivo generado
cat schema_differences.sql
# Analizar qué cambios son esperados vs inesperados
```

#### **Solución LEVEL 1: Remote is Source of Truth**
```bash
# ⚠️ PIERDE CAMBIOS LOCALES NO MIGRADOS

# 1. Pull remote schema to local
supabase db pull

# 2. Verificar sincronización
supabase db diff --linked
# Expected: "No differences found"

# 3. Si tenías cambios locales importantes, crearlos como nueva migración
supabase db diff -f recuperar_cambios_locales
```

#### **Solución LEVEL 2: Local is Source of Truth**  
```bash
# ⚠️ SOBREESCRIBE REMOTE - Solo si estás 100% seguro

# 1. Verificar que tienes los cambios correctos localmente
supabase db diff --linked

# 2. Force push (PELIGROSO en production)
supabase db push --force

# 3. Verificar sincronización
supabase db diff --linked
# Expected: "No differences found"
```

#### **Solución LEVEL 3: Manual Reconciliation**
```bash
# Para casos complejos donde ambos tienen cambios válidos

# 1. Crear backup de local
pg_dump -h 127.0.0.1 -p 54322 -U postgres postgres > local_backup.sql

# 2. Pull remote
supabase db pull

# 3. Crear migración con diferencias de local backup
supabase db diff -f merge_local_remote_changes

# 4. Editar migración manualmente para merge inteligente
# 5. Test migración
supabase db reset
```

---

### **🛡️ MEDIUM: RLS Policy Blocks Backend**

#### **Síntomas:**
- Backend FastAPI recibe "permission denied" errors
- CRUD operations fallan con RLS errors
- `service_role` parece no tener acceso completo
- Frontend no puede cargar datos

#### **Diagnóstico:**
```bash
# Conectar como service_role y test
supabase db connect

# En psql:
SET ROLE service_role;
SELECT * FROM pacientes LIMIT 1;  -- Debe funcionar

SET ROLE authenticated;
SELECT * FROM pacientes LIMIT 1;  -- Puede fallar según policy

SET ROLE anon;  
SELECT * FROM pacientes LIMIT 1;  -- Debe fallar (expected)
```

#### **Solución LEVEL 1: Fix Service Role Policies**
```sql
-- En psql o Studio SQL Editor

-- Verificar policies existentes
SELECT schemaname, tablename, policyname, cmd, roles 
FROM pg_policies 
WHERE tablename = '[tabla_problematica]';

-- Crear/fix policy para service_role
CREATE POLICY "service_role_full_access_[tabla]" ON [tabla_problematica]
FOR ALL USING (auth.role() = 'service_role');

-- Grant table permissions
GRANT ALL ON [tabla_problematica] TO service_role;
```

#### **Solución LEVEL 2: Reset RLS Configuration**
```sql
-- Para tabla específica

-- Disable RLS temporalmente
ALTER TABLE [tabla_problematica] DISABLE ROW LEVEL SECURITY;

-- Drop all existing policies
DROP POLICY IF EXISTS [policy_name] ON [tabla_problematica];

-- Re-enable RLS
ALTER TABLE [tabla_problematica] ENABLE ROW LEVEL SECURITY;

-- Create clean policies
CREATE POLICY "service_role_access" ON [tabla_problematica]
FOR ALL TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "authenticated_read" ON [tabla_problematica]  
FOR SELECT TO authenticated
USING (true);
```

#### **Solución LEVEL 3: Global RLS Reset**
```bash
# Si múltiples tablas tienen problemas RLS

# Crear migración de limpieza RLS
supabase db diff -f reset_all_rls_policies

# En la migración, usar script global:
```
```sql
DO $$
DECLARE
    table_record RECORD;
BEGIN
    -- Para cada tabla con RLS
    FOR table_record IN 
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
        AND tablename != 'supabase_migrations'
    LOOP
        -- Grant service_role access
        EXECUTE format('GRANT ALL ON %I TO service_role', table_record.tablename);
        
        -- Create service_role policy si no existe
        EXECUTE format('
            CREATE POLICY IF NOT EXISTS "service_role_full_%I" ON %I
            FOR ALL USING (auth.role() = ''service_role'')
        ', table_record.tablename, table_record.tablename);
        
        RAISE NOTICE 'Fixed RLS for table: %', table_record.tablename;
    END LOOP;
END $$;
```

---

### **⚠️ LOW: Performance Issues**

#### **Síntomas:**
- Queries muy lentas (>1s para operaciones simples)
- `supabase db reset` toma mucho tiempo
- Studio UI slow loading tables
- Backend timeouts en operaciones database

#### **Diagnóstico:**
```sql
-- En psql, identificar queries lentas
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- Verificar índices missing
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats 
WHERE schemaname = 'public'
ORDER BY tablename, attname;

-- Tables más grandes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### **Solución LEVEL 1: Add Missing Indexes**
```sql
-- Índices para foreign keys (críticos)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_atenciones_paciente_id 
ON atenciones(paciente_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_atencion_mp_atencion_id
ON atencion_materno_perinatal(atencion_id);

-- Índices para búsquedas frecuentes  
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pacientes_documento
ON pacientes(numero_documento);

-- Índices parciales para filtros comunes
CREATE INDEX IF NOT EXISTS idx_atenciones_recientes 
ON atenciones(fecha_atencion)
WHERE fecha_atencion >= CURRENT_DATE - INTERVAL '90 days';
```

#### **Solución LEVEL 2: Query Optimization**
```sql
-- Usar EXPLAIN ANALYZE para debug
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM atenciones a
JOIN pacientes p ON a.paciente_id = p.id  
WHERE p.numero_documento = '12345678';

-- Optimizar con índices compuestos si es necesario
CREATE INDEX IF NOT EXISTS idx_pacientes_atencion_lookup
ON pacientes(numero_documento) INCLUDE (id, primer_nombre, primer_apellido);
```

---

## 📋 **Quick Diagnostic Commands**

### **🔍 Health Check Completo:**
```bash
#!/bin/bash
# scripts/health-check.sh

echo "🏥 === SUPABASE HEALTH CHECK ==="

# 1. Servicios status
echo "1. Checking services..."
supabase status

# 2. Database connectivity  
echo "2. Testing database connection..."
supabase db connect -c "SELECT 'Database OK' as status;"

# 3. Migrations status
echo "3. Checking migrations..."
supabase migration list

# 4. Schema consistency
echo "4. Checking schema consistency..."
supabase db diff

# 5. Basic query test
echo "5. Testing basic queries..."
supabase db connect -c "SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = 'public';"

echo "✅ Health check completed"
```

### **📊 Performance Diagnostics:**
```sql
-- Quick performance check queries

-- 1. Top 5 largest tables
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 5;

-- 2. Missing indexes (foreign keys sin index)
SELECT conrelid::regclass AS table_name, conname AS constraint_name, 
       pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint 
WHERE contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i WHERE i.indrelid = conrelid 
    AND (i.indkey::int[])[0] = conkey[1]
  );

-- 3. RLS policies summary
SELECT schemaname, tablename, COUNT(*) as policy_count
FROM pg_policies 
WHERE schemaname = 'public'
GROUP BY schemaname, tablename
ORDER BY tablename;
```

---

## 🚀 **Recovery Procedures**

### **🆘 Emergency Recovery: Complete Reset**
```bash
#!/bin/bash
# scripts/emergency-recovery.sh
# ⚠️ USE ONLY IN EMERGENCIES - LOSES LOCAL STATE

echo "🚨 EMERGENCY RECOVERY PROCEDURE"
echo "This will reset everything. Are you sure? (yes/no)"
read confirmation

if [ "$confirmation" = "yes" ]; then
    echo "1. Stopping services..."
    supabase stop
    
    echo "2. Removing local state..."
    rm -rf .supabase/
    
    echo "3. Starting fresh..."  
    supabase start
    
    echo "4. Rebuilding from migrations..."
    supabase db reset
    
    echo "5. Verifying health..."
    supabase status
    supabase migration list
    
    echo "✅ Emergency recovery completed"
else
    echo "❌ Recovery cancelled"
    exit 1
fi
```

### **💾 Backup Before Major Changes**
```bash
#!/bin/bash
# scripts/backup-before-migration.sh

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "📦 Creating backup..."

# Schema backup
pg_dump -h 127.0.0.1 -p 54322 -U postgres --schema-only postgres > $BACKUP_DIR/schema_backup.sql

# Data backup (critical tables only)
pg_dump -h 127.0.0.1 -p 54322 -U postgres --data-only --table=pacientes --table=medicos postgres > $BACKUP_DIR/data_backup.sql

# Migration files backup  
cp -r supabase/migrations/ $BACKUP_DIR/migrations_backup/

echo "✅ Backup completed: $BACKUP_DIR"
echo "Restore command: psql -h 127.0.0.1 -p 54322 -U postgres postgres < $BACKUP_DIR/schema_backup.sql"
```

---

## 📞 **Escalation Procedures**

### **🆘 When to Escalate:**
1. **Data loss occurred** en production
2. **Multiple migration failures** no resueltos con reset
3. **RLS completely broken** impacting production API  
4. **Performance degradation** >10x slower than normal
5. **CLI completely non-functional** después de todos los troubleshoots

### **📋 Information to Collect Before Escalation:**
```bash
# Run este script y adjuntar output
#!/bin/bash
# scripts/escalation-info.sh

echo "=== ESCALATION INFORMATION COLLECTION ==="
echo "Date: $(date)"
echo "System: $(uname -a)"
echo ""

echo "=== Supabase CLI Version ==="
supabase --version

echo "=== Service Status ==="  
supabase status

echo "=== Recent Migrations ==="
supabase migration list | tail -10

echo "=== Recent Logs ==="
echo "--- DB Logs ---"
supabase logs -t db | tail -20
echo "--- API Logs ---"  
supabase logs -t api | tail -20

echo "=== Database Stats ==="
supabase db connect -c "
SELECT 
    COUNT(*) as total_tables,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'public') as total_columns,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public') as total_policies
FROM information_schema.tables WHERE table_schema = 'public';
"

echo "=== Disk Space ==="
df -h

echo "=== Process List ==="
ps aux | grep supabase
```

### **📞 Contact Information:**
- **Database Team Lead:** [TBD]
- **DevOps Team:** [TBD]  
- **Supabase Support:** https://supabase.com/support
- **Emergency Escalation:** [TBD]

---

## 🎯 **Prevention Best Practices**

### **✅ Daily Development:**
- Siempre `supabase db reset` después de crear migración
- Test migraciones localmente antes de push
- Backup antes de cambios major
- Use descriptive migration names
- Document complex changes thoroughly

### **✅ Weekly Maintenance:**  
- Run `supabase stop && supabase start` para clean restart
- Review migration history con `supabase migration list`
- Check logs para warnings: `supabase logs -t db`
- Monitor database size y performance

### **✅ Before Production Deploy:**
- Complete health check script
- Backup production database
- Test migration on staging first
- Have rollback plan ready
- Monitor deployment closely

---

**🔧 Troubleshooting guide maintained para minimize downtime**  
**👥 Maintained by:** Database Operations Team  
**🚨 Emergency contact:** Database Team Lead  
**📊 Success metric:** <5 min resolution time para issues comunes