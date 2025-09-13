-- Re-enable all development policies for RLS
-- This migration ensures that all tables have permissive policies for development

-- Enable RLS and create permissive policies for all tables

-- POLICY: Enable all access for all roles on atencion_materno_perinatal
DROP POLICY IF EXISTS "atencion_materno_perinatal_dev_policy" ON public.atencion_materno_perinatal;
CREATE POLICY "atencion_materno_perinatal_dev_policy" ON public.atencion_materno_perinatal
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on atencion_primera_infancia
DROP POLICY IF EXISTS "atencion_primera_infancia_dev_policy" ON public.atencion_primera_infancia;
CREATE POLICY "atencion_primera_infancia_dev_policy" ON public.atencion_primera_infancia
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on atenciones
DROP POLICY IF EXISTS "atenciones_dev_policy" ON public.atenciones;
CREATE POLICY "atenciones_dev_policy" ON public.atenciones
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on codigos_rias
DROP POLICY IF EXISTS "codigos_rias_dev_policy" ON public.codigos_rias;
CREATE POLICY "codigos_rias_dev_policy" ON public.codigos_rias
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on control_cronicidad
DROP POLICY IF EXISTS "control_cronicidad_dev_policy" ON public.control_cronicidad;
CREATE POLICY "control_cronicidad_dev_policy" ON public.control_cronicidad
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on control_diabetes_detalles
DROP POLICY IF EXISTS "control_diabetes_detalles_dev_policy" ON public.control_diabetes_detalles;
CREATE POLICY "control_diabetes_detalles_dev_policy" ON public.control_diabetes_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on control_dislipidemia_detalles
DROP POLICY IF EXISTS "control_dislipidemia_detalles_dev_policy" ON public.control_dislipidemia_detalles;
CREATE POLICY "control_dislipidemia_detalles_dev_policy" ON public.control_dislipidemia_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on control_erc_detalles
DROP POLICY IF EXISTS "control_erc_detalles_dev_policy" ON public.control_erc_detalles;
CREATE POLICY "control_erc_detalles_dev_policy" ON public.control_erc_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on control_hipertension_detalles
DROP POLICY IF EXISTS "control_hipertension_detalles_dev_policy" ON public.control_hipertension_detalles;
CREATE POLICY "control_hipertension_detalles_dev_policy" ON public.control_hipertension_detalles
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on intervenciones_colectivas
DROP POLICY IF EXISTS "intervenciones_colectivas_dev_policy" ON public.intervenciones_colectivas;
CREATE POLICY "intervenciones_colectivas_dev_policy" ON public.intervenciones_colectivas
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on medicos
DROP POLICY IF EXISTS "medicos_dev_policy" ON public.medicos;
CREATE POLICY "medicos_dev_policy" ON public.medicos
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on pacientes (replacing existing)
DROP POLICY IF EXISTS "Allow all for anon role on pacientes" ON public.pacientes;
DROP POLICY IF EXISTS "pacientes_dev_policy" ON public.pacientes;
CREATE POLICY "pacientes_dev_policy" ON public.pacientes
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on tamizaje_oncologico
DROP POLICY IF EXISTS "tamizaje_oncologico_dev_policy" ON public.tamizaje_oncologico;
CREATE POLICY "tamizaje_oncologico_dev_policy" ON public.tamizaje_oncologico
FOR ALL USING (true) WITH CHECK (true);

-- Also add policies for all detail tables for maternal-perinatal care
-- POLICY: Enable all access for all roles on detalle_control_prenatal
DROP POLICY IF EXISTS "detalle_control_prenatal_dev_policy" ON public.detalle_control_prenatal;
CREATE POLICY "detalle_control_prenatal_dev_policy" ON public.detalle_control_prenatal
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on detalle_parto
DROP POLICY IF EXISTS "detalle_parto_dev_policy" ON public.detalle_parto;
CREATE POLICY "detalle_parto_dev_policy" ON public.detalle_parto
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on detalle_recien_nacido
DROP POLICY IF EXISTS "detalle_recien_nacido_dev_policy" ON public.detalle_recien_nacido;
CREATE POLICY "detalle_recien_nacido_dev_policy" ON public.detalle_recien_nacido
FOR ALL USING (true) WITH CHECK (true);

-- POLICY: Enable all access for all roles on detalle_puerperio
DROP POLICY IF EXISTS "detalle_puerperio_dev_policy" ON public.detalle_puerperio;
CREATE POLICY "detalle_puerperio_dev_policy" ON public.detalle_puerperio
FOR ALL USING (true) WITH CHECK (true);

-- Add any other detail tables that might exist
DROP POLICY IF EXISTS "detalle_salud_bucal_mp_dev_policy" ON public.detalle_salud_bucal_mp;
CREATE POLICY "detalle_salud_bucal_mp_dev_policy" ON public.detalle_salud_bucal_mp
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_nutricion_mp_dev_policy" ON public.detalle_nutricion_mp;
CREATE POLICY "detalle_nutricion_mp_dev_policy" ON public.detalle_nutricion_mp
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_ive_dev_policy" ON public.detalle_ive;
CREATE POLICY "detalle_ive_dev_policy" ON public.detalle_ive
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_curso_maternidad_paternidad_dev_policy" ON public.detalle_curso_maternidad_paternidad;
CREATE POLICY "detalle_curso_maternidad_paternidad_dev_policy" ON public.detalle_curso_maternidad_paternidad
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_seguimiento_rn_dev_policy" ON public.detalle_seguimiento_rn;
CREATE POLICY "detalle_seguimiento_rn_dev_policy" ON public.detalle_seguimiento_rn
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_preconcepcional_anamnesis_dev_policy" ON public.detalle_preconcepcional_anamnesis;
CREATE POLICY "detalle_preconcepcional_anamnesis_dev_policy" ON public.detalle_preconcepcional_anamnesis
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_preconcepcional_paraclinicos_dev_policy" ON public.detalle_preconcepcional_paraclinicos;
CREATE POLICY "detalle_preconcepcional_paraclinicos_dev_policy" ON public.detalle_preconcepcional_paraclinicos
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_preconcepcional_antropometria_dev_policy" ON public.detalle_preconcepcional_antropometria;
CREATE POLICY "detalle_preconcepcional_antropometria_dev_policy" ON public.detalle_preconcepcional_antropometria
FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "detalle_rn_atencion_inmediata_dev_policy" ON public.detalle_rn_atencion_inmediata;
CREATE POLICY "detalle_rn_atencion_inmediata_dev_policy" ON public.detalle_rn_atencion_inmediata
FOR ALL USING (true) WITH CHECK (true);