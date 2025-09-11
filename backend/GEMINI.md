# Contexto del Proyecto: API para IPS Santa Helena del Valle

Este documento proporciona el contexto esencial para la asistencia de IA en este proyecto.

### 1. Propósito y Dominio
El proyecto es una API REST para una Institución Prestadora de Salud (IPS) en Colombia. Su objetivo es gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana, específicamente la Resolución 3280. El lenguaje, los modelos de datos y la lógica de negocio deben ser consistentes con el dominio de la salud en Colombia.

### 2. Stack Tecnológico Principal
- **Backend:** Python
- **Framework:** FastAPI
- **Validación de Datos:** Pydantic
- **Base de Datos:** PostgreSQL (gestionada a través de Supabase)
- **Pruebas:** Pytest

### 3. Fuente de la Verdad para Convenciones y Arquitectura
El archivo `docs/recomendaciones_equipo_asesor_externo.md` es la guía principal y la fuente de la verdad para:
- La arquitectura de datos.
- Los patrones de diseño de la base de datos.
- El roadmap de implementación del proyecto.
**Este documento debe ser consultado antes de proponer o realizar cambios estructurales.**

### 4. Arquitectura de Datos Clave: Atenciones Polimórficas
Las atenciones médicas siguen un patrón de diseño polimórfico para evitar tablas sobrecargadas y mantener la flexibilidad.
- La tabla `atenciones` funciona como un registro de eventos de alto nivel, conteniendo datos comunes a todas las atenciones.
- Cada tipo de atención especializada (ej. `AtencionPrimeraInfancia`) tiene su propia tabla de "detalles" (ej. `atencion_primera_infancia`).
- **Flujo de Creación:** Al crear una nueva atención especializada:
    1.  Se debe insertar el registro en la tabla de **detalles específica**.
    2.  Se debe crear un registro en la tabla `atenciones` que contenga una referencia al detalle a través de los campos `detalle_id` (la FK) y `tipo_atencion` (un string descriptivo, ej: "Atencion Primera Infancia").

### 5. Procedimiento de Pruebas
- Todas las nuevas funcionalidades, endpoints o modificaciones de lógica deben estar cubiertas por pruebas automatizadas.
- Las pruebas se encuentran en el directorio `/tests`.
- El framework utilizado es `pytest`.
- Las pruebas deben ser autocontenidas, creando y eliminando sus propios datos de prueba para no depender del estado de la base de datos.

### 6. Idioma de Interacción
La comunicación con el usuario debe realizarse preferentemente en **español**.

### 7. Estrategia de Diseño Detallado: Polimorfismo Anidado y Tipado de Datos
Para manejar la alta granularidad exigida por la Resolución 3280 y asegurar una base de datos escalable y preparada para el futuro (IA, RAG), se ha definido la siguiente estrategia de diseño detallado:

#### a. Polimorfismo Anidado
Cuando una tabla de "detalles" (como `atencion_materno_perinatal`) se vuelve demasiado grande y representa múltiples sub-eventos, aplicaremos el mismo patrón polimórfico un nivel más abajo.
- La tabla de detalle principal se mantiene "delgada", conteniendo solo FKs y campos comunes.
- Se crean nuevas tablas de "sub-detalle" para cada fase o sub-evento lógico (ej. `detalle_control_prenatal`, `detalle_parto`).
- La tabla de detalle principal utiliza un `sub_tipo_atencion` (TEXT) y un `sub_detalle_id` (UUID) para apuntar al sub-detalle correspondiente.
- **Beneficios:** Se evita tener tablas excesivamente anchas con muchas columnas nulas, se aumenta la claridad del esquema y se mejora la flexibilidad.

#### b. Estrategia de Manejo de Datos
Para los campos de datos, especialmente aquellos que podrían ser texto libre, se seguirá una estrategia de 3 capas para maximizar la consistencia y la utilidad analítica:

1.  **Capa 1: Estandarización (Máxima Prioridad):** Para campos con un conjunto finito y predecible de opciones (ej. niveles de riesgo, tipos de parto, resultados de tamizajes sí/no/reactivo), se utilizarán **Tablas de Catálogo** (con Foreign Keys) o, en su defecto, tipos **ENUM** de PostgreSQL. Esto garantiza la integridad de los datos y facilita enormemente las consultas y la creación de interfaces.

2.  **Capa 2: Texto Libre (`TEXT`):** Se reserva exclusivamente para datos que son inherentemente narrativos y no estructurados, como `observaciones`, `resumen_complicaciones`, o notas del médico. Estos campos son el objetivo principal para futuras integraciones con sistemas RAG y búsqueda semántica.

3.  **Capa 3: Semi-Estructurado (`JSONB`):** Para grupos de hallazgos o checklists (ej. `signos_de_alarma`), se puede utilizar un campo de tipo `JSONB`. Esto permite agrupar datos relacionados de forma flexible (ej. `{"sangrado": true, "cefalea": false}`) sin necesidad de añadir múltiples columnas booleanas, facilitando la evolución del esquema y manteniendo la capacidad de realizar consultas internas sobre estos datos.

#### c. Integración de Recomendaciones de Expertos y Refinamiento de Tipado
Hemos revisado las recomendaciones de un equipo experto en bases de datos, las cuales validan y complementan nuestra estrategia. La integración clave se centra en el manejo de tipos de datos:

- **Catálogos Normalizados:** Se priorizarán para listas de valores **grandes, dinámicas, o que requieran metadatos adicionales** (ej. códigos CUPS, CIE-10, medicamentos). Esto permite una mayor flexibilidad y gestión externa de los catálogos.

- **Tipos ENUM de PostgreSQL:** Se utilizarán para listas de valores **pequeñas, estables y fijas** (ej. `tipo_parto`, `riesgo_biopsicosocial`, resultados de tamizajes con pocas opciones predefinidas como 'REACTIVO'/'NO_REACTIVO'). Esto ofrece eficiencia y simplicidad para conjuntos de datos que no cambian frecuentemente.

- **JSONB:** Se reafirma su uso para datos **semi-estructurados o de alta variabilidad** (ej. `sintomas_preeclampsia_premonitorios`, `signos_vitales_maternos`). Permite flexibilidad sin sacrificar la capacidad de consulta estructurada.

Esta aproximación híbrida optimiza la integridad, flexibilidad y preparación para futuras integraciones con IA (RAG, LLM), asegurando que los datos estén modelados de la forma más útil posible.

### 8. Resumen de Avances Recientes del Esquema

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