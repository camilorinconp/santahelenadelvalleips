# Análisis e Guía de Implementación: Anexos Técnicos de la Resolución 202 de 2021

**Para:** Equipo de Desarrollo Principal, IPS Santa Helena del Valle
**De:** Equipo Asesor Externo (Gemini)
**Fecha:** 12 de septiembre, 2025
**Asunto:** Guía técnica para desarrolladores sobre la implementación de los requisitos de reporte de la Resolución 202, basada en el análisis de sus anexos técnicos y su articulación con la Resolución 3280.

---

## 1. Introducción

Este documento es la guía técnica de referencia para el equipo de desarrollo. Su objetivo es desglosar y explicar los anexos de la Resolución 202 de 2021 y su impacto directo en el diseño de la base de datos, la lógica de negocio del backend y la implementación del frontend.

**Principio Rector:** La Resolución 3280 define **QUÉ** atenciones clínicas debemos realizar y qué datos capturar. La Resolución 202 y estos anexos definen **CÓMO** debemos estructurar y reportar esos datos a los entes de control. Por lo tanto, estos anexos son la especificación técnica para nuestro futuro **"Módulo de Reportería Regulatoria" (Fase 4)** y una guía indispensable para el diseño de datos que estamos realizando **hoy**.

---

## 2. El Diccionario de Datos Principal (`Anexos.csv`)

Este archivo es el más importante. Define la estructura final del archivo plano que la IPS debe generar y reportar. Es, en efecto, el **esquema de datos del reporte**. Contiene 119 variables que debemos ser capaces de generar a partir de nuestra base de datos.

La siguiente tabla resume las variables más relevantes y, lo que es más importante, su **impacto y correspondencia con nuestro modelo de datos**.

| ID | Nombre de la Variable | Valores Permitidos / Descripción | Impacto y Alineación con Nuestro Modelo de Datos |
|:---|:---|:---|:---|
| 14 | `Gestante` | 1=Sí, 2=No, 21=Riesgo no evaluado | **Campo Derivado.** No debe ser un campo directo en la tabla `pacientes`. Es una bandera que se calcula en el momento de generar el reporte, basado en si la paciente tiene una gestación activa en nuestra tabla `atencion_materno_perinatal`. |
| 33 | `Fecha probable de parto` | AAAA-MM-DD | **Mapeo Directo.** Corresponde al campo `fecha_probable_parto` en nuestra tabla `detalle_control_prenatal`. |
| 35 | `Clasificación del riesgo gestacional` | 4=Alto riesgo, 5=Bajo riesgo | **Mapeo de ENUM.** Corresponde a nuestro `EnumRiesgoBiopsicosocial`. Debemos asegurar que los valores de nuestro ENUM se mapeen a estos códigos numéricos. **Fuente: Res. 3280, Anexo 2, pág. 333 (Escala Herrera y Hurtado).** |
| 43-46 | `Resultado de escala abreviada de desarrollo...` | 3=Sospecha, 4=Riesgo, 5=Normal | **Mapeo de ENUM.** Corresponde a los resultados de la valoración EAD-3. Nuestro modelo debe tener 4 campos separados para cada área. **Fuente: Res. 3280, pág. 107.** |
| 52 | `Fecha de consulta de valoracin integral` | AAAA-MM-DD | **Campo Clave.** Corresponde a la `fecha_atencion` de una atención de tipo "Valoración Integral" en la RPMS para cualquier momento de vida. |
| 54 | `Suministro de mtodo anticonceptivo` | 1=DIU, 3=Implante, 5=Oral, etc. | **Mapeo de Catálogo.** Corresponde a nuestro futuro `catalogo_metodos_anticonceptivos`. El código numérico del reporte debe estar en nuestro catálogo. **Fuente: Res. 3280, pág. 182.** |
| 56 | `Fecha de primera consulta prenatal` | AAAA-MM-DD | **Mapeo Directo.** Corresponde a la `fecha_atencion` de la *primera* atención de tipo `detalle_control_prenatal` para una gestación. Requiere una lógica de consulta específica. |
| 86 | `Tamizaje del cncer de cuello uterino` | 1=Citología, 2=Prueba VPH, etc. | **Mapeo de Catálogo.** Define los tipos de tamizaje que nuestro sistema debe poder registrar. **Fuente: Res. 3280, pág. 168.** |
| 88 | `Resultado tamizaje cncer de cuello uterino` | 1=ASC-US, 3=LEI bajo grado, 19=Positivo VPH... | **Campo de Alta Complejidad.** Es un campo polimórfico en sí mismo. Nuestro modelo de datos para `tamizaje_oncologico` debe ser lo suficientemente flexible para almacenar estos diferentes tipos de resultados. |
| 97 | `Resultado de mamografa` | 1=BIRADS 0, 2=BIRADS 1, etc. | **Mapeo de ENUM/Catálogo.** Corresponde a la clasificación BIRADS, un estándar en mamografía. Nuestro sistema debe usar estos mismos códigos. **Fuente: Res. 3280, pág. 173.** |
| 102 | `COP por persona` | Formato de 12 dígitos | **Campo Compuesto.** Es un índice odontológico. El frontend debe tener un componente específico para calcularlo, y el backend debe almacenarlo como un string de 12 dígitos. |

---

## 2.1. Análisis Profundo de la Simbiosis (Res. 3280 -> Res. 202)

