-- =============================================
-- TEMPLATE: AGREGAR COLUMNA A TABLA EXISTENTE
-- =============================================
-- Descripción: Template reutilizable para agregar columnas siguiendo
--              convenciones del proyecto IPS Santa Helena del Valle
-- Fecha: [DD mes AAAA]
-- Autor: [Tu nombre]
-- Contexto: [Por qué se necesita esta nueva columna]
-- Impacto: [Describir impacto en aplicación existente]
-- =============================================

BEGIN;

-- =============================================
-- 1. VERIFICACIONES PRE-EJECUCIÓN
-- =============================================
DO $pre_check$
DECLARE
    table_exists BOOLEAN;
    column_exists BOOLEAN;
BEGIN
    -- Verificar que la tabla existe
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = '[NOMBRE_TABLA]'
    ) INTO table_exists;
    
    IF NOT table_exists THEN
        RAISE EXCEPTION 'Tabla [NOMBRE_TABLA] no existe. Crear tabla primero.';
    END IF;
    
    -- Verificar que la columna no existe ya
    SELECT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = '[NOMBRE_TABLA]'
        AND column_name = '[NOMBRE_COLUMNA]'
    ) INTO column_exists;
    
    IF column_exists THEN
        RAISE NOTICE 'ℹ️  Columna [NOMBRE_COLUMNA] ya existe en [NOMBRE_TABLA], saltando creación';
    ELSE
        RAISE NOTICE '➕ Agregando columna [NOMBRE_COLUMNA] a tabla [NOMBRE_TABLA]';
    END IF;
END;
$pre_check$;

-- =============================================
-- 2. AGREGAR COLUMNA(S) PRINCIPAL(ES)
-- =============================================

-- Columna básica - TEXT
ALTER TABLE [NOMBRE_TABLA] 
ADD COLUMN IF NOT EXISTS [NOMBRE_COLUMNA] TEXT;

-- Columna con valor por defecto - BOOLEAN
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_columna_boolean BOOLEAN DEFAULT FALSE;

-- Columna numérica con constraints
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_columna_numerica INTEGER DEFAULT 0
-- CHECK (nueva_columna_numerica >= 0);

-- Columna fecha/timestamp
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_columna_fecha TIMESTAMPTZ DEFAULT NOW();

-- Columna ENUM (crear enum primero si no existe)
-- CREATE TYPE IF NOT EXISTS nuevo_enum_type AS ENUM ('valor1', 'valor2', 'valor3');
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_columna_enum nuevo_enum_type DEFAULT 'valor1';

-- Columna JSONB para datos semi-estructurados
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_columna_jsonb JSONB DEFAULT '{}';

-- Columna FOREIGN KEY (agregar constraint después)
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD COLUMN IF NOT EXISTS nueva_fk_id UUID;

-- =============================================
-- 3. POBLAR DATOS EXISTENTES (SI ES NECESARIO)
-- =============================================

-- Actualizar registros existentes con valor por defecto
UPDATE [NOMBRE_TABLA] 
SET [NOMBRE_COLUMNA] = '[VALOR_DEFECTO]'
WHERE [NOMBRE_COLUMNA] IS NULL;

-- Ejemplo: Poblar basado en lógica business
-- UPDATE [NOMBRE_TABLA] 
-- SET nueva_columna_calculada = 
--     CASE 
--         WHEN condicion_1 THEN 'valor_a'
--         WHEN condicion_2 THEN 'valor_b'
--         ELSE 'valor_default'
--     END
-- WHERE nueva_columna_calculada IS NULL;

-- Ejemplo: Poblar desde otra tabla
-- UPDATE [NOMBRE_TABLA] t
-- SET nueva_columna_desde_otra_tabla = o.campo_origen
-- FROM otra_tabla o
-- WHERE t.fk_id = o.id 
-- AND t.nueva_columna_desde_otra_tabla IS NULL;

