from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum

class TipoAbordajeAtencionIntegralSalud(str, Enum):
    """Tipos de abordaje para atención integral de salud según enfoque Resolución 3280"""
    ABORDAJE_INDIVIDUAL_PERSONALIZADO = "ABORDAJE_INDIVIDUAL_PERSONALIZADO"
    ABORDAJE_FAMILIAR_NUCLEO_DOMESTICO = "ABORDAJE_FAMILIAR_NUCLEO_DOMESTICO" 
    ABORDAJE_COLECTIVO_GRUPAL_COMUNITARIO = "ABORDAJE_COLECTIVO_GRUPAL_COMUNITARIO"
    ABORDAJE_COMUNITARIO_TERRITORIAL = "ABORDAJE_COMUNITARIO_TERRITORIAL"
    ABORDAJE_POBLACIONAL_MASIVO_EPIDEMIOLOGICO = "ABORDAJE_POBLACIONAL_MASIVO_EPIDEMIOLOGICO"

class NivelComplejidadAtencionIntegralSalud(str, Enum):
    """Nivel de complejidad para atención integral de salud según capacidad resolutiva"""
    COMPLEJIDAD_BAJA_PROMOCION_PREVENCION = "COMPLEJIDAD_BAJA_PROMOCION_PREVENCION"  # Promoción y prevención básica primaria
    COMPLEJIDAD_MEDIA_INTERVENCIONES_ESPECIFICAS = "COMPLEJIDAD_MEDIA_INTERVENCIONES_ESPECIFICAS"  # Intervenciones específicas especializadas
    COMPLEJIDAD_ALTA_CASOS_COMPLEJOS_ESPECIALIZADOS = "COMPLEJIDAD_ALTA_CASOS_COMPLEJOS_ESPECIALIZADOS"  # Manejo de casos complejos especializados
    COMPLEJIDAD_MUY_ALTA_VULNERABILIDAD_CRITICA = "COMPLEJIDAD_MUY_ALTA_VULNERABILIDAD_CRITICA"  # Casos de alta vulnerabilidad y riesgo crítico

class ModeloAtencionIntegralTransversalSalud(BaseModel):
    """
    Modelo para atención integral transversal de salud pública
    Art. 2570: 'de manera integrada e integral en los entornos de salud'
    Art. 32: 'integral de los principales riesgos en salud poblacional'
    """
    id: Optional[UUID] = None
    
    # Sujeto de atención integral (individual o familiar)
    paciente_persona_individual_id: Optional[UUID] = None
    familia_nucleo_familiar_id: Optional[UUID] = None
    
    # Identificación y cronograma de la atención integral
    codigo_identificacion_atencion_integral: Optional[str] = None
    fecha_inicio_atencion_integral: date
    fecha_finalizacion_estimada_planificada: Optional[date] = None
    fecha_finalizacion_real_ejecutada: Optional[date] = None
    
    # Características metodológicas de la atención integral
    tipo_abordaje_atencion_integral: TipoAbordajeAtencionIntegralSalud
    nivel_complejidad_atencion_integral: NivelComplejidadAtencionIntegralSalud
    
    # Contexto integral multidimensional (Art. 1367)
    contexto_dinamicas_familiares: Optional[Dict[str, Any]] = None  # JSONB con dinámicas del núcleo familiar
    contexto_social_comunitario_territorial: Optional[Dict[str, Any]] = None  # JSONB con contexto social y territorial
    entornos_salud_publica_involucrados: Optional[List[UUID]] = None  # IDs de entornos de salud pública
    
    # Valoración y diagnóstico integral inicial
    motivo_consulta_atencion_integral: Optional[str] = None
    problemas_salud_identificados_priorizados: Optional[Dict[str, Any]] = None  # JSONB con problemas de salud identificados
    necesidades_salud_priorizadas_identificadas: Optional[List[str]] = None
    
    # Enfoque de riesgo integral y determinantes sociales
    factores_riesgo_salud_identificados: Optional[Dict[str, Any]] = None  # JSONB con factores de riesgo en salud
    factores_protectores_salud_identificados: Optional[Dict[str, Any]] = None  # JSONB con factores protectores en salud
    vulnerabilidades_sociales_sanitarias: Optional[Dict[str, Any]] = None  # JSONB con vulnerabilidades socio-sanitarias
    
    # Plan de atención integral estructurado
    objetivos_atencion_integral_especificos: Optional[List[str]] = None
    intervenciones_salud_programadas_planificadas: Optional[Dict[str, Any]] = None  # JSONB con intervenciones planificadas
    profesionales_equipo_interdisciplinario: Optional[List[UUID]] = None  # IDs de profesionales del equipo
    instituciones_salud_involucradas: Optional[List[str]] = None
    
    # Coordinación y articulación intersectorial
    profesional_coordinador_caso_responsable: Optional[UUID] = None  # ID del profesional coordinador principal
    plan_coordinacion_intersectorial: Optional[Dict[str, Any]] = None  # JSONB con estrategias de coordinación
    reuniones_equipo_interdisciplinario: Optional[List[Dict[str, Any]]] = None  # JSONB con registro de reuniones
    
    # Resultados esperados e indicadores de impacto
    indicadores_seguimiento_evaluacion: Optional[Dict[str, Any]] = None  # JSONB con indicadores de proceso y resultado
    metas_salud_corto_plazo_trimestre: Optional[List[str]] = None
    metas_salud_mediano_plazo_ano: Optional[List[str]] = None
    metas_salud_largo_plazo_plurianual: Optional[List[str]] = None
    
    # Estado y seguimiento continuo
    estado_actual_atencion_integral: str = "ATENCION_ACTIVA_VIGENTE"  # ATENCION_ACTIVA_VIGENTE, ATENCION_SUSPENDIDA_TEMPORAL, ATENCION_COMPLETADA_FINALIZADA, ATENCION_CANCELADA_TERMINADA
    porcentaje_cumplimiento_objetivos: Optional[int] = None  # Escala 0-100 porcentaje
    fecha_ultima_evaluacion_seguimiento: Optional[date] = None
    fecha_proxima_evaluacion_programada: Optional[date] = None
    
    # Metadatos de registro y auditoria
    atencion_integral_activa: bool = True
    fecha_hora_creacion_atencion_integral: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_atencion: Optional[datetime] = None
    profesional_creador_atencion_integral_id: Optional[UUID] = None

