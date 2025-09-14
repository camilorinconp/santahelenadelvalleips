# 🛡️ RLS Security Model - Enterprise Row Level Security

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía completa Row Level Security para sistema médico crítico  
**📍 Audiencia:** Security Engineers, Database Architects, Compliance Officers  

---

## 🔒 **Filosofía de Seguridad**

### **🎯 Principios Fundamentales:**
1. **Defense in Depth:** Múltiples capas de seguridad (RLS + Application + Network)
2. **Least Privilege:** Acceso mínimo necesario por rol
3. **Data Classification:** Seguridad proporcional a sensibilidad de datos
4. **Compliance First:** Cumplimiento HABEAS DATA y normativa salud
5. **Zero Trust:** Nunca confiar, siempre verificar

### **📊 Modelo de Roles y Permisos:**
```
🏥 JERARQUÍA DE ACCESO:

├── service_role (Backend FastAPI)
│   ├── Acceso: COMPLETO (CRUD + Admin)
│   ├── Uso: Operaciones backend automatizadas
│   └── Validación: API Key + JWT del servicio
│
├── authenticated (Usuarios del sistema)
│   ├── Acceso: LIMITADO por contexto business
│   ├── Subtipos:
│   │   ├── admin: Gestión sistema + reportes
│   │   ├── medico: Datos pacientes asignados
│   │   ├── enfermero: Datos limitados pacientes
│   │   ├── recepcionista: Solo datos básicos
│   │   └── auditor: Solo lectura para compliance
│   └── Validación: JWT + Context business rules
│
└── anon (Acceso público)
    ├── Acceso: MUY LIMITADO (catálogos públicos)
    ├── Uso: Consultas públicas, formularios web
    └── Validación: Rate limiting + IP filtering
```

---

## 🏗️ **Arquitectura RLS por Capas**

### **🔒 CAPA 1: Security Foundation**

#### **Configuración Base:**
```sql
-- Habilitar RLS en TODAS las tablas sensibles
DO $$
DECLARE
    table_record RECORD;
BEGIN
    FOR table_record IN 
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
        AND tablename NOT LIKE 'supabase_%'
        AND tablename NOT IN ('schema_migrations')
    LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', table_record.tablename);
        RAISE NOTICE 'RLS enabled for: %', table_record.tablename;
    END LOOP;
END $$;
```

#### **Service Role Foundation (CRÍTICO):**
```sql
-- Service role debe tener acceso COMPLETO
-- Esta policy es CRÍTICA para funcionamiento del backend
CREATE OR REPLACE FUNCTION create_service_role_policy(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('
        CREATE POLICY "service_role_full_access_%I" ON %I
        FOR ALL 
        TO service_role
        USING (true)
        WITH CHECK (true)
    ', table_name, table_name);
    
    -- Grant explícito adicional
    EXECUTE format('GRANT ALL ON %I TO service_role', table_name);
END;
$$ LANGUAGE plpgsql;

-- Aplicar a todas las tablas
SELECT create_service_role_policy(tablename) 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename NOT LIKE 'supabase_%';
```

### **🔒 CAPA 2: Data Classification Security**

#### **NIVEL CRÍTICO: Datos Pacientes**
```sql
-- Tabla: pacientes
CREATE POLICY "authenticated_read_assigned_patients" ON pacientes
FOR SELECT TO authenticated
USING (
    -- Médico/Enfermero ve pacientes asignados
    EXISTS (
        SELECT 1 FROM medico_paciente_asignacion mpa
        JOIN medicos m ON m.id = mpa.medico_id
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE mpa.paciente_id = pacientes.id
        AND u.id = auth.uid()
        AND mpa.activa = true
    )
    OR
    -- Admin ve todos los pacientes de su centro
    EXISTS (
        SELECT 1 FROM usuarios u
        JOIN usuario_centros uc ON uc.usuario_id = u.id
        WHERE u.id = auth.uid()
        AND u.rol = 'admin'
        AND uc.centro_salud_id = pacientes.centro_salud_id
    )
    OR
    -- Recepcionista ve solo datos básicos (implementar via campos específicos)
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid()
        AND u.rol = 'recepcionista'
        AND u.centro_salud_id = pacientes.centro_salud_id
    )
);

-- Auditoría especial para updates de datos pacientes
CREATE POLICY "authenticated_update_patients_with_audit" ON pacientes
FOR UPDATE TO authenticated
USING (
    -- Solo médicos asignados o admin pueden actualizar
    EXISTS (
        SELECT 1 FROM medico_paciente_asignacion mpa
        JOIN medicos m ON m.id = mpa.medico_id
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE mpa.paciente_id = pacientes.id
        AND u.id = auth.uid()
        AND mpa.activa = true
    )
    OR
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid() AND u.rol = 'admin'
    )
)
WITH CHECK (
    -- Validaciones adicionales en updates
    actualizado_en = NOW()  -- Timestamp se actualiza automáticamente
    AND actualizado_por = auth.uid()  -- Usuario se registra
);
```

