---
name: Propuesta Arquitectónica
about: Template para propuestas de cambios arquitectónicos al sistema de salud IPS
title: '[ARCH] '
labels: ['arquitectura', 'propuesta', 'necesita-revision']
assignees: ''

---

# 🏗️ Propuesta Arquitectónica

## 📋 Información Básica

**Tipo de Propuesta:** 
- [ ] Cambio de Base de Datos
- [ ] Nuevas APIs/Endpoints
- [ ] Refactorización de Modelos
- [ ] Integración Externa
- [ ] Performance/Optimización
- [ ] Seguridad/RLS
- [ ] Compliance Normativo

**Nivel de Impacto:**
- [ ] Bajo (cambios localizados)
- [ ] Medio (afecta 2-3 módulos)
- [ ] Alto (cambios transversales)
- [ ] Crítico (requiere migración compleja)

**Regulación Asociada:**
- [ ] Resolución 3280 de 2018 (RIAS)
- [ ] Resolución 202 de 2021 (PEDT)
- [ ] Otras normativas colombianas
- [ ] No aplica

## 🎯 Descripción del Problema

### Contexto
<!-- Describe el problema o necesidad actual -->

### Limitaciones Actuales
<!-- Qué limitaciones del sistema actual motivan esta propuesta -->

### Impacto si No se Implementa
<!-- Qué riesgos o problemas surgen si no se aborda esto -->

## 💡 Solución Propuesta

### Descripción General
<!-- Describe la solución de alto nivel -->

### Componentes Afectados
- [ ] Database Schema (Supabase)
- [ ] Backend APIs (FastAPI)
- [ ] Frontend Components (React)
- [ ] Modelos Pydantic
- [ ] Tests
- [ ] Documentación

### Diagrama/Mockup
<!-- Si aplica, incluir diagramas o mockups -->
```
[Insertar diagrama o descripción visual]
```

## 🔧 Detalles Técnicos

### Base de Datos
<!-- Si aplica, describir cambios de esquema -->

### APIs/Endpoints
<!-- Si aplica, describir nuevos endpoints o cambios -->

### Modelos de Datos
<!-- Si aplica, describir cambios en modelos Pydantic -->

## 📊 Análisis de Impacto

### Ventajas
1. 
2. 
3. 

### Desventajas/Riesgos
1. 
2. 
3. 

### Alternativas Consideradas
<!-- Qué otras opciones se evaluaron y por qué se descartaron -->

## 🚀 Plan de Implementación

### Fases
1. **Fase 1:** 
2. **Fase 2:** 
3. **Fase 3:** 

### Estimación Tiempo
- **Desarrollo:** X días
- **Testing:** X días  
- **Documentación:** X días
- **Total:** X días

### Dependencias
<!-- Qué otras tareas/PRs deben completarse antes -->

## ✅ Criterios de Aceptación

- [ ] Cumple normativas colombianas aplicables
- [ ] Mantiene compatibilidad hacia atrás
- [ ] Incluye tests comprehensivos
- [ ] Performance no se degrada
- [ ] Documentación actualizada
- [ ] RLS policies configuradas (si aplica)
- [ ] Migración de datos exitosa (si aplica)

## 🧪 Plan de Testing

### Tests Unitarios
- [ ] 

### Tests de Integración
- [ ] 

### Tests de Performance
- [ ] 

## 📚 Referencias

### Documentación Relevante
- [ ] `docs/02-regulations/resolucion-3280-master.md`
- [ ] `docs/01-foundations/architecture-overview.md`
- [ ] Otras:

### Issues/PRs Relacionados
- 

---

## 👥 Para el Equipo Revisor

### Checklist Revisión Arquitectónica
- [ ] **Compliance:** Alineado con Resolución 3280/202
- [ ] **Consistencia:** Sigue patrones arquitectónicos existentes
- [ ] **Escalabilidad:** Diseño prepara para crecimiento futuro
- [ ] **Mantenibilidad:** Código limpio y documentado
- [ ] **Performance:** No introduce regresiones
- [ ] **Seguridad:** RLS y validaciones apropiadas
- [ ] **Testing:** Cobertura adecuada de tests

### Decisión
- [ ] ✅ **Aprobado** - Proceder con implementación
- [ ] ⚠️ **Aprobado con Cambios** - Implementar con modificaciones sugeridas
- [ ] ❌ **Rechazado** - No proceder, revisar alternativas
- [ ] 🔄 **Necesita Más Información** - Clarificar puntos antes de decidir