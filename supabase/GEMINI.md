# Contexto del Proyecto: Migraciones de Supabase

Este documento proporciona el contexto para la gestión de la base de datos con Supabase.

### 1. Propósito
Esta carpeta contiene toda la configuración y las migraciones de la base de datos PostgreSQL gestionada por Supabase. Es la fuente de la verdad para la estructura de la base de datos del proyecto.

### 2. Stack Tecnológico
- **Base de Datos:** PostgreSQL
- **Plataforma:** Supabase
- **Herramienta CLI:** Supabase CLI

### 3. Flujo de Trabajo para Migraciones

Para mantener la consistencia entre el entorno de desarrollo local y el de producción, se debe seguir el siguiente flujo:

1.  **Iniciar el entorno local:** Usar `supabase start` para levantar los servicios.
2.  **Realizar cambios en el esquema:** Se pueden hacer cambios directamente en la UI de Studio local o aplicando SQL.
3.  **Generar el archivo de migración:** Una vez satisfecho con los cambios, ejecutar el comando:
    ```bash
    supabase db diff -f nombre_descriptivo_de_la_migracion
    ```
    Esto creará un nuevo archivo SQL en la carpeta `supabase/migrations`.
4.  **Aplicar migraciones (si es necesario):** Para resetear la base de datos local y aplicar todas las migraciones desde cero, se puede usar `supabase db reset`.
5.  **Desplegar en producción:** Vincular el proyecto con `supabase link` y luego empujar las migraciones con `supabase db push`.

### 4. Idioma de Interacción
La comunicación con el usuario debe realizarse preferentemente en **español**.
