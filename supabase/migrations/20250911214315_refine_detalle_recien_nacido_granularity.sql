-- Refinamiento de la granularidad para la tabla detalle_recien_nacido con polimorfismo anidado.

-- 1. Crear nuevos tipos ENUM

-- Tipo para alimentacion_egreso
CREATE TYPE public.enum_alimentacion_egreso AS ENUM (
    'LACTANCIA_MATERNA_EXCLUSIVA',
    'FORMULA',
    'MIXTA',
    'PENDIENTE',
    'NO_APLICA'
);

-- Tipo para tipo_pinzamiento_cordon
CREATE TYPE public.enum_tipo_pinzamiento_cordon AS ENUM (
    'INMEDIATO',
    'TARDIO',
    'NO_APLICA'
);

-- Tipo para metodo_identificacion_rn
CREATE TYPE public.enum_metodo_identificacion_rn AS ENUM (
    'BRAZALETE',
    'HUELLA_PLANTAR',
    'FOTO',
    'OTRO',
    'PENDIENTE',
    'NO_APLICA'
);

-- 2. Crear la nueva tabla de sub-sub-detalle: detalle_rn_atencion_inmediata

CREATE TABLE public.detalle_rn_atencion_inmediata (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    detalle_recien_nacido_id uuid NOT NULL REFERENCES public.detalle_recien_nacido(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Campos específicos de la atención inmediata en sala de partos
    limpieza_vias_aereas_realizada boolean,
    secado_rn_realizado boolean,
    observacion_respiracion_llanto_tono text,
    tipo_pinzamiento_cordon public.enum_tipo_pinzamiento_cordon,
    contacto_piel_a_piel_realizado boolean,
    manejo_termico_observaciones text,
    metodo_identificacion_rn public.enum_metodo_identificacion_rn,
    registro_nacido_vivo_realizado boolean,
    examen_fisico_rn_observaciones text
);
COMMENT ON TABLE public.detalle_rn_atencion_inmediata IS 'Detalles específicos de la atención inmediata del recién nacido en sala de partos.';


-- 3. Modificar la tabla principal 'detalle_recien_nacido'

ALTER TABLE public.detalle_recien_nacido
ADD COLUMN sub_tipo_rn_atencion text,
ADD COLUMN sub_detalle_rn_id uuid;

COMMENT ON COLUMN public.detalle_recien_nacido.sub_tipo_rn_atencion IS 'Tipo de sub-atención dentro del cuidado del recién nacido (ej. ATENCION_INMEDIATA, CUIDADOS_24H, SEGUIMIENTO).';


-- 4. Eliminar las columnas antiguas de detalle_recien_nacido que ahora están en sub-tablas
-- ADVERTENCIA: Esto es una operación destructiva de columnas. Se asume que no hay datos que migrar en este punto.

ALTER TABLE public.detalle_recien_nacido
DROP COLUMN IF EXISTS adaptacion_neonatal_observaciones,
DROP COLUMN IF EXISTS tamizaje_auditivo_neonatal,
DROP COLUMN IF EXISTS tamizaje_metabolico_neonatal,
DROP COLUMN IF EXISTS tamizaje_cardiopatias_congenitas,
DROP COLUMN IF EXISTS profilaxis_vitamina_k,
DROP COLUMN IF EXISTS profilaxis_ocular,
DROP COLUMN IF EXISTS vacunacion_bcg,
DROP COLUMN IF EXISTS vacunacion_hepatitis_b;

-- 5. Alterar tipo de columna existente en detalle_recien_nacido

ALTER TABLE public.detalle_recien_nacido
ALTER COLUMN alimentacion_egreso TYPE public.enum_alimentacion_egreso
USING alimentacion_egreso::public.enum_alimentacion_egreso;
