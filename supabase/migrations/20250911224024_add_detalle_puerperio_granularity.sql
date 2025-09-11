-- Añadir campos de granularidad a la tabla detalle_puerperio

ALTER TABLE public.detalle_puerperio
ADD COLUMN IF NOT EXISTS temperatura_corporal real,
ADD COLUMN IF NOT EXISTS presion_arterial_sistolica integer,
ADD COLUMN IF NOT EXISTS presion_arterial_diastolica integer,
ADD COLUMN IF NOT EXISTS ritmo_cardiaco integer,
ADD COLUMN IF NOT EXISTS frecuencia_respiratoria integer,
ADD COLUMN IF NOT EXISTS perfusion_observaciones text,
ADD COLUMN IF NOT EXISTS estado_conciencia_materna public.enum_estado_conciencia,
ADD COLUMN IF NOT EXISTS involucion_uterina_observaciones text,
ADD COLUMN IF NOT EXISTS loquios_observaciones text,
ADD COLUMN IF NOT EXISTS complicaciones_puerperales jsonb,
ADD COLUMN IF NOT EXISTS deambulacion_temprana boolean,
ADD COLUMN IF NOT EXISTS alimentacion_adecuada_observaciones text,
ADD COLUMN IF NOT EXISTS dificultad_miccional boolean,
ADD COLUMN IF NOT EXISTS cicatriz_cesarea_episiotomia_observaciones text,
ADD COLUMN IF NOT EXISTS vacunacion_esquema_completo_postparto boolean,
ADD COLUMN IF NOT EXISTS inmunoglobulina_anti_d_administrada boolean,
ADD COLUMN IF NOT EXISTS dolor_involucion_uterina boolean,
ADD COLUMN IF NOT EXISTS dificultad_miccional_observaciones text,
ADD COLUMN IF NOT EXISTS signos_alarma_madre_postparto jsonb,
ADD COLUMN IF NOT EXISTS asesoria_anticoncepcion_postparto boolean;