drop trigger if exists "handle_updated_at" on "public"."atencion_materno_perinatal";

drop trigger if exists "handle_updated_at" on "public"."atencion_primera_infancia";

drop trigger if exists "handle_updated_at" on "public"."atenciones";

drop trigger if exists "handle_updated_at" on "public"."control_cronicidad";

drop trigger if exists "handle_updated_at" on "public"."control_hipertension_detalles";

drop trigger if exists "handle_updated_at" on "public"."intervenciones_colectivas";

drop trigger if exists "handle_updated_at" on "public"."medicos";

drop trigger if exists "handle_updated_at" on "public"."pacientes";

drop trigger if exists "handle_updated_at" on "public"."tamizaje_oncologico";

revoke delete on table "public"."atencion_materno_perinatal" from "anon";

revoke insert on table "public"."atencion_materno_perinatal" from "anon";

revoke references on table "public"."atencion_materno_perinatal" from "anon";

revoke select on table "public"."atencion_materno_perinatal" from "anon";

revoke trigger on table "public"."atencion_materno_perinatal" from "anon";

revoke truncate on table "public"."atencion_materno_perinatal" from "anon";

revoke update on table "public"."atencion_materno_perinatal" from "anon";

revoke delete on table "public"."atencion_materno_perinatal" from "authenticated";

revoke insert on table "public"."atencion_materno_perinatal" from "authenticated";

revoke references on table "public"."atencion_materno_perinatal" from "authenticated";

revoke select on table "public"."atencion_materno_perinatal" from "authenticated";

revoke trigger on table "public"."atencion_materno_perinatal" from "authenticated";

revoke truncate on table "public"."atencion_materno_perinatal" from "authenticated";

revoke update on table "public"."atencion_materno_perinatal" from "authenticated";

revoke delete on table "public"."atencion_materno_perinatal" from "service_role";

revoke insert on table "public"."atencion_materno_perinatal" from "service_role";

revoke references on table "public"."atencion_materno_perinatal" from "service_role";

revoke select on table "public"."atencion_materno_perinatal" from "service_role";

revoke trigger on table "public"."atencion_materno_perinatal" from "service_role";

revoke truncate on table "public"."atencion_materno_perinatal" from "service_role";

revoke update on table "public"."atencion_materno_perinatal" from "service_role";

revoke delete on table "public"."atencion_primera_infancia" from "anon";

revoke insert on table "public"."atencion_primera_infancia" from "anon";

revoke references on table "public"."atencion_primera_infancia" from "anon";

revoke select on table "public"."atencion_primera_infancia" from "anon";

revoke trigger on table "public"."atencion_primera_infancia" from "anon";

revoke truncate on table "public"."atencion_primera_infancia" from "anon";

revoke update on table "public"."atencion_primera_infancia" from "anon";

revoke delete on table "public"."atencion_primera_infancia" from "authenticated";

revoke insert on table "public"."atencion_primera_infancia" from "authenticated";

revoke references on table "public"."atencion_primera_infancia" from "authenticated";

revoke select on table "public"."atencion_primera_infancia" from "authenticated";

revoke trigger on table "public"."atencion_primera_infancia" from "authenticated";

revoke truncate on table "public"."atencion_primera_infancia" from "authenticated";

revoke update on table "public"."atencion_primera_infancia" from "authenticated";

revoke delete on table "public"."atencion_primera_infancia" from "service_role";

revoke insert on table "public"."atencion_primera_infancia" from "service_role";

revoke references on table "public"."atencion_primera_infancia" from "service_role";

revoke select on table "public"."atencion_primera_infancia" from "service_role";

revoke trigger on table "public"."atencion_primera_infancia" from "service_role";

revoke truncate on table "public"."atencion_primera_infancia" from "service_role";

revoke update on table "public"."atencion_primera_infancia" from "service_role";

revoke delete on table "public"."atenciones" from "anon";

revoke insert on table "public"."atenciones" from "anon";

revoke references on table "public"."atenciones" from "anon";

revoke select on table "public"."atenciones" from "anon";

revoke trigger on table "public"."atenciones" from "anon";

revoke truncate on table "public"."atenciones" from "anon";

revoke update on table "public"."atenciones" from "anon";

revoke delete on table "public"."atenciones" from "authenticated";

revoke insert on table "public"."atenciones" from "authenticated";

revoke references on table "public"."atenciones" from "authenticated";

revoke select on table "public"."atenciones" from "authenticated";

revoke trigger on table "public"."atenciones" from "authenticated";

revoke truncate on table "public"."atenciones" from "authenticated";

revoke update on table "public"."atenciones" from "authenticated";

revoke delete on table "public"."atenciones" from "service_role";

revoke insert on table "public"."atenciones" from "service_role";

revoke references on table "public"."atenciones" from "service_role";

