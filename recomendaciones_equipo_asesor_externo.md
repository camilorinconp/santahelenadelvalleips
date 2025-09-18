# Recomendaciones del Equipo Asesor Externo

Este documento contiene un resumen de las recomendaciones de mayor impacto y prioridad para el proyecto. Los análisis detallados se encuentran en los informes de auditoría individuales.

---

## Auditoría General (Septiembre 2025)

### 1. Backend

**Recomendación Crítica: Implementar Transacciones Atómicas y Unificar Arquitectura.**

- **Problema:** Defecto sistémico en la creación de datos (no son atómicos) y severa inconsistencia en los patrones de diseño (3 arquitecturas distintas conviviendo).
- **Impacto:** Riesgo crítico de corrupción de datos, alta deuda técnica y mantenibilidad reducida.
- **Solución Propuesta:** Refactorizar la lógica de negocio a una capa de servicios que utilice funciones de base de datos (RPCs) para garantizar transacciones atómicas, y unificar el modelado de datos a un único patrón.
- **Informe Detallado:** **[Informe de Auditoría de Backend](./backend/docs/06-auditorias/2025-09-17_informe_auditoria_backend.md)**

### 2. Supabase (Base de Datos)

**Recomendación Crítica: Reimplantar el Modelo de Seguridad (RLS).**

- **Problema:** La implementación de la Seguridad a Nivel de Fila (RLS) ha sido caótica e inconsistente, lo que genera un riesgo de seguridad a pesar de la intención de proteger los datos.
- **Impacto:** Potenciales agujeros de seguridad y una configuración difícil de verificar y mantener.
- **Solución Propuesta:** Realizar una auditoría y reimplementación completa de todas las políticas de RLS desde una única migración "limpia" que sirva como fuente de la verdad para el modelo de seguridad.
- **Informe Detallado:** **[Informe de Auditoría de Supabase](./supabase/docs/04-auditorias/2025-09-17_informe_auditoria_supabase.md)**

### 3. Frontend

**Recomendación Estratégica: Detener Desarrollo y Priorizar Refactorización del Backend.**

- **Problema:** La funcionalidad más compleja (formularios de atención polimórficos) no ha sido construida y su desarrollo está bloqueado por las inconsistencias del backend.
- **Impacto:** Riesgo de multiplicar la deuda técnica del backend en el frontend, resultando en un UI/UX complejo, lento de desarrollar y propenso a errores.
- **Solución Propuesta:** Pausar el desarrollo de nuevas funcionalidades y, una vez el backend sea consistente, implementar un motor de formularios dinámico basado en metadatos en lugar de formularios hard-coded.
- **Informe Detallado:** **[Informe de Auditoría de Frontend](./frontend/docs/06-auditorias/2025-09-17_informe_auditoria_frontend.md)**