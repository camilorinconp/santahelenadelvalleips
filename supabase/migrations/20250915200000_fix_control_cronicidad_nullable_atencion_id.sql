-- =============================================================================
-- Migración: Corregir Control Cronicidad para soportar patrón polimórfico
-- Fecha: 15 septiembre 2025
-- Descripción: Hacer atencion_id NULLABLE en control_cronicidad para permitir 
--              el patrón polimórfico de creación (detalle primero, luego atención)
-- =============================================================================

-- 1. Hacer atencion_id NULLABLE para permitir creación por pasos
ALTER TABLE public.control_cronicidad 
ALTER COLUMN atencion_id DROP NOT NULL;

-- 2. Añadir comentario explicativo
COMMENT ON COLUMN public.control_cronicidad.atencion_id IS 
'Foreign key to atenciones table. Nullable to support polymorphic pattern: create control_cronicidad first, then create atencion record referencing this control';

-- 3. Verificar que la estructura esté correcta
DO $$
BEGIN
    -- Verificar que la columna ahora es nullable
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'control_cronicidad' 
        AND column_name = 'atencion_id' 
        AND is_nullable = 'YES'
    ) THEN
        RAISE NOTICE 'SUCCESS: atencion_id is now nullable in control_cronicidad';
    ELSE
        RAISE EXCEPTION 'ERROR: atencion_id is still NOT NULL in control_cronicidad';
    END IF;
END $$;