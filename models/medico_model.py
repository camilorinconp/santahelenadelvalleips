from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID # Importar UUID

class Medico(BaseModel):
    id: Optional[UUID] = None # Usar UUID
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    registro_profesional: Optional[str] = None
    especialidad: Optional[str] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None