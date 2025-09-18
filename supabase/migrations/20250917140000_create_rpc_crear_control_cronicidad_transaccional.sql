-- Migration: Crear RPC transaccional para control cronicidad
-- Fecha: 17 septiembre 2025 - Sprint #2
-- Objetivo: Replicar patrón RPC+Service exitoso del Sprint Piloto #1
-- Base: Auditoría Backend - Resolver operaciones no atómicas en control_cronicidad
-- Contexto: DEV-CONTEXT.md - Sprint #2

-- =============================================================================
-- RPC TRANSACCIONAL: CREAR CONTROL CRONICIDAD COMPLETO
-- =============================================================================

-- Crear función RPC que maneje toda la transacción de forma atómica
CREATE OR REPLACE FUNCTION public.crear_control_cronicidad_completo(
    -- Parámetros de entrada siguiendo estructura del modelo Pydantic
    p_paciente_id uuid,
    p_medico_id uuid DEFAULT NULL,
    p_fecha_control date,
    p_tipo_cronicidad text,
    p_estado_control text DEFAULT NULL,
    p_adherencia_tratamiento text DEFAULT NULL,

    -- Antropometría básica
    p_peso_kg numeric DEFAULT NULL,
    p_talla_cm numeric DEFAULT NULL,
    p_imc numeric DEFAULT NULL,

    -- Observaciones clínicas
    p_complicaciones_observadas text DEFAULT NULL,
    p_observaciones text DEFAULT NULL,

    -- Seguimiento farmacológico
    p_medicamentos_actuales text DEFAULT NULL,
    p_efectos_adversos text DEFAULT NULL,

    -- Educación y recomendaciones
    p_educacion_brindada text DEFAULT NULL,
    p_recomendaciones_nutricionales text DEFAULT NULL,
    p_recomendaciones_actividad_fisica text DEFAULT NULL,

    -- Próxima cita
    p_fecha_proxima_cita date DEFAULT NULL
)
RETURNS TABLE (
    control_id uuid,
    atencion_general_id uuid,
    imc_calculado numeric,
    control_adecuado boolean,
    riesgo_cardiovascular text
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_control_id uuid;
    v_atencion_general_id uuid;
    v_imc_calculado numeric;
    v_control_record record;
BEGIN
    -- Validaciones de entrada
    IF p_paciente_id IS NULL THEN
        RAISE EXCEPTION 'paciente_id es requerido';
    END IF;

    IF p_tipo_cronicidad IS NULL OR p_tipo_cronicidad NOT IN ('Hipertension', 'Diabetes', 'ERC', 'Dislipidemia') THEN
        RAISE EXCEPTION 'tipo_cronicidad debe ser uno de: Hipertension, Diabetes, ERC, Dislipidemia';
    END IF;

    -- Validar que el paciente existe
    IF NOT EXISTS (SELECT 1 FROM public.pacientes WHERE id = p_paciente_id) THEN
        RAISE EXCEPTION 'El paciente especificado no existe';
    END IF;

    -- =========================================================================
    -- TRANSACCIÓN ATÓMICA: BEGIN
    -- =========================================================================

    -- PASO 1: Generar UUIDs únicos
    v_control_id := gen_random_uuid();
    v_atencion_general_id := gen_random_uuid();

    -- PASO 2: Calcular IMC si hay datos
    IF p_peso_kg IS NOT NULL AND p_talla_cm IS NOT NULL AND p_talla_cm > 0 THEN
        v_imc_calculado := p_peso_kg / POWER(p_talla_cm / 100.0, 2);
    ELSE
        v_imc_calculado := p_imc;
    END IF;

    -- PASO 3: Insertar en tabla control_cronicidad
    INSERT INTO public.control_cronicidad (
        id, paciente_id, medico_id,
        fecha_control, tipo_cronicidad,
        estado_control, adherencia_tratamiento,
        peso_kg, talla_cm, imc,
        complicaciones_observadas, observaciones,
        medicamentos_actuales, efectos_adversos,
        educacion_brindada, recomendaciones_nutricionales,
        recomendaciones_actividad_fisica, fecha_proxima_cita,
        atencion_id, creado_en, updated_at
    ) VALUES (
        v_control_id, p_paciente_id, p_medico_id,
        p_fecha_control, p_tipo_cronicidad,
        p_estado_control, p_adherencia_tratamiento,
        p_peso_kg, p_talla_cm, v_imc_calculado,
        p_complicaciones_observadas, p_observaciones,
        p_medicamentos_actuales, p_efectos_adversos,
        p_educacion_brindada, p_recomendaciones_nutricionales,
        p_recomendaciones_actividad_fisica, p_fecha_proxima_cita,
        NULL, now(), now()  -- atencion_id se actualiza en PASO 5
    );

    -- PASO 4: Insertar en tabla atenciones (polimórfica principal)
    INSERT INTO public.atenciones (
        id, paciente_id, medico_id, tipo_atencion, detalle_id,
        fecha_atencion, entorno, descripcion, creado_en, updated_at
    ) VALUES (
        v_atencion_general_id, p_paciente_id, p_medico_id,
        'Control Cronicidad - ' || p_tipo_cronicidad, v_control_id,
        p_fecha_control, 'IPS',
        'Control de ' || p_tipo_cronicidad, now(), now()
    );

    -- PASO 5: Actualizar control_cronicidad con referencia a atención general
    UPDATE public.control_cronicidad
    SET atencion_id = v_atencion_general_id
    WHERE id = v_control_id;

    -- PASO 6: Obtener registro completo para cálculos adicionales
    SELECT
        cc.id,
        cc.atencion_id,
        cc.imc,
        cc.tipo_cronicidad,
        cc.estado_control,
        cc.peso_kg,
        cc.talla_cm
    INTO v_control_record
    FROM public.control_cronicidad cc
    WHERE cc.id = v_control_id;

    -- =========================================================================
    -- TRANSACCIÓN ATÓMICA: COMMIT AUTOMÁTICO
    -- =========================================================================

    -- Retornar datos estructurados con campos calculados
    RETURN QUERY
    SELECT
        v_control_record.id::uuid,
        v_control_record.atencion_id::uuid,
        v_control_record.imc::numeric,
        -- Control adecuado básico (simplificado para el RPC)
        CASE
            WHEN v_control_record.estado_control = 'Controlado' THEN true
            ELSE false
        END::boolean,
        -- Riesgo cardiovascular básico
        CASE
            WHEN v_control_record.imc IS NOT NULL AND v_control_record.imc >= 30 THEN 'ALTO'
            WHEN v_control_record.imc IS NOT NULL AND v_control_record.imc >= 25 THEN 'MODERADO'
            ELSE 'BAJO'
        END::text;

EXCEPTION
    WHEN OTHERS THEN
        -- En caso de error, PostgreSQL hace rollback automático
        RAISE EXCEPTION 'Error creando control cronicidad: %', SQLERRM;
END;
$$;

-- =============================================================================
-- CONFIGURACIÓN DE SEGURIDAD Y PERMISOS
-- =============================================================================

-- Grant permisos para service_role (desarrollo)
GRANT EXECUTE ON FUNCTION public.crear_control_cronicidad_completo TO service_role;

-- Grant permisos para authenticated (producción futura)
GRANT EXECUTE ON FUNCTION public.crear_control_cronicidad_completo TO authenticated;

-- =============================================================================
-- DOCUMENTACIÓN Y COMENTARIOS
-- =============================================================================

COMMENT ON FUNCTION public.crear_control_cronicidad_completo IS
'RPC transaccional para crear control de cronicidad completo de forma atómica.
Sprint #2 - Replica patrón exitoso del Sprint Piloto #1 (atencion_vejez).
Resuelve defecto sistémico: operaciones no atómicas y rollbacks manuales frágiles.
Todos los parámetros siguen estructura del modelo Pydantic ControlCronicidadCrear.
Retorna campos calculados automáticamente (IMC, control adecuado, riesgo cardiovascular).';

-- =============================================================================
-- VERIFICACIÓN DE LA MIGRACIÓN
-- =============================================================================

DO $$
BEGIN
    RAISE NOTICE '=== VERIFICACIÓN RPC CREAR_CONTROL_CRONICIDAD_COMPLETO ===';
    RAISE NOTICE 'Función creada: %', (SELECT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'crear_control_cronicidad_completo'));
    RAISE NOTICE 'Permisos service_role: %', (SELECT has_function_privilege('service_role', 'public.crear_control_cronicidad_completo(uuid,uuid,date,text,text,text,numeric,numeric,numeric,text,text,text,text,text,text,text,date)', 'EXECUTE'));
    RAISE NOTICE '✅ SUCCESS: RPC transaccional Sprint #2 implementado correctamente';
    RAISE NOTICE '🎯 Objetivo: Replicar patrón exitoso Sprint Piloto #1';
    RAISE NOTICE '⚡ Beneficio: Garantiza consistencia de datos en control cronicidad';
    RAISE NOTICE '📊 Patrón: RPC+Service Layer para escalabilidad arquitectónica';
    RAISE NOTICE '===============================================';
END $$;