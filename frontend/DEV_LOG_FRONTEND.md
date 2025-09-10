# Diario de Desarrollo - Frontend

Este documento (`DEV_LOG_FRONTEND.md`) registra las decisiones y los pasos de desarrollo tomados por el Equipo Principal Frontend.

---

### **2025-09-10**

**Objetivo:** Establecer la base del proyecto frontend según la recomendación aprobada y la nomenclatura de archivos acordada.

**Acciones:**

1.  **Decisión de Arquitectura:** Se acordó una estructura de **Monorepo** con carpetas `backend/` y `frontend/` separadas en la raíz del proyecto para mayor claridad.
2.  **Reestructuración:** Se creó la carpeta `backend/` y se movieron todos los archivos existentes del proyecto a ella.
3.  **Inicialización del Frontend:** Se eliminó el directorio `frontend/` conflictivo y se inicializó exitosamente un nuevo proyecto de React con TypeScript usando `create-react-app`.
4.  **Restauración de Documentación:** Se han vuelto a crear los archivos `README_FRONTEND.md` y `DEV_LOG_FRONTEND.md` dentro de la nueva estructura del proyecto `frontend/`.

**Próximos Pasos:**

-   Instalar las dependencias principales (`MUI`, `axios`, `react-query`, `react-router-dom`).
-   Configurar la estructura de directorios base dentro de `frontend/src/`.
