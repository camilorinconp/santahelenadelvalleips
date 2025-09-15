-- =============================================================================
-- MIGRACIÓN MAESTRA DE CONSOLIDACIÓN - ARQUITECTURA VERTICAL
-- Consolida 38 migraciones previas en estructura limpia y funcional
-- Fecha: 15 septiembre 2025
-- Objetivo: Base sólida para desarrollo vertical de RIAS
-- =============================================================================

-- NOTA: Esta migración asume que las tablas base ya existen
-- Se enfoca en limpiar y consolidar funcionalidad existente

BEGIN;

-- =============================================================================
-- 1. TABLAS CORE (Pacientes, Médicos, Atenciones Base)
-- =============================================================================

-- Verificar y consolidar tabla pacientes
DO $$
BEGIN
    -- Agregar campos faltantes si no existen
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'pacientes' AND column_name = 'ocupacion_id') THEN
        ALTER TABLE pacientes ADD COLUMN ocupacion_id VARCHAR(10) REFERENCES catalogo_ocupaciones_dane(codigo_ocupacion_dane);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'pacientes' AND column_name = 'nivel_educativo') THEN
        ALTER TABLE pacientes ADD COLUMN nivel_educativo VARCHAR(100);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'pacientes' AND column_name = 'pertenencia_etnica') THEN
        ALTER TABLE pacientes ADD COLUMN pertenencia_etnica VARCHAR(100);
    END IF;
END $$;

-- =============================================================================
-- 2. CONSOLIDAR ATENCION_PRIMERA_INFANCIA - VERSIÓN BÁSICA UNIFICADA
-- =============================================================================

-- Limpiar tabla Primera Infancia y mantener solo campos esenciales
DO $$
BEGIN
    -- Verificar si la tabla existe
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'atencion_primera_infancia') THEN
        
        -- Remover columnas complejas del sistema expandido si existen
        -- Sistema de alertas
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'alertas_desarrollo_generadas') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN alertas_desarrollo_generadas;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'nivel_riesgo_desarrollo') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN nivel_riesgo_desarrollo;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'requiere_intervencion_temprana') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN requiere_intervencion_temprana;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'especialidades_referencia_requeridas') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN especialidades_referencia_requeridas;
        END IF;
        
        -- Campos EAD-3 complejos (mantener solo básicos)
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'ead3_motricidad_gruesa_items_logrados') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN ead3_motricidad_gruesa_items_logrados;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'ead3_motricidad_fina_items_logrados') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN ead3_motricidad_fina_items_logrados;
        END IF;
        
        -- Campos validaciones complejas
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'fecha_ultima_generacion_alertas') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN fecha_ultima_generacion_alertas;
        END IF;
        
        -- Campos ASQ-3 detallados (mantener solo básicos)
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'atencion_primera_infancia' AND column_name = 'asq3_formulario_aplicado') THEN
            ALTER TABLE atencion_primera_infancia DROP COLUMN asq3_formulario_aplicado;
        END IF;
        
    ELSE
        -- Crear tabla Primera Infancia básica si no existe
        CREATE TABLE atencion_primera_infancia (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            paciente_id UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
            medico_id UUID REFERENCES medicos(id),
            atencion_id UUID REFERENCES atenciones(id) ON DELETE CASCADE,
            fecha_atencion DATE NOT NULL DEFAULT CURRENT_DATE,
            entorno VARCHAR(100),
            
            -- Código único de atención
            codigo_atencion_primera_infancia_unico VARCHAR(100) UNIQUE,
            
            -- Datos antropométricos básicos
            peso_kg DECIMAL(5,2),
            talla_cm DECIMAL(5,2),
            perimetro_cefalico_cm DECIMAL(5,2),
            
            -- Estado nutricional básico
            estado_nutricional VARCHAR(50),
            
            -- Desarrollo básico (EAD-3 simplificado)
            ead3_aplicada BOOLEAN DEFAULT FALSE,
            ead3_motricidad_gruesa_puntaje INTEGER CHECK (ead3_motricidad_gruesa_puntaje >= 0 AND ead3_motricidad_gruesa_puntaje <= 100),
            ead3_motricidad_fina_puntaje INTEGER CHECK (ead3_motricidad_fina_puntaje >= 0 AND ead3_motricidad_fina_puntaje <= 100),
            ead3_audicion_lenguaje_puntaje INTEGER CHECK (ead3_audicion_lenguaje_puntaje >= 0 AND ead3_audicion_lenguaje_puntaje <= 100),
            ead3_personal_social_puntaje INTEGER CHECK (ead3_personal_social_puntaje >= 0 AND ead3_personal_social_puntaje <= 100),
            ead3_puntaje_total INTEGER,
            fecha_aplicacion_ead3 DATE,
            
            -- Tamizaje ASQ-3 básico
            asq3_aplicado BOOLEAN DEFAULT FALSE,
            asq3_comunicacion_puntaje INTEGER,
            asq3_motor_grueso_puntaje INTEGER,
            asq3_motor_fino_puntaje INTEGER,
            asq3_resolucion_problemas_puntaje INTEGER,
            asq3_personal_social_puntaje INTEGER,
            fecha_aplicacion_asq3 DATE,
            
            -- Vacunación básica
            esquema_vacunacion_completo BOOLEAN DEFAULT FALSE,
            bcg_aplicada BOOLEAN DEFAULT FALSE,
            hepatitis_b_rn_aplicada BOOLEAN DEFAULT FALSE,
            pentavalente_dosis_completas INTEGER DEFAULT 0,
            srp_aplicada BOOLEAN DEFAULT FALSE,
            
            -- Tamizajes básicos
            tamizaje_visual_realizado BOOLEAN DEFAULT FALSE,
            tamizaje_visual_resultado VARCHAR(100),
            tamizaje_auditivo_realizado BOOLEAN DEFAULT FALSE,
            tamizaje_auditivo_resultado VARCHAR(100),
            
            -- Salud oral básica
            salud_oral_estado VARCHAR(50),
            salud_oral_observaciones TEXT,
            
            -- Observaciones profesionales
            observaciones_profesional_primera_infancia TEXT,
            recomendaciones_generales TEXT,
            
            -- Metadatos
            creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    END IF;
END $$;

-- =============================================================================
-- 3. CONSOLIDAR MATERNO PERINATAL (Mantener funcional)
-- =============================================================================

-- Verificar que atencion_materno_perinatal esté funcional
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'atencion_materno_perinatal') THEN
        -- Agregar campos básicos si faltan
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'atencion_materno_perinatal' AND column_name = 'fecha_atencion') THEN
            ALTER TABLE atencion_materno_perinatal ADD COLUMN fecha_atencion DATE DEFAULT CURRENT_DATE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'atencion_materno_perinatal' AND column_name = 'entorno') THEN
            ALTER TABLE atencion_materno_perinatal ADD COLUMN entorno VARCHAR(100);
        END IF;
    END IF;
