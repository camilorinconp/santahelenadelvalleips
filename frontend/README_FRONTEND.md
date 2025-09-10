# Proyecto Frontend - IPS Santa Helena del Valle

Este documento (`README_FRONTEND.md`) es la fuente de la verdad y la guía principal para el desarrollo de la interfaz de usuario (frontend) de la aplicación de gestión de Rutas Integrales de Atención en Salud (RIAS).

## 1. Propósito

El frontend es una **Single Page Application (SPA)** diseñada para ser utilizada por profesionales de la salud. Su objetivo es proporcionar una herramienta de trabajo robusta, eficiente e intuitiva para registrar y consultar las atenciones médicas de los pacientes, siguiendo los lineamientos de la Resolución 3280.

## 2. Stack Tecnológico Principal

| Categoría             | Elección                                                              | Razón                                                                                                                              |
| --------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Framework**         | [React](https://reactjs.org/) con [TypeScript](https://www.typescriptlang.org/) | Estándar de la industria, basado en componentes y con tipado estático para una integración segura y sin errores con la API de FastAPI. |
| **Librería de UI**    | [Material-UI (MUI)](https://mui.com/)                                 | Suite de componentes completa y profesional, ideal para aplicaciones densas en datos y formularios complejos. Acelera el desarrollo. |
| **Gestión de Estado** | [React Query (TanStack Query)](https://tanstack.com/query/latest)     | Simplifica drásticamente la obtención, cacheo y sincronización de datos del servidor, manejando estados de carga y error.        |
| **Cliente HTTP**      | [Axios](https://axios-http.com/)                                      | Cliente HTTP robusto y estándar para la comunicación con el backend.                                                               |
| **Enrutamiento**      | [React Router](https://reactrouter.com/)                              | Librería estándar para la gestión de rutas en aplicaciones React.                                                                  |
| **Gestión de Paquetes** | [npm](https://www.npmjs.com/)                                         | Gestor de paquetes estándar en el ecosistema de JavaScript.                                                                        |

## 3. Arquitectura y Estructura de Directorios

La estructura del proyecto está organizada por funcionalidades para mantener el código modular y escalable.

```
frontend/
├── src/
│   ├── api/              # Configuración de Axios y funciones de llamada a la API (ej. atencionesApi.ts)
│   ├── components/       # Componentes de UI genéricos y reutilizables (Button, Input, etc.)
│   ├── features/         # Lógica y componentes por funcionalidad de negocio (Pacientes, Atenciones)
│   ├── hooks/            # Hooks personalizados (ej. useAuth)
│   ├── pages/            # Componentes que representan una página/ruta completa
│   ├── App.tsx           # Componente raíz con el enrutador principal
│   └── ...
├── package.json
└── tsconfig.json
```

### 3.1. Manejo de Atenciones Polimórficas

Este es el reto arquitectónico principal. La solución implementada es un "Asistente de Creación" (`CrearAtencionWizard`):

1.  **Selección de Tipo:** El usuario elige el `tipo_atencion` desde un desplegable.
2.  **Renderizado Dinámico:** El asistente renderiza el formulario específico (ej. `AtencionPrimeraInfanciaForm`) correspondiente al tipo seleccionado.
3.  **Envío en Dos Pasos:**
    a. Se envía el formulario de **detalle** al endpoint específico (ej. `POST /atencion-primera-infancia/`).
    b. Con el ID del detalle, se crea el registro principal en `POST /atenciones/`.

## 4. Cómo Empezar

1.  **Instalar dependencias:**
    ```bash
    npm install
    ```
2.  **Iniciar el servidor de desarrollo:**
    ```bash
    npm start
    ```

## 5. Guías de Desarrollo

- **Tipado Estricto:** Todo nuevo código debe tener una cobertura de tipos adecuada. Aprovechar los modelos de la API.
- **Componentes Reutilizables:** Antes de crear un nuevo componente de UI, verificar si existe uno similar en `MUI` o en `src/components`.
- **Manejo de Estado del Servidor:** Utilizar `React Query` para toda la interacción con la API. Evitar el uso de `useState` para almacenar datos del servidor.
