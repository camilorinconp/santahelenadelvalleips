# =============================================================================
# Modelo Atención Vejez - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 17 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
# Resolución 202 de 2021 - Variables 16-17 (Test Vejez)
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# =============================================================================
# ENUMS ESPECÍFICOS PARA VEJEZ (60+ AÑOS)
# =============================================================================

class EstadoFuncionalVejez(str, Enum):
    """Estado funcional según escalas geriátricas"""
    INDEPENDIENTE = "INDEPENDIENTE"                    # Katz 6-5, Lawton 8
    DEPENDENCIA_LEVE = "DEPENDENCIA_LEVE"             # Katz 4, Lawton 6-7
    DEPENDENCIA_MODERADA = "DEPENDENCIA_MODERADA"     # Katz 2-3, Lawton 4-5
    DEPENDENCIA_SEVERA = "DEPENDENCIA_SEVERA"         # Katz 0-1, Lawton 0-3
    EVALUACION_REQUERIDA = "EVALUACION_REQUERIDA"

class EstadoCognitivoVejez(str, Enum):
    """Estado cognitivo según Mini Mental State Examination - Resolución 202"""
    NORMAL = "NORMAL"                                  # >24 puntos
    DETERIORO_LEVE = "DETERIORO_LEVE"                 # 18-24 puntos
    DETERIORO_MODERADO = "DETERIORO_MODERADO"         # 12-17 puntos
    DETERIORO_SEVERO = "DETERIORO_SEVERO"             # <12 puntos
    SOSPECHA_DETERIORO = "SOSPECHA_DETERIORO"         # Variables de alerta
    RIESGO_NO_EVALUADO = "RIESGO_NO_EVALUADO"         # Código 21 PEDT

class SindromeFragilidad(str, Enum):
    """Síndrome de fragilidad según criterios Fried"""
    ROBUSTO = "ROBUSTO"                               # 0 criterios
    PRE_FRAGIL = "PRE_FRAGIL"                         # 1-2 criterios
    FRAGIL = "FRAGIL"                                 # 3-5 criterios
    FRAGILIDAD_SEVERA = "FRAGILIDAD_SEVERA"           # >5 criterios + comorbilidad

class RiesgoNutricionalVejez(str, Enum):
    """Riesgo nutricional en adultos mayores"""
    NORMAL = "NORMAL"
    RIESGO_BAJO = "RIESGO_BAJO"
    RIESGO_MODERADO = "RIESGO_MODERADO"
    RIESGO_ALTO = "RIESGO_ALTO"
    DESNUTRICION = "DESNUTRICION"

class RiesgoCaidaVejez(str, Enum):
    """Riesgo de caídas específico para vejez"""
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    MUY_ALTO = "MUY_ALTO"

class SaludMentalVejez(str, Enum):
    """Evaluación salud mental específica para vejez"""
    NORMAL = "NORMAL"
    DEPRESION_LEVE = "DEPRESION_LEVE"
    DEPRESION_MODERADA = "DEPRESION_MODERADA"
    DEPRESION_SEVERA = "DEPRESION_SEVERA"
    ANSIEDAD = "ANSIEDAD"
    DETERIORO_COGNITIVO_ASOCIADO = "DETERIORO_COGNITIVO_ASOCIADO"

class CalidadVidaVejez(str, Enum):
    """Calidad de vida específica para adultos mayores"""
    EXCELENTE = "EXCELENTE"
    BUENA = "BUENA"
    REGULAR = "REGULAR"
    DEFICIENTE = "DEFICIENTE"
    CRITICA = "CRITICA"

class NivelApoyoSocial(str, Enum):
    """Nivel de apoyo social y familiar"""
    APOYO_FAMILIAR_FUERTE = "APOYO_FAMILIAR_FUERTE"
    APOYO_MODERADO = "APOYO_MODERADO"
    APOYO_LIMITADO = "APOYO_LIMITADO"
    AISLAMIENTO_SOCIAL = "AISLAMIENTO_SOCIAL"
    ABANDONO = "ABANDONO"

