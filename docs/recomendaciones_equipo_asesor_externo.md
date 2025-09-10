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
    *   **Avance Actual:** Modelo `AtencionPrimeraInfancia` y `AtencionMaternoPerinatal` definidos e implementados.
    *   **Próximos Pasos:**
        *   Crear la tabla `atencion_primera_infancia` en Supabase (con sus triggers y RLS).
        *   Implementar las rutas API (CRUD) para `AtencionPrimeraInfancia`.
        *   Escribir pruebas unitarias y de integración para `AtencionPrimeraInfancia`.
        *   Crear la tabla `atencion_materno_perinatal` en Supabase (con sus triggers y RLS).
        *   Implementar las rutas API (CRUD) para `AtencionMaternoPerinatal`.
        *   Escribir pruebas unitarias y de integración para `AtencionMaternoPerinatal`.
        *   **A Futuro:** Identificar otros tipos de atención individual que requieran especialización (ej. `TamizajeOncologico`, `ControlCronicidad`) y repetir el proceso.

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

**Nota de Priorización (2025-09-09):** Por decisión del equipo, se priorizará el inicio de la **Fase 3 (Integración y Análisis Transversal de Datos)**, específicamente la implementación de la arquitectura polimórfica para las atenciones individuales. Esta decisión se basa en que dicha arquitectura es el pilar técnico fundamental para la futura generación de indicadores y reportes, siendo el cambio de mayor impacto estratégico para el proyecto. Las tareas restantes de la Fase 2, como la especialización de `IntervencionColectiva`, se posponen para una futura intervención.

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

## 4. Seguimiento del Avance del Proyecto

Este documento sirve como una guía viva para el progreso del proyecto, asegurando la trazabilidad y la claridad para cualquier miembro del equipo.

**Objetivo:** Alcanzar el 100% de implementación de los requisitos de datos y reportes de la Resolución 3280.

**Estado General:** En progreso.

### 4.1. Fase 1: Especialización de Atenciones Individuales Clave

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Definir e implementar `AtencionPrimeraInfancia` | **Completado** | Modelo Pydantic, tabla DB, rutas API y pruebas implementadas y pasando. | `models/atencion_primera_infancia_model.py`, `routes/atencion_primera_infancia.py`, `tests/test_atencion_primera_infancia.py` | 2025-09-08 |
| Definir e implementar `AtencionMaternoPerinatal` | **Completado** | Modelo Pydantic, tabla DB, rutas API y pruebas implementadas y pasando. | `models/atencion_materno_perinatal_model.py`, `routes/atencion_materno_perinatal.py`, `tests/test_atencion_materno_perinatal.py` | 2025-09-08 |
| Definir e implementar `TamizajeOncologico` | Pendiente | Análisis inicial de requisitos de la Resolución 3280. | N/A | 2025-09-08 |
| Definir e implementar `ControlCronicidad` | Pendiente | Análisis inicial de requisitos de la Resolución 3280. | N/A | 2025-09-08 |
| **Otras Atenciones Individuales** | Pendiente | Identificación de otros tipos de atención individual que requieran especialización. | N/A | 2025-09-08 |

### 4.2. Fase 2: Consolidación de Intervenciones Colectivas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Definir e implementar `IntervencionColectiva` | **Completado** | Modelo Pydantic, tabla DB, rutas API básicas y pruebas implementadas y pasando. | `models/intervencion_colectiva_model.py`, `routes/intervenciones_colectivas.py`, `tests/test_intervenciones_colectivas.py` | 2025-09-08 |
| Expandir CRUD para `IntervencionColectiva` | **Completado** | Implementados endpoints GET (todos, por ID, por filtro), POST, PUT y DELETE. | `routes/intervenciones_colectivas.py`, `tests/test_intervenciones_colectivas.py` | 2025-09-09 |
| Especializar tipos de `IntervencionColectiva` | Pendiente | Análisis inicial de la necesidad de especialización. | N/A | 2025-09-08 |

