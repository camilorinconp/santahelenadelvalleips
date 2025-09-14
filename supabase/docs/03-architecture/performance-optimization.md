# ⚡ Performance Optimization - Enterprise Database Performance

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía completa optimización performance PostgreSQL + Supabase médico  
**📍 Audiencia:** Database Performance Engineers, Senior Database Architects, DevOps  

---

## 🎯 **Filosofía de Performance**

### **⚡ Principios de Optimización:**
1. **Measure First:** Nunca optimizar sin métricas
2. **Index Strategy:** Índices inteligentes, no índices everywhere
3. **Query Patterns:** Optimizar consultas más frecuentes primero
4. **Scalability Focus:** Soluciones que escalen con crecimiento de datos
5. **Medical Context:** Performance crítico para sistemas de salud

### **📊 Performance Targets (SLA):**
```
🎯 PERFORMANCE GOALS:

├── CRUD Operations Individual
│   ├── SELECT single record: <50ms (95th percentile)
│   ├── INSERT single record: <100ms (95th percentile)
│   ├── UPDATE single record: <100ms (95th percentile)
│   └── DELETE single record: <100ms (95th percentile)
│
├── Complex Queries (Polimórficos)
│   ├── Resolución 1 nivel: <150ms (95th percentile)
│   ├── Resolución 2 niveles: <300ms (95th percentile)
│   └── Agregaciones complejas: <500ms (95th percentile)
│
├── Bulk Operations
│   ├── Export pacientes (100 registros): <2s
│   ├── Reportes compliance: <5s
│   └── Dashboards tiempo real: <3s
│
└── Database Health
    ├── Connection pool utilization: <70%
    ├── Cache hit ratio: >99%
    ├── Index usage ratio: >95%
    └── Long-running queries: <1% total
```

---

## 🏗️ **Indexing Strategy Arquitectónica**

### **📊 TIER 1: Critical Performance Indexes**

#### **Polimorfismo Resolución (Críticos):**
```sql
-- 1. Resolución polimórfica nivel 1
CREATE INDEX CONCURRENTLY idx_atenciones_polymorphic_resolution
ON atenciones(tipo_atencion, detalle_id)
INCLUDE (paciente_id, medico_id, fecha_atencion);

-- 2. Resolución polimórfica nivel 2 (RIAMP)
CREATE INDEX CONCURRENTLY idx_atencion_mp_polymorphic_resolution
ON atencion_materno_perinatal(sub_tipo_atencion, sub_detalle_id)
INCLUDE (atencion_id, numero_embarazo, edad_gestacional_semanas);

-- 3. Foreign Keys críticos (evitar sequential scans)
CREATE INDEX CONCURRENTLY idx_atenciones_paciente_fecha
ON atenciones(paciente_id, fecha_atencion DESC);

CREATE INDEX CONCURRENTLY idx_atenciones_medico_fecha  
ON atenciones(medico_id, fecha_atencion DESC);

CREATE INDEX CONCURRENTLY idx_atencion_mp_atencion_id
ON atencion_materno_perinatal(atencion_id);
```

#### **Búsquedas Pacientes (Críticas):**
```sql
-- 4. Búsqueda por documento (más frecuente)
CREATE UNIQUE INDEX idx_pacientes_documento_unique
ON pacientes(numero_documento)
WHERE numero_documento IS NOT NULL;

-- 5. Búsqueda por nombres (segunda más frecuente)
CREATE INDEX CONCURRENTLY idx_pacientes_nombres_search
ON pacientes(primer_nombre, primer_apellido)
WHERE primer_nombre IS NOT NULL AND primer_apellido IS NOT NULL;

-- 6. Índice compuesto para listados con filtros
CREATE INDEX CONCURRENTLY idx_pacientes_listado_performance
ON pacientes(fecha_nacimiento, genero, centro_salud_id)
INCLUDE (primer_nombre, primer_apellido, numero_documento);
```

### **📊 TIER 2: Business Logic Indexes**

