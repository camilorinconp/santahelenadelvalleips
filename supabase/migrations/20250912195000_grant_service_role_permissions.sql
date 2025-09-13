-- Grant explicit permissions to service_role for all tables
-- This ensures that service_role can bypass RLS and perform all operations

-- Grant all privileges on all tables to service_role
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;

-- Grant all privileges on all sequences to service_role (for auto-increment IDs)
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO service_role;

-- Grant specific permissions for each table to ensure full access
GRANT ALL PRIVILEGES ON public.pacientes TO service_role;
GRANT ALL PRIVILEGES ON public.medicos TO service_role;
GRANT ALL PRIVILEGES ON public.atenciones TO service_role;
GRANT ALL PRIVILEGES ON public.atencion_materno_perinatal TO service_role;
GRANT ALL PRIVILEGES ON public.atencion_primera_infancia TO service_role;
GRANT ALL PRIVILEGES ON public.control_cronicidad TO service_role;
GRANT ALL PRIVILEGES ON public.control_diabetes_detalles TO service_role;
GRANT ALL PRIVILEGES ON public.control_dislipidemia_detalles TO service_role;
GRANT ALL PRIVILEGES ON public.control_erc_detalles TO service_role;
GRANT ALL PRIVILEGES ON public.control_hipertension_detalles TO service_role;
GRANT ALL PRIVILEGES ON public.tamizaje_oncologico TO service_role;
GRANT ALL PRIVILEGES ON public.intervenciones_colectivas TO service_role;
GRANT ALL PRIVILEGES ON public.codigos_rias TO service_role;

-- Grant permissions on maternal-perinatal detail tables
GRANT ALL PRIVILEGES ON public.detalle_control_prenatal TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_parto TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_recien_nacido TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_puerperio TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_salud_bucal_mp TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_nutricion_mp TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_ive TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_curso_maternidad_paternidad TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_seguimiento_rn TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_preconcepcional_anamnesis TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_preconcepcional_paraclinicos TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_preconcepcional_antropometria TO service_role;
GRANT ALL PRIVILEGES ON public.detalle_rn_atencion_inmediata TO service_role;

-- Ensure service_role bypasses RLS by setting bypass_rls attribute
-- This is the key configuration that should allow service_role to bypass RLS
ALTER ROLE service_role SET row_security = off;