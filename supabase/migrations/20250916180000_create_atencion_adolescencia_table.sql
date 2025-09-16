-- Migration: Crear tabla atencion_adolescencia para momento curso de vida 12-29 años
-- Fecha: 16 septiembre 2025
-- Base Normativa: Resolución 3280 de 2018 - Art. 3.3.3 y 3.3.4
-- Descripción: Implementar atención adolescencia y juventud siguiendo patrón vertical establecido

-- Crear ENUMs específicos para Adolescencia y Juventud
CREATE TYPE estado_nutricional_adolescencia AS ENUM (
    'NORMAL',
    'DELGADEZ',
    'SOBREPESO',
    'OBESIDAD_GRADO_I',
    'OBESIDAD_GRADO_II',
    'OBESIDAD_GRADO_III'
);

CREATE TYPE desarrollo_psicosocial AS ENUM (
    'APROPIADO',
    'RIESGO_LEVE',
    'RIESGO_MODERADO',
    'RIESGO_ALTO',
    'REQUIERE_INTERVENCION'
);

CREATE TYPE riesgo_cardiovascular AS ENUM (
    'BAJO',
    'MODERADO',
    'ALTO',
    'MUY_ALTO'
);

CREATE TYPE salud_sexual_reproductiva AS ENUM (
    'NORMAL',
    'FACTORES_RIESGO',
    'REQUIERE_CONSEJERIA',
    'REQUIERE_TRATAMIENTO',
    'NO_EVALUADO'
);

CREATE TYPE trastorno_alimentario AS ENUM (
    'SIN_RIESGO',
    'RIESGO_BAJO',
    'RIESGO_MODERADO',
    'RIESGO_ALTO',
    'DIAGNOSTICO_CONFIRMADO'
);

CREATE TYPE salud_mental AS ENUM (
    'NORMAL',
    'SINTOMAS_LEVES',
    'SINTOMAS_MODERADOS',
    'SINTOMAS_SEVEROS',
    'REQUIERE_ATENCION_ESPECIALIZADA'
);

CREATE TYPE consumo_sustancias AS ENUM (
    'SIN_CONSUMO',
    'CONSUMO_EXPERIMENTAL',
    'CONSUMO_OCASIONAL',
    'CONSUMO_HABITUAL',
    'CONSUMO_PROBLEMATICO'
);

CREATE TYPE proyecto_vida AS ENUM (
    'DEFINIDO',
    'EN_CONSTRUCCION',
    'POCO_CLARO',
    'AUSENTE',
    'REQUIERE_ORIENTACION'
);

CREATE TYPE nivel_riesgo_integral AS ENUM (
    'BAJO',
    'MODERADO',
    'ALTO',
    'MUY_ALTO',
    'CRITICO'
);

CREATE TYPE factor_protector AS ENUM (
    'FAMILIA_FUNCIONAL',
    'BUEN_RENDIMIENTO_ACADEMICO',
    'ACTIVIDAD_FISICA_REGULAR',
    'HABILIDADES_SOCIALES',
    'PROYECTO_VIDA_CLARO',
    'RED_APOYO_SOCIAL',
    'AUTOESTIMA_ADECUADA'
);

