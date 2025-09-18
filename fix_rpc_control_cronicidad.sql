-- Función RPC corregida para Control Cronicidad
CREATE OR REPLACE FUNCTION public.crear_control_cronicidad_completo(
    p_paciente_id uuid,
    p_fecha_control date,
    p_tipo_cronicidad text,
    p_medico_id uuid DEFAULT NULL,
    p_estado_control text DEFAULT NULL,
    p_adherencia_tratamiento text DEFAULT NULL,
    p_peso_kg numeric DEFAULT NULL,
    p_talla_cm numeric DEFAULT NULL,
    p_imc numeric DEFAULT NULL,
    p_complicaciones_observadas text DEFAULT NULL,
    p_observaciones text DEFAULT NULL,
    p_medicamentos_actuales text DEFAULT NULL,
    p_efectos_adversos text DEFAULT NULL,
    p_educacion_brindada text DEFAULT NULL,
    p_recomendaciones_nutricionales text DEFAULT NULL,
    p_recomendaciones_actividad_fisica text DEFAULT NULL,
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

    -- Generar UUIDs únicos
    v_control_id := gen_random_uuid();
    v_atencion_general_id := gen_random_uuid();

    -- Calcular IMC si hay datos
    IF p_peso_kg IS NOT NULL AND p_talla_cm IS NOT NULL AND p_talla_cm > 0 THEN
        v_imc_calculado := p_peso_kg / POWER(p_talla_cm / 100.0, 2);
    ELSE
        v_imc_calculado := p_imc;
    END IF;

    -- Insertar en tabla atenciones PRIMERO
    INSERT INTO public.atenciones (
        id, paciente_id, medico_id, tipo_atencion, detalle_id,
        fecha_atencion, entorno, descripcion, creado_en, updated_at
    ) VALUES (
        v_atencion_general_id, p_paciente_id, p_medico_id,
        'Control Cronicidad - ' || p_tipo_cronicidad, v_control_id,
        p_fecha_control, 'IPS',
        'Control de ' || p_tipo_cronicidad, now(), now()
    );

    -- Insertar en tabla control_cronicidad
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
        v_atencion_general_id, now(), now()
    );

    -- Obtener registro completo para cálculos adicionales
    SELECT
        cc.id,
        cc.atencion_id,
        cc.imc,
        cc.tipo_cronicidad,
        cc.estado_control
    INTO v_control_record
    FROM public.control_cronicidad cc
    WHERE cc.id = v_control_id;

    -- Retornar datos estructurados con campos calculados
    RETURN QUERY
    SELECT
        v_control_record.id::uuid,
        v_control_record.atencion_id::uuid,
        v_control_record.imc::numeric,
        -- Control adecuado básico
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
        RAISE EXCEPTION 'Error creando control cronicidad: %', SQLERRM;
END;
$$;

-- Otorgar permisos
GRANT EXECUTE ON FUNCTION public.crear_control_cronicidad_completo TO service_role;
GRANT EXECUTE ON FUNCTION public.crear_control_cronicidad_completo TO authenticated;

-- Marcar migración como aplicada
INSERT INTO supabase_migrations.schema_migrations (version) VALUES ('20250917140000')
ON CONFLICT (version) DO NOTHING;

-- Verificación
SELECT 'Control Cronicidad RPC creado exitosamente' as status;