revoke select on table "public"."atenciones" from "service_role";

revoke trigger on table "public"."atenciones" from "service_role";

revoke truncate on table "public"."atenciones" from "service_role";

revoke update on table "public"."atenciones" from "service_role";

revoke delete on table "public"."codigos_rias" from "anon";

revoke insert on table "public"."codigos_rias" from "anon";

revoke references on table "public"."codigos_rias" from "anon";

revoke select on table "public"."codigos_rias" from "anon";

revoke trigger on table "public"."codigos_rias" from "anon";

revoke truncate on table "public"."codigos_rias" from "anon";

revoke update on table "public"."codigos_rias" from "anon";

revoke delete on table "public"."codigos_rias" from "authenticated";

revoke insert on table "public"."codigos_rias" from "authenticated";

revoke references on table "public"."codigos_rias" from "authenticated";

revoke select on table "public"."codigos_rias" from "authenticated";

revoke trigger on table "public"."codigos_rias" from "authenticated";

revoke truncate on table "public"."codigos_rias" from "authenticated";

revoke update on table "public"."codigos_rias" from "authenticated";

revoke delete on table "public"."codigos_rias" from "service_role";

revoke insert on table "public"."codigos_rias" from "service_role";

revoke references on table "public"."codigos_rias" from "service_role";

revoke select on table "public"."codigos_rias" from "service_role";

revoke trigger on table "public"."codigos_rias" from "service_role";

revoke truncate on table "public"."codigos_rias" from "service_role";

revoke update on table "public"."codigos_rias" from "service_role";

revoke delete on table "public"."control_cronicidad" from "anon";

revoke insert on table "public"."control_cronicidad" from "anon";

revoke references on table "public"."control_cronicidad" from "anon";

revoke select on table "public"."control_cronicidad" from "anon";

revoke trigger on table "public"."control_cronicidad" from "anon";

revoke truncate on table "public"."control_cronicidad" from "anon";

revoke update on table "public"."control_cronicidad" from "anon";

revoke delete on table "public"."control_cronicidad" from "authenticated";

revoke insert on table "public"."control_cronicidad" from "authenticated";

revoke references on table "public"."control_cronicidad" from "authenticated";

revoke select on table "public"."control_cronicidad" from "authenticated";

revoke trigger on table "public"."control_cronicidad" from "authenticated";

revoke truncate on table "public"."control_cronicidad" from "authenticated";

revoke update on table "public"."control_cronicidad" from "authenticated";

revoke delete on table "public"."control_cronicidad" from "service_role";

revoke insert on table "public"."control_cronicidad" from "service_role";

revoke references on table "public"."control_cronicidad" from "service_role";

revoke select on table "public"."control_cronicidad" from "service_role";

revoke trigger on table "public"."control_cronicidad" from "service_role";

revoke truncate on table "public"."control_cronicidad" from "service_role";

revoke update on table "public"."control_cronicidad" from "service_role";

revoke delete on table "public"."control_diabetes_detalles" from "anon";

revoke insert on table "public"."control_diabetes_detalles" from "anon";

revoke references on table "public"."control_diabetes_detalles" from "anon";

revoke select on table "public"."control_diabetes_detalles" from "anon";

revoke trigger on table "public"."control_diabetes_detalles" from "anon";

revoke truncate on table "public"."control_diabetes_detalles" from "anon";

revoke update on table "public"."control_diabetes_detalles" from "anon";

revoke delete on table "public"."control_diabetes_detalles" from "authenticated";

revoke insert on table "public"."control_diabetes_detalles" from "authenticated";

revoke references on table "public"."control_diabetes_detalles" from "authenticated";

revoke select on table "public"."control_diabetes_detalles" from "authenticated";

revoke trigger on table "public"."control_diabetes_detalles" from "authenticated";

revoke truncate on table "public"."control_diabetes_detalles" from "authenticated";

revoke update on table "public"."control_diabetes_detalles" from "authenticated";

revoke delete on table "public"."control_diabetes_detalles" from "service_role";

revoke insert on table "public"."control_diabetes_detalles" from "service_role";

revoke references on table "public"."control_diabetes_detalles" from "service_role";

revoke select on table "public"."control_diabetes_detalles" from "service_role";

revoke trigger on table "public"."control_diabetes_detalles" from "service_role";

revoke truncate on table "public"."control_diabetes_detalles" from "service_role";

revoke update on table "public"."control_diabetes_detalles" from "service_role";

revoke delete on table "public"."control_dislipidemia_detalles" from "anon";

revoke insert on table "public"."control_dislipidemia_detalles" from "anon";

revoke references on table "public"."control_dislipidemia_detalles" from "anon";

revoke select on table "public"."control_dislipidemia_detalles" from "anon";

revoke trigger on table "public"."control_dislipidemia_detalles" from "anon";

