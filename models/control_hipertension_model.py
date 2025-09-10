from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID # Importar UUID

class ControlHipertensionDetalles(BaseModel):
    id: Optional[UUID] = None
    control_cronicidad_id: UUID # FK a la tabla ControlCronicidad

    presion_arterial_sistolica: Optional[int] = None
    presion_arterial_diastolica: Optional[int] = None
    presion_arterial_sistolica_anterior: Optional[int] = None
    presion_arterial_diastolica_anterior: Optional[int] = None
    fecha_ta_anterior: Optional[date] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None