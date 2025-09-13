-- Añadir política de RLS a la tabla pacientes para permitir inserciones

ALTER TABLE public.pacientes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anonymous insert for patients" ON public.pacientes
FOR INSERT WITH CHECK (true);
