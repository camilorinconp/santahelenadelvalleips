from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class ControlDislipidemiaDetalles(BaseModel):
    id: Optional[UUID4] = None
    control_cronicidad_id: UUID4 # FK a la tabla ControlCronicidad

    ultimo_ct: Optional[float] = None # Colesterol Total
    fecha_ultimo_ct: Optional[date] = None
    fuente_ultimo_ct: Optional[str] = None

    ultimo_ldl: Optional[float] = None
    fecha_ultimo_ldl: Optional[date] = None
    fuente_ultimo_ldl: Optional[str] = None

    ultimo_tg: Optional[float] = None # Triglicéridos
    fecha_ultimo_tg: Optional[date] = None
    fuente_ultimo_tg: Optional[str] = None

    ultimo_hdl: Optional[float] = None
    fecha_ultimo_hdl: Optional[date] = None
    fuente_ultimo_hdl: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
