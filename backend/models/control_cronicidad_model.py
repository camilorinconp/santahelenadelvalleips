from pydantic import BaseModel, Field
from typing import Optional, Union, Literal
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
    # tipo_cronicidad ya no necesita el discriminator aquí
    tipo_cronicidad: str
    detalle_cronicidad_id: Optional[UUID] = None # FK a la tabla de detalles específicos

class ControlCronicidadHipertension(ControlCronicidad):
    tipo_cronicidad: Literal["Hipertension"]
    detalles: ControlHipertensionDetalles

class ControlCronicidadDiabetes(ControlCronicidad):
    tipo_cronicidad: Literal["Diabetes"]
    detalles: ControlDiabetesDetalles

class ControlCronicidadERC(ControlCronicidad):
    tipo_cronicidad: Literal["ERC"]
    detalles: ControlERCDetalles

class ControlCronicidadDislipidemia(ControlCronicidad):
    tipo_cronicidad: Literal["Dislipidemia"]
    detalles: ControlDislipidemiaDetalles

# La unión discriminada se define aquí, usando el campo 'tipo_cronicidad' como discriminador
ControlCronicidadPolimorfica = Union[
    ControlCronicidadHipertension,
    ControlCronicidadDiabetes,
    ControlCronicidadERC,
    ControlCronicidadDislipidemia
]