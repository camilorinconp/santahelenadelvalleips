## 5. Hitos y Lecciones Aprendidas (2025-09-10)

En esta fecha, se realizó una sesión intensiva de depuración y refactorización que estabilizó por completo la suite de pruebas del proyecto. Las lecciones aprendidas y acciones tomadas son un pilar para el futuro del desarrollo.

### 5.1. Implementación del Flujo de Migraciones de Base de Datos

- **Problema:** Los cambios en el esquema de la base de datos se realizaban manualmente en el panel de Supabase, lo que causaba inconsistencias con los modelos de la aplicación y dificultaba la depuración.
- **Solución:** Se implementó un flujo de trabajo de **migraciones de base de datos** utilizando la **CLI oficial de Supabase**. Todos los cambios en el esquema ahora se gestionan como archivos de migración SQL versionados en el directorio `supabase/migrations`.
- **Estado:** Completado. El proyecto ahora tiene un método robusto y profesional para la gestión de cambios en la base de datos.

### 5.2. Sincronización Total de Modelos, Rutas y Base de Datos

- **Problema:** Una serie de 14 tests fallaban debido a una profunda desincronización entre los modelos Pydantic, la lógica de las rutas de la API y el esquema real de la base de datos.
- **Solución:** Se realizó un proceso de depuración metódico:
    1. Se crearon y aplicaron migraciones para añadir todas las columnas faltantes en las tablas de detalle (`atencion_materno_perinatal`, `atencion_primera_infancia`, etc.).
    2. Se corrigieron las restricciones de nulidad (`NOT NULL`) y se establecieron valores por defecto (`DEFAULT now()`) para los campos `creado_en`.
    3. Se refactorizó la lógica de creación en todas las rutas polimórficas para asegurar un manejo de transacciones y relaciones correcto y consistente.
    4. Se ajustaron los modelos Pydantic y los tests para reflejar la lógica final.
- **Estado:** Completado. Los 25 tests del proyecto ahora pasan con éxito, confirmando la estabilidad de la capa de datos y la API.

### 5.3. Lección Clave sobre el Caché de Esquema de Supabase

- **Observación:** Durante la depuración, la API de Supabase (PostgREST) a menudo no reflejaba inmediatamente los cambios aplicados a través de las migraciones, reportando columnas como inexistentes cuando ya habían sido creadas. El reinicio de los servicios locales (`supabase stop` y `start`) o del proyecto en la nube (Pausar/Restaurar) demostró ser una solución efectiva para forzar la recarga del caché del esquema.
- **Recomendación:** Si después de una migración un test falla con un error de "columna no encontrada", el primer paso de diagnóstico debe ser reiniciar los servicios de Supabase para descartar un problema de caché.