#### **Compliance y Reportería:**
```sql
-- 7. Reportes por rango de fechas (común en compliance)
CREATE INDEX CONCURRENTLY idx_atenciones_fecha_tipo
ON atenciones(fecha_atencion, tipo_atencion)
WHERE fecha_atencion >= '2024-01-01';

-- 8. Variables PEDT por periodo
CREATE INDEX CONCURRENTLY idx_pedt_variables_periodo
ON atenciones(DATE_TRUNC('month', fecha_atencion), tipo_atencion)
INCLUDE (paciente_id, medico_id);

-- 9. Control prenatal por trimestre gestacional
CREATE INDEX CONCURRENTLY idx_control_prenatal_trimestre
ON detalle_control_prenatal((
    CASE 
        WHEN semanas_gestacion <= 12 THEN 1
        WHEN semanas_gestacion <= 27 THEN 2
        ELSE 3
    END
), riesgo_biopsicosocial)
WHERE semanas_gestacion IS NOT NULL;
```

#### **RLS Performance Support:**
```sql
-- 10. Optimización RLS: asignación médico-paciente
CREATE INDEX CONCURRENTLY idx_medico_paciente_rls_performance
ON medico_paciente_asignacion(medico_id, paciente_id, activa)
WHERE activa = true;

-- 11. Optimización RLS: usuarios por centro
CREATE INDEX CONCURRENTLY idx_usuarios_centro_rls_performance  
ON usuario_centros(usuario_id, centro_salud_id, activa)
WHERE activa = true;

-- 12. Optimización RLS: médicos por usuario
CREATE INDEX CONCURRENTLY idx_medicos_usuario_rls_performance
ON medicos(usuario_id)
INCLUDE (id, especialidad);
```

### **📊 TIER 3: Advanced Performance Indexes**

#### **JSONB Optimization:**
```sql
-- 13. Búsquedas en antecedentes médicos
CREATE INDEX CONCURRENTLY idx_control_prenatal_antecedentes_gin
ON detalle_control_prenatal USING GIN (antecedentes_medicos_detallados);

-- 14. Búsquedas en plan de manejo
CREATE INDEX CONCURRENTLY idx_control_prenatal_plan_gin
ON detalle_control_prenatal USING GIN (plan_manejo_personalizado);

-- 15. Búsquedas específicas en JSONB (path optimization)
CREATE INDEX CONCURRENTLY idx_antecedentes_diabetes
ON detalle_control_prenatal USING GIN ((antecedentes_medicos_detallados -> 'diabetes'));

CREATE INDEX CONCURRENTLY idx_plan_medicamentos
ON detalle_control_prenatal USING GIN ((plan_manejo_personalizado -> 'medicamentos'));
```

#### **Full-Text Search:**
```sql
-- 16. Búsqueda texto completo en observaciones clínicas
CREATE INDEX CONCURRENTLY idx_observaciones_clinicas_fts
ON detalle_control_prenatal USING GIN (to_tsvector('spanish', observaciones_clinicas))
WHERE observaciones_clinicas IS NOT NULL;

-- 17. Búsqueda texto completo en notas seguimiento
CREATE INDEX CONCURRENTLY idx_notas_seguimiento_fts  
ON detalle_control_prenatal USING GIN (to_tsvector('spanish', notas_seguimiento))
WHERE notas_seguimiento IS NOT NULL;
```

---

## 🚀 **Query Optimization Patterns**

### **⚡ Pattern 1: Optimized Polymorphic Resolution**

#### **ANTES (Subóptimo):**
```sql
-- ❌ Problema: N+1 queries, múltiples round trips
SELECT a.* FROM atenciones a WHERE a.paciente_id = $1;
-- Luego para cada atención:
SELECT amp.* FROM atencion_materno_perinatal amp WHERE amp.atencion_id = $atencion_id;
-- Y luego para cada sub-detalle:
SELECT dcp.* FROM detalle_control_prenatal dcp WHERE dcp.id = $sub_detalle_id;
```

