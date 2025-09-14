# 🗄️ Database Overview - PostgreSQL Medical System

**📅 Última actualización:** 14 septiembre 2025  
**📍 Versión:** v2.1 - Post reorganización documental  
**🎯 Propósito:** Hub central navegación database completa

---

## 🎯 **Resumen Ejecutivo Database**

La base de datos PostgreSQL de IPS Santa Helena del Valle implementa un **diseño polimórfico anidado** especializado para gestionar RIAS (Rutas Integrales de Atención en Salud) según Resolución 3280 de 2018, con arquitectura híbrida que combina escalabilidad técnica con compliance normativo colombiano.

**Estado actual:** 35 migraciones aplicadas, arquitectura transversal completa, polimorfismo anidado funcional, RLS security configurado.

**Fortaleza clave:** Diseño polimórfico permite agregar nuevas RIAS sin modificar estructura existente, garantizando escalabilidad normativa futura.

---

## 🗺️ **Mapa de Navegación Database**

### 📊 **Para Database Developers** → [docs/02-migrations/](../02-migrations/)
- **📋 [Migration Guide](../02-migrations/migration-guide.md)** - Workflow completo migraciones
- **📄 [Templates](../02-migrations/templates/)** - Templates SQL reutilizables
- **🔧 [Troubleshooting](../02-migrations/troubleshooting.md)** - Problemas CLI comunes

### 🏗️ **Para Database Architects** → [docs/03-architecture/](../03-architecture/)
- **🧬 [Polimorfismo Anidado](../03-architecture/polymorphic-design.md)** - Diseño técnico detallado
- **🛡️ [RLS Security Model](../03-architecture/rls-security-model.md)** - Row Level Security strategy
- **⚡ [Performance Optimization](../03-architecture/performance-optimization.md)** - Índices y queries

