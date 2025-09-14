# 🚀 Migration Guide - Database Workflow Completo

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía completa workflow migraciones database PostgreSQL + Supabase  
**📍 Audiencia:** Database Developers, Backend Developers, DevOps Engineers  

---

## 🎯 **Filosofía de Migraciones**

### **🏗️ Principios Fundamentales:**
1. **Atomic Operations:** Cada migración completa o rollback completo
2. **Forward-only Evolution:** Schema evoluciona sin breaking changes
3. **Data Preservation:** Nunca perder datos en production
4. **Descriptive History:** Cada cambio documentado y rastreable
5. **Local-first Development:** Probar localmente antes que production

---

## 📋 **Workflow Completo Migraciones**

### **🔄 CICLO DESARROLLO → PRODUCTION**

#### **FASE 1: Setup Local Environment**
```bash
# 1. Verificar Supabase CLI instalado
supabase --version

# 2. Iniciar servicios locales
supabase start

# 3. Verificar estado servicios
supabase status
# Expected output:
# API URL: http://127.0.0.1:54321
# Studio URL: http://127.0.0.1:54323  
# DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres

# 4. Verificar conexión database
supabase db connect
# Test basic SQL: \dt (list tables)
# Exit: \q
```

#### **FASE 2: Desarrollo de Schema Changes**

**MÉTODO A: UI-driven Development (Recomendado para exploración)**
```bash
# 1. Acceder Supabase Studio local
open http://127.0.0.1:54323

# 2. Realizar cambios en UI:
#    - Table Editor: Crear/modificar tablas
#    - SQL Editor: Ejecutar SQL directo
#    - Database: Explore schema actual

# 3. Generar migración desde diff
supabase db diff -f descripcion_clara_del_cambio

# Output esperado: 
# Created new migration at supabase/migrations/[timestamp]_descripcion_clara_del_cambio.sql
```

**MÉTODO B: Code-first Development (Recomendado para producción)**
```bash
# 1. Crear archivo migración manual
touch supabase/migrations/$(date +%Y%m%d%H%M%S)_descripcion_clara.sql

# 2. Escribir SQL siguiendo template (ver sección Template)

# 3. Aplicar migración localmente
supabase db reset  # ¡Reconstruye desde todas las migraciones!
```

#### **FASE 3: Validación Local (CRÍTICO)**
```bash
# 1. Reset database completo con nuevas migraciones
supabase db reset

# 2. Verificar que no hay errores en logs
supabase logs -t db

# 3. Testing desde backend (si aplica)
cd ../backend
pytest tests/test_database_integration.py -v

# 4. Validar schema consistency
supabase db lint

# 5. Manual testing en Studio
# - Verificar tablas creadas correctamente
# - Test inserción/actualización datos
# - Verificar constraints y índices
```

#### **FASE 4: Deploy Production (¡CUIDADO!)**
```bash
# 1. Verificar proyecto linkado
supabase projects list
supabase link --project-ref [tu-project-ref]

# 2. Comparar local vs remote
supabase db diff --linked
# Output: Debe mostrar exactamente los cambios que queremos aplicar

# 3. Deploy a production (IRREVERSIBLE)
supabase db push

# 4. Verificar deployment exitoso
supabase db diff --linked  
# Output esperado: "No schema differences found"
```

---

## 📄 **Template Migración Estándar**

