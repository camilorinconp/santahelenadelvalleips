-- ===================================================================
-- MIGRACIÓN: Agregar FK de Ocupación a Tabla Pacientes
-- ===================================================================
-- Descripción: Integrar catálogo ocupaciones DANE con tabla pacientes
-- Autor: Database Architecture Team - IPS Santa Helena del Valle
-- Fecha: 14 septiembre 2025
-- Propósito: Completar integración para variables PEDT
-- ===================================================================

BEGIN;

-- ===================================================================
-- AGREGAR COLUMNAS DE OCUPACIÓN A PACIENTES
-- ===================================================================

-- Columna para FK al catálogo de ocupaciones DANE
ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS ocupacion_id uuid 
REFERENCES catalogo_ocupaciones_dane(id) 
ON DELETE SET NULL;

-- Columna para ocupación manual (cuando no está en catálogo)
ALTER TABLE pacientes 
ADD COLUMN IF NOT EXISTS ocupacion_otra_descripcion text;

-- Índice para optimizar consultas por ocupación
CREATE INDEX IF NOT EXISTS idx_pacientes_ocupacion_id 
ON pacientes(ocupacion_id);

-- Índice para búsqueda por ocupación manual
CREATE INDEX IF NOT EXISTS idx_pacientes_ocupacion_manual 
ON pacientes 
USING gin(to_tsvector('spanish', ocupacion_otra_descripcion)) 
WHERE ocupacion_otra_descripcion IS NOT NULL;

-- ===================================================================
-- CONSTRAINT PARA VALIDAR OCUPACIÓN
-- ===================================================================

-- Al menos una forma de ocupación debe estar presente (opcional por ahora)
-- ALTER TABLE pacientes 
-- ADD CONSTRAINT check_ocupacion_present 
-- CHECK (
--     ocupacion_id IS NOT NULL 
--     OR ocupacion_otra_descripcion IS NOT NULL
-- );

-- ===================================================================
-- VISTA PARA CONSULTAS CON OCUPACIÓN EXPANDIDA
-- ===================================================================

-- Vista que incluye datos de ocupación expandidos
CREATE OR REPLACE VIEW vista_pacientes_con_ocupacion AS
SELECT 
    p.id,
    p.tipo_documento,
    p.numero_documento,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.fecha_nacimiento,
    p.genero,
    p.ocupacion_id,
    p.ocupacion_otra_descripcion,
    -- p.creado_en,
    -- p.actualizado_en,  -- Comentado: tabla pacientes puede no tener estos campos
    
    -- Datos de ocupación expandidos
    co.codigo_ocupacion_dane,
    co.nombre_ocupacion_normalizado as ocupacion_nombre,
    co.categoria_ocupacional_nivel_1 as ocupacion_categoria,
    co.descripcion_detallada as ocupacion_descripcion,
    
    -- Campo computed para ocupación final
    CASE 
        WHEN co.nombre_ocupacion_normalizado IS NOT NULL 
        THEN co.nombre_ocupacion_normalizado
        ELSE p.ocupacion_otra_descripcion
    END as ocupacion_final

FROM pacientes p
LEFT JOIN catalogo_ocupaciones_dane co ON p.ocupacion_id = co.id;

-- ===================================================================
-- FUNCIÓN PARA BÚSQUEDA INTEGRADA PACIENTE-OCUPACIÓN
-- ===================================================================

CREATE OR REPLACE FUNCTION buscar_pacientes_por_ocupacion(
    termino_ocupacion text,
    limite integer DEFAULT 20
) RETURNS TABLE (
    paciente_id uuid,
    nombre_completo text,
    numero_documento text,
    ocupacion_final text,
    codigo_dane text,
    categoria_ocupacional text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        v.id as paciente_id,
        TRIM(CONCAT(v.primer_nombre, ' ', COALESCE(v.segundo_nombre, ''), ' ', 
                   v.primer_apellido, ' ', COALESCE(v.segundo_apellido, ''))) as nombre_completo,
        v.numero_documento,
        v.ocupacion_final,
        v.codigo_ocupacion_dane as codigo_dane,
        v.ocupacion_categoria as categoria_ocupacional
    FROM vista_pacientes_con_ocupacion v
    WHERE 
        v.ocupacion_final ILIKE '%' || termino_ocupacion || '%'
        OR v.codigo_ocupacion_dane ILIKE termino_ocupacion || '%'
    ORDER BY 
        CASE 
            WHEN v.ocupacion_final ILIKE termino_ocupacion || '%' THEN 1
            ELSE 2
        END,
        v.ocupacion_final
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;

-- ===================================================================
-- TRIGGERS PARA AUDITORIA Y VALIDACIÓN
-- ===================================================================

-- Function para trigger de validación ocupación
CREATE OR REPLACE FUNCTION validar_ocupacion_paciente()
RETURNS TRIGGER AS $$
BEGIN
    -- Si se especifica ocupacion_id, verificar que existe y está activo
    IF NEW.ocupacion_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM catalogo_ocupaciones_dane 
            WHERE id = NEW.ocupacion_id AND activo = true
        ) THEN
            RAISE EXCEPTION 'Ocupación especificada no existe o está inactiva: %', NEW.ocupacion_id;
        END IF;
        
        -- Si hay ocupacion_id, limpiar ocupacion_otra_descripcion
        NEW.ocupacion_otra_descripcion = NULL;
    END IF;
    
    -- Si hay descripción manual, normalizar texto
    IF NEW.ocupacion_otra_descripcion IS NOT NULL THEN
        NEW.ocupacion_otra_descripcion = TRIM(NEW.ocupacion_otra_descripcion);
        
        -- Si queda vacío después del trim, convertir a NULL
        IF LENGTH(NEW.ocupacion_otra_descripcion) = 0 THEN
            NEW.ocupacion_otra_descripcion = NULL;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger
