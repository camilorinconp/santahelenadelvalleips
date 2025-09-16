# =============================================================================
# Modelo Atención Infancia - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# =============================================================================
# ENUMS ESPECÍFICOS PARA INFANCIA
# =============================================================================

class EstadoNutricionalInfancia(str, Enum):
    """Estado nutricional para niños de 6-11 años"""
    NORMAL = "NORMAL"
    DELGADEZ = "DELGADEZ"
    SOBREPESO = "SOBREPESO"
    OBESIDAD = "OBESIDAD"
    TALLA_BAJA = "TALLA_BAJA"

class DesempenoEscolar(str, Enum):
    """Evaluación del desempeño escolar"""
    SUPERIOR = "SUPERIOR"
    ALTO = "ALTO"
    BASICO = "BASICO"
    BAJO = "BAJO"
    NO_ESCOLARIZADO = "NO_ESCOLARIZADO"

class ResultadoTamizaje(str, Enum):
    """Resultado de tamizajes específicos"""
    NORMAL = "NORMAL"
    ALTERADO = "ALTERADO"
    REQUIERE_EVALUACION = "REQUIERE_EVALUACION"
    NO_REALIZADO = "NO_REALIZADO"

class FactorRiesgo(str, Enum):
    """Factores de riesgo identificados en infancia"""
    SEDENTARISMO = "SEDENTARISMO"
    ALIMENTACION_INADECUADA = "ALIMENTACION_INADECUADA"
    EXPOSICION_PANTALLAS = "EXPOSICION_PANTALLAS"
    PROBLEMAS_SUENO = "PROBLEMAS_SUENO"
    VIOLENCIA_ESCOLAR = "VIOLENCIA_ESCOLAR"
    NINGUNO = "NINGUNO"

# =============================================================================
# MODELOS BASE
# =============================================================================

class AtencionInfanciaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[UUID] = None
    paciente_id: UUID = Field(description="ID del paciente")
    medico_id: Optional[UUID] = Field(None, description="ID del médico responsable")
    atencion_id: Optional[UUID] = Field(None, description="Referencia a atención general")

    # Datos básicos de la consulta
    fecha_atencion: date = Field(description="Fecha de la atención")
    entorno: str = Field(default="IPS", description="Entorno de atención")
    
    # DATOS ANTROPOMÉTRICOS (OBLIGATORIOS según Resolución 3280)
    peso_kg: float = Field(gt=0, le=150, description="Peso en kilogramos")
    talla_cm: float = Field(gt=50, le=200, description="Talla en centímetros")
    
    # DESARROLLO Y RENDIMIENTO ESCOLAR
    grado_escolar: Optional[str] = Field(None, description="Grado escolar actual")
    desempeno_escolar: DesempenoEscolar = Field(description="Evaluación del desempeño escolar")
    dificultades_aprendizaje: bool = Field(default=False, description="Presenta dificultades de aprendizaje")
    observaciones_desarrollo_cognitivo: Optional[str] = Field(None, description="Observaciones sobre desarrollo cognitivo")
    
    # SALUD VISUAL Y AUDITIVA (CRÍTICO EN EDAD ESCOLAR)
    tamizaje_visual: ResultadoTamizaje = Field(description="Resultado tamizaje visual")
    agudeza_visual_ojo_derecho: Optional[str] = Field(None, description="Agudeza visual ojo derecho")
    agudeza_visual_ojo_izquierdo: Optional[str] = Field(None, description="Agudeza visual ojo izquierdo")
    tamizaje_auditivo: ResultadoTamizaje = Field(description="Resultado tamizaje auditivo")
    observaciones_salud_visual_auditiva: Optional[str] = Field(None, description="Observaciones salud visual y auditiva")
    
    # SALUD BUCAL (DENTICIÓN PERMANENTE)
    tamizaje_salud_bucal: ResultadoTamizaje = Field(description="Resultado tamizaje salud bucal")
    numero_dientes_permanentes: Optional[int] = Field(None, ge=0, le=32, description="Número de dientes permanentes")
    numero_caries: Optional[int] = Field(None, ge=0, description="Número de caries identificadas")
    higiene_bucal: Optional[str] = Field(None, description="Evaluación de higiene bucal")
    observaciones_salud_bucal: Optional[str] = Field(None, description="Observaciones salud bucal")
    
    # ESQUEMA DE VACUNACIÓN
    esquema_vacunacion_completo: bool = Field(description="Esquema de vacunación completo para la edad")
    vacunas_faltantes: Optional[str] = Field(None, description="Vacunas faltantes si aplica")
    
    # ESTILOS DE VIDA Y FACTORES DE RIESGO
    actividad_fisica_semanal_horas: Optional[float] = Field(None, ge=0, le=168, description="Horas de actividad física por semana")
    horas_pantalla_diarias: Optional[float] = Field(None, ge=0, le=24, description="Horas de exposición a pantallas por día")
    horas_sueno_diarias: Optional[float] = Field(None, ge=0, le=24, description="Horas de sueño por día")
    factores_riesgo_identificados: Optional[list[FactorRiesgo]] = Field(default=[], description="Factores de riesgo identificados")
    
    # ALIMENTACIÓN Y NUTRICIÓN
    alimentacion_escolar: bool = Field(default=False, description="Recibe alimentación en el colegio")
    consume_comida_chatarra: bool = Field(default=False, description="Consumo frecuente de comida chatarra")
    observaciones_alimentacion: Optional[str] = Field(None, description="Observaciones sobre alimentación")
    
    # OBSERVACIONES GENERALES
    observaciones_profesional_infancia: Optional[str] = Field(None, description="Observaciones generales del profesional")
    
    # METADATOS
    creado_en: Optional[datetime] = Field(default_factory=datetime.now, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Fecha de última actualización")

# =============================================================================
# MODELOS ESPECIALIZADOS PARA API
# =============================================================================

class AtencionInfanciaCrear(BaseModel):
    """Modelo para crear nueva atención de infancia"""
    model_config = ConfigDict(from_attributes=True)
    
    paciente_id: UUID = Field(description="ID del paciente")
    medico_id: Optional[UUID] = Field(None, description="ID del médico responsable")

    # Datos básicos de la consulta
    fecha_atencion: date = Field(description="Fecha de la atención")
    entorno: str = Field(default="IPS", description="Entorno de atención")
    
    # DATOS ANTROPOMÉTRICOS (OBLIGATORIOS según Resolución 3280)
    peso_kg: float = Field(gt=0, le=150, description="Peso en kilogramos")
    talla_cm: float = Field(gt=50, le=200, description="Talla en centímetros")
    
    # DESARROLLO Y RENDIMIENTO ESCOLAR
    grado_escolar: Optional[str] = Field(None, description="Grado escolar actual")
    desempeno_escolar: DesempenoEscolar = Field(description="Evaluación del desempeño escolar")
    dificultades_aprendizaje: bool = Field(default=False, description="Presenta dificultades de aprendizaje")
    observaciones_desarrollo_cognitivo: Optional[str] = Field(None, description="Observaciones sobre desarrollo cognitivo")
    
    # SALUD VISUAL Y AUDITIVA (CRÍTICO EN EDAD ESCOLAR)
    tamizaje_visual: ResultadoTamizaje = Field(description="Resultado tamizaje visual")
    agudeza_visual_ojo_derecho: Optional[str] = Field(None, description="Agudeza visual ojo derecho")
    agudeza_visual_ojo_izquierdo: Optional[str] = Field(None, description="Agudeza visual ojo izquierdo")
    tamizaje_auditivo: ResultadoTamizaje = Field(description="Resultado tamizaje auditivo")
    observaciones_salud_visual_auditiva: Optional[str] = Field(None, description="Observaciones salud visual y auditiva")
    
    # SALUD BUCAL (DENTICIÓN PERMANENTE)
    tamizaje_salud_bucal: ResultadoTamizaje = Field(description="Resultado tamizaje salud bucal")
    numero_dientes_permanentes: Optional[int] = Field(None, ge=0, le=32, description="Número de dientes permanentes")
    numero_caries: Optional[int] = Field(None, ge=0, description="Número de caries identificadas")
    higiene_bucal: Optional[str] = Field(None, description="Evaluación de higiene bucal")
    observaciones_salud_bucal: Optional[str] = Field(None, description="Observaciones salud bucal")
    
    # ESQUEMA DE VACUNACIÓN
    esquema_vacunacion_completo: bool = Field(description="Esquema de vacunación completo para la edad")
    vacunas_faltantes: Optional[str] = Field(None, description="Vacunas faltantes si aplica")
    
    # ESTILOS DE VIDA Y FACTORES DE RIESGO
    actividad_fisica_semanal_horas: Optional[float] = Field(None, ge=0, le=168, description="Horas de actividad física por semana")
    horas_pantalla_diarias: Optional[float] = Field(None, ge=0, le=24, description="Horas de exposición a pantallas por día")
    horas_sueno_diarias: Optional[float] = Field(None, ge=0, le=24, description="Horas de sueño por día")
    factores_riesgo_identificados: Optional[list[FactorRiesgo]] = Field(default=[], description="Factores de riesgo identificados")
    
    # ALIMENTACIÓN Y NUTRICIÓN
    alimentacion_escolar: bool = Field(default=False, description="Recibe alimentación en el colegio")
    consume_comida_chatarra: bool = Field(default=False, description="Consumo frecuente de comida chatarra")
    observaciones_alimentacion: Optional[str] = Field(None, description="Observaciones sobre alimentación")
    
    # OBSERVACIONES GENERALES
    observaciones_profesional_infancia: Optional[str] = Field(None, description="Observaciones generales del profesional")

class AtencionInfanciaActualizar(BaseModel):
    """Modelo para actualizar atención de infancia"""
    model_config = ConfigDict(from_attributes=True)
    
    # Solo campos que pueden ser actualizados
    peso_kg: Optional[float] = Field(None, gt=0, le=150)
    talla_cm: Optional[float] = Field(None, gt=50, le=200)
    grado_escolar: Optional[str] = None
    desempeno_escolar: Optional[DesempenoEscolar] = None
    dificultades_aprendizaje: Optional[bool] = None
    observaciones_desarrollo_cognitivo: Optional[str] = None
    tamizaje_visual: Optional[ResultadoTamizaje] = None
    agudeza_visual_ojo_derecho: Optional[str] = None
    agudeza_visual_ojo_izquierdo: Optional[str] = None
    tamizaje_auditivo: Optional[ResultadoTamizaje] = None
    observaciones_salud_visual_auditiva: Optional[str] = None
    tamizaje_salud_bucal: Optional[ResultadoTamizaje] = None
    numero_dientes_permanentes: Optional[int] = Field(None, ge=0, le=32)
    numero_caries: Optional[int] = Field(None, ge=0)
    higiene_bucal: Optional[str] = None
    observaciones_salud_bucal: Optional[str] = None
    esquema_vacunacion_completo: Optional[bool] = None
    vacunas_faltantes: Optional[str] = None
    actividad_fisica_semanal_horas: Optional[float] = Field(None, ge=0, le=168)
    horas_pantalla_diarias: Optional[float] = Field(None, ge=0, le=24)
    horas_sueno_diarias: Optional[float] = Field(None, ge=0, le=24)
    factores_riesgo_identificados: Optional[list[FactorRiesgo]] = None
    alimentacion_escolar: Optional[bool] = None
    consume_comida_chatarra: Optional[bool] = None
    observaciones_alimentacion: Optional[str] = None
    observaciones_profesional_infancia: Optional[str] = None

class AtencionInfanciaResponse(AtencionInfanciaBase):
    """Modelo para respuesta de API con campos calculados"""
    
    # CAMPOS CALCULADOS AUTOMÁTICAMENTE
    estado_nutricional: EstadoNutricionalInfancia = Field(description="Estado nutricional calculado según IMC para la edad")
    indice_masa_corporal: float = Field(description="IMC calculado")
    percentil_peso: Optional[int] = Field(None, description="Percentil de peso para la edad")
    percentil_talla: Optional[int] = Field(None, description="Percentil de talla para la edad")
    desarrollo_apropiado_edad: bool = Field(description="Desarrollo apropiado para la edad")
    riesgo_nutricional: str = Field(description="Evaluación de riesgo nutricional")
    requiere_seguimiento_especializado: bool = Field(description="Requiere seguimiento por especialista")
    proxima_consulta_recomendada_dias: int = Field(description="Días hasta próxima consulta recomendada")
    completitud_evaluacion: float = Field(description="Porcentaje de completitud de la evaluación")

# =============================================================================
# FUNCIONES DE CÁLCULO PARA CAMPOS AUTOMÁTICOS
# =============================================================================

def calcular_estado_nutricional(peso_kg: float, talla_cm: float, edad_anos: int) -> EstadoNutricionalInfancia:
    """Calcular estado nutricional según IMC para edad en niños de 6-11 años"""
    try:
        imc = peso_kg / ((talla_cm / 100) ** 2)
        
        # Percentiles IMC para edad según OMS (simplificado)
        # Para niños de 6-11 años
        if imc < 14.5:
            return EstadoNutricionalInfancia.DELGADEZ
        elif 14.5 <= imc < 18.5:
            return EstadoNutricionalInfancia.NORMAL
        elif 18.5 <= imc < 21.0:
            return EstadoNutricionalInfancia.SOBREPESO
        else:
            return EstadoNutricionalInfancia.OBESIDAD
            
    except (ZeroDivisionError, ValueError):
        return EstadoNutricionalInfancia.NORMAL

def calcular_desarrollo_apropiado(
    desempeno_escolar: DesempenoEscolar,
    tamizaje_visual: ResultadoTamizaje,
    tamizaje_auditivo: ResultadoTamizaje,
    dificultades_aprendizaje: bool
) -> bool:
    """Evaluar si el desarrollo es apropiado para la edad"""
    
    # Desarrollo apropiado si:
    # - Desempeño escolar básico o superior
    # - Tamizajes sensoriales normales
    # - Sin dificultades de aprendizaje significativas
    
    desempeno_adecuado = desempeno_escolar in [DesempenoEscolar.SUPERIOR, DesempenoEscolar.ALTO, DesempenoEscolar.BASICO]
    tamizajes_normales = tamizaje_visual == ResultadoTamizaje.NORMAL and tamizaje_auditivo == ResultadoTamizaje.NORMAL
    sin_dificultades_mayores = not dificultades_aprendizaje
    
    return desempeno_adecuado and tamizajes_normales and sin_dificultades_mayores

def calcular_riesgo_nutricional(
    estado_nutricional: EstadoNutricionalInfancia,
    consume_comida_chatarra: bool,
    actividad_fisica_semanal_horas: Optional[float]
) -> str:
    """Evaluar riesgo nutricional basado en múltiples factores"""
    
    factores_riesgo = 0
    
    # Factor 1: Estado nutricional
    if estado_nutricional in [EstadoNutricionalInfancia.DELGADEZ, EstadoNutricionalInfancia.OBESIDAD]:
        factores_riesgo += 2
    elif estado_nutricional == EstadoNutricionalInfancia.SOBREPESO:
        factores_riesgo += 1
    
    # Factor 2: Consumo comida chatarra
    if consume_comida_chatarra:
        factores_riesgo += 1
    
    # Factor 3: Actividad física insuficiente (menos de 7 horas/semana)
    if actividad_fisica_semanal_horas is not None and actividad_fisica_semanal_horas < 7:
        factores_riesgo += 1
    
    # Clasificación de riesgo
    if factores_riesgo >= 3:
        return "Alto"
    elif factores_riesgo >= 2:
        return "Moderado"
    else:
        return "Bajo"

def calcular_proxima_consulta_dias(
    estado_nutricional: EstadoNutricionalInfancia,
    requiere_seguimiento: bool,
    factores_riesgo: list[FactorRiesgo]
) -> int:
    """Calcular días hasta próxima consulta según riesgo y estado"""
    
    # Seguimiento especializado: 30 días
    if requiere_seguimiento:
        return 30
    
    # Estado nutricional alterado: 90 días
    if estado_nutricional in [EstadoNutricionalInfancia.DELGADEZ, EstadoNutricionalInfancia.OBESIDAD]:
        return 90
    
    # Sobrepeso o factores de riesgo: 180 días
    if estado_nutricional == EstadoNutricionalInfancia.SOBREPESO or len(factores_riesgo) > 1:
        return 180
    
    # Normal: 365 días (anual según Resolución 3280)
    return 365

def calcular_completitud_evaluacion(atencion: dict) -> float:
    """Calcular porcentaje de completitud de la evaluación"""
    
    campos_obligatorios = [
        'peso_kg', 'talla_cm', 'desempeno_escolar', 'tamizaje_visual', 
        'tamizaje_auditivo', 'tamizaje_salud_bucal', 'esquema_vacunacion_completo'
    ]
    
    campos_opcionales = [
        'grado_escolar', 'observaciones_desarrollo_cognitivo', 'agudeza_visual_ojo_derecho',
        'agudeza_visual_ojo_izquierdo', 'numero_dientes_permanentes', 'numero_caries',
        'actividad_fisica_semanal_horas', 'horas_pantalla_diarias', 'horas_sueno_diarias'
    ]
    
    total_campos = len(campos_obligatorios) + len(campos_opcionales)
    campos_completados = 0
    
    # Campos obligatorios (peso doble)
    for campo in campos_obligatorios:
        if atencion.get(campo) is not None:
            campos_completados += 2
    
    # Campos opcionales (peso simple)
    for campo in campos_opcionales:
        if atencion.get(campo) is not None:
            campos_completados += 1
    
    # Máximo posible: obligatorios * 2 + opcionales * 1
    max_puntos = len(campos_obligatorios) * 2 + len(campos_opcionales)
    
    return round((campos_completados / max_puntos) * 100, 1)

def determinar_seguimiento_especializado(
    tamizaje_visual: ResultadoTamizaje,
    tamizaje_auditivo: ResultadoTamizaje,
    tamizaje_salud_bucal: ResultadoTamizaje,
    dificultades_aprendizaje: bool,
    numero_caries: Optional[int]
) -> bool:
    """Determinar si requiere seguimiento especializado"""
    
    # Requiere seguimiento si:
    # - Tamizajes alterados
    # - Dificultades de aprendizaje
    # - Caries múltiples (>3)
    
    tamizajes_alterados = tamizaje_visual == ResultadoTamizaje.ALTERADO or \
                         tamizaje_auditivo == ResultadoTamizaje.ALTERADO or \
                         tamizaje_salud_bucal == ResultadoTamizaje.ALTERADO
    
    caries_multiples = numero_caries is not None and numero_caries > 3
    
    return tamizajes_alterados or dificultades_aprendizaje or caries_multiples