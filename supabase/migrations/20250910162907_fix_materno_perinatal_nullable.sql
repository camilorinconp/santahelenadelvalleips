-- Hacer que la columna fecha_parto sea opcional para permitir registros prenatales.
ALTER TABLE public.atencion_materno_perinatal ALTER COLUMN fecha_parto DROP NOT NULL;