#### **DESPUÉS (Optimizado):**
```sql
-- ✅ Solución: Single query con CTEs y resolución inteligente
WITH atencion_base AS (
    SELECT 
        a.id,
        a.tipo_atencion,
        a.fecha_atencion,
        a.paciente_id,
        a.detalle_id,
        p.primer_nombre,
        p.primer_apellido,
        m.nombre as medico_nombre
    FROM atenciones a
    JOIN pacientes p ON p.id = a.paciente_id
    LEFT JOIN medicos m ON m.id = a.medico_id
    WHERE a.paciente_id = $1
    ORDER BY a.fecha_atencion DESC
    LIMIT 50  -- Paginación
),
detalles_materno_perinatal AS (
    SELECT 
        ab.id as atencion_id,
        amp.sub_tipo_atencion,
        amp.numero_embarazo,
        amp.edad_gestacional_semanas,
        amp.sub_detalle_id,
        
        -- Resolución condicional en CTE (más eficiente)
        CASE amp.sub_tipo_atencion
            WHEN 'control_prenatal' THEN (
                SELECT json_build_object(
                    'semanas_gestacion', dcp.semanas_gestacion,
                    'peso_gestante', dcp.peso_gestante,
                    'presion_sistolica', dcp.presion_arterial_sistolica,
                    'riesgo', dcp.riesgo_biopsicosocial
                )
                FROM detalle_control_prenatal dcp
                WHERE dcp.id = amp.sub_detalle_id
            )
            WHEN 'parto' THEN (
                SELECT json_build_object(
                    'tipo_parto', dp.tipo_parto,
                    'peso_rn', dp.peso_recien_nacido,
                    'apgar_1min', dp.apgar_1_minuto
                )
                FROM detalle_parto dp
                WHERE dp.id = amp.sub_detalle_id
            )
            ELSE NULL
        END as detalle_clinico
        
    FROM atencion_base ab
    JOIN atencion_materno_perinatal amp ON amp.atencion_id = ab.id
    WHERE ab.tipo_atencion = 'materno_perinatal'
)
SELECT 
    ab.*,
    dmp.sub_tipo_atencion,
    dmp.numero_embarazo,
    dmp.detalle_clinico
FROM atencion_base ab
LEFT JOIN detalles_materno_perinatal dmp ON dmp.atencion_id = ab.id
ORDER BY ab.fecha_atencion DESC;
```

### **⚡ Pattern 2: Efficient Aggregations**

#### **Dashboard Materno-Perinatal Optimizado:**
```sql
-- ✅ Agregaciones eficientes con window functions
WITH stats_base AS (
    SELECT 
        p.id as paciente_id,
        p.primer_nombre || ' ' || p.primer_apellido as nombre_completo,
        p.numero_documento,
        
        -- Estadísticas con window functions (más eficiente que subqueries)
        COUNT(*) OVER (PARTITION BY p.id) as total_atenciones,
        COUNT(*) FILTER (WHERE amp.sub_tipo_atencion = 'control_prenatal') 
            OVER (PARTITION BY p.id) as total_controles,
        
        MAX(amp.edad_gestacional_semanas) 
            OVER (PARTITION BY p.id) as semanas_gestacion_actual,
        MAX(dcp.riesgo_biopsicosocial::text) 
            OVER (PARTITION BY p.id)::riesgo_enum as riesgo_maximo,
        
        -- Ranking para obtener último control
        ROW_NUMBER() OVER (
            PARTITION BY p.id 
            ORDER BY a.fecha_atencion DESC
        ) as rn
        
    FROM pacientes p
    JOIN atenciones a ON a.paciente_id = p.id
    JOIN atencion_materno_perinatal amp ON amp.atencion_id = a.id
    LEFT JOIN detalle_control_prenatal dcp ON dcp.id = amp.sub_detalle_id
        AND amp.sub_tipo_atencion = 'control_prenatal'
    
    WHERE a.tipo_atencion = 'materno_perinatal'
    AND a.fecha_atencion >= CURRENT_DATE - INTERVAL '12 months'
)
SELECT DISTINCT
    paciente_id,
    nombre_completo,
    numero_documento,
    total_atenciones,
    total_controles,
    semanas_gestacion_actual,
    riesgo_maximo,
    
    -- Compliance calculado eficientemente
    CASE 
        WHEN semanas_gestacion_actual IS NULL THEN NULL
        WHEN semanas_gestacion_actual <= 12 AND total_controles >= 1 THEN true
        WHEN semanas_gestacion_actual <= 27 AND total_controles >= 4 THEN true  
        WHEN semanas_gestacion_actual > 27 AND total_controles >= 7 THEN true
        ELSE false
    END as cumple_controles_minimos
    
FROM stats_base
WHERE rn = 1  -- Solo el registro más reciente por paciente
ORDER BY semanas_gestacion_actual DESC NULLS LAST;
```