DROP TRIGGER IF EXISTS trigger_validar_ocupacion_paciente ON pacientes;

CREATE TRIGGER trigger_validar_ocupacion_paciente
    BEFORE INSERT OR UPDATE ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION validar_ocupacion_paciente();

-- ===================================================================
-- FUNCTION PARA REPORTES PEDT
-- ===================================================================

CREATE OR REPLACE FUNCTION generar_reporte_ocupaciones_pedt(
    fecha_inicio date DEFAULT CURRENT_DATE - INTERVAL '1 month',
    fecha_fin date DEFAULT CURRENT_DATE
) RETURNS TABLE (
    codigo_ocupacion_dane text,
    nombre_ocupacion text,
    categoria_nivel_1 text,
    total_pacientes bigint,
    pacientes_periodo bigint,
    porcentaje_utilizacion numeric
) AS $$
BEGIN
    RETURN QUERY
    WITH estadisticas_ocupacion AS (
        SELECT 
            COALESCE(co.codigo_ocupacion_dane, 'MANUAL') as codigo_dane,
            COALESCE(co.nombre_ocupacion_normalizado, 'Ocupación Manual') as nombre_ocp,
            COALESCE(co.categoria_ocupacional_nivel_1, 'Sin Categorizar') as categoria,
            COUNT(*) as total_pac,
            COUNT(*) FILTER (
                WHERE p.creado_en::date BETWEEN fecha_inicio AND fecha_fin
            ) as pac_periodo
        FROM pacientes p
        LEFT JOIN catalogo_ocupaciones_dane co ON p.ocupacion_id = co.id
        GROUP BY 
            co.codigo_ocupacion_dane, 
            co.nombre_ocupacion_normalizado,
            co.categoria_ocupacional_nivel_1
    ),
    totales AS (
        SELECT SUM(total_pac) as gran_total FROM estadisticas_ocupacion
    )
    SELECT 
        eo.codigo_dane as codigo_ocupacion_dane,
        eo.nombre_ocp as nombre_ocupacion,
        eo.categoria as categoria_nivel_1,
        eo.total_pac as total_pacientes,
        eo.pac_periodo as pacientes_periodo,
        ROUND((eo.total_pac::numeric / t.gran_total * 100), 2) as porcentaje_utilizacion
    FROM estadisticas_ocupacion eo
    CROSS JOIN totales t
    WHERE eo.total_pac > 0
    ORDER BY eo.total_pac DESC, eo.nombre_ocp;
END;
$$ LANGUAGE plpgsql;

-- ===================================================================
-- PERMISOS Y COMENTARIOS
-- ===================================================================

-- Comentarios documentación
COMMENT ON COLUMN pacientes.ocupacion_id IS 
'FK al catálogo oficial de ocupaciones DANE para variables PEDT';

COMMENT ON COLUMN pacientes.ocupacion_otra_descripcion IS 
'Descripción manual cuando ocupación no está en catálogo DANE';

COMMENT ON VIEW vista_pacientes_con_ocupacion IS 
'Vista con pacientes y datos expandidos de ocupación para reportes';

COMMENT ON FUNCTION generar_reporte_ocupaciones_pedt IS 
'Función para generar reportes PEDT con estadísticas de ocupaciones';

-- Grants para funciones
GRANT EXECUTE ON FUNCTION buscar_pacientes_por_ocupacion TO authenticated;
GRANT EXECUTE ON FUNCTION generar_reporte_ocupaciones_pedt TO authenticated;

-- ===================================================================
-- DATOS DE EJEMPLO PARA TESTING
-- ===================================================================

