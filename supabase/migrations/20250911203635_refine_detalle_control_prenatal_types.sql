-- Crear tipos ENUM para campos específicos en detalle_control_prenatal

-- Tipo para riesgo_biopsicosocial
CREATE TYPE public.enum_riesgo_biopsicosocial AS ENUM (
    'ALTO',
    'MEDIO',
    'BAJO',
    'NO_APLICA',
    'PENDIENTE'
);

-- Tipo para resultados de tamizajes (VIH, Sífilis, Hepatitis B, Toxoplasmosis)
CREATE TYPE public.enum_resultado_tamizaje_serologia AS ENUM (
    'REACTIVO',
    'NO_REACTIVO',
    'INDETERMINADO',
    'PENDIENTE',
    'NO_APLICA'
);

-- Tipo para resultado de tamizaje de Estreptococo B y Urocultivo
CREATE TYPE public.enum_resultado_positivo_negativo AS ENUM (
    'POSITIVO',
    'NEGATIVO',
    'PENDIENTE',
    'NO_APLICA'
);

-- Tipo para hemoclasificacion
CREATE TYPE public.enum_hemoclasificacion AS ENUM (
    'A_POS',
    'A_NEG',
    'B_POS',
    'B_NEG',
    'AB_POS',
    'AB_NEG',
    'O_POS',
    'O_NEG',
    'PENDIENTE',
    'NO_APLICA'
);

-- Alterar columnas en detalle_control_prenatal para usar los nuevos tipos ENUM

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN riesgo_biopsicosocial TYPE public.enum_riesgo_biopsicosocial
USING riesgo_biopsicosocial::public.enum_riesgo_biopsicosocial;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_tamizaje_vih TYPE public.enum_resultado_tamizaje_serologia
USING resultado_tamizaje_vih::public.enum_resultado_tamizaje_serologia;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_tamizaje_sifilis TYPE public.enum_resultado_tamizaje_serologia
USING resultado_tamizaje_sifilis::public.enum_resultado_tamizaje_serologia;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_tamizaje_hepatitis_b TYPE public.enum_resultado_tamizaje_serologia
USING resultado_tamizaje_hepatitis_b::public.enum_resultado_tamizaje_serologia;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_tamizaje_toxoplasmosis TYPE public.enum_resultado_tamizaje_serologia
USING resultado_tamizaje_toxoplasmosis::public.enum_resultado_tamizaje_serologia;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_tamizaje_estreptococo_b TYPE public.enum_resultado_positivo_negativo
USING resultado_tamizaje_estreptococo_b::public.enum_resultado_positivo_negativo;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN hemoclasificacion TYPE public.enum_hemoclasificacion
USING hemoclasificacion::public.enum_hemoclasificacion;

ALTER TABLE public.detalle_control_prenatal
ALTER COLUMN resultado_urocultivo TYPE public.enum_resultado_positivo_negativo
USING resultado_urocultivo::public.enum_resultado_positivo_negativo;