### **⚡ Pattern 3: Cached Expensive Calculations**

#### **Materialized Views para Performance:**
```sql
-- Vista materializada para indicadores compliance (actualización diaria)
CREATE MATERIALIZED VIEW mv_indicadores_compliance AS
WITH periodo_reporte AS (
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) as mes_actual,
        DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '11 months' as inicio_periodo
),
estadisticas_base AS (
    SELECT 
        pr.mes_actual,
        pr.inicio_periodo,
        
        -- Total pacientes activos
        COUNT(DISTINCT p.id) as total_pacientes,
        
        -- Pacientes con atención materno-perinatal
        COUNT(DISTINCT p.id) FILTER (
            WHERE EXISTS (
                SELECT 1 FROM atenciones a 
                WHERE a.paciente_id = p.id 
                AND a.tipo_atencion = 'materno_perinatal'
                AND a.fecha_atencion >= pr.inicio_periodo
            )
        ) as pacientes_materno_perinatal,
        
        -- Total controles prenatales
        COUNT(*) FILTER (
            WHERE a.tipo_atencion = 'materno_perinatal'
            AND EXISTS (
                SELECT 1 FROM atencion_materno_perinatal amp
                WHERE amp.atencion_id = a.id 
                AND amp.sub_tipo_atencion = 'control_prenatal'
            )
        ) as total_controles_prenatales,
        
        -- Partos atendidos
        COUNT(*) FILTER (
            WHERE a.tipo_atencion = 'materno_perinatal'
            AND EXISTS (
                SELECT 1 FROM atencion_materno_perinatal amp
                WHERE amp.atencion_id = a.id 
                AND amp.sub_tipo_atencion = 'parto'
            )
        ) as total_partos_atendidos,
        
        -- Casos de alto riesgo
        COUNT(*) FILTER (
            WHERE a.tipo_atencion = 'materno_perinatal'
            AND EXISTS (
                SELECT 1 FROM atencion_materno_perinatal amp
                JOIN detalle_control_prenatal dcp ON dcp.id = amp.sub_detalle_id
                WHERE amp.atencion_id = a.id 
                AND amp.sub_tipo_atencion = 'control_prenatal'
                AND dcp.riesgo_biopsicosocial IN ('alto', 'critico')
            )
        ) as casos_alto_riesgo
        
    FROM periodo_reporte pr
    CROSS JOIN pacientes p
    LEFT JOIN atenciones a ON a.paciente_id = p.id 
        AND a.fecha_atencion >= pr.inicio_periodo
        AND a.fecha_atencion < pr.mes_actual + INTERVAL '1 month'
    
    GROUP BY pr.mes_actual, pr.inicio_periodo
)
SELECT 
    mes_actual,
    inicio_periodo,
    total_pacientes,
    pacientes_materno_perinatal,
    
    -- Cálculos de indicadores
    ROUND(100.0 * pacientes_materno_perinatal / NULLIF(total_pacientes, 0), 2) 
        as cobertura_materno_perinatal_pct,
    
    total_controles_prenatales,
    total_partos_atendidos,
    casos_alto_riesgo,
    
    ROUND(100.0 * casos_alto_riesgo / NULLIF(total_controles_prenatales, 0), 2)
        as casos_alto_riesgo_pct,
    
    -- Metadata actualización
    NOW() as calculado_en,
    'daily_refresh' as tipo_actualizacion

FROM estadisticas_base;

-- Índices en MV
CREATE UNIQUE INDEX idx_mv_indicadores_compliance_mes 
ON mv_indicadores_compliance(mes_actual);

-- Refresh automático (vía cron job o scheduled function)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_indicadores_compliance;
```

---

## 📊 **Connection Pooling Optimization**

### **🔌 PgBouncer Configuration:**
```ini
# Configuración optimizada para aplicación médica
[databases]
isp_salud_production = host=db.supabase.co port=5432 dbname=postgres

[pgbouncer]
# Pool settings optimizados para carga médica
pool_mode = transaction
listen_port = 6543
listen_addr = *
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Sizing basado en carga esperada
max_client_conn = 200
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 10

# Timeouts ajustados para operaciones médicas
server_connect_timeout = 15
server_login_retry = 3
query_timeout = 300
query_wait_timeout = 120

# Monitoring y logs
stats_period = 60
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
```

