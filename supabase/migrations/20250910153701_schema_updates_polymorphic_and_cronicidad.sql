-- 1. Añadir columnas para la relación polimórfica en la tabla 'atenciones'.
-- Se añaden como opcionales (NULL) para evitar errores si la tabla ya tiene datos.
-- En un futuro, se pueden poblar los datos existentes y luego alterar las columnas a NOT NULL.
ALTER TABLE public.atenciones
ADD COLUMN tipo_atencion TEXT,
ADD COLUMN detalle_id UUID;

-- 2. Añadir la columna opcional 'medico_id' a la tabla 'control_cronicidad'.
-- Esto alinea la base de datos con el modelo Pydantic 'ControlCronicidad'.
ALTER TABLE public.control_cronicidad
ADD COLUMN medico_id UUID;