END $$;

-- =============================================================================
-- 4. PREPARAR CONTROL CRONICIDAD (Próxima RIAS vertical)
-- =============================================================================

-- Verificar tabla control_cronicidad está lista para desarrollo
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'control_cronicidad') THEN
        -- Agregar campos básicos para desarrollo futuro
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'control_cronicidad' AND column_name = 'fecha_atencion') THEN
            ALTER TABLE control_cronicidad ADD COLUMN fecha_atencion DATE DEFAULT CURRENT_DATE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name = 'control_cronicidad' AND column_name = 'entorno') THEN
            ALTER TABLE control_cronicidad ADD COLUMN entorno VARCHAR(100);
        END IF;
    END IF;
END $$;

-- =============================================================================
-- 5. LIMPIAR ENUMS INNECESARIOS Y CREAR LOS BÁSICOS
-- =============================================================================

-- Remover ENUMs complejos del sistema expandido si existen
DO $$
BEGIN
    -- Sistema alertas (remover)
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_alerta') THEN
        DROP TYPE IF EXISTS tipo_alerta CASCADE;
    END IF;
    
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'prioridad_alerta') THEN
        DROP TYPE IF EXISTS prioridad_alerta CASCADE;
    END IF;
    
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_alerta') THEN
        DROP TYPE IF EXISTS estado_alerta CASCADE;
    END IF;
    
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'resultado_area_desarrollo') THEN
        DROP TYPE IF EXISTS resultado_area_desarrollo CASCADE;
    END IF;
    
    -- Crear ENUMs básicos necesarios
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_nutricional_enum') THEN
        CREATE TYPE estado_nutricional_enum AS ENUM (
            'NORMAL',
            'DESNUTRICION_AGUDA',
            'DESNUTRICION_CRONICA', 
            'SOBREPESO',
            'OBESIDAD'
        );
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'resultado_tamizaje_enum') THEN
        CREATE TYPE resultado_tamizaje_enum AS ENUM (
            'NORMAL',
            'ALTERADO',
            'NO_REALIZADO'
        );
    END IF;
