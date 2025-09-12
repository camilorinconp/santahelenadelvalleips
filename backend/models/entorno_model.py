from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class TipoEntornoSaludPublica(str, Enum):
    """Tipos de entorno para intervenciones en salud pública según Resolución 3280 Art. 2570-2572"""
    ENTORNO_FAMILIAR_HOGAR_DOMESTICO = "ENTORNO_FAMILIAR_HOGAR_DOMESTICO"
    ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL = "ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL" 
    ENTORNO_COMUNITARIO_SOCIAL_TERRITORIAL = "ENTORNO_COMUNITARIO_SOCIAL_TERRITORIAL"
    ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO = "ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO"
    ENTORNO_INSTITUCIONAL_SALUD_ASISTENCIAL = "ENTORNO_INSTITUCIONAL_SALUD_ASISTENCIAL"

class ModeloEntornoIntegralSaludPublica(BaseModel):
    """
    Modelo transversal para gestión integral de entornos según Resolución 3280
    Art. 2593-2599: Características sociales y ambientales de cada entorno de salud pública
    """
    id: Optional[UUID] = None
    tipo_entorno_salud_publica: TipoEntornoSaludPublica
    nombre_descriptivo_entorno: str
    descripcion_detallada_entorno: Optional[str] = None
    
    # Características sociales y ambientales (Art. 2593)
    caracteristicas_sociales_ambientales: Optional[Dict[str, Any]] = None  # JSONB con dinámicas sociales del entorno
    factores_ambientales_determinantes: Optional[Dict[str, Any]] = None  # JSONB con condiciones físicas y ambientales
    
    # Información geográfica y territorial
    municipio_territorio_ubicacion: Optional[str] = None
    departamento_division_territorial: Optional[str] = None
    direccion_fisica_completa: Optional[str] = None
    coordenadas_geograficas_geolocalizacion: Optional[Dict[str, float]] = None  # {"latitud": x, "longitud": y}
    
    # Población objetivo beneficiaria
    poblacion_objetivo_beneficiaria: Optional[str] = None
    numero_personas_beneficiarias_estimadas: Optional[int] = None
    
    # Prioridades sanitarias definidas (Art. 2598)
    prioridades_salud_publica_identificadas: Optional[Dict[str, Any]] = None  # JSONB con prioridades sanitarias del entorno
    objetivos_resultados_salud_esperados: Optional[Dict[str, Any]] = None  # JSONB con metas e indicadores de salud
    
    # Metadatos de registro y auditoria
    estado_activo_entorno: bool = True
    fecha_hora_creacion_registro: Optional[datetime] = None
    fecha_hora_ultima_actualizacion: Optional[datetime] = None
    profesional_responsable_creacion_id: Optional[UUID] = None  # ID del profesional de salud que registró el entorno

class RelacionPersonaEntornoSaludPublica(BaseModel):
    """
    Relación integral entre personas y entornos de salud pública donde se desenvuelven
    Una persona puede participar en múltiples entornos simultáneamente
    """
    id: Optional[UUID] = None
    paciente_persona_id: UUID  # ID del paciente/persona en el entorno
    entorno_salud_publica_id: UUID  # ID del entorno de salud pública
    
    # Tiempo de permanencia y exposición al entorno
    fecha_inicio_vinculacion_entorno: Optional[datetime] = None
    fecha_finalizacion_vinculacion_entorno: Optional[datetime] = None
    horas_permanencia_promedio_dia: Optional[int] = None
    dias_permanencia_promedio_semana: Optional[int] = None
    
    # Rol y función en el entorno
    rol_funcion_entorno: Optional[str] = None  # "estudiante", "trabajador", "residente", "visitante", etc.
    descripcion_actividades_desarrolladas: Optional[str] = None
    
    # Factores de riesgo y protección específicos del entorno
    factores_riesgo_salud_entorno: Optional[Dict[str, Any]] = None  # JSONB con riesgos específicos del entorno
    factores_proteccion_salud_entorno: Optional[Dict[str, Any]] = None  # JSONB con elementos protectores del entorno
    
    # Estado de la relación persona-entorno
    relacion_activa_vigente: bool = True
    fecha_hora_creacion_relacion: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_relacion: Optional[datetime] = None

class IntervencionSaludPublicaEntorno(BaseModel):
    """
    Intervenciones de salud pública específicas realizadas en cada entorno
    Art. 2570: Intervenciones integradas e integrales en los entornos de salud pública
    """
    id: Optional[UUID] = None
    entorno_intervencion_id: UUID  # ID del entorno donde se realiza la intervención
    atencion_salud_vinculada_id: Optional[UUID] = None  # Vinculación con atención médica específica
    
    # Tipo de intervención de salud pública
    tipo_intervencion_salud_publica: str  # "individual_personalizada", "colectiva_grupal", "poblacional_masiva"
    nombre_descriptivo_intervencion: str
    descripcion_detallada_intervencion: Optional[str] = None
    
    # Cronograma de ejecución
    fecha_planificacion_intervencion: Optional[datetime] = None
    fecha_ejecucion_intervencion: Optional[datetime] = None
    fecha_evaluacion_resultados: Optional[datetime] = None
    
    # Resultados y evaluación de impacto
    numero_personas_beneficiadas_intervencion: Optional[int] = None
    resultados_salud_obtenidos: Optional[Dict[str, Any]] = None  # JSONB con resultados sanitarios y sociales
    indicadores_cumplimiento_objetivos: Optional[Dict[str, Any]] = None  # JSONB con métricas de efectividad
    nivel_satisfaccion_comunidad: Optional[int] = None  # Escala evaluación 1-5
    
    # Recursos humanos y materiales utilizados
    profesionales_equipo_participante: Optional[Dict[str, Any]] = None  # JSONB con información del talento humano
    recursos_materiales_utilizados: Optional[Dict[str, Any]] = None  # JSONB con inventario de recursos
    costo_financiero_estimado: Optional[float] = None
    
    # Estado de la intervención
    estado_actual_intervencion: Optional[str] = "PLANIFICADA_PENDIENTE"  # PLANIFICADA_PENDIENTE, EN_EJECUCION_ACTIVA, COMPLETADA_FINALIZADA, CANCELADA_SUSPENDIDA
    intervencion_activa_vigente: bool = True
    fecha_hora_creacion_intervencion: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_intervencion: Optional[datetime] = None
    profesional_responsable_intervencion_id: Optional[UUID] = None  # ID del profesional líder