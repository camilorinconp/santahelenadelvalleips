drop trigger if exists "handle_updated_at" on "public"."atencion_materno_perinatal";

drop trigger if exists "handle_updated_at" on "public"."atencion_primera_infancia";

drop trigger if exists "handle_updated_at" on "public"."atenciones";

drop trigger if exists "handle_updated_at" on "public"."control_cronicidad";

drop trigger if exists "handle_updated_at" on "public"."control_hipertension_detalles";

drop trigger if exists "handle_updated_at" on "public"."intervenciones_colectivas";

drop trigger if exists "handle_updated_at" on "public"."medicos";

drop trigger if exists "handle_updated_at" on "public"."pacientes";

drop trigger if exists "handle_updated_at" on "public"."tamizaje_oncologico";

revoke delete on table "public"."detalle_control_prenatal" from "anon";

revoke insert on table "public"."detalle_control_prenatal" from "anon";

revoke references on table "public"."detalle_control_prenatal" from "anon";

revoke select on table "public"."detalle_control_prenatal" from "anon";

revoke trigger on table "public"."detalle_control_prenatal" from "anon";

revoke truncate on table "public"."detalle_control_prenatal" from "anon";

revoke update on table "public"."detalle_control_prenatal" from "anon";

revoke delete on table "public"."detalle_control_prenatal" from "authenticated";

revoke insert on table "public"."detalle_control_prenatal" from "authenticated";

revoke references on table "public"."detalle_control_prenatal" from "authenticated";

revoke select on table "public"."detalle_control_prenatal" from "authenticated";

revoke trigger on table "public"."detalle_control_prenatal" from "authenticated";

revoke truncate on table "public"."detalle_control_prenatal" from "authenticated";

revoke update on table "public"."detalle_control_prenatal" from "authenticated";

revoke delete on table "public"."detalle_control_prenatal" from "service_role";

revoke insert on table "public"."detalle_control_prenatal" from "service_role";

revoke references on table "public"."detalle_control_prenatal" from "service_role";

revoke select on table "public"."detalle_control_prenatal" from "service_role";

revoke trigger on table "public"."detalle_control_prenatal" from "service_role";

revoke truncate on table "public"."detalle_control_prenatal" from "service_role";

revoke update on table "public"."detalle_control_prenatal" from "service_role";

revoke delete on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke insert on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke references on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke select on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke trigger on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke truncate on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke update on table "public"."detalle_curso_maternidad_paternidad" from "anon";

revoke delete on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke insert on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke references on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke select on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke trigger on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke truncate on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke update on table "public"."detalle_curso_maternidad_paternidad" from "authenticated";

revoke delete on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke insert on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke references on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke select on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke trigger on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke truncate on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke update on table "public"."detalle_curso_maternidad_paternidad" from "service_role";

revoke delete on table "public"."detalle_ive" from "anon";

revoke insert on table "public"."detalle_ive" from "anon";

revoke references on table "public"."detalle_ive" from "anon";

revoke select on table "public"."detalle_ive" from "anon";

revoke trigger on table "public"."detalle_ive" from "anon";

revoke truncate on table "public"."detalle_ive" from "anon";

revoke update on table "public"."detalle_ive" from "anon";

revoke delete on table "public"."detalle_ive" from "authenticated";

revoke insert on table "public"."detalle_ive" from "authenticated";

revoke references on table "public"."detalle_ive" from "authenticated";

revoke select on table "public"."detalle_ive" from "authenticated";

revoke trigger on table "public"."detalle_ive" from "authenticated";

revoke truncate on table "public"."detalle_ive" from "authenticated";

revoke update on table "public"."detalle_ive" from "authenticated";

revoke delete on table "public"."detalle_ive" from "service_role";

revoke insert on table "public"."detalle_ive" from "service_role";

revoke references on table "public"."detalle_ive" from "service_role";

revoke select on table "public"."detalle_ive" from "service_role";

revoke trigger on table "public"."detalle_ive" from "service_role";

revoke truncate on table "public"."detalle_ive" from "service_role";

revoke update on table "public"."detalle_ive" from "service_role";

revoke delete on table "public"."detalle_nutricion_mp" from "anon";

revoke insert on table "public"."detalle_nutricion_mp" from "anon";

revoke references on table "public"."detalle_nutricion_mp" from "anon";

revoke select on table "public"."detalle_nutricion_mp" from "anon";

revoke trigger on table "public"."detalle_nutricion_mp" from "anon";

revoke truncate on table "public"."detalle_nutricion_mp" from "anon";

revoke update on table "public"."detalle_nutricion_mp" from "anon";

revoke delete on table "public"."detalle_nutricion_mp" from "authenticated";

revoke insert on table "public"."detalle_nutricion_mp" from "authenticated";

