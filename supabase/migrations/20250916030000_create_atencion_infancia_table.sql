-- Migration: Crear tabla atencion_infancia para momento curso de vida 6-11 años
-- Fecha: 16 septiembre 2025
-- Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2
-- Descripción: Implementar atención infancia siguiendo patrón vertical establecido

-- Crear ENUMs específicos para Infancia
CREATE TYPE estado_nutricional_infancia AS ENUM (
    'NORMAL',
    'DELGADEZ', 
    'SOBREPESO',
    'OBESIDAD',
    'TALLA_BAJA'
);

CREATE TYPE desempeno_escolar AS ENUM (
    'SUPERIOR',
    'ALTO',
    'BASICO',
    'BAJO',
    'NO_ESCOLARIZADO'
);

CREATE TYPE resultado_tamizaje AS ENUM (
    'NORMAL',
    'ALTERADO',
    'REQUIERE_EVALUACION',
    'NO_REALIZADO'
);

CREATE TYPE factor_riesgo_infancia AS ENUM (
    'SEDENTARISMO',
    'ALIMENTACION_INADECUADA',
    'EXPOSICION_PANTALLAS',
    'PROBLEMAS_SUENO',
    'VIOLENCIA_ESCOLAR',
    'NINGUNO'
);

-- Crear tabla principal atencion_infancia
CREATE TABLE IF NOT EXISTS public.atencion_infancia (
    -- Identificadores principales
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id uuid NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
    medico_id uuid REFERENCES public.medicos(id) ON DELETE SET NULL,
    atencion_id uuid REFERENCES public.atenciones(id) ON DELETE SET NULL,
    
    -- Datos básicos de la consulta
    fecha_atencion date NOT NULL DEFAULT CURRENT_DATE,
    entorno text NOT NULL DEFAULT 'IPS',
    
    -- DATOS ANTROPOMÉTRICOS (OBLIGATORIOS según Resolución 3280)
    peso_kg decimal(5,2) NOT NULL CHECK (peso_kg > 0 AND peso_kg <= 150),
    talla_cm decimal(5,2) NOT NULL CHECK (talla_cm > 50 AND talla_cm <= 200),
    
    -- DESARROLLO Y RENDIMIENTO ESCOLAR
    grado_escolar text,
    desempeno_escolar desempeno_escolar NOT NULL,
    dificultades_aprendizaje boolean NOT NULL DEFAULT false,
    observaciones_desarrollo_cognitivo text,
    
    -- SALUD VISUAL Y AUDITIVA (CRÍTICO EN EDAD ESCOLAR)
    tamizaje_visual resultado_tamizaje NOT NULL,
    agudeza_visual_ojo_derecho text,
    agudeza_visual_ojo_izquierdo text,
    tamizaje_auditivo resultado_tamizaje NOT NULL,
    observaciones_salud_visual_auditiva text,
    
    -- SALUD BUCAL (DENTICIÓN PERMANENTE)
    tamizaje_salud_bucal resultado_tamizaje NOT NULL,
    numero_dientes_permanentes integer CHECK (numero_dientes_permanentes >= 0 AND numero_dientes_permanentes <= 32),
    numero_caries integer CHECK (numero_caries >= 0),
    higiene_bucal text,
    observaciones_salud_bucal text,
    
    -- ESQUEMA DE VACUNACIÓN
    esquema_vacunacion_completo boolean NOT NULL,
    vacunas_faltantes text,
    
    -- ESTILOS DE VIDA Y FACTORES DE RIESGO
    actividad_fisica_semanal_horas decimal(4,2) CHECK (actividad_fisica_semanal_horas >= 0 AND actividad_fisica_semanal_horas <= 168),
    horas_pantalla_diarias decimal(4,2) CHECK (horas_pantalla_diarias >= 0 AND horas_pantalla_diarias <= 24),
    horas_sueno_diarias decimal(4,2) CHECK (horas_sueno_diarias >= 0 AND horas_sueno_diarias <= 24),
    factores_riesgo_identificados text[], -- Array de factores de riesgo
    
    -- ALIMENTACIÓN Y NUTRICIÓN
    alimentacion_escolar boolean NOT NULL DEFAULT false,
    consume_comida_chatarra boolean NOT NULL DEFAULT false,
    observaciones_alimentacion text,
    
    -- OBSERVACIONES GENERALES
    observaciones_profesional_infancia text,
    
    -- METADATOS
    creado_en timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

-- Comentarios de documentación
COMMENT ON TABLE public.atencion_infancia IS 'Atenciones para momento del curso de vida Infancia (6-11 años) según Resolución 3280 Art. 3.3.2';
COMMENT ON COLUMN public.atencion_infancia.paciente_id IS 'Referencia al paciente (6-11 años)';
COMMENT ON COLUMN public.atencion_infancia.atencion_id IS 'Referencia a atención general - nullable para patrón polimórfico';
COMMENT ON COLUMN public.atencion_infancia.peso_kg IS 'Peso en kilogramos - obligatorio según normativa';
COMMENT ON COLUMN public.atencion_infancia.talla_cm IS 'Talla en centímetros - obligatorio según normativa';
COMMENT ON COLUMN public.atencion_infancia.desempeno_escolar IS 'Evaluación del rendimiento académico';
COMMENT ON COLUMN public.atencion_infancia.tamizaje_visual IS 'Tamizaje visual - crítico en edad escolar';
COMMENT ON COLUMN public.atencion_infancia.tamizaje_auditivo IS 'Tamizaje auditivo - crítico en edad escolar';
COMMENT ON COLUMN public.atencion_infancia.tamizaje_salud_bucal IS 'Salud bucal en período de dentición permanente';
COMMENT ON COLUMN public.atencion_infancia.factores_riesgo_identificados IS 'Array de factores de riesgo modulables';

-- Índices para optimización de consultas
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_paciente_id ON public.atencion_infancia(paciente_id);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_fecha ON public.atencion_infancia(fecha_atencion);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_medico_id ON public.atencion_infancia(medico_id);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_atencion_id ON public.atencion_infancia(atencion_id);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_desempeno ON public.atencion_infancia(desempeno_escolar);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_tamizajes ON public.atencion_infancia(tamizaje_visual, tamizaje_auditivo, tamizaje_salud_bucal);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_vacunacion ON public.atencion_infancia(esquema_vacunacion_completo);
CREATE INDEX IF NOT EXISTS idx_atencion_infancia_factores_riesgo ON public.atencion_infancia USING GIN(factores_riesgo_identificados);

-- Trigger para actualización automática de updated_at
CREATE OR REPLACE FUNCTION update_atencion_infancia_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atencion_infancia_updated_at
    BEFORE UPDATE ON public.atencion_infancia
    FOR EACH ROW
    EXECUTE FUNCTION update_atencion_infancia_updated_at();

-- Habilitar RLS (Row Level Security)
ALTER TABLE public.atencion_infancia ENABLE ROW LEVEL SECURITY;

-- Política RLS para desarrollo (permitir todas las operaciones)
-- En producción, estas políticas deberían ser más restrictivas basadas en roles
CREATE POLICY "desarrollo_full_access_atencion_infancia"
    ON public.atencion_infancia
    FOR ALL
    TO authenticated, anon
    USING (true)
    WITH CHECK (true);

-- Política adicional para service_role
CREATE POLICY "service_role_full_access_atencion_infancia"
    ON public.atencion_infancia
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Verificación de la creación
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'atencion_infancia' 
    AND table_schema = 'public'
ORDER BY ordinal_position;

-- Verificar ENUMs creados
SELECT 
    enumtypid::regtype AS enum_type,
    enumlabel AS enum_value
FROM pg_enum
WHERE enumtypid::regtype::text LIKE '%infancia%' OR 
      enumtypid::regtype::text LIKE '%desempeno%' OR
      enumtypid::regtype::text LIKE '%resultado_tamizaje%'
ORDER BY enumtypid, enumsortorder;

-- Verificar índices creados
SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'atencion_infancia'
    AND schemaname = 'public';

-- Verificar RLS habilitado
SELECT 
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename = 'atencion_infancia'
    AND schemaname = 'public';

-- Mensaje de éxito
SELECT 'SUCCESS: Tabla atencion_infancia creada exitosamente con arquitectura vertical' as message;
SELECT 'COMPLIANCE: Implementación según Resolución 3280 Art. 3.3.2 completada' as compliance_status;
SELECT 'PATRÓN: Siguiendo estructura polimórfica establecida exitosamente' as arquitectura_status;