### **⚡ Connection Pool Monitoring:**
```sql
-- Función para monitorear connection pool health
CREATE OR REPLACE FUNCTION connection_pool_health()
RETURNS TABLE (
    metric_name TEXT,
    metric_value NUMERIC,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'Active Connections'::TEXT,
        COUNT(*)::NUMERIC,
        CASE 
            WHEN COUNT(*) < 50 THEN 'Good'
            WHEN COUNT(*) < 80 THEN 'Warning' 
            ELSE 'Critical'
        END,
        CASE 
            WHEN COUNT(*) > 80 THEN 'Consider increasing pool size'
            ELSE 'Connection usage normal'
        END
    FROM pg_stat_activity 
    WHERE state = 'active'
    
    UNION ALL
    
    SELECT 
        'Idle Connections'::TEXT,
        COUNT(*)::NUMERIC,
        CASE 
            WHEN COUNT(*) < 20 THEN 'Good'
            ELSE 'Warning'
        END,
        CASE 
            WHEN COUNT(*) > 30 THEN 'Too many idle connections'
            ELSE 'Idle connections normal'
        END
    FROM pg_stat_activity 
    WHERE state = 'idle'
    
    UNION ALL
    
    SELECT 
        'Long Running Queries (>30s)'::TEXT,
        COUNT(*)::NUMERIC,
        CASE 
            WHEN COUNT(*) = 0 THEN 'Good'
            WHEN COUNT(*) < 3 THEN 'Warning'
            ELSE 'Critical'
        END,
        'Review and optimize long-running queries'
    FROM pg_stat_activity 
    WHERE state = 'active' 
    AND NOW() - query_start > INTERVAL '30 seconds';
END;
$$ LANGUAGE plpgsql;
```

---

## 📈 **Performance Monitoring Dashboard**

### **📊 Core Performance Metrics:**
```sql
-- Vista comprehensiva de performance database
CREATE VIEW database_performance_dashboard AS
WITH query_stats AS (
    SELECT 
        query,
        calls,
        total_exec_time,
        mean_exec_time,
        stddev_exec_time,
        rows,
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
    FROM pg_stat_statements 
    WHERE calls > 10  -- Solo queries frecuentes
),
table_stats AS (
    SELECT 
        schemaname,
        tablename,
        n_tup_ins + n_tup_upd + n_tup_del as total_modifications,
        n_tup_ins as inserts,
        n_tup_upd as updates, 
        n_tup_del as deletes,
        seq_scan,
        seq_tup_read,
        idx_scan,
        idx_tup_fetch,
        CASE 
            WHEN seq_scan + idx_scan = 0 THEN 0
            ELSE 100.0 * idx_scan / (seq_scan + idx_scan)
        END as index_usage_percent
    FROM pg_stat_user_tables
    WHERE schemaname = 'public'
),
index_stats AS (
    SELECT 
        schemaname,
        tablename,
        indexname,
        idx_scan,
        idx_tup_read,
        idx_tup_fetch
    FROM pg_stat_user_indexes
    WHERE schemaname = 'public'
    AND idx_scan > 0
)
SELECT 
    'Query Performance' as category,
    'Top Slow Queries' as metric_name,
    COUNT(*) FILTER (WHERE mean_exec_time > 1000) as slow_queries_count,
    ROUND(AVG(mean_exec_time), 2) as avg_execution_time_ms,
    ROUND(AVG(hit_percent), 2) as avg_cache_hit_percent
FROM query_stats

UNION ALL

SELECT 
    'Table Performance' as category,
    'Index Usage' as metric_name,
    COUNT(*) FILTER (WHERE index_usage_percent < 95) as tables_low_index_usage,
    ROUND(AVG(index_usage_percent), 2) as avg_index_usage_percent,
    SUM(seq_tup_read) as total_sequential_reads
FROM table_stats

UNION ALL

SELECT 
    'Index Effectiveness' as category,
    'Index Scans' as metric_name,
    COUNT(*) as total_indexes_used,
    SUM(idx_scan) as total_index_scans,
    ROUND(AVG(idx_tup_fetch::NUMERIC / NULLIF(idx_scan, 0)), 2) as avg_rows_per_index_scan
FROM index_stats;
```

