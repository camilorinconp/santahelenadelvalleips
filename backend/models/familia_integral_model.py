# =============================================================================
# Modelo de Familia Integral CORREGIDO - Coincide exactamente con BD
# Basado en migración: 20250913000000_create_transversal_models_consolidated.sql
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID
from decimal import Decimal

# =============================================================================
# ENUMS - Exactamente como están en la migración de BD
# =============================================================================

class TipoEstructuraFamiliarIntegral(str, Enum):
    """Enum exacto según migración BD líneas 91-102"""
    NUCLEAR_BIPARENTAL = "NUCLEAR_BIPARENTAL"
    NUCLEAR_MONOPARENTAL_MATERNA = "NUCLEAR_MONOPARENTAL_MATERNA"
    NUCLEAR_MONOPARENTAL_PATERNA = "NUCLEAR_MONOPARENTAL_PATERNA"
    EXTENSA_BIPARENTAL = "EXTENSA_BIPARENTAL"
    EXTENSA_MONOPARENTAL = "EXTENSA_MONOPARENTAL"
    COMPUESTA_MIXTA = "COMPUESTA_MIXTA"
    UNIPERSONAL_ADULTO = "UNIPERSONAL_ADULTO"
    RECONSTITUIDA_NUEVA_UNION = "RECONSTITUIDA_NUEVA_UNION"
    HOMOPARENTAL_BIPARENTAL = "HOMOPARENTAL_BIPARENTAL"
    HOMOPARENTAL_MONOPARENTAL = "HOMOPARENTAL_MONOPARENTAL"

class CicloVitalFamiliar(str, Enum):
    """Enum exacto según migración BD líneas 105-113"""
    FORMACION_PAREJA_SIN_HIJOS = "FORMACION_PAREJA_SIN_HIJOS"
    EXPANSION_HIJOS_PEQUENOS = "EXPANSION_HIJOS_PEQUENOS"
    CONSOLIDACION_HIJOS_ESCOLARES = "CONSOLIDACION_HIJOS_ESCOLARES"
    APERTURA_HIJOS_ADOLESCENTES = "APERTURA_HIJOS_ADOLESCENTES"
    CONTRACCION_INDEPENDENCIA_HIJOS = "CONTRACCION_INDEPENDENCIA_HIJOS"
    DISOLUCCION_NIDO_VACIO = "DISOLUCCION_NIDO_VACIO"
    POST_PARENTAL_ADULTOS_MAYORES = "POST_PARENTAL_ADULTOS_MAYORES"

class NivelSocioeconomicoFamiliar(str, Enum):
    """Enum exacto según migración BD líneas 116-123"""
    ESTRATO_1_BAJO_BAJO = "ESTRATO_1_BAJO_BAJO"
    ESTRATO_2_BAJO = "ESTRATO_2_BAJO"
    ESTRATO_3_MEDIO_BAJO = "ESTRATO_3_MEDIO_BAJO"
    ESTRATO_4_MEDIO = "ESTRATO_4_MEDIO"
    ESTRATO_5_MEDIO_ALTO = "ESTRATO_5_MEDIO_ALTO"
    ESTRATO_6_ALTO = "ESTRATO_6_ALTO"

# =============================================================================
# MODELO COMPLETO - Todos los campos según migración BD líneas 126-193
# =============================================================================

