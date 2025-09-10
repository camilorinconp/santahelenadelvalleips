from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID # Importar UUID

class Atencion(BaseModel):
    id: Optional[UUID] = None
    paciente_id: Optional[UUID] = None
    medico_id: Optional[UUID] = None
    fecha_atencion: date
    entorno: Optional[str] = None
    tipo_atencion: str
    detalle_id: UUID
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None