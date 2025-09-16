# =============================================================================
# Modelo Tamizaje Oncológico - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime
from uuid import UUID

class TamizajeOncologicoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[UUID] = None
    paciente_id: UUID = Field(description="ID del paciente")
    medico_id: Optional[UUID] = Field(None, description="ID del médico responsable")
    atencion_id: Optional[UUID] = Field(None, description="Vínculo con atención general")

    # Datos generales del tamizaje
    fecha_tamizaje: date = Field(description="Fecha de realización del tamizaje")
    resultado_tamizaje: Optional[str] = Field(None, description="Resultado general: Negativo, Positivo, Anormal, Pendiente")
    fecha_proximo_tamizaje: Optional[date] = Field(None, description="Fecha programada para próximo tamizaje")
    
    # Observaciones y seguimiento
    observaciones: Optional[str] = Field(None, description="Observaciones generales del profesional")
    recomendaciones: Optional[str] = Field(None, description="Recomendaciones específicas para el paciente")
    
    # Control de seguimiento
    fecha_proximo_control: Optional[date] = Field(None, description="Fecha para próximo control médico")
    requiere_seguimiento_especializado: Optional[bool] = Field(False, description="Si requiere derivación a especialista")
    
    # Timestamps
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TamizajeOncologicoCrear(TamizajeOncologicoBase):
    tipo_tamizaje: Literal["Cuello Uterino", "Mama", "Prostata", "Colon y Recto"] = Field(description="Tipo de tamizaje oncológico")
    
    # Campos específicos por tipo - opcionales en creación
    # Cuello Uterino
    citologia_resultado: Optional[str] = Field(None, description="Normal, ASCUS, LSIL, HSIL, etc.")
    adn_vph_resultado: Optional[str] = Field(None, description="Positivo, Negativo, No realizado")
    colposcopia_realizada: Optional[bool] = Field(False, description="Si se realizó colposcopia")
    biopsia_realizada_cuello: Optional[bool] = Field(False, description="Si se realizó biopsia de cuello")
    
    # Mama
    mamografia_resultado: Optional[str] = Field(None, description="BI-RADS 0-6")
    examen_clinico_mama_observaciones: Optional[str] = Field(None, description="Hallazgos del examen clínico")
    biopsia_realizada_mama: Optional[bool] = Field(False, description="Si se realizó biopsia de mama")
    
    # Próstata
    psa_resultado: Optional[float] = Field(None, ge=0, le=100, description="Resultado PSA en ng/mL")
    tacto_rectal_resultado: Optional[str] = Field(None, description="Normal, Anormal, No realizado")
    biopsia_realizada_prostata: Optional[bool] = Field(False, description="Si se realizó biopsia prostática")
    
    # Colon y Recto
    sangre_oculta_heces_resultado: Optional[str] = Field(None, description="Positivo, Negativo, No concluyente")
    colonoscopia_realizada: Optional[bool] = Field(False, description="Si se realizó colonoscopia")
    biopsia_realizada_colon: Optional[bool] = Field(False, description="Si se realizó biopsia colónica")