#### **NIVEL ALTO: Datos Clínicos**
```sql
-- Tabla: atenciones (polimórfica principal)
CREATE POLICY "authenticated_read_clinical_data" ON atenciones
FOR SELECT TO authenticated
USING (
    -- Médico que registró la atención
    EXISTS (
        SELECT 1 FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id  
        WHERE m.id = atenciones.medico_id
        AND u.id = auth.uid()
    )
    OR
    -- Médico actualmente asignado al paciente
    EXISTS (
        SELECT 1 FROM medico_paciente_asignacion mpa
        JOIN medicos m ON m.id = mpa.medico_id
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE mpa.paciente_id = atenciones.paciente_id
        AND u.id = auth.uid()
        AND mpa.activa = true
    )
    OR
    -- Personal de enfermería del mismo centro (solo lecturas básicas)
    EXISTS (
        SELECT 1 FROM usuarios u
        JOIN pacientes p ON p.id = atenciones.paciente_id
        WHERE u.id = auth.uid()
        AND u.rol = 'enfermero'
        AND u.centro_salud_id = p.centro_salud_id
        -- Solo atenciones de últimos 30 días
        AND atenciones.fecha_atencion >= CURRENT_DATE - INTERVAL '30 days'
    )
);

-- Política específica para creación de atenciones
CREATE POLICY "authenticated_create_clinical_data" ON atenciones
FOR INSERT TO authenticated
WITH CHECK (
    -- Solo médicos pueden crear atenciones
    EXISTS (
        SELECT 1 FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE m.id = medico_id
        AND u.id = auth.uid()
    )
    AND
    -- Y deben estar asignados al paciente
    EXISTS (
        SELECT 1 FROM medico_paciente_asignacion mpa
        WHERE mpa.paciente_id = atenciones.paciente_id
        AND mpa.medico_id = atenciones.medico_id
        AND mpa.activa = true
    )
);
```

#### **NIVEL MEDIO: Catálogos y Referencias**
```sql
-- Tablas: catalogo_ocupaciones, catalogo_etnias, etc.
CREATE POLICY "authenticated_read_catalogs" ON catalogo_ocupaciones
FOR SELECT TO authenticated
USING (activo = true);  -- Solo catálogos activos

-- Admin puede gestionar catálogos
CREATE POLICY "admin_manage_catalogs" ON catalogo_ocupaciones
FOR ALL TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM usuarios u 
        WHERE u.id = auth.uid() 
        AND u.rol = 'admin'
    )
)
WITH CHECK (
    EXISTS (
        SELECT 1 FROM usuarios u 
        WHERE u.id = auth.uid() 
        AND u.rol = 'admin'
    )
);
```

### **🔒 CAPA 3: Context-Aware Security**

#### **Seguridad por Centro de Salud:**
```sql
-- Función helper para verificar acceso por centro
CREATE OR REPLACE FUNCTION user_has_center_access(target_center_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM usuarios u
        JOIN usuario_centros uc ON uc.usuario_id = u.id
        WHERE u.id = auth.uid()
        AND uc.centro_salud_id = target_center_id
        AND uc.activa = true
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Aplicar a tablas relevantes
CREATE POLICY "center_based_access_entornos" ON entornos_salud_publica
FOR SELECT TO authenticated
USING (user_has_center_access(centro_salud_id));
```

