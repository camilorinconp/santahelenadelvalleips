from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class ControlDiabetesDetalles(BaseModel):
    id: Optional[UUID4] = None
    control_cronicidad_id: UUID4 # FK a la tabla ControlCronicidad

    ultima_hba1c: Optional[float] = None
    fecha_ultima_hba1c: Optional[date] = None
    fuente_ultima_hba1c: Optional[str] = None
    rango_hba1c_ultima: Optional[str] = None
    anterior_hba1c: Optional[float] = None
    fecha_anterior_hba1c: Optional[date] = None
    fuente_anterior_hba1c: Optional[str] = None
    rango_hba1c_anterior: Optional[str] = None
    diferencia_hba1c: Optional[float] = None
    seguimiento_hba1c: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
