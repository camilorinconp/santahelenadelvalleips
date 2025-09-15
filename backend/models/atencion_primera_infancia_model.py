# =============================================================================
# Modelo Consolidado Atención Primera Infancia - Arquitectura Vertical
# Resolución 3280 de 2018 - Versión básica unificada
# Fecha: 15 septiembre 2025
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# =============================================================================
# ENUMS BÁSICOS CONSOLIDADOS
# =============================================================================

class EstadoNutricional(str, Enum):
    """Estado nutricional básico"""
    NORMAL = "NORMAL"
    DESNUTRICION_AGUDA = "DESNUTRICION_AGUDA"
    DESNUTRICION_CRONICA = "DESNUTRICION_CRONICA"
    SOBREPESO = "SOBREPESO"
    OBESIDAD = "OBESIDAD"

class ResultadoTamizaje(str, Enum):
    """Resultado de tamizajes básicos"""
    NORMAL = "NORMAL"
    ALTERADO = "ALTERADO"
    NO_REALIZADO = "NO_REALIZADO"

# =============================================================================
# MODELO PRINCIPAL CONSOLIDADO
# =============================================================================

class AtencionPrimeraInfancia(BaseModel):
    """
    Modelo consolidado para Atención Primera Infancia.
    
    Versión básica que incluye:
    - Datos antropométricos esenciales
    - EAD-3 básico (sin complejidades)
    - ASQ-3 simplificado
    - Esquema vacunación básico
    - Tamizajes esenciales
    """
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )
    
    # Identificación
    id: Optional[UUID] = None
    paciente_id: UUID = Field(..., description="ID del paciente menor de 6 años")
    medico_id: Optional[UUID] = Field(None, description="ID del médico que realiza la atención")
    atencion_id: Optional[UUID] = Field(None, description="ID de la atención genérica (polimorfismo)")
    
    # Metadatos de atención
    fecha_atencion: date = Field(default_factory=date.today, description="Fecha de la atención")
    entorno: Optional[str] = Field(None, max_length=100, description="Entorno donde se realiza la atención")
    codigo_atencion_primera_infancia_unico: Optional[str] = Field(
        None, 
        max_length=100, 
        description="Código único de identificación de la atención"
    )
    
    # =============================================================================
    # ANTROPOMETRÍA BÁSICA
    # =============================================================================
    
    peso_kg: Optional[float] = Field(
        None, 
        ge=0, 
        le=50, 
        description="Peso en kilogramos (0-50 kg)"
    )
    talla_cm: Optional[float] = Field(
        None, 
        ge=30, 
        le=150, 
        description="Talla en centímetros (30-150 cm)"
    )
    perimetro_cefalico_cm: Optional[float] = Field(
        None, 
        ge=25, 
        le=65, 
        description="Perímetro cefálico en centímetros (25-65 cm)"
    )
    
    # Estado nutricional
    estado_nutricional: Optional[EstadoNutricional] = Field(
        None, 
        description="Estado nutricional según curvas OMS"
    )
    
    # =============================================================================
    # DESARROLLO BÁSICO - EAD-3 SIMPLIFICADO
    # =============================================================================
    
    ead3_aplicada: Optional[bool] = Field(None, description="¿Se aplicó la Escala Abreviada de Desarrollo?")
    
    # Puntajes EAD-3 por área (0-100)
    ead3_motricidad_gruesa_puntaje: Optional[int] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Puntaje motricidad gruesa EAD-3 (0-100)"
    )
    ead3_motricidad_fina_puntaje: Optional[int] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Puntaje motricidad fina EAD-3 (0-100)"
    )
    ead3_audicion_lenguaje_puntaje: Optional[int] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Puntaje audición y lenguaje EAD-3 (0-100)"
    )
    ead3_personal_social_puntaje: Optional[int] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Puntaje personal-social EAD-3 (0-100)"
    )
    
    # Puntaje total (calculado automáticamente)
    ead3_puntaje_total: Optional[int] = Field(
        None, 
        description="Puntaje total EAD-3 (suma de las 4 áreas)"
    )
    fecha_aplicacion_ead3: Optional[date] = Field(
        None, 
        description="Fecha de aplicación de EAD-3"
    )
    
    # =============================================================================
    # TAMIZAJE ASQ-3 BÁSICO
    # =============================================================================
    
    asq3_aplicado: Optional[bool] = Field(None, description="¿Se aplicó el cuestionario ASQ-3?")
    
    # Puntajes ASQ-3 por área
    asq3_comunicacion_puntaje: Optional[int] = Field(
        None, 
        description="Puntaje comunicación ASQ-3"
    )
    asq3_motor_grueso_puntaje: Optional[int] = Field(
        None, 
        description="Puntaje motor grueso ASQ-3"
    )
    asq3_motor_fino_puntaje: Optional[int] = Field(
        None, 
        description="Puntaje motor fino ASQ-3"
    )
    asq3_resolucion_problemas_puntaje: Optional[int] = Field(
        None, 
        description="Puntaje resolución de problemas ASQ-3"
    )
    asq3_personal_social_puntaje: Optional[int] = Field(
        None, 
        description="Puntaje personal-social ASQ-3"
    )
    fecha_aplicacion_asq3: Optional[date] = Field(
        None, 
        description="Fecha de aplicación de ASQ-3"
    )
    
    # =============================================================================
    # ESQUEMA VACUNACIÓN BÁSICO
    # =============================================================================
    
    esquema_vacunacion_completo: Optional[bool] = Field(
        None, 
        description="¿Esquema de vacunación completo para la edad?"
    )
    
    # Vacunas básicas principales
    bcg_aplicada: Optional[bool] = Field(None, description="BCG aplicada")
    hepatitis_b_rn_aplicada: Optional[bool] = Field(None, description="Hepatitis B recién nacido aplicada")
    pentavalente_dosis_completas: Optional[int] = Field(None, ge=0, le=3, description="Dosis completas de pentavalente (0-3)")
    srp_aplicada: Optional[bool] = Field(None, description="SRP (Sarampión, Rubéola, Paperas) aplicada")
    
    # =============================================================================
    # TAMIZAJES BÁSICOS
    # =============================================================================
    
    # Tamizaje visual
    tamizaje_visual_realizado: Optional[bool] = Field(None, description="¿Se realizó tamizaje visual?")
    tamizaje_visual_resultado: Optional[ResultadoTamizaje] = Field(
        None, 
        description="Resultado del tamizaje visual"
    )
    
    # Tamizaje auditivo
    tamizaje_auditivo_realizado: Optional[bool] = Field(None, description="¿Se realizó tamizaje auditivo?")
    tamizaje_auditivo_resultado: Optional[ResultadoTamizaje] = Field(
        None, 
        description="Resultado del tamizaje auditivo"
    )
    
    # =============================================================================
    # SALUD ORAL BÁSICA
    # =============================================================================
    
    salud_oral_estado: Optional[str] = Field(
        None, 
        max_length=50, 
        description="Estado general de salud oral"
    )
    salud_oral_observaciones: Optional[str] = Field(
        None, 
        description="Observaciones específicas de salud oral"
    )
    
    # =============================================================================
    # OBSERVACIONES Y SEGUIMIENTO
    # =============================================================================
    
    observaciones_profesional_primera_infancia: Optional[str] = Field(
        None, 
        description="Observaciones del profesional de salud"
    )
    recomendaciones_generales: Optional[str] = Field(
        None, 
        description="Recomendaciones generales para cuidadores"
    )
    
    # =============================================================================
    # METADATOS
    # =============================================================================
    
    creado_en: Optional[datetime] = Field(
        default_factory=datetime.now, 
        description="Fecha y hora de creación del registro"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now, 
        description="Fecha y hora de última actualización"
    )

