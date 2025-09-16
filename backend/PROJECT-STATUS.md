# Contexto del Proyecto (Backend): API para IPS Santa Helena del Valle
**Última Actualización:** 16 de septiembre, 2025 - EXCELENCIA DOCUMENTAL ALCANZADA ✨

## 1. Propósito y Dominio
El proyecto es una API REST para una Institución Prestadora de Salud (IPS) en Colombia. Su objetivo es gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana, específicamente la **Resolución 3280 de 2018**, y generar los reportes de cumplimiento exigidos por la **Resolución 202 de 2021**.

## 2. Stack Tecnológico Principal
- **Backend:** Python
- **Framework:** FastAPI
- **Validación de Datos:** Pydantic
- **Base de Datos:** PostgreSQL (gestionada a través de Supabase)
- **Pruebas:** Pytest
- **Tareas Asíncronas:** Celery con Redis (para la capa de ingesta de datos)

## 3. Arquitectura Documental Excelente ⭐

**🎯 LOGRO MAYOR:** Se ha alcanzado una excelencia documental completa con estructura navegable, fragmentación inteligente y sistema de referencias cruzadas automático.

### **📚 Jerarquía Documental Optimizada**
Toda la documentación reside en `backend/docs/` con la siguiente estructura:

1.  **`00-quick-start/`**: **ONBOARDING RÁPIDO** - Guías especializadas por rol (15-30 min)
2.  **`01-foundations/architecture-overview.md`**: **PUNTO DE PARTIDA OBLIGATORIO** - Hub central navegable
3.  **`02-regulations/`**: Normativa fragmentada inteligentemente (Res. 3280 dividida en 5 documentos navegables)
4.  **`03-architecture/`**: Decisiones estratégicas de alto nivel optimizadas
5.  **`04-development/`**: Guías operativas fragmentadas por especialidad

### **🎯 Sistema de Referencias Documentales con Navegación Automática**
- **Cross-referencias inteligentes:** Cada documento enlaza automáticamente a recursos relacionados
- **Fragmentación coherente:** 28K líneas divididas manteniendo contexto y navegación
- **Nomenclatura descriptiva:** Eliminación completa de nombres genéricos (ej: GEMINI.md → PROJECT-STATUS.md)
- **Onboarding especializado:** Developer (20min), Compliance (15min), Architect (30min)

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

## 5. Análisis Compliance Crítico

**📊 Documento Clave:** [Análisis Compliance Resolución 3280](docs/02-regulations/compliance-analysis-3280.md)

### **Hallazgos Críticos:**
- **Compliance General:** 35% - DEFICIENTE ⚠️
- **Momentos Curso Vida:** 33% (2/6 implementados) - MEJORADO 🔄
- **Arquitectura Técnica:** 100% alineada - EXCELENTE ✅

**📋 Próximo Paso:** Adolescencia y Juventud (12-29 años) siguiendo patrón vertical consolidado

## 6. Módulos Clave y Estado de Avance

### ✅ **COMPLETADOS (100%)**
- **Primera Infancia (0-5 años):** EAD-3 y ASQ-3 funcionales, 14 tests pasando, arquitectura vertical consolidada
- **Infancia (6-11 años):** 5 campos calculados automáticos, 20 tests comprehensivos, reportes desarrollo escolar
- **Control Cronicidad:** 4 tipos (Diabetes, HTA, ERC, Dislipidemia), endpoints especializados  
- **Tamizaje Oncológico:** 4 tipos tamizaje, 21 tests, estadísticas y reportes adherencia

### 🔄 **EN DESARROLLO**
- **RIAMP (Materno Perinatal) (40%):** Estructura polimórfica anidada implementada, modelos granulares según Res. 3280, pendiente lógica negocio
- **Reportería Regulatoria Res. 202 (20%):** Capa reportería inteligente iniciada con `reporteria_pedt.py`

