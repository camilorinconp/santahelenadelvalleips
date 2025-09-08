from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class Medico(BaseModel):
    id: Optional[UUID4] = None
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    registro_profesional: Optional[str] = None
    especialidad: Optional[str] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
