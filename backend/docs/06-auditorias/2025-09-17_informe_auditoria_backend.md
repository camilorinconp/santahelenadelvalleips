# Informe de Auditoría de Backend (Versión Final Consolidada)

- **Fecha:** 2025-09-17
- **Auditor:** Equipo Consultor Externo (Gemini)
- **Alcance:** Arquitectura de Backend, con foco en los módulos de creación de atenciones y su alineación con la normativa.

---

## 1. Resumen Ejecutivo

El backend del proyecto demuestra una **intención de diseño robusta y alineada con la normativa** (Resolución 3280), especialmente en el modelado de datos, que es de una granularidad y fidelidad excelentes. Sin embargo, esta fortaleza se ve críticamente comprometida por un **defecto de diseño sistémico en la capa de acceso a datos**: la ausencia de transacciones atómicas. Este fallo, repetido en todos los módulos de atención, introduce un riesgo muy alto de corrupción de datos.

Adicionalmente, la auditoría revela una **severa inconsistencia arquitectónica**, con al menos **tres patrones de diseño distintos** para modelar datos, y una lógica de negocio fragmentada en múltiples capas (rutas, modelos). La necesidad de cumplir con la **Resolución 202** (reportería) parece haber influido en estas decisiones de diseño ad-hoc. La remediación de estos problemas estructurales es de **máxima prioridad** para asegurar la fiabilidad y mantenibilidad del proyecto.

---

## 2. Alcance y Metodología

La auditoría se centró en el código fuente del directorio `backend/`. La metodología incluyó:

- Análisis estático de la estructura de directorios y archivos.
- Revisión detallada de los patrones de diseño en los módulos de rutas (`/backend/routes`).
- Análisis comparativo de los modelos de datos (`/backend/models`) para las rutas `atencion_materno_perinatal`, `atencion_vejez` y `control_cronicidad`.
- Búsqueda global de patrones de código para determinar la extensión de los problemas identificados.
- Comparación conceptual de la implementación con los requerimientos de la **Resolución 3280 (operativa) y la Resolución 202 (reportería)**.

---

## 3. Hallazgos Clave

### 3.1. Hallazgos Críticos de Arquitectura

- **Ausencia de Transacciones Atómicas (CRÍTICO):** Las operaciones de creación que involucran múltiples tablas se realizan mediante una secuencia de llamadas a la API de la base de datos sin un contenedor transaccional. El código intenta implementar "rollbacks" manuales, un patrón frágil y propenso a fallos que deja la base de datos en estados inconsistentes.
  - **Evidencia:** Patrón de `db.table(...).insert()` repetido en `atencion_adolescencia.py`, `atencion_adultez.py`, `atencion_infancia.py`, `atencion_materno_perinatal.py`, `atencion_vejez.py`, `control_cronicidad.py` y `tamizaje_oncologico.py`.

### 3.2. Hallazgos de Inconsistencia de Diseño

- **Triple Personalidad en Modelado de Datos (ALTO):** Existen al menos tres filosofías de diseño de modelos de datos contradictorias en el proyecto:
  1.  **Modelo Anidado/Polimórfico:** Usado en `atencion_materno_perinatal` (múltiples modelos pequeños y especializados).
  2.  **Modelo Plano/Monolítico:** Usado en `atencion_vejez` (una única clase gigante).
  3.  **Modelo de Unión Discriminada:** Usado en `control_cronicidad` (una `Union` de Pydantic de varios sub-modelos).
  - **Impacto:** Dificulta drásticamente el mantenimiento, la reutilización de código y la curva de aprendizaje.

- **Lógica de Negocio Fragmentada (ALTO):** La lógica de negocio está dispersa en al menos tres lugares distintos:
  - **En archivos de rutas:** ej. `control_cronicidad.py` contiene funciones de cálculo de riesgo.
  - **En archivos de modelos:** ej. `atencion_vejez_model.py` contiene funciones de evaluación geriátrica.
  - **En una capa de servicios incipiente:** ej. `reporteria_pedt.py`.
  - **Impacto:** Viola el principio de Separación de Inquietudes, haciendo el código difícil de probar, depurar y mantener.

