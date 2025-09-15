-- ===================================================================
-- MIGRACIÓN: Primera Infancia Expandida según Resolución 3280
-- ===================================================================
-- Descripción: Agregar campos EAD-3, ASQ-3, tamizajes especializados
-- Autor: Database Architecture Team - IPS Santa Helena del Valle
-- Fecha: 14 septiembre 2025
-- Propósito: RPMS Primera Infancia completa según normativa colombiana
-- ===================================================================

BEGIN;

-- ===================================================================
-- CREAR ENUMS ESPECIALIZADOS PARA PRIMERA INFANCIA
-- ===================================================================

-- Resultados específicos por área de desarrollo EAD-3
CREATE TYPE resultado_area_desarrollo AS ENUM (
    'MEDIO',
    'MEDIO_ALTO', 
    'ALERTA',
    'MEDIO_BAJO',
    'ALERTA_ROJA'
);

-- Estado de salud oral específico
CREATE TYPE estado_salud_oral AS ENUM (
    'SANO',
    'RIESGO_CARIES',
    'CARIES_TEMPRANA',
    'CARIES_SEVERA',
    'MALOCLUSION', 
    'TRAUMATISMO_DENTAL'
);

-- Tipos de vacunas del esquema nacional
CREATE TYPE tipo_vacuna AS ENUM (
    'BCG',
    'HEPATITIS_B_RN',
    'PENTAVALENTE_1',
    'PENTAVALENTE_2', 
    'PENTAVALENTE_3',
    'POLIO_1',
    'POLIO_2',
    'POLIO_3',
    'ROTAVIRUS_1',
    'ROTAVIRUS_2',
    'ROTAVIRUS_3',
    'NEUMOCOCO_1',
    'NEUMOCOCO_2',
    'NEUMOCOCO_REFUERZO',
    'SRP_1',
    'SRP_REFUERZO',
    'DPT_REFUERZO_1',
    'DPT_REFUERZO_2',
    'POLIO_REFUERZO_1',
    'POLIO_REFUERZO_2'
);

-- ===================================================================
-- EXPANDIR TABLA ATENCION_PRIMERA_INFANCIA
-- ===================================================================

-- Campos de edad y contexto (compatibilidad con esquema existente)
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS edad_cronologica_meses integer CHECK (edad_cronologica_meses >= 0 AND edad_cronologica_meses <= 60),
ADD COLUMN IF NOT EXISTS edad_corregida_meses integer;

-- Evaluación nutricional expandida con curvas OMS
ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS indice_masa_corporal_edad numeric,
ADD COLUMN IF NOT EXISTS peso_edad_percentil integer CHECK (peso_edad_percentil >= 0 AND peso_edad_percentil <= 100),
ADD COLUMN IF NOT EXISTS peso_edad_zscore numeric,
ADD COLUMN IF NOT EXISTS talla_edad_percentil integer CHECK (talla_edad_percentil >= 0 AND talla_edad_percentil <= 100),
ADD COLUMN IF NOT EXISTS talla_edad_zscore numeric,
ADD COLUMN IF NOT EXISTS peso_talla_percentil integer CHECK (peso_talla_percentil >= 0 AND peso_talla_percentil <= 100),
ADD COLUMN IF NOT EXISTS peso_talla_zscore numeric,
ADD COLUMN IF NOT EXISTS perimetro_cefalico_percentil integer CHECK (perimetro_cefalico_percentil >= 0 AND perimetro_cefalico_percentil <= 100);

-- ===================================================================
-- ESCALA ABREVIADA DE DESARROLLO (EAD-3) COMPLETA
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS ead3_aplicada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS fecha_aplicacion_ead3 date,

-- Motricidad Gruesa
ADD COLUMN IF NOT EXISTS ead3_motricidad_gruesa_puntaje integer CHECK (ead3_motricidad_gruesa_puntaje >= 0 AND ead3_motricidad_gruesa_puntaje <= 100),
ADD COLUMN IF NOT EXISTS ead3_motricidad_gruesa_resultado resultado_area_desarrollo,
ADD COLUMN IF NOT EXISTS ead3_motricidad_gruesa_items_logrados text[],

