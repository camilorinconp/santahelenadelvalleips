-- =============================================
-- MIGRACIÓN: CATÁLOGOS CRÍTICOS RESOLUCIÓN 202
-- =============================================
-- Descripción: Crear tablas catálogos transversales prerequisito 
--              para variables PEDT válidas según Resolución 202/2021
-- Fecha: 13 septiembre 2025
-- Autor: Equipo IPS Santa Helena del Valle
-- Impacto: Variables PEDT de hardcoded inválidos → códigos reales válidos
-- =============================================

BEGIN;

-- =============================================
-- 1. CATÁLOGO OCUPACIONES (Variable 11 PEDT)
-- =============================================
-- Fuente: docs_IPS/resolucion_202_data/Tabla ocupaciones.csv
-- Registros: 10,919 ocupaciones según CIUO-08 A.C.
-- Crítico para: Variable 11 (Ocupación) - actualmente hardcoded a 9999

CREATE TABLE IF NOT EXISTS catalogo_ocupaciones (
    codigo_ciuo VARCHAR(10) PRIMARY KEY,
    descripcion TEXT NOT NULL,
    categoria_principal VARCHAR(100),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- Índices para performance en lookups PEDT
CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_activo 
ON catalogo_ocupaciones(activo) WHERE activo = TRUE;

CREATE INDEX IF NOT EXISTS idx_catalogo_ocupaciones_categoria 
ON catalogo_ocupaciones(categoria_principal) WHERE activo = TRUE;

-- Comentarios documentación
COMMENT ON TABLE catalogo_ocupaciones IS 
'Catálogo ocupaciones según CIUO-08 A.C. para Variable 11 PEDT Resolución 202/2021';

COMMENT ON COLUMN catalogo_ocupaciones.codigo_ciuo IS 
'Código CIUO-08 A.C. - Clasificación Internacional Uniforme Ocupaciones';

-- =============================================
-- 2. CATÁLOGO ETNIAS (Variable 10 PEDT)  
-- =============================================
-- Fuente: DANE + Resolución 202/2021
-- Crítico para: Variable 10 (Pertenencia étnica) - actualmente hardcoded a 6

CREATE TABLE IF NOT EXISTS catalogo_etnias (
    codigo_etnia INTEGER PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    grupo_poblacional VARCHAR(50),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- Datos oficiales según DANE
INSERT INTO catalogo_etnias (codigo_etnia, descripcion, grupo_poblacional) VALUES
(1, 'Indígena', 'Grupos étnicos'),
(2, 'Rom (gitano)', 'Grupos étnicos'), 
(3, 'Raizal (archipiélago de San Andrés y Providencia)', 'Grupos étnicos'),
(4, 'Palenquero (San Basilio de Palenque)', 'Grupos étnicos'),
(5, 'Negro, mulato, afrodescendiente, afrocolombiano', 'Grupos étnicos'),
(6, 'Sin pertenencia étnica', 'Población general'),
(7, 'No sabe, no informa', 'Sin información')
ON CONFLICT (codigo_etnia) DO UPDATE SET
    descripcion = EXCLUDED.descripcion,
    grupo_poblacional = EXCLUDED.grupo_poblacional,
    actualizado_en = NOW();

COMMENT ON TABLE catalogo_etnias IS 
'Catálogo etnias según DANE para Variable 10 PEDT Resolución 202/2021';

-- =============================================  
-- 3. CATÁLOGO TIPOS DOCUMENTO (Variable 2 PEDT)
-- =============================================
-- Fuente: Normativa colombiana registro civil + RIPS
-- Crítico para: Variable 2 (Tipo identificación) - actualmente hardcoded

CREATE TABLE IF NOT EXISTS catalogo_tipos_documento (
    codigo_documento VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    aplica_menores BOOLEAN NOT NULL DEFAULT FALSE,
    aplica_adultos BOOLEAN NOT NULL DEFAULT TRUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- Datos oficiales según normativa colombiana
INSERT INTO catalogo_tipos_documento VALUES
('RC', 'Registro Civil', TRUE, FALSE, TRUE, 'Menores de 7 años'),
('TI', 'Tarjeta de Identidad', TRUE, FALSE, TRUE, 'Menores 7-17 años'),
('CC', 'Cédula de Ciudadanía', FALSE, TRUE, TRUE, 'Ciudadanos colombianos ≥18 años'),
('CE', 'Cédula de Extranjería', FALSE, TRUE, TRUE, 'Extranjeros residentes'),
('PA', 'Pasaporte', TRUE, TRUE, TRUE, 'Documento internacional'),
('MS', 'Menor Sin Identificación', TRUE, FALSE, TRUE, 'Menores sin documento'),
('AS', 'Adulto Sin Identificación', FALSE, TRUE, TRUE, 'Adultos sin documento'),
('CD', 'Carné Diplomático', FALSE, TRUE, TRUE, 'Personal diplomático'),
('SC', 'Salvoconducto', TRUE, TRUE, TRUE, 'Documento temporal'),
('PT', 'Permiso Temporal de Permanencia', FALSE, TRUE, TRUE, 'Migrantes venezolanos')
ON CONFLICT (codigo_documento) DO UPDATE SET
    descripcion = EXCLUDED.descripcion,
    aplica_menores = EXCLUDED.aplica_menores,
    aplica_adultos = EXCLUDED.aplica_adultos,
    observaciones = EXCLUDED.observaciones,
    actualizado_en = NOW();

COMMENT ON TABLE catalogo_tipos_documento IS 
'Catálogo tipos documento según normativa colombiana para Variable 2 PEDT Resolución 202/2021';

-- =============================================
-- 4. CATÁLOGO NIVELES EDUCATIVO (Variable 12 PEDT)
-- =============================================  
-- Fuente: DANE + Ministerio Educación Nacional
-- Crítico para: Variable 12 (Nivel educativo) - actualmente hardcoded a 12

CREATE TABLE IF NOT EXISTS catalogo_niveles_educativo (
    codigo_nivel INTEGER PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    nivel_dane VARCHAR(50),
    orden_jerarquico INTEGER,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    observaciones TEXT,
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- Datos oficiales según DANE / MEN
INSERT INTO catalogo_niveles_educativo VALUES
(1, 'Ninguno', 'Sin educación formal', 1, TRUE, 'Sin estudios'),
(2, 'Preescolar', 'Educación inicial', 2, TRUE, 'Educación inicial 3-5 años'),
(3, 'Básica primaria (1° - 5°)', 'Educación básica primaria', 3, TRUE, 'Primaria completa'),
(4, 'Básica secundaria (6° - 9°)', 'Educación básica secundaria', 4, TRUE, 'Secundaria completa'),
(5, 'Media académica o clásica (10° - 11°)', 'Educación media académica', 5, TRUE, 'Bachillerato académico'),
(6, 'Media técnica (10° - 11°)', 'Educación media técnica', 5, TRUE, 'Bachillerato técnico'),
(7, 'Normalista', 'Educación para el trabajo', 6, TRUE, 'Formación docente básica'),
(8, 'Técnica profesional', 'Educación superior técnica', 7, TRUE, '2-3 años educación superior'),
(9, 'Tecnológica', 'Educación superior tecnológica', 8, TRUE, '3-4 años educación superior'), 
(10, 'Profesional', 'Educación superior universitaria', 9, TRUE, '4-6 años educación superior'),
(11, 'Especialización', 'Educación superior postgrado', 10, TRUE, 'Postgrado especialización'),
(12, 'Maestría', 'Educación superior postgrado', 11, TRUE, 'Postgrado maestría'),
(13, 'Doctorado', 'Educación superior postgrado', 12, TRUE, 'Postgrado doctorado'),
(99, 'Sin información', 'No determinado', 99, TRUE, 'Datos no disponibles')
ON CONFLICT (codigo_nivel) DO UPDATE SET
    descripcion = EXCLUDED.descripcion,
    nivel_dane = EXCLUDED.nivel_dane,
    orden_jerarquico = EXCLUDED.orden_jerarquico,
    observaciones = EXCLUDED.observaciones,
    actualizado_en = NOW();

COMMENT ON TABLE catalogo_niveles_educativo IS 
'Catálogo niveles educativo según DANE/MEN para Variable 12 PEDT Resolución 202/2021';

-- =============================================
-- 5. ÍNDICES ADICIONALES DE PERFORMANCE
-- =============================================

-- Índices para lookups frecuentes en GeneradorReportePEDT
CREATE INDEX IF NOT EXISTS idx_catalogo_etnias_activo 
ON catalogo_etnias(activo) WHERE activo = TRUE;

CREATE INDEX IF NOT EXISTS idx_catalogo_tipos_documento_activo 
ON catalogo_tipos_documento(activo) WHERE activo = TRUE;

CREATE INDEX IF NOT EXISTS idx_catalogo_niveles_educativo_activo 
ON catalogo_niveles_educativo(activo) WHERE activo = TRUE;

-- =============================================
-- 6. POLÍTICAS RLS (ROW LEVEL SECURITY)
-- =============================================

-- Habilitar RLS en todas las tablas de catálogos
ALTER TABLE catalogo_ocupaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE catalogo_etnias ENABLE ROW LEVEL SECURITY;
ALTER TABLE catalogo_tipos_documento ENABLE ROW LEVEL SECURITY;  
ALTER TABLE catalogo_niveles_educativo ENABLE ROW LEVEL SECURITY;

-- Política para service_role (backend) - acceso completo
CREATE POLICY service_role_full_access_ocupaciones ON catalogo_ocupaciones 
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY service_role_full_access_etnias ON catalogo_etnias
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY service_role_full_access_tipos_documento ON catalogo_tipos_documento
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY service_role_full_access_niveles_educativo ON catalogo_niveles_educativo
FOR ALL USING (auth.role() = 'service_role');

-- Política para authenticated users - solo lectura en catálogos activos
CREATE POLICY authenticated_read_ocupaciones ON catalogo_ocupaciones
FOR SELECT USING (auth.role() = 'authenticated' AND activo = TRUE);

CREATE POLICY authenticated_read_etnias ON catalogo_etnias  
FOR SELECT USING (auth.role() = 'authenticated' AND activo = TRUE);

CREATE POLICY authenticated_read_tipos_documento ON catalogo_tipos_documento
FOR SELECT USING (auth.role() = 'authenticated' AND activo = TRUE);

CREATE POLICY authenticated_read_niveles_educativo ON catalogo_niveles_educativo
FOR SELECT USING (auth.role() = 'authenticated' AND activo = TRUE);

-- =============================================
-- 7. VALIDACIONES Y CONSTRAINTS
-- =============================================

-- Constraint: códigos etnias válidos según DANE  
ALTER TABLE catalogo_etnias 
ADD CONSTRAINT check_codigo_etnia_valido 
CHECK (codigo_etnia BETWEEN 1 AND 99);

-- Constraint: códigos nivel educativo válidos
ALTER TABLE catalogo_niveles_educativo
ADD CONSTRAINT check_codigo_nivel_valido 
CHECK (codigo_nivel BETWEEN 1 AND 99);

-- Constraint: códigos documento válidos (formato estándar)
ALTER TABLE catalogo_tipos_documento
ADD CONSTRAINT check_codigo_documento_formato
CHECK (LENGTH(codigo_documento) BETWEEN 2 AND 5);

-- =============================================
-- 8. TRIGGERS PARA AUDITORÍA
-- =============================================

-- Trigger para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION actualizar_timestamp_catalogo()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas de catálogos
CREATE TRIGGER trigger_actualizar_timestamp_ocupaciones
    BEFORE UPDATE ON catalogo_ocupaciones
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp_catalogo();

CREATE TRIGGER trigger_actualizar_timestamp_etnias  
    BEFORE UPDATE ON catalogo_etnias
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp_catalogo();

CREATE TRIGGER trigger_actualizar_timestamp_tipos_documento
    BEFORE UPDATE ON catalogo_tipos_documento  
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp_catalogo();

CREATE TRIGGER trigger_actualizar_timestamp_niveles_educativo
    BEFORE UPDATE ON catalogo_niveles_educativo
    FOR EACH ROW EXECUTE FUNCTION actualizar_timestamp_catalogo();

-- =============================================
-- 9. VERIFICACIÓN FINAL
-- =============================================

-- Verificar que todas las tablas fueron creadas exitosamente
DO $verification$
DECLARE
    tabla_count INTEGER;
    registro_count INTEGER;
BEGIN
    -- Contar tablas creadas
    SELECT COUNT(*) INTO tabla_count
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('catalogo_ocupaciones', 'catalogo_etnias', 
                      'catalogo_tipos_documento', 'catalogo_niveles_educativo');
    
    -- Contar registros base insertados
    SELECT 
        (SELECT COUNT(*) FROM catalogo_etnias) +
        (SELECT COUNT(*) FROM catalogo_tipos_documento) + 
        (SELECT COUNT(*) FROM catalogo_niveles_educativo)
    INTO registro_count;
    
    -- Log resultados
    RAISE NOTICE '=== VERIFICACIÓN CATÁLOGOS CRÍTICOS ===';
    RAISE NOTICE 'Tablas catálogos creadas: % de 4', tabla_count;
    RAISE NOTICE 'Registros base insertados: %', registro_count;
    
    IF tabla_count = 4 THEN
        RAISE NOTICE '✅ SUCCESS: Todos los catálogos críticos creados exitosamente';
        RAISE NOTICE 'Prerequisito para variables PEDT válidas: COMPLETADO';
    ELSE
        RAISE EXCEPTION '❌ ERROR: Faltan catálogos por crear (% de 4)', tabla_count;
    END IF;
    
    RAISE NOTICE 'Próximo paso: Importar 10,919 ocupaciones desde CSV';
    RAISE NOTICE '===========================================';
END;
$verification$;

COMMIT;

-- =============================================
-- NOTAS PARA IMPLEMENTACIÓN
-- =============================================
/*
PRÓXIMOS PASOS REQUERIDOS:

1. IMPORTAR OCUPACIONES (10,919 registros):
   - Ejecutar script: importar_catalogos_202.py
   - Fuente: docs_IPS/resolucion_202_data/Tabla ocupaciones.csv
   
2. ACTUALIZAR TABLA PACIENTES:
   - Migración: agregar FK a catálogos
   - Script: migrar_pacientes_catalogos.py
   
3. ACTUALIZAR GENERADOR PEDT:
   - Modificar _calcular_variables_identificacion()
   - Implementar métodos _lookup_catalogo_*()
   
4. TESTING VALIDACIÓN:
   - test_catalogos_criticos.py
   - Validar variables PEDT con códigos reales
   
IMPACTO ESPERADO:
- Variables PEDT: de 10.1% hardcoded → 25% real válido
- Compliance Resolución 202: Significativamente mejorado  
- Reportes SISPRO: Códigos válidos vs. rechazados por defecto
*/