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

## 6. Análisis Experto de la Estrategia de Base de Datos Híbrida y Polimórfica

Nuestra estrategia se basa en dos pilares fundamentales:

1.  **Base de Datos Híbrida:** Utilizar Supabase como un servicio gestionado de PostgreSQL, combinado con la CLI de Supabase para la gestión de migraciones (tratando el esquema como código).
2.  **Polimorfismo de Datos:** Implementar un modelo donde una tabla central (`atenciones`) contiene atributos comunes y se vincula a tablas de detalle especializadas (ej. `atencion_materno_perinatal`, `atencion_primera_infancia`) para atributos únicos.

### Fortalezas de la Estrategia Actual:

*   **Alineación con el Dominio (Salud):** El modelo polimórfico es ideal para el sector salud. Permite manejar la diversidad de tipos de atención (RIAS) con sus datos específicos, mientras se mantiene una visión unificada de todas las atenciones. Esto mapea directamente a la complejidad de la Resolución 3280.
*   **Escalabilidad y Flexibilidad:** Es relativamente sencillo añadir nuevos tipos de atención o expandir los existentes sin afectar la estructura central de `atenciones`.
*   **Integridad de Datos:** El uso de UUIDs para IDs y claves foráneas es una buena práctica que asegura la unicidad y la integridad referencial.
*   **Aprovechamiento de Supabase:** Delegamos la gestión de infraestructura a Supabase, y su CLI nos permite versionar el esquema, lo cual es un salto cualitativo enorme respecto a los cambios manuales.
*   **Separación de Intereses:** Nuestra FastAPI aplicación se enfoca en la lógica de negocio y API endpoints, mientras que Supabase (con PostgREST) maneja la capa de persistencia y su API relacional.

### Áreas de Mejora y Consideraciones (Desafíos y Refinamientos):

1.  **Robustez del Flujo de Migraciones (Lección Aprendida Reciente):**
    *   **Desafío:** Hemos experimentado que la CLI de Supabase, en ocasiones, no aplica completamente los cambios o el caché del esquema de PostgREST no se refresca.
    *   **Recomendación:**
        *   **Vigilancia Continua:** Mantenerse al tanto de las actualizaciones de la CLI de Supabase y sus mejores prácticas.
        *   **Validación Post-Migración:** Considerar la implementación de un paso de validación automatizado en CI/CD que, después de aplicar migraciones, verifique que el esquema de la base de datos en el entorno de destino coincide con el esperado por los modelos Pydantic.
        *   **Documentar Workarounds:** Mantener un registro claro (en `DEVELOPMENT_LOG.md`) de los "workarounds" para problemas de plataforma, como el reinicio de servicios.

2.  **Consulta de Datos Polimórficos:**
    *   **Desafío:** Recuperar un registro completo de "atención" (desde `atenciones` más su tabla de detalle específica) requiere unir tablas basándose en `tipo_atencion` y `detalle_id`. Esto puede volverse complejo para consultas genéricas.
    *   **Recomendación:**
        *   **Vistas de Base de Datos (Views):** Crear vistas SQL en Supabase que pre-unan la tabla `atenciones` con cada tabla de detalle. Esto simplifica las consultas desde la aplicación.
        *   **Funciones de Base de Datos (RPC):** Para agregaciones complejas o consultas polimórficas específicas, considerar el uso de funciones de base de datos de Supabase (endpoints RPC) para encapsular la lógica SQL compleja.
        *   **Capa de Servicio de Aplicación:** Asegurar que la lógica de unión y transformación de datos se maneje en una capa de servicio clara en FastAPI, separada de las rutas de la API y el acceso a la base de datos.

3.  **Validación de Datos y Lógica de Negocio (Alineación con Resolución 3280):**
    *   **Desafío:** La Resolución 3280 tiene reglas de negocio complejas y dependencias de datos.
    *   **Recomendación:**
        *   **Restricciones de Base de Datos:** Siempre que sea posible, aplicar restricciones a nivel de base de datos (ej. `CHECK` constraints, `NOT NULL`, `DEFAULT now()` para timestamps) para asegurar la integridad y consistencia de los datos.
        *   **Validación de la Capa de Aplicación:** Implementar validaciones de Pydantic y lógica de negocio en la capa de servicio de FastAPI para reglas más complejas que no pueden ser manejadas por la base de datos.

4.  **Estandarización del Campo `tipo_atencion`:**
    *   **Desafío:** Actualmente, `tipo_atencion` es un campo de texto, propenso a errores tipográficos.
    *   **Recomendación:** Convertir `tipo_atencion` a un tipo `ENUM` en PostgreSQL y Python. Esto proporcionará una tipificación fuerte y evitará valores inválidos.

### Conclusión y Próximos Pasos

La estrategia actual es **sólida y muy adecuada** para el proyecto, especialmente por su alineación con la Resolución 3280 y la flexibilidad del modelo polimórfico. Los desafíos que hemos encontrado son manejables y, al abordarlos, fortaleceremos aún más la robustez del sistema.

El plan de **Expansión y Detalle de Modelos de Datos** (Fase 1) es el paso correcto a seguir. Después de eso, nos enfocaremos en las recomendaciones para la consulta de datos polimórficos y la implementación de lógica de negocio más compleja.

---

### **2025-09-10**

**Objetivo:** Implementar recomendaciones de arquitectura y funcionalidad CRUD de pacientes.

**Acciones:**

1.  **Gestión de Secretos:** Se modificó `backend/database.py` para cargar variables de entorno condicionalmente (solo en desarrollo).
2.  **Fijación de Dependencias:** Se generó `backend/requirements.txt` usando `pip freeze` para asegurar la reproducibilidad.
3.  **CI/CD con GitHub Actions:** Se creó `backend/.github/workflows/ci.yml` para automatizar pruebas y linting de backend y frontend.
4.  **CRUD de Pacientes (Frontend):**
    *   **Listar:** Implementado y funcional.
    *   **Crear:** Implementado y funcional.
    *   **Eliminar:** Implementado y funcional.
    *   **Editar:** Implementado, pero presenta problemas de actualización y advertencias en consola.

**Problemas Pendientes:**

*   **Edición de Pacientes:** La actualización de datos no se persiste correctamente en el backend. Se requiere depuración.
*   **Advertencias en Consola:** Persisten advertencias de React (`value` prop on `input` should not be null) al cargar el formulario de edición, indicando problemas con el saneamiento de valores `null` en campos opcionales (`segundo_nombre`, `segundo_apellido`).
