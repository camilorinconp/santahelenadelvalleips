# =============================================================================
# Modelo de Atención Integral Transversal de Salud - Arquitectura Transversal 
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

class TipoAbordajeAtencionIntegralSalud(str, Enum):
    """
    Enum para tipos de abordaje de atención integral.
    Alineado con la tabla atencion_integral_transversal_salud en Supabase.
    """
    INDIVIDUAL_PERSONALIZADO = "INDIVIDUAL_PERSONALIZADO"
    FAMILIAR_GRUPAL = "FAMILIAR_GRUPAL"
    COMUNITARIO_COLECTIVO = "COMUNITARIO_COLECTIVO"
    POBLACIONAL_MASIVO = "POBLACIONAL_MASIVO"
    INTERSECTORIAL_COORDINADO = "INTERSECTORIAL_COORDINADO"


class ModalidadAtencionIntegral(str, Enum):
    """
    Enum para modalidades de atención integral.
    """
    PRESENCIAL_DIRECTA = "PRESENCIAL_DIRECTA"
    VIRTUAL_REMOTA = "VIRTUAL_REMOTA"
    MIXTA_HIBRIDA = "MIXTA_HIBRIDA"
    DOMICILIARIA_TERRENO = "DOMICILIARIA_TERRENO"
    INSTITUCIONAL_AMBULATORIA = "INSTITUCIONAL_AMBULATORIA"


class NivelComplejidadAtencionIntegral(str, Enum):
    """
    Enum para niveles de complejidad de atención integral.
    """
    BASICO_PROMOCION_PREVENCION = "BASICO_PROMOCION_PREVENCION"
    INTERMEDIO_DETECCION_TEMPRANA = "INTERMEDIO_DETECCION_TEMPRANA"
    AVANZADO_INTERVENCION_ESPECIALIZADA = "AVANZADO_INTERVENCION_ESPECIALIZADA"
    ALTA_COMPLEJIDAD_MULTIDISCIPLINARIA = "ALTA_COMPLEJIDAD_MULTIDISCIPLINARIA"


class EstadoAtencionIntegral(str, Enum):
    """
    Enum para estados de atención integral.
    """
    EN_PROCESO = "EN_PROCESO"
    COMPLETADA = "COMPLETADA"
    SUSPENDIDA = "SUSPENDIDA"
    CANCELADA = "CANCELADA"

# =============================================================================
# MODELOS PRINCIPALES - Alineados con tabla Supabase
# =============================================================================