### 4.3. Fase 3: Integración y Análisis Transversal de Datos

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Refinar manejo de `entornos` | Pendiente | `entorno` añadido como campo `TEXT` en `atenciones`. | `models/atencion_model.py` | 2025-09-08 |
| Diseñar estrategia de vinculación `atenciones` (polimórfica) | Pendiente | Propuesta arquitectónica definida. | `docs/recomendaciones_equipo_asesor_externo.md` | 2025-09-08 |
| Desarrollar módulos de reporte y consulta | Pendiente | Análisis de requisitos de indicadores de la Resolución 3280. | N/A | 2025-09-08 |

### 4.4. Fase 4: Lógica de Negocio y Reglas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Implementar validaciones específicas de la Resolución 3280 | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar flujos de trabajo y lógica de remisión | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar lógica de cálculo de indicadores | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar gestión de "Plan de Cuidado" | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |

### 4.5. Fase 5: Reportes y Analíticas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Desarrollar servicios de agregación de datos | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar endpoints de reportes | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |

### 4.6. Fase 6: Seguridad

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Implementar gestión de usuarios y roles | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar políticas RLS granulares | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |
| Implementar autorización en la API | Pendiente | Análisis de requisitos. | N/A | 2025-09-08 |

### 4.7. Fase 7: Interfaz de Usuario (UI)

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Diseño e implementación de UI | Pendiente | N/A | N/A | 2025-09-08 |

## NOTA IMPORTANTE: Estrategia de Documentación y Colaboración (2025-09-10)

Estimado Equipo Consultor Externo,

Para optimizar nuestra colaboración y asegurar la máxima eficiencia en el proyecto "Santa Helena del Valle IPS", hemos formalizado una estrategia clara de documentación y flujo de trabajo.

**Su rol como Equipo Consultor Externo es crucial y se centra en la guía estratégica y el aseguramiento de la calidad arquitectónica.**

### Reglas Claras para la Colaboración y Documentación:

1.  **No Modifican Código Directamente:** Su valiosa experiencia se canaliza a través de la asesoría y revisión, no mediante la implementación directa en el repositorio.
2.  **Revisión de Pull Requests (PRs):** Son revisores obligatorios en todos nuestros PRs. Su foco es la **alineación arquitectónica, la robustez, la escalabilidad y el cumplimiento de la Resolución 3280**.
3.  **Su Guía Documental Maestra: Este Documento (`docs/recomendaciones_equipo_asesor_externo.md`)**
    *   **Propósito:** Este archivo es su principal canal de comunicación y su "guía documental". Todas sus **recomendaciones, directrices, lecciones aprendidas de alto nivel, decisiones arquitectónicas y el roadmap estratégico** deben plasmarse y mantenerse actualizadas aquí.
    *   **Cómo Contribuir:** Para añadir o modificar contenido en este documento, por favor, háganlo a través de un **Pull Request**. Este PR será revisado por nuestro equipo, sirviendo como un paso de verificación formal antes de que la directriz se considere oficial.
4.  **Propuestas y Discusiones Previas:**
    *   Para ideas o propuestas que requieran discusión antes de ser formalizadas en este documento, por favor, inicien un **GitHub Issue** o un **Tema de Discussion** en el repositorio. Esto permite una colaboración transparente y con trazabilidad, identificando claramente a cada participante.

**En resumen:**
*   **Para directrices estratégicas y arquitectónicas:** Pull Request a este documento (`docs/recomendaciones_equipo_asesor_externo.md`).
*   **Para discusiones y propuestas:** GitHub Issues o Discussions.
*   **Para el código y su documentación interna (README.md, docstrings):** Responsabilidad del Equipo Principal.

Esta estructura asegura que su valiosa guía estratégica sea el pilar del proyecto, con un proceso claro para su incorporación y validación.

Agradecemos su compromiso y colaboración para hacer de este proyecto un éxito.