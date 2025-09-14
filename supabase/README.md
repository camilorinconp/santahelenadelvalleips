# 🗄️ Database - PostgreSQL + Supabase

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Proyecto:** IPS Santa Helena del Valle - Database Hub Central  
**📊 Estado:** 35 migraciones aplicadas, arquitectura transversal completa  

---

## 🚀 **Inicio Rápido - Database Navigation**

### **📖 Para Database Developers**
**👉 PUNTO DE ENTRADA:** [Database Overview Hub](docs/01-overview/database-overview.md) ⭐

### **📋 Quick Commands**
```bash
# Setup database local
supabase start && echo "Studio: http://127.0.0.1:54323"

# Crear nueva migración
supabase db diff -f descripcion_clara_cambio

# Aplicar migraciones
supabase db reset
```

---

## 🎯 **Navegación Especializada por Rol**

### 🛠️ **Database Developers** → [docs/02-migrations/](docs/02-migrations/)
- **Workflow migraciones** completo con templates SQL reutilizables
- **Troubleshooting** problemas CLI comunes (reset, repair)
- **Performance** optimization y indexing strategy

### 🏗️ **Database Architects** → [docs/03-architecture/](docs/03-architecture/)  
- **Polimorfismo anidado** diseño técnico detallado
- **RLS Security Model** comprehensive row-level security
- **Database evolution** strategy y future roadmap

### 📈 **Project Managers** → [docs/01-overview/](docs/01-overview/)
- **Database Overview** hub central con métricas y estado
- **Schema Evolution** historia completa por fases business
- **Roadmap Database** próximos hitos críticos con owners

### 🛠️ **DevOps Engineers** → [scripts/](scripts/)
- **Backup/Restore** automatización y disaster recovery  
- **Development Setup** configuración rápida nuevos devs
- **Migration Validation** pre-apply scripts y health checks

---

## 📊 **Database Status Dashboard**

### **✅ Completado (85%)**
- **Infraestructura:** Polimorfismo anidado operativo
- **RIAMP:** Materno-perinatal 100% funcional 
- **Security:** RLS policies todas las tablas
- **Transversal:** Entornos + Familia + Atención Integral

### **🚧 En Desarrollo (10%)**
- **Variables PEDT:** 60/119 operativas con catálogos
- **RPMS:** Primera infancia estructura base
- **Indicadores:** Triggers automáticos básicos

### **📋 Próximos Hitos (5%)**
- **Catálogos críticos:** Completion urgente ocupaciones + etnias
- **Audit logging:** Sistema auditoría enterprise
- **Performance Phase 2:** Optimization + monitoring

---

## 🧬 **Arquitectura Database Técnica**

### **Polimorfismo Anidado (2 Niveles)**
```sql
-- NIVEL 1: Discriminador Principal
atenciones { 
    tipo_atencion: text → detalle_id: uuid 
}

-- NIVEL 2: Discriminador Anidado (RIAMP)  
atencion_materno_perinatal { 
    sub_tipo_atencion: text → sub_detalle_id: uuid 
}

-- Detalles Específicos
detalle_control_prenatal { ... }
detalle_parto { ... }  
detalle_recien_nacido { ... }
detalle_puerperio { ... }
```

### **Estrategia Tipado (3 Capas)**
- **ENUMs PostgreSQL:** Valores pequeños estables
- **Tablas Catálogo + FKs:** Listas grandes dinámicas  
- **JSONB + TEXT:** Semi-estructurado + preparado IA/RAG

---

## 🌐 **Cross-Referencias Proyecto**

### **🔗 Integración Backend**
- **[FastAPI Models](../backend/docs/01-foundations/architecture-overview.md)** - Sincronización Pydantic ↔ PostgreSQL
- **[Compliance Guide](../backend/docs/02-regulations/resolucion-3280-master.md)** - Requirements normativos database

### **🔗 Integración Frontend**  
- **[React Integration](../frontend/docs/03-integration/backend-api-guide.md)** - TypeScript types database-derived
- **[Component Patterns](../frontend/docs/02-architecture/component-patterns.md)** - UI para datos polimórficos

---

## ⚡ **Database Performance Metrics**

- **Migration Success Rate:** 35/35 (100%) ✅
- **Schema Consistency:** Local ↔ Remote synced ✅  
- **Query Performance:** <100ms CRUD operations ✅
- **RLS Coverage:** 100% sensitive tables ✅
- **Compliance Coverage:** 85% Resolución 3280 ✅

---

## 🚨 **Critical Database Actions**

### **🟢 Health Indicators**
- Migraciones aplicadas exitosamente
- Schema sincronización completa
- RLS policies configuradas correctamente

### **🟡 Monitoring Required**
- Variables PEDT completion crítico
- Catálogos transversales setup
- Performance monitoring alerts

### **🔴 Urgent Actions** 
- **Ocupaciones:** Importar 10,919 registros CSV ⚠️
- **PEDT Variables:** Resolver 59 variables faltantes ⚠️

---

## 🤖 **Database Philosophy**

> **"PostgreSQL schema que evoluciona con normativa colombiana sin breaking changes"**

**Principios fundamentales:**
1. **Compliance normativo** como design constraint
2. **Polimorfismo anidado** escalabilidad sin refactoring  
3. **Security by design** RLS desde día 1
4. **Migration safety** rollback capability siempre

---

**🗄️ Database foundation sólida para sistema médico crítico**  
**👥 Maintained by:** Database Architecture Team  
**🎯 Next milestone:** Variables PEDT completas + RPMS primera infancia  
**📊 Success metric:** Zero refactoring para nuevas RIAS implementation