### **Estructura Template Completa:**
```sql
-- =============================================
-- MIGRACIÓN: [TÍTULO DESCRIPTIVO EN MAYÚSCULAS]
-- =============================================
-- Descripción: [Explicación detallada del propósito y contexto]
-- Fecha: [DD mes AAAA]
-- Autor: [Nombre/Equipo]
-- Impacto: [Descripción del impacto en aplicación/usuarios]
-- Rollback: [Instrucciones de rollback si es posible]
-- =============================================

BEGIN;

-- =============================================
-- 1. VERIFICACIONES PRE-EJECUCIÓN
-- =============================================
-- Verificar que prerequisitos estén en su lugar

DO $pre_check$
DECLARE
    table_exists BOOLEAN;
    constraint_exists BOOLEAN;
BEGIN
    -- Ejemplo: Verificar que tabla prerequisito existe
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'prerequisito_tabla'
    ) INTO table_exists;
    
    IF NOT table_exists THEN
        RAISE EXCEPTION 'Prerequisito falta: prerequisito_tabla debe existir antes de esta migración';
    END IF;
    
    RAISE NOTICE '✅ Pre-checks passed: Prerequisitos verificados';
END;
$pre_check$;

-- =============================================
-- 2. CAMBIOS PRINCIPALES DE SCHEMA
-- =============================================

-- 2.1. CREAR NUEVAS TABLAS (si aplica)
CREATE TABLE IF NOT EXISTS nueva_tabla (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campo_requerido TEXT NOT NULL,
    campo_opcional TEXT,
    
    -- Campos auditoría estándar
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints business logic
    CONSTRAINT check_campo_valido CHECK (campo_requerido != '')
);

-- 2.2. MODIFICAR TABLAS EXISTENTES (si aplica)
-- IMPORTANTE: Usar IF NOT EXISTS para operaciones idempotentes
ALTER TABLE tabla_existente 
ADD COLUMN IF NOT EXISTS nueva_columna TEXT;

-- 2.3. CREAR ÍNDICES PARA PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_nueva_tabla_campo_frecuente 
ON nueva_tabla(campo_requerido) 
WHERE campo_requerido IS NOT NULL;

-- =============================================
-- 3. DATOS INICIALES / SEED DATA
-- =============================================
-- Insertar datos críticos que la aplicación necesita

INSERT INTO nueva_tabla (campo_requerido, campo_opcional) VALUES
('valor_critico_1', 'descripción'),
('valor_critico_2', 'descripción')
ON CONFLICT (campo_requerido) DO UPDATE SET
    campo_opcional = EXCLUDED.campo_opcional,
    actualizado_en = NOW();

-- =============================================
-- 4. ROW LEVEL SECURITY (RLS)
-- =============================================
-- IMPORTANTE: Configurar RLS para todas las tablas sensibles

-- Habilitar RLS
ALTER TABLE nueva_tabla ENABLE ROW LEVEL SECURITY;

-- Policy para service_role (backend FastAPI)
CREATE POLICY "service_role_full_access_nueva_tabla" ON nueva_tabla
FOR ALL USING (auth.role() = 'service_role');

-- Policy para authenticated users
CREATE POLICY "authenticated_read_nueva_tabla" ON nueva_tabla  
FOR SELECT USING (auth.role() = 'authenticated');

-- =============================================
-- 5. TRIGGERS Y FUNCIONES (si aplica)
-- =============================================

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION trigger_actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger
CREATE TRIGGER trigger_nueva_tabla_timestamp
    BEFORE UPDATE ON nueva_tabla
    FOR EACH ROW EXECUTE FUNCTION trigger_actualizar_timestamp();

-- =============================================
-- 6. COMENTARIOS DOCUMENTACIÓN
-- =============================================

COMMENT ON TABLE nueva_tabla IS 
'[Descripción completa del propósito de la tabla y contexto business]';

COMMENT ON COLUMN nueva_tabla.campo_requerido IS 
'[Descripción del campo, valores válidos, constraints]';

-- =============================================
-- 7. VERIFICACIONES POST-EJECUCIÓN
-- =============================================

DO $verification$
DECLARE
    tabla_count INTEGER;
    registro_count INTEGER;
    indice_count INTEGER;
BEGIN
    -- Verificar tabla creada
    SELECT COUNT(*) INTO tabla_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'nueva_tabla';
    
    -- Verificar registros insertados
    SELECT COUNT(*) INTO registro_count FROM nueva_tabla;
    
    -- Verificar índices creados
    SELECT COUNT(*) INTO indice_count
    FROM pg_indexes 
    WHERE tablename = 'nueva_tabla';
    
    -- Log resultados
    RAISE NOTICE '=== VERIFICACIÓN POST-MIGRACIÓN ===';
    RAISE NOTICE 'Tablas creadas: %', tabla_count;
    RAISE NOTICE 'Registros insertados: %', registro_count;
    RAISE NOTICE 'Índices creados: %', indice_count;
    
    IF tabla_count > 0 AND registro_count > 0 THEN
        RAISE NOTICE '✅ SUCCESS: Migración aplicada exitosamente';
    ELSE
        RAISE EXCEPTION '❌ ERROR: Migración falló verificación post-ejecución';
    END IF;
    
    RAISE NOTICE '================================';
END;
$verification$;

COMMIT;

-- =============================================
-- NOTAS PARA ROLLBACK (si es posible)
-- =============================================
/*
ROLLBACK INSTRUCTIONS (solo para emergencias):

1. Crear migración reversa:
   supabase db diff -f rollback_[nombre_migración]

2. SQL rollback (CUIDADO - puede perder datos):
   DROP TABLE IF EXISTS nueva_tabla CASCADE;
   
3. Alternativa segura:
   ALTER TABLE nueva_tabla RENAME TO nueva_tabla_deprecated;
   -- Mantener datos pero desactivar uso
   
IMPACTO ROLLBACK:
- [Describir qué funcionalidad se verá afectada]
- [Describir qué datos se podrían perder]
- [Describir pasos adicionales necesarios en aplicación]
*/
```

