# 🧬 Polymorphic Design - Arquitectura Técnica Detallada

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía técnica completa polimorfismo anidado y patterns arquitectónicos  
**📍 Audiencia:** Database Architects, Senior Backend Developers, Tech Leads  

---

## 🎯 **Filosofía Arquitectónica**

### **🧬 Polimorfismo como Solución Normativa:**
El sistema de salud colombiano (Resolución 3280 de 2018) define múltiples **Rutas Integrales de Atención en Salud (RIAS)** con estructuras de datos específicas pero superpuestas. El polimorfismo anidado resuelve esta complejidad manteniendo:

1. **Flexibilidad normativa:** Agregar nuevas RIAS sin refactoring
2. **Integridad referencial:** Relaciones FK correctas
3. **Performance queries:** Joins eficientes
4. **Compliance automático:** Estructura refleja normativa

---

## 🏗️ **Arquitectura Polimórfica (2 Niveles)**

### **📊 NIVEL 1: Polimorfismo Principal**

#### **Tabla Central: `atenciones`**
```sql
CREATE TABLE atenciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación básica
    paciente_id UUID NOT NULL REFERENCES pacientes(id),
    medico_id UUID REFERENCES medicos(id),
    
    -- 🧬 POLIMORFISMO NIVEL 1
    tipo_atencion TEXT NOT NULL,    -- Discriminador: 'materno_perinatal', 'control_cronicidad', 'rpms', etc.
    detalle_id UUID NOT NULL,       -- Referencia polimórfica a tabla específica
    
    -- Campos transversales
    fecha_atencion TIMESTAMPTZ NOT NULL,
    modalidad_atencion modalidad_atencion_enum DEFAULT 'presencial',
    duracion_minutos INTEGER,
    
    -- Auditoría
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);
```

#### **Patrón de Referencia Polimórfica:**
```sql
-- Ejemplo de resolución polimórfica
SELECT 
    a.id,
    a.tipo_atencion,
    a.fecha_atencion,
    
    -- Resolución condicional según tipo
    CASE a.tipo_atencion
        WHEN 'materno_perinatal' THEN (
            SELECT json_build_object(
                'numero_embarazo', amp.numero_embarazo,
                'sub_tipo', amp.sub_tipo_atencion
            )
            FROM atencion_materno_perinatal amp 
            WHERE amp.id = a.detalle_id
        )
        WHEN 'control_cronicidad' THEN (
            SELECT json_build_object(
                'tipo_cronicidad', cc.tipo_cronicidad,
                'estado_control', cc.estado_control
            )
            FROM control_cronicidad cc
            WHERE cc.id = a.detalle_id
        )
        ELSE NULL
    END as detalle_especifico
    
FROM atenciones a
WHERE a.paciente_id = $1;
```

### **📊 NIVEL 2: Polimorfismo Anidado (RIAMP)**

#### **Tabla Intermedia: `atencion_materno_perinatal`**
```sql
CREATE TABLE atencion_materno_perinatal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Referencia al nivel 1
    atencion_id UUID NOT NULL REFERENCES atenciones(id) ON DELETE CASCADE,
    
    -- 🧬 POLIMORFISMO NIVEL 2  
    sub_tipo_atencion TEXT NOT NULL,    -- 'control_prenatal', 'parto', 'recien_nacido', 'puerperio'
    sub_detalle_id UUID NOT NULL,       -- Referencia a tabla específica nivel 2
    
    -- Campos específicos materno-perinatales
    numero_embarazo INTEGER NOT NULL CHECK (numero_embarazo > 0),
    fecha_ultimo_parto DATE,
    edad_gestacional_semanas INTEGER CHECK (edad_gestacional_semanas BETWEEN 0 AND 50),
    
    -- Auditoría
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);
```

