from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class ControlHipertensionDetalles(BaseModel):
    id: Optional[UUID4] = None
    control_cronicidad_id: UUID4 # FK a la tabla ControlCronicidad

    presion_arterial_sistolica: Optional[int] = None
    presion_arterial_diastolica: Optional[int] = None
    presion_arterial_sistolica_anterior: Optional[int] = None
    presion_arterial_diastolica_anterior: Optional[int] = None
    fecha_ta_anterior: Optional[date] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
