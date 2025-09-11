-- Refactorización de la tabla atencion_materno_perinatal a un modelo de polimorfismo anidado.

-- 1. Crear las nuevas tablas de sub-detalle

-- Tabla para Controles Prenatales
CREATE TABLE public.detalle_control_prenatal (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Campos específicos del control prenatal
    estado_gestacional_semanas integer,
    fecha_probable_parto date,
    numero_controles_prenatales integer,
    riesgo_biopsicosocial text,
    resultado_tamizaje_vih text,
    resultado_tamizaje_sifilis text,
    resultado_tamizaje_hepatitis_b text,
    resultado_tamizaje_toxoplasmosis text,
    resultado_tamizaje_estreptococo_b text,
    vacunacion_tdap_completa boolean,
    vacunacion_influenza_completa boolean,
    suplementacion_hierro boolean,
    suplementacion_acido_folico boolean,
    suplementacion_calcio boolean,
    condicion_diabetes_preexistente boolean,
    condicion_hipertension_preexistente boolean,
    condicion_tiroidea_preexistente boolean,
    condicion_epilepsia_preexistente boolean,
    num_gestaciones integer,
    num_partos integer,
    num_cesareas integer,
    num_abortos integer,
    num_muertes_perinatales integer,
    antecedente_preeclampsia boolean,
    antecedente_hemorragia_postparto boolean,
    antecedente_embarazo_multiple boolean,
    signo_alarma_sangrado boolean,
    signo_alarma_cefalea boolean,
    signo_alarma_vision_borrosa boolean,
    -- Nuevos campos de granularidad
    hemoclasificacion text,
    resultado_urocultivo text,
    igg_rubeola_reactivo boolean
);
COMMENT ON TABLE public.detalle_control_prenatal IS 'Detalles específicos para un control prenatal dentro de la ruta materno-perinatal.';

-- Tabla para el Parto
CREATE TABLE public.detalle_parto (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Campos específicos del parto
    tipo_parto text,
    fecha_parto date,
    hora_parto text,
    complicaciones_parto text,
    manejo_alumbramiento text
);
COMMENT ON TABLE public.detalle_parto IS 'Detalles específicos del momento del parto.';

-- Tabla para el Recién Nacido
CREATE TABLE public.detalle_recien_nacido (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Campos específicos del recién nacido
    peso_recien_nacido_kg real,
    talla_recien_nacido_cm real,
    apgar_min1 integer,
    apgar_min5 integer,
    adaptacion_neonatal_observaciones text,
    tamizaje_auditivo_neonatal boolean,
    tamizaje_metabolico_neonatal boolean,
    tamizaje_cardiopatias_congenitas boolean,
    profilaxis_vitamina_k boolean,
    profilaxis_ocular boolean,
    vacunacion_bcg boolean,
    vacunacion_hepatitis_b boolean,
    alimentacion_egreso text
);
COMMENT ON TABLE public.detalle_recien_nacido IS 'Detalles específicos del recién nacido en el momento del parto.';

-- Tabla para el Puerperio (Postparto)
CREATE TABLE public.detalle_puerperio (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    -- Campos específicos del puerperio
    estado_puerperio_observaciones text,
    signo_alarma_fiebre_postparto boolean,
    signo_alarma_sangrado_excesivo_postparto boolean,
    metodo_anticonceptivo_postparto text,
    -- Nuevo campo de granularidad
    tamizaje_depresion_postparto_epds integer
);
COMMENT ON TABLE public.detalle_puerperio IS 'Detalles específicos del seguimiento en el puerperio.';


-- 2. Modificar la tabla principal 'atencion_materno_perinatal' para añadir el vínculo polimórfico

ALTER TABLE public.atencion_materno_perinatal
ADD COLUMN sub_tipo_atencion text,
ADD COLUMN sub_detalle_id uuid;

COMMENT ON COLUMN public.atencion_materno_perinatal.sub_tipo_atencion IS 'Tipo de sub-atención dentro de la ruta materno-perinatal (ej. CONTROL_PRENATAL, PARTO, RECIEN_NACIDO, PUERPERIO).';


-- 3. Eliminar las columnas antiguas de la tabla 'atencion_materno_perinatal'
-- ADVERTENCIA: Esto es una operación destructiva de columnas. Se asume que no hay datos que migrar en este punto.

ALTER TABLE public.atencion_materno_perinatal
DROP COLUMN estado_gestacional_semanas,
DROP COLUMN fecha_probable_parto,
DROP COLUMN numero_controles_prenatales,
DROP COLUMN riesgo_biopsicosocial,
DROP COLUMN resultado_tamizaje_vih,
DROP COLUMN resultado_tamizaje_sifilis,
DROP COLUMN resultado_tamizaje_hepatitis_b,
DROP COLUMN resultado_tamizaje_toxoplasmosis,
DROP COLUMN resultado_tamizaje_estreptococo_b,
DROP COLUMN vacunacion_tdap_completa,
DROP COLUMN vacunacion_influenza_completa,
DROP COLUMN suplementacion_hierro,
DROP COLUMN suplementacion_acido_folico,
DROP COLUMN suplementacion_calcio,
DROP COLUMN condicion_diabetes_preexistente,
DROP COLUMN condicion_hipertension_preexistente,
DROP COLUMN condicion_tiroidea_preexistente,
DROP COLUMN condicion_epilepsia_preexistente,
DROP COLUMN num_gestaciones,
DROP COLUMN num_partos,
DROP COLUMN num_cesareas,
DROP COLUMN num_abortos,
DROP COLUMN num_muertes_perinatales,
DROP COLUMN antecedente_preeclampsia,
DROP COLUMN antecedente_hemorragia_postparto,
DROP COLUMN antecedente_embarazo_multiple,
DROP COLUMN signo_alarma_sangrado,
DROP COLUMN signo_alarma_cefalea,
DROP COLUMN signo_alarma_vision_borrosa,
DROP COLUMN tipo_parto,
DROP COLUMN fecha_parto,
DROP COLUMN hora_parto,
DROP COLUMN complicaciones_parto,
DROP COLUMN manejo_alumbramiento,
DROP COLUMN peso_recien_nacido_kg,
DROP COLUMN talla_recien_nacido_cm,
DROP COLUMN apgar_recien_nacido, -- Columna original que fue reemplazada
DROP COLUMN apgar_min1,
DROP COLUMN apgar_min5,
DROP COLUMN adaptacion_neonatal_observaciones,
DROP COLUMN tamizaje_auditivo_neonatal,
DROP COLUMN tamizaje_metabolico_neonatal,
DROP COLUMN tamizaje_cardiopatias_congenitas,
DROP COLUMN profilaxis_vitamina_k,
DROP COLUMN profilaxis_ocular,
DROP COLUMN vacunacion_bcg,
DROP COLUMN vacunacion_hepatitis_b,
DROP COLUMN alimentacion_egreso,
DROP COLUMN estado_puerperio_observaciones,
DROP COLUMN signo_alarma_fiebre_postparto,
DROP COLUMN signo_alarma_sangrado_excesivo_postparto,
DROP COLUMN metodo_anticonceptivo_postparto;
