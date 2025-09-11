-- Refinamiento de la granularidad para la tabla detalle_seguimiento_rn

-- 1. Alterar tipo de columna existente en detalle_seguimiento_rn
ALTER TABLE public.detalle_seguimiento_rn
ALTER COLUMN estado_nutricional_rn TYPE public.enum_estado_nutricional
USING estado_nutricional_rn::public.enum_estado_nutricional;

-- 2. Añadir nuevas columnas JSONB a detalle_seguimiento_rn
ALTER TABLE public.detalle_seguimiento_rn
ADD COLUMN antecedentes_seguimiento_rn jsonb,
ADD COLUMN examen_fisico_rn_seguimiento jsonb,
ADD COLUMN plan_cuidado_rn_seguimiento jsonb,
ADD COLUMN tamizajes_rn_pendientes_detalle jsonb; -- Nuevo campo JSONB para detalles de tamizajes pendientes

-- 3. Eliminar la columna antigua de tamizajes_pendientes_rn si era TEXT
-- Asumimos que era TEXT y la reemplazamos por la JSONB para mayor granularidad.
ALTER TABLE public.detalle_seguimiento_rn
DROP COLUMN IF EXISTS tamizajes_pendientes_rn;
