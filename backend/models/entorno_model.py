# =============================================================================
# Modelo de Entornos de Salud Pública - Arquitectura Transversal 
# Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID

# =============================================================================
# ENUMS - Tipos de Entorno y Estados
# =============================================================================

class TipoEntornoSaludPublica(str, Enum):
    """
    Enum para los 5 tipos de entorno de salud pública según Resolución 3280.
    
    Artículo 1364-1370: Los entornos constituyen espacios territoriales donde
    las personas desarrollan cotidianamente su vida y donde se llevan a cabo
    intervenciones de promoción de la salud y prevención de la enfermedad.
    """
    ENTORNO_FAMILIAR_HOGAR_DOMESTICO = "ENTORNO_FAMILIAR_HOGAR_DOMESTICO"
    ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL = "ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL"
    ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL = "ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL"
    ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO = "ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO"
    ENTORNO_INSTITUCIONAL_SERVICIOS_SALUD = "ENTORNO_INSTITUCIONAL_SERVICIOS_SALUD"


class NivelComplejidadIntervencionEntorno(str, Enum):
    """Nivel de complejidad de las intervenciones en el entorno"""
    BASICO_PROMOCION_PREVENCION = "BASICO_PROMOCION_PREVENCION"
    INTERMEDIO_INTERVENCION_TEMPRANA = "INTERMEDIO_INTERVENCION_TEMPRANA"
    AVANZADO_MANEJO_ESPECIALIZADO = "AVANZADO_MANEJO_ESPECIALIZADO"
    INTEGRAL_COORDINACION_INTERSECTORIAL = "INTEGRAL_COORDINACION_INTERSECTORIAL"


class EstadoActivacionEntorno(str, Enum):
    """Estado de activación del entorno para intervenciones"""
    ACTIVO_OPERATIVO = "ACTIVO_OPERATIVO"
    PARCIALMENTE_ACTIVO = "PARCIALMENTE_ACTIVO"
    INACTIVO_TEMPORAL = "INACTIVO_TEMPORAL"
    DESACTIVADO_DEFINITIVO = "DESACTIVADO_DEFINITIVO"

# =============================================================================
# MODELO PRINCIPAL - ENTORNO DE SALUD PÚBLICA
# =============================================================================

