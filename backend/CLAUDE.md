# Claude Code - Backend Configuration

## About This Project

Este es el backend de la IPS Santa Helena del Valle, una API REST desarrollada con FastAPI para gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana (Resolución 3280 de 2018).

## Architecture

### Core Concepts
- **Domain**: Sistema de salud colombiano con enfoque en RIAS (Rutas Integrales de Atención en Salud)
- **Pattern**: Polimorfismo anidado para manejo de diferentes tipos de atenciones médicas
- **Database**: PostgreSQL con Supabase como plataforma de gestión

### Database Strategy
El proyecto implementa una arquitectura polimórfica de datos con dos niveles:
1. **Tabla Principal**: `atenciones` contiene datos comunes a todas las atenciones
2. **Tablas de Detalle**: Cada tipo de atención tiene su tabla específica (ej: `atencion_materno_perinatal`, `control_cronicidad`)
3. **Polimorfismo Anidado**: Las tablas de detalle complejas se subdividen en sub-detalles (ej: `detalle_control_prenatal`, `detalle_parto`)

### Data Types Strategy
- **ENUMs**: Para listas de valores pequeñas, estables y fijas
- **Foreign Keys + Catalog Tables**: Para listas grandes, dinámicas o que requieren metadatos
- **JSONB**: Para datos semi-estructurados o de alta variabilidad
- **TEXT**: Para narrativas y datos no estructurados (preparado para IA/RAG)

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Supabase)
- **Validation**: Pydantic
- **Testing**: Pytest
- **Server**: Uvicorn

## Key Files

### Configuration
- `main.py`: Application entry point
- `database.py`: Database connection and configuration
- `.env`: Environment variables (not tracked)
- `requirements.txt`: Python dependencies

### Models
- `models/`: Pydantic models for data validation
  - `paciente_model.py`: Patient management
  - `atencion_model.py`: Base attention model
  - `atencion_materno_perinatal_model.py`: Maternal-perinatal care with nested polymorphism
  - `control_cronicidad_model.py`: Chronic disease control

### Routes
- `routes/`: FastAPI route definitions
  - `pacientes.py`: Patient CRUD operations
  - `atenciones.py`: General attention management
  - `atencion_materno_perinatal.py`: Maternal-perinatal specific routes

### Tests
- `tests/`: Comprehensive test suite using Pytest
  - All major functionalities have corresponding tests
  - Tests are self-contained and create/cleanup their own data

## Development Guidelines

### Code Organization
1. **Models First**: Always define Pydantic models before implementing routes
2. **Polymorphic Flow**: For specialized attentions:
   - Create record in detail table first
   - Get the detail_id
   - Create record in main `atenciones` table with reference
3. **Testing**: All new features must have corresponding tests

### Database Workflow
**📖 Consultar**: `/docs/02-DEVELOPMENT-WORKFLOW.md` para el flujo completo de desarrollo

1. Use Supabase CLI for migrations: `supabase db diff -f migration_name`
2. Apply locally: `supabase db reset` 
3. Deploy to production: `supabase db push`
4. Always verify RLS policies are properly configured
5. **Seguir convenciones**: Formato `YYYYMMDD_HHMMSS_descripcion_clara.sql`
6. **Validar migración**: Ejecutar tests después de cada migración

### Common Commands

```bash
# Setup
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Run tests
pytest -v

# Database migrations (from project root)
supabase db diff -f migration_name
supabase db push
```

## Important Considerations

### Resolution 3280 Compliance
This project strictly follows Colombian health regulations (Resolución 3280 de 2018). All data models, business logic, and workflows must align with these requirements. The document `docs/02-regulations/resolucion-3280-master.md` is the ultimate authority for implementation decisions.

### Architecture References

### **📚 Documentación Reorganizada (Lectura Obligatoria)**

**👉 PUNTO DE ENTRADA:** [Guía Arquitectónica Maestra](docs/01-foundations/architecture-overview.md) ⭐

### **📋 Por Propósito:**
- **`docs/01-foundations/`** - Fundamentos críticos y arquitectura completa
- **`docs/02-regulations/`** - Compliance normativo (Res. 3280, 202)  
- **`docs/03-architecture/`** - Decisiones estratégicas y perfiles duales
- **`docs/04-development/`** - Guías operativas día a día
- **`docs/05-logs/`** - Registros históricos y verificaciones

### **⚖️ Normatividad y Compliance**  
- **`docs/02-regulations/resolucion-3280-master.md`**: Documento normativo maestro
- **`docs/03-architecture/external-recommendations.md`**: Guía arquitectónica expertos

