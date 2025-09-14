-- =============================================
-- TEMPLATE: CREAR NUEVA TABLA
-- =============================================
-- Descripción: Template reutilizable para crear tablas siguiendo
--              convenciones del proyecto IPS Santa Helena del Valle
-- Fecha: [DD mes AAAA]
-- Autor: [Tu nombre]
-- Contexto: [Explicar por qué se necesita esta tabla]
-- =============================================

BEGIN;

-- =============================================
-- 1. VERIFICACIONES PRE-EJECUCIÓN
-- =============================================
DO $pre_check$
DECLARE
    table_exists BOOLEAN;
BEGIN
    -- Verificar que la tabla no existe ya
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = '[NOMBRE_TABLA]'
    ) INTO table_exists;
    
    IF table_exists THEN
        RAISE NOTICE 'ℹ️  Tabla [NOMBRE_TABLA] ya existe, saltando creación';
    ELSE
        RAISE NOTICE '🏗️  Creando nueva tabla: [NOMBRE_TABLA]';
    END IF;
END;
$pre_check$;

-- =============================================
-- 2. CREAR TABLA PRINCIPAL
-- =============================================

CREATE TABLE IF NOT EXISTS [NOMBRE_TABLA] (
    -- ================================
    -- CAMPOS IDENTIFICACIÓN
    -- ================================
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- ================================  
    -- CAMPOS BUSINESS LOGIC
    -- ================================
    -- [Agregar campos específicos del negocio]
    campo_requerido_text TEXT NOT NULL,
    campo_opcional_text TEXT,
    campo_numerico INTEGER,
    campo_decimal DECIMAL(10,2),
    campo_booleano BOOLEAN DEFAULT FALSE,
    campo_fecha DATE,
    campo_timestamp TIMESTAMPTZ,
    
    -- ================================
    -- CAMPOS ENUM (usar para valores fijos pequeños)
    -- ================================
    -- Ejemplo: estado_registro estado_tabla_enum DEFAULT 'activo',
    
    -- ================================
    -- CAMPOS FOREIGN KEYS
    -- ================================
    -- Ejemplo: paciente_id UUID REFERENCES pacientes(id) ON DELETE CASCADE,
    -- Ejemplo: medico_id UUID REFERENCES medicos(id) ON DELETE SET NULL,
    
    -- ================================
    -- CAMPOS JSONB (datos semi-estructurados)
    -- ================================
    metadatos_adicionales JSONB DEFAULT '{}',
    configuracion_especifica JSONB,
    
    -- ================================
    -- CAMPOS AUDITORÍA (OBLIGATORIOS)
    -- ================================
    creado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    actualizado_en TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    creado_por UUID, -- FK a usuarios cuando esté implementado
    actualizado_por UUID,
    
    -- ================================
    -- CONSTRAINTS BUSINESS LOGIC
    -- ================================
    CONSTRAINT check_campo_requerido_no_vacio 
        CHECK (campo_requerido_text != ''),
    
    CONSTRAINT check_campo_numerico_positivo 
        CHECK (campo_numerico > 0),
        
    CONSTRAINT check_fecha_logica 
        CHECK (campo_fecha <= CURRENT_DATE),
        
    -- Constraint para JSONB structure validation (ejemplo)
    CONSTRAINT check_metadatos_structure 
        CHECK (jsonb_typeof(metadatos_adicionales) = 'object')
);

-- =============================================
-- 3. CREAR ENUM SI ES NECESARIO
-- =============================================
-- Solo si necesitas valores fijos pequeños

-- CREATE TYPE IF NOT EXISTS estado_tabla_enum AS ENUM (
--     'activo',
--     'inactivo', 
--     'pendiente',
--     'cancelado'
-- );

-- =============================================
-- 4. ÍNDICES PARA PERFORMANCE
-- =============================================

-- Índice para búsquedas por campo principal
CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_campo_principal
ON [NOMBRE_TABLA](campo_requerido_text)
WHERE campo_requerido_text IS NOT NULL;

-- Índice para foreign keys (crítico para performance)
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_paciente_id
-- ON [NOMBRE_TABLA](paciente_id);

-- Índice compuesto para queries frecuentes
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_lookup
-- ON [NOMBRE_TABLA](campo_requerido_text, campo_fecha)
-- WHERE campo_booleano = TRUE;

-- Índice parcial para registros activos (común pattern)
CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_activos
ON [NOMBRE_TABLA](creado_en, actualizado_en)
WHERE campo_booleano = TRUE;

