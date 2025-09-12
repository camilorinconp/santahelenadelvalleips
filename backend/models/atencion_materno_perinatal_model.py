from pydantic import BaseModel
from typing import Optional, Union
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# Definición de ENUMs (reflejando los de la DB)
class EnumRiesgoBiopsicosocial(str, Enum):
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"
    NO_APLICA = "NO_APLICA"
    PENDIENTE = "PENDIENTE"

class EnumResultadoTamizajeSerologia(str, Enum):
    REACTIVO = "REACTIVO"
    NO_REACTIVO = "NO_REACTIVO"
    INDETERMINADO = "INDETERMINADO"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumResultadoPositivoNegativo(str, Enum):
    POSITIVO = "POSITIVO"
    NEGATIVO = "NEGATIVO"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumHemoclasificacion(str, Enum):
    A_POS = "A_POS"
    A_NEG = "A_NEG"
    B_POS = "B_POS"
    B_NEG = "B_NEG"
    AB_POS = "AB_POS"
    AB_NEG = "AB_NEG"
    O_POS = "O_POS"
    O_NEG = "O_NEG"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumTipoParto(str, Enum):
    VAGINAL = "VAGINAL"
    CESAREA = "CESAREA"
    INSTRUMENTADO = "INSTRUMENTADO"
    OTRO = "OTRO"
    PENDIENTE = "PENDIENTE"

class EnumManejoAlumbramiento(str, Enum):
    ACTIVO = "ACTIVO"
    FISIOLOGICO = "FISIOLOGICO"
    NO_APLICA = "NO_APLICA"
    PENDIENTE = "PENDIENTE"

class EnumEstadoConciencia(str, Enum):
    ALERTA = "ALERTA"
    SOMNOLIENTA = "SOMNOLIENTA"
    CONFUSA = "CONFUSA"
    COMA = "COMA"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumViaAdministracion(str, Enum):
    IM = "IM"
    IV = "IV"
    SUBLINGUAL = "SUBLINGUAL"
    ORAL = "ORAL"
    NO_APLICA = "NO_APLICA"
    PENDIENTE = "PENDIENTE"

class EnumAlimentacionEgreso(str, Enum):
    LACTANCIA_MATERNA_EXCLUSIVA = "LACTANCIA_MATERNA_EXCLUSIVA"
    FORMULA = "FORMULA"
    MIXTA = "MIXTA"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumTipoPinzamientoCordon(str, Enum):
    INMEDIATO = "INMEDIATO"
    TARDIO = "TARDIO"
    NO_APLICA = "NO_APLICA"

class EnumMetodoIdentificacionRN(str, Enum):
    BRAZALETE = "BRAZALETE"
    HUELLA_PLANTAR = "HUELLA_PLANTAR"
    FOTO = "FOTO"
    OTRO = "OTRO"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumMetodoAnticonceptivoPostparto(str, Enum):
    DIU_POSPARTO = "DIU_POSPARTO"
    OTB = "OTB"
    IMPLANTE_SUBDERMICO = "IMPLANTE_SUBDERMICO"
    INYECTABLE = "INYECTABLE"
    ORAL_PROGESTINA = "ORAL_PROGESTINA"
    CONDONES = "CONDONES"
    NINGUNO = "NINGUNO"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

class EnumEstadoNutricional(str, Enum):
    NORMAL = "NORMAL"
    SOBREPESO = "SOBREPESO"
    OBESIDAD = "OBESIDAD"
    BAJO_PESO = "BAJO_PESO"
    PENDIENTE = "PENDIENTE"
    NO_APLICA = "NO_APLICA"

# Modelos de Sub-Sub-Detalle (Polimorfismo Anidado Nivel 2)