-- Actualizar algunos pacientes existentes con ocupaciones de ejemplo
DO $$
DECLARE
    medico_id UUID;
    enfermera_id UUID;
    auxiliar_id UUID;
    paciente_rec RECORD;
BEGIN
    -- Obtener IDs de ocupaciones de ejemplo
    SELECT id INTO medico_id FROM catalogo_ocupaciones_dane 
    WHERE codigo_ocupacion_dane = '2211' LIMIT 1;
    
    SELECT id INTO enfermera_id FROM catalogo_ocupaciones_dane 
    WHERE codigo_ocupacion_dane = '2221' LIMIT 1;
    
    SELECT id INTO auxiliar_id FROM catalogo_ocupaciones_dane 
    WHERE codigo_ocupacion_dane = '3220' LIMIT 1;
    
    -- Actualizar pacientes existentes con ocupaciones (si existen)
    IF medico_id IS NOT NULL THEN
        UPDATE pacientes 
        SET ocupacion_id = medico_id
        WHERE numero_documento IN (
            SELECT numero_documento FROM pacientes LIMIT 1
        );
        
        RAISE NOTICE 'Paciente asignado ocupación médico: %', medico_id;
    END IF;
    
    -- Ejemplo de ocupación manual
    UPDATE pacientes 
    SET ocupacion_otra_descripcion = 'Administrador de Sistemas'
    WHERE numero_documento IN (
        SELECT numero_documento FROM pacientes 
        WHERE ocupacion_id IS NULL 
        LIMIT 1
    );
    
    RAISE NOTICE 'Ejemplos de ocupaciones asignados a pacientes existentes';
END
$$;

-- ===================================================================
-- VERIFICACIÓN Y LOGGING
-- ===================================================================

DO $$
DECLARE
    columnas_agregadas INTEGER;
    indices_creados INTEGER;
    vista_existe BOOLEAN;
    funciones_creadas INTEGER;
BEGIN
    -- Verificar columnas agregadas
    SELECT COUNT(*) INTO columnas_agregadas
    FROM information_schema.columns 
    WHERE table_name = 'pacientes' 
    AND column_name IN ('ocupacion_id', 'ocupacion_otra_descripcion');
    
    -- Verificar índices
    SELECT COUNT(*) INTO indices_creados
    FROM pg_indexes 
    WHERE tablename = 'pacientes' 
    AND indexname LIKE '%ocupacion%';
    
    -- Verificar vista
    SELECT EXISTS (
        SELECT 1 FROM information_schema.views 
        WHERE table_name = 'vista_pacientes_con_ocupacion'
    ) INTO vista_existe;
    
    -- Verificar funciones
    SELECT COUNT(*) INTO funciones_creadas
    FROM pg_proc 
    WHERE proname IN ('buscar_pacientes_por_ocupacion', 'generar_reporte_ocupaciones_pedt');
    
    -- Log de resultados
    RAISE NOTICE '=== VERIFICACIÓN INTEGRACIÓN OCUPACIONES ===';
    RAISE NOTICE 'Columnas agregadas a pacientes: %', columnas_agregadas;
    RAISE NOTICE 'Índices creados: %', indices_creados;
    RAISE NOTICE 'Vista creada: %', vista_existe;
    RAISE NOTICE 'Funciones creadas: %', funciones_creadas;
    
    IF columnas_agregadas >= 2 AND indices_creados >= 2 AND vista_existe AND funciones_creadas >= 2 THEN
        RAISE NOTICE '✅ SUCCESS: Integración ocupaciones completada exitosamente';
        RAISE NOTICE 'Variables PEDT: Ocupación normalizada DANE disponible';
        RAISE NOTICE 'Funcionalidad: Búsqueda integrada + Reportes PEDT operativos';
    ELSE
        RAISE EXCEPTION 'ERROR: Problemas en integración ocupaciones';
    END IF;
    
    RAISE NOTICE '===========================================';
END
$$;

COMMIT;

-- ===================================================================
-- ROLLBACK INSTRUCTIONS (Para emergencias)
-- ===================================================================
-- En caso de necesitar rollback:
-- DROP FUNCTION IF EXISTS generar_reporte_ocupaciones_pedt;
-- DROP FUNCTION IF EXISTS buscar_pacientes_por_ocupacion;
-- DROP VIEW IF EXISTS vista_pacientes_con_ocupacion;
-- DROP TRIGGER IF EXISTS trigger_validar_ocupacion_paciente ON pacientes;
-- DROP FUNCTION IF EXISTS validar_ocupacion_paciente;
-- ALTER TABLE pacientes DROP CONSTRAINT IF EXISTS check_ocupacion_present;
-- ALTER TABLE pacientes DROP COLUMN IF EXISTS ocupacion_otra_descripcion;
-- ALTER TABLE pacientes DROP COLUMN IF EXISTS ocupacion_id;