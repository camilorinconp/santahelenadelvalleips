# Claude Code - Supabase Database Configuration

## About This Project

Esta carpeta contiene toda la configuración y migraciones de la base de datos PostgreSQL gestionada por Supabase para el proyecto de la IPS Santa Helena del Valle. Es la fuente de la verdad para la estructura de la base de datos que soporta las Rutas Integrales de Atención en Salud (RIAS) según la Resolución 3280 de 2018.

## Architecture

### Database Strategy
La base de datos implementa un diseño híbrido que combina:

1. **Polimorfismo de Primer Nivel**: 
   - Tabla central `atenciones` con datos comunes
   - Tablas de detalle específicas por tipo de atención (`atencion_materno_perinatal`, `control_cronicidad`, etc.)

2. **Polimorfismo Anidado (Segundo Nivel)**:
   - Las tablas de detalle complejas se subdividen en sub-detalles
   - Ejemplo: `atencion_materno_perinatal` → `detalle_control_prenatal`, `detalle_parto`, `detalle_recien_nacido`, `detalle_puerperio`

3. **Estrategia de Tipado de Datos**:
   - **ENUMs de PostgreSQL**: Valores pequeños, estables y fijos
   - **Tablas de Catálogo con FKs**: Listas grandes, dinámicas o con metadatos
   - **JSONB**: Datos semi-estructurados de alta variabilidad
   - **TEXT**: Narrativas y contenido no estructurado (preparado para IA/RAG)

### Key Design Principles
- **Integridad Referencial**: UUIDs como claves primarias y foráneas
- **Auditabilidad**: Campos `creado_en` y `updated_at` en todas las tablas
- **Seguridad**: Row Level Security (RLS) habilitado en todas las tablas sensibles
- **Escalabilidad**: Diseño preparado para agregar nuevas RIAS sin modificar estructuras existentes

## Tech Stack

- **Database**: PostgreSQL 17
- **Platform**: Supabase
- **CLI Tool**: Supabase CLI
- **Migration System**: SQL migration files with version control
- **Security**: Row Level Security (RLS) policies

## Key Files

### Configuration
- `config.toml`: Supabase project configuration
- `migrations/`: All database schema changes as SQL files
- `DATABASE-STATUS.md`: Database context and workflow documentation

### Migration History
Las migraciones están organizadas cronológicamente y documentan la evolución del esquema:

#### Core Infrastructure (Sep 10, 2025)
- `20250910151835_remote_schema.sql`: Initial schema synchronization
- `20250910153701_schema_updates_polymorphic_and_cronicidad.sql`: Base polymorphic structure
- `20250910154446_fix_missing_columns_in_detail_tables.sql`: Column alignment fixes
- `20250910160224_set_default_timestamps.sql`: Timestamp standardization

#### Maternal-Perinatal Refinement (Sep 11, 2025)
- `20250911201521_refactor_materno_perinatal_polymorphic.sql`: Nested polymorphism implementation
- `20250911203635_refine_detalle_control_prenatal_types.sql`: Prenatal care granularity
- `20250911212257_refine_detalle_parto_granularity.sql`: Delivery details
- `20250911214315_refine_detalle_recien_nacido_granularity.sql`: Newborn care
- `20250911220753_refine_detalle_puerperio_granularity.sql`: Postpartum care
- `20250911222353_add_mp_missing_detail_tables.sql`: Additional MP detail tables

#### Security & Access (Sep 12, 2025)
- `20250912025908_add_rls_policy_to_pacientes.sql`: Patient table RLS
- `20250912030639_add_full_rls_policy_to_pacientes.sql`: Comprehensive patient policies
- `20250912195000_grant_service_role_permissions.sql`: Service role configuration

#### **Arquitectura Transversal - COMPLETADA (Sep 13, 2025)**
- `20250913000000_create_transversal_models_consolidated.sql`: **Tablas transversales completas**
- `20250913001000_fix_rls_entornos_development.sql`: RLS policies para entornos
- `20250913002000_fix_inconsistent_rls_configuration.sql`: **Limpieza RLS completa**
- `20250913003000_enable_rls_with_service_role_all_tables.sql`: Service role para todas las tablas
- `20250913004000_complete_rls_cleanup_and_reset.sql`: Reset y configuración uniforme
- `20250913005000_fix_entornos_rls_specifically.sql`: RLS específico para entornos

#### **Estado Actual: 30 Migraciones Aplicadas (Sep 13, 2025)**
- **Rango**: `20250910151835` → `20250913005000` 
- **Sincronización**: Local-Remoto COMPLETADA con `supabase db reset`
- **Problemas CLI**: Resueltos con reset manual y migration repair

## Database Schema Overview

### Core Tables
```sql
-- Main polymorphic table
atenciones (
  id uuid PRIMARY KEY,
  paciente_id uuid REFERENCES pacientes(id),
  medico_id uuid REFERENCES medicos(id),
  tipo_atencion text,  -- Discriminator field
  detalle_id uuid,     -- Polymorphic reference
  fecha_atencion timestamptz,
  creado_en timestamptz DEFAULT now()
)

-- Base entities
pacientes (id, tipo_documento, numero_documento, ...)
medicos (id, nombre, especialidad, ...)
```

