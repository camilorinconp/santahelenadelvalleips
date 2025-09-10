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
