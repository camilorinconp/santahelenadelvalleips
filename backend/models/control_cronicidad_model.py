from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union, Literal
from datetime import date, datetime
from uuid import UUID

from .control_hipertension_model import ControlHipertensionDetalles
from .control_diabetes_model import ControlDiabetesDetalles
from .control_erc_model import ControlERCDetalles
from .control_dislipidemia_model import ControlDislipidemiaDetalles

class ControlCronicidadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[UUID] = None
    paciente_id: UUID
    medico_id: Optional[UUID] = None
    atencion_id: Optional[UUID] = None

    fecha_control: date = Field(description="Fecha del control de cronicidad")
    estado_control: Optional[str] = Field(None, description="Estado del control: Controlado, No controlado, En proceso")
    adherencia_tratamiento: Optional[str] = Field(None, description="Adherencia al tratamiento: Buena, Regular, Mala")

    # Antropometría básica
    peso_kg: Optional[float] = Field(None, ge=0, le=300, description="Peso en kilogramos")
    talla_cm: Optional[float] = Field(None, ge=0, le=250, description="Talla en centímetros")
    imc: Optional[float] = Field(None, ge=0, le=100, description="Índice de masa corporal")
    
    # Observaciones clínicas
    complicaciones_observadas: Optional[str] = Field(None, description="Complicaciones observadas durante el control")
    observaciones: Optional[str] = Field(None, description="Observaciones generales del profesional")
    
    # Seguimiento farmacológico
    medicamentos_actuales: Optional[str] = Field(None, description="Lista de medicamentos actuales")
    efectos_adversos: Optional[str] = Field(None, description="Efectos adversos reportados")
    
    # Educación y recomendaciones
    educacion_brindada: Optional[str] = Field(None, description="Educación en salud brindada")
    recomendaciones_nutricionales: Optional[str] = Field(None, description="Recomendaciones nutricionales específicas")
    recomendaciones_actividad_fisica: Optional[str] = Field(None, description="Recomendaciones de actividad física")
    
    # Próxima cita
    fecha_proxima_cita: Optional[date] = Field(None, description="Fecha programada para próxima cita")
    
    # Timestamps
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Modelos para requests
class ControlCronicidadCrear(ControlCronicidadBase):
    tipo_cronicidad: Literal["Hipertension", "Diabetes", "ERC", "Dislipidemia"] = Field(description="Tipo de cronicidad a controlar")

class ControlCronicidadActualizar(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    medico_id: Optional[UUID] = None
    estado_control: Optional[str] = None
    adherencia_tratamiento: Optional[str] = None
    peso_kg: Optional[float] = Field(None, ge=0, le=300)
    talla_cm: Optional[float] = Field(None, ge=0, le=250)
    imc: Optional[float] = Field(None, ge=0, le=100)
    complicaciones_observadas: Optional[str] = None
    observaciones: Optional[str] = None
    medicamentos_actuales: Optional[str] = None
    efectos_adversos: Optional[str] = None
    educacion_brindada: Optional[str] = None
    recomendaciones_nutricionales: Optional[str] = None
    recomendaciones_actividad_fisica: Optional[str] = None
    fecha_proxima_cita: Optional[date] = None

# Modelo de respuesta con campos calculados
class ControlCronicidadResponse(ControlCronicidadBase):
    tipo_cronicidad: str
    detalle_cronicidad_id: Optional[UUID] = None
    
    # Campos calculados
    control_adecuado: Optional[bool] = Field(None, description="Si el control es adecuado según parámetros")
    riesgo_cardiovascular: Optional[str] = Field(None, description="Nivel de riesgo cardiovascular")
    adherencia_score: Optional[float] = Field(None, description="Score de adherencia 0-100")
    proxima_cita_recomendada_dias: Optional[int] = Field(None, description="Días recomendados para próxima cita")

# Modelos polimórficos con detalles específicos
class ControlCronicidad(ControlCronicidadBase):
    tipo_cronicidad: str
    detalle_cronicidad_id: Optional[UUID] = None

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

# Unión discriminada polimórfica
ControlCronicidadPolimorfica = Union[
    ControlCronicidadHipertension,
    ControlCronicidadDiabetes,
    ControlCronicidadERC,
    ControlCronicidadDislipidemia
]

# Funciones de utilidad para cálculos
def calcular_imc(peso_kg: float, talla_cm: float) -> float:
    """Calcular IMC a partir de peso y talla."""
    if peso_kg and talla_cm and talla_cm > 0:
        talla_m = talla_cm / 100
        return round(peso_kg / (talla_m ** 2), 2)
    return 0.0

def evaluar_control_adecuado(tipo_cronicidad: str, datos_control: dict) -> bool:
    """Evaluar si el control es adecuado según el tipo de cronicidad."""
    if tipo_cronicidad == "Hipertension":
        # Control adecuado si PA < 140/90
        sistolica = datos_control.get("presion_arterial_sistolica", 999)
        diastolica = datos_control.get("presion_arterial_diastolica", 999)
        return sistolica < 140 and diastolica < 90
    elif tipo_cronicidad == "Diabetes":
        # Control adecuado si HbA1c < 7%
        hba1c = datos_control.get("hba1c_porcentaje", 999)
        return hba1c < 7.0
    elif tipo_cronicidad == "ERC":
        # Control adecuado si TFG estable y proteinuria controlada
        tfg = datos_control.get("tasa_filtracion_glomerular", 0)
        return tfg >= 60  # Simplificado
    elif tipo_cronicidad == "Dislipidemia":
        # Control adecuado si LDL < 100
        ldl = datos_control.get("colesterol_ldl", 999)
        return ldl < 100
    return False