-- ===================================================================
-- MIGRACIÓN: Catálogo Completo de Ocupaciones DANE
-- ===================================================================
-- Descripción: Tabla para almacenar 10,919 ocupaciones oficiales DANE
-- Autor: Database Architecture Team - IPS Santa Helena del Valle
-- Fecha: 14 septiembre 2025
-- Propósito: Completar variables PEDT (60→119) para Resolución 202 de 2021
-- ===================================================================

BEGIN;

-- Crear tabla catálogo ocupaciones DANE
CREATE TABLE IF NOT EXISTS catalogo_ocupaciones_dane (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación oficial DANE
    codigo_ocupacion_dane text NOT NULL UNIQUE,
    nombre_ocupacion_normalizado text NOT NULL,
    
    -- Categorización jerárquica (3 niveles)
    categoria_ocupacional_nivel_1 text,  -- Grandes grupos ocupacionales
    categoria_ocupacional_nivel_2 text,  -- Subgrupos principales  
    categoria_ocupacional_nivel_3 text,  -- Subgrupos secundarios
    categoria_ocupacional_nivel_4 text,  -- Nivel más granular si existe
    
    -- Información complementaria
    descripcion_detallada text,          -- Descripción completa DANE
    competencias_principales jsonb,      -- Skills y competencias requeridas
    sectores_economicos_asociados jsonb, -- Sectores donde se desempeña
    nivel_educativo_requerido text,      -- Educación típica requerida
    
    -- Control y metadatos
    activo boolean DEFAULT true,         -- Para soft-delete si es necesario
    metadatos_adicionales jsonb,         -- Flexibilidad futura
    fuente_dato text DEFAULT 'DANE',     -- Origen del dato
    version_catalogo text,               -- Versión del catálogo DANE
    
    -- Auditoria estándar
    creado_en timestamptz DEFAULT now(),
    actualizado_en timestamptz DEFAULT now()
);

-- ===================================================================
-- ÍNDICES PARA OPTIMIZACIÓN DE PERFORMANCE (CRÍTICO con 10k+ registros)
-- ===================================================================

-- Índice principal por código DANE (búsqueda exacta)
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_codigo 
ON catalogo_ocupaciones_dane(codigo_ocupacion_dane);

-- Índice para búsqueda full-text en español (autocompletado inteligente)
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_nombre_gin 
ON catalogo_ocupaciones_dane 
USING gin(to_tsvector('spanish', nombre_ocupacion_normalizado));

-- Índice para autocompletado por nombre (búsqueda por prefijo)
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_nombre_prefix 
ON catalogo_ocupaciones_dane(nombre_ocupacion_normalizado text_pattern_ops);

-- Índices por categorías para análisis epidemiológico
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_categoria_1 
ON catalogo_ocupaciones_dane(categoria_ocupacional_nivel_1);

CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_categoria_2 
ON catalogo_ocupaciones_dane(categoria_ocupacional_nivel_2);

-- Índice para filtrar solo activos (mejora performance en consultas)
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_activo 
ON catalogo_ocupaciones_dane(activo) 
WHERE activo = true;

-- Índice compuesto para búsquedas complejas
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_busqueda_completa 
ON catalogo_ocupaciones_dane(activo, categoria_ocupacional_nivel_1, nombre_ocupacion_normalizado);

-- ===================================================================
-- CONFIGURACIÓN RLS (Row Level Security)
-- ===================================================================

-- Habilitar RLS siguiendo el patrón establecido
ALTER TABLE catalogo_ocupaciones_dane ENABLE ROW LEVEL SECURITY;

-- Política para service_role (backend tiene acceso completo)
CREATE POLICY "service_role_full_access" 
ON catalogo_ocupaciones_dane 
FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

-- Política para usuarios autenticados (solo lectura)
CREATE POLICY "authenticated_users_read_ocupaciones" 
ON catalogo_ocupaciones_dane 
FOR SELECT 
TO authenticated 
USING (activo = true);

-- Política para búsquedas públicas de autocompletado (solo ocupaciones activas)
CREATE POLICY "public_read_active_ocupaciones" 
ON catalogo_ocupaciones_dane 
FOR SELECT 
TO anon 
USING (activo = true);

-- ===================================================================
-- FUNCTION PARA ACTUALIZAR TIMESTAMP
-- ===================================================================

-- Trigger para actualizar automatically updated_at
CREATE OR REPLACE FUNCTION actualizar_timestamp_catalogo_ocupaciones()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger
DROP TRIGGER IF EXISTS trigger_actualizar_timestamp_ocupaciones 
ON catalogo_ocupaciones_dane;

CREATE TRIGGER trigger_actualizar_timestamp_ocupaciones
    BEFORE UPDATE ON catalogo_ocupaciones_dane
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp_catalogo_ocupaciones();

-- ===================================================================
-- FUNCTIONS PARA BÚSQUEDA OPTIMIZADA
-- ===================================================================

