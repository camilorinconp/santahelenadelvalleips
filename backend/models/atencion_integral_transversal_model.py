# =============================================================================
# Modelo de Atención Integral Transversal CORREGIDO - Coincide exactamente con BD
# Basado en migración: 20250913000000_create_transversal_models_consolidated.sql
# Líneas 230-300: Tabla atencion_integral_transversal_salud
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID
from decimal import Decimal

# =============================================================================
# ENUMS - Exactamente como están en la migración BD líneas 199-227
# =============================================================================

class TipoAbordajeAtencionIntegralSalud(str, Enum):
    """Enum exacto según migración BD líneas 200-209"""
    PROMOCION_SALUD_POBLACIONAL = "PROMOCION_SALUD_POBLACIONAL"
    PREVENCION_PRIMARIA_INDIVIDUAL = "PREVENCION_PRIMARIA_INDIVIDUAL"
    PREVENCION_SECUNDARIA_TAMIZAJE = "PREVENCION_SECUNDARIA_TAMIZAJE"
    INTERVENCION_TEMPRANA_RIESGO = "INTERVENCION_TEMPRANA_RIESGO"
    MANEJO_INTEGRAL_ENFERMEDAD = "MANEJO_INTEGRAL_ENFERMEDAD"
    REHABILITACION_FUNCIONAL = "REHABILITACION_FUNCIONAL"
    CUIDADOS_PALIATIVOS_CRONICOS = "CUIDADOS_PALIATIVOS_CRONICOS"
    ATENCION_URGENCIAS_EMERGENCIAS = "ATENCION_URGENCIAS_EMERGENCIAS"

class NivelComplejidadAtencionIntegral(str, Enum):
    """Enum exacto según migración BD líneas 212-217"""
    BAJA_ATENCION_PRIMARIA = "BAJA_ATENCION_PRIMARIA"
    MEDIA_ATENCION_ESPECIALIZADA = "MEDIA_ATENCION_ESPECIALIZADA"
    ALTA_ATENCION_SUBESPECIALIZADA = "ALTA_ATENCION_SUBESPECIALIZADA"
    MAXIMA_ATENCION_CRITICA = "MAXIMA_ATENCION_CRITICA"

class ModalidadAtencionIntegral(str, Enum):
    """Enum exacto según migración BD líneas 220-227"""
    PRESENCIAL_INSTITUCIONAL = "PRESENCIAL_INSTITUCIONAL"
    DOMICILIARIA_TERRITORIO = "DOMICILIARIA_TERRITORIO"
    TELEATENCION_VIRTUAL = "TELEATENCION_VIRTUAL"
    MIXTA_HIBRIDA = "MIXTA_HIBRIDA"
    ITINERANTE_MOVIL = "ITINERANTE_MOVIL"
    COMUNITARIA_COLECTIVA = "COMUNITARIA_COLECTIVA"

# =============================================================================
# MODELO COMPLETO - Todos los campos según migración BD líneas 230-300
# =============================================================================