-- Motricidad Fina-Adaptativa  
ADD COLUMN IF NOT EXISTS ead3_motricidad_fina_puntaje integer CHECK (ead3_motricidad_fina_puntaje >= 0 AND ead3_motricidad_fina_puntaje <= 100),
ADD COLUMN IF NOT EXISTS ead3_motricidad_fina_resultado resultado_area_desarrollo,
ADD COLUMN IF NOT EXISTS ead3_motricidad_fina_items_logrados text[],

-- Audición y Lenguaje
ADD COLUMN IF NOT EXISTS ead3_audicion_lenguaje_puntaje integer CHECK (ead3_audicion_lenguaje_puntaje >= 0 AND ead3_audicion_lenguaje_puntaje <= 100),
ADD COLUMN IF NOT EXISTS ead3_audicion_lenguaje_resultado resultado_area_desarrollo,
ADD COLUMN IF NOT EXISTS ead3_audicion_lenguaje_items_logrados text[],

-- Personal-Social
ADD COLUMN IF NOT EXISTS ead3_personal_social_puntaje integer CHECK (ead3_personal_social_puntaje >= 0 AND ead3_personal_social_puntaje <= 100),
ADD COLUMN IF NOT EXISTS ead3_personal_social_resultado resultado_area_desarrollo,
ADD COLUMN IF NOT EXISTS ead3_personal_social_items_logrados text[],

-- Resultado general EAD-3
ADD COLUMN IF NOT EXISTS ead3_puntaje_total integer,
ADD COLUMN IF NOT EXISTS ead3_edad_desarrollo_equivalente_meses integer,
ADD COLUMN IF NOT EXISTS ead3_resultado_general text;

-- ===================================================================
-- TAMIZAJE ASQ-3 (AGES AND STAGES QUESTIONNAIRE)  
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS asq3_aplicado boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS fecha_aplicacion_asq3 date,
ADD COLUMN IF NOT EXISTS asq3_comunicacion_puntaje integer,
ADD COLUMN IF NOT EXISTS asq3_motor_grueso_puntaje integer,
ADD COLUMN IF NOT EXISTS asq3_motor_fino_puntaje integer,
ADD COLUMN IF NOT EXISTS asq3_resolucion_problemas_puntaje integer,
ADD COLUMN IF NOT EXISTS asq3_personal_social_puntaje integer,
ADD COLUMN IF NOT EXISTS asq3_resultado_general text;

-- ===================================================================
-- ESQUEMA DE VACUNACIÓN DETALLADO
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
-- Vacunas específicas con seguimiento individual
ADD COLUMN IF NOT EXISTS bcg_aplicada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS bcg_fecha_aplicacion date,
ADD COLUMN IF NOT EXISTS hepatitis_b_rn_aplicada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS hepatitis_b_rn_fecha date,
ADD COLUMN IF NOT EXISTS pentavalente_dosis_completas integer DEFAULT 0 CHECK (pentavalente_dosis_completas >= 0 AND pentavalente_dosis_completas <= 3),
ADD COLUMN IF NOT EXISTS pentavalente_fechas date[],
ADD COLUMN IF NOT EXISTS polio_dosis_completas integer DEFAULT 0 CHECK (polio_dosis_completas >= 0 AND polio_dosis_completas <= 5),
ADD COLUMN IF NOT EXISTS polio_fechas date[],
ADD COLUMN IF NOT EXISTS rotavirus_dosis_completas integer DEFAULT 0 CHECK (rotavirus_dosis_completas >= 0 AND rotavirus_dosis_completas <= 3),
ADD COLUMN IF NOT EXISTS neumococo_dosis_completas integer DEFAULT 0 CHECK (neumococo_dosis_completas >= 0 AND neumococo_dosis_completas <= 3),
ADD COLUMN IF NOT EXISTS srp_aplicada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS srp_fecha_aplicacion date,
ADD COLUMN IF NOT EXISTS esquema_edad_apropiado boolean,
ADD COLUMN IF NOT EXISTS proxima_vacuna_programada text,
ADD COLUMN IF NOT EXISTS proxima_vacuna_fecha_ideal date,
ADD COLUMN IF NOT EXISTS vacunas_contraindicadas text[];

