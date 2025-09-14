# Contexto del Proyecto (Backend): API para IPS Santa Helena del Valle
**Última Actualización:** 14 de septiembre, 2025

## 1. Propósito y Dominio
El proyecto es una API REST para una Institución Prestadora de Salud (IPS) en Colombia. Su objetivo es gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana, específicamente la **Resolución 3280 de 2018**, y generar los reportes de cumplimiento exigidos por la **Resolución 202 de 2021**.

## 2. Stack Tecnológico Principal
- **Backend:** Python
- **Framework:** FastAPI
- **Validación de Datos:** Pydantic
- **Base de Datos:** PostgreSQL (gestionada a través de Supabase)
- **Pruebas:** Pytest
- **Tareas Asíncronas:** Celery con Redis (para la capa de ingesta de datos)

## 3. Fuentes de la Verdad (Jerarquía de Documentación)
Para entender el proyecto, los documentos deben ser consultados en el siguiente orden. Toda la documentación reside en `backend/docs/`.

1.  **`01-foundations/architecture-overview.md`**: **PUNTO DE PARTIDA OBLIGATORIO.** Es el hub central que resume la arquitectura y enlaza a los demás documentos detallados.
2.  **`02-regulations/`**: Contiene la normativa (Res. 3280, anexos de la 202) que es la base de todos los requisitos funcionales.
3.  **`03-architecture/`**: Contiene las decisiones estratégicas de alto nivel sobre el diseño del software.
4.  **`04-development/`**: Guías prácticas para el trabajo del día a día (testing, lecciones aprendidas).

## 4. Arquitectura General

#### 4.1. Lógica de Aplicación (3 Capas)
El backend sigue una arquitectura de 3 capas para una clara separación de responsabilidades:
1.  **Capa de Rutas (`/routes`):** Maneja las peticiones y respuestas HTTP. Es la puerta de entrada a la API.
2.  **Capa de Servicios (`/services`):** Contiene la lógica de negocio compleja. Orquesta las operaciones, realiza cálculos y se comunica con la capa de datos. (Ej: `reporteria_pedt.py`).
3.  **Capa de Modelos (`/models`):** Define la estructura de los datos (Pydantic) y la interacción con la base de datos.

#### 4.2. Base de Datos: Híbrida y Polimórfica Anidada
- **Híbrida:** Combina la robustez de **PostgreSQL** con la agilidad de la plataforma **Supabase** y la disciplina de la **CLI de Supabase** para gestionar el esquema como código.
- **Polimórfica Anidada:** Es la estrategia de modelado de datos para manejar la complejidad de las RIAS. La tabla `atenciones` es la principal, y se vincula a tablas de detalle cada vez más específicas (ej. `atencion_materno_perinatal` -> `detalle_control_prenatal`).

#### 4.3. Estrategia de Tipado (Las 3 Capas de Granularidad)
- **Capa 1 (Estructurada):** `ENUMs` de PostgreSQL y `Tablas de Catálogo` para datos estandarizados.
- **Capa 2 (Semi-Estructurada):** `JSONB` para datos flexibles como checklists o grupos de síntomas.
- **Capa 3 (No Estructurada):** `TEXT` para narrativas médicas, siendo la materia prima para futuras implementaciones de IA (RAG/LLM).

## 5. Módulos Clave y Estado de Avance

- **Núcleo y Arquitectura (80%):** La base del proyecto (FastAPI, conexión a BD, estructura de carpetas, sistema de migraciones, RLS) es sólida y madura.
- **RIAMP (Ruta Materno Perinatal) (35%):** La estructura polimórfica está implementada. Los modelos de datos son aún esqueléticos y requieren la adición de la mayoría de los campos granulares de la Res. 3280.
- **RPMS (Rutas de Promoción y Mantenimiento) (15%):** Existen modelos y rutas esqueléticas, pero la implementación de la lógica de negocio detallada por momento de vida no ha comenzado.
- **Reportería Regulatoria (Res. 202) (20%):** **Iniciado.** La existencia del servicio `reporteria_pedt.py` y sus tests (`test_reporteria_pedt.py`) confirma que el desarrollo de la "Capa de Reportería Inteligente" ha comenzado, siguiendo la estrategia híbrida acordada.
- **Gestión Proactiva (Demanda Inducida) (0%):** No iniciado. Las tablas `oportunidades_cuidado` y `gestiones_contacto` aún no han sido creadas.
- **Capa de Ingesta de Datos Externos (0%):** No iniciado. La arquitectura con Celery/Redis es un plan a futuro.

## 6. Procedimiento de Pruebas
- El framework de pruebas es **Pytest**.
- Los archivos de prueba se encuentran en `backend/tests/`.
- Las pruebas deben ser autocontenidas y no depender del estado de la base de datos.
- La guía de testing detallada se encuentra en `backend/docs/04-development/testing-guide.md`.

## 7. Idioma de Interacción
La comunicación con el asistente de IA y toda la terminología del proyecto debe ser en **español**.