END $$;

-- =============================================================================
-- 6. ÍNDICES BÁSICOS PARA PERFORMANCE
-- =============================================================================

-- Índices Primera Infancia
CREATE INDEX IF NOT EXISTS idx_atencion_primera_infancia_paciente_id 
ON atencion_primera_infancia(paciente_id);

CREATE INDEX IF NOT EXISTS idx_atencion_primera_infancia_fecha 
ON atencion_primera_infancia(fecha_atencion);

CREATE INDEX IF NOT EXISTS idx_atencion_primera_infancia_codigo_unico 
ON atencion_primera_infancia(codigo_atencion_primera_infancia_unico);

-- Índices Materno Perinatal
CREATE INDEX IF NOT EXISTS idx_atencion_materno_perinatal_paciente_id 
ON atencion_materno_perinatal(paciente_id);

CREATE INDEX IF NOT EXISTS idx_atencion_materno_perinatal_fecha 
ON atencion_materno_perinatal(fecha_atencion);

-- =============================================================================
-- 7. REMOVER TRIGGERS Y FUNCIONES COMPLEJAS DEL SISTEMA EXPANDIDO
-- =============================================================================

-- Remover trigger de alertas automáticas (sistema expandido)
DROP TRIGGER IF EXISTS trigger_alertas_primera_infancia ON atencion_primera_infancia;
DROP FUNCTION IF EXISTS trigger_generar_alertas_primera_infancia();

-- Remover otras funciones complejas si existen
DROP FUNCTION IF EXISTS calcular_alertas_desarrollo(UUID);
DROP FUNCTION IF EXISTS evaluar_riesgo_nutricional(UUID);
DROP FUNCTION IF EXISTS generar_alertas_vacunacion(UUID);

-- =============================================================================
-- 8. TRIGGERS BÁSICOS PARA TIMESTAMP
-- =============================================================================

-- Trigger para actualizar timestamp en Primera Infancia
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_atencion_primera_infancia_updated_at ON atencion_primera_infancia;
CREATE TRIGGER update_atencion_primera_infancia_updated_at
    BEFORE UPDATE ON atencion_primera_infancia
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- 9. RLS POLICIES BÁSICAS (DESARROLLO)
-- =============================================================================

-- Habilitar RLS en tablas principales
ALTER TABLE atencion_primera_infancia ENABLE ROW LEVEL SECURITY;

-- Policy desarrollo - acceso completo
DROP POLICY IF EXISTS "desarrollo_full_access_primera_infancia" ON atencion_primera_infancia;
CREATE POLICY "desarrollo_full_access_primera_infancia" ON atencion_primera_infancia
    FOR ALL USING (true) WITH CHECK (true);

-- =============================================================================
-- 10. LIMPIEZA Y COMENTARIOS
-- =============================================================================

-- Comentarios en tablas principales
COMMENT ON TABLE atencion_primera_infancia IS 'Atención Primera Infancia básica según Resolución 3280 - Versión consolidada vertical';
COMMENT ON COLUMN atencion_primera_infancia.ead3_aplicada IS 'Indica si se aplicó Escala Abreviada de Desarrollo (EAD-3)';
COMMENT ON COLUMN atencion_primera_infancia.asq3_aplicado IS 'Indica si se aplicó Ages and Stages Questionnaire (ASQ-3)';
COMMENT ON COLUMN atencion_primera_infancia.esquema_vacunacion_completo IS 'Estado general del esquema de vacunación';
COMMENT ON COLUMN atencion_primera_infancia.updated_at IS 'Fecha y hora de última actualización del registro';

-- Mensaje de finalización
DO $$
BEGIN
    RAISE NOTICE '=== MIGRACIÓN MAESTRA CONSOLIDADA COMPLETADA ===';
    RAISE NOTICE 'Estado: Arquitectura vertical consolidada';
    RAISE NOTICE 'Primera Infancia: Versión básica unificada funcional';
    RAISE NOTICE 'Materno Perinatal: Mantenido funcional';
    RAISE NOTICE 'Preparado para: Control Cronicidad (próxima RIAS)';
    RAISE NOTICE 'Sistema de alertas complejas: REMOVIDO';
    RAISE NOTICE 'Base de datos: LIMPIA y lista para desarrollo vertical';
END $$;

COMMIT;