revoke references on table "public"."detalle_nutricion_mp" from "authenticated";

revoke select on table "public"."detalle_nutricion_mp" from "authenticated";

revoke trigger on table "public"."detalle_nutricion_mp" from "authenticated";

revoke truncate on table "public"."detalle_nutricion_mp" from "authenticated";

revoke update on table "public"."detalle_nutricion_mp" from "authenticated";

revoke delete on table "public"."detalle_nutricion_mp" from "service_role";

revoke insert on table "public"."detalle_nutricion_mp" from "service_role";

revoke references on table "public"."detalle_nutricion_mp" from "service_role";

revoke select on table "public"."detalle_nutricion_mp" from "service_role";

revoke trigger on table "public"."detalle_nutricion_mp" from "service_role";

revoke truncate on table "public"."detalle_nutricion_mp" from "service_role";

revoke update on table "public"."detalle_nutricion_mp" from "service_role";

revoke delete on table "public"."detalle_parto" from "anon";

revoke insert on table "public"."detalle_parto" from "anon";

revoke references on table "public"."detalle_parto" from "anon";

revoke select on table "public"."detalle_parto" from "anon";

revoke trigger on table "public"."detalle_parto" from "anon";

revoke truncate on table "public"."detalle_parto" from "anon";

revoke update on table "public"."detalle_parto" from "anon";

revoke delete on table "public"."detalle_parto" from "authenticated";

revoke insert on table "public"."detalle_parto" from "authenticated";

revoke references on table "public"."detalle_parto" from "authenticated";

revoke select on table "public"."detalle_parto" from "authenticated";

revoke trigger on table "public"."detalle_parto" from "authenticated";

revoke truncate on table "public"."detalle_parto" from "authenticated";

revoke update on table "public"."detalle_parto" from "authenticated";

revoke delete on table "public"."detalle_parto" from "service_role";

revoke insert on table "public"."detalle_parto" from "service_role";

revoke references on table "public"."detalle_parto" from "service_role";

revoke select on table "public"."detalle_parto" from "service_role";

revoke trigger on table "public"."detalle_parto" from "service_role";

revoke truncate on table "public"."detalle_parto" from "service_role";

revoke update on table "public"."detalle_parto" from "service_role";

revoke delete on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke insert on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke references on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke select on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke trigger on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke truncate on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke update on table "public"."detalle_preconcepcional_anamnesis" from "anon";

revoke delete on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke insert on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke references on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke select on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke trigger on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke truncate on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke update on table "public"."detalle_preconcepcional_anamnesis" from "authenticated";

revoke delete on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke insert on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke references on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke select on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke trigger on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke truncate on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke update on table "public"."detalle_preconcepcional_anamnesis" from "service_role";

revoke delete on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke insert on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke references on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke select on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke trigger on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke truncate on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke update on table "public"."detalle_preconcepcional_antropometria" from "anon";

revoke delete on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke insert on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke references on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke select on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke trigger on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke truncate on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke update on table "public"."detalle_preconcepcional_antropometria" from "authenticated";

revoke delete on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke insert on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke references on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke select on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke trigger on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke truncate on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke update on table "public"."detalle_preconcepcional_antropometria" from "service_role";

revoke delete on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke insert on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke references on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke select on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke trigger on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke truncate on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke update on table "public"."detalle_preconcepcional_paraclinicos" from "anon";

revoke delete on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke insert on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke references on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke select on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke trigger on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke truncate on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke update on table "public"."detalle_preconcepcional_paraclinicos" from "authenticated";

revoke delete on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke insert on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke references on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke select on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke trigger on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke truncate on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke update on table "public"."detalle_preconcepcional_paraclinicos" from "service_role";

revoke delete on table "public"."detalle_puerperio" from "anon";

revoke insert on table "public"."detalle_puerperio" from "anon";

revoke references on table "public"."detalle_puerperio" from "anon";

revoke select on table "public"."detalle_puerperio" from "anon";

revoke trigger on table "public"."detalle_puerperio" from "anon";

revoke truncate on table "public"."detalle_puerperio" from "anon";

revoke update on table "public"."detalle_puerperio" from "anon";

revoke delete on table "public"."detalle_puerperio" from "authenticated";

revoke insert on table "public"."detalle_puerperio" from "authenticated";

revoke references on table "public"."detalle_puerperio" from "authenticated";

revoke select on table "public"."detalle_puerperio" from "authenticated";

revoke trigger on table "public"."detalle_puerperio" from "authenticated";

revoke truncate on table "public"."detalle_puerperio" from "authenticated";

revoke update on table "public"."detalle_puerperio" from "authenticated";

revoke delete on table "public"."detalle_puerperio" from "service_role";

