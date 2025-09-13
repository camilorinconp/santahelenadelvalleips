-- =============================================================================
-- Migración Simplificada: Primera Infancia Transversal (Fase 1)
-- Fecha: 13 de septiembre, 2025
-- Descripción: Agregar campos transversales sin modificar existentes
-- =============================================================================

BEGIN;

-- Crear ENUMs específicos de primera infancia
DO $$ BEGIN
    CREATE TYPE estado_nutricional_primera_infancia AS ENUM (
        'PESO_ADECUADO_EDAD',
        'PESO_BAJO_EDAD',
        'PESO_MUY_BAJO_EDAD', 
        'SOBREPESO_OBESIDAD',
        'RIESGO_DESNUTRICION',
        'DESNUTRICION_AGUDA'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE resultado_tamizaje_desarrollo AS ENUM (
        'DESARROLLO_ACORDE_EDAD',
        'ALERTA_SEGUIMIENTO_REQUERIDO',
        'RETRASO_DERIVACION_ESPECIALIZADA',
        'EVALUACION_INCOMPLETA'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE estado_esquema_vacunacion AS ENUM (
        'COMPLETO_AL_DIA',
        'INCOMPLETO_RECUPERABLE',
        'ATRASADO_INTERVENCION_REQUERIDA',
        'CONTRAINDICACION_MEDICA_TEMPORAL'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Agregar campos de integración transversal (NUEVOS)
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS codigo_atencion_primera_infancia_unico TEXT UNIQUE,
ADD COLUMN IF NOT EXISTS entorno_desarrollo_asociado_id UUID,
ADD COLUMN IF NOT EXISTS familia_integral_pertenencia_id UUID,
ADD COLUMN IF NOT EXISTS atencion_integral_coordinada_id UUID;

-- Agregar nuevos campos con nomenclatura descriptiva
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS estado_nutricional_evaluacion estado_nutricional_primera_infancia,
ADD COLUMN IF NOT EXISTS tamizaje_desarrollo_integral_resultado resultado_tamizaje_desarrollo,
ADD COLUMN IF NOT EXISTS esquema_vacunacion_estado_actual estado_esquema_vacunacion;

-- Nuevos campos JSONB para datos semi-estructurados
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS practicas_alimentarias_evaluacion JSONB,
ADD COLUMN IF NOT EXISTS suplementacion_micronutrientes_registro JSONB,
ADD COLUMN IF NOT EXISTS salud_visual_tamizaje_detallado JSONB,
ADD COLUMN IF NOT EXISTS salud_auditiva_comunicativa_tamizaje JSONB,
ADD COLUMN IF NOT EXISTS salud_bucal_evaluacion_integral JSONB,
ADD COLUMN IF NOT EXISTS vacunas_aplicadas_registro JSONB,
ADD COLUMN IF NOT EXISTS vacunas_pendientes_programacion JSONB,
ADD COLUMN IF NOT EXISTS desparasitacion_profilaxis_registro JSONB,
ADD COLUMN IF NOT EXISTS intervenciones_educativas_realizadas JSONB,
ADD COLUMN IF NOT EXISTS coordinacion_intersectorial_realizada JSONB,
ADD COLUMN IF NOT EXISTS plan_seguimiento_longitudinal JSONB;

-- Campos de evaluación narrativa mejorados
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS desarrollo_fisico_motor_evaluacion TEXT,
ADD COLUMN IF NOT EXISTS desarrollo_socioemocional_evaluacion TEXT,
ADD COLUMN IF NOT EXISTS desarrollo_cognitivo_lenguaje_evaluacion TEXT,
ADD COLUMN IF NOT EXISTS salud_mental_bienestar_psicosocial TEXT,
ADD COLUMN IF NOT EXISTS observaciones_profesional_primera_infancia TEXT;

-- Crear referencias a tablas transversales (sin FK constraints por ahora)
-- Índices para optimización de consultas transversales
CREATE INDEX IF NOT EXISTS idx_primera_infancia_entorno 
ON atencion_primera_infancia(entorno_desarrollo_asociado_id);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_familia 
ON atencion_primera_infancia(familia_integral_pertenencia_id);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_atencion_coordinada 
ON atencion_primera_infancia(atencion_integral_coordinada_id);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_codigo_unico 
ON atencion_primera_infancia(codigo_atencion_primera_infancia_unico);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_estado_nutricional 
ON atencion_primera_infancia(estado_nutricional_evaluacion);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_vacunacion 
ON atencion_primera_infancia(esquema_vacunacion_estado_actual);

-- Crear secuencia para códigos únicos
CREATE SEQUENCE IF NOT EXISTS seq_primera_infancia START 1;

-- Función para generar código único si no existe
CREATE OR REPLACE FUNCTION generar_codigo_primera_infancia()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.codigo_atencion_primera_infancia_unico IS NULL THEN
        NEW.codigo_atencion_primera_infancia_unico := 
            'PI-' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || 
            LPAD(NEXTVAL('seq_primera_infancia')::TEXT, 6, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para generar código automáticamente
DROP TRIGGER IF EXISTS trigger_codigo_primera_infancia ON atencion_primera_infancia;
CREATE TRIGGER trigger_codigo_primera_infancia
    BEFORE INSERT ON atencion_primera_infancia
    FOR EACH ROW
    EXECUTE FUNCTION generar_codigo_primera_infancia();

COMMIT;

-- Comentarios
COMMENT ON COLUMN atencion_primera_infancia.entorno_desarrollo_asociado_id IS 
'Referencia al entorno de salud pública donde se desarrolla el menor';

COMMENT ON COLUMN atencion_primera_infancia.familia_integral_pertenencia_id IS 
'Referencia a la familia integral a la que pertenece el menor';

COMMENT ON COLUMN atencion_primera_infancia.atencion_integral_coordinada_id IS 
'Referencia a la atención integral transversal que coordina este cuidado';

-- Nota de migración completada
SELECT 'Migración Primera Infancia Transversal (Fase 1) aplicada exitosamente' as resultado;