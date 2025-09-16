# 🏗️ Guía Arquitectónica Maestra - IPS Santa Helena del Valle

**📅 Última actualización:** 13 septiembre 2025  
**📍 Versión:** v2.0 - Post reorganización documental  
**🎯 Propósito:** Hub central navegación arquitectónica completa

---

## 🎯 **Resumen Ejecutivo**

El proyecto IPS Santa Helena del Valle es un **sistema integral de gestión de RIAS** (Rutas Integrales de Atención en Salud) según Resolución 3280 de 2018, construido con arquitectura polimórfica anidada y estrategia de perfiles duales. 

**Estado actual:** 75% arquitectura completada, 30% funcionalidades operativas, enfoque crítico en compliance Resolución 202 de 2021 para reportería SISPRO automatizada.

**Fortaleza clave:** Base técnica sólida con polimorfismo de datos que permite escalabilidad normativa y funcional sin refactorizaciones mayores.

---

## 🗺️ **Mapa de Documentación por Propósito**

### 📋 **Compliance Normativo** → [docs/02-regulations/](../02-regulations/)
**Para:** Auditores, equipo médico, responsables compliance
- **⭐ [ANÁLISIS COMPLIANCE 3280](../02-regulations/compliance-analysis-3280.md)** - Articulación completa con normativa ⭐
- **🏛️ [Resolución 3280 Maestro](../02-regulations/resolucion-3280-master.md)** - Documento normativo definitivo
- **📊 [Estrategia Resolución 202](../02-regulations/resolucion-202-strategy.md)** - Desarrollo híbrido PEDT
- **🔍 [Análisis Completo 202](../02-regulations/resolucion-202-analysis.md)** - 540+ líneas análisis detallado
- **🏛️ [Estrategia Catálogos](../02-regulations/catalogs-strategy.md)** - Catálogos transversales críticos
- **👥 [Insights Consultores](../02-regulations/external-consultant-insights.md)** - Análisis equipo externo

### 🏗️ **Arquitectura Estratégica** → [docs/03-architecture/](../03-architecture/)
**Para:** Arquitectos, líderes técnicos, stakeholders estratégicos
- **👥 [Estrategia Perfiles Duales](../03-architecture/dual-profiles-strategy.md)** - Clínico + Call Center
- **📋 [Recomendaciones Expertas](../03-architecture/external-recommendations.md)** - Guía arquitectónica externa
- **🛣️ [Roadmap Perfiles Duales](../03-architecture/roadmap-dual-profiles.md)** - Cronograma implementación
- **🗺️ [Roadmap Estratégico](../03-architecture/strategic-roadmap.md)** - Análisis y hoja de ruta maestra

### 👨‍💻 **Guías Desarrollo** → [docs/04-development/](../04-development/)
**Para:** Desarrolladores activos, equipo técnico día a día
- **📚 [Lecciones Aprendidas](../04-development/lessons-learned.md)** - Mejores prácticas críticas
- **🧪 [Guía Testing](../04-development/testing-guide.md)** - Suite pruebas automatizadas
- **📊 [Estado Actual](../04-development/current-status.md)** - Progreso y próximos pasos
- **🏗️ [Framework Mejores Prácticas](../04-development/best-practices-framework.md)** - Metodología enterprise
- **⚙️ [Workflow de Desarrollo](../04-development/development-workflow.md)** - Flujo completo desarrollo

### 📜 **Registros Históricos** → [docs/05-logs/](../05-logs/)
**Para:** Referencias históricas, troubleshooting, auditorías
- **[Milestones](../05-logs/milestones/)** - Hitos importantes del proyecto
- **[Logs de Sesiones](../05-logs/session-logs/)** - Registros sesiones específicas
- **[Infraestructura](../05-logs/infrastructure/)** - Verificaciones técnicas

---

## 🚀 **Decisiones Arquitectónicas Clave**

### **1. 🧬 Polimorfismo Anidado**
**Decisión:** Arquitectura polimórfica con tablas base + detalles específicos  
**Impacto:** Escalabilidad normativa sin refactorizaciones  
**Documento:** [Contexto Polimorfismo](../../GEMINI.md) ⭐

### **2. 👥 Estrategia Perfiles Duales**  
**Decisión:** Backend unificado + frontends especializados (Clínico + Call Center)  
**Impacto:** Maximiza valor operativo por tipo usuario  
**Documento:** [Estrategia Perfiles Duales](../03-architecture/dual-profiles-strategy.md) ⭐

### **3. 🔄 Desarrollo Híbrido Resolución 202**
**Decisión:** Implementación incremental variables PEDT (no 119 campos físicos nuevos)  
**Impacto:** 90% reutilización arquitectura existente  
**Documento:** [Estrategia Resolución 202](../02-regulations/resolucion-202-strategy.md) ⭐

### **4. 🏛️ Arquitectura Transversal**
**Decisión:** Entornos + Familias + Atención Integral como base coordinación cuidados  
**Impacto:** Base sólida para escalamiento normativo completo  
**Documento:** [Recomendaciones Expertas](../03-architecture/external-recommendations.md)

