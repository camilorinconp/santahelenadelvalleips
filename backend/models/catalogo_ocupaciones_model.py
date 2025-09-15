# ===================================================================
# MODELS: Catálogo de Ocupaciones DANE  
# ===================================================================
# Descripción: Modelos Pydantic para catálogo de ocupaciones DANE
# Autor: Backend Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Propósito: Soporte para variables PEDT y autocompletado inteligente
# ===================================================================

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


# ===================================================================
# MODELOS BASE
# ===================================================================

class OcupacionDaneBase(BaseModel):
    """Modelo base para ocupación DANE"""
    model_config = ConfigDict(from_attributes=True)
    
    codigo_ocupacion_dane: str = Field(
        ..., 
        description="Código oficial DANE único de la ocupación",
        examples=["2211"]
    )
    nombre_ocupacion_normalizado: str = Field(
        ..., 
        description="Nombre completo normalizado de la ocupación",
        examples=["Médicos Generales"]
    )
    categoria_ocupacional_nivel_1: Optional[str] = Field(
        None,
        description="Grandes grupos ocupacionales",
        examples=["2 - Profesionales Científicos e Intelectuales"]
    )
    categoria_ocupacional_nivel_2: Optional[str] = Field(
        None,
        description="Subgrupos principales",
        examples=["22 - Profesionales en ciencias biológicas y de la salud"]
    )
    categoria_ocupacional_nivel_3: Optional[str] = Field(
        None,
        description="Subgrupos secundarios",
        examples=["221 - Profesionales en medicina"]
    )
    categoria_ocupacional_nivel_4: Optional[str] = Field(
        None,
        description="Nivel más granular si existe"
    )
    descripcion_detallada: Optional[str] = Field(
        None,
        description="Descripción completa DANE",
        examples=["Médicos que brindan atención médica general"]
    )
    nivel_educativo_requerido: Optional[str] = Field(
        None,
        description="Nivel educativo típicamente requerido",
        examples=["Universitaria"]
    )
    activo: bool = Field(
        True,
        description="Estado activo de la ocupación"
    )

    @field_validator('codigo_ocupacion_dane')
    @classmethod
    def validar_codigo_dane(cls, v):
        if not v or not v.strip():
            raise ValueError('Código DANE no puede estar vacío')
        return v.strip()

    @field_validator('nombre_ocupacion_normalizado')
    @classmethod
    def validar_nombre_ocupacion(cls, v):
        if not v or not v.strip():
            raise ValueError('Nombre ocupación no puede estar vacío')
        return v.strip()


class OcupacionDaneCreate(OcupacionDaneBase):
    """Modelo para crear nueva ocupación DANE"""
    competencias_principales: Optional[Dict[str, Any]] = Field(
        None,
        description="Skills y competencias requeridas en formato JSON"
    )
    sectores_economicos_asociados: Optional[Dict[str, Any]] = Field(
        None,
        description="Sectores económicos donde se desempeña"
    )
    metadatos_adicionales: Optional[Dict[str, Any]] = Field(
        None,
        description="Información adicional flexible"
    )


class OcupacionDaneUpdate(BaseModel):
    """Modelo para actualizar ocupación DANE"""
    nombre_ocupacion_normalizado: Optional[str] = None
    categoria_ocupacional_nivel_1: Optional[str] = None
    categoria_ocupacional_nivel_2: Optional[str] = None
    categoria_ocupacional_nivel_3: Optional[str] = None
    categoria_ocupacional_nivel_4: Optional[str] = None
    descripcion_detallada: Optional[str] = None
    nivel_educativo_requerido: Optional[str] = None
    activo: Optional[bool] = None
    metadatos_adicionales: Optional[Dict[str, Any]] = None


class OcupacionDaneResponse(OcupacionDaneBase):
    """Modelo de respuesta para ocupación DANE"""
    id: uuid.UUID = Field(..., description="UUID único del registro")
    fuente_dato: str = Field("DANE", description="Fuente del dato")
    version_catalogo: Optional[str] = Field(None, description="Versión del catálogo")
    metadatos_adicionales: Optional[Dict[str, Any]] = Field(
        None, 
        description="Metadatos adicionales en formato JSON"
    )
    creado_en: datetime = Field(..., description="Fecha de creación")
    actualizado_en: datetime = Field(..., description="Fecha de última actualización")

    model_config = ConfigDict(from_attributes=True)


# ===================================================================
# MODELOS PARA BÚSQUEDA Y AUTOCOMPLETADO
# ===================================================================