class ModeloFamiliaIntegralCompleto(BaseModel):
    """
    Modelo que coincide EXACTAMENTE con la tabla familia_integral_salud_publica
    Basado en migración líneas 126-193
    """
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True
    )

    # Campos principales (línea 127-131)
    id: Optional[UUID] = Field(None, description="ID único del registro")
    codigo_identificacion_familiar_unico: str = Field(
        ..., 
        description="Código único identificador de la familia - LÍNEA 128"
    )
    tipo_estructura_familiar: TipoEstructuraFamiliarIntegral = Field(
        ...,
        description="Tipo de estructura familiar - LÍNEA 129"
    )
    ciclo_vital_familiar: Optional[CicloVitalFamiliar] = Field(
        None,
        description="Ciclo vital familiar - LÍNEA 130"
    )
    nivel_socioeconomico_familiar: Optional[NivelSocioeconomicoFamiliar] = Field(
        None,
        description="Nivel socioeconómico - LÍNEA 131"
    )
    
    # Composición familiar (líneas 133-138)
    numero_total_integrantes: int = Field(
        ..., 
        description="Número total de integrantes - LÍNEA 134"
    )
    numero_menores_18_anos: Optional[int] = Field(
        None, 
        description="Número de menores de 18 años - LÍNEA 135"
    )
    numero_adultos_mayores_60_anos: Optional[int] = Field(
        None,
        description="Número de adultos mayores de 60 años - LÍNEA 136"
    )
    numero_personas_discapacidad: Optional[int] = Field(
        None,
        description="Número de personas con discapacidad - LÍNEA 137"
    )
    numero_mujeres_edad_fertil: Optional[int] = Field(
        None,
        description="Número de mujeres en edad fértil - LÍNEA 138"
    )
    
    # Información socioeconómica (líneas 140-145)
    ingreso_familiar_mensual_estimado: Optional[Decimal] = Field(
        None,
        description="Ingreso familiar mensual estimado - LÍNEA 141"
    )
    tipo_vivienda: Optional[str] = Field(
        None,
        description="Tipo de vivienda - LÍNEA 142"
    )
    tenencia_vivienda: Optional[str] = Field(
        None,
        description="Tenencia de vivienda - LÍNEA 143"
    )
    servicios_publicos_disponibles: Optional[Dict[str, Any]] = Field(
        None,
        description="Servicios públicos disponibles JSONB - LÍNEA 144"
    )
    acceso_tecnologias_informacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Acceso a tecnologías de información JSONB - LÍNEA 145"
    )
    
    # Evaluación funcionalidad familiar APGAR (líneas 147-150)
    puntaje_apgar_familiar_funcionamiento: Optional[int] = Field(
        None,
        description="Puntaje APGAR familiar 0-20 - LÍNEA 148"
    )
    fecha_aplicacion_apgar_familiar: Optional[datetime] = Field(
        None,
        description="Fecha aplicación APGAR familiar - LÍNEA 149"
    )
    interpretacion_apgar_familiar: Optional[str] = Field(
        None,
        description="Interpretación APGAR familiar - LÍNEA 150"
    )
    
    # Dinámicas familiares (líneas 152-156)
    patron_comunicacion_familiar: Optional[str] = Field(
        None,
        description="Patrón de comunicación familiar - LÍNEA 153"
    )
    mecanismos_resolucion_conflictos: Optional[str] = Field(
        None,
        description="Mecanismos de resolución de conflictos - LÍNEA 154"
    )
    distribucion_roles_responsabilidades: Optional[Dict[str, Any]] = Field(
        None,
        description="Distribución de roles y responsabilidades JSONB - LÍNEA 155"
    )
    tiempo_calidad_familiar_semanal: Optional[int] = Field(
        None,
        description="Tiempo de calidad familiar semanal en horas - LÍNEA 156"
    )
    
    # Red de apoyo familiar Ecomapa (líneas 158-162)
    red_apoyo_familiar_primaria: Optional[Dict[str, Any]] = Field(
        None,
        description="Red de apoyo familiar primaria JSONB - LÍNEA 159"
    )
    red_apoyo_institucional: Optional[Dict[str, Any]] = Field(
        None,
        description="Red de apoyo institucional JSONB - LÍNEA 160"
    )
    red_apoyo_comunitaria: Optional[Dict[str, Any]] = Field(
        None,
        description="Red de apoyo comunitaria JSONB - LÍNEA 161"
    )
    fortaleza_vinculos_red_apoyo: Optional[str] = Field(
        None,
        description="Fortaleza de vínculos de red de apoyo - LÍNEA 162"
    )
    
    # Antecedentes y factores de riesgo (líneas 164-168)
    antecedentes_familiares_relevantes: Optional[Dict[str, Any]] = Field(
        None,
        description="Antecedentes familiares relevantes JSONB - LÍNEA 165"
    )
    factores_riesgo_psicosocial: Optional[Dict[str, Any]] = Field(
        None,
        description="Factores de riesgo psicosocial JSONB - LÍNEA 166"
    )
    factores_protectores_identificados: Optional[Dict[str, Any]] = Field(
        None,
        description="Factores protectores identificados JSONB - LÍNEA 167"
    )
    eventos_vitales_estresantes_recientes: Optional[Dict[str, Any]] = Field(
        None,
        description="Eventos vitales estresantes recientes JSONB - LÍNEA 168"
    )
    
    # Atención en salud familiar (líneas 170-174)
    ips_asignada_familia: Optional[str] = Field(
        None,
        description="IPS asignada a la familia - LÍNEA 171"
    )
    medico_familia_asignado: Optional[UUID] = Field(
        None,
        description="Médico de familia asignado UUID - LÍNEA 172"
    )
    fecha_ultima_atencion_familiar: Optional[datetime] = Field(
        None,
        description="Fecha última atención familiar - LÍNEA 173"
    )
    plan_atencion_familiar_vigente: Optional[Dict[str, Any]] = Field(
        None,
        description="Plan de atención familiar vigente JSONB - LÍNEA 174"
    )
    
    # Participación comunitaria (líneas 176-179)
    participacion_organizaciones_comunitarias: Optional[bool] = Field(
        None,
        description="Participación en organizaciones comunitarias - LÍNEA 177"
    )
    liderazgo_comunitario_familiar: Optional[bool] = Field(
        None,
        description="Liderazgo comunitario familiar - LÍNEA 178"
    )
    actividades_promocion_salud_participacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Actividades de promoción de salud participación JSONB - LÍNEA 179"
    )
    
    # Seguimiento y monitoreo (líneas 181-186)
    fecha_caracterizacion_inicial: Optional[datetime] = Field(
        None,
        description="Fecha de caracterización inicial - LÍNEA 182"
    )
    fecha_proxima_evaluacion: Optional[datetime] = Field(
        None,
        description="Fecha próxima evaluación - LÍNEA 183"
    )
    responsable_seguimiento_familiar: Optional[UUID] = Field(
        None,
        description="Responsable del seguimiento familiar UUID - LÍNEA 184"
    )
    estado_seguimiento_familiar: Optional[str] = Field(
        None,
        description="Estado del seguimiento familiar - LÍNEA 185"
    )
    observaciones_adicionales_familia: Optional[str] = Field(
        None,
        description="Observaciones adicionales de la familia - LÍNEA 186"
    )
    
    # Auditoría (líneas 188-192)
    creado_en: Optional[datetime] = Field(
        None,
        description="Fecha de creación - LÍNEA 189"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Fecha de última actualización - LÍNEA 190"
    )
    creado_por: Optional[UUID] = Field(
        None,
        description="Usuario que creó el registro - LÍNEA 191"
    )
    actualizado_por: Optional[UUID] = Field(
        None,
        description="Usuario que actualizó el registro - LÍNEA 192"
    )

