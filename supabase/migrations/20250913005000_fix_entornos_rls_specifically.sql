-- =====================================================================================
-- Fix Specific RLS Issue for entornos_salud_publica
-- Fecha: 2025-01-13
-- Descripción: Arregla específicamente la tabla entornos_salud_publica
-- =====================================================================================

-- Verificar y mostrar estado actual
DO $$
DECLARE
    rls_status BOOLEAN;
    policy_count INTEGER;
BEGIN
    -- Verificar estado RLS
    SELECT rowsecurity INTO rls_status 
    FROM pg_tables 
    WHERE schemaname = 'public' AND tablename = 'entornos_salud_publica';
    
    -- Contar políticas
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE schemaname = 'public' AND tablename = 'entornos_salud_publica';
    
    RAISE NOTICE 'ESTADO ACTUAL entornos_salud_publica:';
    RAISE NOTICE '- RLS habilitado: %', rls_status;
    RAISE NOTICE '- Número de políticas: %', policy_count;
END $$;

-- Limpiar todas las políticas existentes en entornos_salud_publica
DROP POLICY IF EXISTS "Allow full access for service role on entornos" ON entornos_salud_publica;
DROP POLICY IF EXISTS "Allow read access for authenticated users on entornos" ON entornos_salud_publica;
DROP POLICY IF EXISTS "service_role_full_access" ON entornos_salud_publica;
DROP POLICY IF EXISTS "Allow all operations for development" ON entornos_salud_publica;

-- Deshabilitar y re-habilitar RLS para reset completo
ALTER TABLE entornos_salud_publica DISABLE ROW LEVEL SECURITY;
ALTER TABLE entornos_salud_publica ENABLE ROW LEVEL SECURITY;

-- Crear política service_role limpia
CREATE POLICY "service_role_full_access" ON entornos_salud_publica
FOR ALL TO service_role
USING (true) WITH CHECK (true);

-- Verificar resultado
DO $$
DECLARE
    rls_status BOOLEAN;
    policy_count INTEGER;
    policy_names TEXT;
BEGIN
    -- Verificar estado RLS
    SELECT rowsecurity INTO rls_status 
    FROM pg_tables 
    WHERE schemaname = 'public' AND tablename = 'entornos_salud_publica';
    
    -- Contar políticas
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE schemaname = 'public' AND tablename = 'entornos_salud_publica';
    
    -- Obtener nombres de políticas
    SELECT string_agg(policyname, ', ') INTO policy_names
    FROM pg_policies 
    WHERE schemaname = 'public' AND tablename = 'entornos_salud_publica';
    
    RAISE NOTICE 'ESTADO FINAL entornos_salud_publica:';
    RAISE NOTICE '- RLS habilitado: %', rls_status;
    RAISE NOTICE '- Número de políticas: %', policy_count;
    RAISE NOTICE '- Nombres de políticas: %', COALESCE(policy_names, 'ninguna');
    
    IF rls_status AND policy_count = 1 THEN
        RAISE NOTICE 'SUCCESS ✅ - Configuración correcta aplicada';
    ELSE
        RAISE NOTICE 'ERROR ❌ - Configuración incorrecta';
    END IF;
END $$;