### **🚨 Performance Alerts:**
```sql
-- Function para detectar problemas de performance automáticamente
CREATE OR REPLACE FUNCTION detect_performance_issues()
RETURNS TABLE (
    severity TEXT,
    category TEXT,  
    issue TEXT,
    affected_object TEXT,
    recommendation TEXT,
    metric_value NUMERIC
) AS $$
BEGIN
    -- Queries muy lentas
    RETURN QUERY
    SELECT 
        'CRITICAL'::TEXT,
        'Query Performance'::TEXT,
        'Extremely slow query detected'::TEXT,
        LEFT(query, 100)::TEXT,
        'Review and optimize this query immediately'::TEXT,
        mean_exec_time
    FROM pg_stat_statements
    WHERE mean_exec_time > 5000  -- >5 segundos
    AND calls > 5
    ORDER BY mean_exec_time DESC
    LIMIT 5;
    
    -- Tablas sin índices eficientes
    RETURN QUERY
    SELECT 
        'WARNING'::TEXT,
        'Table Performance'::TEXT,
        'Low index usage detected'::TEXT,
        (schemaname || '.' || tablename)::TEXT,
        'Consider adding indexes for frequent queries'::TEXT,
        CASE 
            WHEN seq_scan + idx_scan = 0 THEN 0
            ELSE 100.0 * idx_scan / (seq_scan + idx_scan)
        END
    FROM pg_stat_user_tables
    WHERE schemaname = 'public'
    AND seq_scan > 1000  -- Muchos sequential scans
    AND CASE 
        WHEN seq_scan + idx_scan = 0 THEN 0
        ELSE 100.0 * idx_scan / (seq_scan + idx_scan)
    END < 90
    ORDER BY seq_scan DESC;
    
    -- Conexiones colgadas
    RETURN QUERY
    SELECT 
        'WARNING'::TEXT,
        'Connection Health'::TEXT,
        'Long-running connection detected'::TEXT,
        (pid || ': ' || COALESCE(usename, 'unknown'))::TEXT,
        'Review connection and consider termination'::TEXT,
        EXTRACT(EPOCH FROM (NOW() - backend_start))::NUMERIC
    FROM pg_stat_activity
    WHERE state != 'idle'
    AND NOW() - backend_start > INTERVAL '10 minutes'
    AND pid != pg_backend_pid();
    
END;
$$ LANGUAGE plpgsql;
```

---

## 🔧 **Maintenance Automation**

### **🧹 Automated Database Maintenance:**
```sql
-- Función para mantenimiento automático optimizado
CREATE OR REPLACE FUNCTION automated_maintenance()
RETURNS TEXT AS $$
DECLARE
    maintenance_log TEXT := '';
    table_record RECORD;
    analyze_threshold INTEGER := 1000;
    vacuum_threshold INTEGER := 10000;
BEGIN
    maintenance_log := 'AUTOMATED MAINTENANCE STARTED: ' || NOW() || E'\n';
    
    -- ANALYZE tables que necesitan actualización de estadísticas
    FOR table_record IN
        SELECT schemaname, tablename, n_tup_ins + n_tup_upd + n_tup_del as modifications
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        AND n_tup_ins + n_tup_upd + n_tup_del > analyze_threshold
        AND (last_analyze IS NULL OR last_analyze < NOW() - INTERVAL '1 day')
        ORDER BY modifications DESC
        LIMIT 10
    LOOP
        EXECUTE format('ANALYZE %I.%I', table_record.schemaname, table_record.tablename);
        maintenance_log := maintenance_log || format('ANALYZED: %s.%s (%s modifications)' || E'\n', 
            table_record.schemaname, table_record.tablename, table_record.modifications);
    END LOOP;
    
    -- VACUUM tables con muchas modificaciones
    FOR table_record IN
        SELECT schemaname, tablename, n_tup_ins + n_tup_upd + n_tup_del as modifications
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        AND n_tup_ins + n_tup_upd + n_tup_del > vacuum_threshold
        AND (last_vacuum IS NULL OR last_vacuum < NOW() - INTERVAL '3 days')
        ORDER BY modifications DESC
        LIMIT 5
    LOOP
        EXECUTE format('VACUUM %I.%I', table_record.schemaname, table_record.tablename);
        maintenance_log := maintenance_log || format('VACUUMED: %s.%s (%s modifications)' || E'\n',
            table_record.schemaname, table_record.tablename, table_record.modifications);
    END LOOP;
    
    -- Refresh materialized views críticas
    BEGIN
        REFRESH MATERIALIZED VIEW CONCURRENTLY mv_indicadores_compliance;
        maintenance_log := maintenance_log || 'REFRESHED: mv_indicadores_compliance' || E'\n';
    EXCEPTION
        WHEN OTHERS THEN
            maintenance_log := maintenance_log || 'ERROR refreshing mv_indicadores_compliance: ' || SQLERRM || E'\n';
    END;
    
    -- Limpiar pg_stat_statements si está muy grande
    IF (SELECT COUNT(*) FROM pg_stat_statements) > 10000 THEN
        PERFORM pg_stat_statements_reset();
        maintenance_log := maintenance_log || 'RESET: pg_stat_statements (was too large)' || E'\n';
    END IF;
    
    maintenance_log := maintenance_log || 'AUTOMATED MAINTENANCE COMPLETED: ' || NOW() || E'\n';
    
    RETURN maintenance_log;
END;
$$ LANGUAGE plpgsql;

-- Programar ejecución (ejemplo con pg_cron si está disponible)
-- SELECT cron.schedule('automated-maintenance', '0 2 * * *', 'SELECT automated_maintenance()');
```