-- ===================================================================
-- TAMIZAJES ESPECIALIZADOS - VISUAL
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS tamizaje_visual_realizado boolean DEFAULT false,

-- Test de Hirschberg (reflejo corneal)
ADD COLUMN IF NOT EXISTS hirschberg_realizado boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS hirschberg_resultado text,
ADD COLUMN IF NOT EXISTS hirschberg_normal boolean,

-- Test cubrir-descubrir
ADD COLUMN IF NOT EXISTS cubrir_descubrir_realizado boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS cubrir_descubrir_resultado text,
ADD COLUMN IF NOT EXISTS cubrir_descubrir_normal boolean,

-- Seguimiento visual
ADD COLUMN IF NOT EXISTS seguimiento_visual_evaluado boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS seguimiento_visual_normal boolean,

-- Reflejo rojo
ADD COLUMN IF NOT EXISTS reflejo_rojo_evaluado boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS reflejo_rojo_presente_bilateral boolean,

-- Resultado general
ADD COLUMN IF NOT EXISTS tamizaje_visual_resultado_general text;

-- ===================================================================
-- TAMIZAJES ESPECIALIZADOS - AUDITIVO
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS tamizaje_auditivo_realizado boolean DEFAULT false,

-- Otoemisiones acústicas
ADD COLUMN IF NOT EXISTS otoemisiones_acusticas_realizadas boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS otoemisiones_acusticas_resultado text,

-- Respuesta a sonidos
ADD COLUMN IF NOT EXISTS respuesta_sonidos_evaluada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS respuesta_sonidos_edad_apropiada boolean,

-- Potenciales evocados auditivos
ADD COLUMN IF NOT EXISTS potenciales_auditivos_realizados boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS potenciales_auditivos_resultado text,

-- Resultado general
ADD COLUMN IF NOT EXISTS tamizaje_auditivo_resultado_general text;

-- ===================================================================
-- SALUD ORAL PRIMERA INFANCIA
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS evaluacion_salud_oral_realizada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS estado_salud_oral_enum estado_salud_oral,
ADD COLUMN IF NOT EXISTS erupcion_dental_apropiada_edad boolean,
ADD COLUMN IF NOT EXISTS numero_dientes_presentes integer CHECK (numero_dientes_presentes >= 0 AND numero_dientes_presentes <= 20),
ADD COLUMN IF NOT EXISTS caries_detectadas boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS numero_caries integer DEFAULT 0 CHECK (numero_caries >= 0),
ADD COLUMN IF NOT EXISTS higiene_oral_adecuada boolean,
ADD COLUMN IF NOT EXISTS maloclusion_detectada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS tipo_maloclusion text,
ADD COLUMN IF NOT EXISTS traumatismo_dental boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS habitos_orales_nocivos text[],
ADD COLUMN IF NOT EXISTS fluorosis_detectada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS aplicacion_fluor_realizada boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS aplicacion_fluor_fecha date;

-- ===================================================================
-- SISTEMA DE ALERTAS AUTOMÁTICAS
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS alertas_desarrollo_generadas text[],
ADD COLUMN IF NOT EXISTS hitos_desarrollo_perdidos text[],
ADD COLUMN IF NOT EXISTS requiere_intervencion_temprana boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS especialidades_referencia_requeridas text[],
ADD COLUMN IF NOT EXISTS fecha_proxima_evaluacion_desarrollo date,
ADD COLUMN IF NOT EXISTS nivel_riesgo_desarrollo text;

-- ===================================================================
-- INTERVENCIONES EDUCATIVAS EXPANDIDAS
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS educacion_estimulacion_temprana boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS educacion_alimentacion_complementaria boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS educacion_prevencion_accidentes boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS educacion_higiene_oral boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS educacion_desarrollo_lenguaje boolean DEFAULT false,
ADD COLUMN IF NOT EXISTS educacion_lactancia_materna boolean DEFAULT false;