#### **Tablas Específicas Nivel 2:**
```sql
-- Control Prenatal Específico
CREATE TABLE detalle_control_prenatal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Campos específicos control prenatal
    semanas_gestacion INTEGER NOT NULL CHECK (semanas_gestacion BETWEEN 1 AND 42),
    peso_gestante DECIMAL(5,2) CHECK (peso_gestante > 0),
    presion_arterial_sistolica INTEGER CHECK (presion_arterial_sistolica BETWEEN 70 AND 250),
    presion_arterial_diastolica INTEGER CHECK (presion_arterial_diastolica BETWEEN 40 AND 150),
    altura_uterina DECIMAL(4,1) CHECK (altura_uterina > 0),
    presentacion_fetal presentacion_fetal_enum,
    frecuencia_cardiaca_fetal INTEGER CHECK (frecuencia_cardiaca_fetal BETWEEN 110 AND 180),
    
    -- Riesgos y observaciones
    riesgo_biopsicosocial riesgo_enum DEFAULT 'bajo',
    signos_alarma TEXT[],  -- Array de signos de alarma
    observaciones_clinicas TEXT,
    
    -- Plan de manejo
    proxima_cita DATE,
    indicaciones_especificas TEXT,
    
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Parto Específico  
CREATE TABLE detalle_parto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    tipo_parto tipo_parto_enum NOT NULL,
    duracion_trabajo_parto_horas DECIMAL(4,1),
    presentacion_final presentacion_fetal_enum,
    peso_recien_nacido DECIMAL(5,3) CHECK (peso_recien_nacido > 0),
    apgar_1_minuto INTEGER CHECK (apgar_1_minuto BETWEEN 0 AND 10),
    apgar_5_minutos INTEGER CHECK (apgar_5_minutos BETWEEN 0 AND 10),
    
    -- Complicaciones
    complicaciones_maternas TEXT[],
    complicaciones_perinatales TEXT[],
    requirio_cesarea BOOLEAN DEFAULT FALSE,
    motivo_cesarea TEXT,
    
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🔍 **Patterns de Consulta Avanzados**

### **🚀 Query Pattern: Nested Join Resolution**
```sql
-- Consulta completa con resolución de 2 niveles polimórficos
WITH atencion_completa AS (
    SELECT 
        a.id as atencion_id,
        a.tipo_atencion,
        a.fecha_atencion,
        a.detalle_id as nivel1_detalle_id,
        
        -- Datos paciente
        p.primer_nombre,
        p.primer_apellido,
        p.numero_documento,
        
        -- Datos médico
        m.nombre as medico_nombre,
        m.especialidad
        
    FROM atenciones a
    JOIN pacientes p ON a.paciente_id = p.id
    LEFT JOIN medicos m ON a.medico_id = m.id
    WHERE a.tipo_atencion = 'materno_perinatal'
),
detalle_materno_perinatal AS (
    SELECT 
        amp.id as amp_id,
        amp.atencion_id,
        amp.sub_tipo_atencion,
        amp.numero_embarazo,
        amp.edad_gestacional_semanas,
        amp.sub_detalle_id as nivel2_detalle_id
        
    FROM atencion_completa ac
    JOIN atencion_materno_perinatal amp ON amp.atencion_id = ac.atencion_id
)
SELECT 
    ac.*,
    dmp.numero_embarazo,
    dmp.sub_tipo_atencion,
    
    -- Resolución específica según sub_tipo
    CASE dmp.sub_tipo_atencion
        WHEN 'control_prenatal' THEN (
            SELECT json_build_object(
                'semanas_gestacion', dcp.semanas_gestacion,
                'peso_gestante', dcp.peso_gestante,
                'presion_sistolica', dcp.presion_arterial_sistolica,
                'presion_diastolica', dcp.presion_arterial_diastolica,
                'riesgo_biopsicosocial', dcp.riesgo_biopsicosocial,
                'proxima_cita', dcp.proxima_cita
            )
            FROM detalle_control_prenatal dcp
            WHERE dcp.id = dmp.nivel2_detalle_id
        )
        WHEN 'parto' THEN (
            SELECT json_build_object(
                'tipo_parto', dp.tipo_parto,
                'duracion_horas', dp.duracion_trabajo_parto_horas,
                'peso_recien_nacido', dp.peso_recien_nacido,
                'apgar_1min', dp.apgar_1_minuto,
                'apgar_5min', dp.apgar_5_minutos,
                'complicaciones', dp.complicaciones_maternas
            )
            FROM detalle_parto dp
            WHERE dp.id = dmp.nivel2_detalle_id
        )
        ELSE json_build_object('tipo', dmp.sub_tipo_atencion)
    END as detalle_clinico_especifico