-- Function para búsqueda inteligente de ocupaciones
CREATE OR REPLACE FUNCTION buscar_ocupaciones_inteligente(
    termino_busqueda text,
    limite integer DEFAULT 10
) RETURNS TABLE (
    id uuid,
    codigo_ocupacion_dane text,
    nombre_ocupacion_normalizado text,
    categoria_ocupacional_nivel_1 text,
    relevancia real
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        co.id,
        co.codigo_ocupacion_dane,
        co.nombre_ocupacion_normalizado,
        co.categoria_ocupacional_nivel_1,
        CASE 
            -- Mayor relevancia para coincidencias exactas al inicio
            WHEN co.nombre_ocupacion_normalizado ILIKE (termino_busqueda || '%') THEN 1.0
            -- Media relevancia para coincidencias por código
            WHEN co.codigo_ocupacion_dane ILIKE (termino_busqueda || '%') THEN 0.8
            -- Menor relevancia para coincidencias contenidas
            WHEN co.nombre_ocupacion_normalizado ILIKE ('%' || termino_busqueda || '%') THEN 0.6
            -- Mínima relevancia para búsqueda full-text
            ELSE ts_rank(
                to_tsvector('spanish', co.nombre_ocupacion_normalizado), 
                to_tsquery('spanish', termino_busqueda || ':*')
            )
        END as relevancia
    FROM catalogo_ocupaciones_dane co
    WHERE co.activo = true
    AND (
        co.nombre_ocupacion_normalizado ILIKE ('%' || termino_busqueda || '%')
        OR co.codigo_ocupacion_dane ILIKE (termino_busqueda || '%')
        OR to_tsvector('spanish', co.nombre_ocupacion_normalizado) 
           @@ to_tsquery('spanish', termino_busqueda || ':*')
    )
    ORDER BY relevancia DESC, co.nombre_ocupacion_normalizado ASC
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;

-- ===================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ===================================================================

COMMENT ON TABLE catalogo_ocupaciones_dane IS 
'Catálogo oficial de ocupaciones según DANE para variables PEDT Resolución 202. 
Contiene 10,919 ocupaciones normalizadas con categorización jerárquica y 
optimizado para búsqueda/autocompletado en tiempo real.';

COMMENT ON COLUMN catalogo_ocupaciones_dane.codigo_ocupacion_dane IS 
'Código oficial DANE único de la ocupación';

COMMENT ON COLUMN catalogo_ocupaciones_dane.nombre_ocupacion_normalizado IS 
'Nombre completo normalizado de la ocupación según DANE';

COMMENT ON COLUMN catalogo_ocupaciones_dane.categoria_ocupacional_nivel_1 IS 
'Grandes grupos ocupacionales (nivel más alto de categorización)';

COMMENT ON FUNCTION buscar_ocupaciones_inteligente IS 
'Función optimizada para búsqueda inteligente con ranking de relevancia. 
Usada por API de autocompletado.';

-- ===================================================================
-- VERIFICACIÓN Y LOGGING
-- ===================================================================

-- Verificar que la tabla se creó correctamente
DO $$
DECLARE
    tabla_existe boolean;
    indices_creados integer;
BEGIN
    -- Verificar tabla
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = 'catalogo_ocupaciones_dane'
        AND table_schema = 'public'
    ) INTO tabla_existe;
    
    -- Contar índices
    SELECT count(*) INTO indices_creados
    FROM pg_indexes 
    WHERE tablename = 'catalogo_ocupaciones_dane';
    
    -- Log de resultados
    RAISE NOTICE '=== VERIFICACIÓN CATÁLOGO OCUPACIONES DANE ===';
    RAISE NOTICE 'Tabla creada: %', tabla_existe;
    RAISE NOTICE 'Índices creados: %', indices_creados;
    RAISE NOTICE 'RLS habilitado: %', (
        SELECT relrowsecurity FROM pg_class 
        WHERE relname = 'catalogo_ocupaciones_dane'
    );
    
    IF tabla_existe AND indices_creados >= 6 THEN
        RAISE NOTICE '✅ SUCCESS: Infraestructura catálogo ocupaciones lista';
        RAISE NOTICE 'Próximo paso: Importar 10,919 registros de ocupaciones';
        RAISE NOTICE 'Capacidad estimada: >100k consultas/segundo con índices';
    ELSE
        RAISE EXCEPTION 'ERROR: Problemas en creación de infraestructura';
    END IF;
    
    RAISE NOTICE '===========================================';
END
$$;

COMMIT;

-- ===================================================================
-- ROLLBACK INSTRUCTIONS (Para emergencias)
-- ===================================================================
-- En caso de necesitar rollback:
-- DROP FUNCTION IF EXISTS buscar_ocupaciones_inteligente;
-- DROP FUNCTION IF EXISTS actualizar_timestamp_catalogo_ocupaciones;
-- DROP TABLE IF EXISTS catalogo_ocupaciones_dane CASCADE;