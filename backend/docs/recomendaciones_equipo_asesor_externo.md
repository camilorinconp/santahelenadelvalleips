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
                *   **Endpoints API:** Desarrollar endpoints específicos para cada sub-intervención, asegurando la correcta vinculación polimórfica con la tabla `atenciones` general.
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

### 3.2. Recomendación Arquitectónica de Alto Nivel

**Principio Arquitectónico Central: Evolución de la Tabla `atenciones` hacia un Registro de Eventos Polimórfico.**

-   **`atenciones` (Tabla Principal):** Contendrá los campos comunes a *todas* las atenciones (ej. `id`, `paciente_id`, `medico_id`, `fecha_atencion`, `entorno`, `creado_en`, `updated_at`). Además, tendrá una columna `tipo_atencion` (ej. "Valoración Primera Infancia", "Tamizaje Oncológico", "Control Cronicidad - Hipertensión", "IVE") y una columna `detalle_id` que será una clave foránea a la tabla específica de detalles.
-   **Tablas de Detalle Especializadas:** Crearemos tablas separadas para cada tipo de atención especializada (ej. `atencion_primera_infancia_detalles`, `atencion_oncologica_cuello_uterino_detalles`, `control_hipertension_detalles`, `ive_detalles`). Estas tablas contendrán los campos específicos y estructurados que exige la resolución para ese tipo de atención.

**Ventajas de este enfoque:**
-   **Claridad y Organización:** Cada tipo de atención tiene su propio esquema claro.
-   **Eficiencia:** La tabla principal `atenciones` se mantiene ligera, y las tablas de detalle solo almacenan los datos relevantes para su tipo.
-   **Escalabilidad:** Es fácil añadir nuevos tipos de atención sin modificar la tabla principal.
-   **Cumplimiento Normativo:** Permite capturar la granularidad de datos que la Resolución 3280 exige para sus indicadores.

## 4. Seguimiento del Avance del Proyecto

Este documento sirve como una guía viva para el progreso del proyecto, asegurando la trazabilidad y la claridad para cualquier miembro del equipo.

**Objetivo:** Alcanzar el 100% de implementación de los requisitos de datos y reportes de la Resolución 3280.

**Estado General:** En progreso.

### 4.1. Fase 1: Consolidación de RIAS Individuales Clave

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Definir e implementar `AtencionPrimeraInfancia` | **Completado** | Modelo Pydantic, tabla DB, rutas API y pruebas implementadas y pasando. | `models/atencion_primera_infancia_model.py`, `routes/atencion_primera_infancia.py`, `tests/test_atencion_primera_infancia.py` | 2025-09-08 |
| Definir e implementar `AtencionMaternoPerinatal` (Básico) | **Completado** | Modelo Pydantic, tabla DB, rutas API y pruebas implementadas y pasando para la estructura básica. | `models/atencion_materno_perinatal_model.py`, `routes/atencion_materno_perinatal.py`, `tests/test_atencion_materno_perinatal.py` | 2025-09-08 |
| **Implementación Completa de `ControlCronicidad`** | **En Progreso (Refactorización Necesaria)** | Modelos de detalle (`control_hipertension_model.py`, `control_diabetes_model.py`, `control_erc_model.py`, `control_dislipidemia_model.py`) existen. La ruta `routes/control_cronicidad.py` necesita refactorización para implementar el flujo polimórfico correcto (creación de detalle específico -> `control_cronicidad` -> `atenciones`). | `models/control_cronicidad_model.py`, `models/control_hipertension_model.py`, `models/control_diabetes_model.py`, `models/control_erc_model.py`, `models/control_dislipidemia_model.py`, `routes/control_cronicidad.py` | 2025-09-10 |
| **Implementación Completa de `TamizajeOncologico`** | **Pendiente (Refactorización de Modelado Potencial)** | Modelo general (`tamizaje_oncologico_model.py`) y ruta (`routes/tamizaje_oncologico.py`) existen. Se requiere evaluar la creación de modelos de detalle específicos para cada tipo de cáncer (cuello uterino, mama, próstata, colon y recto) para una implementación polimórfica completa. | `models/tamizaje_oncologico_model.py`, `routes/tamizaje_oncologico.py` | 2025-09-10 |
| **Implementación Detallada de la Ruta Materno Perinatal (RIAMP)** | **Pendiente (Gran Alcance)** | La `resolucion_3280_de_2018_limpio.md` detalla extensamente sub-intervenciones como Preconcepcional, IVE, Prenatal, Parto, Puerperio, Recién Nacido y Complicaciones del Recién Nacido. Esto representa un gran volumen de trabajo pendiente para modelado de datos, lógica de negocio y endpoints API. | `models/atencion_materno_perinatal_model.py`, `routes/atencion_materno_perinatal.py`, `resolucion_3280_de_2018_limpio.md` (Secciones 4.1 a 4.11) | 2025-09-10 |
| **Otras Atenciones Individuales** | Pendiente | Identificación de otros tipos de atención individual que requieran especialización, según la Resolución 3280. | N/A | 2025-09-10 |

### 4.2. Fase 2: Consolidación de Intervenciones Colectivas

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Definir e implementar `IntervencionColectiva` | **Completado** | Modelo Pydantic, tabla DB, rutas API básicas y pruebas implementadas y pasando. CRUD expandido. | `models/intervencion_colectiva_model.py`, `routes/intervenciones_colectivas.py`, `tests/test_intervenciones_colectivas.py` | 2025-09-09 |
| Especializar tipos de `IntervencionColectiva` | Pendiente | Análisis inicial de la necesidad de especialización, según la sección 3.2 de la Resolución 3280. | N/A | 2025-09-10 |

### 4.3. Fase 3: Integración y Análisis Transversal de Datos

| Tarea | Estado | Avance Actual | Archivos Clave | Fecha Última Actualización |
| :--- | :--- | :--- | :--- | :--- |
| Refinar manejo de `entornos` | Pendiente | `entorno` añadido como campo `TEXT` en `atenciones`. Se requiere definir una tabla `Entornos` con tipos predefinidos y una FK. | `models/atencion_model.py` | 2025-09-10 |
| **Implementación Detallada de `Educación y Comunicación para la Salud`** | **Pendiente** | Requiere modelado de datos para contenidos educativos, registro de asistencia y seguimiento de capacidades desarrolladas, según la Sección 16 de la Resolución 3280. | N/A | 2025-09-10 |
| **Implementación Detallada de `Atención a la Familia`** | **Pendiente** | Requiere modelado de datos para la valoración familiar (Familiograma, APGAR familiar, Ecomapa, Zarit Scale) y las atenciones de orientación y educación familiar, según la Sección 15 de la Resolución 3280. | N/A | 2025-09-10 |
| **Desarrollo de Módulos de Monitoreo y Evaluación** | **Pendiente** | Requiere asegurar que los modelos de datos de todas las RIAS contengan los campos necesarios para calcular los **Indicadores de Resultado** e **Indicadores de Proceso** (Capítulo 6 de la Resolución 3280). Desarrollar lógica para la agregación y reporte. | N/A | 2025-09-10 |
| **Consideraciones de Adaptabilidad** | **Pendiente** | Requiere identificar campos en los modelos que permitan registrar particularidades poblacionales y territoriales (etnia, discapacidad, género, ruralidad) y diseñar mecanismos para la configuración de reglas de negocio o flujos de trabajo diferenciados (Capítulo 7 de la Resolución 3280). | N/A | 2025-09-10 |

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
