# 🏛️ ESTRATEGIA CATÁLOGOS CRÍTICOS - RESOLUCIÓN 202
## PREREQUISITO PARA VARIABLES PEDT VÁLIDAS

**📅 Fecha:** 13 septiembre 2025  
**🎯 Estado:** Estrategia definida - Implementación inmediata requerida  
**🔴 Criticidad:** MÁXIMA - Sin catálogos, compliance Res. 202 imposible  
**👥 Decisión:** Equipo Principal + validación Consultores Externos

---

## 🚨 **DESCUBRIMIENTO CRÍTICO**

### **PROBLEMA IDENTIFICADO:**
Durante análisis desarrollo híbrido se descubrió que **NINGÚN catálogo transversal existe** en la BD:

```
❌ catalogo_ocupaciones: NO EXISTE (10,919 registros necesarios)
❌ catalogo_etnias: NO EXISTE  
❌ catalogo_niveles_educativo: NO EXISTE
❌ catalogo_tipos_documento: NO EXISTE
❌ catalogo_departamentos: NO EXISTE
❌ catalogo_municipios: NO EXISTE
[... 12 catálogos críticos: TODOS NO EXISTEN]
```

### **IMPACTO EN VARIABLES PEDT:**
- **Variable 11 (Ocupación):** Usando 9999 (Sin información) - **INVÁLIDO**
- **Variable 10 (Etnia):** Usando 6 (Sin pertenencia) - **INVÁLIDO**  
- **Variable 2 (Tipo documento):** Hardcoded - **INVÁLIDO**
- **Variable 12 (Nivel educativo):** Hardcoded - **INVÁLIDO**

**Resultado:** Reportes SISPRO serán **RECHAZADOS** por validaciones automáticas SISPRO.

---

## 📊 **ANÁLISIS DE IMPACTO**

### **✅ DATOS FUENTE DISPONIBLES:**
- **Ocupaciones:** `docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv` - **10,919 registros** ✅
- **Etnias:** Disponible en archivos Resolución 202 ✅  
- **Documentos:** Especificado en normativa colombiana ✅
- **Niveles educativo:** Estándar DANE disponible ✅

### **❌ ESTADO ACTUAL BD:**
- **0 catálogos implementados**
- **Variables PEDT con valores por defecto inválidos**
- **Imposibilidad de validaciones normativas reales**
- **Reportes SISPRO no pasarán validación automática**

---

## 🎯 **ESTRATEGIA DE IMPLEMENTACIÓN**

### **FASE 1: CATÁLOGOS CRÍTICOS MÍNIMOS (DÍA 1-2)**

#### **🔴 PRIORIDAD MÁXIMA - Variables PEDT Identificación:**

**1. Catálogo Ocupaciones (Variable 11)**
```sql
CREATE TABLE catalogo_ocupaciones (
    codigo_ciuo VARCHAR(10) PRIMARY KEY,
    descripcion TEXT NOT NULL,
    categoria_principal VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT NOW()
);

-- Importar 10,919 registros desde CSV
COPY catalogo_ocupaciones(codigo_ciuo, descripcion) 
FROM 'docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv'
DELIMITER ';'
CSV HEADER;
```

**2. Catálogo Etnias (Variable 10)**
```sql
CREATE TABLE catalogo_etnias (
    codigo_etnia INTEGER PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    grupo_poblacional VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

-- Datos según DANE/Resolución 202
INSERT INTO catalogo_etnias VALUES
(1, 'Indígena', 'Grupos étnicos'),
(2, 'Rom (gitano)', 'Grupos étnicos'), 
(3, 'Raizal', 'Grupos étnicos'),
(4, 'Palenquero', 'Grupos étnicos'),
(5, 'Negro, mulato, afrodescendiente', 'Grupos étnicos'),
(6, 'Sin pertenencia étnica', 'General');
```

**3. Catálogo Tipos Documento (Variable 2)**
```sql
CREATE TABLE catalogo_tipos_documento (
    codigo_documento VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    aplica_menores BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO catalogo_tipos_documento VALUES
('RC', 'Registro Civil', TRUE),
('TI', 'Tarjeta de Identidad', TRUE),
('CC', 'Cédula de Ciudadanía', FALSE),
('CE', 'Cédula de Extranjería', FALSE),
('PA', 'Pasaporte', FALSE),
('MS', 'Menor Sin Identificación', TRUE);
```