# =============================================================================
# MODELOS AUXILIARES PARA API
# =============================================================================

class AtencionPrimeraInfanciaCrear(BaseModel):
    """Modelo para crear nueva atención Primera Infancia"""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )
    
    # Campos requeridos
    paciente_id: UUID
    fecha_atencion: date = Field(default_factory=date.today)
    codigo_atencion_primera_infancia_unico: str = Field(max_length=100)
    
    # Campos opcionales básicos
    medico_id: Optional[UUID] = None
    entorno: Optional[str] = Field(None, max_length=100)
    peso_kg: Optional[float] = Field(None, ge=0, le=50)
    talla_cm: Optional[float] = Field(None, ge=30, le=150)
    perimetro_cefalico_cm: Optional[float] = Field(None, ge=25, le=65)
    estado_nutricional: Optional[EstadoNutricional] = None
    observaciones_profesional_primera_infancia: Optional[str] = None

class AtencionPrimeraInfanciaActualizar(BaseModel):
    """Modelo para actualizar atención Primera Infancia"""
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )
    
    # Todos los campos opcionales para actualización
    medico_id: Optional[UUID] = None
    fecha_atencion: Optional[date] = None
    entorno: Optional[str] = Field(None, max_length=100)
    peso_kg: Optional[float] = Field(None, ge=0, le=50)
    talla_cm: Optional[float] = Field(None, ge=30, le=150)
    perimetro_cefalico_cm: Optional[float] = Field(None, ge=25, le=65)
    estado_nutricional: Optional[EstadoNutricional] = None
    
    # EAD-3
    ead3_aplicada: Optional[bool] = None
    ead3_motricidad_gruesa_puntaje: Optional[int] = Field(None, ge=0, le=100)
    ead3_motricidad_fina_puntaje: Optional[int] = Field(None, ge=0, le=100)
    ead3_audicion_lenguaje_puntaje: Optional[int] = Field(None, ge=0, le=100)
    ead3_personal_social_puntaje: Optional[int] = Field(None, ge=0, le=100)
    fecha_aplicacion_ead3: Optional[date] = None
    
    # ASQ-3
    asq3_aplicado: Optional[bool] = None
    asq3_comunicacion_puntaje: Optional[int] = None
    asq3_motor_grueso_puntaje: Optional[int] = None
    asq3_motor_fino_puntaje: Optional[int] = None
    asq3_resolucion_problemas_puntaje: Optional[int] = None
    asq3_personal_social_puntaje: Optional[int] = None
    fecha_aplicacion_asq3: Optional[date] = None
    
    # Vacunación
    esquema_vacunacion_completo: Optional[bool] = None
    bcg_aplicada: Optional[bool] = None
    hepatitis_b_rn_aplicada: Optional[bool] = None
    pentavalente_dosis_completas: Optional[int] = Field(None, ge=0, le=3)
    srp_aplicada: Optional[bool] = None
    
    # Tamizajes
    tamizaje_visual_realizado: Optional[bool] = None
    tamizaje_visual_resultado: Optional[ResultadoTamizaje] = None
    tamizaje_auditivo_realizado: Optional[bool] = None
    tamizaje_auditivo_resultado: Optional[ResultadoTamizaje] = None
    
    # Salud oral
    salud_oral_estado: Optional[str] = Field(None, max_length=50)
    salud_oral_observaciones: Optional[str] = None
    
    # Observaciones
    observaciones_profesional_primera_infancia: Optional[str] = None
    recomendaciones_generales: Optional[str] = None