class ModeloEntornoSaludPublicaIntegralCompleto(BaseModel):
    """
    Modelo completo de Entorno de Salud Pública que integra todos los aspectos
    de caracterización según Resolución 3280 de 2018.
    
    Este modelo permite la gestión integral de los 5 entornos normativos:
    - Entorno Familiar/Hogar/Doméstico
    - Entorno Educativo/Formativo/Institucional  
    - Entorno Comunitario/Territorial/Social
    - Entorno Laboral/Ocupacional/Productivo
    - Entorno Institucional/Servicios de Salud
    """
    
    # Campos básicos identificación
    id: Optional[UUID] = Field(None, description="ID único del entorno")
    codigo_identificacion_entorno_unico: str = Field(
        ..., 
        description="Código único identificador del entorno",
        example="ENT-FAM-001"
    )
    tipo_entorno: TipoEntornoSaludPublica = Field(
        ...,
        description="Tipo de entorno según clasificación normativa"
    )
    nombre_descriptivo_entorno: str = Field(
        ...,
        description="Nombre descriptivo del entorno",
        example="Entorno Familiar Barrio Los Pinos"
    )
    descripcion_caracterizacion_entorno: Optional[str] = Field(
        None,
        description="Descripción detallada de la caracterización del entorno"
    )
    nivel_complejidad_intervencion: Optional[NivelComplejidadIntervencionEntorno] = Field(
        NivelComplejidadIntervencionEntorno.BASICO_PROMOCION_PREVENCION,
        description="Nivel de complejidad de intervenciones en el entorno"
    )
    estado_activacion: Optional[EstadoActivacionEntorno] = Field(
        EstadoActivacionEntorno.ACTIVO_OPERATIVO,
        description="Estado actual de activación del entorno"
    )
    
    # Geolocalización y contexto territorial
    departamento_ubicacion: Optional[str] = Field(
        None,
        description="Departamento donde se ubica el entorno",
        example="Valle del Cauca"
    )
    municipio_ubicacion: Optional[str] = Field(
        None,
        description="Municipio donde se ubica el entorno",
        example="Cali"
    )
    zona_territorial: Optional[str] = Field(
        None,
        description="Zona territorial: urbana, rural, dispersa",
        example="urbana"
    )
    coordenadas_geograficas: Optional[Dict[str, Any]] = Field(
        None,
        description="Coordenadas geográficas del entorno",
        example={"latitud": 3.4516, "longitud": -76.5320}
    )
    
    # Caracterización poblacional del entorno
    poblacion_objetivo_estimada: Optional[int] = Field(
        None,
        description="Población objetivo estimada para intervenciones",
        example=1500
    )
    rango_edad_poblacion_objetivo: Optional[Dict[str, int]] = Field(
        None,
        description="Rango de edad de población objetivo",
        example={"min_edad": 0, "max_edad": 18}
    )
    caracteristicas_demograficas_poblacion: Optional[Dict[str, Any]] = Field(
        None,
        description="Características demográficas específicas de la población"
    )
    
    # Capacidades y recursos del entorno
    recursos_disponibles_entorno: Optional[Dict[str, Any]] = Field(
        None,
        description="Recursos técnicos, humanos y físicos disponibles en el entorno"
    )
    actores_institucionales_involucrados: Optional[Dict[str, Any]] = Field(
        None,
        description="Actores institucionales que participan en el entorno"
    )
    programas_servicios_disponibles: Optional[Dict[str, Any]] = Field(
        None,
        description="Programas y servicios de salud disponibles en el entorno"
    )
    
    # Intervenciones y actividades
    intervenciones_realizadas_historico: Optional[Dict[str, Any]] = Field(
        None,
        description="Histórico de intervenciones realizadas en el entorno"
    )
    indicadores_resultado_entorno: Optional[Dict[str, Any]] = Field(
        None,
        description="Indicadores de resultado y evaluación del entorno"
    )
    plan_trabajo_entorno_vigente: Optional[Dict[str, Any]] = Field(
        None,
        description="Plan de trabajo vigente para el entorno"
    )
    
    # Articulación intersectorial
    alianzas_estrategicas_activas: Optional[Dict[str, Any]] = Field(
        None,
        description="Alianzas estratégicas activas en el entorno"
    )
    coordinacion_institucional_nivel: Optional[str] = Field(
        None,
        description="Nivel de coordinación institucional",
        example="ALTO"
    )
    mecanismos_participacion_comunitaria: Optional[Dict[str, Any]] = Field(
        None,
        description="Mecanismos de participación comunitaria implementados"
    )
    
    # Monitoreo y evaluación
    fecha_ultima_caracterizacion: Optional[datetime] = Field(
        None,
        description="Fecha de la última caracterización del entorno"
    )
    proxima_fecha_evaluacion: Optional[datetime] = Field(
        None,
        description="Próxima fecha programada de evaluación"
    )
    responsable_coordinacion_entorno: Optional[str] = Field(
        None,
        description="Responsable de la coordinación del entorno",
        example="Dr. Juan Pérez - Coordinador Territorial"
    )
    observaciones_adicionales_entorno: Optional[str] = Field(
        None,
        description="Observaciones adicionales sobre el entorno"
    )
    
    # Auditoría
    creado_en: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    creado_por: Optional[UUID] = Field(None, description="Usuario que creó el registro")
    actualizado_por: Optional[UUID] = Field(None, description="Usuario que actualizó el registro")
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "codigo_identificacion_entorno_unico": "ENT-FAM-001",
                "tipo_entorno": "ENTORNO_FAMILIAR_HOGAR_DOMESTICO",
                "nombre_descriptivo_entorno": "Entorno Familiar Barrio Los Pinos",
                "descripcion_caracterizacion_entorno": "Entorno familiar caracterizado para atención materno perinatal y primera infancia",
                "nivel_complejidad_intervencion": "BASICO_PROMOCION_PREVENCION",
                "estado_activacion": "ACTIVO_OPERATIVO",
                "departamento_ubicacion": "Valle del Cauca",
                "municipio_ubicacion": "Cali",
                "zona_territorial": "urbana",
                "poblacion_objetivo_estimada": 1500,
                "rango_edad_poblacion_objetivo": {"min_edad": 0, "max_edad": 18}
            }
        }
    )