class ModeloAtencionIntegralTransversalSaludCompleto(BaseModel):
    """
    Modelo completo para atención integral transversal de salud.
    Corresponde exactamente con la tabla atencion_integral_transversal_salud en Supabase.
    
    Artículo 1364-1370 Resolución 3280: Atención integral como eje transversal de las RIAS.
    """
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True
    )

    # Campos principales (requeridos)
    codigo_atencion_integral_unico: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Código único identificador de la atención integral (ej: AIT-001-2025)"
    )
    
    tipo_abordaje_atencion: TipoAbordajeAtencionIntegralSalud = Field(
        ...,
        description="Tipo de abordaje de la atención integral"
    )
    
    modalidad_atencion: ModalidadAtencionIntegral = Field(
        ...,
        description="Modalidad de prestación de la atención integral"
    )
    
    nivel_complejidad_atencion: NivelComplejidadAtencionIntegral = Field(
        ...,
        description="Nivel de complejidad de la atención integral"
    )
    
    fecha_inicio_atencion_integral: datetime = Field(
        ...,
        description="Fecha y hora de inicio de la atención integral"
    )
    
    objetivos_atencion_integral: Dict[str, Any] = Field(
        ...,
        description="Objetivos específicos de la atención integral (JSONB)"
    )

    # Referencias a otras entidades (opcionales)
    sujeto_atencion_individual_id: Optional[UUID] = Field(
        None,
        description="ID del paciente individual (si es atención individual)"
    )
    
    familia_integral_id: Optional[UUID] = Field(
        None,
        description="ID de la familia integral asociada"
    )
    
    entorno_asociado_id: Optional[UUID] = Field(
        None,
        description="ID del entorno de salud pública asociado"
    )

    # Fechas de planificación
    fecha_finalizacion_prevista: Optional[datetime] = Field(
        None,
        description="Fecha prevista para finalización de la atención"
    )
    
    fecha_finalizacion_real: Optional[datetime] = Field(
        None,
        description="Fecha real de finalización de la atención"
    )

    # Profesionales involucrados
    profesional_coordinador_id: Optional[UUID] = Field(
        None,
        description="ID del profesional coordinador de la atención"
    )
    
    equipo_interdisciplinario_ids: Optional[Dict[str, Any]] = Field(
        None,
        description="IDs del equipo interdisciplinario participante (JSONB)"
    )

    # Planificación y seguimiento
    plan_intervencion_detallado: Optional[Dict[str, Any]] = Field(
        None,
        description="Plan detallado de intervenciones (JSONB)"
    )
    
    actividades_realizadas_log: Optional[Dict[str, Any]] = Field(
        None,
        description="Log de actividades realizadas (JSONB)"
    )
    
    resultados_obtenidos_medicion: Optional[Dict[str, Any]] = Field(
        None,
        description="Resultados obtenidos y mediciones (JSONB)"
    )
    
    indicadores_proceso_seguimiento: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores de proceso y seguimiento (JSONB)"
    )

    # Barreras y facilitadores
    barreras_dificultades_encontradas: Optional[Dict[str, Any]] = Field(
        None,
        description="Barreras y dificultades encontradas (JSONB)"
    )
    
    facilitadores_recursos_utilizados: Optional[Dict[str, Any]] = Field(
        None,
        description="Facilitadores y recursos utilizados (JSONB)"
    )

    # Evaluación y satisfacción
    evaluacion_satisfaccion_usuario: Optional[Dict[str, Any]] = Field(
        None,
        description="Evaluación de satisfacción del usuario (JSONB)"
    )
    
    recomendaciones_seguimiento: Optional[Dict[str, Any]] = Field(
        None,
        description="Recomendaciones para seguimiento (JSONB)"
    )
    
    articulacion_otros_servicios: Optional[Dict[str, Any]] = Field(
        None,
        description="Articulación con otros servicios (JSONB)"
    )

    # Estado y fechas de seguimiento
    estado_atencion_integral: Optional[str] = Field(
        "EN_PROCESO",
        max_length=50,
        description="Estado actual de la atención integral"
    )
    
    fecha_ultima_evaluacion: Optional[datetime] = Field(
        None,
        description="Fecha de la última evaluación realizada"
    )
    
    proxima_fecha_seguimiento: Optional[datetime] = Field(
        None,
        description="Fecha programada para próximo seguimiento"
    )

    # Observaciones adicionales
    observaciones_adicionales_atencion: Optional[str] = Field(
        None,
        max_length=2000,
        description="Observaciones adicionales sobre la atención"
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

class ModeloAtencionIntegralTransversalSaludCrear(BaseModel):
    """Modelo para crear una nueva atención integral - solo campos requeridos y opcionales de entrada"""
    
    codigo_atencion_integral_unico: str = Field(..., min_length=3, max_length=50)
    tipo_abordaje_atencion: TipoAbordajeAtencionIntegralSalud
    modalidad_atencion: ModalidadAtencionIntegral
    nivel_complejidad_atencion: NivelComplejidadAtencionIntegral
    fecha_inicio_atencion_integral: datetime
    objetivos_atencion_integral: Dict[str, Any]
    
    # Campos opcionales para creación
    sujeto_atencion_individual_id: Optional[UUID] = None
    familia_integral_id: Optional[UUID] = None
    entorno_asociado_id: Optional[UUID] = None
    fecha_finalizacion_prevista: Optional[datetime] = None
    profesional_coordinador_id: Optional[UUID] = None
    equipo_interdisciplinario_ids: Optional[Dict[str, Any]] = None
    plan_intervencion_detallado: Optional[Dict[str, Any]] = None
    estado_atencion_integral: Optional[str] = "EN_PROCESO"
    observaciones_adicionales_atencion: Optional[str] = None


class ModeloAtencionIntegralTransversalSaludRespuesta(ModeloAtencionIntegralTransversalSaludCompleto):
    """Modelo de respuesta - incluye todos los campos incluyendo metadatos del sistema"""
    id: UUID = Field(..., description="ID único del registro")
    creado_en: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")


class ModeloAtencionIntegralTransversalSaludActualizar(BaseModel):
    """Modelo para actualizar atención integral - todos los campos opcionales"""
    
    tipo_abordaje_atencion: Optional[TipoAbordajeAtencionIntegralSalud] = None
    modalidad_atencion: Optional[ModalidadAtencionIntegral] = None
    nivel_complejidad_atencion: Optional[NivelComplejidadAtencionIntegral] = None
    sujeto_atencion_individual_id: Optional[UUID] = None
    familia_integral_id: Optional[UUID] = None
    entorno_asociado_id: Optional[UUID] = None
    fecha_finalizacion_prevista: Optional[datetime] = None
    fecha_finalizacion_real: Optional[datetime] = None
    profesional_coordinador_id: Optional[UUID] = None
    equipo_interdisciplinario_ids: Optional[Dict[str, Any]] = None
    objetivos_atencion_integral: Optional[Dict[str, Any]] = None
    plan_intervencion_detallado: Optional[Dict[str, Any]] = None
    actividades_realizadas_log: Optional[Dict[str, Any]] = None
    resultados_obtenidos_medicion: Optional[Dict[str, Any]] = None
    indicadores_proceso_seguimiento: Optional[Dict[str, Any]] = None
    barreras_dificultades_encontradas: Optional[Dict[str, Any]] = None
    facilitadores_recursos_utilizados: Optional[Dict[str, Any]] = None
    evaluacion_satisfaccion_usuario: Optional[Dict[str, Any]] = None
    recomendaciones_seguimiento: Optional[Dict[str, Any]] = None
    articulacion_otros_servicios: Optional[Dict[str, Any]] = None
    estado_atencion_integral: Optional[str] = None
    fecha_ultima_evaluacion: Optional[datetime] = None
    proxima_fecha_seguimiento: Optional[datetime] = None
    observaciones_adicionales_atencion: Optional[str] = None