class RiesgoMaltrato(str, Enum):
    """Detección riesgo de maltrato en adultos mayores"""
    SIN_RIESGO = "SIN_RIESGO"
    INDICADORES_LEVES = "INDICADORES_LEVES"
    INDICADORES_MODERADOS = "INDICADORES_MODERADOS"
    ALTO_RIESGO = "ALTO_RIESGO"
    SITUACION_CONFIRMADA = "SITUACION_CONFIRMADA"

class PlanificacionCuidadosPaliativos(str, Enum):
    """Planificación de cuidados paliativos"""
    NO_REQUIERE = "NO_REQUIERE"
    ORIENTACION_INICIAL = "ORIENTACION_INICIAL"
    EVALUACION_ESPECIALIZADA = "EVALUACION_ESPECIALIZADA"
    CUIDADOS_PALIATIVOS_ACTIVOS = "CUIDADOS_PALIATIVOS_ACTIVOS"
    CUIDADOS_TERMINALES = "CUIDADOS_TERMINALES"

# =============================================================================
# FUNCIONES CALCULADAS AUTOMÁTICAS
# =============================================================================

def calcular_indice_katz(
    banarse: bool,
    vestirse: bool,
    usar_inodoro: bool,
    movilizarse: bool,
    continencia: bool,
    alimentarse: bool
) -> int:
    """Calcula índice de Katz (0-6) para actividades básicas de la vida diaria"""
    actividades = [banarse, vestirse, usar_inodoro, movilizarse, continencia, alimentarse]
    return sum(1 for actividad in actividades if actividad)

def calcular_escala_lawton_brody(
    usar_telefono: int,
    hacer_compras: int,
    preparar_comida: int,
    cuidar_casa: int,
    lavar_ropa: int,
    usar_transporte: int,
    manejar_medicamentos: int,
    manejar_dinero: int
) -> int:
    """Calcula escala de Lawton-Brody (0-8) para actividades instrumentales"""
    return usar_telefono + hacer_compras + preparar_comida + cuidar_casa + \
           lavar_ropa + usar_transporte + manejar_medicamentos + manejar_dinero

def calcular_riesgo_fragilidad(
    perdida_peso_no_intencionada: bool,
    agotamiento: bool,
    debilidad_fuerza_prension: bool,
    lentitud_marcha: bool,
    baja_actividad_fisica: bool
) -> SindromeFragilidad:
    """Calcula síndrome de fragilidad según criterios de Fried"""
    criterios = sum([
        perdida_peso_no_intencionada,
        agotamiento,
        debilidad_fuerza_prension,
        lentitud_marcha,
        baja_actividad_fisica
    ])

    if criterios == 0:
        return SindromeFragilidad.ROBUSTO
    elif criterios <= 2:
        return SindromeFragilidad.PRE_FRAGIL
    elif criterios <= 5:
        return SindromeFragilidad.FRAGIL
    else:
        return SindromeFragilidad.FRAGILIDAD_SEVERA

def interpretar_mini_mental(puntaje_mini_mental: int) -> EstadoCognitivoVejez:
    """Interpreta puntaje Mini Mental State Examination según normativas"""
    if puntaje_mini_mental > 24:
        return EstadoCognitivoVejez.NORMAL
    elif 18 <= puntaje_mini_mental <= 24:
        return EstadoCognitivoVejez.DETERIORO_LEVE
    elif 12 <= puntaje_mini_mental <= 17:
        return EstadoCognitivoVejez.DETERIORO_MODERADO
    elif puntaje_mini_mental < 12:
        return EstadoCognitivoVejez.DETERIORO_SEVERO
    else:
        return EstadoCognitivoVejez.RIESGO_NO_EVALUADO

