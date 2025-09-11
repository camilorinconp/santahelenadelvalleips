-- Migración Maestra: Sincroniza todas las tablas de detalle con sus modelos Pydantic.

-- Tabla: atencion_materno_perinatal
ALTER TABLE public.atencion_materno_perinatal
ADD COLUMN IF NOT EXISTS paciente_id UUID,
ADD COLUMN IF NOT EXISTS medico_id UUID,
ADD COLUMN IF NOT EXISTS fecha_atencion DATE,
ADD COLUMN IF NOT EXISTS entorno TEXT;

-- Tabla: atencion_primera_infancia
ALTER TABLE public.atencion_primera_infancia
ADD COLUMN IF NOT EXISTS paciente_id UUID,
ADD COLUMN IF NOT EXISTS medico_id UUID,
ADD COLUMN IF NOT EXISTS fecha_atencion DATE,
ADD COLUMN IF NOT EXISTS entorno TEXT;

-- Tabla: control_cronicidad
ALTER TABLE public.control_cronicidad
ADD COLUMN IF NOT EXISTS paciente_id UUID,
ADD COLUMN IF NOT EXISTS medico_id UUID,
ADD COLUMN IF NOT EXISTS atencion_id UUID;

-- Tabla: tamizaje_oncologico
ALTER TABLE public.tamizaje_oncologico
ADD COLUMN IF NOT EXISTS paciente_id UUID,
ADD COLUMN IF NOT EXISTS medico_id UUID,
ADD COLUMN IF NOT EXISTS atencion_id UUID;