revoke insert on table "public"."detalle_puerperio" from "service_role";

revoke references on table "public"."detalle_puerperio" from "service_role";

revoke select on table "public"."detalle_puerperio" from "service_role";

revoke trigger on table "public"."detalle_puerperio" from "service_role";

revoke truncate on table "public"."detalle_puerperio" from "service_role";

revoke update on table "public"."detalle_puerperio" from "service_role";

revoke delete on table "public"."detalle_recien_nacido" from "anon";

revoke insert on table "public"."detalle_recien_nacido" from "anon";

revoke references on table "public"."detalle_recien_nacido" from "anon";

revoke select on table "public"."detalle_recien_nacido" from "anon";

revoke trigger on table "public"."detalle_recien_nacido" from "anon";

revoke truncate on table "public"."detalle_recien_nacido" from "anon";

revoke update on table "public"."detalle_recien_nacido" from "anon";

revoke delete on table "public"."detalle_recien_nacido" from "authenticated";

revoke insert on table "public"."detalle_recien_nacido" from "authenticated";

revoke references on table "public"."detalle_recien_nacido" from "authenticated";

revoke select on table "public"."detalle_recien_nacido" from "authenticated";

revoke trigger on table "public"."detalle_recien_nacido" from "authenticated";

revoke truncate on table "public"."detalle_recien_nacido" from "authenticated";

revoke update on table "public"."detalle_recien_nacido" from "authenticated";

revoke delete on table "public"."detalle_recien_nacido" from "service_role";

revoke insert on table "public"."detalle_recien_nacido" from "service_role";

revoke references on table "public"."detalle_recien_nacido" from "service_role";

revoke select on table "public"."detalle_recien_nacido" from "service_role";

revoke trigger on table "public"."detalle_recien_nacido" from "service_role";

revoke truncate on table "public"."detalle_recien_nacido" from "service_role";

revoke update on table "public"."detalle_recien_nacido" from "service_role";

revoke delete on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke insert on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke references on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke select on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke trigger on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke truncate on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke update on table "public"."detalle_rn_atencion_inmediata" from "anon";

revoke delete on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke insert on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke references on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke select on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke trigger on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke truncate on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke update on table "public"."detalle_rn_atencion_inmediata" from "authenticated";

revoke delete on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke insert on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke references on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke select on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke trigger on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke truncate on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke update on table "public"."detalle_rn_atencion_inmediata" from "service_role";

revoke delete on table "public"."detalle_salud_bucal_mp" from "anon";

revoke insert on table "public"."detalle_salud_bucal_mp" from "anon";

revoke references on table "public"."detalle_salud_bucal_mp" from "anon";

revoke select on table "public"."detalle_salud_bucal_mp" from "anon";

revoke trigger on table "public"."detalle_salud_bucal_mp" from "anon";

revoke truncate on table "public"."detalle_salud_bucal_mp" from "anon";

revoke update on table "public"."detalle_salud_bucal_mp" from "anon";

revoke delete on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke insert on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke references on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke select on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke trigger on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke truncate on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke update on table "public"."detalle_salud_bucal_mp" from "authenticated";

revoke delete on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke insert on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke references on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke select on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke trigger on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke truncate on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke update on table "public"."detalle_salud_bucal_mp" from "service_role";

revoke delete on table "public"."detalle_seguimiento_rn" from "anon";

revoke insert on table "public"."detalle_seguimiento_rn" from "anon";

revoke references on table "public"."detalle_seguimiento_rn" from "anon";

revoke select on table "public"."detalle_seguimiento_rn" from "anon";

revoke trigger on table "public"."detalle_seguimiento_rn" from "anon";

revoke truncate on table "public"."detalle_seguimiento_rn" from "anon";

revoke update on table "public"."detalle_seguimiento_rn" from "anon";

revoke delete on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke insert on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke references on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke select on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke trigger on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke truncate on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke update on table "public"."detalle_seguimiento_rn" from "authenticated";

revoke delete on table "public"."detalle_seguimiento_rn" from "service_role";

revoke insert on table "public"."detalle_seguimiento_rn" from "service_role";

revoke references on table "public"."detalle_seguimiento_rn" from "service_role";

revoke select on table "public"."detalle_seguimiento_rn" from "service_role";

revoke trigger on table "public"."detalle_seguimiento_rn" from "service_role";

revoke truncate on table "public"."detalle_seguimiento_rn" from "service_role";

revoke update on table "public"."detalle_seguimiento_rn" from "service_role";

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_materno_perinatal FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_primera_infancia FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atenciones FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_cronicidad FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_hipertension_detalles FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.intervenciones_colectivas FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.medicos FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.tamizaje_oncologico FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');


