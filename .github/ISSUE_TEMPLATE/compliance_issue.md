---
name: ⚖️ Issue de Compliance Normativo
about: Reportar discrepancias con la Resolución 3280 de 2018
title: '[COMPLIANCE] '
labels: ['compliance', 'resolution-3280', 'high-priority']
assignees: ''
---

## ⚖️ Resumen del Issue de Compliance
<!-- Descripción clara de la discrepancia con la Resolución 3280 -->

## 📜 Referencia Normativa
**Resolución 3280 de 2018**
- **Sección**: [ej. 4.3.1 - Control Prenatal]
- **Artículo**: [ej. Art. 15]
- **Página**: [ej. p. 45-48]
- **Texto específico**: 
  > "Citar el texto exacto de la resolución que no se está cumpliendo"

## 🎯 RIAS Afectada
- [ ] **RIAMP** - Ruta Integral Atención Materno Perinatal
  - [ ] Atención Preconcepcional
  - [ ] Atención Prenatal  
  - [ ] Atención del Parto
  - [ ] Atención del Puerperio
  - [ ] Atención del Recién Nacido
- [ ] **RPMS** - Ruta Promoción y Mantenimiento de Salud
  - [ ] Primera Infancia (0-5 años)
  - [ ] Infancia (6-11 años)
  - [ ] Adolescencia (12-17 años)
  - [ ] Juventud (18-28 años)
  - [ ] Adultez (29-59 años)
  - [ ] Vejez (60+ años)

## 🚫 Discrepancia Identificada

### **Estado Actual del Sistema**:
<!-- Describe cómo está implementado actualmente -->

### **Requerimiento Normativo**:
<!-- Describe qué requiere exactamente la Resolución 3280 -->

### **Gap Identificado**:
<!-- Diferencia específica entre lo actual y lo requerido -->

## 📊 Tipo de Compliance Issue
- [ ] **Campo Obligatorio Faltante** - La normativa requiere un campo que no está capturado
- [ ] **Validación Incorrecta** - Las validaciones no siguen los criterios normativos
- [ ] **Indicador Faltante** - Indicador obligatorio no está siendo calculado
- [ ] **Protocolo Incompleto** - Flujo de atención no sigue el protocolo establecido
- [ ] **Periodicidad Incorrecta** - Frecuencia de controles no coincide con la normativa
- [ ] **Escala/Instrumento Faltante** - Herramienta de evaluación requerida no implementada

## 🔍 Impacto del Compliance Issue

### **Severidad**:
- [ ] **Crítica** - Incumplimiento total de una RIAS obligatoria
- [ ] **Alta** - Campos obligatorios o indicadores críticos faltantes  
- [ ] **Media** - Protocolo parcialmente implementado
- [ ] **Baja** - Detalles menores o recomendaciones no implementadas

### **Riesgo Legal/Regulatorio**:
- [ ] Alto riesgo de observaciones por parte de entes de control
- [ ] Posible impacto en acreditación de la IPS
- [ ] Requerimiento para auditorías internas
- [ ] Necesario para reportes obligatorios

## 💡 Solución Propuesta
<!-- Descripción técnica de cómo abordar el compliance gap -->

### **Campos de Datos Requeridos**:
<!-- Lista específica de campos que deben agregarse/modificarse -->
- Campo 1: [tipo, validaciones, obligatoriedad]
- Campo 2: [tipo, validaciones, obligatoriedad]

### **Validaciones Específicas**:
<!-- Reglas de negocio que deben implementarse -->
- Validación 1: [condiciones específicas]
- Validación 2: [condiciones específicas]

### **Indicadores Afectados**:
<!-- Métricas que se ven impactadas por este compliance gap -->
- Indicador 1: [fórmula, frecuencia]
- Indicador 2: [fórmula, frecuencia]

## 🏗️ Consideraciones de Implementación

### **Componentes Afectados**:
- [ ] Modelos de Datos (Pydantic + Database Schema)
- [ ] API Endpoints (Validaciones y lógica de negocio)
- [ ] Frontend (Forms y validaciones del lado cliente)
- [ ] Sistema de Reportes (Cálculo de indicadores)
- [ ] Migraciones de Base de Datos

### **Backward Compatibility**:
- [ ] Cambio compatible hacia atrás
- [ ] Requiere migración de datos existentes
- [ ] Breaking change - requiere coordinación especial

## 🧪 Criterios de Validación
<!-- Cómo verificar que el compliance issue ha sido resuelto -->
- [ ] Campo/protocolo implementado según especificación exacta
- [ ] Validaciones funcionando correctamente
- [ ] Tests de compliance pasando
- [ ] Indicadores calculándose correctamente
- [ ] Documentación técnica actualizada

## 📅 Prioridad y Timeline

### **Urgencia**:
- [ ] **Inmediata** - Requerido para próxima auditoría
- [ ] **Alta** - Necesario en próximo sprint
- [ ] **Media** - Incluir en roadmap Q4 2024
- [ ] **Baja** - Backlog para futuras iteraciones

### **Dependencias**:
<!-- Issues o tareas que deben completarse primero -->
- Issue #123: [descripción]
- Migración de datos específica
- Capacitación del equipo médico

## 📚 Referencias Adicionales
<!-- Documentación y recursos relevantes -->
- **Resolución Completa**: [enlace al documento]
- **Guías Técnicas del Ministerio**: [enlaces relevantes]
- **Casos de Uso Similares**: [referencias]
- **Issues Relacionados**: #123, #456

## 📝 Notas del Analista de Compliance
<!-- Observaciones adicionales del equipo que identifica el gap -->

---

**Identificado por**: [Nombre del analista/auditor]  
**Fecha de Identificación**: [Fecha]  
**Revisión Normativa**: [Fecha de última revisión de la Resolución]  
**Estado**: [ Nuevo | En Análisis | En Implementación | Verificando | Cerrado ]