-- =============================================
-- 4. APLICAR CONSTRAINTS DESPUÉS DE POBLAR
-- =============================================

-- NOT NULL constraint (después de poblar datos)
-- ALTER TABLE [NOMBRE_TABLA] 
-- ALTER COLUMN [NOMBRE_COLUMNA] SET NOT NULL;

-- CHECK constraint business logic
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD CONSTRAINT check_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]_valido
-- CHECK ([NOMBRE_COLUMNA] != '' AND [NOMBRE_COLUMNA] IS NOT NULL);

-- UNIQUE constraint si aplica
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD CONSTRAINT unique_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]
-- UNIQUE ([NOMBRE_COLUMNA]);

-- FOREIGN KEY constraint
-- ALTER TABLE [NOMBRE_TABLA] 
-- ADD CONSTRAINT fk_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]
-- FOREIGN KEY ([NOMBRE_COLUMNA]) REFERENCES [TABLA_REFERENCIA](id)
-- ON DELETE [CASCADE|SET NULL|RESTRICT];

-- =============================================
-- 5. CREAR ÍNDICES PARA PERFORMANCE
-- =============================================

-- Índice básico para búsquedas
CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]
ON [NOMBRE_TABLA]([NOMBRE_COLUMNA])
WHERE [NOMBRE_COLUMNA] IS NOT NULL;

-- Índice parcial para valores específicos (performance)
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]_activos
-- ON [NOMBRE_TABLA]([NOMBRE_COLUMNA])
-- WHERE [NOMBRE_COLUMNA] = 'valor_frecuente';

-- Índice compuesto si se usa en queries junto con otras columnas
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_compuesto
-- ON [NOMBRE_TABLA]([NOMBRE_COLUMNA], otra_columna_frecuente);

-- Índice GIN para JSONB
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]_gin
-- ON [NOMBRE_TABLA] USING GIN ([NOMBRE_COLUMNA]);

-- Índice para foreign key (crítico performance)
-- CREATE INDEX IF NOT EXISTS idx_[NOMBRE_TABLA]_[NOMBRE_COLUMNA]_fk
-- ON [NOMBRE_TABLA]([NOMBRE_COLUMNA]);

-- =============================================
-- 6. ACTUALIZAR RLS POLICIES SI ES NECESARIO
-- =============================================

-- Si la nueva columna afecta las políticas de seguridad
-- Ejemplo: columna que determina visibilidad

-- DROP policy existente si necesita modificación
-- DROP POLICY IF EXISTS "authenticated_read_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- Crear policy actualizada
-- CREATE POLICY "authenticated_read_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT USING (
--     auth.role() = 'authenticated' 
--     AND ([NOMBRE_COLUMNA] = 'publico' OR [NOMBRE_COLUMNA] IS NULL)
-- );

-- Policy para service_role sigue siendo completa (no modificar)
-- Mantener: "service_role_full_access_[NOMBRE_TABLA]" intacta

-- =============================================
-- 7. ACTUALIZAR TRIGGERS SI ES NECESARIO
-- =============================================

-- Si necesitas que el trigger de timestamp considere la nueva columna
-- Ejemplo: Trigger que se dispara solo cuando ciertos campos cambian

-- CREATE OR REPLACE FUNCTION trigger_[NOMBRE_TABLA]_selective_update()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- Solo actualizar timestamp si campos críticos cambiaron
--     IF (OLD.[NOMBRE_COLUMNA] IS DISTINCT FROM NEW.[NOMBRE_COLUMNA]) 
--        OR (OLD.otra_columna_critica IS DISTINCT FROM NEW.otra_columna_critica) THEN
--         NEW.actualizado_en = NOW();
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- =============================================
-- 8. COMENTARIOS DOCUMENTACIÓN
-- =============================================

COMMENT ON COLUMN [NOMBRE_TABLA].[NOMBRE_COLUMNA] IS 
'[Descripción completa de la columna: propósito, valores válidos, 
relación con otras columnas, contexto business, etc.]';

