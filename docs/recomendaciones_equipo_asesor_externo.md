# Recomendaciones del Equipo Asesor Externo

Este documento centraliza las lecciones aprendidas y buenas prácticas identificadas durante el desarrollo del proyecto, para que sirvan como guía en este y futuros proyectos.

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