class DetallePreconcepcionalAnamnesis(BaseModel):
    id: Optional[UUID] = None
    detalle_control_prenatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    antecedente_trombofilias: Optional[bool] = None
    antecedente_anemia: Optional[bool] = None
    antecedente_asma: Optional[bool] = None
    antecedente_tuberculosis: Optional[bool] = None
    antecedente_neoplasias: Optional[bool] = None
    antecedente_obesidad_morbida: Optional[bool] = None
    antecedente_patologia_cervical_vph: Optional[bool] = None
    antecedente_cumplimiento_tamizaje_ccu: Optional[bool] = None
    antecedente_numero_companeros_sexuales: Optional[int] = None
    antecedente_uso_preservativo: Optional[bool] = None
    antecedente_uso_anticonceptivos: Optional[bool] = None
    antecedente_parto_pretermito_previo: Optional[bool] = None
    antecedente_cesarea_previa: Optional[bool] = None
    antecedente_abortos_previos: Optional[int] = None
    antecedente_muerte_fetal_previa: Optional[bool] = None
    antecedente_gran_multiparidad: Optional[bool] = None
    antecedente_periodo_intergenesico_corto: Optional[bool] = None
    antecedente_incompatibilidad_rh: Optional[bool] = None
    antecedente_preeclampsia_gestacion_anterior: Optional[bool] = None
    antecedente_rn_peso_menor_2500g: Optional[bool] = None
    antecedente_rn_macrosomico: Optional[bool] = None
    antecedente_hemorragia_postparto_previo: Optional[bool] = None
    antecedente_embarazo_molar: Optional[bool] = None
    antecedente_depresion_postparto_previo: Optional[bool] = None

class DetallePreconcepcionalParaclinicos(BaseModel):
    id: Optional[UUID] = None
    detalle_control_prenatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resultado_glicemia_ayunas: Optional[float] = None
    resultado_hemograma: Optional[str] = None
    resultado_igg_varicela: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_tamizaje_ccu: Optional[str] = None

class DetallePreconcepcionalAntropometria(BaseModel):
    id: Optional[UUID] = None
    detalle_control_prenatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    imc: Optional[float] = None
    estado_nutricional: Optional[EnumEstadoNutricional] = None

class DetalleRNAtencionInmediata(BaseModel):
    id: Optional[UUID] = None
    detalle_recien_nacido_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    limpieza_vias_aereas_realizada: Optional[bool] = None
    secado_rn_realizado: Optional[bool] = None
    observacion_respiracion_llanto_tono: Optional[str] = None
    tipo_pinzamiento_cordon: Optional[EnumTipoPinzamientoCordon] = None
    contacto_piel_a_piel_realizado: Optional[bool] = None
    manejo_termico_observaciones: Optional[str] = None
    metodo_identificacion_rn: Optional[EnumMetodoIdentificacionRN] = None
    registro_nacido_vivo_realizado: Optional[bool] = None
    examen_fisico_rn_observaciones: Optional[str] = None

# Modelos de Sub-Detalle (Polimorfismo Anidado Nivel 1)

