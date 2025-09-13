-- =====================================================================================
-- Migración Consolidada: Modelos Transversales de Salud Pública
-- Fecha: 2025-01-13
-- Descripción: Implementa la arquitectura transversal según Resolución 3280 de 2018
-- Incluye: Entornos de Salud Pública, Familia Integral, Atención Integral Transversal
-- =====================================================================================

-- ========================
-- 1. ENTORNOS DE SALUD PÚBLICA
-- ========================

-- Enum para tipos de entorno de salud pública según Resolución 3280
CREATE TYPE tipo_entorno_salud_publica AS ENUM (
    'ENTORNO_FAMILIAR_HOGAR_DOMESTICO',
    'ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL', 
    'ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL',
    'ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO',
    'ENTORNO_INSTITUCIONAL_SERVICIOS_SALUD'
);

-- Enum para nivel de complejidad de intervención en entorno
CREATE TYPE nivel_complejidad_intervencion_entorno AS ENUM (
    'BASICO_PROMOCION_PREVENCION',
    'INTERMEDIO_INTERVENCION_TEMPRANA',
    'AVANZADO_MANEJO_ESPECIALIZADO',
    'INTEGRAL_COORDINACION_INTERSECTORIAL'
);

-- Enum para estado de activación del entorno
CREATE TYPE estado_activacion_entorno AS ENUM (
    'ACTIVO_OPERATIVO',
    'PARCIALMENTE_ACTIVO',
    'INACTIVO_TEMPORAL',
    'DESACTIVADO_DEFINITIVO'
);

-- Tabla principal de entornos de salud pública
CREATE TABLE entornos_salud_publica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_identificacion_entorno_unico TEXT NOT NULL,
    tipo_entorno tipo_entorno_salud_publica NOT NULL,
    nombre_descriptivo_entorno TEXT NOT NULL,
    descripcion_caracterizacion_entorno TEXT,
    nivel_complejidad_intervencion nivel_complejidad_intervencion_entorno DEFAULT 'BASICO_PROMOCION_PREVENCION',
    estado_activacion estado_activacion_entorno DEFAULT 'ACTIVO_OPERATIVO',
    
    -- Geolocalización y contexto territorial
    departamento_ubicacion TEXT,
    municipio_ubicacion TEXT,
    zona_territorial TEXT, -- urbana, rural, dispersa
    coordenadas_geograficas JSONB,
    
    -- Caracterización poblacional del entorno
    poblacion_objetivo_estimada INTEGER,
    rango_edad_poblacion_objetivo JSONB, -- {min_edad: number, max_edad: number}
    caracteristicas_demograficas_poblacion JSONB,
    
    -- Capacidades y recursos del entorno
    recursos_disponibles_entorno JSONB,
    actores_institucionales_involucrados JSONB,
    programas_servicios_disponibles JSONB,
    
    -- Intervenciones y actividades
    intervenciones_realizadas_historico JSONB,
    indicadores_resultado_entorno JSONB,
    plan_trabajo_entorno_vigente JSONB,
    
    -- Articulación intersectorial
    alianzas_estrategicas_activas JSONB,
    coordinacion_institucional_nivel TEXT,
    mecanismos_participacion_comunitaria JSONB,
    
    -- Monitoreo y evaluación
    fecha_ultima_caracterizacion TIMESTAMPTZ,
    proxima_fecha_evaluacion TIMESTAMPTZ,
    responsable_coordinacion_entorno TEXT,
    observaciones_adicionales_entorno TEXT,
    
    -- Auditoría
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    creado_por UUID,
    actualizado_por UUID
);

-- ========================
-- 2. FAMILIA INTEGRAL
-- ========================

-- Enum para tipo de estructura familiar
CREATE TYPE tipo_estructura_familiar_integral AS ENUM (
    'NUCLEAR_BIPARENTAL',
    'NUCLEAR_MONOPARENTAL_MATERNA',
    'NUCLEAR_MONOPARENTAL_PATERNA',
    'EXTENSA_BIPARENTAL',
    'EXTENSA_MONOPARENTAL',
    'COMPUESTA_MIXTA',
    'UNIPERSONAL_ADULTO',
    'RECONSTITUIDA_NUEVA_UNION',
    'HOMOPARENTAL_BIPARENTAL',
    'HOMOPARENTAL_MONOPARENTAL'
);