def generar_alertas_vejez(
    estado_funcional: EstadoFuncionalVejez,
    estado_cognitivo: EstadoCognitivoVejez,
    sindrome_fragilidad: SindromeFragilidad,
    riesgo_caida: RiesgoCaidaVejez,
    riesgo_maltrato: RiesgoMaltrato
) -> List[str]:
    """Genera alertas automáticas basadas en evaluación geriátrica integral"""
    alertas = []

    # Alertas funcionalidad
    if estado_funcional in [EstadoFuncionalVejez.DEPENDENCIA_SEVERA]:
        alertas.append("ALERTA CRÍTICA: Dependencia funcional severa requiere evaluación geriátrica urgente")
    elif estado_funcional in [EstadoFuncionalVejez.DEPENDENCIA_MODERADA]:
        alertas.append("ALERTA: Dependencia moderada requiere plan de rehabilitación")

    # Alertas cognitivas
    if estado_cognitivo in [EstadoCognitivoVejez.DETERIORO_SEVERO]:
        alertas.append("ALERTA CRÍTICA: Deterioro cognitivo severo requiere evaluación neurológica")
    elif estado_cognitivo in [EstadoCognitivoVejez.SOSPECHA_DETERIORO]:
        alertas.append("ALERTA: Sospecha deterioro cognitivo - aplicar Mini Mental State")

    # Alertas fragilidad
    if sindrome_fragilidad == SindromeFragilidad.FRAGIL:
        alertas.append("ALERTA: Síndrome de fragilidad confirmado - iniciar intervenciones")
    elif sindrome_fragilidad == SindromeFragilidad.FRAGILIDAD_SEVERA:
        alertas.append("ALERTA CRÍTICA: Fragilidad severa requiere cuidados especializados")

    # Alertas caídas
    if riesgo_caida == RiesgoCaidaVejez.MUY_ALTO:
        alertas.append("ALERTA CRÍTICA: Riesgo muy alto de caídas - implementar medidas preventivas inmediatas")
    elif riesgo_caida == RiesgoCaidaVejez.ALTO:
        alertas.append("ALERTA: Alto riesgo de caídas - evaluar entorno domiciliario")

    # Alertas maltrato
    if riesgo_maltrato in [RiesgoMaltrato.SITUACION_CONFIRMADA, RiesgoMaltrato.ALTO_RIESGO]:
        alertas.append("ALERTA CRÍTICA: Riesgo de maltrato detectado - activar protocolo de protección")

    return alertas

# =============================================================================
# MODELOS PYDANTIC PARA VEJEZ
# =============================================================================

