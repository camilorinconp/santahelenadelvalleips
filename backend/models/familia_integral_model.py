# =============================================================================
# Modelo de Familia Integral de Salud Pública - Arquitectura Transversal 
# Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID

# =============================================================================
# ENUMS - Alineados con la tabla de Supabase
# =============================================================================

class TipoEstructuraFamiliarIntegral(str, Enum):
    """
    Enum para tipos de estructura familiar según lineamientos de salud familiar.
    Alineado con la tabla familia_integral_salud_publica en Supabase.
    """
    NUCLEAR_BIPARENTAL = "NUCLEAR_BIPARENTAL"
    NUCLEAR_MONOPARENTAL = "NUCLEAR_MONOPARENTAL"
    EXTENSA_MULTIGENERACIONAL = "EXTENSA_MULTIGENERACIONAL"
    COMPUESTA_ALLEGADOS = "COMPUESTA_ALLEGADOS"
    UNIPERSONAL_INDIVIDUAL = "UNIPERSONAL_INDIVIDUAL"


class CicloVitalFamiliar(str, Enum):
    """
    Enum para el ciclo vital familiar evolutivo.
    Alineado con la tabla familia_integral_salud_publica en Supabase.
    """
    FORMACION_PAREJA = "FORMACION_PAREJA"
    EXPANSION_HIJOS_PEQUENOS = "EXPANSION_HIJOS_PEQUENOS"
    CONSOLIDACION_HIJOS_ESCOLARES = "CONSOLIDACION_HIJOS_ESCOLARES"
    APERTURA_HIJOS_ADOLESCENTES = "APERTURA_HIJOS_ADOLESCENTES"
    PLATAFORMA_LANZAMIENTO_JOVENES = "PLATAFORMA_LANZAMIENTO_JOVENES"
    NIDO_VACIO_PAREJA_MADURA = "NIDO_VACIO_PAREJA_MADURA"
    DISOLUCACION_VIUDEZ_SEPARACION = "DISOLUCACION_VIUDEZ_SEPARACION"


class NivelSocioeconomicoFamiliar(str, Enum):
    """
    Enum para el nivel socioeconómico familiar basado en estratificación colombiana.
    """
    ESTRATO_1_BAJO_BAJO = "ESTRATO_1_BAJO_BAJO"
    ESTRATO_2_BAJO = "ESTRATO_2_BAJO"
    ESTRATO_3_MEDIO_BAJO = "ESTRATO_3_MEDIO_BAJO"
    ESTRATO_4_MEDIO = "ESTRATO_4_MEDIO"
    ESTRATO_5_MEDIO_ALTO = "ESTRATO_5_MEDIO_ALTO"
    ESTRATO_6_ALTO = "ESTRATO_6_ALTO"

# =============================================================================
# MODELOS PRINCIPALES - Alineados con tabla Supabase
# =============================================================================