-- Enum para ciclo vital familiar
CREATE TYPE ciclo_vital_familiar AS ENUM (
    'FORMACION_PAREJA_SIN_HIJOS',
    'EXPANSION_HIJOS_PEQUENOS',
    'CONSOLIDACION_HIJOS_ESCOLARES',
    'APERTURA_HIJOS_ADOLESCENTES',
    'CONTRACCION_INDEPENDENCIA_HIJOS',
    'DISOLUCCION_NIDO_VACIO',
    'POST_PARENTAL_ADULTOS_MAYORES'
);

-- Enum para nivel socioeconómico familiar
CREATE TYPE nivel_socioeconomico_familiar AS ENUM (
    'ESTRATO_1_BAJO_BAJO',
    'ESTRATO_2_BAJO',
    'ESTRATO_3_MEDIO_BAJO',
    'ESTRATO_4_MEDIO',
    'ESTRATO_5_MEDIO_ALTO',
    'ESTRATO_6_ALTO'
);

-- Tabla principal de familia integral
CREATE TABLE familia_integral_salud_publica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_identificacion_familiar_unico TEXT NOT NULL UNIQUE,
    tipo_estructura_familiar tipo_estructura_familiar_integral NOT NULL,
    ciclo_vital_familiar ciclo_vital_familiar,
    nivel_socioeconomico_familiar nivel_socioeconomico_familiar,
    
    -- Composición familiar
    numero_total_integrantes INTEGER NOT NULL DEFAULT 1,
    numero_menores_18_anos INTEGER DEFAULT 0,
    numero_adultos_mayores_60_anos INTEGER DEFAULT 0,
    numero_personas_discapacidad INTEGER DEFAULT 0,
    numero_mujeres_edad_fertil INTEGER DEFAULT 0,
    
    -- Información socioeconómica
    ingreso_familiar_mensual_estimado DECIMAL(12,2),
    tipo_vivienda TEXT,
    tenencia_vivienda TEXT, -- propia, arrendada, familiar, otro
    servicios_publicos_disponibles JSONB,
    acceso_tecnologias_informacion JSONB,
    
    -- Evaluación funcionalidad familiar (APGAR Familiar)
    puntaje_apgar_familiar_funcionamiento INTEGER, -- 0-20
    fecha_aplicacion_apgar_familiar TIMESTAMPTZ,
    interpretacion_apgar_familiar TEXT, -- funcional, disfuncional leve, moderada, severa
    
    -- Dinámicas familiares
    patron_comunicacion_familiar TEXT,
    mecanismos_resolucion_conflictos TEXT,
    distribucion_roles_responsabilidades JSONB,
    tiempo_calidad_familiar_semanal INTEGER, -- horas
    
    -- Red de apoyo familiar (Ecomapa)
    red_apoyo_familiar_primaria JSONB,
    red_apoyo_institucional JSONB,
    red_apoyo_comunitaria JSONB,
    fortaleza_vinculos_red_apoyo TEXT, -- fuerte, moderada, débil
    
    -- Antecedentes y factores de riesgo
    antecedentes_familiares_relevantes JSONB,
    factores_riesgo_psicosocial JSONB,
    factores_protectores_identificados JSONB,
    eventos_vitales_estresantes_recientes JSONB,
    
    -- Atención en salud familiar
    ips_asignada_familia TEXT,
    medico_familia_asignado UUID,
    fecha_ultima_atencion_familiar TIMESTAMPTZ,
    plan_atencion_familiar_vigente JSONB,
    
    -- Participación comunitaria
    participacion_organizaciones_comunitarias BOOLEAN DEFAULT FALSE,
    liderazgo_comunitario_familiar BOOLEAN DEFAULT FALSE,
    actividades_promocion_salud_participacion JSONB,
    
    -- Seguimiento y monitoreo
    fecha_caracterizacion_inicial TIMESTAMPTZ DEFAULT NOW(),
    fecha_proxima_evaluacion TIMESTAMPTZ,
    responsable_seguimiento_familiar UUID,
    estado_seguimiento_familiar TEXT DEFAULT 'ACTIVO',
    observaciones_adicionales_familia TEXT,
    
    -- Auditoría
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    creado_por UUID,
    actualizado_por UUID
);

-- ========================
-- 3. ATENCIÓN INTEGRAL TRANSVERSAL
-- ========================

