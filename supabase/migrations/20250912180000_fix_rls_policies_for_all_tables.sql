-- 1. Drop old conflicting policies on 'pacientes' to ensure a clean state.
DROP POLICY IF EXISTS "Allow all for anon role on pacientes" ON public.pacientes;
DROP POLICY IF EXISTS "Allow anonymous insert for patients" ON public.pacientes;

-- 2. Create permissive development policies for all RLS-enabled tables.

-- POLICY: Enable all access for dev on atencion_materno_perinatal
CREATE POLICY "atencion_materno_perinatal_dev_policy" ON public.atencion_materno_perinatal
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on atencion_primera_infancia
CREATE POLICY "atencion_primera_infancia_dev_policy" ON public.atencion_primera_infancia
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on atenciones
CREATE POLICY "atenciones_dev_policy" ON public.atenciones
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on codigos_rias
CREATE POLICY "codigos_rias_dev_policy" ON public.codigos_rias
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on control_cronicidad
CREATE POLICY "control_cronicidad_dev_policy" ON public.control_cronicidad
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on control_diabetes_detalles
CREATE POLICY "control_diabetes_detalles_dev_policy" ON public.control_diabetes_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on control_dislipidemia_detalles
CREATE POLICY "control_dislipidemia_detalles_dev_policy" ON public.control_dislipidemia_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on control_erc_detalles
CREATE POLICY "control_erc_detalles_dev_policy" ON public.control_erc_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on control_hipertension_detalles
CREATE POLICY "control_hipertension_detalles_dev_policy" ON public.control_hipertension_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on intervenciones_colectivas
CREATE POLICY "intervenciones_colectivas_dev_policy" ON public.intervenciones_colectivas
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on medicos
CREATE POLICY "medicos_dev_policy" ON public.medicos
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on pacientes
CREATE POLICY "pacientes_dev_policy" ON public.pacientes
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for dev on tamizaje_oncologico
CREATE POLICY "tamizaje_oncologico_dev_policy" ON public.tamizaje_oncologico
FOR ALL USING (true) WITH CHECK (true);
