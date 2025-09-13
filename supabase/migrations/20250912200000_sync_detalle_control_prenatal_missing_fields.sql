-- Sincronizar campos faltantes en detalle_control_prenatal 
-- para alinearlo con el modelo Pydantic DetalleControlPrenatal

-- Agregar campos que están en el modelo Pydantic pero faltan en la base de datos

-- Campos de hemoclasificación y urocultivo
ALTER TABLE public.detalle_control_prenatal 
ADD COLUMN IF NOT EXISTS hemoclasificacion text;

ALTER TABLE public.detalle_control_prenatal 
ADD COLUMN IF NOT EXISTS resultado_urocultivo text;

-- Comentarios para documentar los campos
COMMENT ON COLUMN public.detalle_control_prenatal.hemoclasificacion IS 'Clasificación sanguínea de la paciente (A+, A-, B+, B-, AB+, AB-, O+, O-)';
COMMENT ON COLUMN public.detalle_control_prenatal.resultado_urocultivo IS 'Resultado del urocultivo (POSITIVO, NEGATIVO, NO_APLICA)';

-- Nota: Estos campos se agregan como text para compatibilidad con ENUMs de Pydantic
-- En producción se podrían convertir a ENUMs nativos de PostgreSQL si se requiere