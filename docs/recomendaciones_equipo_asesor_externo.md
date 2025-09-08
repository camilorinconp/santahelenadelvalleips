# Recomendaciones del Equipo Asesor Externo

Este documento centraliza las lecciones aprendidas y buenas prácticas identificadas durante el desarrollo del proyecto, para que sirvan como guía en este y futuros proyectos.

## 1. Sincronización entre Base de Datos y Aplicación

**Lección Aprendida:** Durante la fase de pruebas de las atenciones, nos encontramos con una serie de errores que no estaban en el código de la aplicación, sino en la configuración de la base de datos en Supabase.

**Recomendación:** Es crucial que la configuración del esquema de la base de datos sea un reflejo exacto de la lógica de la aplicación y sus modelos de datos (Pydantic). Antes de escribir pruebas o implementar nuevas funcionalidades, se debe verificar siempre que:

1.  **Políticas de Seguridad a Nivel de Fila (RLS):** Cada tabla que vaya a ser accedida por la API debe tener una política de RLS que permita las operaciones necesarias (SELECT, INSERT, UPDATE, DELETE). Supabase activa RLS por defecto y bloquea todo si no hay una política explícita.
2.  **Restricciones de Nulidad (`NOT NULL`):** Si un campo en un modelo Pydantic es opcional (ej. `Optional[str] = None`), la columna correspondiente en la base de datos **debe ser nullable** (aceptar valores nulos). Un conflicto aquí causará errores `violates not-null constraint`.
3.  **Valores por Defecto (`DEFAULT`):** Las columnas de clave foránea que son opcionales no deben tener valores por defecto que generen datos aleatorios (como `gen_random_uuid()`), ya que esto viola las restricciones de integridad referencial. El valor por defecto para estas columnas debe ser `NULL`.
4.  **Restricciones de Unicidad (`UNIQUE`):** Aplicar esta restricción únicamente cuando la lógica de negocio lo exija de forma estricta. Una columna como `especialidad` en la tabla `medicos` no debe ser única, ya que es natural tener múltiples médicos con la misma especialidad.

Mantener esta sincronía previene errores difíciles de depurar y asegura que la aplicación se comporte como se espera.
