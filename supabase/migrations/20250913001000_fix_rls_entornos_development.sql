-- =====================================================================================
-- Fix RLS Policies for Entornos de Salud Pública - Development Environment
-- Fecha: 2025-01-13
-- Descripción: Ajusta políticas RLS para permitir operaciones en desarrollo
-- =====================================================================================

-- Deshabilitar temporalmente RLS para desarrollo
ALTER TABLE entornos_salud_publica DISABLE ROW LEVEL SECURITY;

-- Alternativamente, crear políticas permisivas para desarrollo
-- ALTER TABLE entornos_salud_publica ENABLE ROW LEVEL SECURITY;

-- DROP POLICY IF EXISTS "Allow full access for service role on entornos" ON entornos_salud_publica;
-- DROP POLICY IF EXISTS "Allow read access for authenticated users on entornos" ON entornos_salud_publica;

-- CREATE POLICY "Allow all operations for development" ON entornos_salud_publica
-- FOR ALL USING (true) WITH CHECK (true);

-- Log de finalización
DO $$ 
BEGIN 
    RAISE NOTICE 'RLS policies updated for entornos_salud_publica - Development mode enabled';
END $$;