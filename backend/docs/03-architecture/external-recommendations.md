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

**Estrategia:** Evolucionar el modelo de `Atenciones` de un registro genérico a un sistema que soporte tipos de atención especializados, manteniendo la flexibilidad y la trazabilidad, con un enfoque polimórfico.

**Fases de Implementación:**

1.  **Fase 1: Consolidación de RIAS Individuales Clave (Basado en Resolución 3280)**
    *   **Objetivo:** Implementar completamente las RIAS individuales prioritarias, asegurando la granularidad de datos y la lógica polimórfica según la Resolución 3280.
    *   **Tareas:**
        *   **1.1. Implementación Completa de `ControlCronicidad` (Prioridad Alta)**
            *   **Descripción:** Desarrollar los modelos de datos, la lógica de negocio y los endpoints API para la gestión polimórfica de los controles de cronicidad (Hipertensión, Diabetes, ERC, Dislipidemia), según las especificaciones de la Resolución 3280.
            *   **Acciones Clave:**
                *   **Modelado de Datos:** Confirmar/ajustar modelos Pydantic para `ControlCronicidad` (general) y sus tablas de detalle específicas (`ControlHipertensionDetalles`, `ControlDiabetesDetalles`, `ControlERCDetalles`, `ControlDislipidemiaDetalles`), incluyendo todos los campos de anamnesis, examen físico, paraclínicos y plan de cuidado mencionados en la resolución para estas condiciones.
                *   **Refactorización de Lógica de Creación:** Ajustar el endpoint `POST /control-cronicidad/` en `routes/control_cronicidad.py` para implementar el flujo polimórfico correcto:
                    1.  Insertar el registro en la tabla de **detalles específica** (ej. `control_hipertension_detalles`).
                    2.  Obtener el `id` del registro de detalle (`detalle_cronicidad_id`).
                    3.  Crear el registro en la tabla `control_cronicidad`, utilizando el `detalle_cronicidad_id` obtenido y el `tipo_cronicidad` correspondiente.
                    4.  Crear/Actualizar la entrada genérica en la tabla `atenciones`, vinculándola con el `id` del registro de `control_cronicidad` a través de `detalle_id` y `tipo_atencion` (ej. "Control Cronicidad - Hipertensión").
                *   **Endpoints de Consulta:** Asegurar/desarrollar endpoints para consultar los detalles específicos de cronicidad, posiblemente utilizando el `detalle_cronicidad_id` del registro general.
                *   **Pruebas:** Escribir pruebas unitarias y de integración exhaustivas para validar el flujo polimórfico y las reglas de negocio.
        *   **1.2. Implementación Completa de `TamizajeOncologico` (Prioridad Alta)**
            *   **Descripción:** Desarrollar los modelos de datos, la lógica de negocio y los endpoints API para los tamizajes de cáncer de Cuello Uterino, Mama, Próstata y Colon y Recto, siguiendo las secciones 9, 10, 11 y 12 de la Resolución 3280.
            *   **Acciones Clave:**
                *   **Modelado de Datos (Refactorización Potencial):** Evaluar la necesidad de crear modelos de detalle específicos para cada tipo de tamizaje oncológico (ej., `TamizajeCuelloUterinoDetalles`, `TamizajeMamaDetalles`) para una implementación verdaderamente polimórfica y granular, similar al enfoque de `ControlCronicidad`. Si se decide por esta refactorización, ajustar el modelo `TamizajeOncologico` actual para que actúe como un "padre" polimórfico.
                *   **Lógica de Negocio:** Implementar reglas para la frecuencia de tamizajes por edad y riesgo, criterios de positividad, y flujos de remisión para pruebas confirmatorias o manejo, según la resolución.
                *   **Endpoints API:** Desarrollar/ajustar endpoints para la gestión de cada tipo de tamizaje, considerando el flujo polimórfico si se refactoriza el modelado.
                *   **Pruebas:** Asegurar cobertura de pruebas para todos los flujos.
        *   **1.3. Implementación Detallada de la Ruta Materno Perinatal (RIAMP) (Prioridad Muy Alta)**
            *   **Descripción:** Implementar las sub-intervenciones de la RIAMP (Preconcepcional, IVE, Prenatal, Parto, Puerperio, Recién Nacido, Complicaciones del Recién Nacido) con la granularidad y protocolos detallados en la Resolución 3280 (Secciones 4.1 a 4.11).
            *   **Acciones Clave:**
                *   **Modelado de Datos:** Crear/ajustar modelos Pydantic y tablas de base de datos para cada sub-intervención, capturando todos los campos de anamnesis, examen físico, paraclínicos, escalas, medicamentos, procedimientos y planes de cuidado específicos.
                *   **Lógica de Negocio:** Implementar la lógica de negocio para cada sub-intervención, incluyendo validaciones, flujos de derivación, manejo de emergencias, y adherencia a los tiempos y protocolos definidos en la resolución.
                *   **Endpoints API:** Desarrollar/ajustar endpoints específicos para cada sub-intervención, asegurando la correcta vinculación polimórfica con la tabla `atenciones` general.
                *   **Pruebas:** Desarrollar un conjunto exhaustivo de pruebas unitarias y de integración para cada sub-intervención.