-- Índice GIN para búsquedas en JSONB
CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_metadatos
ON [NOMBRE_TABLA] USING GIN (metadatos_adicionales);

-- =============================================
-- 5. DATOS INICIALES / SEED DATA
-- =============================================
-- Insertar datos críticos que la aplicación necesita

INSERT INTO [NOMBRE_TABLA] (
    campo_requerido_text, 
    campo_opcional_text,
    metadatos_adicionales
) VALUES
('valor_inicial_1', 'descripción 1', '{"tipo": "inicial", "version": "1.0"}'),
('valor_inicial_2', 'descripción 2', '{"tipo": "inicial", "version": "1.0"}')
ON CONFLICT (campo_requerido_text) DO UPDATE SET
    campo_opcional_text = EXCLUDED.campo_opcional_text,
    metadatos_adicionales = EXCLUDED.metadatos_adicionales,
    actualizado_en = NOW();

-- =============================================
-- 6. ROW LEVEL SECURITY (OBLIGATORIO)
-- =============================================

-- Habilitar RLS en la tabla
ALTER TABLE [NOMBRE_TABLA] ENABLE ROW LEVEL SECURITY;

-- Policy para service_role (backend FastAPI) - ACCESO COMPLETO
CREATE POLICY "service_role_full_access_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR ALL 
USING (auth.role() = 'service_role')
WITH CHECK (auth.role() = 'service_role');

-- Policy para authenticated users - SOLO LECTURA de registros activos
CREATE POLICY "authenticated_read_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR SELECT 
USING (auth.role() = 'authenticated' AND campo_booleano = TRUE);

-- Policy adicional para INSERT/UPDATE si usuarios autenticados necesitan
-- CREATE POLICY "authenticated_insert_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR INSERT
-- WITH CHECK (auth.role() = 'authenticated');

-- Policy para anon users - SOLO LECTURA muy limitada
-- CREATE POLICY "anon_read_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]  
-- FOR SELECT
-- USING (auth.role() = 'anon' AND campo_booleano = TRUE);

-- =============================================
-- 7. TRIGGERS PARA AUDITORÍA
-- =============================================

-- Trigger para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION trigger_actualizar_timestamp_[NOMBRE_TABLA]()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    -- Agregar actualizado_por cuando usuarios esté implementado
    -- NEW.actualizado_por = auth.uid();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger
CREATE TRIGGER trigger_[NOMBRE_TABLA]_timestamp
    BEFORE UPDATE ON [NOMBRE_TABLA]
    FOR EACH ROW EXECUTE FUNCTION trigger_actualizar_timestamp_[NOMBRE_TABLA]();

-- =============================================
-- 8. COMENTARIOS DOCUMENTACIÓN
-- =============================================

COMMENT ON TABLE [NOMBRE_TABLA] IS 
'[Descripción completa del propósito de la tabla, qué datos almacena, 
cómo se relaciona con otras tablas del sistema, y contexto business]';

COMMENT ON COLUMN [NOMBRE_TABLA].id IS 
'UUID identificador único de la tabla, generado automáticamente';

COMMENT ON COLUMN [NOMBRE_TABLA].campo_requerido_text IS 
'[Descripción específica del campo, valores válidos, constraints aplicables]';

COMMENT ON COLUMN [NOMBRE_TABLA].metadatos_adicionales IS 
'JSONB para datos semi-estructurados específicos del contexto. 
Estructura esperada: {"tipo": string, "version": string, "configuracion": object}';

COMMENT ON COLUMN [NOMBRE_TABLA].creado_en IS 
'Timestamp de creación del registro, se asigna automáticamente';

COMMENT ON COLUMN [NOMBRE_TABLA].actualizado_en IS 
'Timestamp de última actualización, se actualiza automáticamente via trigger';

-- =============================================
-- 9. GRANTS ADICIONALES SI ES NECESARIO
-- =============================================

-- Grant explícitos para service_role (ya cubierto por RLS pero por claridad)
GRANT ALL ON [NOMBRE_TABLA] TO service_role;
GRANT ALL ON [NOMBRE_TABLA] TO postgres;

-- Grant para authenticated si necesitan acceso directo
GRANT SELECT ON [NOMBRE_TABLA] TO authenticated;

-- =============================================
-- 10. VERIFICACIONES POST-EJECUCIÓN
-- =============================================