# =============================================================================
# MODELOS DE RESPUESTA Y CREACIÓN
# =============================================================================

class ModeloEntornoSaludPublicaCrear(BaseModel):
    """Modelo para crear un nuevo entorno de salud pública"""
    
    codigo_identificacion_entorno_unico: str = Field(
        ..., 
        description="Código único identificador del entorno",
        example="ENT-FAM-001"
    )
    tipo_entorno: TipoEntornoSaludPublica = Field(
        ...,
        description="Tipo de entorno según clasificación normativa"
    )
    nombre_descriptivo_entorno: str = Field(
        ...,
        description="Nombre descriptivo del entorno",
        example="Entorno Familiar Barrio Los Pinos"
    )
    descripcion_caracterizacion_entorno: Optional[str] = Field(
        None,
        description="Descripción detallada de la caracterización del entorno"
    )
    nivel_complejidad_intervencion: Optional[NivelComplejidadIntervencionEntorno] = Field(
        NivelComplejidadIntervencionEntorno.BASICO_PROMOCION_PREVENCION,
        description="Nivel de complejidad de intervenciones en el entorno"
    )
    estado_activacion: Optional[EstadoActivacionEntorno] = Field(
        EstadoActivacionEntorno.ACTIVO_OPERATIVO,
        description="Estado actual de activación del entorno"
    )
    
    # Campos geográficos y poblacionales opcionales
    departamento_ubicacion: Optional[str] = None
    municipio_ubicacion: Optional[str] = None
    zona_territorial: Optional[str] = None
    coordenadas_geograficas: Optional[Dict[str, Any]] = None
    poblacion_objetivo_estimada: Optional[int] = None
    rango_edad_poblacion_objetivo: Optional[Dict[str, int]] = None
    caracteristicas_demograficas_poblacion: Optional[Dict[str, Any]] = None
    recursos_disponibles_entorno: Optional[Dict[str, Any]] = None
    actores_institucionales_involucrados: Optional[Dict[str, Any]] = None
    programas_servicios_disponibles: Optional[Dict[str, Any]] = None
    intervenciones_realizadas_historico: Optional[Dict[str, Any]] = None
    indicadores_resultado_entorno: Optional[Dict[str, Any]] = None
    plan_trabajo_entorno_vigente: Optional[Dict[str, Any]] = None
    alianzas_estrategicas_activas: Optional[Dict[str, Any]] = None
    coordinacion_institucional_nivel: Optional[str] = None
    mecanismos_participacion_comunitaria: Optional[Dict[str, Any]] = None
    fecha_ultima_caracterizacion: Optional[datetime] = None
    proxima_fecha_evaluacion: Optional[datetime] = None
    responsable_coordinacion_entorno: Optional[str] = None
    observaciones_adicionales_entorno: Optional[str] = None
    
    # Auditoría
    creado_por: Optional[UUID] = Field(None, description="Usuario que crea el registro")


