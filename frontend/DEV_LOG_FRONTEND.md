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

---

### **2025-09-10**

**Objetivo:** Actualizar la documentación del proyecto.

**Acciones:**

1.  **Actualización de `backend/README.md`:** Se actualizó para reflejar la estructura de monorepo y se añadieron secciones sobre prácticas de desarrollo y operación (gestión de secretos, CI/CD, fijación de dependencias).
2.  **Actualización de `frontend/README_FRONTEND.md`:** Se refactorizó para ser más conciso y específico del frontend, complementando el `README` principal.

---

### **2025-09-10**

**Objetivo:** Implementar funcionalidad CRUD de pacientes.

**Acciones:**

1.  **Listar Pacientes:** Implementación de la tabla de pacientes con `DataGrid` y `useQuery`.
2.  **Crear Pacientes:** Implementación del formulario de creación con `react-hook-form` y `zod`, y conexión a la API con `useMutation`.
3.  **Eliminar Pacientes:** Implementación de la función de eliminación con confirmación y `useMutation`.
4.  **Editar Pacientes:** Refactorización del formulario para soportar edición, carga de datos existentes y actualización vía API con `useMutation`.

**Problemas Pendientes:**

*   **Edición de Pacientes:** La actualización de datos no se persiste correctamente en el backend. Se requiere depuración.
*   **Advertencias en Consola:** Persisten advertencias de React (`value` prop on `input` should not be null) al cargar el formulario de edición, indicando problemas con el saneamiento de valores `null` en campos opcionales (`segundo_nombre`, `segundo_apellido`).