### 3.3. Influencia de la Resolución 202 (Reportería)

- **Endpoints de Agregación (HALLAZGO CLAVE):** La presencia de endpoints de estadísticas y reportes (ej. `/estadisticas/basicas` en `control_cronicidad.py`) confirma la sospecha de que el proyecto está intentando implementar los requerimientos de la Resolución 202. La necesidad de generar estos reportes probablemente ha impulsado la creación de lógica de negocio en lugares inapropiados (como las rutas) para obtener resultados rápidamente.

### 3.4. Hallazgos Específicos por Módulo

- **Ruta `atenciones.py`:** Permite la creación de registros "genéricos" sin detalle, lo que puede generar datos huérfanos.
- **Ruta `atencion_vejez.py`:** La existencia de archivos `_fixed` y `_corrupted.bak` es un síntoma de problemas de estabilidad previos, probablemente causados por los defectos de diseño mencionados.

### 3.5. Buenas Prácticas Identificadas

- **Fidelidad a la Norma:** El modelado de datos es extremadamente detallado y fiel a los requerimientos de la Resolución 3280.
- **Uso de Tipos Estrictos:** El uso extensivo de `Enum` en Pydantic es una excelente práctica.
- **Monitoreo y Métricas:** La inclusión de código de monitoreo (`apm_collector`) es una práctica madura, aunque su ubicación actual puede mejorarse.
- **Documentación en Código:** Módulos como `atencion_vejez` presentan una excelente documentación en los encabezados.

---

## 4. Análisis de Riesgos

- **Corrupción de Datos (CRÍTICO):** El riesgo más significativo. Un fallo durante la creación de una atención puede llevar a una base de datos inconsistente y no fiable.
- **Incremento del Coste de Mantenimiento (ALTO):** La inconsistencia en la arquitectura obliga a los desarrolladores a aprender y mantener múltiples formas de hacer las cosas, ralentizando el desarrollo.
- **Baja Fiabilidad de los Reportes (ALTO):** Es difícil garantizar la precisión de los reportes para la Resolución 202 si los datos base están en riesgo de corrupción.

---

## 5. Plan de Remediación y Recomendaciones

- **1. (CRÍTICO) Implementar Transacciones Atómicas:**
  - **Recomendación:** Refactorizar toda la lógica de creación de atenciones para que se ejecute dentro de una única transacción atómica. La solución más robusta es crear **funciones de base de datos (RPC) en PostgreSQL** que encapsulen la lógica de `INSERT/UPDATE` en un bloque `BEGIN...COMMIT/ROLLBACK`.
  - **Acción Inmediata:** El equipo debe crear una función RPC (ej. `crear_atencion_completa`) y refactorizar un endpoint para usarla. Luego, replicar este patrón en todas las demás rutas.

- **2. (ALTO) Unificar el Patrón de Modelado y Centralizar la Lógica de Negocio:**
  - **Recomendación:** Realizar una reunión de arquitectura para decidir **un único patrón de diseño** (se recomienda el anidado/polimórfico por su escalabilidad) y crear una **capa de servicio** (`backend/services/`) que será el único lugar donde resida la lógica de negocio (cálculos, validaciones complejas, lógica de monitoreo).
  - **Acción Inmediata:** Crear el directorio `backend/services/` y migrar la lógica de cálculo de `control_cronicidad` (tanto de la ruta como del modelo) a un nuevo `services/cronicidad_service.py` como proyecto piloto.

- **3. (MEDIO) Estandarizar la Reportería:**
  - **Recomendación:** La lógica para generar estadísticas y reportes (Res. 202) debe residir en su propia capa de servicio (ej. `services/reporting_service.py`), no en los archivos de rutas. Estos servicios deben leer de la base de datos una vez que los datos hayan sido escritos de forma transaccional y segura.