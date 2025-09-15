-- =============================================================================
-- Fix: Corregir trigger para usar 'updated_at' en lugar de 'actualizado_en'
-- Fecha: 15 septiembre 2025
-- =============================================================================

BEGIN;

-- Corregir función de trigger para usar el campo correcto
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Verificar que el trigger usa la función corregida
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_atencion_primera_infancia_updated_at') THEN
        RAISE NOTICE '✅ Trigger existe, función actualizada para usar updated_at';
    ELSE
        RAISE NOTICE '⚠️ Trigger no encontrado, creándolo...';
        CREATE TRIGGER update_atencion_primera_infancia_updated_at
            BEFORE UPDATE ON atencion_primera_infancia
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

COMMIT;