class ModeloAtencionIntegralTransversalCompleto(BaseModel):
    """
    Modelo que coincide EXACTAMENTE con la tabla atencion_integral_transversal_salud
    Basado en migración líneas 230-300
    """
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        str_strip_whitespace=True
    )

    # Campos principales (línea 231-235)
    id: Optional[UUID] = Field(None, description="ID único del registro")
    codigo_atencion_integral_unico: str = Field(
        ..., 
        description="Código único de atención integral - LÍNEA 232"
    )
    tipo_abordaje_atencion_integral: TipoAbordajeAtencionIntegralSalud = Field(
        ...,
        description="Tipo de abordaje de atención integral - LÍNEA 233"
    )
    nivel_complejidad_atencion: Optional[NivelComplejidadAtencionIntegral] = Field(
        NivelComplejidadAtencionIntegral.BAJA_ATENCION_PRIMARIA,
        description="Nivel de complejidad atención - LÍNEA 234"
    )
    modalidad_atencion: Optional[ModalidadAtencionIntegral] = Field(
        ModalidadAtencionIntegral.PRESENCIAL_INSTITUCIONAL,
        description="Modalidad de atención - LÍNEA 235"
    )
    
    # Sujeto de atención (líneas 237-239)
    sujeto_atencion: str = Field(
        ..., 
        description="Sujeto de atención - LÍNEA 238"
    )
    identificacion_sujeto_atencion: Optional[str] = Field(
        None,
        description="Identificación del sujeto de atención - LÍNEA 239"
    )
    
    # Contexto de la atención integral (líneas 241-243)
    entornos_salud_publica_involucrados: Optional[List[UUID]] = Field(
        None,
        description="Array de IDs de entornos involucrados - LÍNEA 242"
    )
    familia_beneficiaria_id: Optional[UUID] = Field(
        None,
        description="ID de la familia beneficiaria - LÍNEA 243"
    )
    
    # Caracterización de la atención (líneas 245-249)
    motivo_atencion_integral: str = Field(
        ...,
        description="Motivo de atención integral - LÍNEA 246"
    )
    objetivos_atencion_integral: Optional[Dict[str, Any]] = Field(
        None,
        description="Objetivos de atención integral JSONB - LÍNEA 247"
    )
    intervenciones_programadas: Optional[Dict[str, Any]] = Field(
        None,
        description="Intervenciones programadas JSONB - LÍNEA 248"
    )
    resultados_esperados: Optional[Dict[str, Any]] = Field(
        None,
        description="Resultados esperados JSONB - LÍNEA 249"
    )
    
    # Equipo de atención integral (líneas 251-254)
    profesional_coordinador_atencion: Optional[UUID] = Field(
        None,
        description="Profesional coordinador de atención UUID - LÍNEA 252"
    )
    equipo_interdisciplinario_ids: Optional[List[UUID]] = Field(
        None,
        description="Equipo interdisciplinario IDs array - LÍNEA 253"
    )
    especialidades_involucradas: Optional[Dict[str, Any]] = Field(
        None,
        description="Especialidades involucradas JSONB - LÍNEA 254"
    )
    
    # Temporalidad y seguimiento (líneas 256-261)
    fecha_inicio_atencion_integral: Optional[datetime] = Field(
        None,
        description="Fecha inicio atención integral - LÍNEA 257"
    )
    fecha_finalizacion_programada: Optional[datetime] = Field(
        None,
        description="Fecha finalización programada - LÍNEA 258"
    )
    fecha_finalizacion_real: Optional[datetime] = Field(
        None,
        description="Fecha finalización real - LÍNEA 259"
    )
    duracion_estimada_dias: Optional[int] = Field(
        None,
        description="Duración estimada en días - LÍNEA 260"
    )
    frecuencia_seguimiento: Optional[str] = Field(
        None,
        description="Frecuencia de seguimiento - LÍNEA 261"
    )
    
    # Recursos y tecnologías (líneas 263-267)
    recursos_tecnicos_utilizados: Optional[Dict[str, Any]] = Field(
        None,
        description="Recursos técnicos utilizados JSONB - LÍNEA 264"
    )
    tecnologias_informacion_salud: Optional[Dict[str, Any]] = Field(
        None,
        description="Tecnologías información salud JSONB - LÍNEA 265"
    )
    dispositivos_medicos_requeridos: Optional[Dict[str, Any]] = Field(
        None,
        description="Dispositivos médicos requeridos JSONB - LÍNEA 266"
    )
    medicamentos_dispositivos_suministrados: Optional[Dict[str, Any]] = Field(
        None,
        description="Medicamentos dispositivos suministrados JSONB - LÍNEA 267"
    )
    
    # Coordinación intersectorial (líneas 269-272)
    instituciones_participantes: Optional[Dict[str, Any]] = Field(
        None,
        description="Instituciones participantes JSONB - LÍNEA 270"
    )
    sectores_involucrados: Optional[Dict[str, Any]] = Field(
        None,
        description="Sectores involucrados JSONB - LÍNEA 271"
    )
    mecanismos_coordinacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Mecanismos de coordinación JSONB - LÍNEA 272"
    )
    
    # Indicadores y resultados (líneas 274-278)
    indicadores_proceso_atencion: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores proceso atención JSONB - LÍNEA 275"
    )
    indicadores_resultado_atencion: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores resultado atención JSONB - LÍNEA 276"
    )
    indicadores_impacto_poblacional: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores impacto poblacional JSONB - LÍNEA 277"
    )
    nivel_satisfaccion_usuario: Optional[Decimal] = Field(
        None,
        description="Nivel satisfacción usuario 0.00-10.00 - LÍNEA 278"
    )
    
    # Continuidad de la atención (líneas 280-283)
    atencion_previa_relacionada: Optional[UUID] = Field(
        None,
        description="Atención previa relacionada UUID - LÍNEA 281"
    )
    atencion_posterior_programada: Optional[UUID] = Field(
        None,
        description="Atención posterior programada UUID - LÍNEA 282"
    )
    referencia_contrarreferencia: Optional[Dict[str, Any]] = Field(
        None,
        description="Referencia contrarreferencia JSONB - LÍNEA 283"
    )
    
    # Documentación y evidencia (líneas 285-288)
    documentos_soporte_atencion: Optional[Dict[str, Any]] = Field(
        None,
        description="Documentos soporte atención JSONB - LÍNEA 286"
    )
    evidencia_cientifica_utilizada: Optional[Dict[str, Any]] = Field(
        None,
        description="Evidencia científica utilizada JSONB - LÍNEA 287"
    )
    guias_protocolos_aplicados: Optional[Dict[str, Any]] = Field(
        None,
        description="Guías protocolos aplicados JSONB - LÍNEA 288"
    )
    
    # Estado y seguimiento (líneas 290-293)
    estado_atencion_integral: Optional[str] = Field(
        "PROGRAMADA",
        description="Estado atención integral - LÍNEA 291"
    )
    porcentaje_cumplimiento_objetivos: Optional[Decimal] = Field(
        None,
        description="Porcentaje cumplimiento objetivos 0.00-100.00 - LÍNEA 292"
    )
    observaciones_seguimiento: Optional[str] = Field(
        None,
        description="Observaciones seguimiento - LÍNEA 293"
    )
    
    # Auditoría (líneas 295-299)
    creado_en: Optional[datetime] = Field(
        None,
        description="Fecha de creación - LÍNEA 296"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Fecha de última actualización - LÍNEA 297"
    )
    creado_por: Optional[UUID] = Field(
        None,
        description="Usuario que creó el registro - LÍNEA 298"
    )
    actualizado_por: Optional[UUID] = Field(
        None,
        description="Usuario que actualizó el registro - LÍNEA 299"
    )