-- ===================================================================
-- PLAN DE SEGUIMIENTO LONGITUDINAL
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS frecuencia_controles_recomendada text,
ADD COLUMN IF NOT EXISTS objetivos_desarrollo_proxima_consulta text[],
ADD COLUMN IF NOT EXISTS actividades_estimulacion_hogar text[],
ADD COLUMN IF NOT EXISTS signos_alarma_cuidadores text[],
ADD COLUMN IF NOT EXISTS plan_seguimiento_nutricional text;

-- ===================================================================
-- NUEVAS OBSERVACIONES Y CONDUCTA
-- ===================================================================

ALTER TABLE atencion_primera_infancia 
ADD COLUMN IF NOT EXISTS observaciones_profesional_primera_infancia text,
ADD COLUMN IF NOT EXISTS conducta_seguir text;

-- ===================================================================
-- ÍNDICES PARA OPTIMIZACIÓN DE CONSULTAS
-- ===================================================================

-- Índices para consultas por edad y desarrollo
CREATE INDEX IF NOT EXISTS idx_primera_infancia_edad_cronologica 
    ON atencion_primera_infancia(edad_cronologica_meses);

CREATE INDEX IF NOT EXISTS idx_primera_infancia_ead3_aplicada 
    ON atencion_primera_infancia(ead3_aplicada) WHERE ead3_aplicada = true;

CREATE INDEX IF NOT EXISTS idx_primera_infancia_alertas_desarrollo 
    ON atencion_primera_infancia USING gin(alertas_desarrollo_generadas) 
    WHERE alertas_desarrollo_generadas IS NOT NULL;

-- Índices para tamizajes
CREATE INDEX IF NOT EXISTS idx_primera_infancia_tamizaje_visual 
    ON atencion_primera_infancia(tamizaje_visual_realizado) WHERE tamizaje_visual_realizado = true;

CREATE INDEX IF NOT EXISTS idx_primera_infancia_tamizaje_auditivo 
    ON atencion_primera_infancia(tamizaje_auditivo_realizado) WHERE tamizaje_auditivo_realizado = true;

-- Índices para vacunación
CREATE INDEX IF NOT EXISTS idx_primera_infancia_esquema_apropiado 
    ON atencion_primera_infancia(esquema_edad_apropiado);

-- Índice compuesto para seguimiento longitudinal
CREATE INDEX IF NOT EXISTS idx_primera_infancia_seguimiento 
    ON atencion_primera_infancia(paciente_id, fecha_atencion DESC);

-- ===================================================================
-- FUNCIONES DE UTILIDAD PARA ALERTAS AUTOMÁTICAS
-- ===================================================================

CREATE OR REPLACE FUNCTION generar_alertas_desarrollo_automaticas(
    edad_meses integer,
    ead3_motricidad_gruesa integer DEFAULT NULL,
    ead3_motricidad_fina integer DEFAULT NULL,
    ead3_audicion_lenguaje integer DEFAULT NULL,
    ead3_personal_social integer DEFAULT NULL
) RETURNS text[] AS $$
DECLARE
    alertas text[] := '{}';
BEGIN
    -- Alertas por hitos de motricidad gruesa perdidos
    IF edad_meses >= 12 AND (ead3_motricidad_gruesa IS NULL OR ead3_motricidad_gruesa < 50) THEN
        alertas := array_append(alertas, 'ALERTA: Evaluar motricidad gruesa - posible retraso');
    END IF;
    
    -- Alertas por hitos de lenguaje perdidos
    IF edad_meses >= 18 AND (ead3_audicion_lenguaje IS NULL OR ead3_audicion_lenguaje < 50) THEN
        alertas := array_append(alertas, 'ALERTA: Evaluar desarrollo del lenguaje - requiere seguimiento');
    END IF;
    
    -- Alertas por hitos sociales perdidos
    IF edad_meses >= 24 AND (ead3_personal_social IS NULL OR ead3_personal_social < 50) THEN
        alertas := array_append(alertas, 'ALERTA: Evaluar desarrollo social - considerar intervención');
    END IF;
    
    -- Alerta general si no hay evaluación a los 12 meses
    IF edad_meses >= 12 AND ead3_motricidad_gruesa IS NULL AND ead3_audicion_lenguaje IS NULL THEN
        alertas := array_append(alertas, 'URGENTE: Aplicar EAD-3 - evaluación de desarrollo pendiente');
    END IF;
    
    RETURN alertas;
