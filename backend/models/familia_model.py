from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum

class TipoEstructuraFamiliarIntegral(str, Enum):
    """Tipos de estructura familiar para atención integral según lineamientos de salud familiar"""
    FAMILIA_NUCLEAR_TRADICIONAL_COMPLETA = "FAMILIA_NUCLEAR_TRADICIONAL_COMPLETA"  # Padres e hijos biologicos
    FAMILIA_EXTENSA_MULTIGENERACIONAL = "FAMILIA_EXTENSA_MULTIGENERACIONAL"  # Incluye abuelos, tíos, primos
    FAMILIA_MONOPARENTAL_JEFE_UNICO = "FAMILIA_MONOPARENTAL_JEFE_UNICO"  # Un solo padre o madre responsable
    FAMILIA_ENSAMBLADA_RECOMPUESTA = "FAMILIA_ENSAMBLADA_RECOMPUESTA"  # Nuevas parejas con hijos de relaciones previas  
    FAMILIA_HOMOPARENTAL_MISMO_SEXO = "FAMILIA_HOMOPARENTAL_MISMO_SEXO"  # Padres del mismo sexo
    FAMILIA_ADOPTIVA_ACOGIMIENTO = "FAMILIA_ADOPTIVA_ACOGIMIENTO"  # Familia conformada por adopción legal
    FAMILIA_ACOGIDA_TEMPORAL_PROTECCION = "FAMILIA_ACOGIDA_TEMPORAL_PROTECCION"  # Familia de acogida temporal
    HOGAR_UNIPERSONAL_INDIVIDUAL = "HOGAR_UNIPERSONAL_INDIVIDUAL"  # Persona que vive sola

class CicloVitalFamiliarEvolutivo(str, Enum):
    """Ciclo vital familiar evolutivo según lineamientos de desarrollo familiar"""
    ETAPA_FORMACION_PAREJA_INICIAL = "ETAPA_FORMACION_PAREJA_INICIAL"  # Pareja en formación sin hijos
    ETAPA_EXPANSION_LLEGADA_HIJOS = "ETAPA_EXPANSION_LLEGADA_HIJOS"  # Llegada y nacimiento de hijos
    ETAPA_CONSOLIDACION_CRIANZA_EDUCACION = "ETAPA_CONSOLIDACION_CRIANZA_EDUCACION"  # Crianza y educación de hijos
    ETAPA_APERTURA_ADOLESCENCIA_JUVENTUD = "ETAPA_APERTURA_ADOLESCENCIA_JUVENTUD"  # Hijos adolescentes y jóvenes
    ETAPA_CONTRACCION_INDEPENDIZACION_HIJOS = "ETAPA_CONTRACCION_INDEPENDIZACION_HIJOS"  # Salida e independencia de hijos
    ETAPA_DISOLUCION_PAREJA_MADURA = "ETAPA_DISOLUCION_PAREJA_MADURA"  # Pareja mayor en soledad

