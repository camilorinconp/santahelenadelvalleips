-- =====================================================================================
-- CREAR TABLAS TRANSVERSALES EN SUPABASE REMOTO - VERSION CORREGIDA
-- Fecha: 2025-09-13
-- Descripción: Script compatible con Supabase para crear las 3 tablas transversales
-- =====================================================================================

-- ====================
-- CREAR TIPOS ENUM (SIN IF NOT EXISTS)
-- ====================
DO $$
BEGIN
    -- Crear tipos solo si no existen
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_entorno_salud_publica') THEN
        CREATE TYPE tipo_entorno_salud_publica AS ENUM (
            'ENTORNO_FAMILIAR_HOGAR_DOMESTICO',
            'ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL', 
            'ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL',
            'ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO',
            'ENTORNO_INSTITUCIONAL_SERVICIOS_SALUD'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nivel_complejidad_intervencion_entorno') THEN
        CREATE TYPE nivel_complejidad_intervencion_entorno AS ENUM (
            'BASICO_PROMOCION_PREVENCION',
            'INTERMEDIO_INTERVENCION_TEMPRANA',
            'AVANZADO_MANEJO_ESPECIALIZADO',
            'INTEGRAL_COORDINACION_INTERSECTORIAL'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_activacion_entorno') THEN
        CREATE TYPE estado_activacion_entorno AS ENUM (
            'ACTIVO_OPERATIVO',
            'PARCIALMENTE_ACTIVO',
            'INACTIVO_TEMPORAL',
            'DESACTIVADO_DEFINITIVO'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_estructura_familiar_integral') THEN
        CREATE TYPE tipo_estructura_familiar_integral AS ENUM (
            'NUCLEAR_BIPARENTAL',
            'NUCLEAR_MONOPARENTAL',
            'EXTENSA_MULTIGENERACIONAL',
            'COMPUESTA_ALLEGADOS',
            'UNIPERSONAL_INDIVIDUAL'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ciclo_vital_familiar') THEN
        CREATE TYPE ciclo_vital_familiar AS ENUM (
            'FORMACION_PAREJA',
            'EXPANSION_HIJOS_PEQUENOS',
            'CONSOLIDACION_HIJOS_ESCOLARES',
            'APERTURA_HIJOS_ADOLESCENTES',
            'PLATAFORMA_LANZAMIENTO_JOVENES',
            'NIDO_VACIO_PAREJA_MADURA',
            'DISOLUCACION_VIUDEZ_SEPARACION'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nivel_socioeconomico_familiar') THEN
        CREATE TYPE nivel_socioeconomico_familiar AS ENUM (
            'ESTRATO_1_BAJO_BAJO',
            'ESTRATO_2_BAJO',
            'ESTRATO_3_MEDIO_BAJO',
            'ESTRATO_4_MEDIO',
            'ESTRATO_5_MEDIO_ALTO',
            'ESTRATO_6_ALTO'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_abordaje_atencion_integral_salud') THEN
        CREATE TYPE tipo_abordaje_atencion_integral_salud AS ENUM (
            'INDIVIDUAL_PERSONALIZADO',
            'FAMILIAR_GRUPAL',
            'COMUNITARIO_COLECTIVO',
            'POBLACIONAL_MASIVO',
            'INTERSECTORIAL_COORDINADO'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'modalidad_atencion_integral') THEN
        CREATE TYPE modalidad_atencion_integral AS ENUM (
            'PRESENCIAL_DIRECTA',
            'VIRTUAL_REMOTA',
            'MIXTA_HIBRIDA',
            'DOMICILIARIA_TERRENO',
            'INSTITUCIONAL_AMBULATORIA'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nivel_complejidad_atencion_integral') THEN
        CREATE TYPE nivel_complejidad_atencion_integral AS ENUM (
            'BASICO_PROMOCION_PREVENCION',
            'INTERMEDIO_DETECCION_TEMPRANA',
            'AVANZADO_INTERVENCION_ESPECIALIZADA',
            'ALTA_COMPLEJIDAD_MULTIDISCIPLINARIA'
        );
    END IF;

    RAISE NOTICE 'Tipos ENUM creados exitosamente';
END $$;

-- ====================
-- TABLA 1: ENTORNOS_SALUD_PUBLICA
-- ====================
CREATE TABLE entornos_salud_publica (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    codigo_identificacion_entorno_unico text UNIQUE NOT NULL,
    tipo_entorno tipo_entorno_salud_publica NOT NULL,
    nombre_descriptivo_entorno text NOT NULL,
    descripcion_caracterizacion_entorno text,
    nivel_complejidad_intervencion nivel_complejidad_intervencion_entorno DEFAULT 'BASICO_PROMOCION_PREVENCION',
    estado_activacion estado_activacion_entorno DEFAULT 'ACTIVO_OPERATIVO',
    departamento_ubicacion text,
    municipio_ubicacion text,
    zona_territorial text,
    coordenadas_geograficas jsonb,
    poblacion_objetivo_estimada integer,
    rango_edad_poblacion_objetivo text,
    caracteristicas_demograficas_poblacion jsonb,
    recursos_disponibles_entorno jsonb,
    actores_institucionales_involucrados jsonb,
    programas_servicios_disponibles jsonb,
    intervenciones_realizadas_historico jsonb,
    indicadores_resultado_entorno jsonb,
    plan_trabajo_entorno_vigente jsonb,
    alianzas_estrategicas_activas jsonb,
    coordinacion_institucional_nivel text,
    mecanismos_participacion_comunitaria jsonb,
    fecha_ultima_caracterizacion timestamptz,
    proxima_fecha_evaluacion timestamptz,
    responsable_coordinacion_entorno text,
    observaciones_adicionales_entorno text,
    creado_en timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    creado_por uuid,
    actualizado_por uuid
);

-- ====================
-- TABLA 2: FAMILIA_INTEGRAL_SALUD_PUBLICA
-- ====================
CREATE TABLE familia_integral_salud_publica (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    codigo_identificacion_familia_unico text UNIQUE NOT NULL,
    tipo_estructura_familiar tipo_estructura_familiar_integral NOT NULL,
    ciclo_vital_familiar ciclo_vital_familiar NOT NULL,
    nombre_apellidos_jefe_hogar text NOT NULL,
    numero_integrantes_familia integer NOT NULL,
    nivel_socioeconomico nivel_socioeconomico_familiar,
    direccion_residencia_completa text NOT NULL,
    telefono_contacto_principal text,
    correo_electronico_familia text,
    medico_familiar_asignado_id uuid,
    entorno_salud_publica_id uuid REFERENCES entornos_salud_publica(id),
    caracteristicas_vivienda_jsonb jsonb,
    condiciones_saneamiento_basico jsonb,
    acceso_servicios_salud_jsonb jsonb,
    antecedentes_patologicos_familiares jsonb,
    factores_riesgo_identificados jsonb,
    fortalezas_recursos_familiares jsonb,
    dinamica_relacional_familiar jsonb,
    apoyo_social_redes_disponibles jsonb,
    plan_atencion_integral_familiar jsonb,
    intervenciones_realizadas_familia jsonb,
    seguimiento_indicadores_familiares jsonb,
    fecha_primera_caracterizacion timestamptz,
    fecha_ultima_actualizacion_plan timestamptz,
    proxima_visita_programada timestamptz,
    estado_seguimiento_familia text DEFAULT 'ACTIVO',
    observaciones_adicionales_familia text,
    creado_en timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    creado_por uuid,
    actualizado_por uuid
);

-- ====================
-- TABLA 3: ATENCION_INTEGRAL_TRANSVERSAL_SALUD
-- ====================
CREATE TABLE atencion_integral_transversal_salud (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    codigo_atencion_integral_unico text UNIQUE NOT NULL,
    tipo_abordaje_atencion tipo_abordaje_atencion_integral_salud NOT NULL,
    modalidad_atencion modalidad_atencion_integral NOT NULL,
    nivel_complejidad_atencion nivel_complejidad_atencion_integral NOT NULL,
    sujeto_atencion_individual_id uuid,
    familia_integral_id uuid REFERENCES familia_integral_salud_publica(id),
    entorno_asociado_id uuid REFERENCES entornos_salud_publica(id),
    fecha_inicio_atencion_integral timestamptz NOT NULL,
    fecha_finalizacion_prevista timestamptz,
    fecha_finalizacion_real timestamptz,
    profesional_coordinador_id uuid,
    equipo_interdisciplinario_ids jsonb,
    objetivos_atencion_integral jsonb NOT NULL,
    plan_intervencion_detallado jsonb,
    actividades_realizadas_log jsonb,
    resultados_obtenidos_medicion jsonb,
    indicadores_proceso_seguimiento jsonb,
    barreras_dificultades_encontradas jsonb,
    facilitadores_recursos_utilizados jsonb,
    evaluacion_satisfaccion_usuario jsonb,
    recomendaciones_seguimiento jsonb,
    articulacion_otros_servicios jsonb,
    estado_atencion_integral text DEFAULT 'EN_PROCESO',
    fecha_ultima_evaluacion timestamptz,
    proxima_fecha_seguimiento timestamptz,
    observaciones_adicionales_atencion text,
    creado_en timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    creado_por uuid,
    actualizado_por uuid
);

-- ====================
-- FUNCIÓN PARA updated_at (SOLO SI NO EXISTE)
-- ====================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;   
END;
$$ language 'plpgsql';

-- ====================
-- CREAR TRIGGERS
-- ====================
DROP TRIGGER IF EXISTS update_entornos_salud_publica_updated_at ON entornos_salud_publica;
DROP TRIGGER IF EXISTS update_familia_integral_salud_publica_updated_at ON familia_integral_salud_publica;
DROP TRIGGER IF EXISTS update_atencion_integral_transversal_salud_updated_at ON atencion_integral_transversal_salud;

CREATE TRIGGER update_entornos_salud_publica_updated_at BEFORE UPDATE ON entornos_salud_publica FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_familia_integral_salud_publica_updated_at BEFORE UPDATE ON familia_integral_salud_publica FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_atencion_integral_transversal_salud_updated_at BEFORE UPDATE ON atencion_integral_transversal_salud FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- ====================
-- CREAR ÍNDICES PARA RENDIMIENTO
-- ====================
CREATE INDEX idx_entornos_tipo_entorno ON entornos_salud_publica(tipo_entorno);
CREATE INDEX idx_entornos_estado_activacion ON entornos_salud_publica(estado_activacion);
CREATE INDEX idx_entornos_departamento_municipio ON entornos_salud_publica(departamento_ubicacion, municipio_ubicacion);
CREATE INDEX idx_entornos_nivel_complejidad ON entornos_salud_publica(nivel_complejidad_intervencion);
CREATE INDEX idx_entornos_recursos_gin ON entornos_salud_publica USING gin(recursos_disponibles_entorno);

CREATE INDEX idx_familia_tipo_estructura ON familia_integral_salud_publica(tipo_estructura_familiar);
CREATE INDEX idx_familia_ciclo_vital ON familia_integral_salud_publica(ciclo_vital_familiar);
CREATE INDEX idx_familia_medico_asignado ON familia_integral_salud_publica(medico_familiar_asignado_id);
CREATE INDEX idx_familia_entorno ON familia_integral_salud_publica(entorno_salud_publica_id);
CREATE INDEX idx_familia_codigo_identificacion ON familia_integral_salud_publica(codigo_identificacion_familia_unico);
CREATE INDEX idx_familia_antecedentes_gin ON familia_integral_salud_publica USING gin(antecedentes_patologicos_familiares);

CREATE INDEX idx_atencion_integral_tipo_abordaje ON atencion_integral_transversal_salud(tipo_abordaje_atencion);
CREATE INDEX idx_atencion_integral_modalidad ON atencion_integral_transversal_salud(modalidad_atencion);
CREATE INDEX idx_atencion_integral_familia ON atencion_integral_transversal_salud(familia_integral_id);
CREATE INDEX idx_atencion_integral_entorno ON atencion_integral_transversal_salud(entorno_asociado_id);
CREATE INDEX idx_atencion_integral_fecha_inicio ON atencion_integral_transversal_salud(fecha_inicio_atencion_integral);
CREATE INDEX idx_atencion_integral_estado ON atencion_integral_transversal_salud(estado_atencion_integral);
CREATE INDEX idx_atencion_integral_sujeto ON atencion_integral_transversal_salud(sujeto_atencion_individual_id);
CREATE INDEX idx_atencion_integral_codigo ON atencion_integral_transversal_salud(codigo_atencion_integral_unico);
CREATE INDEX idx_atencion_integral_objetivos_gin ON atencion_integral_transversal_salud USING gin(objetivos_atencion_integral);

-- ====================
-- CONFIGURAR RLS INMEDIATAMENTE
-- ====================
ALTER TABLE entornos_salud_publica ENABLE ROW LEVEL SECURITY;
ALTER TABLE familia_integral_salud_publica ENABLE ROW LEVEL SECURITY;
ALTER TABLE atencion_integral_transversal_salud ENABLE ROW LEVEL SECURITY;

-- Crear políticas service_role
CREATE POLICY "service_role_full_access" ON entornos_salud_publica FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON familia_integral_salud_publica FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_full_access" ON atencion_integral_transversal_salud FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Conceder permisos
GRANT ALL ON TABLE entornos_salud_publica TO service_role;
GRANT ALL ON TABLE familia_integral_salud_publica TO service_role;
GRANT ALL ON TABLE atencion_integral_transversal_salud TO service_role;

-- ====================
-- INSERTAR DATOS DE PRUEBA
-- ====================
INSERT INTO entornos_salud_publica (
    codigo_identificacion_entorno_unico,
    tipo_entorno,
    nombre_descriptivo_entorno,
    descripcion_caracterizacion_entorno,
    departamento_ubicacion,
    municipio_ubicacion,
    zona_territorial
) VALUES 
(
    'ENT-FAM-001',
    'ENTORNO_FAMILIAR_HOGAR_DOMESTICO',
    'Entorno Familiar Piloto - Barrio Los Pinos',
    'Entorno familiar de caracterización para familias del barrio Los Pinos con enfoque en primera infancia y materno perinatal',
    'Valle del Cauca',
    'Cali',
    'urbana'
),
(
    'ENT-EDU-001',
    'ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL',
    'Entorno Educativo - IE Santa Helena',
    'Institución educativa con programas de salud escolar y promoción de hábitos saludables',
    'Valle del Cauca',
    'Cali',
    'urbana'
),
(
    'ENT-COM-001',
    'ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL',
    'Entorno Comunitario - Comuna 15',
    'Entorno comunitario territorial con enfoque en participación social y determinantes sociales de la salud',
    'Valle del Cauca',
    'Cali',
    'urbana'
) ON CONFLICT (codigo_identificacion_entorno_unico) DO NOTHING;

-- ====================
-- MENSAJE FINAL
-- ====================
DO $$ 
BEGIN 
    RAISE NOTICE '';
    RAISE NOTICE '===============================================';
    RAISE NOTICE 'TABLAS TRANSVERSALES CREADAS EXITOSAMENTE';
    RAISE NOTICE '===============================================';
    RAISE NOTICE 'Tablas creadas: entornos_salud_publica, familia_integral_salud_publica, atencion_integral_transversal_salud';
    RAISE NOTICE 'RLS: Habilitado con políticas service_role';
    RAISE NOTICE 'Índices: Creados para optimización de consultas';
    RAISE NOTICE 'Datos de prueba: Insertados para testing';
    RAISE NOTICE 'Status: Listo para uso con backend';
END $$;