### Maternal-Perinatal Care (Nested Polymorphism)
```sql
-- First level detail
atencion_materno_perinatal (
  id uuid PRIMARY KEY,
  sub_tipo_atencion text,    -- Second level discriminator
  sub_detalle_id uuid,       -- Second level polymorphic reference
  ...
)

-- Second level details
detalle_control_prenatal (id, campos_específicos_prenatal, ...)
detalle_parto (id, campos_específicos_parto, ...)
detalle_recien_nacido (id, campos_específicos_rn, ...)
detalle_puerperio (id, campos_específicos_puerperio, ...)
```

### **Arquitectura Transversal (COMPLETADA Sep 13, 2025)**
```sql
-- Entornos de Salud Pública (5 tipos)
entornos_salud_publica (
  id uuid PRIMARY KEY,
  codigo_identificacion_entorno_unico text UNIQUE,
  tipo_entorno tipo_entorno_salud_publica,  -- ENUM: 5 tipos
  descripcion_detallada_entorno text,
  actores_institucionales_involucrados jsonb,
  recursos_tecnicos_disponibles jsonb,
  ...
)

-- Familia Integral como Sujeto de Atención
familia_integral_salud_publica (
  id uuid PRIMARY KEY,
  codigo_identificacion_familia_unico text UNIQUE,
  tipo_estructura_familiar tipo_estructura_familiar_integral, -- ENUM: 5 tipos
  ciclo_vital_familiar ciclo_vital_familiar, -- ENUM: 7 etapas
  antecedentes_medicos_familiares jsonb,
  factores_riesgo_contextuales jsonb,
  ...
)

-- Atención Integral Transversal (Coordinación)
atencion_integral_transversal_salud (
  id uuid PRIMARY KEY,
  codigo_atencion_integral_unico text UNIQUE,
  tipo_abordaje_atencion tipo_abordaje_atencion_integral_salud, -- ENUM: 5 tipos
  modalidad_atencion modalidad_atencion_integral, -- ENUM: 5 modalidades
  nivel_complejidad_atencion nivel_complejidad_atencion_integral, -- ENUM: 4 niveles
  plan_intervencion_detallado jsonb,
  resultados_obtenidos_medicion jsonb,
  ...
)
```

### Chronic Disease Control
```sql
control_cronicidad (
  id uuid PRIMARY KEY,
  tipo_cronicidad text,      -- Diabetes, Hipertensión, ERC, Dislipidemia
  detalle_cronicidad_id uuid, -- Reference to specific control detail
  ...
)

-- Specific control tables
control_diabetes_detalles (id, hba1c, glucosa_ayunas, ...)
control_hipertension_detalles (id, presion_sistolica, diastolica, ...)
control_erc_detalles (id, creatinina, filtrado_glomerular, ...)
control_dislipidemia_detalles (id, colesterol_total, hdl, ldl, ...)
```

## Development Workflow

### Local Development
```bash
# Start local Supabase services
supabase start

# Access local dashboard
# Studio: http://127.0.0.1:54323
# API: http://127.0.0.1:54321

# View current status
supabase status
```

### Schema Changes
**📖 Consultar**: `/docs/02-DEVELOPMENT-WORKFLOW.md` para el flujo completo de migraciones

```bash
# Method 1: Generate diff from local changes
supabase db diff -f nombre_descriptivo_migracion

# Method 2: Write migration manually
# Create file: supabase/migrations/[timestamp]_description.sql

# Apply migrations locally
supabase db reset

# Validate migration  
supabase db lint

# IMPORTANTE: Seguir convenciones de nombres
# Formato: YYYYMMDD_HHMMSS_descripcion_clara.sql
# Ejemplo: 20241215_143000_add_riamp_control_prenatal_complete_fields.sql

### **Resolución de Problemas CLI (Sep 13, 2025)**
```bash
# Si CLI falla con conectividad (problema actual)
# Opción 1: Reset completo (RECOMENDADA)
supabase db reset  # ✅ Reconstruye local desde migraciones

# Opción 2: Reparar historial de migraciones
supabase migration repair --status applied [timestamp]

# Opción 3: SQL directo en Supabase Dashboard
# Ejecutar SQL manualmente y crear migración después
```
```

### Production Deployment
```bash
# Link to remote project (one-time setup)
supabase link --project-ref [project-id]

# Push migrations to production
supabase db push

# Verify remote schema
supabase db diff --linked
```

### RLS Policy Management
```sql
-- Enable RLS on all tables
ALTER TABLE nombre_tabla ENABLE ROW LEVEL SECURITY;

-- Create policies for different roles
CREATE POLICY "policy_name" ON tabla_name
FOR operation TO role
USING (condition)
WITH CHECK (condition);
```

## Important Considerations

### Data Consistency
- Always maintain synchronization between Pydantic models and database schema
- RLS policies must be properly configured before API deployment
- Use transactions for complex multi-table operations
- Validate foreign key relationships before deployment