2.  **Fase 2: Consolidación de Intervenciones Colectivas**
    *   **Objetivo:** Desarrollar completamente el soporte para intervenciones dirigidas a grupos y comunidades.
    *   **Avance Actual:** Modelo `IntervencionColectiva`, tabla y rutas básicas implementadas y CRUD expandido.
    *   **Próximos Pasos:**
        *   Considerar la necesidad de especializar `IntervencionColectiva` si surgen tipos muy distintos (ej. `JornadaSaludComunitaria` vs. `CampañaVacunacion`), basándose en la sección 3.2 de la Resolución 3280.

3.  **Fase 3: Integración y Análisis Transversal de Datos**
    *   **Objetivo:** Asegurar que todos los datos (individuales y colectivos) puedan ser consultados y analizados de forma coherente para generar los indicadores de la resolución.
    *   **Tareas:**
        *   **3.1. Refinar manejo de `entornos`:** (ej. crear una tabla `Entornos` con tipos predefinidos y una FK).
        *   **3.2. Implementación Detallada de `Educación y Comunicación para la Salud` (Sección 16 de la Resolución):**
            *   **Descripción:** Modelar los contenidos educativos por momento de curso de vida y tipo de intervención, permitiendo el registro de la participación en sesiones individuales, grupales y colectivas.
            *   **Acciones:** Crear modelos para contenidos educativos, registro de asistencia, y seguimiento de capacidades desarrolladas.
        *   **3.3. Implementación Detallada de `Atención a la Familia` (Sección 15 de la Resolución):**
            *   **Descripción:** Modelar la valoración familiar (Familiograma, APGAR familiar, Ecomapa, Zarit Scale) y las atenciones de orientación y educación familiar.
            *   **Acciones:** Crear modelos para la valoración familiar y los registros de las intervenciones.
        *   **3.4. Desarrollo de Módulos de Monitoreo y Evaluación (Capítulo 6 de la Resolución):**
            *   **Descripción:** Implementar la recolección de datos para todos los **Indicadores de Resultado** e **Indicadores de Proceso** de la RPMS y RIAMP, según las tablas detalladas en la resolución.
            *   **Acciones:** Asegurar que los modelos de datos de todas las RIAS contengan los campos necesarios para calcular estos indicadores. Desarrollar lógica para la agregación y reporte de estos indicadores.
        *   **3.5. Consideraciones de Adaptabilidad (Capítulo 7 de la Resolución):**
            *   **Descripción:** Asegurar que el diseño del sistema permita la adaptabilidad a diferentes contextos poblacionales y territoriales (etnia, discapacidad, género, ruralidad).
            *   **Acciones:** Identificar campos en los modelos que permitan registrar estas particularidades y, si es necesario, diseñar mecanismos para la configuración de reglas de negocio o flujos de trabajo diferenciados.

### 4.4. Fase 4: Lógica de Negocio y Reglas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Implementar validaciones específicas de la Resolución 3280 | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar flujos de trabajo y lógica de remisión | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar lógica de cálculo de indicadores | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar gestión de "Plan de Cuidado" | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |

### 4.5. Fase 5: Reportes y Analíticas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Desarrollar servicios de agregación de datos | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar endpoints de reportes | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |

### 4.6. Fase 6: Seguridad

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Implementar gestión de usuarios y roles | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar políticas RLS granulares | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |
| Implementar autorización en la API | Pendiente | Análisis de requisitos. | N/A | 2025-09-10 |

### 4.7. Fase 7: Interfaz de Usuario (UI)

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Diseño e implementación de UI | Pendiente | N/A | N/A | 2025-09-10 |

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

### 4.8. Resumen de Avances Recientes del Esquema

Hemos completado la refactorización y el refinamiento de la Ruta Materno Perinatal, aplicando la estrategia de polimorfismo anidado y el tipado de datos.

-   **Consolidación de directorios `supabase`:** Se unificaron las configuraciones y migraciones de Supabase en la raíz del proyecto.
-   **Sincronización de la base de datos:** Se resolvió la inconsistencia entre el esquema local y el remoto, reconstruyendo la base de datos en la nube a partir de las migraciones locales.
-   **Refactorización de `atencion_materno_perinatal`:** Implementación de polimorfismo anidado de primer nivel, creando tablas de sub-detalle (`detalle_control_prenatal`, `detalle_parto`, `detalle_recien_nacido`, `detalle_puerperio`).
-   **Refinamiento de `detalle_control_prenatal`:** Se añadieron campos de granularidad y se tiparon con `ENUMs` y `JSONB` (incluyendo polimorfismo anidado de segundo nivel para `anamnesis`, `paraclinicos`, `antropometria`).
-   **Refinamiento de `detalle_parto`:** Se añadieron campos de granularidad y se tiparon con `ENUMs` y `JSONB`.
-   **Refinamiento de `detalle_recien_nacido`:** Se añadió polimorfismo anidado de segundo nivel (`detalle_rn_atencion_inmediata`) y se tiparon campos con `ENUMs` y `JSONB`.
-   **Refinamiento de `detalle_puerperio`:** Se añadieron campos de granularidad y se tiparon con `ENUMs` y `JSONB`.
-   **Creación de tablas de detalle faltantes para MP:** Se crearon `detalle_salud_bucal_mp`, `detalle_nutricion_mp`, `detalle_ive`, `detalle_curso_maternidad_paternidad`, `detalle_seguimiento_rn`.
-   **Estrategia de Tipado de Datos:** Se formalizó el uso de Catálogos/ENUMs para estandarización, TEXT para narrativas y JSONB para datos semi-estructurados, validando la preparación para IA/RAG.