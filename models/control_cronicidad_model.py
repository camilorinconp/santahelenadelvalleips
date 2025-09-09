from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class ControlCronicidad(BaseModel):
    id: Optional[UUID4] = None
    atencion_id: UUID4 # FK a la tabla de atenciones generales

    # Campos Generales del Control de Cronicidad
    tipo_cronicidad: str # Ej: "Diabetes", "Hipertensión", "EPOC", "Enfermedad Cardiovascular"
    fecha_control: date
    estado_control: Optional[str] = None # Ej: "Estable", "Descompensado", "En Remisión"
    adherencia_tratamiento: Optional[str] = None # Ej: "Buena", "Regular", "Mala"

    # Métricas Generales (comunes a muchos controles de cronicidad)
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    imc: Optional[float] = None
    
    # Conexión a tabla de detalles específicos
    detalle_cronicidad_id: Optional[UUID4] = None # FK a la tabla de detalles específicos (ej. ControlHipertensionDetalles)

    complicaciones_observadas: Optional[str] = None
    observaciones: Optional[str] = None

    # Fechas de control
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None