#### **Seguridad por Especialidad Médica:**
```sql
-- Función helper para verificar especialidad requerida
CREATE OR REPLACE FUNCTION user_has_specialty_access(required_specialty TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE u.id = auth.uid()
        AND (m.especialidad = required_specialty OR m.especialidad = 'general')
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Aplicar a datos especializados
CREATE POLICY "specialty_based_access_materno_perinatal" ON atencion_materno_perinatal
FOR SELECT TO authenticated
USING (
    user_has_specialty_access('ginecologia_obstetricia')
    OR user_has_specialty_access('medicina_general')
    OR
    -- O acceso via atención principal
    EXISTS (
        SELECT 1 FROM atenciones a
        WHERE a.id = atencion_id
        -- Hereda policies de atenciones
    )
);
```

---

## 🕐 **Temporal Security Policies**

### **🔄 Time-based Access Control:**
```sql
-- Datos históricos: acceso limitado por tiempo
CREATE POLICY "temporal_access_historical_data" ON atenciones
FOR SELECT TO authenticated
USING (
    -- Datos recientes: acceso normal
    fecha_atencion >= CURRENT_DATE - INTERVAL '2 years'
    OR
    -- Datos históricos: solo roles autorizados
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid()
        AND u.rol IN ('admin', 'auditor')
    )
    OR
    -- Médico que creó el registro: acceso permanente
    EXISTS (
        SELECT 1 FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE m.id = medico_id
        AND u.id = auth.uid()
    )
);

-- Horarios de acceso (business hours)
CREATE OR REPLACE FUNCTION is_business_hours()
RETURNS BOOLEAN AS $$
BEGIN
    -- Lunes a Viernes, 6 AM a 10 PM (Colombia time)
    RETURN EXTRACT(DOW FROM NOW() AT TIME ZONE 'America/Bogota') BETWEEN 1 AND 5
        AND EXTRACT(HOUR FROM NOW() AT TIME ZONE 'America/Bogota') BETWEEN 6 AND 22;
END;
$$ LANGUAGE plpgsql;

-- Aplicar restricción horaria a operaciones sensibles
CREATE POLICY "business_hours_sensitive_updates" ON pacientes
FOR UPDATE TO authenticated
USING (
    is_business_hours()
    OR
    -- Emergencias: siempre permitidas
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid()
        AND u.rol IN ('medico_urgencias', 'admin')
    )
)
WITH CHECK (
    is_business_hours()
    OR
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid()
        AND u.rol IN ('medico_urgencias', 'admin')
    )
);
```

### **📊 Audit Trail Integration:**
```sql
-- Tabla de auditoría para cambios sensibles
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,  -- INSERT, UPDATE, DELETE
    record_id UUID NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES usuarios(id),
    user_role TEXT,
    ip_address INET,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    -- Contexto médico específico
    patient_id UUID REFERENCES pacientes(id),
    medical_context TEXT,
    compliance_flags TEXT[]
);

-- RLS en tabla de auditoría
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_audit_full" ON audit_log
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "admin_auditor_read_audit" ON audit_log
FOR SELECT TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM usuarios u
        WHERE u.id = auth.uid()
        AND u.rol IN ('admin', 'auditor')
    )
);

-- Trigger function para auditoría automática
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
DECLARE
    old_data JSONB;
    new_data JSONB;
    user_info RECORD;
BEGIN
    -- Obtener información del usuario actual
    SELECT u.id, u.rol INTO user_info
    FROM usuarios u WHERE u.id = auth.uid();
    
    -- Preparar datos para auditoría
    IF TG_OP = 'DELETE' THEN
        old_data = to_jsonb(OLD);
        new_data = NULL;
    ELSIF TG_OP = 'UPDATE' THEN
        old_data = to_jsonb(OLD);
        new_data = to_jsonb(NEW);
    ELSIF TG_OP = 'INSERT' THEN
        old_data = NULL;
        new_data = to_jsonb(NEW);
    END IF;
    
    -- Insertar registro de auditoría
    INSERT INTO audit_log (
        table_name,
        operation,
        record_id,
        old_values,
        new_values,
        user_id,
        user_role,
        patient_id
    ) VALUES (
        TG_TABLE_NAME,
        TG_OP,
        COALESCE(NEW.id, OLD.id),
        old_data,
        new_data,
        user_info.id,
        user_info.rol,
        COALESCE(NEW.paciente_id, OLD.paciente_id)  -- Si existe
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Aplicar auditoría a tablas críticas
CREATE TRIGGER audit_pacientes AFTER INSERT OR UPDATE OR DELETE ON pacientes
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_atenciones AFTER INSERT OR UPDATE OR DELETE ON atenciones
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

---

## 🚨 **Emergency Access Procedures**

### **🆘 Break Glass Access:**
```sql
-- Tabla para registrar accesos de emergencia
CREATE TABLE emergency_access_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    patient_id UUID REFERENCES pacientes(id),
    emergency_reason TEXT NOT NULL,
    supervisor_approved_by UUID REFERENCES usuarios(id),
    access_granted_at TIMESTAMPTZ DEFAULT NOW(),
    access_expires_at TIMESTAMPTZ NOT NULL,
    
    -- Validación posterior
    post_validation_required BOOLEAN DEFAULT TRUE,
    post_validation_completed_at TIMESTAMPTZ,
    post_validation_approved BOOLEAN,
    post_validation_notes TEXT
);

