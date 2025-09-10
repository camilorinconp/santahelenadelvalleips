from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID # Importar UUID

class TamizajeOncologico(BaseModel):
    id: Optional[UUID] = None # Usar UUID
    paciente_id: UUID
    medico_id: Optional[UUID] = None
    atencion_id: Optional[UUID] = None # Vínculo con la atención general

    # Campos Generales del Tamizaje
    tipo_tamizaje: str # Ej: "Cuello Uterino", "Mama", "Próstata", "Colon y Recto"
    fecha_tamizaje: date
    resultado_tamizaje: Optional[str] = None # Ej: "Negativo", "Positivo", "Anormal", "Pendiente"
    fecha_proximo_tamizaje: Optional[date] = None

    # Campos Específicos para Cáncer de Cuello Uterino
    citologia_resultado: Optional[str] = None # Ej: "Normal", "ASCUS", "LSIL", "HSIL"
    adn_vph_resultado: Optional[str] = None # Ej: "Positivo", "Negativo"
    colposcopia_realizada: Optional[bool] = None
    biopsia_realizada_cuello: Optional[bool] = None

    # Campos Específicos para Cáncer de Mama
    mamografia_resultado: Optional[str] = None # Ej: "BI-RADS 0", "BI-RADS 1", ..., "BI-RADS 6"
    examen_clinico_mama_observaciones: Optional[str] = None
    biopsia_realizada_mama: Optional[bool] = None

    # Campos Específicos para Cáncer de Próstata
    psa_resultado: Optional[float] = None
    tacto_rectal_resultado: Optional[str] = None # Ej: "Normal", "Anormal"
    biopsia_realizada_prostata: Optional[bool] = None

    # Campos Específicos para Cáncer de Colon y Recto
    sangre_oculta_heces_resultado: Optional[str] = None # Ej: "Positivo", "Negativo"
    colonoscopia_realizada: Optional[bool] = None
    biopsia_realizada_colon: Optional[bool] = None

    # Observaciones Generales
    observaciones: Optional[str] = None

    # Fechas de control
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None