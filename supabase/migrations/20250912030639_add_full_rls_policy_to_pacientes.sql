-- Añadir política de RLS permisiva a la tabla pacientes para pruebas

-- Asegurarse de que RLS esté habilitado
ALTER TABLE public.pacientes ENABLE ROW LEVEL SECURITY;

-- Eliminar políticas existentes para evitar conflictos
DROP POLICY IF EXISTS "Allow anonymous insert for patients" ON public.pacientes;

-- Crear una política que permita todas las operaciones para el rol anon
CREATE POLICY "Allow all for anon role on pacientes" ON public.pacientes
FOR ALL
TO anon
USING (true)
WITH CHECK (true);