class TamizajeOncologicoActualizar(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    medico_id: Optional[UUID] = None
    resultado_tamizaje: Optional[str] = None
    fecha_proximo_tamizaje: Optional[date] = None
    observaciones: Optional[str] = None
    recomendaciones: Optional[str] = None
    fecha_proximo_control: Optional[date] = None
    requiere_seguimiento_especializado: Optional[bool] = None
    
    # Campos específicos actualizables
    citologia_resultado: Optional[str] = None
    adn_vph_resultado: Optional[str] = None
    colposcopia_realizada: Optional[bool] = None
    biopsia_realizada_cuello: Optional[bool] = None
    mamografia_resultado: Optional[str] = None
    examen_clinico_mama_observaciones: Optional[str] = None
    biopsia_realizada_mama: Optional[bool] = None
    psa_resultado: Optional[float] = Field(None, ge=0, le=100)
    tacto_rectal_resultado: Optional[str] = None
    biopsia_realizada_prostata: Optional[bool] = None
    sangre_oculta_heces_resultado: Optional[str] = None
    colonoscopia_realizada: Optional[bool] = None
    biopsia_realizada_colon: Optional[bool] = None

class TamizajeOncologicoResponse(TamizajeOncologicoBase):
    tipo_tamizaje: str
    
    # Campos específicos incluidos en respuesta
    citologia_resultado: Optional[str] = None
    adn_vph_resultado: Optional[str] = None
    colposcopia_realizada: Optional[bool] = None
    biopsia_realizada_cuello: Optional[bool] = None
    mamografia_resultado: Optional[str] = None
    examen_clinico_mama_observaciones: Optional[str] = None
    biopsia_realizada_mama: Optional[bool] = None
    psa_resultado: Optional[float] = None
    tacto_rectal_resultado: Optional[str] = None
    biopsia_realizada_prostata: Optional[bool] = None
    sangre_oculta_heces_resultado: Optional[str] = None
    colonoscopia_realizada: Optional[bool] = None
    biopsia_realizada_colon: Optional[bool] = None
    
    # Campos calculados
    nivel_riesgo: Optional[str] = Field(None, description="Bajo, Moderado, Alto")
    adherencia_tamizaje: Optional[str] = Field(None, description="Buena, Regular, Mala")
    proxima_cita_recomendada_dias: Optional[int] = Field(None, description="Días para próxima cita")
    completitud_tamizaje: Optional[float] = Field(None, description="Porcentaje de completitud 0-100")

# Modelo base para compatibilidad con implementación actual
class TamizajeOncologico(TamizajeOncologicoBase):
    tipo_tamizaje: str
    citologia_resultado: Optional[str] = None
    adn_vph_resultado: Optional[str] = None
    colposcopia_realizada: Optional[bool] = None
    biopsia_realizada_cuello: Optional[bool] = None
    mamografia_resultado: Optional[str] = None
    examen_clinico_mama_observaciones: Optional[str] = None
    biopsia_realizada_mama: Optional[bool] = None
    psa_resultado: Optional[float] = None
    tacto_rectal_resultado: Optional[str] = None
    biopsia_realizada_prostata: Optional[bool] = None
    sangre_oculta_heces_resultado: Optional[str] = None
    colonoscopia_realizada: Optional[bool] = None
    biopsia_realizada_colon: Optional[bool] = None

# =============================================================================
# FUNCIONES DE UTILIDAD PARA CAMPOS CALCULADOS
# =============================================================================

def calcular_nivel_riesgo(tipo_tamizaje: str, datos_tamizaje: dict) -> str:
    """Calcular nivel de riesgo según tipo de tamizaje y resultados."""
    try:
        if tipo_tamizaje == "Cuello Uterino":
            citologia = datos_tamizaje.get("citologia_resultado", "")
            vph = datos_tamizaje.get("adn_vph_resultado", "")
            
            if "HSIL" in citologia or "ASC-H" in citologia:
                return "Alto"
            elif "LSIL" in citologia or vph == "Positivo":
                return "Moderado"
            elif citologia == "Normal" and vph == "Negativo":
                return "Bajo"
                
        elif tipo_tamizaje == "Mama":
            birads = datos_tamizaje.get("mamografia_resultado", "")
            
            if "BI-RADS 5" in birads or "BI-RADS 6" in birads:
                return "Alto"
            elif "BI-RADS 4" in birads:
                return "Moderado"
            elif "BI-RADS 1" in birads or "BI-RADS 2" in birads:
                return "Bajo"
                
        elif tipo_tamizaje == "Prostata":
            psa = datos_tamizaje.get("psa_resultado", 0) or 0
            tacto = datos_tamizaje.get("tacto_rectal_resultado", "")
            
            if psa > 10 or tacto == "Anormal":
                return "Alto"
            elif psa > 4:
                return "Moderado"
            elif psa <= 4:
                return "Bajo"
                
        elif tipo_tamizaje == "Colon y Recto":
            sangre_oculta = datos_tamizaje.get("sangre_oculta_heces_resultado", "")
            
            if sangre_oculta == "Positivo":
                return "Moderado"
            else:
                return "Bajo"
                
        return "No evaluado"
    except Exception:
        return "No evaluado"

def calcular_adherencia_tamizaje(tipo_tamizaje: str, fecha_ultimo_tamizaje: date) -> str:
    """Calcular adherencia según intervalos recomendados por tipo."""
    try:
        from datetime import date
        dias_desde_ultimo = (date.today() - fecha_ultimo_tamizaje).days
        
        intervalos_recomendados = {
            "Cuello Uterino": 365,  # 1 año
            "Mama": 730,            # 2 años
            "Prostata": 365,        # 1 año
            "Colon y Recto": 1095   # 3 años
        }
        
        intervalo = intervalos_recomendados.get(tipo_tamizaje, 365)
        
        if dias_desde_ultimo <= intervalo:
            return "Buena"
        elif dias_desde_ultimo <= intervalo * 1.5:
            return "Regular"
        else:
            return "Mala"
            
    except Exception:
        return "No evaluado"

def calcular_proxima_cita_tamizaje(tipo_tamizaje: str, nivel_riesgo: str) -> int:
    """Calcular días recomendados para próxima cita según riesgo."""
    try:
        if nivel_riesgo == "Alto":
            return 30  # 1 mes para alto riesgo
        elif nivel_riesgo == "Moderado":
            return 90  # 3 meses para riesgo moderado
        else:
            # Intervalos normales por tipo
            intervalos_normales = {
                "Cuello Uterino": 365,  # 1 año
                "Mama": 730,            # 2 años
                "Prostata": 365,        # 1 año
                "Colon y Recto": 1095   # 3 años
            }
            return intervalos_normales.get(tipo_tamizaje, 365)
    except Exception:
        return 365  # Default: 1 año

def calcular_completitud_tamizaje(tipo_tamizaje: str, datos_tamizaje: dict) -> float:
    """Calcular porcentaje de completitud según campos esperados por tipo."""
    try:
        campos_esperados = {
            "Cuello Uterino": ["citologia_resultado", "adn_vph_resultado"],
            "Mama": ["mamografia_resultado", "examen_clinico_mama_observaciones"],
            "Prostata": ["psa_resultado", "tacto_rectal_resultado"],
            "Colon y Recto": ["sangre_oculta_heces_resultado"]
        }
        
        campos_tipo = campos_esperados.get(tipo_tamizaje, [])
        if not campos_tipo:
            return 100.0
            
        campos_completados = sum(1 for campo in campos_tipo 
                               if datos_tamizaje.get(campo) is not None)
        
        return round((campos_completados / len(campos_tipo)) * 100, 1)
        
    except Exception:
        return 0.0