revoke truncate on table "public"."control_dislipidemia_detalles" from "anon";

revoke update on table "public"."control_dislipidemia_detalles" from "anon";

revoke delete on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke insert on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke references on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke select on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke trigger on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke truncate on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke update on table "public"."control_dislipidemia_detalles" from "authenticated";

revoke delete on table "public"."control_dislipidemia_detalles" from "service_role";

revoke insert on table "public"."control_dislipidemia_detalles" from "service_role";

revoke references on table "public"."control_dislipidemia_detalles" from "service_role";

revoke select on table "public"."control_dislipidemia_detalles" from "service_role";

revoke trigger on table "public"."control_dislipidemia_detalles" from "service_role";

revoke truncate on table "public"."control_dislipidemia_detalles" from "service_role";

revoke update on table "public"."control_dislipidemia_detalles" from "service_role";

revoke delete on table "public"."control_erc_detalles" from "anon";

revoke insert on table "public"."control_erc_detalles" from "anon";

revoke references on table "public"."control_erc_detalles" from "anon";

revoke select on table "public"."control_erc_detalles" from "anon";

revoke trigger on table "public"."control_erc_detalles" from "anon";

revoke truncate on table "public"."control_erc_detalles" from "anon";

revoke update on table "public"."control_erc_detalles" from "anon";

revoke delete on table "public"."control_erc_detalles" from "authenticated";

revoke insert on table "public"."control_erc_detalles" from "authenticated";

revoke references on table "public"."control_erc_detalles" from "authenticated";

revoke select on table "public"."control_erc_detalles" from "authenticated";

revoke trigger on table "public"."control_erc_detalles" from "authenticated";

revoke truncate on table "public"."control_erc_detalles" from "authenticated";

revoke update on table "public"."control_erc_detalles" from "authenticated";

revoke delete on table "public"."control_erc_detalles" from "service_role";

revoke insert on table "public"."control_erc_detalles" from "service_role";

revoke references on table "public"."control_erc_detalles" from "service_role";

revoke select on table "public"."control_erc_detalles" from "service_role";

revoke trigger on table "public"."control_erc_detalles" from "service_role";

revoke truncate on table "public"."control_erc_detalles" from "service_role";

revoke update on table "public"."control_erc_detalles" from "service_role";

revoke delete on table "public"."control_hipertension_detalles" from "anon";

revoke insert on table "public"."control_hipertension_detalles" from "anon";

revoke references on table "public"."control_hipertension_detalles" from "anon";

revoke select on table "public"."control_hipertension_detalles" from "anon";

revoke trigger on table "public"."control_hipertension_detalles" from "anon";

revoke truncate on table "public"."control_hipertension_detalles" from "anon";

revoke update on table "public"."control_hipertension_detalles" from "anon";

revoke delete on table "public"."control_hipertension_detalles" from "authenticated";

revoke insert on table "public"."control_hipertension_detalles" from "authenticated";

revoke references on table "public"."control_hipertension_detalles" from "authenticated";

revoke select on table "public"."control_hipertension_detalles" from "authenticated";

revoke trigger on table "public"."control_hipertension_detalles" from "authenticated";

revoke truncate on table "public"."control_hipertension_detalles" from "authenticated";

revoke update on table "public"."control_hipertension_detalles" from "authenticated";

revoke delete on table "public"."control_hipertension_detalles" from "service_role";

revoke insert on table "public"."control_hipertension_detalles" from "service_role";

revoke references on table "public"."control_hipertension_detalles" from "service_role";

revoke select on table "public"."control_hipertension_detalles" from "service_role";

revoke trigger on table "public"."control_hipertension_detalles" from "service_role";

revoke truncate on table "public"."control_hipertension_detalles" from "service_role";

revoke update on table "public"."control_hipertension_detalles" from "service_role";

revoke delete on table "public"."intervenciones_colectivas" from "anon";

revoke insert on table "public"."intervenciones_colectivas" from "anon";

revoke references on table "public"."intervenciones_colectivas" from "anon";

revoke select on table "public"."intervenciones_colectivas" from "anon";

revoke trigger on table "public"."intervenciones_colectivas" from "anon";

revoke truncate on table "public"."intervenciones_colectivas" from "anon";

revoke update on table "public"."intervenciones_colectivas" from "anon";

revoke delete on table "public"."intervenciones_colectivas" from "authenticated";

revoke insert on table "public"."intervenciones_colectivas" from "authenticated";

revoke references on table "public"."intervenciones_colectivas" from "authenticated";

revoke select on table "public"."intervenciones_colectivas" from "authenticated";

revoke trigger on table "public"."intervenciones_colectivas" from "authenticated";

revoke truncate on table "public"."intervenciones_colectivas" from "authenticated";

