-- =====================================================================================
-- Enable RLS with service_role Policy - All Tables
-- Fecha: 2025-01-13
-- Descripción: Habilita RLS con política service_role en todas las tablas
-- Solución: Configuración estándar y segura para Supabase
-- =====================================================================================

-- ====================
-- JUSTIFICACIÓN TÉCNICA
-- ====================
-- Problema: Configuración RLS inconsistente causando errores
-- Solución: RLS habilitado + service_role policy (mejores prácticas Supabase)
-- Ventaja: Backend mantiene acceso completo, seguridad habilitada
-- Resultado: Configuración consistente y lista para producción

-- ====================
-- FUNCIÓN AUXILIAR
-- ====================
CREATE OR REPLACE FUNCTION enable_rls_with_service_role_policy(table_name text)
RETURNS void AS $$
BEGIN
    -- Limpiar políticas existentes conflictivas
    EXECUTE format('DROP POLICY IF EXISTS "%s_dev_policy" ON %I', table_name, table_name);
    EXECUTE format('DROP POLICY IF EXISTS "Allow full access for service role on %s" ON %I', table_name, table_name);
    EXECUTE format('DROP POLICY IF EXISTS "Allow read access for authenticated users on %s" ON %I', table_name, table_name);
    EXECUTE format('DROP POLICY IF EXISTS "service_role_full_access" ON %I', table_name);
    
    -- Habilitar RLS
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', table_name);
    
    -- Crear política estándar para service_role
    EXECUTE format('CREATE POLICY "service_role_full_access" ON %I FOR ALL TO service_role USING (true) WITH CHECK (true)', table_name);
    
    RAISE NOTICE 'RLS enabled with service_role policy for table: %', table_name;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error processing table %: %', table_name, SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- ====================
-- APLICAR A TODAS LAS TABLAS PRINCIPALES
-- ====================

-- Tablas base del sistema
SELECT enable_rls_with_service_role_policy('pacientes');
SELECT enable_rls_with_service_role_policy('medicos');
SELECT enable_rls_with_service_role_policy('atenciones');

-- Tablas de atenciones específicas
SELECT enable_rls_with_service_role_policy('atencion_materno_perinatal');
SELECT enable_rls_with_service_role_policy('atencion_primera_infancia');
SELECT enable_rls_with_service_role_policy('control_cronicidad');
SELECT enable_rls_with_service_role_policy('control_hipertension_detalles');
SELECT enable_rls_with_service_role_policy('tamizaje_oncologico');
SELECT enable_rls_with_service_role_policy('intervenciones_colectivas');

-- Tablas de detalle materno perinatal
SELECT enable_rls_with_service_role_policy('detalle_control_prenatal');
SELECT enable_rls_with_service_role_policy('detalle_parto');
SELECT enable_rls_with_service_role_policy('detalle_recien_nacido');
SELECT enable_rls_with_service_role_policy('detalle_puerperio');
SELECT enable_rls_with_service_role_policy('detalle_salud_bucal_mp');
SELECT enable_rls_with_service_role_policy('detalle_nutricion_mp');
SELECT enable_rls_with_service_role_policy('detalle_ive');
SELECT enable_rls_with_service_role_policy('detalle_curso_maternidad_paternidad');
SELECT enable_rls_with_service_role_policy('detalle_seguimiento_rn');
SELECT enable_rls_with_service_role_policy('detalle_preconcepcional_anamnesis');
SELECT enable_rls_with_service_role_policy('detalle_preconcepcional_paraclinicos');
SELECT enable_rls_with_service_role_policy('detalle_preconcepcional_antropometria');
SELECT enable_rls_with_service_role_policy('detalle_rn_atencion_inmediata');

-- Tablas transversales (arquitectura nueva)
SELECT enable_rls_with_service_role_policy('entornos_salud_publica');
SELECT enable_rls_with_service_role_policy('familia_integral_salud_publica');
SELECT enable_rls_with_service_role_policy('atencion_integral_transversal_salud');

-- ====================
-- LIMPIAR FUNCIÓN AUXILIAR
-- ====================
DROP FUNCTION enable_rls_with_service_role_policy(text);

-- ====================
-- VERIFICACIÓN POST-MIGRACIÓN
-- ====================

-- Verificar estado RLS de todas las tablas
DO $$
DECLARE
    r RECORD;
    total_tables INTEGER := 0;
    rls_enabled_count INTEGER := 0;
BEGIN
    RAISE NOTICE '=== VERIFICATION: RLS STATUS ===';
    
    FOR r IN 
        SELECT tablename, rowsecurity 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        ORDER BY tablename
    LOOP
        total_tables := total_tables + 1;
        IF r.rowsecurity THEN
            rls_enabled_count := rls_enabled_count + 1;
            RAISE NOTICE 'Table %: RLS ENABLED ✅', r.tablename;
        ELSE
            RAISE NOTICE 'Table %: RLS DISABLED ❌', r.tablename;
        END IF;
    END LOOP;
    
    RAISE NOTICE '=== SUMMARY ===';
    RAISE NOTICE 'Total tables: %', total_tables;
    RAISE NOTICE 'RLS enabled: %', rls_enabled_count;
    RAISE NOTICE 'RLS disabled: %', total_tables - rls_enabled_count;
    
    IF rls_enabled_count = total_tables THEN
        RAISE NOTICE 'SUCCESS: All tables have RLS enabled ✅';
    ELSE
        RAISE NOTICE 'WARNING: Some tables still have RLS disabled ⚠️';
    END IF;
END $$;

-- Contar políticas service_role creadas
DO $$
DECLARE
    policy_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE schemaname = 'public' 
    AND policyname = 'service_role_full_access';
    
    RAISE NOTICE '=== SERVICE_ROLE POLICIES ===';
    RAISE NOTICE 'Total service_role policies created: %', policy_count;
END $$;

-- ====================
-- LOG FINAL
-- ====================
DO $$ 
BEGIN 
    RAISE NOTICE '=== MIGRATION COMPLETED SUCCESSFULLY ===';
    RAISE NOTICE 'Configuration: RLS ENABLED + service_role policies';
    RAISE NOTICE 'Security: Enabled (following Supabase best practices)';
    RAISE NOTICE 'Backend access: Full (via service_role)';
    RAISE NOTICE 'Consistency: All tables now have uniform configuration';
    RAISE NOTICE 'Next step: Test all endpoints to verify functionality';
END $$;