-- Enum para tipo de abordaje de atención integral
CREATE TYPE tipo_abordaje_atencion_integral_salud AS ENUM (
    'PROMOCION_SALUD_POBLACIONAL',
    'PREVENCION_PRIMARIA_INDIVIDUAL',
    'PREVENCION_SECUNDARIA_TAMIZAJE',
    'INTERVENCION_TEMPRANA_RIESGO',
    'MANEJO_INTEGRAL_ENFERMEDAD',
    'REHABILITACION_FUNCIONAL',
    'CUIDADOS_PALIATIVOS_CRONICOS',
    'ATENCION_URGENCIAS_EMERGENCIAS'
);

-- Enum para nivel de complejidad atención integral
CREATE TYPE nivel_complejidad_atencion_integral AS ENUM (
    'BAJA_ATENCION_PRIMARIA',
    'MEDIA_ATENCION_ESPECIALIZADA',
    'ALTA_ATENCION_SUBESPECIALIZADA',
    'MAXIMA_ATENCION_CRITICA'
);

-- Enum para modalidad de atención integral
CREATE TYPE modalidad_atencion_integral AS ENUM (
    'PRESENCIAL_INSTITUCIONAL',
    'DOMICILIARIA_TERRITORIO',
    'TELEATENCION_VIRTUAL',
    'MIXTA_HIBRIDA',
    'ITINERANTE_MOVIL',
    'COMUNITARIA_COLECTIVA'
);

-- Tabla principal de atención integral transversal
CREATE TABLE atencion_integral_transversal_salud (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_atencion_integral_unico TEXT NOT NULL UNIQUE,
    tipo_abordaje_atencion_integral tipo_abordaje_atencion_integral_salud NOT NULL,
    nivel_complejidad_atencion nivel_complejidad_atencion_integral DEFAULT 'BAJA_ATENCION_PRIMARIA',
    modalidad_atencion modalidad_atencion_integral DEFAULT 'PRESENCIAL_INSTITUCIONAL',
    
    -- Sujeto de atención (puede ser individual, familiar o poblacional)
    sujeto_atencion TEXT NOT NULL, -- 'INDIVIDUAL', 'FAMILIAR', 'POBLACIONAL', 'COMUNITARIO'
    identificacion_sujeto_atencion TEXT, -- ID del paciente, familia o población
    
    -- Contexto de la atención integral
    entornos_salud_publica_involucrados UUID[], -- Array de IDs de entornos
    familia_beneficiaria_id UUID,
    
    -- Caracterización de la atención
    motivo_atencion_integral TEXT NOT NULL,
    objetivos_atencion_integral JSONB,
    intervenciones_programadas JSONB,
    resultados_esperados JSONB,
    
    -- Equipo de atención integral
    profesional_coordinador_atencion UUID,
    equipo_interdisciplinario_ids UUID[],
    especialidades_involucradas JSONB,
    
    -- Temporalidad y seguimiento
    fecha_inicio_atencion_integral TIMESTAMPTZ DEFAULT NOW(),
    fecha_finalizacion_programada TIMESTAMPTZ,
    fecha_finalizacion_real TIMESTAMPTZ,
    duracion_estimada_dias INTEGER,
    frecuencia_seguimiento TEXT,
    
    -- Recursos y tecnologías
    recursos_tecnicos_utilizados JSONB,
    tecnologias_informacion_salud JSONB,
    dispositivos_medicos_requeridos JSONB,
    medicamentos_dispositivos_suministrados JSONB,
    
    -- Coordinación intersectorial
    instituciones_participantes JSONB,
    sectores_involucrados JSONB, -- salud, educación, protección social, etc.
    mecanismos_coordinacion JSONB,
    
    -- Indicadores y resultados
    indicadores_proceso_atencion JSONB,
    indicadores_resultado_atencion JSONB,
    indicadores_impacto_poblacional JSONB,
    nivel_satisfaccion_usuario DECIMAL(3,2), -- 0.00 a 10.00
    
    -- Continuidad de la atención
    atencion_previa_relacionada UUID,
    atencion_posterior_programada UUID,
    referencia_contrarreferencia JSONB,
    
    -- Documentación y evidencia
    documentos_soporte_atencion JSONB,
    evidencia_cientifica_utilizada JSONB,
    guias_protocolos_aplicados JSONB,
    
    -- Estado y seguimiento
    estado_atencion_integral TEXT DEFAULT 'PROGRAMADA', -- PROGRAMADA, EN_CURSO, COMPLETADA, SUSPENDIDA, CANCELADA
    porcentaje_cumplimiento_objetivos DECIMAL(5,2), -- 0.00 a 100.00
    observaciones_seguimiento TEXT,
    
    -- Auditoría
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    creado_por UUID,
    actualizado_por UUID
);