class ComponenteAtencionIntegralEspecializada(BaseModel):
    """
    Componentes especializados que conforman la atención integral de salud
    Vincula las atenciones específicas con el plan de atención integral transversal
    """
    id: Optional[UUID] = None
    atencion_integral_principal_id: UUID  # ID de la atención integral principal
    
    # Vinculación con atenciones especializadas específicas
    atencion_especializada_especifica_id: Optional[UUID] = None  # ID de atención especializada
    tipo_atencion_especializada: str  # "atencion_primera_infancia", "atencion_materno_perinatal", "atencion_cronicidad_control", etc.
    
    # Características del componente especializado
    nombre_descriptivo_componente: str
    descripcion_detallada_componente: Optional[str] = None
    momento_curso_vida_aplicable: Optional[str] = None  # Momento del curso de vida si aplica
    
    # Planificación del componente
    fecha_programada_componente: Optional[date] = None
    nivel_prioridad_componente: Optional[str] = None  # "prioridad_alta_urgente", "prioridad_media_importante", "prioridad_baja_rutinaria"
    componente_urgente_inmediato: bool = False
    
    # Ejecución del componente
    fecha_realizacion_ejecucion_componente: Optional[date] = None
    profesional_responsable_ejecucion: Optional[UUID] = None
    duracion_minutos_ejecucion: Optional[int] = None
    modalidad_atencion_componente: Optional[str] = None  # "atencion_presencial_consultorio", "atencion_virtual_telematica", "atencion_domiciliaria_hogar"
    
    # Resultados específicos del componente
    objetivos_componente_especificos: Optional[List[str]] = None
    resultados_salud_obtenidos_componente: Optional[Dict[str, Any]] = None  # JSONB con resultados del componente
    observaciones_clinicas_componente: Optional[str] = None
    
    # Articulación con otros componentes especializados
    componentes_relacionados_articulados: Optional[List[UUID]] = None  # IDs de otros componentes relacionados
    requiere_seguimiento_posterior: Optional[bool] = False
    fecha_seguimiento_programado: Optional[date] = None
    
    # Estado del componente
    estado_actual_componente: str = "COMPONENTE_PROGRAMADO_PENDIENTE"  # COMPONENTE_PROGRAMADO_PENDIENTE, COMPONENTE_EN_EJECUCION_ACTIVO, COMPONENTE_COMPLETADO_FINALIZADO, COMPONENTE_CANCELADO_SUSPENDIDO
    componente_activo_vigente: bool = True
    fecha_hora_creacion_componente: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_componente: Optional[datetime] = None