DO $verification$
DECLARE
    tabla_count INTEGER;
    indice_count INTEGER;
    policy_count INTEGER;
    constraint_count INTEGER;
    registro_count INTEGER;
BEGIN
    -- Verificar tabla creada
    SELECT COUNT(*) INTO tabla_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = '[NOMBRE_TABLA]';
    
    -- Verificar índices creados
    SELECT COUNT(*) INTO indice_count
    FROM pg_indexes 
    WHERE tablename = '[NOMBRE_TABLA]' 
    AND schemaname = 'public';
    
    -- Verificar RLS policies
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' 
    AND schemaname = 'public';
    
    -- Verificar constraints
    SELECT COUNT(*) INTO constraint_count
    FROM information_schema.table_constraints
    WHERE table_name = '[NOMBRE_TABLA]' 
    AND table_schema = 'public'
    AND constraint_type = 'CHECK';
    
    -- Verificar registros iniciales
    EXECUTE 'SELECT COUNT(*) FROM [NOMBRE_TABLA]' INTO registro_count;
    
    -- Log resultados verificación
    RAISE NOTICE '=== VERIFICACIÓN CREACIÓN TABLA [NOMBRE_TABLA] ===';
    RAISE NOTICE 'Tabla creada: % (esperado: 1)', tabla_count;
    RAISE NOTICE 'Índices creados: % (esperado: ≥4)', indice_count;
    RAISE NOTICE 'RLS policies: % (esperado: ≥2)', policy_count;
    RAISE NOTICE 'Check constraints: % (esperado: ≥3)', constraint_count;
    RAISE NOTICE 'Registros iniciales: %', registro_count;
    
    -- Validación final
    IF tabla_count = 1 AND indice_count >= 4 AND policy_count >= 2 THEN
        RAISE NOTICE '✅ SUCCESS: Tabla [NOMBRE_TABLA] creada exitosamente';
        RAISE NOTICE 'Schema structure: COMPLETO';
        RAISE NOTICE 'Security policies: CONFIGURADAS';
        RAISE NOTICE 'Performance indexes: APLICADOS';
    ELSE
        RAISE EXCEPTION '❌ ERROR: Creación tabla [NOMBRE_TABLA] incompleta';
    END IF;
    
    RAISE NOTICE '================================================';
END;
$verification$;

COMMIT;

-- =============================================
-- NOTAS DE USO DEL TEMPLATE
-- =============================================
/*
INSTRUCCIONES DE USO:

1. REEMPLAZAR PLACEHOLDERS:
   - [NOMBRE_TABLA]: Nombre de la tabla en snake_case
   - [DD mes AAAA]: Fecha actual
   - [Tu nombre]: Tu nombre o equipo
   - [Agregar campos específicos]: Campos específicos del business

2. CUSTOMIZAR PARA TU CASO:
   - Ajustar campos según necesidad business
   - Modificar constraints según reglas de negocio
   - Agregar/remover índices según queries esperados
   - Ajustar RLS policies según modelo de seguridad

3. VALIDAR ANTES DE APLICAR:
   - Revisar que nombres de campos son descriptivos
   - Verificar que constraints están bien definidos  
   - Confirmar que índices son necesarios
   - Test con `supabase db reset` localmente

4. EJEMPLO DE PERSONALIZACIÓN:
   Ver ejemplo real en: create_catalogo_ocupaciones_example.sql

CAMPOS COMUNES POR CONTEXTO:

MÉDICO/CLÍNICO:
- paciente_id UUID REFERENCES pacientes(id)
- medico_id UUID REFERENCES medicos(id)
- fecha_atencion TIMESTAMPTZ
- observaciones_clinicas TEXT
- diagnosticos JSONB

CATÁLOGOS/LOOKUPS:
- codigo VARCHAR(20) UNIQUE NOT NULL
- descripcion TEXT NOT NULL  
- activo BOOLEAN DEFAULT TRUE
- orden_display INTEGER

TRANSACCIONAL:
- estado estado_enum DEFAULT 'pendiente'
- fecha_inicio DATE
- fecha_fin DATE
- usuario_responsable UUID
- notas_proceso TEXT

COMPLIANCE/REGULATORIO:
- cumple_resolucion_3280 BOOLEAN DEFAULT FALSE
- datos_reporteria_sispro JSONB
- auditoria_normativa JSONB
- fecha_reporte_ultimo DATE
*/