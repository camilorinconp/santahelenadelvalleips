# Contexto del Proyecto: Migraciones de Supabase

Este documento proporciona el contexto para la gestión de la base de datos con Supabase.

### 1. Propósito
Esta carpeta contiene toda la configuración y las migraciones de la base de datos PostgreSQL gestionada por Supabase. Es la **fuente de la verdad** para la estructura de la base de datos del proyecto.

### 2. Stack Tecnológico
- **Base de Datos:** PostgreSQL
- **Plataforma:** Supabase
- **Herramienta CLI:** Supabase CLI

### 3. Flujo de Trabajo para Migraciones
Para mantener la consistencia entre el entorno de desarrollo local y el remoto, se debe seguir el siguiente flujo, detallado en `docs/02-DEVELOPMENT-WORKFLOW.md`:

1.  **Iniciar entorno local:** Usar `supabase start`.
2.  **Realizar cambios en el esquema:** Se pueden hacer cambios directamente en la UI de Studio local (`http://127.0.0.1:54323`) o aplicando SQL.
3.  **Generar el archivo de migración:** Una vez satisfecho con los cambios, ejecutar el comando desde la raíz del proyecto:
    ```bash
    supabase db diff -f nombre_descriptivo_de_la_migracion
    ```
    Esto creará un nuevo archivo SQL en la carpeta `supabase/migrations`.

4.  **Validar la migración localmente:** Para asegurar que la migración es correcta y no rompe nada, es crucial resetear la base de datos local y correr las pruebas del backend.
    ```bash
    supabase db reset
    cd backend && pytest -v
    ```
5.  **Desplegar en producción:** Vincular el proyecto (`supabase link`) y luego empujar las migraciones con `supabase db push`.

### 4. Convenciones y Buenas Prácticas
- **Nomenclatura:** Los archivos de migración deben seguir el formato `YYYYMMDDHHMMSS_descripcion_clara.sql`.
- **Atomicidad:** Cada migración debe ser atómica y, si es posible, reversible.
- **Documentación:** Incluir comentarios en el archivo SQL explicando el propósito del cambio.
- **Seguridad (RLS):** Cualquier tabla nueva con datos sensibles debe tener RLS habilitado y políticas definidas dentro de la misma migración.
- **Sincronización:** Es vital mantener la sincronía entre el esquema de la BD, los modelos Pydantic del backend y los formularios del frontend.

### 5. Fuentes de la Verdad (Lectura Obligatoria)
1.  **`docs/01-ARCHITECTURE-GUIDE.md`**: Fuente de la verdad para la arquitectura de datos, incluyendo el patrón polimórfico y la estrategia de tipado (ENUMs, JSONB, TEXT).
2.  **`docs/02-DEVELOPMENT-WORKFLOW.md`**: Guía detallada sobre el flujo de trabajo de desarrollo, incluyendo el manejo de migraciones.
3.  **`backend/DATABASE-STATUS.md`**: Contexto sobre cómo los modelos de la API se relacionan con el esquema de la base de datos.

### 6. Idioma de Interacción
La comunicación con el asistente de IA y los comentarios en las migraciones deben realizarse preferentemente en **español**.