FROM atencion_completa ac
JOIN detalle_materno_perinatal dmp ON dmp.atencion_id = ac.atencion_id
ORDER BY ac.fecha_atencion DESC;
```

### **📊 Query Pattern: Aggregation Across Polymorphic Types**
```sql
-- Estadísticas por tipo de atención polimórfica
SELECT 
    a.tipo_atencion,
    COUNT(*) as total_atenciones,
    COUNT(DISTINCT a.paciente_id) as pacientes_unicos,
    
    -- Sub-estadísticas para materno-perinatal
    COUNT(*) FILTER (
        WHERE a.tipo_atencion = 'materno_perinatal' 
        AND EXISTS (
            SELECT 1 FROM atencion_materno_perinatal amp 
            WHERE amp.atencion_id = a.id 
            AND amp.sub_tipo_atencion = 'control_prenatal'
        )
    ) as controles_prenatales,
    
    COUNT(*) FILTER (
        WHERE a.tipo_atencion = 'materno_perinatal' 
        AND EXISTS (
            SELECT 1 FROM atencion_materno_perinatal amp 
            WHERE amp.atencion_id = a.id 
            AND amp.sub_tipo_atencion = 'parto'
        )
    ) as partos_atendidos,
    
    -- Métricas temporales
    DATE_TRUNC('month', a.fecha_atencion) as mes_atencion,
    AVG(a.duracion_minutos) as duracion_promedio

FROM atenciones a
WHERE a.fecha_atencion >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY a.tipo_atencion, DATE_TRUNC('month', a.fecha_atencion)
ORDER BY mes_atencion DESC, total_atenciones DESC;
```

---

## 🎯 **Estrategias de Tipado por Capas**

### **🏷️ CAPA 1: PostgreSQL ENUMs (Valores Fijos)**
```sql
-- Para valores pequeños, estables, conocidos
CREATE TYPE modalidad_atencion_enum AS ENUM (
    'presencial',
    'telemedicina',
    'domiciliaria',
    'ambulatoria',
    'hospitalaria'
);

CREATE TYPE riesgo_enum AS ENUM (
    'bajo',
    'medio', 
    'alto',
    'critico'
);

