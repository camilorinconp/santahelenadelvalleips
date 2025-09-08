from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date

class Paciente(BaseModel):
    id: Optional[UUID4] = None
    tipo_documento: str
    numero_documento: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date
    genero: str