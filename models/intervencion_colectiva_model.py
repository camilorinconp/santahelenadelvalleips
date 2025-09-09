from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class IntervencionColectiva(BaseModel):
    id: Optional[UUID4] = None
    fecha_intervencion: date
    entorno: str  # Educativo, Comunitario, Laboral, etc.
    tema: str  # Ej: "Promoción de la salud mental", "Prevención de enfermedades transmitidas por vectores"
    poblacion_objetivo: str  # Ej: "Estudiantes de 5to grado", "Familias de la vereda X"
    responsable_id: Optional[UUID4] = None  # ID del médico o profesional a cargo
    resumen: Optional[str] = None
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
