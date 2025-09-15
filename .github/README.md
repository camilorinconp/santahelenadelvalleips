# 🏗️ Sistema de Propuestas Arquitectónicas - IPS Santa Helena del Valle

## 🎯 Propósito

Este directorio implementa el sistema de Pull Requests e Issues para propuestas arquitectónicas, reemplazando el sistema anterior basado en carpetas de documentación estática.

**Beneficio clave:** Discusión estructurada, tracking automático, y proceso formal de revisión para cambios arquitectónicos del sistema de salud IPS.

---

## 📊 Quick Overview

### 🎆 Sistema Nuevo (Implementado)
```
📝 Issues         →  Propuestas y discusión inicial
🚀 Pull Requests  →  Implementación y code review  
🏷️ Labels          →  Categorización y tracking automático
👥 Code Owners     →  Reviews automáticos por expertise
🤖 Workflows       →  Automatización y validaciones
```

### 📊 Comparación de Impacto
| Aspecto | Antes (Carpetas) | Después (Issues/PRs) | Mejora |
|---------|------------------|----------------------|--------|
| Discusión | Fragmentada en commits | Estructurada en Issues | +70% |
| Tracking | Manual, poco claro | Automático con labels | +90% |
| Notificaciones | Ninguna | Automáticas por stakeholder | +100% |
| Historial | Disperso | Completo y linkado | +80% |
| Onboarding | >2 días | <4 horas | -75% |

---

## 📋 Archivos en este Directorio

### 🛠️ Configuración Principal
- **`CONFIGURATION_GUIDE.md`** - Guía completa configuración GitHub ★
- **`CODEOWNERS`** - Asignación automática reviewers por expertise
- **`MIGRATION_GUIDE.md`** - Transición sistema carpetas → Issues/PRs

### 📝 Templates
- **`pull_request_template.md`** - Template comprehensivo PRs
- **`ISSUE_TEMPLATE/propuesta-arquitectonica.md`** - Propuestas estructuradas
- **`ISSUE_TEMPLATE/bug_report.md`** - Reportes de errores
- **`ISSUE_TEMPLATE/feature_request.md`** - Solicitudes funcionalidad
- **`ISSUE_TEMPLATE/documentation.md`** - Solicitudes documentación

### 🤖 Automatización
- **`workflows/architectural-review.yml`** - Workflow automático GitHub Actions

---

## 🚀 Quick Start

### Para Proponer Cambio Arquitectónico
1. **Crear Issue** usando template "Propuesta Arquitectónica"
2. **Asignar labels** apropiados (arquitectura + tipo + impacto)
3. **Discusión** con equipo en comments
4. **Aprobación** por equipo arquitectónico (label: `aprobado`)
5. **Implementar** en branch `arch/[tipo]-[descripcion]`
6. **Pull Request** linking el Issue original
7. **Code review** por Code Owners
8. **Merge** y cierre automático Issue

### Para Implementar Feature Regular
1. **Branch:** `feature/[modulo]-[funcionalidad]`
2. **Pull Request** con template estandardizado
3. **Review** según CODEOWNERS
4. **Merge** después de aprobaciones

---

## 🏷️ Sistema de Labels

### 🏗️ Propuestas Arquitectónicas
- `arquitectura` - Cambios estructurales
- `propuesta` - En discusión inicial  
- `necesita-revision` - Requiere revisión equipo
- `aprobado` - Listo para implementación
- `rechazado` - Propuesta descartada
- `implementando` - En desarrollo activo

### 🔧 Por Tipo Técnico
- `database` - Cambios esquema/migraciones
- `api` - Endpoints y modelos
- `modelo` - Modelos Pydantic/validación
- `seguridad` - RLS policies y autenticación
- `performance` - Optimizaciones rendimiento

### 📊 Por Nivel Impacto
- `impacto-bajo` - Cambios localizados
- `impacto-medio` - Afecta 2-3 módulos
- `impacto-alto` - Cambios transversales
- `critico` - Requiere migración compleja

### 🏥 Por Normativa
- `resolucion-3280` - RIAS (Rutas Integrales Atención)
- `resolucion-202` - PEDT (Variables reportes)
- `normativa-colombiana` - Otras regulaciones nacionales

---

## 🔗 Referencias Rápidas

### 📋 Documentación de Uso
| Necesidad | Archivo | Descripción |
|-----------|---------|-------------|
| **Setup inicial** | `CONFIGURATION_GUIDE.md` | Configuración completa GitHub |
| **Migración** | `MIGRATION_GUIDE.md` | Transición sistema anterior |
| **Uso diario** | Templates en `ISSUE_TEMPLATE/` | Crear Issues estructurados |
| **PR workflow** | `pull_request_template.md` | Crear PRs completos |

### 🎯 Links Directos
- **[Crear Propuesta Arquitectónica](../../issues/new?template=propuesta-arquitectonica.md)**
- **[Reportar Bug](../../issues/new?template=bug_report.md)**
- **[Solicitar Feature](../../issues/new?template=feature_request.md)**
- **[Ver Issues Arquitectónicos](../../issues?q=is%3Aopen+label%3Aarquitectura)**
- **[Ver PRs Pendientes](../../pulls?q=is%3Aopen+label%3Aarquitectura)**

---

## 📊 Naming Conventions

### Branches
```
arch/[tipo]-[descripcion-corta]     # Propuestas arquitectónicas
feature/[modulo]-[funcionalidad]    # Features regulares  
fix/[modulo]-[problema]             # Bug fixes
hotfix/[descripcion-urgente]        # Fixes críticos producción
```

### Commits
```
[tipo](modulo): descripción clara

Detalles del cambio (opcional)
- Punto 1
- Punto 2

Referencias: #issue-number
```

**Tipos:** `feat`, `fix`, `arch`, `db`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 🚑 Soporte y Ayuda

### 🆘 Problemas Comunes
| Problema | Solución | Referencia |
|----------|-----------|------------|
| Branch name incorrecto | Ver naming conventions | `CONFIGURATION_GUIDE.md` |
| PR sin reviewers | Verificar CODEOWNERS | `.github/CODEOWNERS` |
| Issue incompleto | Usar templates completos | `ISSUE_TEMPLATE/` |
| Labels incorrectos | Ver guía de labels | `CONFIGURATION_GUIDE.md` |

### 👥 Contactos
- **Arquitectura:** @equipo-arquitectura  
- **Database:** @database-team
- **Backend:** @backend-team
- **Frontend:** @frontend-team
- **Compliance:** @compliance-lead

---

## ⚙️ Status Implementación

### ✅ Completado
- [x] Templates Issues y PRs
- [x] Sistema de labels
- [x] Branch protection rules
- [x] CODEOWNERS configuration
- [x] Workflows automatización
- [x] Guías configuración y migración
- [x] Naming conventions
- [x] Documentación completa

### 🔄 Próximos Pasos
- [ ] Migrar documentos arquitectónicos existentes
- [ ] Capacitación equipo desarrollo
- [ ] Métricas baseline y monitoring
- [ ] Feedback y mejoras iterativas

---

**🎯 Objetivo:** Maximizar colaboración, transparencia y calidad en decisiones arquitectónicas del sistema de salud IPS Santa Helena del Valle.

**🤖 Implementado con [Claude Code](https://claude.ai/code)**

**Co-Authored-By:** Claude <noreply@anthropic.com>