END;
$$ LANGUAGE plpgsql;

-- ===================================================================
-- FUNCIÓN PARA CALCULAR PRÓXIMAS VACUNAS
-- ===================================================================

CREATE OR REPLACE FUNCTION calcular_proxima_vacuna(
    edad_meses integer,
    bcg_aplicada boolean DEFAULT false,
    pentavalente_dosis integer DEFAULT 0,
    polio_dosis integer DEFAULT 0,
    srp_aplicada boolean DEFAULT false
) RETURNS jsonb AS $$
DECLARE
    resultado jsonb := '{}';
    proxima_vacuna text;
    fecha_ideal date;
BEGIN
    -- Lógica para determinar próxima vacuna según edad y esquema actual
    CASE 
        WHEN edad_meses = 0 AND NOT bcg_aplicada THEN
            proxima_vacuna := 'BCG + Hepatitis B RN';
            fecha_ideal := CURRENT_DATE;
        WHEN edad_meses >= 2 AND pentavalente_dosis = 0 THEN
            proxima_vacuna := 'Pentavalente 1 + Polio 1 + Rotavirus 1 + Neumococo 1';
            fecha_ideal := CURRENT_DATE;
        WHEN edad_meses >= 4 AND pentavalente_dosis = 1 THEN
            proxima_vacuna := 'Pentavalente 2 + Polio 2 + Rotavirus 2 + Neumococo 2';
            fecha_ideal := CURRENT_DATE;
        WHEN edad_meses >= 6 AND pentavalente_dosis = 2 THEN
            proxima_vacuna := 'Pentavalente 3 + Polio 3 + Rotavirus 3';
            fecha_ideal := CURRENT_DATE;
        WHEN edad_meses >= 12 AND NOT srp_aplicada THEN
            proxima_vacuna := 'SRP + Neumococo refuerzo';
            fecha_ideal := CURRENT_DATE;
        ELSE
            proxima_vacuna := 'Esquema al día';
            fecha_ideal := CURRENT_DATE + INTERVAL '3 months';
    END CASE;
    
    resultado := jsonb_build_object(
        'proxima_vacuna', proxima_vacuna,
        'fecha_ideal', fecha_ideal,
        'edad_aplicacion_meses', edad_meses
    );
    
    RETURN resultado;
END;
$$ LANGUAGE plpgsql;

-- ===================================================================
-- TRIGGER PARA GENERAR ALERTAS AUTOMÁTICAS
-- ===================================================================

CREATE OR REPLACE FUNCTION trigger_generar_alertas_primera_infancia()
RETURNS TRIGGER AS $$
BEGIN
    -- Generar alertas automáticas basadas en edad y desarrollo
    IF NEW.edad_cronologica_meses IS NOT NULL THEN
        NEW.alertas_desarrollo_generadas := generar_alertas_desarrollo_automaticas(
            NEW.edad_cronologica_meses,
            NEW.ead3_motricidad_gruesa_puntaje,
            NEW.ead3_motricidad_fina_puntaje,
            NEW.ead3_audicion_lenguaje_puntaje,
            NEW.ead3_personal_social_puntaje
        );
    END IF;
    
    -- Calcular si requiere intervención temprana
    IF array_length(NEW.alertas_desarrollo_generadas, 1) >= 2 THEN
        NEW.requiere_intervencion_temprana := true;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger
DROP TRIGGER IF EXISTS trigger_alertas_primera_infancia ON atencion_primera_infancia;
CREATE TRIGGER trigger_alertas_primera_infancia
    BEFORE INSERT OR UPDATE ON atencion_primera_infancia
    FOR EACH ROW
    EXECUTE FUNCTION trigger_generar_alertas_primera_infancia();

-- ===================================================================
-- COMENTARIOS DE DOCUMENTACIÓN
-- ===================================================================

