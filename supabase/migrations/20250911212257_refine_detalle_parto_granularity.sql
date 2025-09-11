-- Refinamiento de la granularidad para la tabla detalle_parto

-- 1. Crear nuevos tipos ENUM

-- Tipo para tipo_parto
CREATE TYPE public.enum_tipo_parto AS ENUM (
    'VAGINAL',
    'CESAREA',
    'INSTRUMENTADO',
    'OTRO',
    'PENDIENTE'
);

-- Tipo para manejo_alumbramiento
CREATE TYPE public.enum_manejo_alumbramiento AS ENUM (
    'ACTIVO',
    'FISIOLOGICO',
    'NO_APLICA',
    'PENDIENTE'
);

-- Tipo para estado_conciencia
CREATE TYPE public.enum_estado_conciencia AS ENUM (
    'ALERTA',
    'SOMNOLIENTA',
    'CONFUSA',
    'COMA',
    'PENDIENTE',
    'NO_APLICA'
);

-- Tipo para via_administracion (reutilizable)
CREATE TYPE public.enum_via_administracion AS ENUM (
    'IM',
    'IV',
    'SUBLINGUAL',
    'ORAL',
    'NO_APLICA',
    'PENDIENTE'
);


-- 2. Añadir nuevas columnas a detalle_parto

ALTER TABLE public.detalle_parto
ADD COLUMN inicio_contracciones timestamp with time zone,
ADD COLUMN percepcion_movimientos_fetales boolean,
ADD COLUMN expulsion_tapon_mucoso boolean,
ADD COLUMN ruptura_membranas boolean,
ADD COLUMN sangrado_vaginal text, -- Considerar JSONB o ENUM si se definen categorías
ADD COLUMN sintomas_preeclampsia_premonitorios jsonb,
ADD COLUMN antecedentes_patologicos_parto text,
ADD COLUMN estado_conciencia_materna public.enum_estado_conciencia,
ADD COLUMN estado_nutricional_materna public.enum_estado_nutricional,
ADD COLUMN signos_vitales_maternos jsonb,
ADD COLUMN valoracion_obstetrica_observaciones text,
ADD COLUMN valoracion_ginecologica_observaciones text,
ADD COLUMN resultado_prueba_treponemica_rapida public.enum_resultado_tamizaje_serologia,
ADD COLUMN resultado_vdrl_rpr public.enum_resultado_tamizaje_serologia,
ADD COLUMN resultado_gota_gruesa_malaria public.enum_resultado_positivo_negativo,
ADD COLUMN resultado_hematocrito real,
ADD COLUMN resultado_hemoglobina real,
ADD COLUMN resultado_antigeno_hepatitis_b public.enum_resultado_tamizaje_serologia,
ADD COLUMN pinzamiento_cordon_tardio boolean,
ADD COLUMN oxitocina_administrada_ui real,
ADD COLUMN oxitocina_via public.enum_via_administracion,
ADD COLUMN misoprostol_administrado_mcg real,
ADD COLUMN misoprostol_via public.enum_via_administracion,
ADD COLUMN traccion_cordon_controlada boolean,
ADD COLUMN utero_contraido_postparto boolean;


-- 3. Alterar tipos de columnas existentes en detalle_parto

ALTER TABLE public.detalle_parto
ALTER COLUMN tipo_parto TYPE public.enum_tipo_parto
USING tipo_parto::public.enum_tipo_parto;

ALTER TABLE public.detalle_parto
ALTER COLUMN manejo_alumbramiento TYPE public.enum_manejo_alumbramiento
USING manejo_alumbramiento::public.enum_manejo_alumbramiento;