### **📊 Table Size Monitoring:**
```sql
-- Vista para monitorear crecimiento de tablas
CREATE VIEW table_size_monitoring AS
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_total_relation_size(schemaname||'.'||tablename) as total_size_bytes,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_relation_size(schemaname||'.'||tablename) as table_size_bytes,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size,
    
    -- Estadísticas de uso
    n_tup_ins + n_tup_upd + n_tup_del as total_modifications,
    n_live_tup as estimated_row_count,
    
    -- Eficiencia de storage
    CASE 
        WHEN n_live_tup > 0 
        THEN pg_relation_size(schemaname||'.'||tablename) / n_live_tup
        ELSE NULL 
    END as bytes_per_row,
    
    -- Ratio de índices vs datos
    CASE 
        WHEN pg_relation_size(schemaname||'.'||tablename) > 0
        THEN ROUND(100.0 * (pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) / pg_relation_size(schemaname||'.'||tablename), 2)
        ELSE 0
    END as index_ratio_percent,
    
    last_vacuum,
    last_analyze
    
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 🎯 **Performance Testing Framework**

### **⏱️ Benchmark Queries:**
```sql
-- Suite de pruebas de performance para validar optimizaciones
CREATE OR REPLACE FUNCTION performance_benchmark()
RETURNS TABLE (
    test_name TEXT,
    execution_time_ms NUMERIC,
    rows_returned BIGINT,
    cache_hit_ratio NUMERIC,
    status TEXT
) AS $$
DECLARE
    start_time TIMESTAMPTZ;
    end_time TIMESTAMPTZ;
    exec_time NUMERIC;
    row_count BIGINT;
BEGIN
    -- Test 1: Búsqueda paciente por documento
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count FROM pacientes WHERE numero_documento = '12345678';
    end_time := clock_timestamp();
    exec_time := EXTRACT(MILLISECONDS FROM (end_time - start_time));
    
    RETURN QUERY SELECT 
        'Patient Search by Document'::TEXT,
        exec_time,
        row_count,
        NULL::NUMERIC,
        CASE WHEN exec_time < 50 THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Test 2: Resolución polimórfica materno-perinatal
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count 
    FROM atenciones a
    JOIN atencion_materno_perinatal amp ON amp.atencion_id = a.id
    LEFT JOIN detalle_control_prenatal dcp ON dcp.id = amp.sub_detalle_id
    WHERE a.tipo_atencion = 'materno_perinatal'
    AND a.fecha_atencion >= CURRENT_DATE - INTERVAL '30 days';
    end_time := clock_timestamp();
    exec_time := EXTRACT(MILLISECONDS FROM (end_time - start_time));
    
    RETURN QUERY SELECT 
        'Polymorphic Resolution MP'::TEXT,
        exec_time,
        row_count,
        NULL::NUMERIC,
        CASE WHEN exec_time < 300 THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Test 3: Dashboard agregaciones
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO row_count FROM mv_indicadores_compliance;
    end_time := clock_timestamp();
    exec_time := EXTRACT(MILLISECONDS FROM (end_time - start_time));
    
    RETURN QUERY SELECT 
        'Dashboard Aggregations'::TEXT,
        exec_time,
        row_count,
        NULL::NUMERIC,
        CASE WHEN exec_time < 100 THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Test 4: RLS overhead
    start_time := clock_timestamp();
    PERFORM set_config('role', 'authenticated', true);
    SELECT COUNT(*) INTO row_count FROM pacientes LIMIT 100;
    PERFORM set_config('role', 'service_role', true);
    end_time := clock_timestamp();
    exec_time := EXTRACT(MILLISECONDS FROM (end_time - start_time));
    
    RETURN QUERY SELECT 
        'RLS Overhead Test'::TEXT,
        exec_time,
        row_count,
        NULL::NUMERIC,
        CASE WHEN exec_time < 200 THEN 'PASS' ELSE 'FAIL' END::TEXT;