class OcupacionBusquedaRequest(BaseModel):
    """Modelo para solicitudes de búsqueda de ocupaciones"""
    termino: str = Field(
        ...,
        min_length=3,
        description="Término de búsqueda (mínimo 3 caracteres)",
        examples=["enfer"]
    )
    limite: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Número máximo de resultados"
    )
    categoria_nivel_1: Optional[str] = Field(
        None,
        description="Filtrar por categoría nivel 1"
    )
    solo_activos: bool = Field(
        default=True,
        description="Solo mostrar ocupaciones activas"
    )

    @field_validator('termino')
    @classmethod
    def validar_termino_busqueda(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Término debe tener al menos 3 caracteres')
        return v.strip().lower()


class OcupacionAutocompletadoResponse(BaseModel):
    """Modelo simplificado para respuestas de autocompletado"""
    id: uuid.UUID
    codigo_ocupacion_dane: str
    nombre_ocupacion_normalizado: str
    categoria_ocupacional_nivel_1: Optional[str]
    relevancia: Optional[float] = Field(
        None,
        description="Puntaje de relevancia de la búsqueda (0.0-1.0)"
    )

    model_config = ConfigDict(from_attributes=True)


class OcupacionEstadisticasResponse(BaseModel):
    """Estadísticas del catálogo de ocupaciones"""
    total_ocupaciones: int
    ocupaciones_activas: int
    categorias_nivel_1: int
    categorias_nivel_2: int
    ultima_actualizacion: datetime
    version_catalogo: Optional[str]


# ===================================================================
# MODELOS PARA INTEGRACIÓN CON OTRAS ENTIDADES
# ===================================================================

class PacienteOcupacionUpdate(BaseModel):
    """Modelo para actualizar ocupación de un paciente"""
    ocupacion_id: Optional[uuid.UUID] = Field(
        None,
        description="UUID de la ocupación seleccionada del catálogo"
    )
    ocupacion_otra_descripcion: Optional[str] = Field(
        None,
        description="Descripción manual si no está en catálogo"
    )

    @field_validator('ocupacion_otra_descripcion')
    @classmethod
    def validar_ocupacion_manual(cls, v, values):
        # Si no hay ocupacion_id, debe haber descripción manual
        if not values.get('ocupacion_id') and not v:
            raise ValueError('Debe especificar ocupacion_id o descripción manual')
        return v


class ReporteOcupacionesPEDT(BaseModel):
    """Modelo para reportes PEDT con ocupaciones normalizadas"""
    periodo_inicio: datetime
    periodo_fin: datetime
    total_pacientes: int
    ocupaciones_catalogadas: int
    ocupaciones_manuales: int
    cobertura_porcentaje: float
    principales_ocupaciones: List[Dict[str, Any]]


# ===================================================================
# MODELOS DE RESPUESTA BULK
# ===================================================================

class OcupacionesBulkResponse(BaseModel):
    """Respuesta para operaciones masivas"""
    procesados: int
    exitosos: int
    errores: int
    tiempo_procesamiento: float
    detalles_errores: Optional[List[str]] = None


class OcupacionesCategoriaResponse(BaseModel):
    """Respuesta agrupada por categorías"""
    categoria: str
    total_ocupaciones: int
    ocupaciones: List[OcupacionAutocompletadoResponse]


# ===================================================================
# UTILIDADES DE VALIDACIÓN
# ===================================================================

def validar_codigo_dane_formato(codigo: str) -> bool:
    """
    Validar formato de código DANE (típicamente 4 dígitos)
    """
    try:
        # Códigos DANE suelen ser 4 dígitos, pero pueden variar
        return codigo.isdigit() and len(codigo) >= 3
    except:
        return False


def normalizar_nombre_ocupacion(nombre: str) -> str:
    """
    Normalizar nombre de ocupación para búsqueda consistente
    """
    if not nombre:
        return ""
    
    # Eliminar espacios extra, capitalizar apropiadamente
    normalized = " ".join(nombre.strip().split())
    
    # Capitalizar primera letra de cada palabra importante
    words = normalized.split()
    normalized_words = []
    
    # Palabras que no se capitalizan (artículos, preposiciones)
    no_capitalize = {'de', 'del', 'en', 'con', 'para', 'por', 'la', 'el', 'y', 'o'}
    
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in no_capitalize:
            normalized_words.append(word.capitalize())
        else:
            normalized_words.append(word.lower())
    
    return " ".join(normalized_words)


# ===================================================================
# MODELOS PARA ANÁLISIS Y MÉTRICAS
# ===================================================================

class OcupacionAnalisisResponse(BaseModel):
    """Análisis detallado de ocupaciones para dashboard"""
    distribucion_categorias: Dict[str, int]
    ocupaciones_mas_frecuentes: List[Dict[str, Any]]
    niveles_educativos: Dict[str, int]
    tendencias_utilizacion: List[Dict[str, Any]]
    metricas_completitud: Dict[str, float]


# ===================================================================
# CONFIGURACIÓN DEL MÓDULO
# ===================================================================

__all__ = [
    # Modelos principales
    'OcupacionDaneBase',
    'OcupacionDaneCreate', 
    'OcupacionDaneUpdate',
    'OcupacionDaneResponse',
    
    # Modelos de búsqueda
    'OcupacionBusquedaRequest',
    'OcupacionAutocompletadoResponse',
    'OcupacionEstadisticasResponse',
    
    # Modelos de integración
    'PacienteOcupacionUpdate',
    'ReporteOcupacionesPEDT',
    
    # Modelos bulk
    'OcupacionesBulkResponse',
    'OcupacionesCategoriaResponse',
    'OcupacionAnalisisResponse',
    
    # Utilidades
    'validar_codigo_dane_formato',
    'normalizar_nombre_ocupacion'
]