-- Función para otorgar acceso de emergencia
CREATE OR REPLACE FUNCTION grant_emergency_access(
    target_patient_id UUID,
    emergency_reason TEXT,
    hours_duration INTEGER DEFAULT 4
)
RETURNS BOOLEAN AS $$
DECLARE
    access_record_id UUID;
BEGIN
    -- Registrar acceso de emergencia
    INSERT INTO emergency_access_log (
        user_id,
        patient_id,
        emergency_reason,
        access_expires_at
    ) VALUES (
        auth.uid(),
        target_patient_id,
        emergency_reason,
        NOW() + (hours_duration * INTERVAL '1 hour')
    ) RETURNING id INTO access_record_id;
    
    -- Notificar a supervisores (implementar via webhook/email)
    PERFORM pg_notify('emergency_access_granted', 
        json_build_object(
            'user_id', auth.uid(),
            'patient_id', target_patient_id,
            'reason', emergency_reason,
            'access_id', access_record_id
        )::text
    );
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Policy de emergencia para datos pacientes
CREATE POLICY "emergency_access_patients" ON pacientes
FOR SELECT TO authenticated
USING (
    -- Acceso normal OR acceso de emergencia válido
    (/* ... políticas normales ... */)
    OR
    EXISTS (
        SELECT 1 FROM emergency_access_log eal
        WHERE eal.user_id = auth.uid()
        AND eal.patient_id = pacientes.id
        AND eal.access_expires_at > NOW()
        AND eal.post_validation_approved IS NOT FALSE
    )
);
```

### **🔐 Multi-Factor Authentication Integration:**
```sql
-- Tabla para tracking MFA requerido
CREATE TABLE mfa_required_operations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    operation_type TEXT NOT NULL,  -- 'sensitive_read', 'data_export', 'patient_update'
    table_name TEXT NOT NULL,
    record_id UUID,
    mfa_challenge_sent_at TIMESTAMPTZ DEFAULT NOW(),
    mfa_verified_at TIMESTAMPTZ,
    mfa_expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '10 minutes'),
    operation_context JSONB
);