class DetalleControlPrenatal(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    estado_gestacional_semanas: Optional[int] = None
    fecha_probable_parto: Optional[date] = None
    numero_controles_prenatales: Optional[int] = None
    riesgo_biopsicosocial: Optional[EnumRiesgoBiopsicosocial] = None
    resultado_tamizaje_vih: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_tamizaje_sifilis: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_tamizaje_hepatitis_b: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_tamizaje_toxoplasmosis: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_tamizaje_estreptococo_b: Optional[EnumResultadoPositivoNegativo] = None
    hemoclasificacion: Optional[EnumHemoclasificacion] = None
    resultado_urocultivo: Optional[EnumResultadoPositivoNegativo] = None
    vacunacion_tdap_completa: Optional[bool] = None
    vacunacion_influenza_completa: Optional[bool] = None
    suplementacion_hierro: Optional[bool] = None
    suplementacion_acido_folico: Optional[bool] = None
    suplementacion_calcio: Optional[bool] = None
    condicion_diabetes_preexistente: Optional[bool] = None
    condicion_hipertension_preexistente: Optional[bool] = None
    condicion_tiroidea_preexistente: Optional[bool] = None
    condicion_epilepsia_preexistente: Optional[bool] = None
    num_gestaciones: Optional[int] = None
    num_partos: Optional[int] = None
    num_cesareas: Optional[int] = None
    num_abortos: Optional[int] = None
    num_muertes_perinatales: Optional[int] = None
    antecedente_preeclampsia: Optional[bool] = None
    antecedente_hemorragia_postparto: Optional[bool] = None
    antecedente_embarazo_multiple: Optional[bool] = None
    signo_alarma_sangrado: Optional[bool] = None
    signo_alarma_cefalea: Optional[bool] = None
    signo_alarma_vision_borrosa: Optional[bool] = None
    
    # Polimorfismo anidado para sub-sub-detalles
    sub_tipo_preconcepcional: Optional[str] = None
    sub_detalle_preconcepcional_id: Optional[UUID] = None

class DetalleParto(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tipo_parto: Optional[EnumTipoParto] = None
    fecha_parto: Optional[date] = None
    hora_parto: Optional[str] = None
    complicaciones_parto: Optional[str] = None
    manejo_alumbramiento: Optional[EnumManejoAlumbramiento] = None
    inicio_contracciones: Optional[datetime] = None
    percepcion_movimientos_fetales: Optional[bool] = None
    expulsion_tapon_mucoso: Optional[bool] = None
    ruptura_membranas: Optional[bool] = None
    sangrado_vaginal: Optional[str] = None
    sintomas_preeclampsia_premonitorios: Optional[dict] = None # JSONB
    antecedentes_patologicos_parto: Optional[str] = None
    estado_conciencia_materna: Optional[EnumEstadoConciencia] = None
    estado_nutricional_materna: Optional[EnumEstadoNutricional] = None
    signos_vitales_maternos: Optional[dict] = None # JSONB
    valoracion_obstetrica_observaciones: Optional[str] = None
    valoracion_ginecologica_observaciones: Optional[str] = None
    resultado_prueba_treponemica_rapida: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_vdrl_rpr: Optional[EnumResultadoTamizajeSerologia] = None
    resultado_gota_gruesa_malaria: Optional[EnumResultadoPositivoNegativo] = None
    resultado_hematocrito: Optional[float] = None
    resultado_hemoglobina: Optional[float] = None
    resultado_antigeno_hepatitis_b: Optional[EnumResultadoTamizajeSerologia] = None
    pinzamiento_cordon_tardio: Optional[bool] = None
    oxitocina_administrada_ui: Optional[float] = None
    oxitocina_via: Optional[EnumViaAdministracion] = None
    misoprostol_administrado_mcg: Optional[float] = None
    misoprostol_via: Optional[EnumViaAdministracion] = None
    traccion_cordon_controlada: Optional[bool] = None
    utero_contraido_postparto: Optional[bool] = None

class DetalleRecienNacido(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    peso_recien_nacido_kg: Optional[float] = None
    talla_recien_nacido_cm: Optional[float] = None
    apgar_min1: Optional[int] = None
    apgar_min5: Optional[int] = None
    alimentacion_egreso: Optional[EnumAlimentacionEgreso] = None
    
    # Polimorfismo anidado para sub-sub-detalles
    sub_tipo_rn_atencion: Optional[str] = None
    sub_detalle_rn_id: Optional[UUID] = None

class DetallePuerperio(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    estado_puerperio_observaciones: Optional[str] = None
    signo_alarma_fiebre_postparto: Optional[bool] = None
    signo_alarma_sangrado_excesivo_postparto: Optional[bool] = None
    metodo_anticonceptivo_postparto: Optional[EnumMetodoAnticonceptivoPostparto] = None
    tamizaje_depresion_postparto_epds: Optional[int] = None
    temperatura_corporal: Optional[float] = None
    presion_arterial_sistolica: Optional[int] = None
    presion_arterial_diastolica: Optional[int] = None
    ritmo_cardiaco: Optional[int] = None
    frecuencia_respiratoria: Optional[int] = None
    perfusion_observaciones: Optional[str] = None
    estado_conciencia_materna: Optional[EnumEstadoConciencia] = None
    involucion_uterina_observaciones: Optional[str] = None
    loquios_observaciones: Optional[str] = None
    complicaciones_puerperales: Optional[dict] = None # JSONB
    deambulacion_temprana: Optional[bool] = None
    alimentacion_adecuada_observaciones: Optional[str] = None
    dificultad_miccional: Optional[bool] = None
    cicatriz_cesarea_episiotomia_observaciones: Optional[str] = None
    vacunacion_esquema_completo_postparto: Optional[bool] = None
    inmunoglobulina_anti_d_administrada: Optional[bool] = None
    dolor_involucion_uterina: Optional[bool] = None
    dificultad_miccional_observaciones: Optional[str] = None
    signos_alarma_madre_postparto: Optional[dict] = None # JSONB
    asesoria_anticoncepcion_postparto: Optional[bool] = None

class DetalleSaludBucalMP(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    observaciones_salud_bucal: Optional[str] = None
    fecha_ultima_atencion_bucal: Optional[date] = None
    riesgo_caries: Optional[str] = None # Considerar ENUM
    riesgo_enfermedad_periodontal: Optional[str] = None # Considerar ENUM

class DetalleNutricionMP(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    patron_alimentario: Optional[str] = None
    frecuencia_consumo_alimentos: Optional[str] = None
    alimentos_preferidos_rechazados: Optional[str] = None
    trastornos_alimentarios: Optional[str] = None
    peso_pregestacional: Optional[float] = None
    imc_pregestacional: Optional[float] = None
    diagnostico_nutricional: Optional[str] = None # Considerar ENUM
    plan_manejo_nutricional: Optional[str] = None

class DetalleIVE(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    causal_ive: Optional[str] = None # Considerar ENUM
    fecha_ive: Optional[date] = None
    semanas_gestacion_ive: Optional[int] = None
    metodo_ive: Optional[str] = None # Considerar ENUM
    complicaciones_ive: Optional[str] = None
    asesoria_post_ive: Optional[str] = None

class DetalleCursoMaternidadPaternidad(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    fecha_inicio_curso: Optional[date] = None
    fecha_fin_curso: Optional[date] = None
    asistencia_curso: Optional[str] = None # Considerar ENUM (COMPLETA, PARCIAL, NO_ASISTE)
    temas_cubiertos: Optional[str] = None
    observaciones_curso: Optional[str] = None

class DetalleSeguimientoRN(BaseModel):
    id: Optional[UUID] = None
    atencion_materno_perinatal_id: Optional[UUID] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    fecha_seguimiento: Optional[date] = None
    peso_rn_seguimiento: Optional[float] = None
    talla_rn_seguimiento: Optional[float] = None
    perimetro_cefalico_rn_seguimiento: Optional[float] = None
    estado_nutricional_rn: Optional[EnumEstadoNutricional] = None
    observaciones_desarrollo_rn: Optional[str] = None
    tamizajes_pendientes_rn: Optional[str] = None # Esto se reemplazará por JSONB
    vacunacion_rn_completa: Optional[bool] = None
    antecedentes_seguimiento_rn: Optional[dict] = None # JSONB
    examen_fisico_rn_seguimiento: Optional[dict] = None # JSONB
    plan_cuidado_rn_seguimiento: Optional[dict] = None # JSONB
    tamizajes_rn_pendientes_detalle: Optional[dict] = None # JSONB

# Modelo Principal de AtencionMaternoPerinatal
class AtencionMaternoPerinatal(BaseModel):
    id: Optional[UUID] = None
    paciente_id: Optional[UUID] = None
    medico_id: Optional[UUID] = None
    atencion_id: Optional[UUID] = None # Vínculo con la atención general
    fecha_atencion: date
    entorno: Optional[str] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Relaciones con los modelos de sub-detalle (para lectura/respuesta)
    detalle_control_prenatal: Optional[DetalleControlPrenatal] = None
    detalle_parto: Optional[DetalleParto] = None
    detalle_recien_nacido: Optional[DetalleRecienNacido] = None
    detalle_puerperio: Optional[DetallePuerperio] = None
    detalle_salud_bucal_mp: Optional[DetalleSaludBucalMP] = None
    detalle_nutricion_mp: Optional[DetalleNutricionMP] = None
    detalle_ive: Optional[DetalleIVE] = None
    detalle_curso_maternidad_paternidad: Optional[DetalleCursoMaternidadPaternidad] = None
    detalle_seguimiento_rn: Optional[DetalleSeguimientoRN] = None