class ModeloEntornoSaludPublicaActualizar(BaseModel):
    """Modelo para actualizar entorno de salud pública (campos opcionales)"""
    
    # Todos los campos opcionales para actualización parcial
    codigo_identificacion_entorno_unico: Optional[str] = None
    tipo_entorno: Optional[TipoEntornoSaludPublica] = None
    nombre_descriptivo_entorno: Optional[str] = None
    descripcion_caracterizacion_entorno: Optional[str] = None
    nivel_complejidad_intervencion: Optional[NivelComplejidadIntervencionEntorno] = None
    estado_activacion: Optional[EstadoActivacionEntorno] = None
    departamento_ubicacion: Optional[str] = None
    municipio_ubicacion: Optional[str] = None
    zona_territorial: Optional[str] = None
    coordenadas_geograficas: Optional[Dict[str, Any]] = None
    poblacion_objetivo_estimada: Optional[int] = None
    rango_edad_poblacion_objetivo: Optional[Dict[str, int]] = None
    caracteristicas_demograficas_poblacion: Optional[Dict[str, Any]] = None
    recursos_disponibles_entorno: Optional[Dict[str, Any]] = None
    actores_institucionales_involucrados: Optional[Dict[str, Any]] = None
    programas_servicios_disponibles: Optional[Dict[str, Any]] = None
    intervenciones_realizadas_historico: Optional[Dict[str, Any]] = None
    indicadores_resultado_entorno: Optional[Dict[str, Any]] = None
    plan_trabajo_entorno_vigente: Optional[Dict[str, Any]] = None
    alianzas_estrategicas_activas: Optional[Dict[str, Any]] = None
    coordinacion_institucional_nivel: Optional[str] = None
    mecanismos_participacion_comunitaria: Optional[Dict[str, Any]] = None
    fecha_ultima_caracterizacion: Optional[datetime] = None
    proxima_fecha_evaluacion: Optional[datetime] = None
    responsable_coordinacion_entorno: Optional[str] = None
    observaciones_adicionales_entorno: Optional[str] = None
    actualizado_por: Optional[UUID] = None


class ModeloEntornoSaludPublicaRespuesta(ModeloEntornoSaludPublicaIntegralCompleto):
    """Modelo de respuesta para entorno de salud pública con metadatos"""
    
    id: UUID = Field(..., description="ID único del entorno")
    creado_en: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")


class ModeloListaEntornosSaludPublica(BaseModel):
    """Modelo para lista paginada de entornos de salud pública"""
    
    entornos: List[ModeloEntornoSaludPublicaRespuesta] = Field(
        ..., 
        description="Lista de entornos de salud pública"
    )
    total: int = Field(..., description="Total de registros")
    pagina: int = Field(..., description="Página actual")
    tamaño_pagina: int = Field(..., description="Tamaño de página")
    total_paginas: int = Field(..., description="Total de páginas")


# =============================================================================
# MODELOS DE FILTRADO Y BÚSQUEDA
# =============================================================================

class ModeloFiltrosEntornoSaludPublica(BaseModel):
    """Modelo para filtros de búsqueda de entornos"""
    
    tipo_entorno: Optional[TipoEntornoSaludPublica] = Field(
        None, 
        description="Filtrar por tipo de entorno"
    )
    estado_activacion: Optional[EstadoActivacionEntorno] = Field(
        None,
        description="Filtrar por estado de activación"
    )
    nivel_complejidad_intervencion: Optional[NivelComplejidadIntervencionEntorno] = Field(
        None,
        description="Filtrar por nivel de complejidad"
    )
    departamento_ubicacion: Optional[str] = Field(
        None,
        description="Filtrar por departamento"
    )
    municipio_ubicacion: Optional[str] = Field(
        None,
        description="Filtrar por municipio"
    )
    zona_territorial: Optional[str] = Field(
        None,
        description="Filtrar por zona territorial"
    )
    poblacion_minima: Optional[int] = Field(
        None,
        description="Población objetivo mínima"
    )
    poblacion_maxima: Optional[int] = Field(
        None,
        description="Población objetivo máxima"
    )
    buscar_texto: Optional[str] = Field(
        None,
        description="Búsqueda de texto en nombre y descripción"
    )


# =============================================================================
# MODELO DE ESTADÍSTICAS Y REPORTES
# =============================================================================

class ModeloEstadisticasEntornoSaludPublica(BaseModel):
    """Modelo para estadísticas de entornos de salud pública"""
    
    total_entornos: int = Field(..., description="Total de entornos registrados")
    entornos_por_tipo: Dict[str, int] = Field(..., description="Distribución por tipo de entorno")
    entornos_por_estado: Dict[str, int] = Field(..., description="Distribución por estado de activación")
    entornos_por_departamento: Dict[str, int] = Field(..., description="Distribución por departamento")
    poblacion_total_estimada: int = Field(..., description="Población total estimada en todos los entornos")
    entornos_activos_porcentaje: float = Field(..., description="Porcentaje de entornos activos")
    fecha_generacion_estadisticas: datetime = Field(..., description="Fecha de generación de estadísticas")