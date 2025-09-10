from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID # Importar UUID

class Paciente(BaseModel):
    id: Optional[UUID] = None # Usar UUID
    tipo_documento: str
    numero_documento: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date
    genero: str