-- Crear tabla principal atencion_adolescencia
CREATE TABLE IF NOT EXISTS public.atencion_adolescencia (
    -- Identificadores principales
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    medico_id uuid REFERENCES public.medicos(id) ON DELETE SET NULL,
    atencion_id uuid REFERENCES public.atenciones(id) ON DELETE SET NULL,
    
    -- Datos básicos de la consulta
    fecha_atencion date NOT NULL DEFAULT CURRENT_DATE,
    entorno text NOT NULL DEFAULT 'CONSULTA_EXTERNA',
    edad_anos integer NOT NULL CHECK (edad_anos >= 12 AND edad_anos <= 29),
    
    -- Datos antropométricos y signos vitales
    peso_kg decimal(5,2) NOT NULL CHECK (peso_kg > 0 AND peso_kg <= 200),
    talla_cm decimal(5,1) NOT NULL CHECK (talla_cm > 0 AND talla_cm <= 250),
    presion_sistolica decimal(5,1) NOT NULL CHECK (presion_sistolica >= 70 AND presion_sistolica <= 200),
    presion_diastolica decimal(5,1) NOT NULL CHECK (presion_diastolica >= 40 AND presion_diastolica <= 120),
    frecuencia_cardiaca integer NOT NULL CHECK (frecuencia_cardiaca >= 50 AND frecuencia_cardiaca <= 150),
    
    -- Evaluación desarrollo psicosocial
    autoestima integer NOT NULL CHECK (autoestima >= 1 AND autoestima <= 10),
    habilidades_sociales integer NOT NULL CHECK (habilidades_sociales >= 1 AND habilidades_sociales <= 10),
    proyecto_vida proyecto_vida NOT NULL DEFAULT 'EN_CONSTRUCCION',
    problemas_conductuales boolean NOT NULL DEFAULT false,
    
    -- Salud sexual y reproductiva
    salud_sexual_reproductiva salud_sexual_reproductiva NOT NULL DEFAULT 'NO_EVALUADO',
    inicio_vida_sexual boolean,
    uso_anticonceptivos boolean,
    
    -- Evaluación salud mental
    salud_mental salud_mental NOT NULL DEFAULT 'NORMAL',
    episodios_depresivos boolean NOT NULL DEFAULT false,
    ansiedad_clinica boolean NOT NULL DEFAULT false,
    
    -- Consumo sustancias
    consumo_sustancias consumo_sustancias NOT NULL DEFAULT 'SIN_CONSUMO',
    tipo_sustancias text,
    
    -- Trastornos alimentarios
    trastorno_alimentario trastorno_alimentario NOT NULL DEFAULT 'SIN_RIESGO',
    relacion_comida text,
    
    -- Factores de riesgo y protección
    antecedentes_familiares_cardiovasculares boolean NOT NULL DEFAULT false,
    fumador boolean NOT NULL DEFAULT false,
    sedentarismo boolean NOT NULL DEFAULT false,
    familia_funcional boolean NOT NULL DEFAULT true,
    rendimiento_academico text NOT NULL DEFAULT 'BASICO',
    actividad_fisica_regular boolean NOT NULL DEFAULT false,
    red_apoyo_social boolean NOT NULL DEFAULT true,
    
    -- Observaciones y planes
    observaciones_generales text,
    plan_intervencion text,
    educacion_autocuidado text,
    
    -- Metadatos de auditoría
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Crear índices para optimización de consultas
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_paciente_id ON public.atencion_adolescencia(paciente_id);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_medico_id ON public.atencion_adolescencia(medico_id);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_fecha ON public.atencion_adolescencia(fecha_atencion);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_edad ON public.atencion_adolescencia(edad_anos);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_entorno ON public.atencion_adolescencia(entorno);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_created_at ON public.atencion_adolescencia(created_at);

-- Crear índices compuestos para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_paciente_fecha ON public.atencion_adolescencia(paciente_id, fecha_atencion DESC);
CREATE INDEX IF NOT EXISTS idx_atencion_adolescencia_medico_fecha ON public.atencion_adolescencia(medico_id, fecha_atencion DESC);

-- Configurar Row Level Security (RLS)
ALTER TABLE public.atencion_adolescencia ENABLE ROW LEVEL SECURITY;

-- Políticas RLS para desarrollo (permiten acceso completo)
CREATE POLICY "service_role_full_access_atencion_adolescencia" ON public.atencion_adolescencia
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "desarrollo_full_access_atencion_adolescencia" ON public.atencion_adolescencia
    FOR ALL USING (true);

-- Permisos para roles
GRANT ALL ON public.atencion_adolescencia TO service_role;
GRANT ALL ON public.atencion_adolescencia TO authenticated;
GRANT SELECT ON public.atencion_adolescencia TO anon;

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_atencion_adolescencia_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_atencion_adolescencia_updated_at
    BEFORE UPDATE ON public.atencion_adolescencia
    FOR EACH ROW EXECUTE FUNCTION update_atencion_adolescencia_updated_at();

-- Comentarios para documentación
COMMENT ON TABLE public.atencion_adolescencia IS 'Atención integral para adolescentes y jóvenes (12-29 años) según Resolución 3280 Art. 3.3.3 y 3.3.4';
COMMENT ON COLUMN public.atencion_adolescencia.id IS 'Identificador único de la atención de adolescencia';
COMMENT ON COLUMN public.atencion_adolescencia.paciente_id IS 'Referencia al paciente atendido';
COMMENT ON COLUMN public.atencion_adolescencia.medico_id IS 'Referencia al médico que atiende';
COMMENT ON COLUMN public.atencion_adolescencia.atencion_id IS 'Referencia a la atención general (patrón polimórfico)';
COMMENT ON COLUMN public.atencion_adolescencia.edad_anos IS 'Edad del paciente en años (12-29)';
COMMENT ON COLUMN public.atencion_adolescencia.autoestima IS 'Nivel de autoestima evaluado (escala 1-10)';
COMMENT ON COLUMN public.atencion_adolescencia.habilidades_sociales IS 'Nivel de habilidades sociales (escala 1-10)';
COMMENT ON COLUMN public.atencion_adolescencia.proyecto_vida IS 'Evaluación del proyecto de vida del adolescente/joven';
COMMENT ON COLUMN public.atencion_adolescencia.salud_sexual_reproductiva IS 'Estado de la salud sexual y reproductiva';
COMMENT ON COLUMN public.atencion_adolescencia.salud_mental IS 'Evaluación del estado de salud mental';
COMMENT ON COLUMN public.atencion_adolescencia.consumo_sustancias IS 'Nivel de consumo de sustancias psicoactivas';
COMMENT ON COLUMN public.atencion_adolescencia.trastorno_alimentario IS 'Riesgo o presencia de trastornos alimentarios';

-- Crear vista materializada para estadísticas rápidas (opcional)
CREATE MATERIALIZED VIEW IF NOT EXISTS public.estadisticas_adolescencia AS
SELECT 
    DATE_TRUNC('month', fecha_atencion) as mes,
    COUNT(*) as total_atenciones,
    AVG(edad_anos) as edad_promedio,
    AVG(peso_kg) as peso_promedio,
    AVG(talla_cm) as talla_promedio,
    COUNT(*) FILTER (WHERE salud_mental != 'NORMAL') as problemas_salud_mental,
    COUNT(*) FILTER (WHERE consumo_sustancias != 'SIN_CONSUMO') as casos_consumo_sustancias,
    COUNT(*) FILTER (WHERE sedentarismo = true) as casos_sedentarismo
FROM public.atencion_adolescencia
GROUP BY DATE_TRUNC('month', fecha_atencion)
ORDER BY mes DESC;

-- Índice para la vista materializada
CREATE UNIQUE INDEX IF NOT EXISTS idx_estadisticas_adolescencia_mes ON public.estadisticas_adolescencia(mes);

-- Función para refrescar estadísticas
CREATE OR REPLACE FUNCTION refresh_estadisticas_adolescencia()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY public.estadisticas_adolescencia;
END;
$$ LANGUAGE plpgsql;

-- Crear función para validar datos críticos
CREATE OR REPLACE FUNCTION validar_atencion_adolescencia()
RETURNS trigger AS $$
BEGIN
    -- Validar consistencia de edad con rango adolescencia/juventud
    IF NEW.edad_anos < 12 OR NEW.edad_anos > 29 THEN
        RAISE EXCEPTION 'Edad debe estar entre 12 y 29 años para atención adolescencia/juventud';
    END IF;
    
    -- Validar presión arterial
    IF NEW.presion_sistolica <= NEW.presion_diastolica THEN
        RAISE EXCEPTION 'Presión sistólica debe ser mayor que presión diastólica';
    END IF;
    
    -- Validar IMC extremo
    IF (NEW.peso_kg / POWER(NEW.talla_cm / 100, 2)) > 50 THEN
        RAISE EXCEPTION 'IMC calculado es extremadamente alto, verificar datos antropométricos';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger de validación
CREATE TRIGGER trigger_validar_atencion_adolescencia
    BEFORE INSERT OR UPDATE ON public.atencion_adolescencia
    FOR EACH ROW EXECUTE FUNCTION validar_atencion_adolescencia();

-- Mensaje final
SELECT 'Migración completada: Tabla atencion_adolescencia creada exitosamente con ENUMs, índices, RLS y triggers configurados' as resultado;