class AtencionPrimeraInfanciaResponse(AtencionPrimeraInfancia):
    """Modelo de respuesta API con campos adicionales calculados"""
    
    # Campos calculados básicos
    desarrollo_apropiado_edad: Optional[bool] = Field(
        None, 
        description="¿El desarrollo es apropiado para la edad cronológica?"
    )
    porcentaje_esquema_vacunacion: Optional[float] = Field(
        None, 
        description="Porcentaje de completitud del esquema de vacunación"
    )
    proxima_consulta_recomendada_dias: Optional[int] = Field(
        None, 
        description="Días recomendados hasta próxima consulta"
    )

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def calcular_ead3_puntaje_total(
    motricidad_gruesa: Optional[int],
    motricidad_fina: Optional[int], 
    audicion_lenguaje: Optional[int],
    personal_social: Optional[int]
) -> Optional[int]:
    """Calcular puntaje total EAD-3"""
    puntajes = [motricidad_gruesa, motricidad_fina, audicion_lenguaje, personal_social]
    puntajes_validos = [p for p in puntajes if p is not None]
    
    if len(puntajes_validos) == 4:
        return sum(puntajes_validos)
    return None

def evaluar_desarrollo_apropiado_edad(ead3_total: Optional[int], asq3_aplicado: bool) -> Optional[bool]:
    """Evaluar si desarrollo es apropiado para edad (lógica básica)"""
    if ead3_total is not None:
        # Criterio básico: puntaje total > 200 indica desarrollo apropiado
        return ead3_total > 200
    return None  # No hay suficiente información