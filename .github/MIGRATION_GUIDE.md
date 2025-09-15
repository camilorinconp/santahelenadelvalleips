# 🔄 Guía de Migración: Sistema de Carpetas → Pull Requests/Issues

## 🎯 Propósito de la Migración

Esta guía documenta la transición del sistema basado en carpetas de documentación arquitectónica al sistema colaborativo de Pull Requests e Issues recomendado por el equipo consultor externo.

---

## 📊 Estado Antes de la Migración

### Sistema Anterior (Basado en Carpetas)

#### Ubicaciones de Documentación Arquitectónica
```
docs/
├── 01-foundations/
│   ├── architecture-overview.md          ✅ MANTENER (fundamental)
│   └── ...
├── 02-regulations/
│   ├── resolucion-3280-master.md         ✅ MANTENER (normativo)
│   ├── resolucion-202-analysis.md        ✅ MANTENER (compliance)
│   └── ...
├── 03-architecture/
│   ├── external-recommendations.md       🔄 MIGRAR (propuestas)
│   ├── dual-profiles-strategy.md        🔄 MIGRAR (decisiones)
│   ├── roadmap-dual-profiles.md         🔄 MIGRAR (planning)
│   └── catalogo-ocupaciones-dane-implementation.md  ✅ MANTENER (implementado)
└── 04-development/
    ├── current-status.md                 ✅ MANTENER (operativo)
    └── ...
```

#### Problemas Identificados
1. **Discusión fragmentada** - Decisiones en commits sin contexto
2. **No hay proceso de revisión formal** - Cambios arquitectónicos sin aprobación
3. **Difícil tracking** - Estado de propuestas poco claro
4. **Sin notificaciones** - Stakeholders no informados de cambios
5. **Historial disperso** - Lógica de decisiones perdida

---

## 🎆 Sistema Nuevo (Pull Requests + Issues)

### Estructura del Nuevo Sistema

#### 1. Issues para Propuestas Iniciales
```
GitHub Issues con Labels:
├── 🏷️ arquitectura + propuesta + necesita-revision
├── 🏷️ database/api/modelo/performance (tipo)
├── 🏷️ impacto-bajo/medio/alto/critico (nivel)
└── 🏷️ resolucion-3280/202 (normativa)
```

#### 2. Pull Requests para Implementación
```
PRs Linkados a Issues:
├── Branch: arch/[tipo]-[descripcion]
├── Template comprehensive PR
├── Code Owners auto-asignados
└── Reviews requeridos (1-2 aprobaciones)
```

#### 3. Documentación Híbrida
```
Combinación Optimizada:
├── 📁 docs/ (documentación estática fundamental)
│   ├── 01-foundations/ (arquitectura base)
│   ├── 02-regulations/ (normativas fijas)
│   └── 04-development/ (guías operativas)
├── 📝 Issues (propuestas y discusión dinámica)
└── 🚀 PRs (implementación y revisión código)
```

---

## 🔄 Plan de Migración

### Fase 1: Setup Básico (COMPLETADO ✅)
- [x] Crear templates de Issues y PRs
- [x] Configurar labels de categorización
- [x] Establecer branch protection rules
- [x] Definir naming conventions
- [x] Crear CODEOWNERS
- [x] Implementar workflow de automatización

### Fase 2: Migración de Contenido (EN PROGRESO ⚙️)

#### Documentos para Migrar a Issues

##### Issue #1: Estrategia Dual Profiles
**Migrar:** `docs/03-architecture/dual-profiles-strategy.md`
**Tipo:** Propuesta arquitectónica aprobada (documentar decisión)
**Labels:** `arquitectura`, `aprobado`, `database`, `impacto-alto`
**Estado:** Para crear como Issue de referencia histórica

##### Issue #2: Roadmap Dual Profiles  
**Migrar:** `docs/03-architecture/roadmap-dual-profiles.md`
**Tipo:** Plan de implementación
**Labels:** `arquitectura`, `planning`, `impacto-alto`
**Estado:** Para crear como Issue de seguimiento

##### Issue #3: Recomendaciones Equipo Externo
**Migrar:** `docs/03-architecture/external-recommendations.md`
**Tipo:** Propuesta de proceso (ya implementada)
**Labels:** `arquitectura`, `aprobado`, `proceso`
**Estado:** Issue de referencia para esta migración

#### Documentos que Permanecen en Carpetas
- `docs/01-foundations/` - Arquitectura fundamental (referencia estática)
- `docs/02-regulations/` - Normativas colombianas (compliance fijo)
- `docs/04-development/` - Guías operativas (proceso estable)
- Implementaciones completadas (ej: `catalogo-ocupaciones-dane-implementation.md`)

### Fase 3: Capacitación y Adopción
- [ ] Documentar ejemplos de uso
- [ ] Capacitar al equipo en nuevo flujo
- [ ] Definir métricas de éxito
- [ ] Establecer proceso de retroalimentación

---

## 📋 Template de Migración

### Para Convertir Documento Arquitectónico en Issue

#### 1. Crear Issue con Template "Propuesta Arquitectónica"
```markdown
Tipo: [ ] Migración de documentación existente
Título: [MIGRADO] [Original-Document-Name]

Contexto: 
Este issue migra la documentación existente de [ruta-archivo] 
al nuevo sistema colaborativo de Issues/PRs.

Decisión Original:
[Copiar contenido relevante del documento original]

Estado Actual:
[Especificar si ya fue implementado, está pendiente, etc.]
```

