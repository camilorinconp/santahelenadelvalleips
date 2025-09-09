from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class AtencionMaternoPerinatal(BaseModel):
    id: Optional[UUID4] = None
    atencion_id: UUID4 # FK a la tabla de atenciones generales

    # Datos de la Gestación
    estado_gestacional_semanas: Optional[int] = None
    fecha_probable_parto: Optional[date] = None
    numero_controles_prenatales: Optional[int] = None
    riesgo_biopsicosocial: Optional[str] = None # Ej: "Bajo", "Medio", "Alto"
    resultado_tamizaje_vih: Optional[str] = None # Ej: "Positivo", "Negativo", "No realizado"
    resultado_tamizaje_sifilis: Optional[str] = None # Ej: "Positivo", "Negativo", "No realizado"
    
    # Datos del Parto
    tipo_parto: Optional[str] = None # Ej: "Vaginal", "Cesárea"
    fecha_parto: Optional[date] = None
    complicaciones_parto: Optional[str] = None # Texto libre o código de complicaciones

    # Datos del Recién Nacido
    peso_recien_nacido_kg: Optional[float] = None
    talla_recien_nacido_cm: Optional[float] = None
    apgar_recien_nacido: Optional[int] = None # Puntuación de 0 a 10
    tamizaje_auditivo_neonatal: Optional[bool] = None
    tamizaje_metabolico_neonatal: Optional[bool] = None

    # Datos del Puerperio
    estado_puerperio_observaciones: Optional[str] = None
    
    # Fechas de control
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
