# Frontend de la Aplicación IPS Santa Helena del Valle

Este documento (`README_FRONTEND.md`) contiene la información específica para el desarrollo y operación de la aplicación frontend, que es una Single Page Application (SPA) construida con React y TypeScript.

Para una visión general del proyecto, stack tecnológico completo y prácticas de desarrollo generales, consulta el `backend/README.md` en la raíz del monorepo.

## 1. Stack Tecnológico Específico del Frontend

-   **Framework:** React con TypeScript
-   **Librería de UI:** Material-UI (MUI)
-   **Gestión de Estado del Servidor:** React Query (TanStack Query)
-   **Cliente HTTP:** Axios
-   **Enrutamiento:** React Router
-   **Gestión de Formularios:** React Hook Form con Zod

## 2. Estructura de Directorios

La estructura del proyecto está organizada por funcionalidades para mantener el código modular y escalable.

```
frontend/
├── src/
│   ├── api/              # Configuración de Axios y funciones de llamada a la API
│   ├── components/       # Componentes de UI genéricos y reutilizables
│   ├── features/         # Lógica y componentes por funcionalidad de negocio (ej. pacientes/)
│   ├── hooks/            # Hooks personalizados
│   ├── pages/            # Componentes que representan una página/ruta completa
│   ├── utils/            # Funciones de utilidad generales (ej. formatters.ts)
│   ├── App.tsx           # Componente raíz con el enrutador principal
│   └── ...
├── package.json
└── tsconfig.json
```

### 2.1. Manejo de Atenciones Polimórficas

Este es un patrón arquitectónico clave en el proyecto. La solución implementada en el frontend es un "Asistente de Creación" (`CrearAtencionWizard`):

1.  **Selección de Tipo:** El usuario elige el `tipo_atencion` desde un desplegable.
2.  **Renderizado Dinámico:** El asistente renderiza el formulario específico (ej. `AtencionPrimeraInfanciaForm`) correspondiente al tipo seleccionado.
3.  **Envío en Dos Pasos:**
    a. Se envía el formulario de **detalle** al endpoint específico (ej. `POST /atencion-primera-infancia/`).
    b. Con el ID del detalle, se crea el registro principal en `POST /atenciones/`.

## 3. Cómo Empezar con el Frontend

Desde el directorio `frontend/`:

1.  **Instalar dependencias:**
    ```bash
    npm install
    ```
2.  **Iniciar el servidor de desarrollo:**
    ```bash
    npm start
    ```

## 4. Guías de Desarrollo Específicas del Frontend

Estas guías complementan las prácticas generales definidas en el `backend/README.md`.

-   **Tipado Estricto:** Todo nuevo código debe tener una cobertura de tipos adecuada. Aprovechar los modelos de la API y los esquemas de Zod.
-   **Componentes Reutilizables:** Antes de crear un nuevo componente de UI, verificar si existe uno similar en `MUI` o en `src/components`.
-   **Manejo de Estado del Servidor:** Utilizar `React Query` para toda la interacción con la API (obtención, cacheo, mutaciones). Evitar el uso de `useState` para almacenar datos del servidor.
-   **Gestión de Formularios:** Usar `react-hook-form` para el estado del formulario y `zod` para la validación.

### 4.1. Gestión de Secretos y Variables de Entorno

-   **Implementación:** Para el frontend, las variables de entorno (ej. `REACT_APP_API_URL`) se configuran en el servicio de despliegue (como Vercel). No deben ser versionadas en Git.

### 4.2. Automatización (CI/CD para Frontend)

-   **Validaciones:** El flujo de CI (definido en `.github/workflows/ci.yml`) ejecutará automáticamente:
    -   `npm install`: Para asegurar que las dependencias se instalen correctamente.
    -   `npm run lint`: Para verificar el estilo y la calidad del código (configurado en `package.json`).
    -   `npm test`: Para ejecutar las pruebas unitarias del frontend.

### 4.3. Fijar Dependencias

-   **Implementación:** El archivo `package-lock.json` (generado por npm) ya cumple la función de fijar las versiones exactas de todas las dependencias de Node.js, asegurando la reproducibilidad.

## 5. Cómo Ejecutar las Pruebas del Frontend

Desde el directorio `frontend/`:

```bash
npm test
```
