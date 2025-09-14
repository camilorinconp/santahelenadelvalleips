# =============================================================================
# Modelo de Atención Integral Primera Infancia - Arquitectura Transversal
# Resolución 3280 de 2018 - RPMS (Ruta de Promoción y Mantenimiento de Salud)
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# =============================================================================
# ENUMS - Específicos de Primera Infancia
# =============================================================================

class EstadoNutricionalPrimeraInfancia(str, Enum):
    """Estado nutricional según curvas OMS para primera infancia"""
    PESO_ADECUADO_EDAD = "PESO_ADECUADO_EDAD"
    PESO_BAJO_EDAD = "PESO_BAJO_EDAD"  
    PESO_MUY_BAJO_EDAD = "PESO_MUY_BAJO_EDAD"
    SOBREPESO_OBESIDAD = "SOBREPESO_OBESIDAD"
    RIESGO_DESNUTRICION = "RIESGO_DESNUTRICION"
    DESNUTRICION_AGUDA = "DESNUTRICION_AGUDA"

class ResultadoTamizajeDesarrollo(str, Enum):
    """Resultado de tamizaje de desarrollo EAD-3/ASQ-3"""
    DESARROLLO_ACORDE_EDAD = "DESARROLLO_ACORDE_EDAD"
    ALERTA_SEGUIMIENTO_REQUERIDO = "ALERTA_SEGUIMIENTO_REQUERIDO"
    RETRASO_DERIVACION_ESPECIALIZADA = "RETRASO_DERIVACION_ESPECIALIZADA"
    EVALUACION_INCOMPLETA = "EVALUACION_INCOMPLETA"

class EstadoEsquemaVacunacion(str, Enum):
    """Estado del esquema de vacunación nacional"""
    COMPLETO_AL_DIA = "COMPLETO_AL_DIA"
    INCOMPLETO_RECUPERABLE = "INCOMPLETO_RECUPERABLE"
    ATRASADO_INTERVENCION_REQUERIDA = "ATRASADO_INTERVENCION_REQUERIDA"
    CONTRAINDICACION_MEDICA_TEMPORAL = "CONTRAINDICACION_MEDICA_TEMPORAL"

# =============================================================================
# MODELO PRINCIPAL REFACTORIZADO
# =============================================================================

