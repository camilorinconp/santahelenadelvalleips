-- =====================================================================================
-- Fix Inconsistent RLS Configuration - Standardize All Tables
-- Fecha: 2025-01-13
-- Descripción: Corrige configuración inconsistente de RLS en todas las tablas
-- Problema: Tablas con RLS deshabilitado pero políticas activas (estado inconsistente)
-- =====================================================================================

-- ====================
-- DIAGNÓSTICO DEL PROBLEMA
-- ====================
-- Problema identificado: Tablas con RLS DISABLED pero con políticas activas
-- Esto causa comportamiento impredecible y errores intermitentes
-- Solución: Estandarizar configuración para desarrollo

-- ====================
-- OPCIÓN A: DESARROLLO ABIERTO (APLICADA)
-- ====================
-- Para desarrollo, deshabilitamos RLS completamente y eliminamos políticas conflictivas
-- Esto asegura comportamiento consistente y predecible

-- Tablas problemáticas identificadas
ALTER TABLE atencion_materno_perinatal DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_control_prenatal DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_parto DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_recien_nacido DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_puerperio DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_salud_bucal_mp DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_nutricion_mp DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_ive DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_curso_maternidad_paternidad DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_seguimiento_rn DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_preconcepcional_anamnesis DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_preconcepcional_paraclinicos DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_preconcepcional_antropometria DISABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_rn_atencion_inmediata DISABLE ROW LEVEL SECURITY;

-- Eliminar políticas de desarrollo conflictivas
DROP POLICY IF EXISTS "atencion_materno_perinatal_dev_policy" ON atencion_materno_perinatal;
DROP POLICY IF EXISTS "detalle_control_prenatal_dev_policy" ON detalle_control_prenatal;
DROP POLICY IF EXISTS "detalle_parto_dev_policy" ON detalle_parto;
DROP POLICY IF EXISTS "detalle_recien_nacido_dev_policy" ON detalle_recien_nacido;
DROP POLICY IF EXISTS "detalle_puerperio_dev_policy" ON detalle_puerperio;
DROP POLICY IF EXISTS "detalle_salud_bucal_mp_dev_policy" ON detalle_salud_bucal_mp;
DROP POLICY IF EXISTS "detalle_nutricion_mp_dev_policy" ON detalle_nutricion_mp;
DROP POLICY IF EXISTS "detalle_ive_dev_policy" ON detalle_ive;
DROP POLICY IF EXISTS "detalle_curso_maternidad_paternidad_dev_policy" ON detalle_curso_maternidad_paternidad;
DROP POLICY IF EXISTS "detalle_seguimiento_rn_dev_policy" ON detalle_seguimiento_rn;
DROP POLICY IF EXISTS "detalle_preconcepcional_anamnesis_dev_policy" ON detalle_preconcepcional_anamnesis;
DROP POLICY IF EXISTS "detalle_preconcepcional_paraclinicos_dev_policy" ON detalle_preconcepcional_paraclinicos;
DROP POLICY IF EXISTS "detalle_preconcepcional_antropometria_dev_policy" ON detalle_preconcepcional_antropometria;
DROP POLICY IF EXISTS "detalle_rn_atencion_inmediata_dev_policy" ON detalle_rn_atencion_inmediata;

-- Verificar y corregir tablas principales
ALTER TABLE atenciones DISABLE ROW LEVEL SECURITY;
ALTER TABLE pacientes DISABLE ROW LEVEL SECURITY;
ALTER TABLE medicos DISABLE ROW LEVEL SECURITY;
ALTER TABLE atencion_primera_infancia DISABLE ROW LEVEL SECURITY;
ALTER TABLE control_cronicidad DISABLE ROW LEVEL SECURITY;
ALTER TABLE control_hipertension_detalles DISABLE ROW LEVEL SECURITY;
ALTER TABLE tamizaje_oncologico DISABLE ROW LEVEL SECURITY;
ALTER TABLE intervenciones_colectivas DISABLE ROW LEVEL SECURITY;

-- Mantener las tablas transversales como están (ya configuradas correctamente)
-- entornos_salud_publica - ya deshabilitado en migración anterior
-- familia_integral_salud_publica - ya deshabilitado en migración anterior  
-- atencion_integral_transversal_salud - ya deshabilitado en migración anterior

-- ====================
-- CONFIGURACIÓN PARA FUTURO (PRODUCCIÓN)
-- ====================
-- COMENTADO: Para producción futura, usar esta configuración
-- 
-- -- Habilitar RLS en tablas críticas
-- ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE atenciones ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE atencion_materno_perinatal ENABLE ROW LEVEL SECURITY;
-- 
-- -- Crear políticas de producción restrictivas
-- CREATE POLICY "Allow authenticated users" ON pacientes
-- FOR ALL TO authenticated
-- USING (auth.uid() IS NOT NULL);
-- 
-- CREATE POLICY "Allow service role full access" ON pacientes  
-- FOR ALL TO service_role
-- USING (true);

-- ====================
-- VERIFICACIÓN POST-MIGRACIÓN
-- ====================
-- Query para verificar estado de RLS después de la migración:
-- SELECT schemaname, tablename, rowsecurity 
-- FROM pg_tables 
-- WHERE schemaname = 'public' 
-- ORDER BY tablename;

-- ====================
-- LOG DE FINALIZACIÓN
-- ====================
DO $$ 
BEGIN 
    RAISE NOTICE '=== RLS CONFIGURATION STANDARDIZED ===';
    RAISE NOTICE 'Problema resuelto: Configuración RLS inconsistente';
    RAISE NOTICE 'Estado actual: RLS DISABLED en todas las tablas para desarrollo';
    RAISE NOTICE 'Políticas conflictivas eliminadas';
    RAISE NOTICE 'Comportamiento ahora es consistente y predecible';
    RAISE NOTICE 'Para producción: Habilitar RLS y crear políticas restrictivas';
END $$;