# =============================================================================
# MODELOS DE ENTRADA Y SALIDA
# =============================================================================

class ModeloFamiliaIntegralCrear(BaseModel):
    """Modelo para crear familia - solo campos requeridos según BD"""
    
    codigo_identificacion_familiar_unico: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Código único identificador de la familia"
    )
    tipo_estructura_familiar: TipoEstructuraFamiliarIntegral = Field(
        ...,
        description="Tipo de estructura familiar según clasificación"
    )
    numero_total_integrantes: int = Field(
        ..., 
        ge=1, 
        le=50,
        description="Número total de integrantes de la familia"
    )
    
    # Campos opcionales comunes
    ciclo_vital_familiar: Optional[CicloVitalFamiliar] = None
    nivel_socioeconomico_familiar: Optional[NivelSocioeconomicoFamiliar] = None

class ModeloFamiliaIntegralRespuesta(ModeloFamiliaIntegralCompleto):
    """Modelo de respuesta - incluye todos los campos con ID y auditoría requeridos"""
    
    id: UUID = Field(..., description="ID único del registro")
    creado_en: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

class ModeloFamiliaIntegralActualizar(BaseModel):
    """Modelo para actualizar familia - todos los campos opcionales"""
    
    tipo_estructura_familiar: Optional[TipoEstructuraFamiliarIntegral] = None
    ciclo_vital_familiar: Optional[CicloVitalFamiliar] = None
    numero_total_integrantes: Optional[int] = Field(None, ge=1, le=50)
    nivel_socioeconomico_familiar: Optional[NivelSocioeconomicoFamiliar] = None
    # ... más campos opcionales según necesidad