class AtencionVejezCrear(BaseModel):
    """Modelo para crear nueva atención de vejez"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # Referencias obligatorias
    paciente_id: UUID = Field(..., description="ID del paciente (60+ años)")
    medico_id: UUID = Field(..., description="ID del médico tratante")
    fecha_atencion: date = Field(..., description="Fecha de la atención geriátrica")

    # === VALORACIÓN GERIÁTRICA INTEGRAL ===

    # Evaluación Funcional - Actividades Básicas Vida Diaria (Katz)
    katz_banarse: bool = Field(False, description="Independiente para bañarse")
    katz_vestirse: bool = Field(False, description="Independiente para vestirse")
    katz_usar_inodoro: bool = Field(False, description="Independiente para usar inodoro")
    katz_movilizarse: bool = Field(False, description="Independiente para movilizarse")
    katz_continencia: bool = Field(False, description="Continente")
    katz_alimentarse: bool = Field(False, description="Independiente para alimentarse")

    # Actividades Instrumentales Vida Diaria (Lawton-Brody)
    lawton_usar_telefono: int = Field(0, ge=0, le=1, description="Usar teléfono (0-1)")
    lawton_hacer_compras: int = Field(0, ge=0, le=1, description="Hacer compras (0-1)")
    lawton_preparar_comida: int = Field(0, ge=0, le=1, description="Preparar comida (0-1)")
    lawton_cuidar_casa: int = Field(0, ge=0, le=1, description="Cuidar casa (0-1)")
    lawton_lavar_ropa: int = Field(0, ge=0, le=1, description="Lavar ropa (0-1)")
    lawton_usar_transporte: int = Field(0, ge=0, le=1, description="Usar transporte (0-1)")
    lawton_manejar_medicamentos: int = Field(0, ge=0, le=1, description="Manejar medicamentos (0-1)")
    lawton_manejar_dinero: int = Field(0, ge=0, le=1, description="Manejar dinero (0-1)")

    # === EVALUACIÓN COGNITIVA ===

    # Mini Mental State Examination (Obligatorio Resolución 202)
    mini_mental_aplicado: bool = Field(False, description="Se aplicó Mini Mental State")
    mini_mental_puntaje: Optional[int] = Field(None, ge=0, le=30, description="Puntaje Mini Mental (0-30)")
    orientacion_temporal: Optional[int] = Field(None, ge=0, le=5, description="Orientación temporal (0-5)")
    orientacion_espacial: Optional[int] = Field(None, ge=0, le=5, description="Orientación espacial (0-5)")
    memoria_inmediata: Optional[int] = Field(None, ge=0, le=3, description="Memoria inmediata (0-3)")
    atencion_calculo: Optional[int] = Field(None, ge=0, le=5, description="Atención y cálculo (0-5)")
    memoria_diferida: Optional[int] = Field(None, ge=0, le=3, description="Memoria diferida (0-3)")
    lenguaje_construccion: Optional[int] = Field(None, ge=0, le=9, description="Lenguaje y construcción (0-9)")

    # === SÍNDROME DE FRAGILIDAD (Criterios de Fried) ===

    fragilidad_perdida_peso: bool = Field(False, description="Pérdida involuntaria >4.5kg en último año")
    fragilidad_agotamiento: bool = Field(False, description="Sensación de agotamiento ≥3 días/semana")
    fragilidad_debilidad: bool = Field(False, description="Fuerza de prensión disminuida")
    fragilidad_lentitud: bool = Field(False, description="Velocidad de marcha <0.8 m/s")
    fragilidad_actividad_baja: bool = Field(False, description="Actividad física <383 kcal/semana")

    # === EVALUACIÓN NUTRICIONAL ESPECÍFICA ===

    peso_actual: Optional[float] = Field(None, ge=30, le=200, description="Peso actual en kg")
    talla: Optional[float] = Field(None, ge=1.0, le=2.5, description="Talla en metros")
    circunferencia_pantorrilla: Optional[float] = Field(None, ge=20, le=50, description="Circunferencia pantorrilla cm")
    albumina_serica: Optional[float] = Field(None, ge=1.0, le=6.0, description="Albúmina sérica g/dL")
    perdida_apetito: bool = Field(False, description="Pérdida de apetito significativa")
    dificultad_masticacion: bool = Field(False, description="Dificultad para masticar")
    dificultad_deglucion: bool = Field(False, description="Dificultad para deglutir")

    # === EVALUACIÓN RIESGO DE CAÍDAS ===

    caidas_ultimo_ano: int = Field(0, ge=0, description="Número de caídas en último año")
    miedo_caerse: bool = Field(False, description="Miedo a caerse")
    uso_ayudas_tecnicas: bool = Field(False, description="Uso de bastón, andador, etc.")
    medicamentos_riesgo: int = Field(0, ge=0, description="Número medicamentos que incrementan riesgo caídas")
    alteraciones_vision: bool = Field(False, description="Alteraciones visuales")
    alteraciones_auditivas: bool = Field(False, description="Alteraciones auditivas")
    hipotension_ortostatica: bool = Field(False, description="Hipotensión ortostática")

    # === SALUD MENTAL Y SOCIAL ===

    # Depresión (GDS-15 - Geriatric Depression Scale)
    gds_aplicada: bool = Field(False, description="Se aplicó Escala Depresión Geriátrica")
    gds_puntaje: Optional[int] = Field(None, ge=0, le=15, description="Puntaje GDS-15 (0-15)")
    sintomas_depresivos: bool = Field(False, description="Presenta síntomas depresivos")
    aislamiento_social: bool = Field(False, description="Presenta aislamiento social")
    duelo_reciente: bool = Field(False, description="Duelo reciente (último año)")

    # Apoyo Social y Familiar
    vive_solo: bool = Field(False, description="Vive solo")
    cuidador_principal: Optional[str] = Field(None, max_length=100, description="Cuidador principal")
    red_apoyo_familiar: NivelApoyoSocial = Field(NivelApoyoSocial.APOYO_MODERADO, description="Nivel apoyo familiar")
    acceso_servicios_salud: bool = Field(True, description="Tiene acceso a servicios de salud")

    # === DETECCIÓN MALTRATO ADULTO MAYOR ===

    indicadores_maltrato_fisico: bool = Field(False, description="Indicadores maltrato físico")
    indicadores_maltrato_psicologico: bool = Field(False, description="Indicadores maltrato psicológico")
    indicadores_negligencia: bool = Field(False, description="Indicadores negligencia")
    indicadores_abandono: bool = Field(False, description="Indicadores abandono")
    indicadores_abuso_financiero: bool = Field(False, description="Indicadores abuso financiero")

    # === COMORBILIDADES Y MEDICAMENTOS ===

    numero_comorbilidades: int = Field(0, ge=0, le=20, description="Número de enfermedades crónicas")
    numero_medicamentos: int = Field(0, ge=0, le=30, description="Número total de medicamentos")
    polifarmacia: bool = Field(False, description="Polifarmacia (≥5 medicamentos)")
    medicamentos_potencialmente_inadecuados: int = Field(0, ge=0, description="Medicamentos potencialmente inadecuados")

    # === TAMIZAJES ESPECÍFICOS VEJEZ ===

    # Tamizaje Oncológico Específico
    ultimo_mamografia: Optional[date] = Field(None, description="Fecha última mamografía")
    ultimo_citologia: Optional[date] = Field(None, description="Fecha última citología")
    ultimo_colonoscopia: Optional[date] = Field(None, description="Fecha última colonoscopia")
    ultimo_psa: Optional[date] = Field(None, description="Fecha último PSA (hombres)")

    # Laboratorios Geriátricos
    hemoglobina: Optional[float] = Field(None, ge=5.0, le=20.0, description="Hemoglobina g/dL")
    creatinina: Optional[float] = Field(None, ge=0.3, le=10.0, description="Creatinina mg/dL")
    glicemia_ayunas: Optional[float] = Field(None, ge=50, le=500, description="Glicemia ayunas mg/dL")
    colesterol_total: Optional[float] = Field(None, ge=100, le=400, description="Colesterol total mg/dL")
    vitamina_b12: Optional[float] = Field(None, ge=100, le=2000, description="Vitamina B12 pg/mL")
    vitamina_d: Optional[float] = Field(None, ge=10, le=100, description="Vitamina D ng/mL")
    tsh: Optional[float] = Field(None, ge=0.1, le=20.0, description="TSH mUI/L")

    # === PLANIFICACIÓN CUIDADOS ===

    # Cuidados Paliativos
    requiere_cuidados_paliativos: bool = Field(False, description="Requiere evaluación cuidados paliativos")
    directivas_anticipadas: bool = Field(False, description="Tiene directivas anticipadas")
    planificacion_cuidados_establecida: bool = Field(False, description="Plan de cuidados establecido")

    # Rehabilitación
    requiere_fisioterapia: bool = Field(False, description="Requiere fisioterapia")
    requiere_terapia_ocupacional: bool = Field(False, description="Requiere terapia ocupacional")
    requiere_fonoaudiologia: bool = Field(False, description="Requiere fonoaudiología")

    # Observaciones y Narrativa
    observaciones_generales: Optional[str] = Field(None, max_length=2000, description="Observaciones generales")
    plan_intervencion: Optional[str] = Field(None, max_length=1500, description="Plan de intervención")
    recomendaciones_familia: Optional[str] = Field(None, max_length=1000, description="Recomendaciones a la familia")

class AtencionVejezActualizar(BaseModel):
    """Modelo para actualizar atención de vejez (campos opcionales)"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # Solo campos que pueden ser actualizados (excluir campos de auditoría)
    fecha_atencion: Optional[date] = None

    # Funcionalidad
    katz_banarse: Optional[bool] = None
    katz_vestirse: Optional[bool] = None
    katz_usar_inodoro: Optional[bool] = None
    katz_movilizarse: Optional[bool] = None
    katz_continencia: Optional[bool] = None
    katz_alimentarse: Optional[bool] = None

    # Actividades instrumentales
    lawton_usar_telefono: Optional[int] = Field(None, ge=0, le=1)
    lawton_hacer_compras: Optional[int] = Field(None, ge=0, le=1)
    lawton_preparar_comida: Optional[int] = Field(None, ge=0, le=1)
    lawton_cuidar_casa: Optional[int] = Field(None, ge=0, le=1)
    lawton_lavar_ropa: Optional[int] = Field(None, ge=0, le=1)
    lawton_usar_transporte: Optional[int] = Field(None, ge=0, le=1)
    lawton_manejar_medicamentos: Optional[int] = Field(None, ge=0, le=1)
    lawton_manejar_dinero: Optional[int] = Field(None, ge=0, le=1)

    # Evaluación cognitiva
    mini_mental_aplicado: Optional[bool] = None
    mini_mental_puntaje: Optional[int] = Field(None, ge=0, le=30)

    # Fragilidad
    fragilidad_perdida_peso: Optional[bool] = None
    fragilidad_agotamiento: Optional[bool] = None
    fragilidad_debilidad: Optional[bool] = None
    fragilidad_lentitud: Optional[bool] = None
    fragilidad_actividad_baja: Optional[bool] = None

    # Observaciones
    observaciones_generales: Optional[str] = Field(None, max_length=2000)
    plan_intervencion: Optional[str] = Field(None, max_length=1500)

