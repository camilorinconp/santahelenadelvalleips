-- =============================================================================
-- Remoción de Triggers Complejos - Fix para Sistema Consolidado
-- Elimina triggers de alertas que causan errores con campos inexistentes
-- Fecha: 15 septiembre 2025
-- =============================================================================

BEGIN;

-- Remover trigger de alertas automáticas (sistema expandido)
DROP TRIGGER IF EXISTS trigger_alertas_primera_infancia ON atencion_primera_infancia;
DROP FUNCTION IF EXISTS trigger_generar_alertas_primera_infancia();

-- Remover otras funciones complejas si existen
DROP FUNCTION IF EXISTS calcular_alertas_desarrollo(UUID);
DROP FUNCTION IF EXISTS evaluar_riesgo_nutricional(UUID);
DROP FUNCTION IF EXISTS generar_alertas_vacunacion(UUID);

-- Verificar que no queden triggers problemáticos
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger t 
               JOIN pg_class c ON t.tgrelid = c.oid 
               WHERE c.relname = 'atencion_primera_infancia' 
               AND t.tgname LIKE '%alerta%') THEN
        RAISE NOTICE 'ADVERTENCIA: Aún existen triggers de alertas';
    ELSE
        RAISE NOTICE '✅ SUCCESS: Triggers de alertas removidos exitosamente';
    END IF;
END $$;

COMMIT;