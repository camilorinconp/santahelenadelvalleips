create extension if not exists "moddatetime" with schema "extensions";

drop extension if exists "pg_net";


  create table "public"."atencion_materno_perinatal" (
    "id" uuid not null default gen_random_uuid(),
    "atencion_id" uuid not null,
    "estado_gestacional_semanas" integer,
    "fecha_probable_parto" date,
    "numero_controles_prenatales" integer,
    "riesgo_biopsicosocial" text,
    "resultado_tamizaje_vih" text,
    "resultado_tamizaje_sifilis" text,
    "tipo_parto" text,
    "fecha_parto" date not null,
    "complicaciones_parto" text,
    "peso_recien_nacido_kg" double precision,
    "talla_recien_nacido_cm" double precision,
    "apgar_recien_nacido" integer,
    "tamizaje_auditivo_neonatal" boolean,
    "tamizaje_metabolico_neonatal" boolean,
    "estado_puerperio_observaciones" text,
    "creado_en" timestamp with time zone default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."atencion_materno_perinatal" enable row level security;


  create table "public"."atencion_primera_infancia" (
    "id" uuid not null default gen_random_uuid(),
    "atencion_id" uuid,
    "peso_kg" double precision,
    "talla_cm" double precision,
    "perimetro_cefalico_cm" double precision,
    "estado_nutricional" text,
    "desarrollo_fisico_motor_observaciones" text,
    "desarrollo_socioemocional_observado" text,
    "desarrollo_cognitivo_observaciones" text,
    "salud_visual_observaciones" text,
    "salud_auditiva_comunicativa_observaciones" text,
    "salud_bucal_observaciones" text,
    "salud_sexual_observaciones" text,
    "salud_mental_observaciones" text,
    "practicas_alimentarias_observaciones" text,
    "esquema_vacunacion_completo" boolean,
    "suministro_micronutrientes" boolean,
    "desparasitacion_intestinal" boolean,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."atencion_primera_infancia" enable row level security;


  create table "public"."atenciones" (
    "id" uuid not null default gen_random_uuid(),
    "paciente_id" uuid not null default gen_random_uuid(),
    "medico_id" uuid default gen_random_uuid(),
    "codigo_rias_id" uuid,
    "fecha_atencion" date not null,
    "descripcion" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone,
    "entorno" text,
    "detalle_id" uuid
      );


alter table "public"."atenciones" enable row level security;


  create table "public"."codigos_rias" (
    "id" uuid not null default gen_random_uuid(),
    "codigo CUPS" text not null,
    "descripcion" text not null,
    "ciclo_vida" text not null,
    "creado_en" timestamp with time zone not null default now()
      );


alter table "public"."codigos_rias" enable row level security;


  create table "public"."control_cronicidad" (
    "id" uuid not null default gen_random_uuid(),
    "atencion_id" uuid not null,
    "tipo_cronicidad" text not null,
    "fecha_control" date not null,
    "estado_control" text,
    "adherencia_tratamiento" text,
    "peso_kg" double precision,
    "talla_cm" double precision,
    "imc" double precision,
    "detalle_cronicidad_id" uuid,
    "complicaciones_observadas" text,
    "observaciones" text,
    "creado_en" timestamp with time zone not null,
    "updated_at" timestamp with time zone,
    "medico_id" uuid not null
      );


alter table "public"."control_cronicidad" enable row level security;


  create table "public"."control_diabetes_detalles" (
    "id" uuid not null default gen_random_uuid(),
    "control_cronicidad_id" uuid not null,
    "ultima_hba1c" double precision,
    "fecha_ultima_hba1c" date,
    "fuente_ultima_hba1c" text,
    "rango_hba1c_ultima" text,
    "anterior_hba1c" double precision,
    "fecha_anterior_hba1c" date,
    "fuente_anterior_hba1c" text,
    "rango_hba1c_anterior" text,
    "diferencia_hba1c" double precision,
    "seguimiento_hba1c" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."control_diabetes_detalles" enable row level security;


  create table "public"."control_dislipidemia_detalles" (
    "id" uuid not null default gen_random_uuid(),
    "control_cronicidad_id" uuid not null,
    "ultimo_ct" double precision,
    "fecha_ultimo_ct" date,
    "fuente_ultimo_ct" text,
    "ultimo_ldl" double precision,
    "fecha_ultimo_ldl" date,
    "fuente_ultimo_ldl" text,
    "ultimo_tg" double precision,
    "fecha_ultimo_tg" date,
    "fuente_ultimo_tg" text,
    "ultimo_hdl" double precision,
    "fecha_ultimo_hdl" date,
    "fuente_ultimo_hdl" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."control_dislipidemia_detalles" enable row level security;


  create table "public"."control_erc_detalles" (
    "id" uuid not null default gen_random_uuid(),
    "control_cronicidad_id" uuid not null,
    "ultima_creatinina" double precision,
    "fecha_ultima_creatinina" date,
    "fuente_ultima_creatinina" text,
    "ultima_microalbuminuria" double precision,
    "fecha_ultima_microalbuminuria" date,
    "fuente_ultima_microalbuminuria" text,
    "ultima_relacion_albuminuria_creatinuria" double precision,
    "fecha_ultima_relacion_albuminuria_crea" date,
    "fuente_ultima_relacion_albuminuria_cre" text,
    "tasa_filtracion_glomerular_cockroft_gault" double precision,
    "estadio_erc_cockroft_gault" text,
    "tasa_filtracion_glomerular_ckd_epi" double precision,
    "estadio_erc_ckd_epi" text,
    "tasa_filtracion_glomerular_reportado_c" double precision,
    "estadio_erc_reportado_cac_2020" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."control_erc_detalles" enable row level security;


  create table "public"."control_hipertension_detalles" (
    "id" uuid not null default gen_random_uuid(),
    "control_cronicidad_id" uuid not null,
    "presion_arterial_sistolica" integer,
    "presion_arterial_diastolica" integer,
    "presion_arterial_sistolica_anterior" integer,
    "presion_arterial_diastolica_anterior" integer,
    "fecha_ta_anterior" date,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."control_hipertension_detalles" enable row level security;


  create table "public"."intervenciones_colectivas" (
    "id" uuid not null default gen_random_uuid(),
    "fecha_intervencion" date not null,
    "entorno" text not null,
    "tema" text not null,
    "poblacion_objetivo" text not null,
    "responsable_id" uuid,
    "resumen" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."intervenciones_colectivas" enable row level security;


  create table "public"."medicos" (
    "id" uuid not null default gen_random_uuid(),
    "primer_nombre" text not null,
    "segundo_nombre" text,
    "primer_apellido" text not null,
    "segundo_apellido" text,
    "registro_profesional" text not null,
    "especialidad" text not null,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."medicos" enable row level security;


  create table "public"."pacientes" (
    "id" uuid not null default gen_random_uuid(),
    "tipo_documento" text not null,
    "numero_documento" text not null,
    "primer_nombre" text not null,
    "segundo_nombre" text,
    "primer_apellido" text not null,
    "segundo_apellido" text,
    "fecha_nacimiento" date not null,
    "genero" text not null,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone
      );


alter table "public"."pacientes" enable row level security;


  create table "public"."tamizaje_oncologico" (
    "atencion_id" uuid not null,
    "tipo_tamizaje" text not null,
    "fecha_tamizaje" date not null,
    "resultado_tamizaje" text,
    "fecha_proximo_tamizaje" date,
    "citologia_resultado" text,
    "adn_vph_resultado" text,
    "colposcopia_realizada" boolean,
    "biopsia_realizada_cuello" boolean,
    "mamografia_resultado" text,
    "examen_clinico_mama_observaciones" text,
    "biopsia_realizada_mama" boolean,
    "psa_resultado" double precision,
    "tacto_rectal_resultado" text,
    "biopsia_realizada_prostata" boolean,
    "sangre_oculta_heces_resultado" text,
    "colonoscopia_realizada" boolean,
    "biopsia_realizada_colon" boolean,
    "observaciones" text,
    "creado_en" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone,
    "id" uuid not null default gen_random_uuid()
      );


alter table "public"."tamizaje_oncologico" enable row level security;

CREATE UNIQUE INDEX atencion_materno_perinatal_pkey ON public.atencion_materno_perinatal USING btree (id);

CREATE UNIQUE INDEX atencion_primera_infancia_pkey ON public.atencion_primera_infancia USING btree (id);

CREATE UNIQUE INDEX atenciones_pkey ON public.atenciones USING btree (id);

CREATE UNIQUE INDEX "codigos_rias_codigo CUPS_key" ON public.codigos_rias USING btree ("codigo CUPS");

CREATE UNIQUE INDEX codigos_rias_pkey ON public.codigos_rias USING btree (id);

CREATE UNIQUE INDEX control_cronicidad_pkey ON public.control_cronicidad USING btree (id);

CREATE UNIQUE INDEX control_diabetes_detalles_pkey ON public.control_diabetes_detalles USING btree (id);

CREATE UNIQUE INDEX control_dislipidemia_detalles_pkey ON public.control_dislipidemia_detalles USING btree (id);

CREATE UNIQUE INDEX control_erc_detalles_pkey ON public.control_erc_detalles USING btree (id);

CREATE UNIQUE INDEX control_hipertension_detalles_pkey ON public.control_hipertension_detalles USING btree (id);

CREATE UNIQUE INDEX intervenciones_colectivas_pkey ON public.intervenciones_colectivas USING btree (id);

CREATE UNIQUE INDEX medicos_pkey ON public.medicos USING btree (id);

CREATE UNIQUE INDEX medicos_registro_profesional_key ON public.medicos USING btree (registro_profesional);

CREATE UNIQUE INDEX pacientes_numero_documento_key ON public.pacientes USING btree (numero_documento);

CREATE UNIQUE INDEX pacientes_pkey ON public.pacientes USING btree (id);

alter table "public"."atencion_materno_perinatal" add constraint "atencion_materno_perinatal_pkey" PRIMARY KEY using index "atencion_materno_perinatal_pkey";

alter table "public"."atencion_primera_infancia" add constraint "atencion_primera_infancia_pkey" PRIMARY KEY using index "atencion_primera_infancia_pkey";

alter table "public"."atenciones" add constraint "atenciones_pkey" PRIMARY KEY using index "atenciones_pkey";

alter table "public"."codigos_rias" add constraint "codigos_rias_pkey" PRIMARY KEY using index "codigos_rias_pkey";

alter table "public"."control_cronicidad" add constraint "control_cronicidad_pkey" PRIMARY KEY using index "control_cronicidad_pkey";

alter table "public"."control_diabetes_detalles" add constraint "control_diabetes_detalles_pkey" PRIMARY KEY using index "control_diabetes_detalles_pkey";

alter table "public"."control_dislipidemia_detalles" add constraint "control_dislipidemia_detalles_pkey" PRIMARY KEY using index "control_dislipidemia_detalles_pkey";

alter table "public"."control_erc_detalles" add constraint "control_erc_detalles_pkey" PRIMARY KEY using index "control_erc_detalles_pkey";

alter table "public"."control_hipertension_detalles" add constraint "control_hipertension_detalles_pkey" PRIMARY KEY using index "control_hipertension_detalles_pkey";

alter table "public"."intervenciones_colectivas" add constraint "intervenciones_colectivas_pkey" PRIMARY KEY using index "intervenciones_colectivas_pkey";

alter table "public"."medicos" add constraint "medicos_pkey" PRIMARY KEY using index "medicos_pkey";

alter table "public"."pacientes" add constraint "pacientes_pkey" PRIMARY KEY using index "pacientes_pkey";

alter table "public"."atencion_materno_perinatal" add constraint "atencion_materno_perinatal_atencion_id_fkey" FOREIGN KEY (atencion_id) REFERENCES atenciones(id) ON DELETE CASCADE not valid;

alter table "public"."atencion_materno_perinatal" validate constraint "atencion_materno_perinatal_atencion_id_fkey";

alter table "public"."atencion_primera_infancia" add constraint "atencion_primera_infancia_atencion_id_fkey" FOREIGN KEY (atencion_id) REFERENCES atenciones(id) ON DELETE CASCADE not valid;

alter table "public"."atencion_primera_infancia" validate constraint "atencion_primera_infancia_atencion_id_fkey";

alter table "public"."atenciones" add constraint "atenciones_codigo_rias_id_fkey" FOREIGN KEY (codigo_rias_id) REFERENCES codigos_rias(id) ON DELETE SET NULL not valid;

alter table "public"."atenciones" validate constraint "atenciones_codigo_rias_id_fkey";

alter table "public"."atenciones" add constraint "atenciones_medico_id_fkey" FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE SET NULL not valid;

alter table "public"."atenciones" validate constraint "atenciones_medico_id_fkey";

alter table "public"."atenciones" add constraint "atenciones_paciente_id_fkey" FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE not valid;

alter table "public"."atenciones" validate constraint "atenciones_paciente_id_fkey";

alter table "public"."codigos_rias" add constraint "codigos_rias_codigo CUPS_key" UNIQUE using index "codigos_rias_codigo CUPS_key";

alter table "public"."control_cronicidad" add constraint "control_cronicidad_atencion_id_fkey" FOREIGN KEY (atencion_id) REFERENCES atenciones(id) ON DELETE CASCADE not valid;

alter table "public"."control_cronicidad" validate constraint "control_cronicidad_atencion_id_fkey";

alter table "public"."control_diabetes_detalles" add constraint "control_diabetes_detalles_control_cronicidad_id_fkey" FOREIGN KEY (control_cronicidad_id) REFERENCES control_cronicidad(id) ON DELETE CASCADE not valid;

alter table "public"."control_diabetes_detalles" validate constraint "control_diabetes_detalles_control_cronicidad_id_fkey";

alter table "public"."control_dislipidemia_detalles" add constraint "control_dislipidemia_detalles_control_cronicidad_id_fkey" FOREIGN KEY (control_cronicidad_id) REFERENCES control_cronicidad(id) ON DELETE CASCADE not valid;

alter table "public"."control_dislipidemia_detalles" validate constraint "control_dislipidemia_detalles_control_cronicidad_id_fkey";

alter table "public"."control_erc_detalles" add constraint "control_erc_detalles_control_cronicidad_id_fkey" FOREIGN KEY (control_cronicidad_id) REFERENCES control_cronicidad(id) ON DELETE CASCADE not valid;

alter table "public"."control_erc_detalles" validate constraint "control_erc_detalles_control_cronicidad_id_fkey";

alter table "public"."control_hipertension_detalles" add constraint "control_hipertension_detalles_control_cronicidad_id_fkey" FOREIGN KEY (control_cronicidad_id) REFERENCES control_cronicidad(id) ON DELETE CASCADE not valid;

alter table "public"."control_hipertension_detalles" validate constraint "control_hipertension_detalles_control_cronicidad_id_fkey";

alter table "public"."intervenciones_colectivas" add constraint "intervenciones_colectivas_responsable_id_fkey" FOREIGN KEY (responsable_id) REFERENCES medicos(id) ON DELETE SET NULL not valid;

alter table "public"."intervenciones_colectivas" validate constraint "intervenciones_colectivas_responsable_id_fkey";

alter table "public"."medicos" add constraint "medicos_registro_profesional_key" UNIQUE using index "medicos_registro_profesional_key";

alter table "public"."pacientes" add constraint "pacientes_numero_documento_key" UNIQUE using index "pacientes_numero_documento_key";

alter table "public"."tamizaje_oncologico" add constraint "tamizaje_oncologico_atencion_id_fkey" FOREIGN KEY (atencion_id) REFERENCES atenciones(id) ON DELETE CASCADE not valid;

alter table "public"."tamizaje_oncologico" validate constraint "tamizaje_oncologico_atencion_id_fkey";


  create policy "For full access without any restrictions"
  on "public"."atencion_materno_perinatal"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."atencion_primera_infancia"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."atenciones"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."control_cronicidad"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."control_diabetes_detalles"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."control_dislipidemia_detalles"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."control_erc_detalles"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."control_hipertension_detalles"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."intervenciones_colectivas"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."medicos"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "For full access without any restrictions"
  on "public"."pacientes"
  as permissive
  for all
  to public
using (true)
with check (true);



  create policy "allow_select_all"
  on "public"."pacientes"
  as permissive
  for select
  to public
using (true);



  create policy "For full access without any restrictions"
  on "public"."tamizaje_oncologico"
  as permissive
  for all
  to public
using (true)
with check (true);


CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_materno_perinatal FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atencion_primera_infancia FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.atenciones FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_cronicidad FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.control_hipertension_detalles FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.intervenciones_colectivas FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.medicos FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

CREATE TRIGGER handle_updated_at BEFORE UPDATE ON public.tamizaje_oncologico FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');