class AtencionVejezResponse(BaseModel):
    """Modelo de respuesta con campos calculados automáticamente"""
    model_config = ConfigDict(from_attributes=True)

    # Datos básicos
    id: UUID
    paciente_id: UUID
    medico_id: UUID
    fecha_atencion: date

    # Todos los campos de entrada
    katz_banarse: bool
    katz_vestirse: bool
    katz_usar_inodoro: bool
    katz_movilizarse: bool
    katz_continencia: bool
    katz_alimentarse: bool

    lawton_usar_telefono: int
    lawton_hacer_compras: int
    lawton_preparar_comida: int
    lawton_cuidar_casa: int
    lawton_lavar_ropa: int
    lawton_usar_transporte: int
    lawton_manejar_medicamentos: int
    lawton_manejar_dinero: int

    mini_mental_aplicado: bool
    mini_mental_puntaje: Optional[int]

    fragilidad_perdida_peso: bool
    fragilidad_agotamiento: bool
    fragilidad_debilidad: bool
    fragilidad_lentitud: bool
    fragilidad_actividad_baja: bool

    peso_actual: Optional[float]
    talla: Optional[float]

    caidas_ultimo_ano: int
    numero_comorbilidades: int
    numero_medicamentos: int

    vive_solo: bool
    red_apoyo_familiar: NivelApoyoSocial

    # === CAMPOS CALCULADOS AUTOMÁTICAMENTE ===

    # Funcionalidad
    indice_katz: int = Field(..., description="Índice Katz (0-6)")
    escala_lawton_brody: int = Field(..., description="Escala Lawton-Brody (0-8)")
    estado_funcional: EstadoFuncionalVejez = Field(..., description="Estado funcional global")

    # Cognición
    estado_cognitivo: EstadoCognitivoVejez = Field(..., description="Estado cognitivo según Mini Mental")

    # Fragilidad
    sindrome_fragilidad: SindromeFragilidad = Field(..., description="Síndrome de fragilidad")

    # Estado nutricional
    imc: Optional[float] = Field(None, description="IMC calculado")
    riesgo_nutricional: RiesgoNutricionalVejez = Field(..., description="Riesgo nutricional")

    # Riesgos específicos
    riesgo_caida: RiesgoCaidaVejez = Field(..., description="Riesgo de caídas")
    riesgo_maltrato: RiesgoMaltrato = Field(..., description="Riesgo de maltrato")

    # Calidad de vida
    calidad_vida: CalidadVidaVejez = Field(..., description="Calidad de vida global")

    # Cuidados
    planificacion_cuidados: PlanificacionCuidadosPaliativos = Field(..., description="Planificación cuidados")

    # Alertas automáticas
    alertas_generadas: List[str] = Field(default_factory=list, description="Alertas generadas automáticamente")

    # Observaciones
    observaciones_generales: Optional[str]
    plan_intervencion: Optional[str]

    # Auditoría
    creado_en: Optional[datetime]
    updated_at: Optional[datetime]

# Configuración del modelo
AtencionVejezCrear.model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
AtencionVejezActualizar.model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
AtencionVejezResponse.model_config = ConfigDict(from_attributes=True)