#### 2. Asignar Labels Apropiados
```
Labels de Migración:
- "arquitectura" (siempre)
- "migrado" (identificar contenido migrado)
- "aprobado" (si ya fue implementado)
- Tipo específico (database/api/modelo/etc)
- Nivel de impacto (bajo/medio/alto/critico)
```

#### 3. Linking y Referencias
```markdown
Documento Original: docs/ruta/archivo.md
Fecha Migración: [fecha]
Razón Migración: Adopción sistema colaborativo

Referencias:
- Issue #XX (si hay issues relacionados)
- PR #XX (si ya fue implementado)
```

---

## 📊 Beneficios de la Migración

### Antes vs Después

#### **Sistema de Carpetas (Anterior)**
- Documentos estáticos
- Sin discusión estructurada
- Cambios no auditables
- Sin notificaciones de cambios
- Difícil encontrar lógica de decisiones
- No hay proceso de aprobación

#### **Sistema Issues/PRs (Nuevo)**
- ✅ **Discusión estructurada** en Issues
- ✅ **Historial completo** de decisiones
- ✅ **Notificaciones automáticas** a stakeholders
- ✅ **Proceso formal** de revisión y aprobación
- ✅ **Linking automático** Issues ↔️ PRs ↔️ Código
- ✅ **Métricas** de productividad y calidad
- ✅ **Buscabilidad** mejorada con labels y filters

### Impacto Esperado
- **+50% velocidad** en comunicación de decisiones arquitectónicas
- **+70% transparencia** en proceso de desarrollo
- **+90% tracking** de estado de propuestas
- **-60% tiempo** onboarding nuevos desarrolladores
- **+80% participación** del equipo en decisiones arquitectónicas

---

## ⚙️ Configuración Post-Migración

### Actualizaciones Necesarias

#### 1. Actualizar Referencias en CLAUDE.md
```markdown
# Antes
- Ver `docs/03-architecture/dual-profiles-strategy.md`

# Después  
- Ver Issue #123: Estrategia Dual Profiles
- Implementación: PR #456
```

#### 2. Crear Issue de Seguimiento
**Titulo:** [META] Tracking Migración Sistema Carpetas → Issues/PRs
**Contenido:** Checklist de todos los documentos migrados
**Labels:** `arquitectura`, `meta`, `migracion`

#### 3. Actualizar Documentación de Onboarding
- Modificar guías para referenciar nuevo sistema
- Actualizar quick start guides
- Crear ejemplos de uso del nuevo flujo

### Métricas de Éxito

#### KPIs a Monitorear
- **Issues arquitectónicos creados/mes**
- **Tiempo promedio Issue → PR**
- **Número de participantes en discusiones**
- **PRs con reviews arquitectónicos completos**
- **Satisfacción del equipo** (encuesta mensual)

---

## 📋 Checklist de Migración

### Para el Equipo de Implementación

#### Setup Técnico (Completado ✅)
- [x] Templates de Issues creados
- [x] Template de PR actualizado
- [x] Labels configurados
- [x] CODEOWNERS establecido
- [x] Branch protection rules
- [x] Workflow de automatización
- [x] Guía de configuración

#### Migración de Contenido (En Progreso ⚙️)
- [ ] Issue #1: Migrar dual-profiles-strategy.md
- [ ] Issue #2: Migrar roadmap-dual-profiles.md 
- [ ] Issue #3: Migrar external-recommendations.md
- [ ] Crear Issue meta de tracking
- [ ] Actualizar referencias en CLAUDE.md
- [ ] Actualizar documentación de onboarding

#### Capacitación y Adopción (Pendiente)
- [ ] Demo del nuevo flujo para el equipo
- [ ] Crear issue de ejemplo
- [ ] Crear PR de ejemplo
- [ ] Definir schedule de revisión arquitectónica
- [ ] Establecer métricas baseline

### Para el Equipo de Desarrollo

#### Familiarización (Obligatorio)
- [ ] Leer esta guía completa
- [ ] Revisar templates de Issues y PRs
- [ ] Entender naming conventions
- [ ] Practicar creación de Issue arquitectónico
- [ ] Practicar creación de PR con branch arch/*

#### Adopción del Nuevo Flujo
- [ ] Usar nuevo sistema para próximas propuestas
- [ ] Participar en discusiones de Issues arquitectónicos
- [ ] Dar feedback sobre el proceso
- [ ] Reportar problemas o mejoras sugeridas

---

## 🎆 Ejemplos Prácticos

### Ejemplo 1: Propuesta Nueva Funcionalidad
```
1. 📁 Crear Issue con template "Propuesta Arquitectónica"
2. 🏷️ Labels: arquitectura, api, impacto-medio, feature-request
3. 💬 Discusión con equipo en comments
4. ✅ Equipo arquitectónico label: "aprobado"
5. 🌱 Crear branch: arch/api-reportes-automaticos
6. 📝 Implementar siguiendo criterios de aceptación
7. 🚀 PR linking el Issue
8. 🔍 Code review por Code Owners
9. ✨ Merge y close Issue
```

### Ejemplo 2: Migración de Documento Existente
```
1. 📁 Issue: [MIGRADO] Estrategia Dual Profiles
2. 🏷️ Labels: arquitectura, migrado, aprobado, database
3. 📋 Copiar contenido relevante del documento original
4. 🔗 Linking a PRs donde se implementó
5. 🏷️ Label: "aprobado" (ya implementado)
6. 🗑️ Archivar documento original o mover a docs/archive/
```

---

**🤖 Implementado con [Claude Code](https://claude.ai/code)**

**Co-Authored-By:** Claude <noreply@anthropic.com>