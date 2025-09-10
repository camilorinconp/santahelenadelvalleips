-- Añadir las últimas columnas faltantes identificadas durante las pruebas.

-- Añadir 'fecha_atencion' a la tabla atencion_materno_perinatal
ALTER TABLE public.atencion_materno_perinatal
ADD COLUMN fecha_atencion DATE;

-- Añadir 'fecha_atencion' a la tabla atencion_primera_infancia
ALTER TABLE public.atencion_primera_infancia
ADD COLUMN fecha_atencion DATE;

-- Añadir 'paciente_id' a la tabla tamizaje_oncologico
ALTER TABLE public.tamizaje_oncologico
ADD COLUMN paciente_id UUID;