-- Función para verificar MFA en operaciones sensibles
CREATE OR REPLACE FUNCTION requires_mfa_verification(
    operation_type TEXT,
    target_table TEXT DEFAULT NULL,
    target_record UUID DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Verificar si existe MFA válida para esta operación
    RETURN NOT EXISTS (
        SELECT 1 FROM mfa_required_operations mro
        WHERE mro.user_id = auth.uid()
        AND mro.operation_type = operation_type
        AND (target_table IS NULL OR mro.table_name = target_table)
        AND (target_record IS NULL OR mro.record_id = target_record)
        AND mro.mfa_verified_at IS NOT NULL
        AND mro.mfa_expires_at > NOW()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Policy que requiere MFA para exports masivos
CREATE POLICY "mfa_required_bulk_export" ON pacientes
FOR SELECT TO authenticated
USING (
    -- Acceso normal para queries individuales
    (/* ... políticas normales individuales ... */)
    OR
    -- Para queries bulk: requiere MFA
    (NOT requires_mfa_verification('bulk_read', 'pacientes'))
);
```

---

## 📊 **Performance Impact Analysis**

### **⚡ RLS Performance Optimization:**
```sql
-- Índices optimizados para RLS policies
CREATE INDEX CONCURRENTLY idx_medico_paciente_asignacion_performance
ON medico_paciente_asignacion(medico_id, paciente_id, activa)
WHERE activa = true;

CREATE INDEX CONCURRENTLY idx_usuario_centros_performance
ON usuario_centros(usuario_id, centro_salud_id, activa)
WHERE activa = true;

CREATE INDEX CONCURRENTLY idx_usuarios_rol_centro
ON usuarios(id, rol, centro_salud_id)
WHERE rol IS NOT NULL;

-- Estadísticas específicas para optimizar RLS
CREATE INDEX CONCURRENTLY idx_atenciones_rls_optimization
ON atenciones(medico_id, paciente_id, fecha_atencion)
WHERE fecha_atencion >= CURRENT_DATE - INTERVAL '2 years';
```

### **📈 Performance Monitoring:**
```sql
-- Vista para monitorear impacto de RLS
CREATE VIEW rls_performance_monitor AS
SELECT 
    schemaname,
    tablename,
    COUNT(*) as total_policies,
    
    -- Identificar policies complejas (subconsultas)
    COUNT(*) FILTER (WHERE qual LIKE '%EXISTS%') as complex_policies,
    
    -- Policies por rol
    COUNT(*) FILTER (WHERE 'service_role' = ANY(roles)) as service_role_policies,
    COUNT(*) FILTER (WHERE 'authenticated' = ANY(roles)) as authenticated_policies,
    COUNT(*) FILTER (WHERE 'anon' = ANY(roles)) as anon_policies
    
FROM pg_policies 
WHERE schemaname = 'public'
GROUP BY schemaname, tablename
ORDER BY complex_policies DESC, total_policies DESC;

-- Query para identificar bottlenecks de RLS
SELECT 
    query,
    calls,
    mean_exec_time,
    max_exec_time,
    stddev_exec_time
FROM pg_stat_statements 
WHERE query LIKE '%auth.uid()%' 
   OR query LIKE '%auth.role()%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## 🔧 **Debugging RLS Issues**

### **🐛 Common RLS Problems:**
```sql
-- 1. Verificar que RLS está habilitado
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables t
JOIN pg_class c ON c.relname = t.tablename
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE schemaname = 'public'
AND tablename NOT LIKE 'supabase_%'
ORDER BY tablename;

-- 2. Verificar policies existentes
SELECT 
    schemaname,
    tablename,
    policyname,
    cmd,  -- SELECT, INSERT, UPDATE, DELETE, ALL
    roles,
    qual,  -- USING condition
    with_check  -- WITH CHECK condition
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- 3. Test específico de acceso por rol
-- Ejecutar como diferentes roles para verificar comportamiento
SET ROLE service_role;
SELECT COUNT(*) FROM pacientes;  -- Debe mostrar todos

SET ROLE authenticated; 
SELECT COUNT(*) FROM pacientes;  -- Según policies de authenticated

RESET ROLE;  -- Volver a rol original
```

### **🔍 Debugging Helpers:**
```sql
-- Función para debug de RLS policies
CREATE OR REPLACE FUNCTION debug_rls_access(
    target_table TEXT,
    target_user_id UUID DEFAULT NULL
)
RETURNS TABLE (
    policy_name TEXT,
    policy_cmd TEXT,
    roles TEXT[],
    using_clause TEXT,
    with_check_clause TEXT,
    user_matches BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pp.policyname,
        pp.cmd,
        pp.roles,
        pp.qual,
        pp.with_check,
        (target_user_id IS NOT NULL AND 'authenticated' = ANY(pp.roles)) as user_matches
    FROM pg_policies pp
    WHERE pp.tablename = target_table
    AND pp.schemaname = 'public'
    ORDER BY pp.policyname;
END;
$$ LANGUAGE plpgsql;

-- Uso:
-- SELECT * FROM debug_rls_access('pacientes', auth.uid());
```

---

## 📋 **Compliance y Auditoría**

### **🏥 HABEAS DATA Compliance:**
```sql
-- Registro de consentimientos de datos
CREATE TABLE patient_data_consent (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES pacientes(id),
    consent_type TEXT NOT NULL,  -- 'data_processing', 'research', 'sharing'
    consent_given BOOLEAN NOT NULL,
    consent_date TIMESTAMPTZ NOT NULL,
    consent_expires_at TIMESTAMPTZ,
    consent_withdrawn_at TIMESTAMPTZ,
    
    -- Detalles del consentimiento
    consent_details JSONB,
    legal_basis TEXT,
    witness_user_id UUID REFERENCES usuarios(id),
    
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Policy basada en consentimiento
CREATE POLICY "consent_based_access_patients" ON pacientes
FOR SELECT TO authenticated
USING (
    -- Acceso normal + verificar consentimiento vigente
    (/* ... policies normales ... */)
    AND
    EXISTS (
        SELECT 1 FROM patient_data_consent pdc
        WHERE pdc.paciente_id = pacientes.id
        AND pdc.consent_type = 'data_processing'
        AND pdc.consent_given = true
        AND (pdc.consent_expires_at IS NULL OR pdc.consent_expires_at > NOW())
        AND pdc.consent_withdrawn_at IS NULL
    )
);
```

### **📊 Compliance Reporting:**
```sql
-- Vista para reportes de compliance
CREATE VIEW compliance_security_report AS
SELECT 
    'RLS Coverage' as metric_name,
    COUNT(*) FILTER (WHERE c.relrowsecurity = true) as compliant_tables,
    COUNT(*) as total_tables,
    ROUND(100.0 * COUNT(*) FILTER (WHERE c.relrowsecurity = true) / COUNT(*), 2) as compliance_percentage
FROM pg_tables t
JOIN pg_class c ON c.relname = t.tablename
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE t.schemaname = 'public'
AND t.tablename NOT LIKE 'supabase_%'

UNION ALL

SELECT 
    'Service Role Policies' as metric_name,
    COUNT(DISTINCT pp.tablename) as tables_with_service_policies,
    (SELECT COUNT(DISTINCT tablename) FROM pg_policies WHERE schemaname = 'public') as total_tables_with_policies,
    ROUND(100.0 * COUNT(DISTINCT pp.tablename) / (SELECT COUNT(DISTINCT tablename) FROM pg_policies WHERE schemaname = 'public'), 2)
FROM pg_policies pp
WHERE pp.schemaname = 'public'
AND 'service_role' = ANY(pp.roles)

UNION ALL

SELECT 
    'Authenticated Policies' as metric_name,
    COUNT(*) as authenticated_policies,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public') as total_policies,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public'), 2)
FROM pg_policies pp
WHERE pp.schemaname = 'public'
AND 'authenticated' = ANY(pp.roles);
```

---

## 🚀 **Migration Strategy para RLS**

### **📋 RLS Implementation Checklist:**
```sql
-- Template para habilitar RLS en tabla nueva
CREATE OR REPLACE FUNCTION setup_table_rls(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    -- 1. Habilitar RLS
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', table_name);
    
    -- 2. Service role policy (CRÍTICA)
    EXECUTE format('
        CREATE POLICY "service_role_full_access_%I" ON %I
        FOR ALL TO service_role
        USING (true) WITH CHECK (true)
    ', table_name, table_name);
    
    -- 3. Grants explícitos
    EXECUTE format('GRANT ALL ON %I TO service_role', table_name);
    EXECUTE format('GRANT ALL ON %I TO postgres', table_name);
    
    -- 4. Authenticated basic policy (personalizar después)
    EXECUTE format('
        CREATE POLICY "authenticated_basic_access_%I" ON %I
        FOR SELECT TO authenticated
        USING (true)
    ', table_name, table_name);
    
    RAISE NOTICE 'RLS setup completed for table: %', table_name;
END;
$$ LANGUAGE plpgsql;

-- Uso en migraciones:
-- SELECT setup_table_rls('nueva_tabla');
```

---

**🛡️ RLS Security Model diseñado para máxima protección con usabilidad médica**  
**👥 Maintained by:** Security & Database Architecture Teams  
**🔒 Security level:** Enterprise-grade with healthcare compliance  
**📊 Success metrics:** 100% RLS coverage + 0 security incidents + <5% performance impact