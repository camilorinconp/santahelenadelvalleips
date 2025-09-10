from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class AtencionPrimeraInfancia(BaseModel):
    id: Optional[UUID] = None
    paciente_id: UUID
    medico_id: Optional[UUID] = None
    fecha_atencion: date
    entorno: Optional[str] = None
    atencion_id: Optional[UUID] = None # Vínculo con la atención general

    # Datos Antropométricos y Nutricionales (Expansión)
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    perimetro_cefalico_cm: Optional[float] = None
    estado_nutricional: Optional[str] = None
    practicas_alimentarias_observaciones: Optional[str] = None
    suplementacion_hierro: Optional[bool] = None
    suplementacion_vitamina_a: Optional[bool] = None
    suplementacion_micronutrientes_polvo: Optional[bool] = None
    desparasitacion_intestinal: Optional[bool] = None

    # Desarrollo (Expansión)
    desarrollo_fisico_motor_observaciones: Optional[str] = None
    desarrollo_socioemocional_observaciones: Optional[str] = None
    desarrollo_cognitivo_observaciones: Optional[str] = None
    hitos_desarrollo_acordes_edad: Optional[bool] = None

    # Salud Específica (Expansión)
    salud_visual_observaciones: Optional[str] = None
    salud_visual_tamizaje_resultado: Optional[str] = None
    salud_auditiva_comunicativa_observaciones: Optional[str] = None
    salud_auditiva_tamizaje_resultado: Optional[str] = None
    salud_bucal_observaciones: Optional[str] = None
    salud_bucal_higiene_oral: Optional[str] = None
    salud_sexual_observaciones: Optional[str] = None
    salud_mental_observaciones: Optional[str] = None

    # Inmunizaciones (Expansión)
    esquema_vacunacion_completo: Optional[bool] = None
    vacunas_pendientes: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