---

## 🏷️ **Convenciones Naming**

### **Archivos Migración:**
```bash
# Formato estricto:
YYYYMMDDHHMMSS_descripcion_clara_accion.sql

# Ejemplos BUENOS:
20250914143000_crear_catalogo_ocupaciones_pedt.sql
20250914150000_agregar_indices_performance_pacientes.sql  
20250914160000_fix_rls_policies_atencion_materno_perinatal.sql

# Ejemplos MALOS:
migration1.sql                    # ❌ No descriptivo
add_table.sql                     # ❌ No timestamp
20250914_stuff.sql               # ❌ No descriptivo
```

### **Descripción Commits:**
```bash
# Git commit format:
git commit -m "feat(db): Descripción clara migración

- Detalle específico cambio 1
- Detalle específico cambio 2  
- Contexto business si es relevante

Migration: 20250914143000_descripcion_clara"
```

---

## ⚠️ **Troubleshooting Common Issues**

### **🔧 Problema: CLI Connection Failures**
```bash
# Síntomas:
# - supabase db diff no responde
# - "connection refused" errors
# - Comandos timeout

# Solución 1: Reset completo (RECOMENDADA)
supabase stop
supabase start
supabase db reset  # Reconstruye local desde migraciones

# Solución 2: Check servicios
supabase status
# Si algún servicio down: restart específico

# Solución 3: Clean state
rm -rf .supabase  # ⚠️ CUIDADO: Borra estado local
supabase start
```

### **🔧 Problema: Migration Fails Midway**
```bash
# Síntomas:
# - Migration se aplica parcialmente
# - Algunas tablas creadas, otras no
# - Estado inconsistente

# Solución: Migration repair
supabase migration repair --status applied [timestamp_failed_migration]

# Luego: Reset para validar
supabase db reset
```

### **🔧 Problema: Schema Drift (Local ≠ Remote)**
```bash
# Síntomas:  
# - supabase db diff --linked muestra diferencias inesperadas
# - Local y remote no sincronizados

# Diagnóstico:
supabase db diff --linked > schema_differences.sql
cat schema_differences.sql  # Revisar diferencias

# Solución 1: Reset local to match remote
supabase db pull  # ⚠️ PIERDE CAMBIOS LOCALES NO MIGRADOS

# Solución 2: Force local to remote (si local es correcto)
supabase db push --force-push  # ⚠️ SOBREESCRIBE REMOTE
```

### **🔧 Problema: RLS Policy Blocks**
```bash
# Síntomas:
# - Backend recibe permission denied
# - Queries fallan con RLS errors

# Diagnóstico:
# En psql o Studio SQL Editor:
SET ROLE service_role;
SELECT * FROM tabla_problematica;  -- Debe funcionar

SET ROLE authenticated;  
SELECT * FROM tabla_problematica;  -- Puede fallar según policy

# Solución: Fix policies
CREATE POLICY "fix_policy" ON tabla_problematica
FOR ALL USING (auth.role() = 'service_role');
```

---

## 📊 **Best Practices Performance**

### **🚀 Índices Strategy:**
```sql
-- Índices para columnas de búsqueda frecuente
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pacientes_numero_documento 
ON pacientes(numero_documento);

-- Índices parciales para queries con WHERE conditions
CREATE INDEX IF NOT EXISTS idx_atenciones_activas 
ON atenciones(fecha_atencion) 
WHERE fecha_atencion >= CURRENT_DATE - INTERVAL '30 days';

-- Índices compuestos para queries multi-columna
CREATE INDEX IF NOT EXISTS idx_atenciones_lookup 
ON atenciones(paciente_id, tipo_atencion, fecha_atencion);
```

