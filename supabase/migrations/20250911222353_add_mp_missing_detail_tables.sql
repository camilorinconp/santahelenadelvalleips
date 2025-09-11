-- Añadir tablas de detalle faltantes para la Ruta Materno Perinatal

-- Tabla para Atención en Salud Bucal (Gestantes)
CREATE TABLE public.detalle_salud_bucal_mp (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    observaciones_salud_bucal text,
    fecha_ultima_atencion_bucal date,
    riesgo_caries text, -- Considerar ENUM
    riesgo_enfermedad_periodontal text -- Considerar ENUM
);
COMMENT ON TABLE public.detalle_salud_bucal_mp IS 'Detalles de atención en salud bucal para la ruta materno-perinatal.';

-- Tabla para Atención para la Promoción de la Alimentación y Nutrición (Gestantes)
CREATE TABLE public.detalle_nutricion_mp (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    patron_alimentario text,
    frecuencia_consumo_alimentos text,
    alimentos_preferidos_rechazados text,
    trastornos_alimentarios text,
    peso_pregestacional real,
    imc_pregestacional real,
    diagnostico_nutricional text, -- Considerar ENUM
    plan_manejo_nutricional text
);
COMMENT ON TABLE public.detalle_nutricion_mp IS 'Detalles de atención para la promoción de alimentación y nutrición en la ruta materno-perinatal.';

-- Tabla para Interrupción Voluntaria del Embarazo (IVE)
CREATE TABLE public.detalle_ive (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    causal_ive text, -- Considerar ENUM
    fecha_ive date,
    semanas_gestacion_ive integer,
    metodo_ive text, -- Considerar ENUM
    complicaciones_ive text,
    asesoria_post_ive text
);
COMMENT ON TABLE public.detalle_ive IS 'Detalles de interrupción voluntaria del embarazo.';

-- Tabla para Curso de Preparación para la Maternidad y la Paternidad
CREATE TABLE public.detalle_curso_maternidad_paternidad (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    fecha_inicio_curso date,
    fecha_fin_curso date,
    asistencia_curso text, -- Considerar ENUM (COMPLETA, PARCIAL, NO_ASISTE)
    temas_cubiertos text,
    observaciones_curso text
);
COMMENT ON TABLE public.detalle_curso_maternidad_paternidad IS 'Detalles del curso de preparación para la maternidad y paternidad.';

-- Tabla para Atención para el Seguimiento del Recién Nacido
CREATE TABLE public.detalle_seguimiento_rn (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    atencion_materno_perinatal_id uuid NOT NULL REFERENCES public.atencion_materno_perinatal(id) ON DELETE CASCADE,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone,
    fecha_seguimiento date,
    peso_rn_seguimiento real,
    talla_rn_seguimiento real,
    perimetro_cefalico_rn_seguimiento real,
    estado_nutricional_rn text, -- Considerar ENUM
    observaciones_desarrollo_rn text,
    tamizajes_pendientes_rn text, -- Considerar JSONB o TEXT
    vacunacion_rn_completa boolean
);
COMMENT ON TABLE public.detalle_seguimiento_rn IS 'Detalles de atención para el seguimiento del recién nacido.';