revoke update on table "public"."intervenciones_colectivas" from "authenticated";

revoke delete on table "public"."intervenciones_colectivas" from "service_role";

revoke insert on table "public"."intervenciones_colectivas" from "service_role";

revoke references on table "public"."intervenciones_colectivas" from "service_role";

revoke select on table "public"."intervenciones_colectivas" from "service_role";

revoke trigger on table "public"."intervenciones_colectivas" from "service_role";

revoke truncate on table "public"."intervenciones_colectivas" from "service_role";

revoke update on table "public"."intervenciones_colectivas" from "service_role";

revoke delete on table "public"."medicos" from "anon";

revoke insert on table "public"."medicos" from "anon";

revoke references on table "public"."medicos" from "anon";

revoke select on table "public"."medicos" from "anon";

revoke trigger on table "public"."medicos" from "anon";

revoke truncate on table "public"."medicos" from "anon";

revoke update on table "public"."medicos" from "anon";

revoke delete on table "public"."medicos" from "authenticated";

revoke insert on table "public"."medicos" from "authenticated";

revoke references on table "public"."medicos" from "authenticated";

revoke select on table "public"."medicos" from "authenticated";

revoke trigger on table "public"."medicos" from "authenticated";

revoke truncate on table "public"."medicos" from "authenticated";

revoke update on table "public"."medicos" from "authenticated";

revoke delete on table "public"."medicos" from "service_role";

revoke insert on table "public"."medicos" from "service_role";

revoke references on table "public"."medicos" from "service_role";

revoke select on table "public"."medicos" from "service_role";

revoke trigger on table "public"."medicos" from "service_role";

revoke truncate on table "public"."medicos" from "service_role";

revoke update on table "public"."medicos" from "service_role";

revoke delete on table "public"."pacientes" from "anon";

revoke insert on table "public"."pacientes" from "anon";

revoke references on table "public"."pacientes" from "anon";

revoke select on table "public"."pacientes" from "anon";

revoke trigger on table "public"."pacientes" from "anon";

revoke truncate on table "public"."pacientes" from "anon";

revoke update on table "public"."pacientes" from "anon";

revoke delete on table "public"."pacientes" from "authenticated";

revoke insert on table "public"."pacientes" from "authenticated";

revoke references on table "public"."pacientes" from "authenticated";

revoke select on table "public"."pacientes" from "authenticated";

revoke trigger on table "public"."pacientes" from "authenticated";

revoke truncate on table "public"."pacientes" from "authenticated";

revoke update on table "public"."pacientes" from "authenticated";

revoke delete on table "public"."pacientes" from "service_role";

revoke insert on table "public"."pacientes" from "service_role";

revoke references on table "public"."pacientes" from "service_role";

revoke select on table "public"."pacientes" from "service_role";

revoke trigger on table "public"."pacientes" from "service_role";

revoke truncate on table "public"."pacientes" from "service_role";

revoke update on table "public"."pacientes" from "service_role";

revoke delete on table "public"."tamizaje_oncologico" from "anon";

revoke insert on table "public"."tamizaje_oncologico" from "anon";

revoke references on table "public"."tamizaje_oncologico" from "anon";

revoke select on table "public"."tamizaje_oncologico" from "anon";

revoke trigger on table "public"."tamizaje_oncologico" from "anon";

revoke truncate on table "public"."tamizaje_oncologico" from "anon";

revoke update on table "public"."tamizaje_oncologico" from "anon";

revoke delete on table "public"."tamizaje_oncologico" from "authenticated";

revoke insert on table "public"."tamizaje_oncologico" from "authenticated";

revoke references on table "public"."tamizaje_oncologico" from "authenticated";

revoke select on table "public"."tamizaje_oncologico" from "authenticated";

revoke trigger on table "public"."tamizaje_oncologico" from "authenticated";

revoke truncate on table "public"."tamizaje_oncologico" from "authenticated";

revoke update on table "public"."tamizaje_oncologico" from "authenticated";

revoke delete on table "public"."tamizaje_oncologico" from "service_role";

revoke insert on table "public"."tamizaje_oncologico" from "service_role";

revoke references on table "public"."tamizaje_oncologico" from "service_role";

revoke select on table "public"."tamizaje_oncologico" from "service_role";

revoke trigger on table "public"."tamizaje_oncologico" from "service_role";

revoke truncate on table "public"."tamizaje_oncologico" from "service_role";

revoke update on table "public"."tamizaje_oncologico" from "service_role";

alter table "public"."atenciones" drop column "detalle_id";

alter table "public"."control_cronicidad" drop column "medico_id";

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_materno_perinatal FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_primera_infancia FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atenciones FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_cronicidad FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_hipertension_detalles FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.intervenciones_colectivas FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.medicos FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.tamizaje_oncologico FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');


