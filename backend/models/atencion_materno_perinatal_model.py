from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID # Importar UUID

class AtencionMaternoPerinatal(BaseModel):
    id: Optional[UUID] = None
    paciente_id: Optional[UUID] = None # Hacer opcional como workaround para el problema de caché de Supabase
    medico_id: Optional[UUID] = None
    atencion_id: Optional[UUID] = None # Vínculo con la atención general
    fecha_atencion: date
    entorno: Optional[str] = None

    # Datos de la Gestación (Expansión)
    estado_gestacional_semanas: Optional[int] = None
    fecha_probable_parto: Optional[date] = None
    numero_controles_prenatales: Optional[int] = None
    riesgo_biopsicosocial: Optional[str] = None # Ej: "Bajo", "Medio", "Alto"
    # Nuevos campos de tamizaje
    resultado_tamizaje_vih: Optional[str] = None # Ej: "Positivo", "Negativo", "No realizado"
    resultado_tamizaje_sifilis: Optional[str] = None
    resultado_tamizaje_hepatitis_b: Optional[str] = None
    resultado_tamizaje_toxoplasmosis: Optional[str] = None
    resultado_tamizaje_estreptococo_b: Optional[str] = None
    # Nuevos campos de vacunación y suplementación
    vacunacion_tdap_completa: Optional[bool] = None
    vacunacion_influenza_completa: Optional[bool] = None
    suplementacion_hierro: Optional[bool] = None
    suplementacion_acido_folico: Optional[bool] = None
    suplementacion_calcio: Optional[bool] = None
    # Nuevos campos de condiciones médicas preexistentes
    condicion_diabetes_preexistente: Optional[bool] = None
    condicion_hipertension_preexistente: Optional[bool] = None
    condicion_tiroidea_preexistente: Optional[bool] = None
    condicion_epilepsia_preexistente: Optional[bool] = None
    # Nuevos campos de antecedentes obstétricos
    num_gestaciones: Optional[int] = None
    num_partos: Optional[int] = None
    num_cesareas: Optional[int] = None
    num_abortos: Optional[int] = None
    num_muertes_perinatales: Optional[int] = None
    antecedente_preeclampsia: Optional[bool] = None
    antecedente_hemorragia_postparto: Optional[bool] = None
    antecedente_embarazo_multiple: Optional[bool] = None
    # Nuevos campos de signos de alarma
    signo_alarma_sangrado: Optional[bool] = None
    signo_alarma_cefalea: Optional[bool] = None
    signo_alarma_vision_borrosa: Optional[bool] = None

    # Datos del Parto (Expansión)
    tipo_parto: Optional[str] = None
    fecha_parto: Optional[date] = None
    hora_parto: Optional[str] = None # HH:MM
    complicaciones_parto: Optional[str] = None
    manejo_alumbramiento: Optional[str] = None # Ej: "Activo", "Fisiologico"

    # Datos del Recién Nacido (Expansión)
    peso_recien_nacido_kg: Optional[float] = None
    talla_recien_nacido_cm: Optional[float] = None
    apgar_min1: Optional[int] = None
    apgar_min5: Optional[int] = None
    adaptacion_neonatal_observaciones: Optional[str] = None
    tamizaje_auditivo_neonatal: Optional[bool] = None
    tamizaje_metabolico_neonatal: Optional[bool] = None
    tamizaje_cardiopatias_congenitas: Optional[bool] = None
    profilaxis_vitamina_k: Optional[bool] = None
    profilaxis_ocular: Optional[bool] = None
    vacunacion_bcg: Optional[bool] = None
    vacunacion_hepatitis_b: Optional[bool] = None
    alimentacion_egreso: Optional[str] = None # Ej: "Lactancia Materna Exclusiva", "Mixta"

    # Datos del Puerperio (Expansión)
    estado_puerperio_observaciones: Optional[str] = None
    signo_alarma_fiebre_postparto: Optional[bool] = None
    signo_alarma_sangrado_excesivo_postparto: Optional[bool] = None
    metodo_anticonceptivo_postparto: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None