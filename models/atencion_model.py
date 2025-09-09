from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class Atencion(BaseModel):
    id: Optional[UUID4] = None
    paciente_id: UUID4
    medico_id: Optional[UUID4] = None # Opcional hasta que implementemos medicos
    codigo_rias_id: Optional[UUID4] = None # Opcional hasta que implementemos codigos_rias
    fecha_atencion: date
    entorno: Optional[str] = None # Puede ser: Institucional, Hogar, Comunitario, Laboral, Educativo
    descripcion: Optional[str] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