class ModeloFamiliaIntegralSaludPublica(BaseModel):
    """
    Modelo para gestión familiar integral de salud pública según Resolución 3280 Art. 1364-1370
    'La familia se asuma como sujeto de atención integral en salud'
    """
    id: Optional[UUID] = None
    
    # Identificación y registro familiar
    codigo_identificacion_familiar_unico: Optional[str] = None  # Código único generado para la familia
    nombre_apellidos_familia_completo: Optional[str] = None  # "Familia García Rodríguez", "Familia López-Martínez"
    
    # Características estructurales familiares básicas
    tipo_estructura_familiar: TipoEstructuraFamiliarIntegral
    ciclo_vital_familiar_actual: CicloVitalFamiliarEvolutivo
    numero_total_integrantes_familia: int
    numero_menores_edad_dieciocho_anos: Optional[int] = None
    numero_adultos_mayores_sesenta_anos: Optional[int] = None
    numero_personas_discapacidad_especial: Optional[int] = None
    
    # Ubicación territorial y entorno residencial
    direccion_residencia_principal_completa: Optional[str] = None
    municipio_territorio_residencia: str
    departamento_division_politica: str
    zona_geografica_residencial: Optional[str] = None  # "urbana_ciudad", "rural_campo"
    estrato_socioeconomico_sisben: Optional[int] = None
    
    # Características socioeconómicas familiares
    nivel_ingresos_economicos_familiar: Optional[str] = None  # "bajo_pobreza", "medio_estable", "alto_acomodado"
    fuentes_ingresos_economicos_familia: Optional[Dict[str, Any]] = None  # JSONB con detalle de ingresos
    acceso_servicios_publicos_basicos: Optional[Dict[str, bool]] = None  # agua potable, energia electrica, gas natural, etc.
    tipo_tenencia_vivienda: Optional[str] = None  # "vivienda_propia", "vivienda_arrendada", "vivienda_familiar_cedida"
    condiciones_habitabilidad_vivienda: Optional[Dict[str, Any]] = None  # JSONB con estado físico y sanitario
    
    # Dinámica y funcionamiento familiar integral (Art. 1369)
    evaluacion_dinamica_familiar_general: Optional[str] = None  # Evaluación general de dinámicas
    nivel_funcionamiento_familiar: Optional[str] = None  # "familia_funcional", "familia_disfuncional", "familia_funcionamiento_moderado"
    
    # Instrumentos evaluación y valoración familiar especializada
    puntaje_apgar_familiar_funcionamiento: Optional[int] = None  # Escala valoración 0-20 puntos
    familiograma_estructura_realizado: Optional[bool] = None
    observaciones_familiograma_estructura: Optional[str] = None
    ecomapa_redes_apoyo_realizado: Optional[bool] = None
    observaciones_ecomapa_redes_sociales: Optional[str] = None
    
    # Riesgos y factores protectores en salud familiar
    factores_riesgo_salud_familiar: Optional[Dict[str, Any]] = None  # JSONB con riesgos identificados
    factores_proteccion_salud_familiar: Optional[Dict[str, Any]] = None  # JSONB con elementos protectores
    vulnerabilidades_sociales_identificadas: Optional[Dict[str, Any]] = None  # JSONB con vulnerabilidades socio-sanitarias
    
    # Redes apoyo social y comunitario familiar
    redes_apoyo_social_familiar: Optional[Dict[str, Any]] = None  # JSONB con redes de soporte
    participacion_actividades_comunitarias: Optional[Dict[str, Any]] = None  # JSONB con participación social
    
    # Estado de salud y estilos de vida familiares
    problemas_salud_prevalentes_familia: Optional[Dict[str, Any]] = None  # JSONB con patologías frecuentes
    habitos_estilos_vida_saludables: Optional[Dict[str, Any]] = None  # JSONB con prácticas de salud
    
    # Estado seguimiento y priorización familiar
    fecha_caracterizacion_inicial_familia: Optional[date] = None
    fecha_ultima_actualizacion_registro: Optional[date] = None
    requiere_seguimiento_especial: Optional[bool] = False
    nivel_prioridad_atencion_familiar: Optional[str] = None  # "prioridad_alta_urgente", "prioridad_media_importante", "prioridad_baja_rutinaria"
    
    # Metadatos registro y auditoria familiar
    registro_familiar_activo: bool = True
    fecha_hora_creacion_registro_familia: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_familia: Optional[datetime] = None
    profesional_responsable_caracterizacion_id: Optional[UUID] = None  # ID del profesional caracterizador

