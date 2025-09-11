-- Refinamiento de la granularidad para la tabla detalle_puerperio

-- 1. Crear nuevo tipo ENUM

-- Tipo para metodo_anticonceptivo_postparto
CREATE TYPE public.enum_metodo_anticonceptivo_postparto AS ENUM (
    'DIU_POSPARTO',
    'OTB', -- Oclusión Tubárica Bilateral
    'IMPLANTE_SUBDERMICO',
    'INYECTABLE',
    'ORAL_PROGESTINA',
    'CONDONES',
    'NINGUNO',
    'PENDIENTE',
    'NO_APLICA'
);

-- 2. Añadir nuevas columnas a detalle_puerperio

ALTER TABLE public.detalle_puerperio
ADD COLUMN temperatura_corporal real,
ADD COLUMN presion_arterial_sistolica integer,
ADD COLUMN presion_arterial_diastolica integer,
ADD COLUMN ritmo_cardiaco integer,
ADD COLUMN frecuencia_respiratoria integer,
ADD COLUMN perfusion_observaciones text,
ADD COLUMN estado_conciencia_materna public.enum_estado_conciencia,
ADD COLUMN involucion_uterina_observaciones text,
ADD COLUMN loquios_observaciones text,
ADD COLUMN complicaciones_puerperales jsonb,
ADD COLUMN deambulacion_temprana boolean,
ADD COLUMN alimentacion_adecuada_observaciones text,
ADD COLUMN dificultad_miccional boolean,
ADD COLUMN cicatriz_cesarea_episiotomia_observaciones text,
ADD COLUMN vacunacion_esquema_completo_postparto boolean,
ADD COLUMN inmunoglobulina_anti_d_administrada boolean,
ADD COLUMN dolor_involucion_uterina boolean,
ADD COLUMN dificultad_miccional_observaciones text,
ADD COLUMN signos_alarma_madre_postparto jsonb,
ADD COLUMN asesoria_anticoncepcion_postparto boolean;

-- 3. Alterar tipo de columna existente en detalle_puerperio

ALTER TABLE public.detalle_puerperio
ALTER COLUMN metodo_anticonceptivo_postparto TYPE public.enum_metodo_anticonceptivo_postparto
USING metodo_anticonceptivo_postparto::public.enum_metodo_anticonceptivo_postparto;