La lectura detallada de la Res. 3280 nos permite ver la conexión directa entre el protocolo clínico y la variable de reporte. A continuación, se presentan tres ejemplos clave que ilustran esta simbiosis:

#### Ejemplo A: Riesgo Gestacional
*   **El Reporte (Res. 202):** El `Anexos.csv`, **variable 35**, exige reportar la "Clasificación del riesgo gestacional" con los códigos `4` (Alto) y `5` (Bajo).
*   **El Protocolo Clínico (Res. 3280):** La **página 266**, sección 4.3.6 (Cuidado Prenatal), instruye al profesional a "Clasificar el riesgo biopsicosocial". Para ello, la resolución remite explícitamente al **Anexo 2 (página 333)**, que contiene la **"Escala de Riesgo Biopsicosocial de Herrera y Hurtado"**, la herramienta exacta para obtener dicho resultado.
*   **Impacto en el Desarrollo:** Nuestro sistema no solo debe tener un campo para 'riesgo', sino que idealmente debería implementar en el frontend un formulario interactivo basado en la Escala de Herrera y Hurtado. Esto estandariza la captura y garantiza que el código reportado (`4` o `5`) sea el correcto.

#### Ejemplo B: Tamizaje de Cáncer de Cuello Uterino
*   **El Reporte (Res. 202):** La **variable 88** define una lista detallada de 21 posibles resultados, incluyendo "ASC-US" (código 1), "LEI de bajo grado" (código 3) y "Positivo" para una prueba de VPH (código 19).
*   **El Protocolo Clínico (Res. 3280):** La **página 168**, sección 9.5, describe los "Procedimientos de tamización de cáncer de cuello uterino" y la conducta a seguir según los hallazgos, los cuales se corresponden directamente con los códigos de la Res. 202.
*   **Impacto en el Desarrollo:** El modelo de datos para el tamizaje oncológico debe ser un campo de texto controlado (ENUM o FK a catálogo) que contenga exactamente los 21 valores posibles. Esto es una restricción crítica para la integridad de los datos y la validez del reporte.

#### Ejemplo C: Desarrollo Infantil
*   **El Reporte (Res. 202):** Las **variables 43 a 46** exigen un resultado individual para cada una de las cuatro áreas de la "escala abreviada de desarrollo": motricidad gruesa, motricidad fino-adaptativa, personal-social y audición-lenguaje.
*   **El Protocolo Clínico (Res. 3280):** La **página 107**, en la sección de "Atención para la primera infancia", instruye valorar el desarrollo usando la **EAD-3 (Escala Abreviada de Desarrollo 3)**, la cual se compone precisamente de esas cuatro áreas.
*   **Impacto en el Desarrollo:** El formulario para la "Valoración Integral de Primera Infancia" en nuestro frontend debe tener secciones claras para cada una de las 4 áreas de la EAD-3. La base de datos, en la tabla de detalle correspondiente, debe tener cuatro columnas distintas para almacenar cada resultado, permitiendo así generar el reporte de forma directa.

---

## 3. Las Reglas del Juego (`Controles RPED.csv`)

Este archivo contiene las **reglas de validación de negocio** que el Ministerio de Salud aplica a los reportes. Nuestro objetivo es construir un sistema que genere reportes que **pasen el 100% de estas validaciones**.

**Estrategia de Implementación:** Estas reglas deben traducirse en validaciones en **tres lugares**: la Base de Datos (constraints), el Backend (lógica de negocio en Pydantic/FastAPI) y el Frontend (validación de formularios).

---

## 4. Catálogos y Guías de Referencia (`Tabla ocupaciones.csv`, `GS-SW-0002_GUIA.csv`)

Estos archivos proveen los datos maestros y las guías rápidas para la implementación.

*   **`Tabla ocupaciones.csv`:** Los datos de este CSV deben ser la fuente para poblar nuestra tabla `catalogo_ocupaciones`. El frontend debe usar un campo de autocompletado que consulte un endpoint (`GET /api/catalogos/ocupaciones`) para obtener estos valores.

*   **`GS-SW-0002_GUIA.csv`:** Este archivo es la **biblia para el equipo de frontend**. Permite implementar lógica de visualización condicional de manera precisa (ej. ocultar la sección de gestación si el paciente es masculino o está fuera del rango de edad).

---

## 5. Guía de Implementación para Desarrolladores

Basado en este análisis, el flujo de trabajo para el equipo debe ser:

1.  **Al Modelar la Base de Datos:**
    *   Para cada tabla de `detalle_...`, consultar `Anexos.csv` para asegurar que todos los campos reportables están presentes.
    *   Usar los **códigos numéricos** del reporte como valores preferidos en la BD (vía ENUMs o FKs), ya que simplifica la generación del reporte.

2.  **Al Desarrollar el Backend:**
    *   Implementar las validaciones de `Controles RPED.csv` como validadores de Pydantic y lógica de negocio.
    *   Diseñar el futuro **"Módulo de Reportería Regulatoria" (Fase 4)** como una función que genere un archivo de texto que siga al pie de la letra la estructura de `Anexos.csv`.

3.  **Al Desarrollar el Frontend:**
    *   Usar `GS-SW-0002_GUIA.csv` como guía para implementar **renderizado condicional** en los formularios.
    *   Poblar todos los `select` y autocompletados desde los endpoints de catálogos.

Este enfoque garantiza que el sistema no solo sea funcional para el usuario clínico, sino que también esté, desde su concepción, preparado para cumplir con los complejos requisitos de reporte del sistema de salud colombiano.
