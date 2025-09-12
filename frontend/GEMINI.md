# Contexto del Proyecto: Frontend para IPS Santa Helena del Valle

Este documento proporciona el contexto esencial para la asistencia de IA en el frontend de este proyecto.

### 1. Propósito y Dominio
Este proyecto es el frontend para la API de la IPS Santa Helena del Valle. Su objetivo es proporcionar una interfaz de usuario intuitiva y eficiente para que el personal médico gestione las Rutas Integrales de Atención en Salud (RIAS) de los pacientes, conforme a la **Resolución 3280 de 2018**.

### 2. Stack Tecnológico Principal
- **Framework:** React
- **Lenguaje:** TypeScript
- **Librería de UI:** Material-UI (MUI)
- **Gestión de Estado del Servidor:** React Query (TanStack Query)
- **Cliente HTTP:** Axios
- **Gestión de Formularios:** React Hook Form + Zod
- **Enrutamiento:** React Router
- **Build Tool:** Create React App (CRA)

### 3. Arquitectura y Convenciones
- **Estructura de Carpetas:**
    - `src/pages`: Componentes que representan páginas completas.
    - `src/components`: Componentes de UI genéricos y reutilizables.
    - `src/api`: Lógica para comunicarse con el backend (configuración de Axios y funciones de llamada).
    - `src/hooks`: Hooks de React personalizados.
    - `src/utils`: Funciones de utilidad (ej. `formatters.ts`).
    - `src/theme.ts`: Configuración del tema de Material-UI.

- **Comunicación con Backend:**
    - La comunicación con la API se centraliza en los archivos dentro de `src/api/`.
    - Se debe usar **React Query** para toda la gestión de estado del servidor (fetching, caching, mutaciones).
    - Los formularios se gestionan con **React Hook Form** y la validación se define con **Zod**.

- **Estilo de Código:**
    - Seguir las convenciones de la comunidad de React y TypeScript.
    - Usar componentes funcionales con Hooks.
    - Tipado estricto en todo el código.

### 4. Fuentes de la Verdad (Lectura Obligatoria)
1.  **`docs/01-ARCHITECTURE-GUIDE.md`**: Guía de arquitectura general, incluyendo patrones de frontend.
2.  **`backend/GEMINI.md`**: Para entender la estructura de la API, los modelos de datos y los endpoints que se van a consumir.
3.  **`docs/02-DEVELOPMENT-WORKFLOW.md`**: Flujo de trabajo de desarrollo, incluyendo convenciones de Git y testing.

### 5. Procedimiento de Pruebas
- Las pruebas se escriben con **Jest** y **React Testing Library**.
- Los archivos de prueba deben tener la extensión `.test.tsx` o `.spec.tsx`.
- **Comando de ejecución:** `npm test`
- **Comando con cobertura:** `npm test -- --coverage --watchAll=false`

### 6. Idioma de Interacción
La comunicación con el usuario y toda la UI debe realizarse preferentemente en **español**.