### **📋 Contexto Histórico y Lecciones**
- **`GEMINI.md`**: Contexto del polimorfismo de datos y estrategia inicial
- **`docs/04-development/lessons-learned.md`**: Lecciones aprendidas críticas
- **`docs/04-development/current-status.md`**: Estado actual y próximos pasos

### Database Synchronization
Always ensure synchronization between:
1. Pydantic models in Python
2. Database schema in Supabase
3. RLS policies for data access
4. Test fixtures and assertions

### Performance & Scalability
The nested polymorphic approach provides:
- Clean separation of concerns
- Scalable data model for future RIAS implementation
- Optimized queries through proper indexing
- Preparation for AI/RAG integration via strategic use of TEXT and JSONB fields

## Current Implementation Status

### ✅ Completed
- **Patient CRUD operations** - Fully operational
- **Primera Infancia (Early Childhood) complete** - 14/14 tests passing ⭐
  - EAD-3 (Abbreviated Development Scale) functional
  - ASQ-3 (Ages & Stages Questionnaire) implemented
  - Vertical architecture pattern established
  - Complete CRUD + specialized endpoints + statistics
- **Maternal-perinatal care** with nested polymorphism (Phase 1)
- **Database synchronization** - Models aligned with DB schema
- **Comprehensive test suite** - All critical paths covered

### 🚧 In Progress  
- **Deploy pending migrations** (2 ready: triggers fix)
- **Control Cronicidad implementation** using vertical pattern
- **Oncological Screening (Tamizaje Oncológico)** - Next RIAS module

### 📋 Planned
- **Remaining RIAS implementation** per Resolution 3280 using established vertical pattern
- **Dual profiles frontend** (Clinical + Call Center)
- **Advanced business logic and validation rules**  
- **Reporting and analytics endpoints**
- **User management and granular RLS policies**

### 📍 Current Checkpoint (Safe Return Point)
- **Commit**: `4e4b7fb` - Primera Infancia 100% functional
- **Status**: No technical debt, all systems operational
- **Next**: Deploy migrations + Control Cronicidad expansion

## Communication Language

**IMPORTANTE**: Toda la comunicación con el asistente de IA debe realizarse en **español**. El proyecto está completamente desarrollado en el contexto del sistema de salud colombiano y toda la documentación, terminología médica y comunicación debe mantenerse en español.

## Quick Start para Desarrolladores

### **📋 Para comenzar inmediatamente:**
1. **Leer documentación crítica** (30 min):
   - `docs/01-foundations/architecture-overview.md` - Guía maestra completa ⭐
   - `docs/02-regulations/resolucion-3280-master.md` - Normativa colombiana (crítico)
   - `docs/04-development/current-status.md` - Estado actual y contexto

2. **Setup del entorno** (15 min):
   ```bash
   cd backend && python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   cd ../supabase && supabase start
   cd ../backend && pytest -v  # Validar entorno
   ```

3. **Entender el polimorfismo** (15 min):
   - Revisar `models/atencion_materno_perinatal_model.py`
   - Ejecutar test específico: `pytest tests/test_atencion_materno_perinatal.py -v`

### **🎯 Para contribuir efectivamente:**
- **Workflow completo**: `docs/04-development/testing-guide.md`
- **Patrones arquitectónicos**: `docs/01-foundations/architecture-overview.md`
- **Templates de Issues/PRs**: `/.github/` (usar siempre)

## Notes for AI Assistant

### **📖 Referencias Obligatorias por Orden de Prioridad:**
1. **`docs/01-foundations/architecture-overview.md`** - Guía maestra y navegación completa ⭐
2. **`docs/02-regulations/resolucion-3280-master.md`** - Autoridad normativa definitiva  
3. **`docs/03-architecture/dual-profiles-strategy.md`** - Decisiones técnicas y patrones
4. **`docs/03-architecture/external-recommendations.md`** - Guía de arquitectura de datos

### **🔧 Reglas de Desarrollo:**
- **Compliance First**: Validar contra Resolución 3280 antes de implementar
- **Polimorfismo Anidado**: Seguir patrón establecido para nuevas RIAS
- **Estrategia de Tipado**: Mantener 3 capas (ENUMs, JSONB, TEXT)
- **Testing Obligatorio**: TDD para todas las funcionalidades nuevas
- **Español Exclusivo**: Toda comunicación y terminología en español colombiano