-- Ejemplos de comentarios según tipo de columna:

-- Para columnas de estado/enum:
-- 'Estado del registro: activo|inactivo|pendiente. 
-- Determina si el registro está disponible para operaciones.'

-- Para columnas calculadas:  
-- 'Campo calculado automáticamente basado en [lógica]. 
-- Se actualiza via trigger cuando [condiciones].'

-- Para columnas de compliance:
-- 'Indica cumplimiento con Resolución 3280 artículo X. 
-- Requerido para reportería SISPRO. Valores: true=cumple, false=no_cumple, null=no_evaluado.'

-- =============================================
-- 9. MIGRAR DATOS DE APLICACIÓN SI ES NECESARIO
-- =============================================

-- Si la nueva columna requiere datos de fuentes externas
-- o lógica compleja de migración

-- Ejemplo: Poblar desde archivo CSV
-- COPY [NOMBRE_TABLA]_temp (id, [NOMBRE_COLUMNA])  
-- FROM '/path/to/data.csv' DELIMITER ',' CSV HEADER;

-- UPDATE [NOMBRE_TABLA] t
-- SET [NOMBRE_COLUMNA] = temp.[NOMBRE_COLUMNA]
-- FROM [NOMBRE_TABLA]_temp temp
-- WHERE t.id = temp.id;

-- DROP TABLE [NOMBRE_TABLA]_temp;

-- =============================================
-- 10. VERIFICACIONES POST-EJECUCIÓN
-- =============================================

DO $verification$
DECLARE
    column_exists BOOLEAN;
    non_null_count INTEGER;
    total_count INTEGER;
    index_count INTEGER;
    constraint_count INTEGER;
BEGIN
    -- Verificar columna agregada
    SELECT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = '[NOMBRE_TABLA]'
        AND column_name = '[NOMBRE_COLUMNA]'
    ) INTO column_exists;
    
    -- Verificar poblamiento de datos
    EXECUTE format('SELECT COUNT(*) FROM %I WHERE %I IS NOT NULL', 
                   '[NOMBRE_TABLA]', '[NOMBRE_COLUMNA]') INTO non_null_count;
    
    EXECUTE format('SELECT COUNT(*) FROM %I', 
                   '[NOMBRE_TABLA]') INTO total_count;
    
    -- Verificar índices nuevos
    SELECT COUNT(*) INTO index_count
    FROM pg_indexes 
    WHERE tablename = '[NOMBRE_TABLA]' 
    AND indexname LIKE '%[NOMBRE_COLUMNA]%';
    
    -- Verificar constraints nuevos
    SELECT COUNT(*) INTO constraint_count
    FROM information_schema.constraint_column_usage
    WHERE table_name = '[NOMBRE_TABLA]' 
    AND column_name = '[NOMBRE_COLUMNA]';
    
    -- Log resultados verificación
    RAISE NOTICE '=== VERIFICACIÓN AGREGAR COLUMNA [NOMBRE_COLUMNA] ===';
    RAISE NOTICE 'Columna creada: %', column_exists;
    RAISE NOTICE 'Registros con datos: % de % (%.1f%%)', 
                 non_null_count, total_count, 
                 CASE WHEN total_count > 0 THEN (non_null_count * 100.0 / total_count) ELSE 0 END;
    RAISE NOTICE 'Índices creados: %', index_count;
    RAISE NOTICE 'Constraints aplicados: %', constraint_count;
    
    -- Validación final
    IF column_exists THEN
        RAISE NOTICE '✅ SUCCESS: Columna [NOMBRE_COLUMNA] agregada exitosamente';
        
        IF non_null_count = total_count AND total_count > 0 THEN
            RAISE NOTICE '✅ Datos poblados completamente';
        ELSIF non_null_count > 0 THEN
            RAISE NOTICE '⚠️  Datos parcialmente poblados - revisar lógica';
        ELSE
            RAISE NOTICE 'ℹ️  Sin datos poblados - normal si es columna opcional';
        END IF;
        
        IF index_count > 0 THEN
            RAISE NOTICE '✅ Performance indexes aplicados';
        END IF;
    ELSE
        RAISE EXCEPTION '❌ ERROR: Fallo agregar columna [NOMBRE_COLUMNA]';
    END IF;
    
    RAISE NOTICE '==================================================';