class RelacionIntegranteFamiliaCompleta(BaseModel):
    """
    Relación integral entre pacientes individuales y núcleo familiar
    Un paciente puede cambiar de familia por adopción, matrimonio, migración, etc.
    """
    id: Optional[UUID] = None
    familia_nucleo_id: UUID  # ID del núcleo familiar
    paciente_integrante_id: UUID  # ID del paciente que integra la familia
    
    # Rol y función en el núcleo familiar
    tipo_parentesco_familiar: str  # "padre_biologico", "madre_biologica", "hijo_hija", "abuelo_abuela", "tio_tia", etc.
    es_jefe_cabeza_hogar: bool = False
    es_cuidador_principal_familia: bool = False
    es_responsable_economico_principal: bool = False
    
    # Período temporal de pertenencia familiar
    fecha_ingreso_integracion_familia: Optional[date] = None
    fecha_salida_desvinculacion_familia: Optional[date] = None
    motivo_razon_salida_familia: Optional[str] = None
    
    # Características socioeconomicas del integrante
    aporta_ingresos_economicos_familia: Optional[bool] = None
    nivel_educativo_academico: Optional[str] = None
    ocupacion_laboral_actual: Optional[str] = None
    
    # Estado de salud individual en contexto familiar
    condiciones_salud_relevantes_integrante: Optional[Dict[str, Any]] = None  # JSONB con patologías del integrante
    medicamentos_tratamientos_regulares: Optional[List[str]] = None
    requiere_cuidado_especial_permanente: Optional[bool] = False
    
    # Relaciones interpersonales familiares
    relacion_dinamicas_otros_integrantes: Optional[Dict[str, Any]] = None  # JSONB con dinámicas relacionales
    
    # Estado de la relación familiar
    relacion_familiar_activa: bool = True
    fecha_hora_creacion_relacion_familiar: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_relacion: Optional[datetime] = None

class IntervencionSaludFamiliarIntegral(BaseModel):
    """
    Intervenciones de salud dirigidas integralmente a la familia como unidad de atención
    Art. 1364: 'familia se asuma como sujeto de atención integral en salud'
    """
    id: Optional[UUID] = None
    familia_objetivo_intervencion_id: UUID  # ID de la familia objetivo
    
    # Tipo de intervención de salud familiar
    tipo_intervencion_salud_familiar: str  # "intervencion_educativa_formativa", "intervencion_terapeutica_clinica", "intervencion_social_comunitaria", "intervencion_economica_material"
    nombre_descriptivo_intervencion_familiar: str
    objetivo_intervencion_salud_familiar: Optional[str] = None
    descripcion_detallada_intervencion: Optional[str] = None
    
    # Planificación de la intervención familiar
    fecha_programada_intervencion_familiar: Optional[date] = None
    duracion_estimada_minutos_intervencion: Optional[int] = None
    modalidad_atencion_familiar: Optional[str] = None  # "atencion_presencial_consultorio", "atencion_virtual_telematica", "atencion_domiciliaria_hogar"
    
    # Ejecución de la intervención familiar
    fecha_realizacion_intervencion_familiar: Optional[date] = None
    duracion_real_ejecutada_minutos: Optional[int] = None
    integrantes_familiares_participantes: Optional[List[UUID]] = None  # IDs de pacientes familiares
    profesionales_equipo_participante: Optional[List[UUID]] = None  # IDs de profesionales del equipo
    
    # Desarrollo metodológico de la intervención familiar
    metodologia_pedagogica_utilizada: Optional[str] = None
    temas_salud_familiar_abordados: Optional[List[str]] = None
    actividades_educativas_realizadas: Optional[str] = None
    
    # Resultados y logros de la intervención familiar
    objetivos_salud_familiar_logrados: Optional[Dict[str, Any]] = None  # JSONB con metas alcanzadas
    cambios_comportamiento_familiar_observados: Optional[str] = None
    nivel_satisfaccion_familia_intervencion: Optional[int] = None  # Escala evaluación 1-5
    compromisos_acordados_familia: Optional[List[str]] = None
    
    # Seguimiento continuo de la intervención familiar
    requiere_seguimiento_posterior: Optional[bool] = False
    fecha_proxima_intervencion_familiar: Optional[date] = None
    recomendaciones_salud_familia: Optional[str] = None
    
    # Estado de la intervención familiar
    estado_actual_intervencion_familiar: str = "INTERVENCION_PROGRAMADA_PENDIENTE"  # INTERVENCION_PROGRAMADA_PENDIENTE, INTERVENCION_REALIZADA_COMPLETADA, INTERVENCION_CANCELADA_SUSPENDIDA, INTERVENCION_REPROGRAMADA_DIFERIDA
    intervencion_familiar_activa: bool = True
    fecha_hora_creacion_intervencion_familiar: Optional[datetime] = None
    fecha_hora_ultima_actualizacion_intervencion: Optional[datetime] = None
    profesional_responsable_intervencion_familiar_id: Optional[UUID] = None  # ID del profesional responsable