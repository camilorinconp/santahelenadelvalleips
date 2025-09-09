## 1. Sincronización entre Base de Datos y Aplicación

**Lección Aprendida:** Durante la fase de pruebas de las atenciones, nos encontramos con una serie de errores que no estaban en el código de la aplicación, sino en la configuración de la base de datos en Supabase.

**Recomendación:** Es crucial que la configuración del esquema de la base de datos sea un reflejo exacto de la lógica de la aplicación y sus modelos de datos (Pydantic). Antes de escribir pruebas o implementar nuevas funcionalidades, se debe verificar siempre que:

1.  **Políticas de Seguridad a Nivel de Fila (RLS):** Cada tabla que vaya a ser accedida por la API debe tener una política de RLS que permita las operaciones necesarias (SELECT, INSERT, UPDATE, DELETE). Supabase activa RLS por defecto y bloquea todo si no hay una política explícita.
2.  **Restricciones de Nulidad (`NOT NULL`):** Si un campo en un modelo Pydantic es opcional (ej. `Optional[str] = None`), la columna correspondiente en la base de datos **debe ser nullable** (aceptar valores nulos). Un conflicto aquí causará errores `violates not-null constraint`.
3.  **Valores por Defecto (`DEFAULT`):** Las columnas de clave foránea que son opcionales no deben tener valores por defecto que generen datos aleatorios (como `gen_random_uuid()`), ya que esto viola las restricciones de integridad referencial. El valor por defecto para estas columnas debe ser `NULL`.
4.  **Restricciones de Unicidad (`UNIQUE`):** Aplicar esta restricción únicamente cuando la lógica de negocio lo exija de forma estricta. Una columna como `especialidad` en la tabla `medicos` no debe ser única, ya que es natural tener múltiples médicos con la misma especialidad.

Mantener esta sincronía previene errores difíciles de depurar y asegura que la aplicación se comporte como se espera.

## 2. Patrones de Diseño para la Base de Datos

Para mantener la integridad, consistencia y robustez de la base de datos, hemos establecido los siguientes patrones de diseño:

### 2.1. Columnas de Timestamp (creado_en, updated_at)

-   **`creado_en`**: Su propósito es registrar la fecha de creación de una fila. **Nunca debe cambiar**. 
    -   **Configuración:** `Type: timestamptz`, `Is Nullable: No`, `Default Value: now()`.

-   **`updated_at`**: Su propósito es registrar la **última fecha de modificación** de una fila. Debe actualizarse con cada cambio.
    -   **Configuración:** `Type: timestamptz`, `Is Nullable: Sí` (para permitir la creación inicial con valor nulo), y debe ser actualizada automáticamente por un **Trigger** de base de datos (`moddatetime`).

### 2.2. Políticas para Llaves Foráneas (Foreign Keys)

La acción que se toma cuando una fila referenciada es eliminada (`ON DELETE`) es crítica para la integridad de los datos.

-   **`ON DELETE: CASCADE`**: Usar cuando el registro "hijo" no tiene sentido sin el "padre".
    -   **Ejemplo:** La relación `atenciones.paciente_id` -> `pacientes.id`. Si se borra un paciente, todas sus atenciones deben borrarse con él para no dejar datos huérfanos.

-   **`ON DELETE: SET NULL`**: Usar cuando el registro "hijo" sigue siendo valioso históricamente, aunque el "padre" se elimine. La columna de la llave foránea debe ser **Nullable**.
    -   **Ejemplo:** La relación `atenciones.medico_id` -> `medicos.id`. Si un médico es eliminado del sistema, la atención sigue siendo un evento válido en la historia del paciente. El campo `medico_id` simplemente se vuelve `NULL`.

## 3. Ruta de Implementación y Recomendación Arquitectónica

### 3.1. Ruta de Implementación (Roadmap)

**Objetivo General:** Lograr la capacidad de registrar y analizar datos de salud con la granularidad y estructura necesarias para el monitoreo y evaluación exigidos por la Resolución 3280.

**Estrategia:** Evolucionar el modelo de `Atenciones` de un registro genérico a un sistema que soporte tipos de atención especializados, manteniendo la flexibilidad y la trazabilidad.