END;
$verification$;

COMMIT;

-- =============================================
-- NOTAS DE USO DEL TEMPLATE
-- =============================================
/*
INSTRUCCIONES DE USO:

1. REEMPLAZAR PLACEHOLDERS:
   - [NOMBRE_TABLA]: Tabla existente donde agregar columna
   - [NOMBRE_COLUMNA]: Nueva columna en snake_case
   - [VALOR_DEFECTO]: Valor por defecto para registros existentes
   - [DD mes AAAA]: Fecha actual
   - [Tu nombre]: Tu nombre o equipo

2. CUSTOMIZAR SEGÚN TIPO DE COLUMNA:
   - Uncomment sección relevante (TEXT, BOOLEAN, INTEGER, etc.)
   - Ajustar constraints según reglas business
   - Configurar índices según uso esperado
   - Poblamiento de datos según necesidad

3. CONSIDERACIONES IMPORTANTES:
   - SIEMPRE poblar datos existentes antes de NOT NULL
   - Crear índices para foreign keys (performance crítica)
   - Actualizar RLS policies si la columna afecta seguridad
   - Test performance después de agregar índices

4. ORDEN DE EJECUCIÓN CRÍTICO:
   a. Agregar columna como NULLABLE
   b. Poblar datos existentes
   c. Aplicar constraints (NOT NULL, CHECK, FK)
   d. Crear índices
   e. Actualizar policies si necesario

5. TIPOS COMUNES Y SUS PATTERNS:

   TEXTO SIMPLE:
   - Tipo: TEXT o VARCHAR(N)
   - Default: NULL o ''
   - Index: Básico si se busca frecuentemente

   NUMÉRICO:
   - Tipo: INTEGER, DECIMAL(precision, scale)
   - Default: 0 o NULL
   - Constraint: CHECK para rangos válidos

   BOOLEAN/ESTADO:
   - Tipo: BOOLEAN o ENUM
   - Default: FALSE o estado inicial
   - Index: Parcial para valor TRUE

   FECHA/TIMESTAMP:
   - Tipo: DATE, TIMESTAMPTZ
   - Default: NOW() o NULL
   - Index: Range queries, partials frecuentes

   FOREIGN KEY:
   - Tipo: UUID
   - Constraint: FK DESPUÉS de poblar
   - Index: SIEMPRE para FK (performance crítica)

   JSONB:
   - Tipo: JSONB
   - Default: '{}'
   - Index: GIN para búsquedas dentro del JSON

6. EJEMPLOS POR CONTEXTO BUSINESS:

   COMPLIANCE/REGULATORIO:
   - cumple_norma BOOLEAN DEFAULT FALSE
   - fecha_ultimo_reporte DATE
   - datos_auditoria JSONB DEFAULT '{}'

   WORKFLOW/ESTADO:
   - estado estado_enum DEFAULT 'inicial'
   - fecha_estado_cambio TIMESTAMPTZ DEFAULT NOW()
   - responsable_actual UUID REFERENCES usuarios(id)

   PERFORMANCE/CACHE:
   - datos_cache JSONB
   - cache_ultimo_update TIMESTAMPTZ
   - cache_valido BOOLEAN DEFAULT FALSE

   MÉDICO/CLÍNICO:
   - observaciones_adicionales TEXT
   - riesgo_nivel INTEGER CHECK (riesgo_nivel BETWEEN 1 AND 5)
   - requiere_seguimiento BOOLEAN DEFAULT FALSE
*/