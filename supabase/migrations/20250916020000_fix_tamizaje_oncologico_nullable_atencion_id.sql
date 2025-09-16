-- Migration: Fix tamizaje_oncologico atencion_id nullable for polymorphic pattern
-- Fecha: 16 septiembre 2025
-- Descripción: Hacer atencion_id nullable para permitir patrón polimórfico de 3 pasos

-- Hacer atencion_id NULLABLE para permitir creación por pasos
ALTER TABLE public.tamizaje_oncologico 
ALTER COLUMN atencion_id DROP NOT NULL;

-- Añadir comentario explicativo
COMMENT ON COLUMN public.tamizaje_oncologico.atencion_id IS 
'Foreign key to atenciones table. Nullable to support polymorphic pattern: 
 create tamizaje_oncologico first, then create atencion record referencing this tamizaje';

-- Verificar el cambio
SELECT 
    column_name, 
    is_nullable, 
    data_type 
FROM information_schema.columns 
WHERE table_name = 'tamizaje_oncologico' 
AND column_name = 'atencion_id';

-- Agregar campos faltantes para compatibilidad con modelo actualizado
ALTER TABLE public.tamizaje_oncologico 
ADD COLUMN IF NOT EXISTS recomendaciones text,
ADD COLUMN IF NOT EXISTS fecha_proximo_control date,
ADD COLUMN IF NOT EXISTS requiere_seguimiento_especializado boolean DEFAULT false;

-- Comentarios para nuevos campos
COMMENT ON COLUMN public.tamizaje_oncologico.recomendaciones IS 'Recomendaciones específicas para el paciente';
COMMENT ON COLUMN public.tamizaje_oncologico.fecha_proximo_control IS 'Fecha para próximo control médico';
COMMENT ON COLUMN public.tamizaje_oncologico.requiere_seguimiento_especializado IS 'Si requiere derivación a especialista';

-- Nota: SUCCESS mensaje
SELECT 'SUCCESS: atencion_id is now nullable in tamizaje_oncologico, campos adicionales agregados' as message;