class ModeloFamiliaIntegralSaludPublicaCompleto(BaseModel):
    """
    Modelo completo para familia integral de salud pública.
    Corresponde exactamente con la tabla familia_integral_salud_publica en Supabase.
    
    Artículo 1364-1370 Resolución 3280: La familia como sujeto de atención integral.
    """
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True
    )

    # Campos principales (requeridos)
    codigo_identificacion_familia_unico: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Código único identificador de la familia (ej: FAM-001-2025)"
    )
    
    tipo_estructura_familiar: TipoEstructuraFamiliarIntegral = Field(
        ...,
        description="Tipo de estructura familiar según clasificación"
    )
    
    ciclo_vital_familiar: CicloVitalFamiliar = Field(
        ...,
        description="Etapa del ciclo vital familiar actual"
    )
    
    nombre_apellidos_jefe_hogar: str = Field(
        ..., 
        min_length=2, 
        max_length=200,
        description="Nombre completo del jefe de hogar"
    )
    
    numero_integrantes_familia: int = Field(
        ..., 
        ge=1, 
        le=20,
        description="Número total de integrantes de la familia"
    )
    
    direccion_residencia_completa: str = Field(
        ..., 
        min_length=5, 
        max_length=300,
        description="Dirección completa de residencia familiar"
    )

    # Campos opcionales
    nivel_socioeconomico: Optional[NivelSocioeconomicoFamiliar] = Field(
        None,
        description="Nivel socioeconómico según estratificación"
    )
    
    telefono_contacto_principal: Optional[str] = Field(
        None, 
        max_length=15,
        description="Teléfono principal de contacto familiar"
    )
    
    correo_electronico_familia: Optional[str] = Field(
        None, 
        max_length=100,
        description="Correo electrónico de contacto familiar"
    )
    
    medico_familiar_asignado_id: Optional[UUID] = Field(
        None,
        description="ID del médico familiar asignado"
    )
    
    entorno_salud_publica_id: Optional[UUID] = Field(
        None,
        description="ID del entorno de salud pública asociado"
    )

    # Campos JSONB para datos estructurados
    caracteristicas_vivienda_jsonb: Optional[Dict[str, Any]] = Field(
        None,
        description="Características físicas y condiciones de la vivienda"
    )
    
    condiciones_saneamiento_basico: Optional[Dict[str, Any]] = Field(
        None,
        description="Acceso a servicios públicos y saneamiento básico"
    )
    
    acceso_servicios_salud_jsonb: Optional[Dict[str, Any]] = Field(
        None,
        description="Información sobre acceso a servicios de salud"
    )
    
    antecedentes_patologicos_familiares: Optional[Dict[str, Any]] = Field(
        None,
        description="Antecedentes patológicos relevantes en la familia"
    )
    
    factores_riesgo_identificados: Optional[Dict[str, Any]] = Field(
        None,
        description="Factores de riesgo identificados en el entorno familiar"
    )
    
    fortalezas_recursos_familiares: Optional[Dict[str, Any]] = Field(
        None,
        description="Fortalezas y recursos disponibles en la familia"
    )
    
    dinamica_relacional_familiar: Optional[Dict[str, Any]] = Field(
        None,
        description="Información sobre dinámicas relacionales familiares"
    )
    
    apoyo_social_redes_disponibles: Optional[Dict[str, Any]] = Field(
        None,
        description="Redes de apoyo social disponibles para la familia"
    )
    
    plan_atencion_integral_familiar: Optional[Dict[str, Any]] = Field(
        None,
        description="Plan de atención integral familiar establecido"
    )
    
    intervenciones_realizadas_familia: Optional[Dict[str, Any]] = Field(
        None,
        description="Registro de intervenciones realizadas en la familia"
    )
    
    seguimiento_indicadores_familiares: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores de seguimiento y evaluación familiar"
    )

    # Campos de fechas importantes
    fecha_primera_caracterizacion: Optional[datetime] = Field(
        None,
        description="Fecha de la primera caracterización familiar"
    )
    
    fecha_ultima_actualizacion_plan: Optional[datetime] = Field(
        None,
        description="Fecha de la última actualización del plan familiar"
    )
    
    proxima_visita_programada: Optional[datetime] = Field(
        None,
        description="Fecha programada para la próxima visita familiar"
    )

    # Estado y observaciones
    estado_seguimiento_familia: Optional[str] = Field(
        "ACTIVO",
        max_length=50,
        description="Estado actual del seguimiento familiar"
    )
    
    observaciones_adicionales_familia: Optional[str] = Field(
        None,
        max_length=2000,
        description="Observaciones adicionales sobre la familia"
    )

    # Metadatos del sistema (solo lectura en respuestas)
    id: Optional[UUID] = Field(None, description="ID único del registro")
    creado_en: Optional[datetime] = Field(None, description="Fecha de creación del registro")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    creado_por: Optional[UUID] = Field(None, description="ID del usuario que creó el registro")
    actualizado_por: Optional[UUID] = Field(None, description="ID del usuario que actualizó el registro")



# =============================================================================
# MODELOS DE ENTRADA Y SALIDA
# =============================================================================

