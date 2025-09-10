-- Establecer valores por defecto para las columnas de timestamp para asegurar que siempre se pueblen.

ALTER TABLE public.control_cronicidad ALTER COLUMN creado_en SET DEFAULT now();
ALTER TABLE public.tamizaje_oncologico ALTER COLUMN creado_en SET DEFAULT now();
ALTER TABLE public.atencion_materno_perinatal ALTER COLUMN creado_en SET DEFAULT now();
ALTER TABLE public.atencion_primera_infancia ALTER COLUMN creado_en SET DEFAULT now();