### **🔍 Query Optimization:**
```sql
-- Usar EXPLAIN ANALYZE para identificar bottlenecks
EXPLAIN ANALYZE SELECT * FROM atenciones WHERE paciente_id = $1;

-- Verificar uso de índices
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename = 'nombre_tabla';
```

### **📈 Monitoring Queries:**
```sql
-- Top queries por tiempo promedio
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Tablas más grandes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS size
FROM pg_stat_user_tables 
ORDER BY pg_total_relation_size(relid) DESC;
```

---

## 🤖 **Automation Scripts**

### **📋 Pre-commit Hook (Recomendado):**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Verificar que migración tiene formato correcto
for migration in supabase/migrations/*.sql; do
    if [[ ! $migration =~ ^supabase/migrations/[0-9]{14}_.+\.sql$ ]]; then
        echo "❌ Migration naming format incorrect: $migration"
        exit 1
    fi
done

# Validar SQL syntax
supabase db lint
if [ $? -ne 0 ]; then
    echo "❌ SQL lint failed"
    exit 1
fi

echo "✅ Migration checks passed"
```

### **📋 Migration Validator Script:**
```bash
#!/bin/bash  
# scripts/validate-migration.sh

MIGRATION_FILE=$1

echo "🔍 Validating migration: $MIGRATION_FILE"

# 1. Check file exists
if [[ ! -f "$MIGRATION_FILE" ]]; then
    echo "❌ Migration file not found: $MIGRATION_FILE"
    exit 1
fi

# 2. Check naming convention
if [[ ! $(basename "$MIGRATION_FILE") =~ ^[0-9]{14}_.+\.sql$ ]]; then
    echo "❌ Incorrect naming format. Use: YYYYMMDDHHMMSS_description.sql"
    exit 1
fi

# 3. Check required sections
if ! grep -q "BEGIN;" "$MIGRATION_FILE"; then
    echo "⚠️  Warning: No transaction BEGIN found"
fi

if ! grep -q "COMMIT;" "$MIGRATION_FILE"; then
    echo "⚠️  Warning: No transaction COMMIT found"
fi

# 4. Validate SQL
echo "🔍 Running SQL validation..."
supabase db reset --debug

if [ $? -eq 0 ]; then
    echo "✅ Migration validation successful"
else
    echo "❌ Migration validation failed"
    exit 1
fi
```

---

## 📚 **Referencias y Recursos**

### **📖 Documentación Oficial:**
- **[Supabase Migrations](https://supabase.com/docs/guides/cli/migrations)** - Documentación oficial CLI
- **[PostgreSQL DDL](https://postgresql.org/docs/current/ddl.html)** - Data Definition Language reference
- **[RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)** - Row Level Security patterns

### **🔗 Referencias Internas:**
- **[Database Overview](../01-overview/database-overview.md)** - Architecture y estado actual
- **[Schema Evolution](../01-overview/schema-evolution.md)** - Historia completa database
- **[Backend Models](../../../backend/models/)** - Sincronización Pydantic ↔ PostgreSQL

### **⚡ Templates Reutilizables:**
- **[Create Table Template](templates/create-table-template.sql)** - Template tabla nueva
- **[Add Column Template](templates/add-column-template.sql)** - Template agregar columna
- **[RLS Policy Template](templates/rls-policy-template.sql)** - Template políticas security

---

## 🎯 **Migration Checklist**

### **✅ Pre-Migration:**
- [ ] Cambio documentado en issue/PR
- [ ] Template migración seguido correctamente  
- [ ] Naming convention respetada
- [ ] SQL validado localmente con `supabase db reset`
- [ ] Backend tests pasan después del cambio
- [ ] RLS policies configuradas para tablas nuevas

### **✅ Migration Execution:**
- [ ] Proyecto correcto linkado (`supabase projects list`)
- [ ] Diff reviewed (`supabase db diff --linked`)
- [ ] Backup de production tomado (si cambio major)
- [ ] Deploy ejecutado (`supabase db push`)
- [ ] Verification post-deploy realizada

### **✅ Post-Migration:**
- [ ] Schema consistency confirmada (`supabase db diff --linked`)
- [ ] Backend deployment actualizado si es necesario
- [ ] Monitoring activado para nuevas tablas/indices
- [ ] Documentation actualizada si aplica

---

**🚀 Workflow designed para zero-downtime database evolution**  
**👥 Maintained by:** Database Development Team  
**🎯 Next evolution:** Template library + automated testing pipeline  
**📊 Success metric:** 100% migration success rate con rollback capability