-- ========================
-- 4. VISTA CONSOLIDADA TRANSVERSAL
-- ========================

-- Vista para análisis transversal integrado
CREATE VIEW vista_analisis_transversal_integral AS
SELECT 
    ait.id as atencion_id,
    ait.codigo_atencion_integral_unico,
    ait.tipo_abordaje_atencion_integral,
    ait.sujeto_atencion,
    
    -- Información de entornos involucrados
    esp.tipo_entorno,
    esp.nombre_descriptivo_entorno,
    esp.nivel_complejidad_intervencion,
    esp.departamento_ubicacion,
    esp.municipio_ubicacion,
    
    -- Información familiar si aplica
    fisp.codigo_identificacion_familiar_unico,
    fisp.tipo_estructura_familiar,
    fisp.ciclo_vital_familiar,
    fisp.numero_total_integrantes,
    fisp.puntaje_apgar_familiar_funcionamiento,
    
    -- Indicadores de resultado
    ait.nivel_satisfaccion_usuario,
    ait.porcentaje_cumplimiento_objetivos,
    ait.estado_atencion_integral,
    
    -- Fechas relevantes
    ait.fecha_inicio_atencion_integral,
    ait.fecha_finalizacion_real,
    ait.creado_en
    
FROM atencion_integral_transversal_salud ait
LEFT JOIN familia_integral_salud_publica fisp ON ait.familia_beneficiaria_id = fisp.id
LEFT JOIN entornos_salud_publica esp ON esp.id = ANY(ait.entornos_salud_publica_involucrados);

-- ========================
-- 5. ÍNDICES PARA RENDIMIENTO
-- ========================

-- Índices para entornos de salud pública
CREATE INDEX idx_entornos_tipo_entorno ON entornos_salud_publica(tipo_entorno);
CREATE INDEX idx_entornos_departamento_municipio ON entornos_salud_publica(departamento_ubicacion, municipio_ubicacion);
CREATE INDEX idx_entornos_estado_activacion ON entornos_salud_publica(estado_activacion);
CREATE INDEX idx_entornos_nivel_complejidad ON entornos_salud_publica(nivel_complejidad_intervencion);

-- Índices para familia integral
CREATE INDEX idx_familia_codigo_identificacion ON familia_integral_salud_publica(codigo_identificacion_familiar_unico);
CREATE INDEX idx_familia_tipo_estructura ON familia_integral_salud_publica(tipo_estructura_familiar);
CREATE INDEX idx_familia_ciclo_vital ON familia_integral_salud_publica(ciclo_vital_familiar);
CREATE INDEX idx_familia_medico_asignado ON familia_integral_salud_publica(medico_familia_asignado);

-- Índices para atención integral transversal
CREATE INDEX idx_atencion_integral_codigo ON atencion_integral_transversal_salud(codigo_atencion_integral_unico);
CREATE INDEX idx_atencion_integral_tipo_abordaje ON atencion_integral_transversal_salud(tipo_abordaje_atencion_integral);
CREATE INDEX idx_atencion_integral_sujeto ON atencion_integral_transversal_salud(sujeto_atencion);
CREATE INDEX idx_atencion_integral_familia ON atencion_integral_transversal_salud(familia_beneficiaria_id);
CREATE INDEX idx_atencion_integral_estado ON atencion_integral_transversal_salud(estado_atencion_integral);
CREATE INDEX idx_atencion_integral_fecha_inicio ON atencion_integral_transversal_salud(fecha_inicio_atencion_integral);

-- Índices GIN para campos JSONB
CREATE INDEX idx_entornos_recursos_gin ON entornos_salud_publica USING GIN (recursos_disponibles_entorno);
CREATE INDEX idx_familia_antecedentes_gin ON familia_integral_salud_publica USING GIN (antecedentes_familiares_relevantes);
CREATE INDEX idx_atencion_integral_objetivos_gin ON atencion_integral_transversal_salud USING GIN (objetivos_atencion_integral);