class EvaluacionIntegralSeguimientoSalud(BaseModel):
    """
    Evaluaciones periódicas integrales de seguimiento en salud
    Para monitoreo del progreso y ajuste de intervenciones de salud
    """
    id: Optional[UUID] = None
    atencion_integral_evaluada_id: UUID  # ID de la atención integral a evaluar
    
    # Información de la evaluación integral
    fecha_evaluacion_integral: date
    tipo_evaluacion_seguimiento: str  # "evaluacion_inicial_basal", "evaluacion_seguimiento_periodico", "evaluacion_final_cierre", "evaluacion_extraordinaria_especial"
    profesional_responsable_evaluacion: UUID  # ID del profesional evaluador
    
    # Evaluación del progreso y avances
    avance_objetivos_atencion_integral: Optional[Dict[str, Any]] = None  # JSONB con progreso de objetivos
    indicadores_cumplimiento_metas: Optional[Dict[str, Any]] = None  # JSONB con indicadores de cumplimiento
    cambios_salud_observados: Optional[str] = None
    
    # Evaluación de componentes
    componentes_evaluados: Optional[List[UUID]] = None  # IDs de componentes
    efectividad_componentes: Optional[Dict[str, Any]] = None  # JSONB
    
    # Evaluación del contexto
    cambios_contexto_familiar: Optional[str] = None
    cambios_contexto_comunitario: Optional[str] = None
    nuevos_factores_riesgo: Optional[Dict[str, Any]] = None  # JSONB
    
    # Satisfacción y percepción
    satisfaccion_paciente: Optional[int] = None  # Escala 1-5
    satisfaccion_familia: Optional[int] = None  # Escala 1-5
    percepcion_cambios: Optional[str] = None
    
    # Recomendaciones y ajustes
    recomendaciones: Optional[str] = None
    ajustes_plan: Optional[Dict[str, Any]] = None  # JSONB
    nuevos_componentes_sugeridos: Optional[List[str]] = None
    componentes_suspender: Optional[List[UUID]] = None
    
    # Próximos pasos
    proxima_evaluacion: Optional[date] = None
    acciones_inmediatas: Optional[List[str]] = None
    
    # Metadatos
    activo: bool = True
    creado_en: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class VistaConsolidadaAtencionTransversalIntegral(BaseModel):
    """
    Vista consolidada para análisis transversal integral de atención en salud
    Modelo para respuestas API que integran información multidimensional de salud
    """
    # Información básica del paciente
    paciente_persona_id: UUID
    nombre_completo_paciente_persona: Optional[str] = None
    documento_identificacion_paciente: Optional[str] = None
    edad_anos_actual: Optional[int] = None
    momento_curso_vida_actual: Optional[str] = None
    
    # Información familiar
    familia_id: Optional[UUID] = None
    tipo_familia: Optional[str] = None
    funcionamiento_familiar: Optional[str] = None
    
    # Entornos activos
    entornos_paciente: Optional[List[Dict[str, Any]]] = None  # Lista de entornos
    
    # Atenciones recibidas (últimos 12 meses)
    atenciones_primera_infancia: Optional[List[Dict[str, Any]]] = None
    atenciones_materno_perinatal: Optional[List[Dict[str, Any]]] = None
    atenciones_cronicidad: Optional[List[Dict[str, Any]]] = None
    intervenciones_colectivas: Optional[List[Dict[str, Any]]] = None
    
    # Atención integral actual
    atencion_integral_activa: Optional[Dict[str, Any]] = None
    componentes_activos: Optional[List[Dict[str, Any]]] = None
    
    # Indicadores transversales
    riesgos_identificados: Optional[Dict[str, Any]] = None
    factores_proteccion: Optional[Dict[str, Any]] = None
    adherencia_tratamientos: Optional[Dict[str, Any]] = None
    
    # Última actualización
    ultima_atencion: Optional[datetime] = None
    proxima_cita_programada: Optional[datetime] = None