CREATE TYPE tipo_parto_enum AS ENUM (
    'vaginal_normal',
    'vaginal_instrumental',
    'cesarea_programada',
    'cesarea_emergencia'
);
```

**Ventajas ENUMs:**
- Performance excepcional (almacenamiento compacto)
- Validación automática nivel database
- IntelliSense en queries
- Consistencia datos garantizada

**Cuándo usar:**
- Valores conocidos y estables (<20 opciones)
- No requieren metadata adicional
- Cambios infrecuentes

### **🏷️ CAPA 2: Tablas Catálogo + Foreign Keys**
```sql
-- Para listas grandes, dinámicas, con metadata
CREATE TABLE catalogo_ocupaciones (
    codigo_ciuo VARCHAR(10) PRIMARY KEY,
    descripcion TEXT NOT NULL,
    categoria_principal VARCHAR(100),
    grupo_ocupacional VARCHAR(50),
    requiere_formacion_especifica BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    
    -- Metadata adicional
    salario_promedio_mensual DECIMAL(12,2),
    demanda_laboral_nivel INTEGER CHECK (demanda_laboral_nivel BETWEEN 1 AND 5),
    
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Uso en tablas principales
CREATE TABLE pacientes (
    id UUID PRIMARY KEY,
    -- ... otros campos
    ocupacion_codigo_ciuo VARCHAR(10) REFERENCES catalogo_ocupaciones(codigo_ciuo),
    -- ... 
);
```

**Ventajas Catálogos:**
- Flexibilidad para agregar/modificar valores
- Metadata rica asociada
- Búsquedas complejas (full-text, filtros)
- Internacionalización posible

**Cuándo usar:**
- Listas grandes (>50 elementos)
- Requieren metadata adicional
- Cambios frecuentes o dinámicos
- Fuente externa (DANE, OMS, etc.)

### **🏷️ CAPA 3: JSONB + TEXT (Datos Semi-estructurados)**
```sql
-- Para datos variables, complejos, preparados para IA
CREATE TABLE detalle_control_prenatal (
    id UUID PRIMARY KEY,
    -- ... campos estructurados básicos
    
    -- JSONB para datos complejos variables
    antecedentes_medicos_detallados JSONB DEFAULT '{}',
    -- Estructura ejemplo:
    -- {
    --   "cardiovascular": {"hipertension": true, "fecha_diagnostico": "2023-01-15"},
    --   "diabetes": {"tipo": "gestacional", "controlada": true},
    --   "quirurgicos": [{"procedimiento": "apendicectomia", "fecha": "2020-03-10"}]
    -- }
    
    plan_manejo_personalizado JSONB DEFAULT '{}',
    -- Estructura ejemplo:
    -- {
    --   "medicamentos": [{"nombre": "acido_folico", "dosis": "400mcg", "frecuencia": "diario"}],
    --   "examenes": [{"tipo": "hemoglobina", "fecha_programada": "2025-10-15"}],
    --   "recomendaciones": ["aumentar_ingesta_hierro", "ejercicio_moderado_30min"]
    -- }
    
    -- TEXT para contenido narrativo (preparado IA/RAG)
    observaciones_clinicas TEXT,
    -- "Paciente refiere cefalea ocasional en región frontal, sin náuseas asociadas. 
    --  Movimientos fetales presentes y adecuados para edad gestacional. 
    --  Se observa edema leve en extremidades inferiores."
    
    notas_seguimiento TEXT
    -- "Plan: Continuar con suplementación férrica. Control en 4 semanas. 
    --  Educar sobre signos de alarma. Referir a nutricionista para plan alimentario."
);
```

**Ventajas JSONB/TEXT:**
- Máxima flexibilidad estructura datos
- Búsquedas dentro de JSON (GIN indexes)
- Preparado para procesamiento IA/NLP  
- Evolución schema sin migraciones

**Cuándo usar:**
- Datos altamente variables por registro
- Contenido narrativo médico
- Configuraciones personalizadas
- Datos destinados a análisis IA

---

## 🚀 **Performance Optimization Strategies**

### **📈 Indexing Strategy Polimórfica**
```sql
-- Índices para resolución polimórfica nivel 1
CREATE INDEX CONCURRENTLY idx_atenciones_tipo_detalle 
ON atenciones(tipo_atencion, detalle_id);

CREATE INDEX CONCURRENTLY idx_atenciones_paciente_fecha 
ON atenciones(paciente_id, fecha_atencion DESC);

-- Índices para resolución polimórfica nivel 2  
CREATE INDEX CONCURRENTLY idx_atencion_mp_sub_tipo_detalle
ON atencion_materno_perinatal(sub_tipo_atencion, sub_detalle_id);

CREATE INDEX CONCURRENTLY idx_atencion_mp_atencion_id
ON atencion_materno_perinatal(atencion_id);

-- Índices parciales para queries frecuentes
CREATE INDEX CONCURRENTLY idx_atenciones_mp_recientes
ON atenciones(fecha_atencion DESC, paciente_id)
WHERE tipo_atencion = 'materno_perinatal' 
AND fecha_atencion >= CURRENT_DATE - INTERVAL '6 months';

-- Índices JSONB para búsquedas complejas
CREATE INDEX CONCURRENTLY idx_control_prenatal_antecedentes_gin
ON detalle_control_prenatal USING GIN (antecedentes_medicos_detallados);

-- Índices funcionales para cálculos frecuentes
CREATE INDEX CONCURRENTLY idx_control_prenatal_semanas_trimestre
ON detalle_control_prenatal((
    CASE 
        WHEN semanas_gestacion <= 12 THEN 1
        WHEN semanas_gestacion <= 27 THEN 2
        ELSE 3
    END
));
```

### **📊 Materialized Views para Queries Complejas**
```sql
-- Vista materializada para dashboard materno-perinatal
CREATE MATERIALIZED VIEW dashboard_materno_perinatal AS
SELECT 
    p.id as paciente_id,
    p.primer_nombre,
    p.primer_apellido,
    p.numero_documento,
    p.fecha_nacimiento,
    
    -- Datos embarazo actual
    MAX(amp.numero_embarazo) as embarazo_actual,
    MAX(amp.edad_gestacional_semanas) as semanas_gestacion_actual,
    
    -- Estadísticas controles prenatales
    COUNT(*) FILTER (WHERE amp.sub_tipo_atencion = 'control_prenatal') as total_controles_prenatales,
    MAX(a.fecha_atencion) FILTER (WHERE amp.sub_tipo_atencion = 'control_prenatal') as ultimo_control_prenatal,
    
    -- Próxima cita programada
    MIN(dcp.proxima_cita) FILTER (WHERE dcp.proxima_cita > CURRENT_DATE) as proxima_cita_programada,
    
    -- Riesgo más alto identificado
    MAX(dcp.riesgo_biopsicosocial::text)::riesgo_enum as riesgo_maximo_identificado,
    
    -- Indicadores compliance
    COUNT(*) FILTER (WHERE amp.sub_tipo_atencion = 'control_prenatal') >= 
        CASE 
            WHEN MAX(amp.edad_gestacional_semanas) <= 12 THEN 1
            WHEN MAX(amp.edad_gestacional_semanas) <= 27 THEN 4  
            ELSE 7
        END as cumple_controles_minimos

FROM pacientes p
JOIN atenciones a ON a.paciente_id = p.id
JOIN atencion_materno_perinatal amp ON amp.atencion_id = a.id
LEFT JOIN detalle_control_prenatal dcp ON dcp.id = amp.sub_detalle_id 
    AND amp.sub_tipo_atencion = 'control_prenatal'

WHERE a.tipo_atencion = 'materno_perinatal'
AND a.fecha_atencion >= CURRENT_DATE - INTERVAL '12 months'

GROUP BY p.id, p.primer_nombre, p.primer_apellido, p.numero_documento, p.fecha_nacimiento;

-- Índices en vista materializada
CREATE UNIQUE INDEX idx_dashboard_mp_paciente_id ON dashboard_materno_perinatal(paciente_id);
CREATE INDEX idx_dashboard_mp_proxima_cita ON dashboard_materno_perinatal(proxima_cita_programada) 
WHERE proxima_cita_programada IS NOT NULL;
CREATE INDEX idx_dashboard_mp_riesgo_alto ON dashboard_materno_perinatal(riesgo_maximo_identificado)
WHERE riesgo_maximo_identificado IN ('alto', 'critico');

-- Refresh schedule (via cron o aplicación)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_materno_perinatal;
```

---

## 🔒 **Security Model Polimórfico**

### **🛡️ RLS Policies Anidadas**
```sql
-- Policy nivel 1: Tabla principal atenciones
CREATE POLICY "service_role_full_access_atenciones" ON atenciones
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "authenticated_read_own_center_atenciones" ON atenciones
FOR SELECT USING (
    auth.role() = 'authenticated' 
    AND EXISTS (
        SELECT 1 FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE m.id = medico_id
        AND u.centro_salud_id IN (
            SELECT cs.id FROM centro_salud cs
            JOIN usuario_centros uc ON uc.centro_salud_id = cs.id
            WHERE uc.usuario_id = auth.uid()
        )
    )
);

-- Policy nivel 2: Tablas específicas heredan seguridad del nivel 1
CREATE POLICY "service_role_full_access_atencion_mp" ON atencion_materno_perinatal
FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "authenticated_access_via_atencion_mp" ON atencion_materno_perinatal
FOR SELECT USING (
    auth.role() = 'authenticated'
    AND EXISTS (
        SELECT 1 FROM atenciones a
        WHERE a.id = atencion_id
        -- Hereda la policy de atenciones automáticamente
    )
);
```

### **🔐 Data Encryption para Campos Sensibles**
```sql
-- Función para encriptar/desencriptar datos sensibles
CREATE OR REPLACE FUNCTION encrypt_sensitive_data(data TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Usar pgcrypto extension
    RETURN encode(pgp_sym_encrypt(data, current_setting('app.encryption_key')), 'base64');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION decrypt_sensitive_data(encrypted_data TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(decode(encrypted_data, 'base64'), current_setting('app.encryption_key'));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Aplicar a campos específicos sensibles
ALTER TABLE detalle_control_prenatal 
ADD COLUMN observaciones_clinicas_encrypted TEXT;

-- Trigger para encriptar automáticamente
CREATE OR REPLACE FUNCTION trigger_encrypt_observaciones()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.observaciones_clinicas IS NOT NULL THEN
        NEW.observaciones_clinicas_encrypted = encrypt_sensitive_data(NEW.observaciones_clinicas);
        NEW.observaciones_clinicas = NULL;  -- Limpiar texto plano
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_encrypt_control_prenatal
    BEFORE INSERT OR UPDATE ON detalle_control_prenatal
    FOR EACH ROW 
    WHEN (NEW.observaciones_clinicas IS NOT NULL)
    EXECUTE FUNCTION trigger_encrypt_observaciones();
```

---

## 📋 **Migration Patterns para Polimorfismo**

### **🔄 Agregar Nuevo Tipo Polimórfico**
```sql
-- Template para agregar nueva RIAS (ejemplo: Primera Infancia)
BEGIN;

-- 1. Crear tabla nivel 1 para nueva RIAS
CREATE TABLE atencion_primera_infancia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    atencion_id UUID NOT NULL REFERENCES atenciones(id) ON DELETE CASCADE,
    
    -- Polimorfismo nivel 2 para primera infancia
    sub_tipo_atencion TEXT NOT NULL,  -- 'valoracion_desarrollo', 'vacunacion', 'crecimiento'
    sub_detalle_id UUID NOT NULL,
    
    -- Campos específicos primera infancia
    edad_meses INTEGER NOT NULL CHECK (edad_meses BETWEEN 0 AND 72),
    peso_actual DECIMAL(5,3) CHECK (peso_actual > 0),
    talla_actual DECIMAL(5,2) CHECK (talla_actual > 0),
    
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Crear tablas específicas nivel 2
CREATE TABLE detalle_valoracion_desarrollo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    area_lenguaje_puntaje INTEGER CHECK (area_lenguaje_puntaje BETWEEN 0 AND 100),
    area_motora_puntaje INTEGER CHECK (area_motora_puntaje BETWEEN 0 AND 100),
    area_social_puntaje INTEGER CHECK (area_social_puntaje BETWEEN 0 AND 100),
    area_cognitiva_puntaje INTEGER CHECK (area_cognitiva_puntaje BETWEEN 0 AND 100),
    
    desarrollo_adecuado BOOLEAN,
    requiere_estimulacion BOOLEAN DEFAULT FALSE,
    derivaciones_especializadas TEXT[],
    
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Actualizar constraints en tabla principal
-- Agregar nuevo tipo válido (si existe constraint)
ALTER TABLE atenciones DROP CONSTRAINT IF EXISTS check_tipo_atencion_valido;
ALTER TABLE atenciones ADD CONSTRAINT check_tipo_atencion_valido 
CHECK (tipo_atencion IN ('materno_perinatal', 'control_cronicidad', 'primera_infancia'));

-- 4. Crear índices específicos
CREATE INDEX idx_atencion_pi_sub_tipo ON atencion_primera_infancia(sub_tipo_atencion, sub_detalle_id);
CREATE INDEX idx_atencion_pi_edad ON atencion_primera_infancia(edad_meses);

-- 5. RLS policies
ALTER TABLE atencion_primera_infancia ENABLE ROW LEVEL SECURITY;
ALTER TABLE detalle_valoracion_desarrollo ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_full_access_atencion_pi" ON atencion_primera_infancia
FOR ALL USING (auth.role() = 'service_role');

-- 6. Actualizar vista materializada si existe
-- REFRESH MATERIALIZED VIEW dashboard_general;

COMMIT;
```

---

## 🎯 **Best Practices y Anti-patterns**

### **✅ Best Practices:**

1. **Consistencia Naming:**
   ```sql
   -- GOOD: Nombres descriptivos y consistentes
   atencion_materno_perinatal -> detalle_control_prenatal
   atencion_primera_infancia -> detalle_valoracion_desarrollo
   
   -- BAD: Nombres inconsistentes
   mp_data -> prenatal_info -> birth_details
   ```

2. **Constraints Robustos:**
   ```sql
   -- GOOD: Validaciones business logic
   CHECK (semanas_gestacion BETWEEN 1 AND 42)
   CHECK (peso_recien_nacido > 0 AND peso_recien_nacido < 10)
   
   -- BAD: Sin validaciones o muy permisivas
   peso_recien_nacido DECIMAL -- Permite valores negativos!
   ```

3. **Índices Estratégicos:**
   ```sql
   -- GOOD: Índices para resolución polimórfica
   CREATE INDEX ON tabla_nivel1(discriminador, referencia_polimorfica);
   
   -- BAD: Índices en todas las columnas (overkill)
   CREATE INDEX ON tabla(col1), ON tabla(col2), ON tabla(col3)...
   ```

### **❌ Anti-patterns a Evitar:**

1. **Polimorfismo Excesivo:**
   ```sql
   -- BAD: Más de 3 niveles polimórficos
   tabla_nivel1 -> tabla_nivel2 -> tabla_nivel3 -> tabla_nivel4
   
   -- GOOD: Máximo 2 niveles, usar JSONB para mayor granularidad
   tabla_nivel1 -> tabla_nivel2 + JSONB para detalles variables
   ```

2. **Referencias Polimórficas Sin Validación:**
   ```sql
   -- BAD: Sin constraints, permite referencias inválidas
   detalle_id UUID  -- Puede apuntar a cualquier tabla!
   
   -- GOOD: Validación via triggers o constraints
   CONSTRAINT check_valid_polymorphic_reference CHECK (
       CASE tipo_atencion 
           WHEN 'materno_perinatal' THEN EXISTS(SELECT 1 FROM atencion_materno_perinatal WHERE id = detalle_id)
           ELSE TRUE
       END
   )
   ```

3. **Queries N+1 en Resolución Polimórfica:**
   ```sql
   -- BAD: Query por cada resolución
   SELECT * FROM atenciones;  -- 100 filas
   -- Luego 100 queries adicionales para resolver cada detalle
   
   -- GOOD: Single query con JOINs o CTEs
   WITH resolucion_completa AS (...)
   SELECT ... FROM atenciones a JOIN resolucion_completa rc ON ...
   ```

---

## 📊 **Monitoring y Debugging**

### **📈 Métricas Polimórficas:**
```sql
-- Dashboard de salud polimórfico
SELECT 
    'Distribución por tipo' as metrica,
    tipo_atencion,
    COUNT(*) as total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as porcentaje
FROM atenciones 
WHERE fecha_atencion >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY tipo_atencion

UNION ALL

SELECT 
    'Resolución polimórfica válida' as metrica,
    tipo_atencion,
    COUNT(*) as total_registros,
    COUNT(*) - COUNT(CASE 
        WHEN tipo_atencion = 'materno_perinatal' 
        THEN (SELECT 1 FROM atencion_materno_perinatal WHERE id = detalle_id)
        WHEN tipo_atencion = 'control_cronicidad'
        THEN (SELECT 1 FROM control_cronicidad WHERE id = detalle_id)
        ELSE 1
    END) as referencias_rotas
FROM atenciones
GROUP BY tipo_atencion;
```

### **🔍 Debug Queries:**
```sql
-- Encontrar referencias polimórficas rotas
SELECT 
    a.id,
    a.tipo_atencion,
    a.detalle_id,
    'Referencia rota' as problema
FROM atenciones a
WHERE 
    (a.tipo_atencion = 'materno_perinatal' 
     AND NOT EXISTS (SELECT 1 FROM atencion_materno_perinatal WHERE id = a.detalle_id))
    OR
    (a.tipo_atencion = 'control_cronicidad'
     AND NOT EXISTS (SELECT 1 FROM control_cronicidad WHERE id = a.detalle_id));

-- Análisis performance polimórfico
EXPLAIN (ANALYZE, BUFFERS) 
SELECT a.*, amp.*, dcp.*
FROM atenciones a
JOIN atencion_materno_perinatal amp ON amp.atencion_id = a.id
JOIN detalle_control_prenatal dcp ON dcp.id = amp.sub_detalle_id
WHERE a.paciente_id = $1
AND a.tipo_atencion = 'materno_perinatal'
AND amp.sub_tipo_atencion = 'control_prenatal';
```

---

**🧬 Polimorfismo anidado como foundation escalable para compliance normativo**  
**👥 Maintained by:** Database Architecture Team  
**🎯 Evolution target:** 6 RIAS completas sin refactoring necesario  
**📊 Success metric:** <100ms resolución polimórfica completa + 100% integridad referencial