### **5. 📊 Compliance-First Development**
**Decisión:** Resolución 3280 como autoridad técnica definitiva  
**Impacto:** Garantía cumplimiento normativo desde diseño  
**Documento:** [Resolución 3280 Maestro](../02-regulations/resolucion-3280-master.md) ⭐

---

## ⚡ **Inicio Rápido por Rol**

### **👨‍💻 Desarrollador Nuevo:**
1. **Contexto técnico:** [CLAUDE.md](../../CLAUDE.md) + [GEMINI.md](../../GEMINI.md)
2. **Lecciones críticas:** [Lecciones Aprendidas](../04-development/lessons-learned.md)
3. **Estado actual:** [Estado Actual](../04-development/current-status.md)
4. **Testing:** [Guía Testing](../04-development/testing-guide.md)

### **🏛️ Auditor/Compliance:**
1. **Normativa maestra:** [Resolución 3280](../02-regulations/resolucion-3280-master.md)
2. **Estado compliance:** [Estrategia Resolución 202](../02-regulations/resolucion-202-strategy.md)
3. **Análisis completo:** [Análisis 202](../02-regulations/resolucion-202-analysis.md)

### **🏗️ Arquitecto/Líder Técnico:**
1. **Visión estratégica:** [Estrategia Perfiles Duales](../03-architecture/dual-profiles-strategy.md)
2. **Recomendaciones:** [Recomendaciones Expertas](../03-architecture/external-recommendations.md)
3. **Contexto polimorfismo:** [GEMINI.md](../../GEMINI.md)

### **👔 Stakeholder/Gerencia:**
1. **Estrategia perfiles:** [Estrategia Perfiles Duales](../03-architecture/dual-profiles-strategy.md)
2. **Roadmap:** [Roadmap Perfiles Duales](../03-architecture/roadmap-dual-profiles.md)
3. **Estado actual:** [Estado Actual](../04-development/current-status.md)

---

## 🎯 **Stack Tecnológico**

### **Backend:**
- **Framework:** FastAPI + Pydantic
- **Base de Datos:** PostgreSQL + Supabase
- **Testing:** Pytest (95% cobertura)
- **Documentación:** Markdown + AI-optimized

### **Frontend (Proyectado):**
- **Clínico:** React + TypeScript + Material-UI
- **Call Center:** Interfaz especializada + CTI integration
- **Compartido:** APIs REST + Real-time updates

### **Arquitectura:**
- **Patrón:** Polimorfismo anidado
- **Seguridad:** RLS (Row Level Security)
- **Escalabilidad:** Microservicios preparado
- **Compliance:** Normativo-first development

---

## 📊 **Métricas de Éxito Actuales**

### **Técnicas:**
- ✅ **Cobertura tests:** 95% en áreas implementadas
- ✅ **Migraciones BD:** 34 aplicadas exitosamente
- ✅ **Response time:** <100ms operaciones CRUD
- ✅ **Documentación:** 11 docs especializados

### **Funcionales:**
- ✅ **RIAMP:** 85% estructura implementada
- ⚠️ **Variables PEDT:** 12/119 funcionales (en desarrollo)
- ⚠️ **Compliance 202:** Desarrollo híbrido en curso
- ❌ **Call Center:** 0% implementado (documentado 100%)

### **Normativas:**
- ✅ **Resolución 3280:** 60% campos capturados
- 🔄 **Resolución 202:** Análisis completo, implementación iniciada
- ✅ **Arquitectura:** 100% preparada para escalamiento

---

## 🔄 **Próximos Hitos Críticos**

### **🎯 Hito Inmediato (4 semanas):** Compliance Resolución 202
- Catálogos transversales críticos
- Variables PEDT funcionales (objetivo: 60/119)
- Capa reportería inteligente operativa

### **🎯 Hito Medio Plazo (3 meses):** Backend Consolidado  
- RIAMP 100% normativo
- Indicadores automatizados
- API completa para ambos perfiles

### **🎯 Hito Largo Plazo (6 meses):** Sistema Integral
- Frontend call center operativo
- RPMS completa (6 momentos curso vida)  
- Dashboard ejecutivo funcional

---

## 📚 **Referencias Críticas Externas**

- **[Repositorio Principal](../../)** - Código fuente completo
- **[Configuración AI](../../CLAUDE.md)** - Setup asistente técnico
- **[Contexto Histórico](../../GEMINI.md)** - Evolución arquitectónica
- **[Frontend](../../../frontend/)** - Interfaz usuario (en desarrollo)
- **[Base Datos](../../../supabase/)** - Migraciones y configuración

---

## 🎯 **Filosofía del Proyecto**

> **"Dos caras de una misma moneda: evento clínico y evento administrativo, unidos por datos compartidos pero con interfaces diferenciadas por tipo de usuario"**

**Principios fundamentales:**
1. **Compliance normativo** como restricción de diseño
2. **Polimorfismo** como estrategia de escalabilidad  
3. **Perfiles duales** como optimización operativa
4. **Documentación viva** como garantía de continuidad

---

**🔄 Este documento se actualiza con cada hito arquitectónico significativo**  
**👥 Mantenido por:** Equipo Técnico Principal  
**🤖 Optimizado para:** AI Assistant navigation + Human readability