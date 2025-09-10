from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class ControlERCDetalles(BaseModel):
    id: Optional[UUID4] = None
    control_cronicidad_id: UUID4 # FK a la tabla ControlCronicidad

    ultima_creatinina: Optional[float] = None
    fecha_ultima_creatinina: Optional[date] = None
    fuente_ultima_creatinina: Optional[str] = None
    
    ultima_microalbuminuria: Optional[float] = None
    fecha_ultima_microalbuminuria: Optional[date] = None
    fuente_ultima_microalbuminuria: Optional[str] = None
    
    ultima_relacion_albuminuria_creatinuria: Optional[float] = None
    fecha_ultima_relacion_albuminuria_creatinuria: Optional[date] = None
    fuente_ultima_relacion_albuminuria_creatinuria: Optional[str] = None
    
    tasa_filtracion_glomerular_cockroft_gault: Optional[float] = None
    estadio_erc_cockroft_gault: Optional[str] = None
    
    tasa_filtracion_glomerular_ckd_epi: Optional[float] = None
    estadio_erc_ckd_epi: Optional[str] = None
    
    tasa_filtracion_glomerular_reportado_cac_2020: Optional[float] = None
    estadio_erc_reportado_cac_2020: Optional[str] = None

    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None
