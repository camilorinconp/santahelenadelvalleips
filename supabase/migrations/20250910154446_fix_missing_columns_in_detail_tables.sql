-- Añadir columnas faltantes a las tablas de detalle para que coincidan con los modelos Pydantic.

-- Añadir 'entorno' a la tabla atencion_materno_perinatal
ALTER TABLE public.atencion_materno_perinatal
ADD COLUMN entorno TEXT;

-- Añadir 'entorno' a la tabla atencion_primera_infancia
ALTER TABLE public.atencion_primera_infancia
ADD COLUMN entorno TEXT;

-- Añadir 'paciente_id' a la tabla control_cronicidad
ALTER TABLE public.control_cronicidad
ADD COLUMN paciente_id UUID;

-- Añadir 'medico_id' a la tabla tamizaje_oncologico
ALTER TABLE public.tamizaje_oncologico
ADD COLUMN medico_id UUID;
