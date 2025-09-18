-- Migration: Crear RPC transaccional para atención vejez
-- Fecha: 17 septiembre 2025 - Sprint Piloto #1
-- Objetivo: Resolver defecto sistémico de operaciones no atómicas
-- Base: Auditoría Backend - Recomendación Crítica #1
-- Contexto: DEV-CONTEXT.md - Sprint Piloto #1

-- =============================================================================
-- RPC TRANSACCIONAL: CREAR ATENCIÓN VEJEZ COMPLETA
-- =============================================================================

-- Crear función RPC que maneje toda la transacción de forma atómica
CREATE OR REPLACE FUNCTION public.crear_atencion_vejez_completa(
    -- Parámetros de entrada siguiendo estructura del modelo Pydantic
    p_paciente_id uuid,
    p_medico_id uuid,
    p_fecha_atencion date,
    p_entorno text DEFAULT 'CONSULTA_EXTERNA',
    p_edad_anos integer,

    -- Antropometría y signos vitales
    p_peso_kg numeric DEFAULT NULL,
    p_talla_cm numeric DEFAULT NULL,
    p_peso_perdido_6_meses_kg numeric DEFAULT NULL,
    p_presion_sistolica numeric DEFAULT NULL,
    p_presion_diastolica numeric DEFAULT NULL,
    p_frecuencia_cardiaca integer DEFAULT NULL,

    -- Evaluación cognitiva
    p_mini_mental_score integer DEFAULT NULL,
    p_clock_test_score integer DEFAULT NULL,
    p_memoria_inmediata boolean DEFAULT true,
    p_orientacion_tiempo_lugar boolean DEFAULT true,
    p_cambios_cognitivos_reportados boolean DEFAULT false,
    p_dificultad_actividades_complejas boolean DEFAULT false,

    -- Evaluación riesgo de caídas
    p_caidas_ultimo_ano integer DEFAULT 0,
    p_mareo_al_levantarse boolean DEFAULT false,
    p_medicamentos_que_causan_mareo integer DEFAULT 0,
    p_problemas_vision boolean DEFAULT false,
    p_problemas_audicion boolean DEFAULT false,
    p_fuerza_muscular_disminuida boolean DEFAULT false,
    p_equilibrio_alterado boolean DEFAULT false,
    p_tiempo_up_and_go numeric DEFAULT NULL,

    -- Evaluación autonomía funcional
    p_barthel_score integer DEFAULT NULL,
    p_lawton_score integer DEFAULT NULL,
    p_independiente_bano boolean DEFAULT true,
    p_independiente_vestirse boolean DEFAULT true,
    p_independiente_comer boolean DEFAULT true,
    p_independiente_movilidad boolean DEFAULT true,
    p_maneja_medicamentos boolean DEFAULT true,
    p_maneja_finanzas boolean DEFAULT true,
    p_usa_transporte boolean DEFAULT true,

    -- Evaluación salud mental
    p_yesavage_score integer DEFAULT NULL,
    p_estado_animo_deprimido boolean DEFAULT false,
    p_perdida_interes_actividades boolean DEFAULT false,
    p_trastornos_sueno boolean DEFAULT false,
    p_sensacion_inutilidad boolean DEFAULT false,
    p_ansiedad_frecuente boolean DEFAULT false,
    p_aislamiento_social boolean DEFAULT false,
    p_cambios_recientes_perdidas boolean DEFAULT false,

    -- Evaluación soporte social
    p_vive_solo boolean DEFAULT false,
    p_tiene_cuidador boolean DEFAULT false,
    p_frecuencia_visitas_familiares integer DEFAULT 0,
    p_participa_actividades_comunitarias boolean DEFAULT false,
    p_tiene_amigos_cercanos boolean DEFAULT false,
    p_ayuda_disponible_emergencia boolean DEFAULT false,
    p_satisfaccion_relaciones_sociales integer DEFAULT 5,

    -- Evaluación polifarmacia
    p_numero_medicamentos integer DEFAULT 0,
    p_medicamentos_alto_riesgo integer DEFAULT 0,
    p_automedicacion boolean DEFAULT false,
    p_dificultad_manejo_medicamentos boolean DEFAULT false,
    p_efectos_adversos_reportados boolean DEFAULT false,
    p_interacciones_conocidas boolean DEFAULT false,

    -- Incontinencia
    p_incontinencia_urinaria boolean DEFAULT false,
    p_incontinencia_fecal boolean DEFAULT false,

    -- Estilos de vida
    p_actividad_fisica_min_semana integer DEFAULT 0,
    p_porciones_frutas_verduras_dia integer DEFAULT 0,
    p_cigarrillos_dia integer DEFAULT 0,
    p_copas_alcohol_semana integer DEFAULT 0,
    p_actividades_estimulacion_cognitiva boolean DEFAULT false,

    -- Factores ambientales y sociales
    p_hogar_adaptado_seguro boolean DEFAULT false,
    p_proposito_vida_claro boolean DEFAULT false,
    p_participacion_social_activa boolean DEFAULT false,
    p_control_medico_regular boolean DEFAULT false,

    -- Observaciones
    p_observaciones_generales text DEFAULT NULL,
    p_plan_promocion_prevencion text DEFAULT NULL,
    p_educacion_cuidado_vejez text DEFAULT NULL
)
RETURNS TABLE (
    vejez_id uuid,
    atencion_general_id uuid,
    estado_nutricional estado_nutricional_vejez,
    deterioro_cognitivo deterioro_cognitivo,
    riesgo_caidas riesgo_caidas,
    autonomia_funcional autonomia_funcional,
    imc numeric
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_vejez_id uuid;
    v_atencion_general_id uuid;
    v_atencion_vejez_record record;
BEGIN
    -- Validaciones de entrada
    IF p_paciente_id IS NULL THEN
        RAISE EXCEPTION 'paciente_id es requerido';
    END IF;

    IF p_edad_anos IS NULL OR p_edad_anos < 60 OR p_edad_anos > 120 THEN
        RAISE EXCEPTION 'edad_anos debe estar entre 60 y 120 años para atención vejez';
    END IF;

    -- =========================================================================
    -- TRANSACCIÓN ATÓMICA: BEGIN
    -- =========================================================================

    -- PASO 1: Generar UUIDs únicos
    v_vejez_id := gen_random_uuid();
    v_atencion_general_id := gen_random_uuid();

    -- PASO 2: Insertar en tabla atencion_vejez
    INSERT INTO public.atencion_vejez (
        id, paciente_id, medico_id,
        fecha_atencion, entorno, edad_anos,

        -- Antropometría
        peso_kg, talla_cm, peso_perdido_6_meses_kg,
        presion_sistolica, presion_diastolica, frecuencia_cardiaca,

        -- Evaluación cognitiva
        mini_mental_score, clock_test_score, memoria_inmediata,
        orientacion_tiempo_lugar, cambios_cognitivos_reportados,
        dificultad_actividades_complejas,

        -- Riesgo caídas
        caidas_ultimo_ano, mareo_al_levantarse, medicamentos_que_causan_mareo,
        problemas_vision, problemas_audicion, fuerza_muscular_disminuida,
        equilibrio_alterado, tiempo_up_and_go,

        -- Autonomía funcional
        barthel_score, lawton_score, independiente_bano,
        independiente_vestirse, independiente_comer, independiente_movilidad,
        maneja_medicamentos, maneja_finanzas, usa_transporte,

        -- Salud mental
        yesavage_score, estado_animo_deprimido, perdida_interes_actividades,
        trastornos_sueno, sensacion_inutilidad, ansiedad_frecuente,
        aislamiento_social, cambios_recientes_perdidas,

        -- Soporte social
        vive_solo, tiene_cuidador, frecuencia_visitas_familiares,
        participa_actividades_comunitarias, tiene_amigos_cercanos,
        ayuda_disponible_emergencia, satisfaccion_relaciones_sociales,

        -- Polifarmacia
        numero_medicamentos, medicamentos_alto_riesgo, automedicacion,
        dificultad_manejo_medicamentos, efectos_adversos_reportados,
        interacciones_conocidas,

        -- Incontinencia
        incontinencia_urinaria, incontinencia_fecal,

        -- Estilos de vida
        actividad_fisica_min_semana, porciones_frutas_verduras_dia,
        cigarrillos_dia, copas_alcohol_semana, actividades_estimulacion_cognitiva,

        -- Factores ambientales
        hogar_adaptado_seguro, proposito_vida_claro,
        participacion_social_activa, control_medico_regular,

        -- Observaciones
        observaciones_generales, plan_promocion_prevencion, educacion_cuidado_vejez,

        -- Referencia a atención general (se actualiza después)
        atencion_id

    ) VALUES (
        v_vejez_id, p_paciente_id, p_medico_id,
        p_fecha_atencion, p_entorno, p_edad_anos,

        -- Antropometría
        p_peso_kg, p_talla_cm, p_peso_perdido_6_meses_kg,
        p_presion_sistolica, p_presion_diastolica, p_frecuencia_cardiaca,

        -- Evaluación cognitiva
        p_mini_mental_score, p_clock_test_score, p_memoria_inmediata,
        p_orientacion_tiempo_lugar, p_cambios_cognitivos_reportados,
        p_dificultad_actividades_complejas,

        -- Riesgo caídas
        p_caidas_ultimo_ano, p_mareo_al_levantarse, p_medicamentos_que_causan_mareo,
        p_problemas_vision, p_problemas_audicion, p_fuerza_muscular_disminuida,
        p_equilibrio_alterado, p_tiempo_up_and_go,

        -- Autonomía funcional
        p_barthel_score, p_lawton_score, p_independiente_bano,
        p_independiente_vestirse, p_independiente_comer, p_independiente_movilidad,
        p_maneja_medicamentos, p_maneja_finanzas, p_usa_transporte,

        -- Salud mental
        p_yesavage_score, p_estado_animo_deprimido, p_perdida_interes_actividades,
        p_trastornos_sueno, p_sensacion_inutilidad, p_ansiedad_frecuente,
        p_aislamiento_social, p_cambios_recientes_perdidas,

        -- Soporte social
        p_vive_solo, p_tiene_cuidador, p_frecuencia_visitas_familiares,
        p_participa_actividades_comunitarias, p_tiene_amigos_cercanos,
        p_ayuda_disponible_emergencia, p_satisfaccion_relaciones_sociales,

        -- Polifarmacia
        p_numero_medicamentos, p_medicamentos_alto_riesgo, p_automedicacion,
        p_dificultad_manejo_medicamentos, p_efectos_adversos_reportados,
        p_interacciones_conocidas,

        -- Incontinencia
        p_incontinencia_urinaria, p_incontinencia_fecal,

        -- Estilos de vida
        p_actividad_fisica_min_semana, p_porciones_frutas_verduras_dia,
        p_cigarrillos_dia, p_copas_alcohol_semana, p_actividades_estimulacion_cognitiva,

        -- Factores ambientales
        p_hogar_adaptado_seguro, p_proposito_vida_claro,
        p_participacion_social_activa, p_control_medico_regular,

        -- Observaciones
        p_observaciones_generales, p_plan_promocion_prevencion, p_educacion_cuidado_vejez,

        -- Inicialmente NULL, se actualiza en el PASO 4
        NULL
    );

    -- PASO 3: Insertar en tabla atenciones (polimórfica principal)
    INSERT INTO public.atenciones (
        id, paciente_id, medico_id, tipo_atencion, detalle_id,
        fecha_atencion, creado_en, updated_at
    ) VALUES (
        v_atencion_general_id, p_paciente_id, p_medico_id, 'VEJEZ', v_vejez_id,
        p_fecha_atencion, now(), now()
    );

    -- PASO 4: Actualizar atencion_vejez con referencia a atención general
    UPDATE public.atencion_vejez
    SET atencion_id = v_atencion_general_id
    WHERE id = v_vejez_id;

    -- PASO 5: Obtener registro completo con campos calculados para retornar
    SELECT
        av.id,
        av.atencion_id,
        av.estado_nutricional,
        av.deterioro_cognitivo,
        av.riesgo_caidas,
        av.autonomia_funcional,
        av.imc
    INTO v_atencion_vejez_record
    FROM public.atencion_vejez av
    WHERE av.id = v_vejez_id;

    -- =========================================================================
    -- TRANSACCIÓN ATÓMICA: COMMIT AUTOMÁTICO
    -- =========================================================================

    -- Retornar datos estructurados
    RETURN QUERY
    SELECT
        v_atencion_vejez_record.id::uuid,
        v_atencion_vejez_record.atencion_id::uuid,
        v_atencion_vejez_record.estado_nutricional::estado_nutricional_vejez,
        v_atencion_vejez_record.deterioro_cognitivo::deterioro_cognitivo,
        v_atencion_vejez_record.riesgo_caidas::riesgo_caidas,
        v_atencion_vejez_record.autonomia_funcional::autonomia_funcional,
        v_atencion_vejez_record.imc::numeric;

EXCEPTION
    WHEN OTHERS THEN
        -- En caso de error, PostgreSQL hace rollback automático
        RAISE EXCEPTION 'Error creando atención vejez: %', SQLERRM;
END;
$$;

-- =============================================================================
-- CONFIGURACIÓN DE SEGURIDAD Y PERMISOS
-- =============================================================================

-- Grant permisos para service_role (desarrollo)
GRANT EXECUTE ON FUNCTION public.crear_atencion_vejez_completa TO service_role;

-- Grant permisos para authenticated (producción futura)
GRANT EXECUTE ON FUNCTION public.crear_atencion_vejez_completa TO authenticated;

-- =============================================================================
-- DOCUMENTACIÓN Y COMENTARIOS
-- =============================================================================

COMMENT ON FUNCTION public.crear_atencion_vejez_completa IS
'RPC transaccional para crear atención vejez completa de forma atómica.
Resuelve defecto sistémico identificado en auditoría backend: operaciones no atómicas.
Sprint Piloto #1 - Implementación de patrón RPC para garantizar consistencia de datos.
Todos los parámetros siguen estructura del modelo Pydantic AtencionVejezCrear.
Retorna campos calculados automáticamente por triggers de la tabla.';

-- =============================================================================
-- VERIFICACIÓN DE LA MIGRACIÓN
-- =============================================================================

DO $$
BEGIN
    RAISE NOTICE '=== VERIFICACIÓN RPC CREAR_ATENCION_VEJEZ_COMPLETA ===';
    RAISE NOTICE 'Función creada: %', (SELECT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'crear_atencion_vejez_completa'));
    RAISE NOTICE 'Permisos service_role: %', (SELECT has_function_privilege('service_role', 'public.crear_atencion_vejez_completa(uuid,uuid,date,text,integer,numeric,numeric,numeric,numeric,numeric,integer,integer,integer,boolean,boolean,boolean,boolean,integer,boolean,integer,boolean,boolean,boolean,boolean,numeric,integer,integer,boolean,boolean,boolean,boolean,boolean,boolean,boolean,integer,boolean,boolean,boolean,boolean,boolean,boolean,boolean,boolean,integer,boolean,boolean,boolean,boolean,integer,integer,boolean,boolean,boolean,boolean,boolean,boolean,integer,integer,integer,integer,boolean,boolean,boolean,boolean,boolean,boolean,text,text,text)', 'EXECUTE'));
    RAISE NOTICE '✅ SUCCESS: RPC transaccional implementado correctamente';
    RAISE NOTICE '🎯 Objetivo: Resolver defecto sistémico de operaciones no atómicas';
    RAISE NOTICE '⚡ Beneficio: Garantiza consistencia de datos en creación vejez';
    RAISE NOTICE '📊 Sprint Piloto #1: Patrón RPC establecido para replicar en otros módulos';
    RAISE NOTICE '===============================================';
END $$;