END;
$$ LANGUAGE plpgsql;
```

---

## 📋 **Performance Checklist Deployment**

### **✅ Pre-Deployment Performance Checklist:**
```sql
-- Función para validar performance antes de deployment
CREATE OR REPLACE FUNCTION pre_deployment_performance_check()
RETURNS TABLE (
    check_name TEXT,
    status TEXT,
    details TEXT,
    action_required TEXT
) AS $$
BEGIN
    -- Check 1: Índices críticos existen
    RETURN QUERY
    WITH required_indexes AS (
        SELECT unnest(ARRAY[
            'idx_atenciones_polymorphic_resolution',
            'idx_pacientes_documento_unique', 
            'idx_atencion_mp_polymorphic_resolution',
            'idx_medico_paciente_rls_performance'
        ]) as index_name
    ),
    existing_indexes AS (
        SELECT indexname FROM pg_indexes WHERE schemaname = 'public'
    )
    SELECT 
        'Critical Indexes'::TEXT,
        CASE 
            WHEN COUNT(*) = (SELECT COUNT(*) FROM required_indexes) THEN 'PASS'
            ELSE 'FAIL'
        END::TEXT,
        format('%s of %s critical indexes exist', COUNT(*), (SELECT COUNT(*) FROM required_indexes))::TEXT,
        CASE 
            WHEN COUNT(*) < (SELECT COUNT(*) FROM required_indexes) THEN 'Create missing indexes'
            ELSE 'None'
        END::TEXT
    FROM required_indexes ri
    JOIN existing_indexes ei ON ei.indexname = ri.index_name;
    
    -- Check 2: RLS políticas configuradas  
    RETURN QUERY
    SELECT 
        'RLS Coverage'::TEXT,
        CASE 
            WHEN COUNT(*) FILTER (WHERE 'service_role' = ANY(roles)) >= 10 THEN 'PASS'
            ELSE 'FAIL'
        END::TEXT,
        format('%s service_role policies found', COUNT(*) FILTER (WHERE 'service_role' = ANY(roles)))::TEXT,
        CASE 
            WHEN COUNT(*) FILTER (WHERE 'service_role' = ANY(roles)) < 10 THEN 'Add missing service_role policies'
            ELSE 'None'
        END::TEXT
    FROM pg_policies WHERE schemaname = 'public';
    
    -- Check 3: Materialized views actualizadas
    RETURN QUERY
    SELECT 
        'Materialized Views'::TEXT,
        CASE 
            WHEN EXISTS (SELECT 1 FROM pg_matviews WHERE schemaname = 'public') THEN 'PASS'
            ELSE 'WARNING'
        END::TEXT,
        format('%s materialized views exist', (SELECT COUNT(*) FROM pg_matviews WHERE schemaname = 'public'))::TEXT,
        'Refresh materialized views before deployment'::TEXT;
    
END;
$$ LANGUAGE plpgsql;
```

---

**⚡ Performance optimization diseñado para sistemas médicos críticos de alta concurrencia**  
**👥 Maintained by:** Database Performance Engineering Team  
**🎯 SLA Target:** <100ms CRUD operations + <300ms complex polymorphic queries  
**📊 Success metrics:** 99.9% uptime + <1% slow queries + 99%+ cache hit ratio