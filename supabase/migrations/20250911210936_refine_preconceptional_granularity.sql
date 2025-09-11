-- Refinamiento de la granularidad para la atención preconcepcional con polimorfismo anidado.

-- 1. Definir nuevos tipos ENUM
CREATE TYPE public.enum_estado_nutricional AS ENUM (
    'NORMAL',
    'SOBREPESO',
    'OBESIDAD',
    'BAJO_PESO',
    'PENDIENTE',
    'NO_APLICA'
);

-- 2. Crear las nuevas tablas de sub-sub-detalle

-- Tabla para Anamnesis Preconcepcional
CREATE TABLE public.detalle_preconcepcional_anamnesis (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    detalle_control_prenatal_id uuid NOT NULL REFERENCES public.detalle_control_prenatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Antecedentes personales/clínicos
    antecedente_trombofilias boolean,
    antecedente_anemia boolean,
    antecedente_asma boolean,
    antecedente_tuberculosis boolean,
    antecedente_neoplasias boolean,
    antecedente_obesidad_morbida boolean,
    antecedente_patologia_cervical_vph boolean,
    antecedente_cumplimiento_tamizaje_ccu boolean,
    antecedente_numero_companeros_sexuales integer,
    antecedente_uso_preservativo boolean,
    antecedente_uso_anticonceptivos boolean,
    -- Antecedentes gineco-obstétricos
    antecedente_parto_pretermito_previo boolean,
    antecedente_cesarea_previa boolean,
    antecedente_abortos_previos integer,
    antecedente_muerte_fetal_previa boolean,
    antecedente_gran_multiparidad boolean,
    antecedente_periodo_intergenesico_corto boolean,
    antecedente_incompatibilidad_rh boolean,
    antecedente_preeclampsia_gestacion_anterior boolean,
    antecedente_rn_peso_menor_2500g boolean,
    antecedente_rn_macrosomico boolean,
    antecedente_hemorragia_postparto_previo boolean,
    antecedente_embarazo_molar boolean,
    antecedente_depresion_postparto_previo boolean
);
COMMENT ON TABLE public.detalle_preconcepcional_anamnesis IS 'Detalles de anamnesis para atención preconcepcional.';

-- Tabla para Exámenes Paraclínicos Preconcepcionales
CREATE TABLE public.detalle_preconcepcional_paraclinicos (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    detalle_control_prenatal_id uuid NOT NULL REFERENCES public.detalle_control_prenatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Resultados de exámenes paraclínicos
    resultado_glicemia_ayunas real,
    resultado_hemograma text,
    resultado_igg_varicela public.enum_resultado_tamizaje_serologia,
    resultado_tamizaje_ccu text
);
COMMENT ON TABLE public.detalle_preconcepcional_paraclinicos IS 'Resultados de exámenes paraclínicos para atención preconcepcional.';

-- Tabla para Antropometría Preconcepcional
CREATE TABLE public.detalle_preconcepcional_antropometria (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    detalle_control_prenatal_id uuid NOT NULL REFERENCES public.detalle_control_prenatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Medidas antropométricas
    peso_kg real,
    talla_cm real,
    imc real,
    estado_nutricional public.enum_estado_nutricional
);
COMMENT ON TABLE public.detalle_preconcepcional_antropometria IS 'Medidas antropométricas para atención preconcepcional.';

-- 3. Modificar la tabla principal 'detalle_control_prenatal'

ALTER TABLE public.detalle_control_prenatal
ADD COLUMN sub_tipo_preconcepcional text,
ADD COLUMN sub_detalle_preconcepcional_id uuid;

COMMENT ON COLUMN public.detalle_control_prenatal.sub_tipo_preconcepcional IS 'Tipo de sub-atención dentro del control preconcepcional (ej. ANAMNESIS, PARACLINICOS, ANTROPOMETRIA).';

-- 4. Eliminar las columnas antiguas de detalle_control_prenatal que ahora están en sub-tablas

ALTER TABLE public.detalle_control_prenatal
DROP COLUMN IF EXISTS hemoclasificacion,
DROP COLUMN IF EXISTS resultado_urocultivo,
DROP COLUMN IF EXISTS igg_rubeola_reactivo,
DROP COLUMN IF EXISTS antecedente_trombofilias,
DROP COLUMN IF EXISTS antecedente_anemia,
DROP COLUMN IF EXISTS antecedente_asma,
DROP COLUMN IF EXISTS antecedente_tuberculosis,
DROP COLUMN IF EXISTS antecedente_neoplasias,
DROP COLUMN IF EXISTS antecedente_obesidad_morbida,
DROP COLUMN IF EXISTS antecedente_patologia_cervical_vph,
DROP COLUMN IF EXISTS antecedente_cumplimiento_tamizaje_ccu,
DROP COLUMN IF EXISTS antecedente_numero_companeros_sexuales,
DROP COLUMN IF EXISTS antecedente_uso_preservativo,
DROP COLUMN IF EXISTS antecedente_uso_anticonceptivos,
DROP COLUMN IF EXISTS antecedente_parto_pretermito_previo,
DROP COLUMN IF EXISTS antecedente_cesarea_previa,
DROP COLUMN IF EXISTS antecedente_abortos_previos,
DROP COLUMN IF EXISTS antecedente_muerte_fetal_previa,
DROP COLUMN IF EXISTS antecedente_gran_multiparidad,
DROP COLUMN IF EXISTS antecedente_periodo_intergenesico_corto,
DROP COLUMN IF EXISTS antecedente_incompatibilidad_rh,
DROP COLUMN IF EXISTS antecedente_preeclampsia_gestacion_anterior,
DROP COLUMN IF EXISTS antecedente_rn_peso_menor_2500g,
DROP COLUMN IF EXISTS antecedente_rn_macrosomico,
DROP COLUMN IF EXISTS antecedente_hemorragia_postparto_previo,
DROP COLUMN IF EXISTS antecedente_embarazo_molar,
DROP COLUMN IF EXISTS antecedente_depresion_postparto_previo,
DROP COLUMN IF EXISTS resultado_glicemia_ayunas,
DROP COLUMN IF EXISTS resultado_hemograma,
DROP COLUMN IF EXISTS resultado_tamizaje_ccu,
DROP COLUMN IF EXISTS peso_kg,
DROP COLUMN IF EXISTS talla_cm,
DROP COLUMN IF EXISTS imc,
DROP COLUMN IF EXISTS estado_nutricional;
