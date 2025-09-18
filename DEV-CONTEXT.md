# 🚀 Panel de Control: Auditoría Continua Asistida
**📅 Última Actualización:** 17 septiembre 2025

---

## ✅ CHECKLIST DE INICIO DE JORNADA (OBLIGATORIO)
*Antes de empezar a programar, verifica los siguientes puntos:*

- [ ] **1. Objetivo del Sprint:** He leído y entiendo el **objetivo** definido en la sección "ESTADO ACTUAL DEL SPRINT".
- [ ] **2. Rama de Git:** Estoy trabajando en la **rama Git** correcta para este sprint.
- [ ] **3. Revisión del Asesor:** He verificado el **estado de la revisión** del Asesor Externo. Si hay cambios solicitados, son mi prioridad.

---

## 🎯 ESTADO ACTUAL DEL SPRINT

- **Objetivo:** **Sprint #2** - Refactorizar el módulo `control_cronicidad` para usar el patrón RPC+Service, siguiendo el modelo exacto implementado en `atencion_vejez`.
- **Rama Git:** `arch/refactor-cronicidad-rpc`
- **Pull Request:** (Pendiente de creación)
- **Estado Asesor Externo:** `PENDIENTE DE INICIO`
- **Retroalimentación del Asesor:** El objetivo es replicar el éxito del sprint piloto en un módulo con un patrón de datos diferente. La clave es la consistencia arquitectónica.

---

## 🔄 FLUJO DE TRABAJO: AUDITORÍA CONTINUA ASISTIDA (Paso a Paso)

Este documento es la guía operativa para la colaboración entre el **Equipo Principal** y el **Asesor Externo**, articulada por el **Human-in-the-Loop (HITL)**.

### **Paso 1: Planificación del Sprint**
1.  El **Equipo Principal** define el **Objetivo del Sprint** y lo documenta en la sección de arriba.
2.  (Opcional) El **HITL** presenta el plan al **Asesor Externo** para una validación rápida.

### **Paso 2: Desarrollo**
1.  El **Equipo Principal** crea una nueva rama Git y desarrolla la funcionalidad.

### **Paso 3: Punto de Control (Pull Request)**
1.  Al finalizar, el **Equipo Principal** abre un **Pull Request (PR)** y notifica al **HITL**.
2.  El **Human-in-the-Loop (HITL)** asume sus responsabilidades:
    *   **Articular:** Actúa como el canal de comunicación oficial.
    *   **Notificar:** Informa al **Asesor Externo** que el PR está listo para revisión, proporcionando el enlace y los archivos clave a revisar.
    *   **Gestionar:** Recibe el veredicto del Asesor (`APROBADO` o `CAMBIOS REQUERIDOS`).
    *   **Actualizar:** Refleja el nuevo **"Estado Asesor Externo"** en este documento.

### **Paso 4: Integración**
1.  Si hay `CAMBIOS REQUERIDOS`, el **Equipo Principal** los implementa y se reinicia el ciclo en el Paso 3.
2.  Si el PR es `APROBADO`, un líder del **Equipo Principal** realiza el "merge".
3.  El **Equipo Principal** y el **HITL** actualizan este documento para planificar el siguiente sprint.

---

## 📚 REFERENCIAS CLAVE PARA ESTE SPRINT

- **Guía de Remediación:** [Informe de Auditoría de Backend](../backend/docs/06-auditorias/2025-09-17_informe_auditoria_backend.md)
- **Mejores Prácticas:** [Framework de Mejores Prácticas](../backend/docs/04-development/best-practices-overview.md)