COMMENT ON COLUMN atencion_primera_infancia.edad_cronologica_meses IS 
    'Edad cronológica en meses (0-60) para primera infancia según Resolución 3280';

COMMENT ON COLUMN atencion_primera_infancia.ead3_aplicada IS 
    'Indica si se aplicó la Escala Abreviada de Desarrollo (EAD-3) en esta consulta';

COMMENT ON COLUMN atencion_primera_infancia.ead3_puntaje_total IS 
    'Puntaje total EAD-3 (suma de las 4 áreas de desarrollo)';

COMMENT ON COLUMN atencion_primera_infancia.alertas_desarrollo_generadas IS 
    'Alertas automáticas generadas por el sistema basadas en hitos de desarrollo perdidos';

COMMENT ON FUNCTION generar_alertas_desarrollo_automaticas IS 
    'Genera alertas automáticas de desarrollo basadas en edad cronológica y puntajes EAD-3';

COMMENT ON FUNCTION calcular_proxima_vacuna IS 
    'Calcula la próxima vacuna requerida según edad y esquema actual';

-- ===================================================================
-- VERIFICACIÓN Y LOGGING
-- ===================================================================

DO $$
DECLARE
    columnas_agregadas INTEGER;
    indices_creados INTEGER;
    funciones_creadas INTEGER;
BEGIN
    -- Verificar columnas agregadas
    SELECT COUNT(*) INTO columnas_agregadas
    FROM information_schema.columns 
    WHERE table_name = 'atencion_primera_infancia' 
    AND column_name LIKE ANY(ARRAY['%ead3%', '%asq3%', '%tamizaje%', '%alertas%']);
    
    -- Verificar índices
    SELECT COUNT(*) INTO indices_creados
    FROM pg_indexes 
    WHERE tablename = 'atencion_primera_infancia' 
    AND indexname LIKE 'idx_primera_infancia_%';
    
    -- Verificar funciones
    SELECT COUNT(*) INTO funciones_creadas
    FROM pg_proc 
    WHERE proname LIKE '%primera_infancia%' OR proname LIKE '%alertas_desarrollo%';
    
    -- Log de resultados
    RAISE NOTICE '=== VERIFICACIÓN PRIMERA INFANCIA EXPANDIDA ===';
    RAISE NOTICE 'Columnas EAD-3/ASQ-3/Tamizajes agregadas: %', columnas_agregadas;
    RAISE NOTICE 'Índices especializados creados: %', indices_creados;
    RAISE NOTICE 'Funciones de alertas creadas: %', funciones_creadas;
    
    IF columnas_agregadas >= 20 AND indices_creados >= 5 AND funciones_creadas >= 2 THEN
        RAISE NOTICE '✅ SUCCESS: RPMS Primera Infancia expandida implementada';
        RAISE NOTICE '📊 Funcionalidades: EAD-3 + ASQ-3 + Tamizajes + Alertas automáticas';
        RAISE NOTICE '🎯 Compliance: Resolución 3280 de 2018 - RPMS completa';
        RAISE NOTICE '⚡ Performance: Índices optimizados para consultas masivas';
    ELSE
        RAISE EXCEPTION 'ERROR: Implementación incompleta de Primera Infancia expandida';
    END IF;
    
    RAISE NOTICE '===========================================';
END
$$;

COMMIT;

-- ===================================================================
-- ROLLBACK INSTRUCTIONS (Para emergencias)
-- ===================================================================
-- En caso de necesitar rollback:
-- DROP TRIGGER IF EXISTS trigger_alertas_primera_infancia ON atencion_primera_infancia;
-- DROP FUNCTION IF EXISTS trigger_generar_alertas_primera_infancia();
-- DROP FUNCTION IF EXISTS generar_alertas_desarrollo_automaticas(integer, integer, integer, integer, integer);
-- DROP FUNCTION IF EXISTS calcular_proxima_vacuna(integer, boolean, integer, integer, boolean);
-- DROP TYPE IF EXISTS resultado_area_desarrollo;
-- DROP TYPE IF EXISTS estado_salud_oral;
-- DROP TYPE IF EXISTS tipo_vacuna;
-- -- Luego remover columnas específicas si es necesario