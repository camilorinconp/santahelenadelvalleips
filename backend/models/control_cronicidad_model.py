from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date, datetime
from uuid import UUID # Importar UUID

from .control_hipertension_model import ControlHipertensionDetalles
from .control_diabetes_model import ControlDiabetesDetalles
from .control_erc_model import ControlERCDetalles
from .control_dislipidemia_model import ControlDislipidemiaDetalles

class ControlCronicidadBase(BaseModel):
    id: Optional[UUID] = None
    paciente_id: UUID
    medico_id: Optional[UUID] = None
    atencion_id: Optional[UUID] = None

    fecha_control: date
    estado_control: Optional[str] = None
    adherencia_tratamiento: Optional[str] = None

    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    imc: Optional[float] = None
    
    complicaciones_observadas: Optional[str] = None
    observaciones: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ControlCronicidad(ControlCronicidadBase):
    tipo_cronicidad: str = Field(..., discriminator='tipo_cronicidad')
    detalle_cronicidad_id: Optional[UUID] = None # FK a la tabla de detalles específicos

class ControlCronicidadHipertension(ControlCronicidad):
    tipo_cronicidad: str = Field("Hipertension", Literal="Hipertension")
    detalles: ControlHipertensionDetalles

class ControlCronicidadDiabetes(ControlCronicidad):
    tipo_cronicidad: str = Field("Diabetes", Literal="Diabetes")
    detalles: ControlDiabetesDetalles

class ControlCronicidadERC(ControlCronicidad):
    tipo_cronicidad: str = Field("ERC", Literal="ERC")
    detalles: ControlERCDetalles

class ControlCronicidadDislipidemia(ControlCronicidad):
    tipo_cronicidad: str = Field("Dislipidemia", Literal="Dislipidemia")
    detalles: ControlDislipidemiaDetalles

ControlCronicidadPolimorfica = Union[
    ControlCronicidadHipertension,
    ControlCronicidadDiabetes,
    ControlCronicidadERC,
    ControlCronicidadDislipidemia
]