-- ========================
-- 6. TRIGGERS PARA AUDITORÍA
-- ========================

-- Trigger para updated_at en entornos_salud_publica
CREATE TRIGGER handle_updated_at BEFORE UPDATE ON entornos_salud_publica 
FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

-- Trigger para updated_at en familia_integral_salud_publica
CREATE TRIGGER handle_updated_at BEFORE UPDATE ON familia_integral_salud_publica 
FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

-- Trigger para updated_at en atencion_integral_transversal_salud
CREATE TRIGGER handle_updated_at BEFORE UPDATE ON atencion_integral_transversal_salud 
FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

-- ========================
-- 7. ROW LEVEL SECURITY (RLS)
-- ========================

-- Habilitar RLS en todas las tablas transversales
ALTER TABLE entornos_salud_publica ENABLE ROW LEVEL SECURITY;
ALTER TABLE familia_integral_salud_publica ENABLE ROW LEVEL SECURITY;
ALTER TABLE atencion_integral_transversal_salud ENABLE ROW LEVEL SECURITY;

-- Políticas básicas para desarrollo (serán refinadas en producción)
CREATE POLICY "Allow full access for service role on entornos" ON entornos_salud_publica
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Allow full access for service role on familia" ON familia_integral_salud_publica
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Allow full access for service role on atencion_integral" ON atencion_integral_transversal_salud
FOR ALL USING (auth.role() = 'service_role');

-- Políticas para usuarios autenticados (acceso básico)
CREATE POLICY "Allow read access for authenticated users on entornos" ON entornos_salud_publica
FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Allow read access for authenticated users on familia" ON familia_integral_salud_publica
FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Allow read access for authenticated users on atencion_integral" ON atencion_integral_transversal_salud
FOR SELECT USING (auth.role() = 'authenticated');

-- ========================
-- 8. COMENTARIOS DESCRIPTIVOS
-- ========================

-- Comentarios en tablas principales
COMMENT ON TABLE entornos_salud_publica IS 'Tabla transversal que registra y caracteriza los 5 entornos de salud pública según Resolución 3280: familiar, educativo, comunitario, laboral e institucional. Permite la gestión integral de intervenciones en cada entorno.';

COMMENT ON TABLE familia_integral_salud_publica IS 'Tabla que gestiona a la familia como sujeto de atención integral en salud pública. Incluye caracterización familiar, funcionalidad (APGAR), dinámicas y redes de apoyo según lineamientos normativos.';

COMMENT ON TABLE atencion_integral_transversal_salud IS 'Tabla central de la arquitectura transversal que coordina atenciones integrales que involucran múltiples entornos, familias y niveles de complejidad. Implementa el enfoque transversal de la Resolución 3280.';

-- Comentarios en campos clave
COMMENT ON COLUMN entornos_salud_publica.tipo_entorno IS 'Tipo de entorno según clasificación normativa Resolución 3280: familiar, educativo, comunitario, laboral, institucional';

COMMENT ON COLUMN familia_integral_salud_publica.puntaje_apgar_familiar_funcionamiento IS 'Puntaje APGAR familiar (0-20): 0-10 disfuncional, 11-13 moderadamente funcional, 14-17 funcional, 18-20 altamente funcional';

COMMENT ON COLUMN atencion_integral_transversal_salud.entornos_salud_publica_involucrados IS 'Array de UUIDs de entornos de salud pública que participan en esta atención integral transversal';

-- ========================
-- 9. DATOS SEMILLA (OPCIONAL)
-- ========================

-- Insertar algunos entornos de ejemplo para testing
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
);

-- ========================
-- MIGRACIÓN COMPLETADA
-- ========================

-- Log de finalización
DO $$ 
BEGIN 
    RAISE NOTICE 'Migración transversal completada exitosamente. Tablas creadas: entornos_salud_publica, familia_integral_salud_publica, atencion_integral_transversal_salud';
    RAISE NOTICE 'Vista consolidada creada: vista_analisis_transversal_integral';
    RAISE NOTICE 'Índices, triggers y políticas RLS aplicados';
    RAISE NOTICE 'Datos semilla insertados para testing inicial';
END $$;