class ModeloFamiliaIntegralSaludPublicaCrear(BaseModel):
    """Modelo para crear una nueva familia integral - solo campos requeridos y opcionales de entrada"""
    
    codigo_identificacion_familia_unico: str = Field(..., min_length=3, max_length=50)
    tipo_estructura_familiar: TipoEstructuraFamiliarIntegral
    ciclo_vital_familiar: CicloVitalFamiliar
    nombre_apellidos_jefe_hogar: str = Field(..., min_length=2, max_length=200)
    numero_integrantes_familia: int = Field(..., ge=1, le=20)
    direccion_residencia_completa: str = Field(..., min_length=5, max_length=300)
    
    # Campos opcionales para creación
    nivel_socioeconomico: Optional[NivelSocioeconomicoFamiliar] = None
    telefono_contacto_principal: Optional[str] = None
    correo_electronico_familia: Optional[str] = None
    medico_familiar_asignado_id: Optional[UUID] = None
    entorno_salud_publica_id: Optional[UUID] = None
    caracteristicas_vivienda_jsonb: Optional[Dict[str, Any]] = None
    condiciones_saneamiento_basico: Optional[Dict[str, Any]] = None
    acceso_servicios_salud_jsonb: Optional[Dict[str, Any]] = None
    antecedentes_patologicos_familiares: Optional[Dict[str, Any]] = None
    factores_riesgo_identificados: Optional[Dict[str, Any]] = None
    fortalezas_recursos_familiares: Optional[Dict[str, Any]] = None
    dinamica_relacional_familiar: Optional[Dict[str, Any]] = None
    apoyo_social_redes_disponibles: Optional[Dict[str, Any]] = None
    plan_atencion_integral_familiar: Optional[Dict[str, Any]] = None
    fecha_primera_caracterizacion: Optional[datetime] = None
    estado_seguimiento_familia: Optional[str] = "ACTIVO"
    observaciones_adicionales_familia: Optional[str] = None


class ModeloFamiliaIntegralSaludPublicaRespuesta(ModeloFamiliaIntegralSaludPublicaCompleto):
    """Modelo de respuesta - incluye todos los campos incluyendo metadatos del sistema"""
    id: UUID = Field(..., description="ID único del registro")
    creado_en: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")


class ModeloFamiliaIntegralSaludPublicaActualizar(BaseModel):
    """Modelo para actualizar familia integral - todos los campos opcionales"""
    
    tipo_estructura_familiar: Optional[TipoEstructuraFamiliarIntegral] = None
    ciclo_vital_familiar: Optional[CicloVitalFamiliar] = None
    nombre_apellidos_jefe_hogar: Optional[str] = None
    numero_integrantes_familia: Optional[int] = None
    direccion_residencia_completa: Optional[str] = None
    nivel_socioeconomico: Optional[NivelSocioeconomicoFamiliar] = None
    telefono_contacto_principal: Optional[str] = None
    correo_electronico_familia: Optional[str] = None
    medico_familiar_asignado_id: Optional[UUID] = None
    entorno_salud_publica_id: Optional[UUID] = None
    caracteristicas_vivienda_jsonb: Optional[Dict[str, Any]] = None
    condiciones_saneamiento_basico: Optional[Dict[str, Any]] = None
    acceso_servicios_salud_jsonb: Optional[Dict[str, Any]] = None
    antecedentes_patologicos_familiares: Optional[Dict[str, Any]] = None
    factores_riesgo_identificados: Optional[Dict[str, Any]] = None
    fortalezas_recursos_familiares: Optional[Dict[str, Any]] = None
    dinamica_relacional_familiar: Optional[Dict[str, Any]] = None
    apoyo_social_redes_disponibles: Optional[Dict[str, Any]] = None
    plan_atencion_integral_familiar: Optional[Dict[str, Any]] = None
    intervenciones_realizadas_familia: Optional[Dict[str, Any]] = None
    seguimiento_indicadores_familiares: Optional[Dict[str, Any]] = None
    fecha_ultima_actualizacion_plan: Optional[datetime] = None
    proxima_visita_programada: Optional[datetime] = None
    estado_seguimiento_familia: Optional[str] = None
    observaciones_adicionales_familia: Optional[str] = None