class AtencionIntegralPrimeraInfanciaTransversal(BaseModel):
    """
    Atención integral de primera infancia con arquitectura transversal.
    
    Integra:
    - Referencia a entornos de salud pública
    - Vinculación con núcleo familiar 
    - Coordinación con atención integral transversal
    - Nomenclatura descriptiva para IA/RAG
    """
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        str_strip_whitespace=True
    )
    
    # =============================================================================
    # IDENTIFICACIÓN Y REFERENCIAS TRANSVERSALES
    # =============================================================================
    
    id: Optional[UUID] = None
    codigo_atencion_primera_infancia_unico: str = Field(
        ...,
        description="Código único identificador de la atención de primera infancia"
    )
    
    # Referencias principales
    sujeto_atencion_menor_id: UUID = Field(
        ...,
        description="ID del menor (paciente) sujeto de atención"
    )
    profesional_responsable_atencion_id: Optional[UUID] = Field(
        None,
        description="ID del profesional responsable de la atención"
    )
    
    # Referencias transversales (NUEVAS)
    entorno_desarrollo_asociado_id: Optional[UUID] = Field(
        None,
        description="ID del entorno de salud pública donde se desarrolla el menor"
    )
    familia_integral_pertenencia_id: Optional[UUID] = Field(
        None, 
        description="ID de la familia integral a la que pertenece el menor"
    )
    atencion_integral_coordinada_id: Optional[UUID] = Field(
        None,
        description="ID de la atención integral transversal que coordina este cuidado"
    )
    
    atencion_general_vinculo_id: Optional[UUID] = Field(
        None,
        description="Vínculo con la atención general (tabla polimórfica principal)"
    )

    
    # =============================================================================
    # DATOS TEMPORALES Y CONTEXTUALES  
    # =============================================================================
    
    fecha_atencion_primera_infancia: date = Field(
        ...,
        description="Fecha específica de la atención de primera infancia"
    )
    
    # =============================================================================
    # ANTROPOMETRÍA Y ESTADO NUTRICIONAL (REFINADO)
    # =============================================================================
    
    peso_actual_kilogramos: Optional[float] = Field(
        None,
        ge=0.5, le=50.0,
        description="Peso actual del menor en kilogramos"
    )
    talla_actual_centimetros: Optional[float] = Field(
        None,
        ge=30.0, le=130.0, 
        description="Talla actual del menor en centímetros"
    )
    perimetro_cefalico_centimetros: Optional[float] = Field(
        None,
        ge=25.0, le=60.0,
        description="Perímetro cefálico actual en centímetros"
    )
    
    estado_nutricional_evaluacion: Optional[EstadoNutricionalPrimeraInfancia] = Field(
        None,
        description="Estado nutricional según curvas OMS"
    )
    
    practicas_alimentarias_evaluacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Evaluación detallada de prácticas alimentarias JSONB"
    )
    
    suplementacion_micronutrientes_registro: Optional[Dict[str, Any]] = Field(
        None,
        description="Registro de suplementación (hierro, vitamina A, micronutrientes) JSONB"
    )
    
    # =============================================================================
    # DESARROLLO Y TAMIZAJES ESPECIALIZADOS
    # =============================================================================
    
    tamizaje_desarrollo_integral_resultado: Optional[ResultadoTamizajeDesarrollo] = Field(
        None,
        description="Resultado del tamizaje de desarrollo (EAD-3/ASQ-3)"
    )
    
    desarrollo_fisico_motor_evaluacion: Optional[str] = Field(
        None,
        description="Evaluación narrativa del desarrollo físico-motor"
    )
    desarrollo_socioemocional_evaluacion: Optional[str] = Field(
        None,
        description="Evaluación narrativa del desarrollo socioemocional"
    )
    desarrollo_cognitivo_lenguaje_evaluacion: Optional[str] = Field(
        None,
        description="Evaluación narrativa del desarrollo cognitivo y lenguaje"
    )
    
    # =============================================================================
    # SALUD ESPECÍFICA POR SISTEMAS
    # =============================================================================
    
    salud_visual_tamizaje_detallado: Optional[Dict[str, Any]] = Field(
        None,
        description="Tamizaje visual completo (Hirschberg, cubrir-descubrir) JSONB"
    )
    
    salud_auditiva_comunicativa_tamizaje: Optional[Dict[str, Any]] = Field(
        None,
        description="Tamizaje auditivo y evaluación comunicativa JSONB"
    )
    
    salud_bucal_evaluacion_integral: Optional[Dict[str, Any]] = Field(
        None,
        description="Evaluación integral de salud oral (higiene, caries, maloclusiones) JSONB"
    )
    
    salud_mental_bienestar_psicosocial: Optional[str] = Field(
        None,
        description="Evaluación de salud mental y bienestar psicosocial"
    )
    
    # =============================================================================
    # INMUNIZACIONES Y PREVENCIÓN
    # =============================================================================
    
    esquema_vacunacion_estado_actual: Optional[EstadoEsquemaVacunacion] = Field(
        None,
        description="Estado actual del esquema de vacunación nacional"
    )
    
    vacunas_aplicadas_registro: Optional[Dict[str, Any]] = Field(
        None,
        description="Registro detallado de vacunas aplicadas con fechas JSONB"
    )
    
    vacunas_pendientes_programacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Vacunas pendientes con programación de fechas JSONB" 
    )
    
    desparasitacion_profilaxis_registro: Optional[Dict[str, Any]] = Field(
        None,
        description="Registro de desparasitación y otras profilaxis JSONB"
    )
    
    # =============================================================================
    # INTERVENCIONES Y SEGUIMIENTO TRANSVERSAL
    # =============================================================================
    
    intervenciones_educativas_realizadas: Optional[Dict[str, Any]] = Field(
        None,
        description="Registro de intervenciones educativas a familia/cuidadores JSONB"
    )
    
    coordinacion_intersectorial_realizada: Optional[Dict[str, Any]] = Field(
        None,
        description="Coordinación con otros sectores (educación, protección social) JSONB"
    )
    
    plan_seguimiento_longitudinal: Optional[Dict[str, Any]] = Field(
        None,
        description="Plan detallado de seguimiento longitudinal del desarrollo JSONB"
    )
    
    observaciones_profesional_primera_infancia: Optional[str] = Field(
        None,
        description="Observaciones narrativas del profesional especializado"
    )
    
    # =============================================================================
    # METADATOS DE GESTIÓN
    # =============================================================================
    
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None


# =============================================================================
# MODELOS AUXILIARES PARA CRUD
# =============================================================================

class AtencionPrimeraInfanciaCrear(BaseModel):
    """Modelo para crear nueva atención de primera infancia"""
    codigo_atencion_primera_infancia_unico: str
    sujeto_atencion_menor_id: UUID
    fecha_atencion_primera_infancia: date
    profesional_responsable_atencion_id: Optional[UUID] = None
    entorno_desarrollo_asociado_id: Optional[UUID] = None
    familia_integral_pertenencia_id: Optional[UUID] = None
    
class AtencionPrimeraInfanciaActualizar(BaseModel):
    """Modelo para actualizar atención existente"""
    peso_actual_kilogramos: Optional[float] = None
    talla_actual_centimetros: Optional[float] = None
    estado_nutricional_evaluacion: Optional[EstadoNutricionalPrimeraInfancia] = None
    tamizaje_desarrollo_integral_resultado: Optional[ResultadoTamizajeDesarrollo] = None
    esquema_vacunacion_estado_actual: Optional[EstadoEsquemaVacunacion] = None
    
class AtencionPrimeraInfanciaRespuesta(AtencionIntegralPrimeraInfanciaTransversal):
    """Modelo de respuesta con todos los campos"""
    id: UUID
    creado_en: datetime
    actualizado_en: Optional[datetime] = None


# =============================================================================
# COMPATIBILIDAD HACIA ATRÁS (DEPRECATED)
# =============================================================================

# Alias para compatibilidad con código existente
AtencionPrimeraInfancia = AtencionIntegralPrimeraInfanciaTransversal