### Migration Best Practices
**📖 Ver template completo**: `/docs/02-DEVELOPMENT-WORKFLOW.md` - Sección "Template de Migración"

1. **Descriptive Names**: Migration files should clearly describe their purpose
2. **Incremental Changes**: Each migration should be atomic and reversible
3. **Data Preservation**: Always consider existing data when modifying schemas
4. **Testing**: Validate migrations on local environment before production deployment
5. **Documentation**: Incluir comentarios explicativos en cada migración
6. **Rollback Instructions**: Documentar instrucciones de rollback en comentarios
7. **Compliance Check**: Verificar alineación con Resolución 3280 antes de aplicar

### Schema Cache Issues
- Supabase PostgREST sometimes caches schema information
- After applying migrations, may need to restart services if schema changes aren't reflected
- Local: `supabase stop && supabase start`
- Production: Pause/Resume project in Supabase dashboard

### Resolution 3280 Compliance
The database schema is designed to capture all data requirements specified in the Colombian health regulation:
- Granular data collection for each type of health attention
- Proper categorization using ENUMs aligned with regulatory standards
- Flexible JSONB fields for complex medical findings
- TEXT fields for narrative content and future AI integration

## Security Configuration

### RLS Policies
- All patient-related tables have RLS enabled
- Policies are configured to allow proper access based on user roles
- Anonymous access is limited to specific operations for development/testing
- Production policies should be more restrictive and role-based

### Data Privacy
- Patient data is protected through comprehensive RLS policies
- Audit trails maintained through timestamp fields
- Soft deletes preferred over hard deletes for data integrity
- Sensitive fields can be encrypted at application level if needed

## Communication Language

**IMPORTANTE**: Toda la comunicación con el asistente de IA debe realizarse en **español**. La base de datos contiene terminología médica específica del sistema de salud colombiano y todas las migraciones, comentarios y documentación deben mantenerse en español.

## Quick Start para Trabajo con Base de Datos

### **📋 Para comenzar inmediatamente:**
1. **Entender la arquitectura** (20 min):
   - `/docs/01-ARCHITECTURE-GUIDE.md` - Sección "Arquitectura de Datos"
   - Revisar diagrama de polimorfismo anidado
   - Entender estrategia de 3 capas de tipado (ENUMs, JSONB, TEXT)

2. **Setup y exploración** (15 min):
   ```bash
   supabase start && supabase status
   # Acceder a Studio: http://127.0.0.1:54323
   # Explorar esquema actual en Studio
   ```

3. **Revisar migraciones existentes** (20 min):
   - Ver archivos en `/supabase/migrations/` por orden cronológico
   - Entender evolución del esquema
   - Identificar patrones de naming y estructura

### **🎯 Para crear nuevas migraciones:**
- **Workflow completo**: `/docs/02-DEVELOPMENT-WORKFLOW.md` - Sección "Base de Datos y Migraciones"
- **Template**: Usar template de migración con comentarios descriptivos
- **Validación**: Siempre ejecutar `supabase db reset` después de crear migración

## Documentación de Referencia

### **📚 Documentación Principal**
- **`/docs/01-ARCHITECTURE-GUIDE.md`**: Arquitectura de datos y patrones polimórficos
- **`/docs/02-DEVELOPMENT-WORKFLOW.md`**: Flujo de migraciones y mejores prácticas  
- **`/docs/00-PROJECT-OVERVIEW.md`**: Estado actual del esquema y próximos cambios

### **🔗 Integración con Aplicación**
- **`backend/CLAUDE.md`**: Sincronización con modelos Pydantic
- **`frontend/CLAUDE.md`**: Tipos de datos para TypeScript
- **`docs/resolucion_3280_de_2018_limpio.md`**: Requerimientos normativos de datos

## Notes for AI Assistant

### **🗄️ Reglas de Base de Datos:**
- **RLS Obligatorio**: Verificar políticas en todas las tablas nuevas
- **Polimorfismo Consistente**: Seguir patrón establecido para nuevas RIAS
- **Tipado Estratégico**: Aplicar 3 capas (ENUMs, JSONB, TEXT) según el contexto
- **Compliance Check**: Validar contra Resolución 3280 antes de implementar
- **Testing Local**: Siempre probar migraciones localmente primero

### **📖 Referencias Obligatorias por Prioridad:**
1. **`docs/resolucion_3280_de_2018_limpio.md`** - Autoridad normativa para estructura de datos
2. **`/docs/01-ARCHITECTURE-GUIDE.md`** - Patrones arquitectónicos y decisiones técnicas  
3. **`backend/models/`** - Sincronización con modelos Pydantic actuales
4. **`/docs/02-DEVELOPMENT-WORKFLOW.md`** - Convenciones y template de migraciones

### **⚠️ Consideraciones Críticas:**
- **Cache de Schema**: Reiniciar servicios si cambios no se reflejan
- **Transacciones**: Operaciones multi-tabla deben ser atómicas
- **Backup Strategy**: Considerar rollback antes de cambios mayores
- **Performance**: Agregar índices para queries frecuentes en nuevas tablas