### 📈 **Para Project Managers** → [docs/01-overview/](.)
- **📈 [Schema Evolution](./schema-evolution.md)** - Historia evolución por fases
- **📊 [Database Status](#estado-actual-database)** - Métricas y estado actual
- **🎯 [Roadmap Database](#próximos-hitos-críticos)** - Próximas implementaciones

### 🛠️ **Para DevOps Engineers** → [scripts/](../../scripts/)
- **💾 [Backup Scripts](../../scripts/)** - Automatización backup/restore
- **⚡ [Dev Setup](../../scripts/)** - Setup desarrollo rápido
- **✅ [Migration Validator](../../scripts/)** - Validación pre-apply

---

## 🎯 **Arquitectura Database Técnica**

### **🧬 Polimorfismo Anidado (2 Niveles):**
```sql
-- NIVEL 1: Polimorfismo Principal
atenciones {
    id: uuid,
    tipo_atencion: text,           -- Discriminador nivel 1
    detalle_id: uuid,              -- Referencia polimórfica nivel 1
    paciente_id: uuid,
    fecha_atencion: timestamptz
}

-- NIVEL 2: Polimorfismo Anidado (ejemplo RIAMP)
atencion_materno_perinatal {
    id: uuid,
    sub_tipo_atencion: text,       -- Discriminador nivel 2
    sub_detalle_id: uuid,          -- Referencia polimórfica nivel 2
    numero_embarazo: int,
    fecha_ultimo_parto: date
}

-- NIVEL 2: Detalles Específicos
detalle_control_prenatal { id, semanas_gestacion, peso_gestante, ... }
detalle_parto { id, tipo_parto, duracion_trabajo_parto, ... }
detalle_recien_nacido { id, peso_nacimiento, apgar_1min, ... }
detalle_puerperio { id, estado_puerperio, lactancia_materna, ... }
```

### **📊 Estrategia de Tipado (3 Capas):**
```sql
-- CAPA 1: ENUMs PostgreSQL (valores pequeños, estables)
CREATE TYPE tipo_documento AS ENUM ('CC', 'TI', 'CE', 'PA', 'RC');
CREATE TYPE genero AS ENUM ('M', 'F', 'O');

-- CAPA 2: Tablas Catálogo + FKs (listas grandes, dinámicas)
catalogo_ocupaciones (codigo_ciuo, descripcion, categoria_principal)
catalogo_etnias (codigo_dane, descripcion, grupo_etnico)

-- CAPA 3: JSONB + TEXT (datos semi/no estructurados, preparado IA/RAG)
antecedentes_medicos_familiares: jsonb
plan_intervencion_detallado: jsonb
observaciones_clinicas: text
```

---

## 📊 **Estado Actual Database**

### **✅ Completado (85%):**
- **Infraestructura base:** Polimorfismo nivel 1 completo
- **RIAMP:** Polimorfismo anidado materno-perinatal 100%
- **Arquitectura transversal:** Entornos + Familia + Atención Integral
- **Security:** RLS policies configuradas todas las tablas
- **Catálogos críticos:** Ocupaciones, etnias, documentos, educación
- **Migration system:** 35 migraciones aplicadas exitosamente

### **🚧 En Desarrollo (10%):**
- **RPMS:** Primera infancia tablas base creadas, faltan detalles específicos
- **Control cronicidad:** Estructura base, faltan especializaciones
- **Tamizaje oncológico:** Pendiente implementación completa

### **📋 Pendiente (5%):**
- **Indicadores automatizados:** Triggers para cálculos metrics automáticos
- **Audit logging:** Sistema de auditoría completo
- **Data archival:** Estrategia archivado datos históricos

---

## 🎯 **Métricas Database Success**

### **Técnicas:**
- ✅ **Migraciones aplicadas:** 35/35 exitosas
- ✅ **Schema consistency:** 100% sincronizado local ↔ remoto
- ✅ **RLS coverage:** 100% tablas sensibles protegidas
- ✅ **Query performance:** <100ms operaciones CRUD básicas
- ✅ **Backup strategy:** Automated daily backups configurado

### **Funcionales:**
- ✅ **RIAMP polimorfismo:** 100% operativo nested polymorphism
- ✅ **Compliance Resolución 3280:** 85% campos requeridos capturados
- ⚠️ **Variables PEDT:** 60/119 variables funcionales con catálogos
- ✅ **Arquitectura transversal:** 100% operativa entornos + familia

### **Escalabilidad:**
- ✅ **Nuevas RIAS:** Arquitectura preparada sin refactoring
- ✅ **Data growth:** Partitioning strategy preparada
- ✅ **Performance:** Índices optimizados para queries frecuentes
- ✅ **Maintenance:** Zero-downtime migration capability

---

## 📈 **Database Evolution Timeline**

### **🏗️ FASE 1: Fundación (Sep 10, 2025)**
```sql
-- Migrations: 20250910151835 → 20250910162907
✅ Schema inicial sincronización
✅ Polimorfismo nivel 1 implementado  
✅ Tablas base pacientes + médicos
✅ Timestamp standardization
```

### **🏥 FASE 2: RIAMP Anidado (Sep 11, 2025)**
```sql
-- Migrations: 20250911201521 → 20250911224024  
✅ Polimorfismo anidado materno-perinatal
✅ 5 tablas detalle específicas RIAMP
✅ Granularidad control prenatal completa
✅ Gestión recién nacido + puerperio
```

### **🔒 FASE 3: Security & RLS (Sep 12, 2025)**
```sql
-- Migrations: 20250912025908 → 20250912200000
✅ RLS policies todas las tablas
✅ Service role permissions
✅ Development vs. production security
✅ Data access control granular
```

### **🌐 FASE 4: Arquitectura Transversal (Sep 13, 2025)**
```sql
-- Migrations: 20250913000000 → 20250913140001
✅ Entornos salud pública (5 tipos)
✅ Familia integral como sujeto
✅ Atención integral transversal
✅ Catálogos críticos (ocupaciones, etnias)
```

---

## 🚀 **Próximos Hitos Críticos**

### **🎯 Hito Inmediato (2 semanas):** Variables PEDT Completas
- Completar catálogos faltantes (niveles educativo, regímenes salud)
- Implementar triggers automáticos cálculo variables derivadas
- Testing exhaustivo 119 variables Resolución 202
- **Owner:** Database Team + Backend Integration

### **🎯 Hito Medio Plazo (1 mes):** RPMS Primera Infancia Completa  
- Implementar polimorfismo anidado primera infancia
- Tablas detalle valoración desarrollo, vacunación, crecimiento
- Indicadores automatizados primera infancia
- **Owner:** Database Architecture Team

### **🎯 Hito Largo Plazo (3 meses):** Sistema Completo Escalable
- Todas las RIAS implementadas (6 rutas completas)
- Sistema indicadores automatizado completo  
- Audit logging y data archival operational
- Performance optimization fase 2
- **Owner:** Full Database Team

---

## 🔧 **Quick Commands Database**

### **🚀 Setup Desarrollo:**
```bash
# Iniciar servicios Supabase locales
supabase start

# Verificar estado
supabase status

# Acceso rápido
echo "Studio: http://127.0.0.1:54323"
echo "API: http://127.0.0.1:54321"
```

### **📋 Workflow Migraciones:**
```bash
# Crear migración nueva
supabase db diff -f descripcion_clara_cambio

# Aplicar migraciones localmente  
supabase db reset

# Validar migración
supabase db lint

# Deploy a producción (cuidado!)
supabase db push
```

### **🔍 Debugging Database:**
```bash
# Ver logs en tiempo real
supabase logs -t db

# Conectar via psql directo
supabase db connect

# Backup schema completo
pg_dump [connection] > schema_backup.sql
```

---

## 📚 **Referencias Arquitectónicas**

### **🔗 Documentación Técnica:**
- **[Backend Models](../../../backend/models/)** - Sincronización Pydantic ↔ PostgreSQL
- **[Frontend Types](../../../frontend/docs/03-integration/backend-api-guide.md)** - TypeScript types derivados
- **[Resolución 3280](../../../backend/docs/02-regulations/resolucion-3280-master.md)** - Compliance requirements

### **📖 Documentación Database:**
- **[CLAUDE.md](../../CLAUDE.md)** - Configuración AI para database work
- **[GEMINI.md](../../GEMINI.md)** - Contexto histórico database workflow
- **[Migration Guide](../02-migrations/migration-guide.md)** - Workflow detallado migraciones

### **🌐 Referencias Externas:**
- **[Supabase Documentation](https://supabase.com/docs)** - Platform oficial docs
- **[PostgreSQL Manual](https://postgresql.org/docs/)** - Database engine reference
- **[RLS Best Practices](https://supabase.com/docs/guides/auth/row-level-security)** - Security patterns

---

## 🎯 **Database Philosophy**

> **"Estructura de datos que evoluciona con normativa colombiana sin breaking changes"**

**Principios fundamentales:**
1. **Compliance normativo** como constraint de diseño database
2. **Polimorfismo anidado** como estrategia escalabilidad sin refactoring
3. **Security by design** con RLS desde día 1
4. **Performance optimization** sin sacrificar flexibilidad normativa
5. **Migration safety** con rollback capability siempre disponible

---

## 📊 **Database Health Dashboard**

### **🟢 Healthy Indicators:**
- Migration aplicadas: 35/35 ✅
- RLS policies: 100% coverage ✅  
- Query performance: <100ms avg ✅
- Schema consistency: Local ↔ Remote synced ✅

### **🟡 Monitoring Indicators:**
- Variables PEDT: 60/119 implementadas ⚠️
- RPMS coverage: 40% completado ⚠️
- Audit logging: Basic level implementado ⚠️

### **🔴 Critical Actions:**
- Catálogos críticos: Completion urgente 🚨
- Performance monitoring: Setup automated alerts 🚨

---

**🗄️ Este hub evoluciona con cada milestone database**  
**👥 Mantenido por:** Database Architecture Team  
**🤖 Optimizado para:** Database Developer navigation + Project visibility  
**🎯 Objetivo:** Database foundation sólida para sistema médico crítico