**4. Catálogo Niveles Educativo (Variable 12)**
```sql
CREATE TABLE catalogo_niveles_educativo (
    codigo_nivel INTEGER PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    nivel_dane VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO catalogo_niveles_educativo VALUES
(1, 'Ninguno', 'Sin educación formal'),
(2, 'Preescolar', 'Educación inicial'),
(3, 'Básica primaria (1° - 5°)', 'Educación básica'),
(4, 'Básica secundaria (6° - 9°)', 'Educación básica'),
(5, 'Media académica o clásica (10° - 11°)', 'Educación media'),
(6, 'Media técnica (10° - 11°)', 'Educación media'),
(7, 'Normalista', 'Educación superior'),
(8, 'Técnica profesional', 'Educación superior'),
(9, 'Tecnológica', 'Educación superior'),
(10, 'Profesional', 'Educación superior'),
(11, 'Especialización', 'Postgrado'),
(12, 'Sin información', 'No determinado');
```

---

### **FASE 2: ACTUALIZACIÓN MODELO PACIENTES (DÍA 2)**

#### **Migración Referencias Catálogos:**

```sql
-- Agregar columnas FK a tabla pacientes
ALTER TABLE pacientes ADD COLUMN 
    ocupacion_codigo VARCHAR(10) REFERENCES catalogo_ocupaciones(codigo_ciuo),
    etnia_codigo INTEGER REFERENCES catalogo_etnias(codigo_etnia),
    nivel_educativo_codigo INTEGER REFERENCES catalogo_niveles_educativo(codigo_nivel);

-- Migrar datos existentes con valores válidos por defecto
UPDATE pacientes SET 
    ocupacion_codigo = '9999',  -- Sin información (debe existir en catálogo)
    etnia_codigo = 6,           -- Sin pertenencia étnica  
    nivel_educativo_codigo = 12; -- Sin información

-- Una vez migrado, remover columnas hardcoded viejas si existen
-- ALTER TABLE pacientes DROP COLUMN ocupacion_old;
```

---

### **FASE 3: ACTUALIZACIÓN GENERADOR PEDT (DÍA 2-3)**

#### **Implementar Lookups Reales:**

```python
# services/reporteria_pedt.py - Métodos nuevos

def _lookup_catalogo_ocupaciones(self, codigo_ciuo: str) -> str:
    """Lookup código ocupación en catálogo real"""
    try:
        result = self.db.table('catalogo_ocupaciones')\
            .select('codigo_ciuo')\
            .eq('codigo_ciuo', codigo_ciuo)\
            .eq('activo', True)\
            .execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]['codigo_ciuo']
        else:
            return '9999'  # Sin información - valor válido en catálogo
    except:
        return '9999'  # Fallback seguro

def _lookup_catalogo_etnias(self, codigo_etnia: int) -> int:
    """Lookup código etnia en catálogo real"""
    # Similar implementación...
    pass

# Actualizar método principal
def _calcular_variables_identificacion(self, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'var_0_tipo_registro': '1',
        'var_1_consecutivo': datos_paciente.get('numero_documento', ''),
        'var_2_tipo_identificacion': self._lookup_catalogo_tipos_documento(
            datos_paciente.get('tipo_documento')),
        'var_3_numero_identificacion': datos_paciente.get('numero_documento', ''),
        'var_4_primer_apellido': datos_paciente.get('primer_apellido', ''),
        'var_5_segundo_apellido': datos_paciente.get('segundo_apellido', ''),
        'var_6_primer_nombre': datos_paciente.get('primer_nombre', ''),
        'var_7_segundo_nombre': datos_paciente.get('segundo_nombre', ''),
        'var_8_fecha_nacimiento': self._formatear_fecha(datos_paciente.get('fecha_nacimiento')),
        'var_9_sexo': self._mapear_sexo(datos_paciente.get('genero')),
        
        # CAMBIOS CRÍTICOS - Usar catálogos reales:
        'var_10_pertenencia_etnica': self._lookup_catalogo_etnias(
            datos_paciente.get('etnia_codigo', 6)),
        'var_11_ocupacion': self._lookup_catalogo_ocupaciones(
            datos_paciente.get('ocupacion_codigo', '9999')),
        'var_12_nivel_educativo': self._lookup_catalogo_niveles_educativo(
            datos_paciente.get('nivel_educativo_codigo', 12)),
            
        'var_13_codigo_ips': datos_paciente.get('codigo_ips_primaria', '')
    }
```

