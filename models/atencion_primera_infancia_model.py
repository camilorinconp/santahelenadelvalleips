from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class AtencionPrimeraInfancia(BaseModel):
    id: Optional[UUID4] = None
    atencion_id: UUID4 # FK a la tabla de atenciones generales
    
    # Datos Antropométricos y Nutricionales
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    perimetro_cefalico_cm: Optional[float] = None
    estado_nutricional: Optional[str] = None # Ej: "Adecuado", "Bajo peso", "Sobrepeso"
    
    # Desarrollo
    desarrollo_fisico_motor_observaciones: Optional[str] = None
    desarrollo_socioemocional_observaciones: Optional[str] = None
    desarrollo_cognitivo_observaciones: Optional[str] = None
    
    # Salud Específica
    salud_visual_observaciones: Optional[str] = None
    salud_auditiva_comunicativa_observaciones: Optional[str] = None
    salud_bucal_observaciones: Optional[str] = None
    salud_sexual_observaciones: Optional[str] = None
    salud_mental_observaciones: Optional[str] = None
    
    # Prácticas y Hábitos
    practicas_alimentarias_observaciones: Optional[str] = None
    esquema_vacunacion_completo: Optional[bool] = None
    suministro_micronutrientes: Optional[bool] = None
    desparasitacion_intestinal: Optional[bool] = None
    
    # Fechas de control
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
