# Contexto del Proyecto: API para IPS Santa Helena del Valle

Este documento proporciona el contexto esencial para la asistencia de IA en este proyecto.

### 1. Propósito y Dominio
El proyecto es una API REST para una Institución Prestadora de Salud (IPS) en Colombia. Su objetivo es gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana, específicamente la **Resolución 3280 de 2018**. El lenguaje, los modelos de datos y la lógica de negocio deben ser consistentes con el dominio de la salud en Colombia.

### 2. Stack Tecnológico Principal
- **Backend:** Python
- **Framework:** FastAPI
- **Validación de Datos:** Pydantic
- **Base de Datos:** PostgreSQL (gestionada a través de Supabase)
- **Pruebas:** Pytest

### 3. Fuentes de la Verdad (Lectura Obligatoria)
Para cualquier cambio, consulta o propuesta, referirse a los siguientes documentos en orden de prioridad:

1.  **`backend/docs/resolucion_3280_de_2018_limpio.md`**: La fuente de la verdad **normativa**. Define todos los requisitos de datos, lógica y flujos.
2.  **`docs/01-ARCHITECTURE-GUIDE.md`**: La fuente de la verdad **arquitectónica**. Detalla los patrones de diseño, la estructura de la base de datos y las decisiones técnicas.
3.  **`docs/recomendaciones_equipo_asesor_externo.md`**: Guía complementaria con recomendaciones estratégicas y el roadmap de implementación.
4.  **`ROADMAP.md`**: Hoja de ruta ejecutiva del proyecto.
5.  **`CHANGELOG.md`**: Historial de cambios y versiones.

### 4. Arquitectura de Datos Clave: Atenciones Polimórficas
Las atenciones médicas siguen un patrón de diseño polimórfico anidado para manejar la complejidad y granularidad de la Resolución 3280.

-   **Nivel 1 (Evento Principal):** La tabla `atenciones` es el registro de alto nivel, con datos comunes.
-   **Nivel 2 (Tipo de Atención):** Tablas de "detalle" por cada tipo de atención (ej. `atencion_materno_perinatal`).
-   **Nivel 3 (Sub-evento):** Tablas de "sub-detalle" para fases específicas (ej. `detalle_control_prenatal`, `detalle_parto`).

**Flujo de Creación (Ej: Control Prenatal):**
1.  Crear registro en la tabla de sub-detalle (`detalle_control_prenatal`).
2.  Crear registro en la tabla de detalle (`atencion_materno_perinatal`), apuntando al sub-detalle.
3.  Crear registro en la tabla principal (`atenciones`), apuntando al detalle.

### 5. Estrategia de Tipado de Datos
Para maximizar la consistencia y la utilidad analítica, se sigue una estrategia de 3 capas:

1.  **Estandarización (ENUMs / Catálogos):**
    -   **ENUMs de PostgreSQL:** Para listas de valores **pequeñas y estables** (ej. `tipo_parto`, `riesgo_biopsicosocial`).
    -   **Tablas de Catálogo (FK):** Para listas **grandes o dinámicas** (ej. códigos CIE-10, CUPS).
2.  **Semi-Estructurado (JSONB):**
    -   Para checklists, grupos de hallazgos o datos con variabilidad (ej. `signos_de_alarma`, `sintomas_preeclampsia`).
3.  **Texto Libre (TEXT):**
    -   Exclusivamente para datos narrativos no estructurados (ej. `observaciones`, `resumen_complicaciones`). Ideal para futuras integraciones con IA/RAG.

### 6. Procedimiento de Pruebas
-   Toda nueva funcionalidad debe estar cubierta por pruebas en `tests/`.
-   El framework es `pytest`.
-   Las pruebas deben ser autocontenidas, creando y eliminando sus propios datos.
-   **Comando de ejecución:** `pytest -v`

### 7. Flujo de Trabajo para Implementación de Rutas
El desarrollo sigue un ciclo iterativo por cada RIAS o sub-ruta:
1.  **Análisis de la Resolución 3280:** Identificar todos los requisitos de datos y lógica.
2.  **Diseño de Base de Datos:** Modelar tablas aplicando polimorfismo y la estrategia de tipado. Crear migraciones.
3.  **Implementación de Backend:** Desarrollar modelos Pydantic, endpoints y lógica de negocio.
4.  **Pruebas de Backend:** Escribir y ejecutar tests exhaustivos con `pytest`.
5.  **Implementación de Frontend:** (Posterior a la estabilización del backend) Desarrollar la UI.
6.  **Validación Integral:** Revisión completa del flujo desde la UI hasta la BD.

### 8. Idioma de Interacción
La comunicación con el asistente de IA y toda la terminología del proyecto debe ser en **español**.