# =============================================================================
# MODELOS DE ENTRADA Y SALIDA
# =============================================================================

class ModeloAtencionIntegralTransversalCrear(BaseModel):
    """Modelo para crear atención integral transversal - solo campos requeridos según BD"""
    
    codigo_atencion_integral_unico: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Código único de atención integral"
    )
    tipo_abordaje_atencion_integral: TipoAbordajeAtencionIntegralSalud = Field(
        ...,
        description="Tipo de abordaje de atención integral"
    )
    sujeto_atencion: str = Field(
        ...,
        description="Sujeto de atención (INDIVIDUAL, FAMILIAR, POBLACIONAL, COMUNITARIO)"
    )
    motivo_atencion_integral: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Motivo de la atención integral"
    )
    
    # Campos opcionales comunes
    nivel_complejidad_atencion: Optional[NivelComplejidadAtencionIntegral] = NivelComplejidadAtencionIntegral.BAJA_ATENCION_PRIMARIA
    modalidad_atencion: Optional[ModalidadAtencionIntegral] = ModalidadAtencionIntegral.PRESENCIAL_INSTITUCIONAL
    identificacion_sujeto_atencion: Optional[str] = None
    familia_beneficiaria_id: Optional[UUID] = None
    entornos_salud_publica_involucrados: Optional[List[UUID]] = None

class ModeloAtencionIntegralTransversalRespuesta(ModeloAtencionIntegralTransversalCompleto):
    """Modelo de respuesta - incluye todos los campos con ID y auditoría requeridos"""
    
    id: UUID = Field(..., description="ID único del registro")
    creado_en: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

class ModeloAtencionIntegralTransversalActualizar(BaseModel):
    """Modelo para actualizar atención integral transversal - todos los campos opcionales"""
    
    tipo_abordaje_atencion_integral: Optional[TipoAbordajeAtencionIntegralSalud] = None
    nivel_complejidad_atencion: Optional[NivelComplejidadAtencionIntegral] = None
    modalidad_atencion: Optional[ModalidadAtencionIntegral] = None
    sujeto_atencion: Optional[str] = None
    motivo_atencion_integral: Optional[str] = Field(None, min_length=10, max_length=500)
    identificacion_sujeto_atencion: Optional[str] = None
    familia_beneficiaria_id: Optional[UUID] = None
    entornos_salud_publica_involucrados: Optional[List[UUID]] = None
    objetivos_atencion_integral: Optional[Dict[str, Any]] = None
    intervenciones_programadas: Optional[Dict[str, Any]] = None
    estado_atencion_integral: Optional[str] = None
    observaciones_seguimiento: Optional[str] = None
    # ... más campos opcionales según necesidad