**Fases de Implementación:**

1.  **Fase 1: Especialización de Atenciones Individuales Clave**
    *   **Objetivo:** Reemplazar la `descripcion` genérica por campos estructurados para los tipos de atención individual más críticos y con mayores requisitos de datos.
    *   **Avance Actual:** Modelo `AtencionPrimeraInfancia` definido.
    *   **Próximos Pasos:**
        *   Crear la tabla `atencion_primera_infancia` en Supabase (con sus triggers y RLS).
        *   Implementar las rutas API (CRUD) para `AtencionPrimeraInfancia`.
        *   Escribir pruebas unitarias y de integración para `AtencionPrimeraInfancia`.
        *   **A Futuro:** Identificar otros tipos de atención individual que requieran especialización (ej. `AtencionMaternoPerinatal`, `TamizajeOncologico`, `ControlCronicidad`) y repetir el proceso.

2.  **Fase 2: Consolidación de Intervenciones Colectivas**
    *   **Objetivo:** Desarrollar completamente el soporte para intervenciones dirigidas a grupos y comunidades.
    *   **Avance Actual:** Modelo `IntervencionColectiva`, tabla y rutas básicas implementadas.
    *   **Próximos Pasos:**
        *   Expandir el CRUD para `IntervencionColectiva` (obtener por filtros, actualizar, eliminar).
        *   Considerar la necesidad de especializar `IntervencionColectiva` si surgen tipos muy distintos (ej. `JornadaSaludComunitaria` vs. `CampañaVacunacion`).

3.  **Fase 3: Integración y Análisis Transversal de Datos**
    *   **Objetivo:** Asegurar que todos los datos (individuales y colectivos) puedan ser consultados y analizados de forma coherente para generar los indicadores de la resolución.
    *   **Próximos Pasos:**
        *   Refinar el manejo de `entornos` (ej. crear una tabla `Entornos` con tipos predefinidos y una FK).
        *   Diseñar una estrategia para vincular las atenciones especializadas a la tabla `atenciones` genérica (ej. `atenciones` como tabla polimórfica o de registro de eventos).
        *   Desarrollar módulos de reporte y consulta que utilicen los datos estructurados para generar los indicadores de la Resolución 3280.

### 3.2. Recomendación Arquitectónica de Alto Nivel

Como equipo experto en bases de datos y arquitectura de software, nuestra recomendación de mayor nivel para la persistencia de datos y la articulación con la Resolución 3280 es la siguiente:

**Principio Arquitectónico Central: Evolución de la Tabla `atenciones` hacia un Registro de Eventos Polimórfico.**

En lugar de intentar que la tabla `atenciones` contenga *todos* los campos posibles para *todos* los tipos de atención (lo que la haría enorme y llena de nulos), recomendamos que `atenciones` se convierta en una tabla de **registro de eventos de alto nivel**.

-   **`atenciones` (Tabla Principal):** Contendrá los campos comunes a *todas* las atenciones (ej. `id`, `paciente_id`, `medico_id`, `fecha_atencion`, `entorno`, `creado_en`, `updated_at`). Además, tendrá una columna `tipo_atencion` (ej. "Valoración Primera Infancia", "Tamizaje Oncológico", "Consulta General") y una columna `detalle_id` que será una clave foránea a la tabla específica de detalles.
-   **Tablas de Detalle Especializadas:** Crearemos tablas separadas para cada tipo de atención especializada (ej. `atencion_primera_infancia_detalles`, `atencion_oncologica_detalles`). Estas tablas contendrán los campos específicos y estructurados que exige la resolución para ese tipo de atención.

**Ventajas de este enfoque:**
-   **Claridad y Organización:** Cada tipo de atención tiene su propio esquema claro.
-   **Eficiencia:** La tabla principal `atenciones` se mantiene ligera, y las tablas de detalle solo almacenan los datos relevantes para su tipo.
-   **Escalabilidad:** Es fácil añadir nuevos tipos de atención sin modificar la tabla principal.
-   **Cumplimiento Normativo:** Permite capturar la granularidad de datos que la Resolución 3280 exige para sus indicadores.
