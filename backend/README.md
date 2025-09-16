# Backend IPS Santa Helena del Valle

## 🎯 **Inicio Rápido - Arquitectura Completa**

👉 **Para entender la arquitectura completa del proyecto:**  
📖 **[🏗️ Ver Guía Arquitectónica Maestra](docs/01-foundations/architecture-overview.md)** ⭐

El sistema integral de gestión de RIAS (Rutas Integrales de Atención en Salud) según Resolución 3280 de 2018, con arquitectura polimórfica anidada y estrategia de perfiles duales (Clínico + Call Center).

## 🔧 **Configuración AI Assistant**
- 📋 [Configuración Completa](CLAUDE.md) - Setup desarrollo con AI
- 📊 [Estado del Proyecto](PROJECT-STATUS.md) - Progreso y estado actual por módulos

## 📚 **Documentación Organizada**
La documentación técnica está estructurada por propósito:
- **`docs/01-foundations/`** - Fundamentos críticos y guía maestra
- **`docs/02-regulations/`** - Compliance normativo (Res. 3280, 202)  
- **`docs/03-architecture/`** - Decisiones estratégicas y perfiles duales
- **`docs/04-development/`** - Guías operativas día a día
- **`docs/05-logs/`** - Registros históricos y verificaciones

---

## ⚡ **Configuración Rápida**

## 2. Estructura del Monorepo

El repositorio está organizado en las siguientes carpetas principales:

-   `backend/`: Contiene todo el código de la API (Python, FastAPI).
-   `frontend/`: Contiene el código de la aplicación web (React, TypeScript).

## 3. Stack Tecnológico

### Backend
-   **Lenguaje:** Python 3.12+
-   **Framework:** FastAPI
-   **Base de Datos:** PostgreSQL (gestionada a través de Supabase)
-   **Testing:** Pytest
-   **Servidor ASGI:** Uvicorn

### Frontend
-   **Framework:** React con TypeScript
-   **Librería de UI:** Material-UI (MUI)
-   **Gestión de Estado:** React Query (TanStack Query)
-   **Cliente HTTP:** Axios
-   **Enrutamiento:** React Router

## 4. Configuración del Entorno Local

Sigue estos pasos para configurar el proyecto completo en tu máquina.

### 4.1. Prerrequisitos

-   Tener Python 3.12 o superior instalado.
-   Tener Node.js y npm (o Yarn) instalados.
-   Tener Git instalado.

### 4.2. Clonar el Repositorio

```bash
git clone https://github.com/camilorinconp/santahelenadelvalleips.git
cd santahelenadelvalleips
```

### 4.3. Configuración del Backend

1.  **Navegar al directorio del backend:**
    ```bash
    cd backend
    ```
2.  **Crear y Activar Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # macOS/Linux
    # .\venv\Scripts\activate # Windows
    ```
3.  **Instalar Dependencias:**
    ```bash
    cp .env.example .env # Asegúrate de rellenar .env con tus credenciales de Supabase
    pip install -r requirements.txt
    ```
4.  **Volver a la raíz del proyecto:**
    ```bash
    cd ..
    ```

### 4.4. Configuración del Frontend

Consulta el `frontend/README_FRONTEND.md` para las instrucciones de configuración del frontend.

## 5. Cómo Ejecutar la Aplicación (Ambos Servidores)

Para ejecutar la aplicación completa, necesitas iniciar tanto el servidor del backend como el del frontend.

### 5.1. Iniciar el Backend

Desde la raíz del proyecto:
```bash
cd backend && ./venv/bin/uvicorn main:app --reload &
```

### 5.2. Iniciar el Frontend

Desde la raíz del proyecto:
```bash
cd frontend && npm start &
```

La API estará disponible en `http://127.0.0.1:8000` y la aplicación frontend en `http://localhost:3000`.

## 6. Prácticas de Desarrollo y Operación

Estas son las prácticas esenciales para mantener la calidad, seguridad y eficiencia del proyecto.

### 6.1. Gestión de Entorno y Secretos

-   **Principio:** Los secretos (claves de API, credenciales de DB) nunca deben ser versionados en Git. Para desarrollo, se usa `.env` (excluido por `.gitignore`). Para producción, se deben inyectar de forma segura como variables de entorno en el servidor de despliegue.
-   **Implementación:**
    -   **Backend:** Las variables de entorno son leídas por FastAPI. El entorno de despliegue debe proveerlas.
    -   **Frontend:** Vercel (o el servicio de hosting) permite configurar variables de entorno de forma segura para el proceso de construcción y ejecución.

### 6.2. Automatización (Integración Continua - CI/CD)

-   **Principio:** Todo cambio de código debe ser validado automáticamente para asegurar la calidad, consistencia y detectar errores tempranamente.
-   **Herramienta:** GitHub Actions (`.github/workflows/ci.yml`).
-   **Validaciones:**
    -   **Instalación de Dependencias:** Asegurar que todas las dependencias se instalen correctamente.
    -   **Linting y Formateo:** Ejecutar linters (ej. `ruff` para Python, `eslint` para JS/TS) y formateadores (ej. `black` para Python, `prettier` para JS/TS) para mantener el estilo de código.
    -   **Pruebas Unitarias/Integración:** Ejecutar `pytest` para el backend y `npm test` para el frontend.

### 6.3. Fijar Dependencias

-   **Principio:** Asegurar la reproducibilidad del entorno de desarrollo y producción fijando las versiones exactas de todas las dependencias (directas e indirectas).
-   **Implementación:**
    -   **Backend:** Utilizar `pip freeze > requirements.txt` para generar un `requirements.txt` completo. Este archivo debe ser versionado.
    -   **Frontend:** `package-lock.json` (generado por npm) ya cumple esta función para las dependencias de Node.js.

## 7. Cómo Ejecutar las Pruebas

### 7.1. Pruebas del Backend

Desde el directorio `backend/` (con el entorno virtual activado):
```bash
pytest -v
```

### 7.2. Pruebas del Frontend

Desde el directorio `frontend/`:
```bash
npm test
```
