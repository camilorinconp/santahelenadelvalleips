# 🏗️ Guía de Arquitectura - Proyecto IPS Santa Helena del Valle

**Versión**: v1.0  
**Última actualización**: 12 de septiembre, 2025  
**Audiencia**: Desarrolladores, Arquitectos de Software, Equipo Técnico

## 📋 Tabla de Contenido

1. [Visión Arquitectónica](#visión-arquitectónica)
2. [Estrategia de Perfiles Duales](#estrategia-de-perfiles-duales) **[NUEVO]**
3. [Principios de Diseño](#principios-de-diseño)
4. [Arquitectura de Datos](#arquitectura-de-datos)
5. [Patrones Implementados](#patrones-implementados)
6. [Stack Tecnológico](#stack-tecnológico)
7. [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
8. [Seguridad y Compliance](#seguridad-y-compliance)
9. [Performance y Escalabilidad](#performance-y-escalabilidad)

---

## 🎯 Visión Arquitectónica

## 📊 Estrategia de Perfiles Duales

### **Arquitectura Multi-Perfil Integrada**

La plataforma implementa una **estrategia de perfiles duales** que atiende dos tipos de usuarios con **un backend unificado** y **frontends especializados**:

#### **PERFIL 1: Gestión Clínica Asistencial** 👨‍⚕️
- **Usuarios:** Médicos, enfermeras, profesionales de salud
- **Enfoque:** Atención médica directa, historia clínica, diagnósticos
- **Interface:** Frontend clínico con formularios especializados

#### **PERFIL 2: Gestión Administrativa Call Center** 📞
- **Usuarios:** Operadoras call center, coordinadores administrativos
- **Enfoque:** Atención inducida, seguimiento, cumplimiento normativo
- **Interface:** Frontend administrativo con dashboards y métricas

#### **Puntos de Integración:**
```
📋 FLUJO INTEGRADO:
Médico registra consulta → Sistema calcula próximo control → 
Call center recibe alerta → Contacta paciente → Programa cita → 
Ciclo se reinicia automáticamente

📈 DATOS COMPARTIDOS:
✓ Información del paciente sincronizada en tiempo real
✓ Citas y controles visibles para ambos perfiles  
✓ Métricas consolidadas para gestión gerencial
✓ Reportes unificados de cumplimiento normativo
```

**📚 Documentación Completa:** Ver [`docs/ESTRATEGIA_PERFILES_DUALES.md`](../backend/docs/ESTRATEGIA_PERFILES_DUALES.md)

---

### **Arquitectura Híbrida Multi-Capa**

El sistema implementa una arquitectura híbrida que combina:
- **Patrón MVC**: Separación clara entre modelos, vistas y controladores
- **Arquitectura por Capas**: Presentación, Lógica de Negocio, Datos
- **Microservicios Lógicos**: Separación funcional por dominios de salud
- **Event-Driven**: Para futuros desarrollos de notificaciones y alertas

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (SPA)                           │
│           React + TypeScript + Material-UI                 │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/REST API
┌─────────────────┴───────────────────────────────────────────┐
│                  BACKEND API                                │
│                FastAPI + Pydantic                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │   Models    │ │   Routes    │ │      Services       │   │
│  │ (Pydantic)  │ │ (FastAPI)   │ │   (Lógica Negocio) │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │ SQL/PostgreSQL
┌─────────────────┴───────────────────────────────────────────┐
│                 DATABASE LAYER                              │
│        PostgreSQL + Supabase (PostgREST + RLS)            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ Core Tables │ │Detail Tables│ │   Catalog Tables    │   │
│  │ (atenciones)│ │(polymorphic)│ │     (ENUMs)        │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Principios de Diseño

### **1. Compliance First**
> "Toda decisión arquitectónica debe estar alineada con la Resolución 3280 de 2018"

- **Validación normativa** en cada capa del sistema
- **Campos obligatorios** validados desde la base de datos hasta el frontend
- **Indicadores automáticos** calculados según especificaciones ministeriales

### **2. Polimorfismo Anidado**
> "Un modelo de datos que crece con la complejidad del dominio médico"

- **Primer Nivel**: `atenciones` → `atencion_materno_perinatal`, `control_cronicidad`
- **Segundo Nivel**: `atencion_materno_perinatal` → `detalle_control_prenatal`, `detalle_parto`
- **Flexibilidad**: Agregar nuevas RIAS sin modificar estructuras existentes

### **3. Separation of Concerns**
> "Cada componente tiene una responsabilidad clara y específica"

- **Models**: Validación de datos y reglas de negocio
- **Routes**: Exposición de APIs y manejo de requests/responses
- **Services**: Lógica de negocio compleja y orquestación
- **Database**: Persistencia e integridad referencial

### **4. Test-Driven Development**
> "La confianza en el sistema viene de sus pruebas"

- **90% cobertura** mínima para código crítico
- **Tests unitarios** para cada modelo y endpoint
- **Tests de integración** para flujos completos
- **Tests de compliance** para validación normativa

---

## 🗄️ Arquitectura de Datos

### **Estrategia de Tipado de Datos**

#### **Capa 1: Estandarización (ENUMs)**
```sql
-- Para valores pequeños, estables y fijos
CREATE TYPE tipo_parto_enum AS ENUM (
    'VAGINAL', 'CESAREA', 'INSTRUMENTAL'
);

CREATE TYPE riesgo_biopsicosocial_enum AS ENUM (
    'BAJO', 'MEDIO', 'ALTO'
);
```

**Cuándo usar**: Listas <= 10 elementos, valores que no cambian frecuentemente

#### **Capa 2: Semi-Estructurado (JSONB)**
```sql
-- Para datos complejos con estructura variable
signos_vitales_maternos JSONB DEFAULT '{
    "presion_sistolica": null,
    "presion_diastolica": null, 
    "frecuencia_cardiaca": null,
    "temperatura": null,
    "saturacion_oxigeno": null
}'::jsonb;

sintomas_preeclampsia JSONB DEFAULT '{
    "cefalea": false,
    "vision_borrosa": false,
    "epigastralgia": false,
    "edema_manos_cara": false
}'::jsonb;
```

**Cuándo usar**: Checklists, grupos de síntomas, datos que varían por protocolo

#### **Capa 3: Texto Libre (TEXT)**
```sql
-- Para narrativas médicas y contenido no estructurado
observaciones_clinicas TEXT,
plan_manejo TEXT,
recomendaciones_paciente TEXT
```

**Cuándo usar**: Notas médicas, observaciones, contenido para futura integración IA/RAG

### **Patrón Polimórfico Implementado**

```sql
-- Tabla principal (Primer Nivel)
CREATE TABLE atenciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID NOT NULL REFERENCES pacientes(id),
    medico_id UUID REFERENCES medicos(id),
    tipo_atencion TEXT NOT NULL, -- 'RIAMP', 'Control Cronicidad', etc.
    detalle_id UUID NOT NULL,    -- FK polimórfica
    fecha_atencion TIMESTAMPTZ NOT NULL,
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de detalle específica (Segundo Nivel)
CREATE TABLE atencion_materno_perinatal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sub_tipo_atencion TEXT, -- 'Control Prenatal', 'Parto', 'Puerperio'
    sub_detalle_id UUID,    -- FK al sub-detalle específico
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de sub-detalle (Tercer Nivel)
CREATE TABLE detalle_control_prenatal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    atencion_materno_perinatal_id UUID NOT NULL 
        REFERENCES atencion_materno_perinatal(id) ON DELETE CASCADE,
    -- 47+ campos específicos según Resolución 3280
    semanas_gestacion INTEGER,
    riesgo_biopsicosocial riesgo_biopsicosocial_enum,
    signos_vitales_maternos JSONB,
    resultados_paraclinicos JSONB,
    creado_en TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🔧 Patrones Implementados

### **1. Repository Pattern (Implícito)**
```python
# models/paciente_model.py
class Paciente(BaseModel):
    id: UUID4
    tipo_documento: TipoDocumentoEnum
    numero_documento: str
    
    @validator('numero_documento')
    def validate_numero_documento(cls, v, values):
        # Validaciones específicas por tipo de documento
        return v

# routes/pacientes.py  
@router.post("/", response_model=Paciente)
async def crear_paciente(paciente: PacienteCreate):
    # Lógica de creación centralizada
    return await create_paciente_service(paciente)
```

### **2. Factory Pattern (Para Atenciones Polimórficas)**
```python
class AtencionFactory:
    @staticmethod
    def create_atencion(tipo: str, data: dict):
        if tipo == "RIAMP":
            return create_atencion_materno_perinatal(data)
        elif tipo == "Control Cronicidad":
            return create_control_cronicidad(data)
        # ... otros tipos
        
    @staticmethod 
    def create_sub_atencion(sub_tipo: str, data: dict):
        if sub_tipo == "Control Prenatal":
            return create_detalle_control_prenatal(data)
        # ... otros sub-tipos
```

### **3. Strategy Pattern (Para Validaciones Específicas)**
```python
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data: dict) -> bool:
        pass

class PregnancyValidationStrategy(ValidationStrategy):
    def validate(self, data: dict) -> bool:
        # Validaciones específicas para embarazo
        semanas = data.get('semanas_gestacion')
        if semanas and (semanas < 4 or semanas > 42):
            raise ValueError("Semanas gestación fuera del rango válido")
        return True
```

### **4. Observer Pattern (Para Futuros Desarrollos)**
```python
# Preparado para sistema de notificaciones
class AtencionObserver:
    def __init__(self):
        self._observers = []
    
    def subscribe(self, observer):
        self._observers.append(observer)
    
    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

# Ejemplo de uso futuro:
# cuando se crea control prenatal → notificar siguiente cita
# cuando resultado crítico → alertar médico
```

---

## 🛠️ Stack Tecnológico

### **Backend Stack**
```python
# Core Framework
FastAPI==0.104.1          # API framework moderno y rápido
Pydantic==2.4.2          # Validación de datos y serialización
Uvicorn==0.24.0          # Servidor ASGI de alto rendimiento

# Database & ORM
asyncpg==0.29.0          # Driver PostgreSQL async
Supabase==2.7.4          # BaaS con PostgREST y realtime
SQLAlchemy==2.0.23       # ORM para queries complejas (futuro)

# Testing & Quality
pytest==7.4.3           # Framework de testing
pytest-asyncio==0.21.1  # Testing de código async
coverage==7.3.2          # Cobertura de código
ruff==0.1.6              # Linter y formatter ultrarrápido

# Security & Validation
python-jose==3.3.0       # JWT handling (futuro auth)
passlib==1.7.4          # Hashing de passwords (futuro auth)
```

### **Frontend Stack**
```json
{
  "core": {
    "react": "19.1.1",
    "typescript": "4.9.5",
    "react-router-dom": "7.8.2"
  },
  "ui": {
    "@mui/material": "7.3.2",
    "@emotion/react": "11.14.0",
    "@emotion/styled": "11.14.1"
  },
  "state": {
    "@tanstack/react-query": "5.87.4"
  },
  "forms": {
    "react-hook-form": "7.62.0",
    "zod": "4.1.5"
  },
  "http": {
    "axios": "1.11.0"
  }
}
```

### **Database & Infrastructure**
```yaml
database:
  engine: "PostgreSQL 17"
  platform: "Supabase"
  features:
    - "PostgREST auto-generated APIs"
    - "Row Level Security (RLS)"
    - "Real-time subscriptions"
    - "Automatic API documentation"

infrastructure:
  local_development:
    - "Supabase CLI"
    - "Docker containers"
    - "Local database with migrations"
  
  production:
    - "Supabase Cloud"
    - "Automatic backups"
    - "Global CDN"
    - "SSL certificates"
```

---

## 🔒 Seguridad y Compliance

### **Row Level Security (RLS)**
```sql
-- Ejemplo: Política para pacientes
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "pacientes_policy" ON pacientes
FOR ALL TO authenticated
USING (
    -- Solo médicos del mismo centro de salud
    auth.jwt() ->> 'centro_salud_id' = centro_salud_id::text
);

-- Política de desarrollo (temporal)
CREATE POLICY "Allow all for anon role on pacientes" ON pacientes
FOR ALL TO anon
USING (true) WITH CHECK (true);
```

### **Validación en Capas**
```python
# Capa 1: Base de datos (Constraints)
ALTER TABLE detalle_control_prenatal 
ADD CONSTRAINT check_semanas_gestacion 
CHECK (semanas_gestacion BETWEEN 4 AND 42);

# Capa 2: Pydantic Models (Business Logic)
class DetalleControlPrenatal(BaseModel):
    semanas_gestacion: int = Field(..., ge=4, le=42)
    
    @validator('riesgo_biopsicosocial')
    def validate_riesgo(cls, v, values):
        # Lógica compleja de validación según Resolución 3280
        return v

# Capa 3: Frontend (User Experience)
const validationSchema = z.object({
  semanasGestacion: z.number()
    .min(4, "Mínimo 4 semanas")
    .max(42, "Máximo 42 semanas")
});
```

### **Compliance Resolución 3280**
```python
# Decorador para validar compliance automáticamente
def validate_resolution_3280(required_fields: List[str]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = kwargs.get('data') or args[0]
            missing_fields = [
                field for field in required_fields 
                if not data.get(field)
            ]
            if missing_fields:
                raise ValueError(
                    f"Campos obligatorios faltantes según Resolución 3280: "
                    f"{missing_fields}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Uso en endpoints críticos
@validate_resolution_3280([
    'semanas_gestacion', 'riesgo_biopsicosocial', 
    'resultado_tamizaje_vih', 'hemoclasificacion'
])
async def create_control_prenatal(data: ControlPrenatalCreate):
    # Implementación
    pass
```

---

## 📈 Performance y Escalabilidad

### **Estrategias de Performance**

#### **Database Level**
```sql
-- Índices estratégicos para queries frecuentes
CREATE INDEX idx_atenciones_paciente_fecha 
ON atenciones(paciente_id, fecha_atencion DESC);

CREATE INDEX idx_control_prenatal_semanas 
ON detalle_control_prenatal(semanas_gestacion);

-- Índices parciales para consultas específicas
CREATE INDEX idx_gestantes_activas 
ON atencion_materno_perinatal(fecha_atencion) 
WHERE sub_tipo_atencion = 'Control Prenatal';
```

#### **API Level**
```python
# Paginación estándar
@router.get("/pacientes")
async def get_pacientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    return await get_pacientes_paginated(skip, limit)

# Caching para datos estáticos
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_codigos_rias():
    # Datos que cambian poco
    return await fetch_codigos_rias()
```

#### **Frontend Level**
```typescript
// Lazy loading de componentes
const AtencionesPage = lazy(() => import('./pages/AtencionesPage'));
const PacienteFormPage = lazy(() => import('./pages/PacienteFormPage'));

// Optimización de re-renders
const MemoizedPatientList = memo(({ patients }) => {
  return <PatientList patients={patients} />;
});

// Query optimization con React Query
const usePatients = (filters: PatientFilters) => {
  return useQuery({
    queryKey: ['patients', filters],
    queryFn: () => fetchPatients(filters),
    staleTime: 5 * 60 * 1000, // 5 minutos
    cacheTime: 10 * 60 * 1000, // 10 minutos
  });
};
```

### **Preparación para Escalabilidad**

#### **Horizontal Scaling (Futuro)**
- **Read Replicas**: Para queries de reportería
- **Connection Pooling**: PgBouncer para optimizar conexiones
- **CDN**: Para assets estáticos del frontend
- **Load Balancing**: Para múltiples instancias del API

#### **Vertical Optimization**
- **Query Optimization**: Análisis continuo de slow queries
- **Memory Management**: Configuración óptima de PostgreSQL
- **Caching Strategy**: Redis para sesiones y datos frecuentes

---

## 📊 Métricas y Monitoring

### **Métricas Técnicas**
```python
# Ejemplo de instrumentación
from prometheus_client import Counter, Histogram, start_http_server

# Contadores de requests
api_requests_total = Counter(
    'api_requests_total', 
    'Total API requests', 
    ['method', 'endpoint', 'status']
)

# Histogramas de latencia
api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration'
)
```

### **Métricas de Negocio**
- **Compliance Score**: % de campos obligatorios completos
- **Data Quality Score**: % de registros sin errores de validación  
- **Performance Score**: % de APIs respondiendo < 200ms
- **User Experience Score**: Tiempo promedio de completar formularios

---

## 🔄 Decisiones Arquitectónicas (ADRs)

### **ADR-001: PostgreSQL + Supabase**
**Status**: Aceptado  
**Decisión**: Usar Supabase como plataforma de base de datos  
**Contexto**: Necesidad de desarrollo rápido con capacidades enterprise  
**Consecuencias**: 
- ✅ Desarrollo acelerado
- ✅ RLS automático
- ✅ APIs generadas automáticamente
- ❌ Vendor lock-in potencial

### **ADR-002: Polimorfismo Anidado**  
**Status**: Aceptado  
**Decisión**: Implementar polimorfismo de 2 niveles para atenciones  
**Contexto**: Complejidad de RIAS según Resolución 3280  
**Consecuencias**:
- ✅ Escalabilidad para nuevas RIAS
- ✅ Flexibilidad en modelado de datos
- ❌ Complejidad en queries cross-table

### **ADR-003: FastAPI vs Django**
**Status**: Aceptado  
**Decisión**: FastAPI como framework principal  
**Contexto**: Performance y desarrollo moderno requeridos  
**Consecuencias**:
- ✅ Performance superior
- ✅ Documentación automática (OpenAPI)
- ✅ Typing nativo
- ❌ Ecosistema más pequeño que Django

---

## 🎯 Próximas Evoluciones Arquitectónicas

### **Corto Plazo (Q4 2024)**
- **Service Layer**: Extraer lógica de negocio de routes
- **Error Handling**: Middleware centralizado de manejo de errores
- **Logging**: Sistema estructurado de logs con correlación IDs

### **Medio Plazo (Q1-Q2 2025)**  
- **Authentication**: JWT + RBAC completo
- **Caching Layer**: Redis para performance
- **Background Jobs**: Celery para procesamiento asíncrono

### **Largo Plazo (Q3-Q4 2025)**
- **Event Sourcing**: Para auditoría completa
- **CQRS**: Separación de commands y queries
- **Microservices**: División por dominios médicos

---

**Última revisión**: 2025-09-12  
**Próxima revisión**: Final de Fase 1 (RIAMP completa)  
**Responsable**: Arquitecto Principal / Lead Developer