---

## 🎯 **CRITERIOS DE ÉXITO**

### **Día 1-2 Completado Exitosamente:**
- ✅ **4 catálogos críticos creados** con estructura completa
- ✅ **11,000+ registros importados** desde archivos Resolución 202
- ✅ **Tabla pacientes actualizada** con referencias FK a catálogos
- ✅ **Datos existentes migrados** sin pérdida de información

### **Día 2-3 Validación:**
- ✅ **GeneradorReportePEDT actualizado** con lookups reales
- ✅ **Variables PEDT con códigos válidos** (no hardcoded)
- ✅ **Tests pasando** con datos catalogo-based
- ✅ **Reporte SISPRO mejorado** - códigos reales vs. valores por defecto

### **Validación Final:**
- ✅ **Variable 11:** Ocupaciones reales del catálogo (no 9999 por defecto)
- ✅ **Variable 10:** Etnias válidas según DANE (no 6 por defecto masivo)
- ✅ **Variables 2, 12:** Códigos normalizados y validables
- ✅ **Compliance mejorado:** De ~10% funcional a ~25% real y válido

---

## ⚠️ **RIESGOS E IMPEDIMENTOS**

### **🔴 RIESGO ALTO: Tiempo de importación**
**Descripción:** 10,919 ocupaciones pueden tardar en importarse  
**Mitigación:** Usar COPY bulk insert, no INSERT row-by-row  
**Plan B:** Importar ocupaciones más comunes primero (top 100)

### **🟡 RIESGO MEDIO: Compatibilidad datos existentes**
**Descripción:** Pacientes actuales pueden tener valores incompatibles  
**Mitigación:** Migración cuidadosa con valores por defecto válidos  
**Rollback:** Mantener columnas viejas hasta validación completa

### **🟡 RIESGO MEDIO: Validación SISPRO exacta**
**Descripción:** Códigos pueden no coincidir 100% con validador SISPRO  
**Mitigación:** Usar archivos oficiales Resolución 202 como fuente única  
**Validación:** Testing con archivo SISPRO real en ambiente de pruebas

---

## 📋 **ENTREGABLES Y VERIFICACIÓN**

### **Scripts de Implementación:**
```
/backend/migrations/
├── 20250913_001_crear_catalogos_criticos.sql
├── 20250913_002_importar_ocupaciones_202.sql  
├── 20250913_003_actualizar_pacientes_catalogos.sql
└── 20250913_004_validar_integridad_catalogos.sql

/backend/scripts/
├── importar_catalogos_202.py
├── validar_catalogos_integridad.py
└── test_catalogos_pedt.py
```

### **Testing de Validación:**
```python
# tests/test_catalogos_criticos.py
def test_ocupaciones_importadas():
    assert count_ocupaciones() == 10919
    
def test_variables_pedt_con_catalogos_reales():
    # Validar que variables usan códigos reales, no hardcoded
    variables = generador.generar_variables_119(paciente_id)
    assert variables['var_11_ocupacion'] != 9999  # Debe ser código real
    assert existe_en_catalogo_ocupaciones(variables['var_11_ocupacion'])
```

---

## ✅ **DECLARACIÓN DE COMPROMISO**

**📅 Fecha compromiso:** 13 septiembre 2025  
**⏰ Timeline:** Días 1-2 de Semana 2 (desarrollo híbrido)  
**🎯 Objetivo:** Catálogos críticos 100% funcionales antes de materno perinatal  
**📊 Métricas éxito:** Variables PEDT pasan de 10.1% hardcoded a 25% real y válido

**DECISIÓN ESTRATÉGICA:** Los catálogos son prerequisito ABSOLUTO para compliance real. No se procederá con materno perinatal hasta que catálogos estén implementados y validados.

**Esta estrategia transforma variables PEDT de "simulación con valores por defecto" a "compliance real con datos normativos válidos".**

---

**🏛️ CATÁLOGOS CRÍTICOS | 📅 13 SEPTIEMBRE 2025 | 🔴 IMPLEMENTACIÓN INMEDIATA**