### ⏸️ **PENDIENTE**
- **RPMS Momentos Restantes (0%):** Adolescencia, Adultez, Vejez - 4/6 momentos curso vida faltantes
- **Gestión Proactiva (0%):** Demanda inducida, tablas `oportunidades_cuidado` no creadas

### 🏗️ **INFRAESTRUCTURA (85%)**
- **Núcleo Arquitectónico:** FastAPI, BD, migraciones, RLS - Base sólida y madura
- **Patrón Vertical:** Consolidado y replicable para nuevos módulos
- **Compliance Resolución 3280:** Campos obligatorios, escalas oficiales, esquemas vacunación
- **Base Datos Sincronizada:** Migraciones aplicadas, triggers corregidos, 2 pendientes deploy
- **Capa de Ingesta de Datos Externos (0%):** No iniciado. La arquitectura con Celery/Redis es un plan a futuro.

## 6. Procedimiento de Pruebas
- El framework de pruebas es **Pytest**.
- Los archivos de prueba se encuentran en `backend/tests/`.
- Las pruebas deben ser autocontenidas y no depender del estado de la base de datos.
- La guía de testing detallada se encuentra en `backend/docs/04-development/testing-guide.md`.

## 7. Implementaciones RIAS Completadas

### 7.1. Tamizaje Oncológico (Completado - 16 Sep 2025)
**Arquitectura:** Vertical con patrón polimórfico de 3 pasos siguiendo el modelo establecido en Control Cronicidad.

**Características Técnicas:**
- **Tipos Soportados:** 4 tipos de tamizaje (Cuello Uterino, Mama, Próstata, Colon y Recto)
- **Patrón de Creación:** Polimórfico de 3 pasos (crear tamizaje → crear atención → actualizar referencia)
- **Campos Calculados:** 4 funciones automáticas:
  - `nivel_riesgo`: Bajo/Moderado/Alto según resultados específicos por tipo
  - `adherencia_tamizaje`: Buena/Regular/Mala según temporalidad
  - `proxima_cita_recomendada_dias`: 30/90/365/730/1095 días según riesgo y tipo
  - `completitud_tamizaje`: 0-100% según campos completados

**Endpoints Implementados:**
- CRUD básico: `POST /tamizaje-oncologico/`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`
- Especializados: `/tipo/{tipo_tamizaje}`, `/paciente/{id}/cronologicos`
- Estadísticas: `/estadisticas/basicas` con distribución por tipo y resultados
- Reportes: `/reportes/adherencia` con filtros avanzados
- Legacy: `/tamizajes-oncologicos/` para compatibilidad

**Testing:** 21 tests comprehensivos organizados en 6 grupos:
1. CRUD básico (5 tests)
2. Endpoints especializados (4 tests) 
3. Estadísticas y reportes (3 tests)
4. Casos edge y validaciones (5 tests)
5. Funcionalidad integrada (2 tests)
6. Compatibilidad legacy (2 tests)

**Base de Datos:** Migración `20250916020000_fix_tamizaje_oncologico_nullable_atencion_id.sql` aplicada para permitir patrón polimórfico con `atencion_id` nullable.

**Archivos Clave:**
- `models/tamizaje_oncologico_model.py`: Modelos Crear/Actualizar/Response con campos calculados
- `routes/tamizaje_oncologico.py`: Rutas con patrón vertical y endpoints especializados
- `tests/test_tamizaje_oncologico_completo.py`: Suite completa de 21 tests

### 7.2. Control Cronicidad (Completado - Sep 2025)
Implementación vertical completa para manejo de 4 tipos de cronicidad con arquitectura polimórfica consolidada.

### 7.3. Primera Infancia (Completado - Sep 2025)
Implementación 100% funcional con EAD-3, ASQ-3, arquitectura vertical y 14 tests.

## 8. Idioma de Interacción
La comunicación con el asistente de IA y toda la terminología del proyecto debe ser en **español**.
