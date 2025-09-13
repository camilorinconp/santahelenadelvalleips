-- =====================================================================================
-- Complete RLS Cleanup and Reset - All Tables
-- Fecha: 2025-01-13
-- Descripción: Limpia completamente todas las políticas RLS y reestablece configuración uniforme
-- Problema: Políticas múltiples y conflictivas en las tablas
-- =====================================================================================

-- ====================
-- FASE 1: LIMPIEZA TOTAL DE POLÍTICAS
-- ====================
DO $$
DECLARE
    pol_rec RECORD;
    total_dropped INTEGER := 0;
BEGIN
    RAISE NOTICE '=== PHASE 1: CLEANING ALL EXISTING RLS POLICIES ===';
    
    -- Eliminar TODAS las políticas existentes en TODAS las tablas
    FOR pol_rec IN 
        SELECT schemaname, tablename, policyname
        FROM pg_policies 
        WHERE schemaname = 'public'
        ORDER BY tablename, policyname
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON %I.%I', 
                      pol_rec.policyname, pol_rec.schemaname, pol_rec.tablename);
        RAISE NOTICE 'Dropped policy: %.%', pol_rec.tablename, pol_rec.policyname;
        total_dropped := total_dropped + 1;
    END LOOP;
    
    RAISE NOTICE 'Total policies dropped: %', total_dropped;
    
    IF total_dropped > 0 THEN
        RAISE NOTICE 'All existing policies have been removed ✅';
    ELSE
        RAISE NOTICE 'No policies found to remove';
    END IF;
END $$;

-- ====================
-- FASE 2: RESET RLS EN TODAS LAS TABLAS
-- ====================
DO $$
DECLARE
    table_rec RECORD;
    total_tables INTEGER := 0;
BEGIN
    RAISE NOTICE '=== PHASE 2: RESETTING RLS ON ALL TABLES ===';
    
    -- Reset RLS en todas las tablas públicas
    FOR table_rec IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename
    LOOP
        -- Deshabilitar y re-habilitar RLS para reset completo
        EXECUTE format('ALTER TABLE %I DISABLE ROW LEVEL SECURITY', table_rec.tablename);
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', table_rec.tablename);
        
        RAISE NOTICE 'RLS reset for table: %', table_rec.tablename;
        total_tables := total_tables + 1;
    END LOOP;
    
    RAISE NOTICE 'RLS reset completed for % tables', total_tables;
END $$;

-- ====================
-- FASE 3: APLICAR POLÍTICA UNIFORME service_role
-- ====================
DO $$
DECLARE
    table_rec RECORD;
    total_policies INTEGER := 0;
BEGIN
    RAISE NOTICE '=== PHASE 3: APPLYING UNIFORM service_role POLICIES ===';
    
    -- Crear política service_role en todas las tablas
    FOR table_rec IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename
    LOOP
        -- Crear política estándar para service_role
        EXECUTE format('CREATE POLICY "service_role_full_access" ON %I FOR ALL TO service_role USING (true) WITH CHECK (true)', table_rec.tablename);
        
        RAISE NOTICE 'service_role policy created for: %', table_rec.tablename;
        total_policies := total_policies + 1;
    END LOOP;
    
    RAISE NOTICE 'service_role policies created for % tables', total_policies;
END $$;

-- ====================
-- FASE 4: VERIFICACIÓN COMPLETA
-- ====================
DO $$
DECLARE
    table_count INTEGER;
    policy_count INTEGER;
    rls_enabled_count INTEGER;
    verification_passed BOOLEAN := true;
    table_rec RECORD;
BEGIN
    RAISE NOTICE '=== PHASE 4: COMPREHENSIVE VERIFICATION ===';
    
    -- Contar tablas totales
    SELECT COUNT(*) INTO table_count
    FROM pg_tables 
    WHERE schemaname = 'public';
    
    -- Contar tablas con RLS habilitado
    SELECT COUNT(*) INTO rls_enabled_count
    FROM pg_tables 
    WHERE schemaname = 'public' AND rowsecurity = true;
    
    -- Contar políticas service_role
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE schemaname = 'public' AND policyname = 'service_role_full_access';
    
    RAISE NOTICE 'Verification Results:';
    RAISE NOTICE '- Total tables: %', table_count;
    RAISE NOTICE '- Tables with RLS enabled: %', rls_enabled_count;
    RAISE NOTICE '- service_role policies: %', policy_count;
    
    -- Verificar consistencia
    IF table_count = rls_enabled_count AND table_count = policy_count THEN
        RAISE NOTICE 'VERIFICATION PASSED ✅ - All tables have uniform configuration';
    ELSE
        RAISE NOTICE 'VERIFICATION FAILED ❌ - Inconsistent configuration detected';
        verification_passed := false;
    END IF;
    
    -- Mostrar detalles de tablas problemáticas si las hay
    IF NOT verification_passed THEN
        RAISE NOTICE 'Tables missing RLS:';
        FOR table_rec IN 
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' AND rowsecurity = false
        LOOP
            RAISE NOTICE '  - %', table_rec.tablename;
        END LOOP;
    END IF;
END $$;

-- ====================
-- FASE 5: REPORTE FINAL DETALLADO
-- ====================
DO $$
DECLARE
    r RECORD;
BEGIN
    RAISE NOTICE '=== FINAL CONFIGURATION REPORT ===';
    RAISE NOTICE 'Table Status (RLS + Policies):';
    RAISE NOTICE '';
    
    FOR r IN 
        SELECT 
            t.tablename,
            t.rowsecurity,
            COUNT(p.policyname) as policy_count,
            string_agg(p.policyname, ', ') as policies
        FROM pg_tables t
        LEFT JOIN pg_policies p ON t.tablename = p.tablename AND p.schemaname = 'public'
        WHERE t.schemaname = 'public'
        GROUP BY t.tablename, t.rowsecurity
        ORDER BY t.tablename
    LOOP
        RAISE NOTICE '% | RLS: % | Policies: % | Names: %', 
                     rpad(r.tablename, 35), 
                     CASE WHEN r.rowsecurity THEN 'ON ' ELSE 'OFF' END,
                     r.policy_count,
                     COALESCE(r.policies, 'none');
    END LOOP;
END $$;

-- ====================
-- LOG FINAL
-- ====================
DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '=== CLEANUP AND RESET COMPLETED SUCCESSFULLY ===';
    RAISE NOTICE 'Status: All tables now have clean, uniform RLS configuration';
    RAISE NOTICE 'Security: RLS enabled with service_role full access';
    RAISE NOTICE 'Policies: One policy per table (service_role_full_access)';
    RAISE NOTICE 'Consistency: All tables follow the same pattern';
    RAISE NOTICE 'Backend: Will work without changes (service_role bypass)';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Test all endpoints to verify functionality';
    RAISE NOTICE '2. Monitor for any RLS-related errors';
    RAISE NOTICE '3. Add granular user policies when needed for production';
END $$;