# Contexto del Proyecto (Frontend): UI para IPS Santa Helena del Valle
**Última Actualización:** 14 de septiembre, 2025

## 1. Propósito y Dominio
Este proyecto es la interfaz de usuario (UI) para la API de la IPS Santa Helena del Valle. Es una Single Page Application (SPA) construida con React, cuyo objetivo es proporcionar al personal clínico y administrativo una herramienta eficiente para gestionar las Rutas Integrales de Atención en Salud (RIAS) conforme a la **Resolución 3280 de 2018**.

## 2. Stack Tecnológico Principal
- **Framework:** React con TypeScript
- **Librería de UI:** Material-UI (MUI)
- **Gestión de Estado del Servidor:** React Query (TanStack Query)
- **Gestión de Formularios:** React Hook Form + Zod para validación
- **Cliente HTTP:** Axios
- **Enrutamiento:** React Router
- **Pruebas:** Jest + React Testing Library

## 3. Fuentes de la Verdad (Jerarquía de Documentación)
La documentación del frontend ha sido reorganizada para máxima claridad y eficiencia. Debe ser consultada en el siguiente orden dentro de la carpeta `frontend/docs/`:

1.  **`01-foundations/frontend-overview.md`**: **PUNTO DE PARTIDA OBLIGATORIO.** Es el hub central que resume la arquitectura, el stack y el estado de avance del frontend, enlazando a los demás documentos.
2.  **`02-architecture/`**: Contiene las decisiones y patrones de arquitectura específicos de React (gestión de estado, patrones de componentes, sistema de diseño).
3.  **`03-integration/`**: Guías cruciales sobre cómo el frontend se integra con el backend, incluyendo el manejo de la API polimórfica y los patrones de validación.
4.  **`04-development/`**: Guías prácticas para el día a día: cómo configurar el entorno, guías de testing, etc.
5.  **`05-features/`**: Documentación funcional de cada módulo de negocio implementado.

## 4. Arquitectura General y Patrones Clave

La aplicación sigue un patrón de **Backend Unificado con Vistas de Frontend Especializadas por Rol**. Esto significa que una única aplicación React contiene diferentes "experiencias" para distintos usuarios.

- **Estructura de Carpetas:** El código en `src/` está organizado por funcionalidad:
    - `/pages`: Componentes que representan una página completa o una ruta principal.
    - `/components`: Componentes de UI genéricos y reutilizables.
    - `/api`: Centraliza toda la comunicación con el backend. Contiene las funciones que llaman a los endpoints de FastAPI.
    - `/hooks`: Hooks de React personalizados para encapsular lógica reutilizable.

- **Patrones Arquitectónicos Fundamentales:**
    1.  **Gestión de Estado Dual:** Se separa estrictamente el estado del servidor del estado de la UI.
        *   **Estado del Servidor:** Gestionado **exclusivamente** por **React Query**. Se usa para fetching, caching, y mutaciones de datos del backend.
        *   **Estado de la UI:** Gestionado con hooks nativos de React (`useState`, `useContext`, `useReducer`).
    2.  **Formularios Robustos:**
        *   **React Hook Form** para gestionar el estado, los eventos y el rendimiento de los formularios.
        *   **Zod** para definir los esquemas de validación, que deben ser un espejo de los modelos Pydantic del backend para garantizar la consistencia.

## 5. Módulos Clave y Estado de Avance

- **Núcleo de la Aplicación (85%):** La base está sólidamente construida. Esto incluye el layout principal, el sistema de enrutamiento, la configuración del tema de Material-UI y la integración de React Query.
- **Gestión de Pacientes (100%):** El CRUD (Crear, Leer, Actualizar, Eliminar) de pacientes está completo y funcional. Las páginas `PacientesPage.tsx` y `PacienteFormPage.tsx` existen y están conectadas a la API.
- **Formularios Clínicos Especializados (RIAMP/RPMS) (5%):** Se han definido los patrones, pero **no se ha construido ningún formulario clínico detallado**. No existen componentes como `ControlPrenatalForm.tsx` o similares. Este es el principal trabajo pendiente.
- **Módulo de Gestión Proactiva (Demanda Inducida) (0%):** No iniciado. No existe la página `GestionProactivaPage.tsx` ni los componentes asociados.

## 6. Idioma de Interacción
La comunicación con el asistente de IA y toda la interfaz de usuario debe ser en **español**.
