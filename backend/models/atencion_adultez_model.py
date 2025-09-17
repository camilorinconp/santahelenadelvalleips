# =============================================================================
# Modelo Atención Adultez - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025  
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.5 (Adultez 30-59 años)
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum
from math import log

# =============================================================================
# ENUMS ESPECÍFICOS PARA ADULTEZ (30-59 AÑOS)
# =============================================================================

class EstadoNutricionalAdulto(str, Enum):
    """Estado nutricional para adultos 30-59 años"""
    PESO_BAJO = "PESO_BAJO"
    NORMAL = "NORMAL"
    SOBREPESO = "SOBREPESO"
    OBESIDAD_GRADO_I = "OBESIDAD_GRADO_I"
    OBESIDAD_GRADO_II = "OBESIDAD_GRADO_II"
    OBESIDAD_GRADO_III = "OBESIDAD_GRADO_III"

class RiesgoCardiovascularFramingham(str, Enum):
    """Riesgo cardiovascular según Framingham"""
    BAJO = "BAJO"              # <10%
    INTERMEDIO = "INTERMEDIO"  # 10-19%
    ALTO = "ALTO"              # 20-30%
    MUY_ALTO = "MUY_ALTO"      # >30%

class TamizajeECNT(str, Enum):
    """Tamizaje Enfermedades Crónicas No Transmisibles"""
    NORMAL = "NORMAL"
    ALTERADO_LEVE = "ALTERADO_LEVE"
    ALTERADO_MODERADO = "ALTERADO_MODERADO"
    ALTERADO_SEVERO = "ALTERADO_SEVERO"
    REQUIERE_EVALUACION_ESPECIALIZADA = "REQUIERE_EVALUACION_ESPECIALIZADA"

class SaludMentalLaboral(str, Enum):
    """Evaluación salud mental en contexto laboral"""
    NORMAL = "NORMAL"
    ESTRES_LEVE = "ESTRES_LEVE"
    ESTRES_MODERADO = "ESTRES_MODERADO"
    ESTRES_SEVERO = "ESTRES_SEVERO"
    BURNOUT = "BURNOUT"
    REQUIERE_ATENCION_PSIQUIATRICA = "REQUIERE_ATENCION_PSIQUIATRICA"

class RiesgoOcupacional(str, Enum):
    """Evaluación riesgo ocupacional"""
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    MUY_ALTO = "MUY_ALTO"
    EXPOSICION_CRITICA = "EXPOSICION_CRITICA"

class ViolenciaIntrafamiliar(str, Enum):
    """Detección violencia intrafamiliar"""
    SIN_INDICADORES = "SIN_INDICADORES"
    INDICADORES_LEVES = "INDICADORES_LEVES"
    INDICADORES_MODERADOS = "INDICADORES_MODERADOS"
    INDICADORES_SEVEROS = "INDICADORES_SEVEROS"
    SITUACION_CONFIRMADA = "SITUACION_CONFIRMADA"

class EstilosVidaSaludable(str, Enum):
    """Evaluación estilos de vida saludable"""
    EXCELENTE = "EXCELENTE"
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    DEFICIENTE = "DEFICIENTE"
    CRITICO = "CRITICO"

class NivelRiesgoGlobal(str, Enum):
    """Nivel de riesgo global calculado para adultos"""
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    MUY_ALTO = "MUY_ALTO"
    CRITICO = "CRITICO"

class FactorProtectorAdulto(str, Enum):
    """Factores protectores específicos para adultos"""
    ACTIVIDAD_FISICA_REGULAR = "ACTIVIDAD_FISICA_REGULAR"
    DIETA_SALUDABLE = "DIETA_SALUDABLE"
    NO_FUMADOR = "NO_FUMADOR"
    CONSUMO_ALCOHOL_MODERADO = "CONSUMO_ALCOHOL_MODERADO"
    CONTROL_ESTRES_EFECTIVO = "CONTROL_ESTRES_EFECTIVO"
    SOPORTE_SOCIAL_ADECUADO = "SOPORTE_SOCIAL_ADECUADO"
    TRABAJO_SATISFACTORIO = "TRABAJO_SATISFACTORIO"
    RELACIONES_FAMILIARES_SANAS = "RELACIONES_FAMILIARES_SANAS"
    CONTROL_MEDICO_REGULAR = "CONTROL_MEDICO_REGULAR"

# =============================================================================
# FUNCIONES CALCULADAS AUTOMÁTICAS
# =============================================================================

def calcular_riesgo_framingham(
    edad: int,
    sexo: str,
    colesterol_total: float,
    colesterol_hdl: float,
    presion_sistolica: float,
    fumador: bool,
    diabetes: bool
) -> tuple[float, RiesgoCardiovascularFramingham]:
    """
    Calcula riesgo cardiovascular según ecuación de Framingham
    Retorna: (porcentaje_riesgo, categoria_riesgo)
    """
    # Factores de riesgo según Framingham
    puntos = 0
    
    if sexo.upper() == "M":  # Hombres
        # Edad
        if edad >= 70: puntos += 11
        elif edad >= 65: puntos += 10
        elif edad >= 60: puntos += 8
        elif edad >= 55: puntos += 6
        elif edad >= 50: puntos += 4
        elif edad >= 45: puntos += 2
        elif edad >= 40: puntos += 1
        
        # Colesterol total
        if colesterol_total >= 280: puntos += 3
        elif colesterol_total >= 240: puntos += 2
        elif colesterol_total >= 200: puntos += 1
        
        # HDL
        if colesterol_hdl < 35: puntos += 2
        elif colesterol_hdl < 45: puntos += 1
        elif colesterol_hdl >= 60: puntos -= 1
        
        # Presión sistólica
        if presion_sistolica >= 160: puntos += 3
        elif presion_sistolica >= 140: puntos += 2
        elif presion_sistolica >= 130: puntos += 1
        
        # Fumador
        if fumador: puntos += 2
        
        # Diabetes
        if diabetes: puntos += 2
        
    else:  # Mujeres
        # Edad
        if edad >= 70: puntos += 12
        elif edad >= 65: puntos += 11
        elif edad >= 60: puntos += 9
        elif edad >= 55: puntos += 7
        elif edad >= 50: puntos += 5
        elif edad >= 45: puntos += 3
        elif edad >= 40: puntos += 2
        
        # Colesterol total
        if colesterol_total >= 280: puntos += 4
        elif colesterol_total >= 240: puntos += 3
        elif colesterol_total >= 200: puntos += 2
        elif colesterol_total >= 160: puntos += 1
        
        # HDL
        if colesterol_hdl < 35: puntos += 5
        elif colesterol_hdl < 45: puntos += 2
        elif colesterol_hdl < 50: puntos += 1
        elif colesterol_hdl >= 60: puntos -= 2
        
        # Presión sistólica
        if presion_sistolica >= 160: puntos += 4
        elif presion_sistolica >= 140: puntos += 2
        elif presion_sistolica >= 130: puntos += 1
        
        # Fumador
        if fumador: puntos += 3
        
        # Diabetes
        if diabetes: puntos += 4
    
    # Convertir puntos a porcentaje de riesgo (aproximación)
    if puntos <= 0:
        porcentaje_riesgo = 1.0
    elif puntos >= 20:
        porcentaje_riesgo = 40.0
    else:
        # Fórmula aproximada exponencial
        porcentaje_riesgo = min(40.0, max(1.0, 1.5 * (1.3 ** puntos)))
    
    # Categorizar riesgo
    if porcentaje_riesgo < 10:
        categoria = RiesgoCardiovascularFramingham.BAJO
    elif porcentaje_riesgo < 20:
        categoria = RiesgoCardiovascularFramingham.INTERMEDIO
    elif porcentaje_riesgo < 30:
        categoria = RiesgoCardiovascularFramingham.ALTO
    else:
        categoria = RiesgoCardiovascularFramingham.MUY_ALTO
    
    return round(porcentaje_riesgo, 1), categoria

def evaluar_tamizaje_ecnt(
    glicemia_ayunas: float,
    presion_sistolica: float,
    presion_diastolica: float,
    colesterol_total: float,
    imc: float
) -> TamizajeECNT:
    """Evalúa tamizaje integral de ECNT"""
    alteraciones = 0
    
    # Diabetes/Prediabetes
    if glicemia_ayunas >= 126:
        alteraciones += 3  # Diabetes
    elif glicemia_ayunas >= 100:
        alteraciones += 1  # Prediabetes
    
    # Hipertensión
    if presion_sistolica >= 140 or presion_diastolica >= 90:
        alteraciones += 2  # HTA
    elif presion_sistolica >= 130 or presion_diastolica >= 85:
        alteraciones += 1  # Prehipertensión
    
    # Dislipidemia
    if colesterol_total >= 240:
        alteraciones += 2
    elif colesterol_total >= 200:
        alteraciones += 1
    
    # Obesidad
    if imc >= 35:
        alteraciones += 2
    elif imc >= 30:
        alteraciones += 1
    
    if alteraciones == 0:
        return TamizajeECNT.NORMAL
    elif alteraciones <= 2:
        return TamizajeECNT.ALTERADO_LEVE
    elif alteraciones <= 4:
        return TamizajeECNT.ALTERADO_MODERADO
    elif alteraciones <= 6:
        return TamizajeECNT.ALTERADO_SEVERO
    else:
        return TamizajeECNT.REQUIERE_EVALUACION_ESPECIALIZADA

def evaluar_salud_mental_laboral(
    estres_percibido: int,  # Escala 1-10
    carga_laboral: int,     # Escala 1-10
    satisfaccion_laboral: int,  # Escala 1-10
    conflictos_laborales: bool,
    cambios_recientes_trabajo: bool,
    sintomas_depresivos: bool,
    sintomas_ansiedad: bool
) -> SaludMentalLaboral:
    """Evalúa salud mental en contexto laboral"""
    puntuacion_riesgo = 0
    
    # Estrés percibido
    if estres_percibido >= 8:
        puntuacion_riesgo += 3
    elif estres_percibido >= 6:
        puntuacion_riesgo += 2
    elif estres_percibido >= 4:
        puntuacion_riesgo += 1
    
    # Carga laboral
    if carga_laboral >= 8:
        puntuacion_riesgo += 2
    elif carga_laboral >= 6:
        puntuacion_riesgo += 1
    
    # Satisfacción laboral (inverso)
    if satisfaccion_laboral <= 3:
        puntuacion_riesgo += 3
    elif satisfaccion_laboral <= 5:
        puntuacion_riesgo += 2
    elif satisfaccion_laboral <= 7:
        puntuacion_riesgo += 1
    
    # Factores adicionales
    if conflictos_laborales:
        puntuacion_riesgo += 2
    if cambios_recientes_trabajo:
        puntuacion_riesgo += 1
    if sintomas_depresivos:
        puntuacion_riesgo += 3
    if sintomas_ansiedad:
        puntuacion_riesgo += 2
    
    if puntuacion_riesgo == 0:
        return SaludMentalLaboral.NORMAL
    elif puntuacion_riesgo <= 3:
        return SaludMentalLaboral.ESTRES_LEVE
    elif puntuacion_riesgo <= 6:
        return SaludMentalLaboral.ESTRES_MODERADO
    elif puntuacion_riesgo <= 10:
        return SaludMentalLaboral.ESTRES_SEVERO
    elif puntuacion_riesgo <= 13:
        return SaludMentalLaboral.BURNOUT
    else:
        return SaludMentalLaboral.REQUIERE_ATENCION_PSIQUIATRICA

def evaluar_estilos_vida_saludable(
    actividad_fisica_min_semana: int,
    porciones_frutas_verduras_dia: int,
    cigarrillos_dia: int,
    copas_alcohol_semana: int,
    horas_sueno_promedio: float,
    tecnicas_manejo_estres: bool
) -> EstilosVidaSaludable:
    """Evalúa estilos de vida saludable integralmente"""
    puntuacion = 0
    
    # Actividad física (recomendación: 150 min/semana)
    if actividad_fisica_min_semana >= 150:
        puntuacion += 3
    elif actividad_fisica_min_semana >= 75:
        puntuacion += 2
    elif actividad_fisica_min_semana >= 30:
        puntuacion += 1
    
    # Alimentación (recomendación: 5+ porciones/día)
    if porciones_frutas_verduras_dia >= 5:
        puntuacion += 3
    elif porciones_frutas_verduras_dia >= 3:
        puntuacion += 2
    elif porciones_frutas_verduras_dia >= 1:
        puntuacion += 1
    
    # Tabaquismo (inverso)
    if cigarrillos_dia == 0:
        puntuacion += 3
    elif cigarrillos_dia <= 5:
        puntuacion += 1
    # >5 cigarrillos: 0 puntos
    
    # Alcohol (consumo moderado)
    if copas_alcohol_semana == 0:
        puntuacion += 2
    elif copas_alcohol_semana <= 7:  # Consumo moderado
        puntuacion += 3
    elif copas_alcohol_semana <= 14:
        puntuacion += 1
    # >14 copas: 0 puntos
    
    # Sueño (recomendación: 7-9 horas)
    if 7 <= horas_sueno_promedio <= 9:
        puntuacion += 2
    elif 6 <= horas_sueno_promedio <= 10:
        puntuacion += 1
    
    # Manejo del estrés
    if tecnicas_manejo_estres:
        puntuacion += 2
    
    # Puntuación máxima: 16 puntos
    if puntuacion >= 14:
        return EstilosVidaSaludable.EXCELENTE
    elif puntuacion >= 11:
        return EstilosVidaSaludable.BUENO
    elif puntuacion >= 7:
        return EstilosVidaSaludable.REGULAR
    elif puntuacion >= 3:
        return EstilosVidaSaludable.DEFICIENTE
    else:
        return EstilosVidaSaludable.CRITICO

def identificar_factores_protectores_adulto(
    actividad_fisica_min_semana: int,
    porciones_frutas_verduras_dia: int,
    cigarrillos_dia: int,
    copas_alcohol_semana: int,
    tecnicas_manejo_estres: bool,
    soporte_social_adecuado: bool,
    satisfaccion_laboral: int,
    relaciones_familiares_satisfactorias: bool,
    control_medico_preventivo_regular: bool
) -> List[FactorProtectorAdulto]:
    """Identifica factores protectores presentes en el adulto"""
    factores = []
    
    if actividad_fisica_min_semana >= 150:
        factores.append(FactorProtectorAdulto.ACTIVIDAD_FISICA_REGULAR)
    
    if porciones_frutas_verduras_dia >= 5:
        factores.append(FactorProtectorAdulto.DIETA_SALUDABLE)
    
    if cigarrillos_dia == 0:
        factores.append(FactorProtectorAdulto.NO_FUMADOR)
    
    if 0 <= copas_alcohol_semana <= 7:
        factores.append(FactorProtectorAdulto.CONSUMO_ALCOHOL_MODERADO)
    
    if tecnicas_manejo_estres:
        factores.append(FactorProtectorAdulto.CONTROL_ESTRES_EFECTIVO)
    
    if soporte_social_adecuado:
        factores.append(FactorProtectorAdulto.SOPORTE_SOCIAL_ADECUADO)
    
    if satisfaccion_laboral >= 7:
        factores.append(FactorProtectorAdulto.TRABAJO_SATISFACTORIO)
    
    if relaciones_familiares_satisfactorias:
        factores.append(FactorProtectorAdulto.RELACIONES_FAMILIARES_SANAS)
    
    if control_medico_preventivo_regular:
        factores.append(FactorProtectorAdulto.CONTROL_MEDICO_REGULAR)
    
    return factores

def calcular_nivel_riesgo_global(
    riesgo_framingham_porcentaje: float,
    tamizaje_ecnt: TamizajeECNT,
    salud_mental_laboral: SaludMentalLaboral,
    riesgo_ocupacional: RiesgoOcupacional,
    violencia_intrafamiliar: ViolenciaIntrafamiliar,
    estilos_vida: EstilosVidaSaludable,
    factores_protectores: List[FactorProtectorAdulto]
) -> NivelRiesgoGlobal:
    """Calcula nivel de riesgo global ponderado"""
    puntuacion_riesgo = 0
    
    # Riesgo cardiovascular Framingham (peso alto)
    if riesgo_framingham_porcentaje >= 30:
        puntuacion_riesgo += 4
    elif riesgo_framingham_porcentaje >= 20:
        puntuacion_riesgo += 3
    elif riesgo_framingham_porcentaje >= 10:
        puntuacion_riesgo += 2
    elif riesgo_framingham_porcentaje >= 5:
        puntuacion_riesgo += 1
    
    # Tamizaje ECNT
    ecnt_scores = {
        TamizajeECNT.NORMAL: 0,
        TamizajeECNT.ALTERADO_LEVE: 1,
        TamizajeECNT.ALTERADO_MODERADO: 2,
        TamizajeECNT.ALTERADO_SEVERO: 3,
        TamizajeECNT.REQUIERE_EVALUACION_ESPECIALIZADA: 4
    }
    puntuacion_riesgo += ecnt_scores[tamizaje_ecnt]
    
    # Salud mental laboral
    mental_scores = {
        SaludMentalLaboral.NORMAL: 0,
        SaludMentalLaboral.ESTRES_LEVE: 1,
        SaludMentalLaboral.ESTRES_MODERADO: 2,
        SaludMentalLaboral.ESTRES_SEVERO: 3,
        SaludMentalLaboral.BURNOUT: 4,
        SaludMentalLaboral.REQUIERE_ATENCION_PSIQUIATRICA: 5
    }
    puntuacion_riesgo += mental_scores[salud_mental_laboral]
    
    # Riesgo ocupacional
    ocupacional_scores = {
        RiesgoOcupacional.BAJO: 0,
        RiesgoOcupacional.MODERADO: 1,
        RiesgoOcupacional.ALTO: 2,
        RiesgoOcupacional.MUY_ALTO: 3,
        RiesgoOcupacional.EXPOSICION_CRITICA: 4
    }
    puntuacion_riesgo += ocupacional_scores[riesgo_ocupacional]
    
    # Violencia intrafamiliar
    violencia_scores = {
        ViolenciaIntrafamiliar.SIN_INDICADORES: 0,
        ViolenciaIntrafamiliar.INDICADORES_LEVES: 1,
        ViolenciaIntrafamiliar.INDICADORES_MODERADOS: 2,
        ViolenciaIntrafamiliar.INDICADORES_SEVEROS: 3,
        ViolenciaIntrafamiliar.SITUACION_CONFIRMADA: 4
    }
    puntuacion_riesgo += violencia_scores[violencia_intrafamiliar]
    
    # Estilos de vida (inverso)
    estilos_scores = {
        EstilosVidaSaludable.EXCELENTE: -2,
        EstilosVidaSaludable.BUENO: -1,
        EstilosVidaSaludable.REGULAR: 0,
        EstilosVidaSaludable.DEFICIENTE: 2,
        EstilosVidaSaludable.CRITICO: 3
    }
    puntuacion_riesgo += estilos_scores[estilos_vida]
    
    # Ajuste por factores protectores
    num_factores_protectores = len(factores_protectores)
    if num_factores_protectores >= 7:
        puntuacion_riesgo -= 3
    elif num_factores_protectores >= 5:
        puntuacion_riesgo -= 2
    elif num_factores_protectores >= 3:
        puntuacion_riesgo -= 1
    
    # No puede ser negativo
    puntuacion_riesgo = max(0, puntuacion_riesgo)
    
    if puntuacion_riesgo >= 15:
        return NivelRiesgoGlobal.CRITICO
    elif puntuacion_riesgo >= 12:
        return NivelRiesgoGlobal.MUY_ALTO
    elif puntuacion_riesgo >= 8:
        return NivelRiesgoGlobal.ALTO
    elif puntuacion_riesgo >= 4:
        return NivelRiesgoGlobal.MODERADO
    else:
        return NivelRiesgoGlobal.BAJO

def calcular_proxima_consulta_dias_adulto(
    nivel_riesgo_global: NivelRiesgoGlobal,
    edad: int,
    factores_protectores: List[FactorProtectorAdulto],
    riesgo_framingham_porcentaje: float
) -> int:
    """Calcula días hasta próxima consulta preventiva"""
    base_dias = {
        NivelRiesgoGlobal.CRITICO: 30,
        NivelRiesgoGlobal.MUY_ALTO: 60,
        NivelRiesgoGlobal.ALTO: 90,
        NivelRiesgoGlobal.MODERADO: 180,
        NivelRiesgoGlobal.BAJO: 365
    }
    
    dias = base_dias[nivel_riesgo_global]
    
    # Ajuste por edad (adultos mayores necesitan más seguimiento)
    if edad >= 55:
        dias = int(dias * 0.8)
    elif edad >= 45:
        dias = int(dias * 0.9)
    
    # Ajuste por riesgo cardiovascular alto
    if riesgo_framingham_porcentaje >= 20:
        dias = int(dias * 0.7)
    elif riesgo_framingham_porcentaje >= 10:
        dias = int(dias * 0.85)
    
    # Ajuste por factores protectores
    if len(factores_protectores) >= 7:
        dias = int(dias * 1.3)
    elif len(factores_protectores) >= 5:
        dias = int(dias * 1.2)
    elif len(factores_protectores) <= 2:
        dias = int(dias * 0.8)
    
    return dias

# =============================================================================
# MODELOS PYDANTIC - PATRÓN CREAR/ACTUALIZAR/RESPONSE
# =============================================================================

class AtencionAdultezBase(BaseModel):
    """Modelo base para atención adultez"""
    # Datos básicos del paciente
    paciente_id: UUID = Field(description="ID del paciente")
    medico_id: UUID = Field(description="ID del médico que atiende")
    fecha_atencion: date = Field(description="Fecha de la atención")
    edad_anos: int = Field(ge=30, le=59, description="Edad en años (30-59)")
    
    # Datos antropométricos y signos vitales
    peso_kg: float = Field(gt=0, le=300, description="Peso en kilogramos")
    talla_cm: float = Field(gt=0, le=250, description="Talla en centímetros")
    presion_sistolica: float = Field(ge=70, le=250, description="Presión sistólica")
    presion_diastolica: float = Field(ge=40, le=150, description="Presión diastólica")
    frecuencia_cardiaca: int = Field(ge=40, le=150, description="Frecuencia cardíaca")
    
    # Laboratorios para riesgo cardiovascular
    glicemia_ayunas: float = Field(ge=50, le=500, description="Glicemia en ayunas (mg/dL)")
    colesterol_total: float = Field(ge=100, le=600, description="Colesterol total (mg/dL)")
    colesterol_hdl: float = Field(ge=20, le=150, description="Colesterol HDL (mg/dL)")
    colesterol_ldl: Optional[float] = Field(default=None, ge=20, le=500, description="Colesterol LDL (mg/dL)")
    trigliceridos: Optional[float] = Field(default=None, ge=30, le=1000, description="Triglicéridos (mg/dL)")
    
    # Evaluación salud mental laboral
    estres_percibido: int = Field(ge=1, le=10, description="Nivel estrés percibido (1-10)")
    carga_laboral: int = Field(ge=1, le=10, description="Carga laboral percibida (1-10)")
    satisfaccion_laboral: int = Field(ge=1, le=10, description="Satisfacción laboral (1-10)")
    conflictos_laborales: bool = Field(description="Presencia conflictos laborales")
    cambios_recientes_trabajo: bool = Field(description="Cambios recientes en el trabajo")
    sintomas_depresivos: bool = Field(description="Presencia síntomas depresivos")
    sintomas_ansiedad: bool = Field(description="Presencia síntomas ansiedad")
    
    # Factores de riesgo cardiovascular
    fumador: bool = Field(description="Es fumador activo")
    cigarrillos_dia: int = Field(ge=0, le=100, description="Cigarrillos por día")
    diabetes: bool = Field(description="Diagnóstico previo diabetes")
    hipertension: bool = Field(description="Diagnóstico previo hipertensión")
    antecedentes_familiares_cv: bool = Field(description="Antecedentes familiares cardiovasculares")
    
    # Estilos de vida
    actividad_fisica_min_semana: int = Field(ge=0, le=1000, description="Minutos actividad física/semana")
    porciones_frutas_verduras_dia: int = Field(ge=0, le=20, description="Porciones frutas/verduras día")
    copas_alcohol_semana: int = Field(ge=0, le=50, description="Copas alcohol por semana")
    horas_sueno_promedio: float = Field(ge=3, le=15, description="Horas sueño promedio")
    tecnicas_manejo_estres: bool = Field(description="Utiliza técnicas manejo estrés")
    
    # Evaluación riesgo ocupacional
    riesgo_ocupacional: RiesgoOcupacional = Field(description="Nivel riesgo ocupacional")
    exposicion_quimicos: bool = Field(default=False, description="Exposición a químicos")
    trabajo_turnos: bool = Field(default=False, description="Trabajo por turnos")
    carga_fisica_pesada: bool = Field(default=False, description="Carga física pesada")
    
    # Evaluación violencia intrafamiliar
    violencia_intrafamiliar: ViolenciaIntrafamiliar = Field(description="Indicadores violencia intrafamiliar")
    
    # Factores protectores sociales
    soporte_social_adecuado: bool = Field(description="Cuenta con soporte social adecuado")
    relaciones_familiares_satisfactorias: bool = Field(description="Relaciones familiares satisfactorias")
    control_medico_preventivo_regular: bool = Field(description="Control médico preventivo regular")
    
    # Observaciones y planes
    observaciones_generales: Optional[str] = Field(default=None, description="Observaciones generales")
    plan_promocion_prevencion: Optional[str] = Field(default=None, description="Plan promoción y prevención")
    educacion_estilos_vida: Optional[str] = Field(default=None, description="Educación estilos vida saludable")
    
    # Metadatos
    entorno: str = Field(default="CONSULTA_EXTERNA", description="Entorno de atención")

class AtencionAdultezCrear(AtencionAdultezBase):
    """Modelo para crear nueva atención adultez"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "paciente_id": "123e4567-e89b-12d3-a456-426614174000",
                "medico_id": "123e4567-e89b-12d3-a456-426614174001",
                "fecha_atencion": "2025-09-16",
                "edad_anos": 45,
                "peso_kg": 75.0,
                "talla_cm": 170.0,
                "presion_sistolica": 130.0,
                "presion_diastolica": 85.0,
                "frecuencia_cardiaca": 72,
                "glicemia_ayunas": 95.0,
                "colesterol_total": 200.0,
                "colesterol_hdl": 45.0,
                "estres_percibido": 6,
                "carga_laboral": 7,
                "satisfaccion_laboral": 6,
                "conflictos_laborales": False,
                "cambios_recientes_trabajo": False,
                "sintomas_depresivos": False,
                "sintomas_ansiedad": False,
                "fumador": False,
                "cigarrillos_dia": 0,
                "diabetes": False,
                "hipertension": False,
                "antecedentes_familiares_cv": True,
                "actividad_fisica_min_semana": 120,
                "porciones_frutas_verduras_dia": 3,
                "copas_alcohol_semana": 5,
                "horas_sueno_promedio": 7.5,
                "tecnicas_manejo_estres": True,
                "riesgo_ocupacional": "MODERADO",
                "exposicion_quimicos": False,
                "trabajo_turnos": False,
                "carga_fisica_pesada": False,
                "violencia_intrafamiliar": "SIN_INDICADORES",
                "soporte_social_adecuado": True,
                "relaciones_familiares_satisfactorias": True,
                "control_medico_preventivo_regular": True,
                "observaciones_generales": "Adulto con factores de riesgo moderados",
                "entorno": "CONSULTA_EXTERNA"
            }
        }
    )

class AtencionAdultezActualizar(BaseModel):
    """Modelo para actualizar atención adultez (campos opcionales)"""
    # Todos los campos opcionales para updates parciales
    peso_kg: Optional[float] = Field(default=None, gt=0, le=300)
    talla_cm: Optional[float] = Field(default=None, gt=0, le=250)
    presion_sistolica: Optional[float] = Field(default=None, ge=70, le=250)
    presion_diastolica: Optional[float] = Field(default=None, ge=40, le=150)
    frecuencia_cardiaca: Optional[int] = Field(default=None, ge=40, le=150)
    glicemia_ayunas: Optional[float] = Field(default=None, ge=50, le=500)
    colesterol_total: Optional[float] = Field(default=None, ge=100, le=600)
    colesterol_hdl: Optional[float] = Field(default=None, ge=20, le=150)
    estres_percibido: Optional[int] = Field(default=None, ge=1, le=10)
    carga_laboral: Optional[int] = Field(default=None, ge=1, le=10)
    satisfaccion_laboral: Optional[int] = Field(default=None, ge=1, le=10)
    conflictos_laborales: Optional[bool] = None
    sintomas_depresivos: Optional[bool] = None
    sintomas_ansiedad: Optional[bool] = None
    fumador: Optional[bool] = None
    cigarrillos_dia: Optional[int] = Field(default=None, ge=0, le=100)
    actividad_fisica_min_semana: Optional[int] = Field(default=None, ge=0, le=1000)
    porciones_frutas_verduras_dia: Optional[int] = Field(default=None, ge=0, le=20)
    tecnicas_manejo_estres: Optional[bool] = None
    riesgo_ocupacional: Optional[RiesgoOcupacional] = None
    violencia_intrafamiliar: Optional[ViolenciaIntrafamiliar] = None
    observaciones_generales: Optional[str] = None
    plan_promocion_prevencion: Optional[str] = None

class AtencionAdultezResponse(AtencionAdultezBase):
    """Modelo response con campos calculados automáticamente"""
    id: UUID = Field(description="ID único de la atención")
    atencion_id: Optional[UUID] = Field(default=None, description="ID de la atención general")
    
    # Campos calculados automáticamente
    imc: float = Field(description="Índice de masa corporal calculado")
    estado_nutricional: EstadoNutricionalAdulto = Field(description="Estado nutricional calculado")
    riesgo_framingham_porcentaje: float = Field(description="Riesgo cardiovascular Framingham (%)")
    riesgo_framingham_categoria: RiesgoCardiovascularFramingham = Field(description="Categoría riesgo Framingham")
    tamizaje_ecnt: TamizajeECNT = Field(description="Resultado tamizaje ECNT")
    salud_mental_laboral: SaludMentalLaboral = Field(description="Evaluación salud mental laboral")
    estilos_vida_saludable: EstilosVidaSaludable = Field(description="Evaluación estilos vida")
    factores_protectores_identificados: List[FactorProtectorAdulto] = Field(description="Factores protectores presentes")
    nivel_riesgo_global: NivelRiesgoGlobal = Field(description="Nivel riesgo global calculado")
    proxima_consulta_recomendada_dias: int = Field(description="Días hasta próxima consulta")
    completitud_evaluacion: float = Field(description="Porcentaje completitud evaluación (0-100)")
    
    # Metadatos de auditoría
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")

    @staticmethod
    def calcular_campos_automaticos(data: dict) -> dict:
        """Calcula todos los campos automáticos basados en los datos de entrada"""
        # Calcular IMC
        imc = data["peso_kg"] / ((data["talla_cm"] / 100) ** 2)
        data["imc"] = round(imc, 2)
        
        # Estado nutricional
        if imc < 18.5:
            data["estado_nutricional"] = EstadoNutricionalAdulto.PESO_BAJO
        elif imc < 25:
            data["estado_nutricional"] = EstadoNutricionalAdulto.NORMAL
        elif imc < 30:
            data["estado_nutricional"] = EstadoNutricionalAdulto.SOBREPESO
        elif imc < 35:
            data["estado_nutricional"] = EstadoNutricionalAdulto.OBESIDAD_GRADO_I
        elif imc < 40:
            data["estado_nutricional"] = EstadoNutricionalAdulto.OBESIDAD_GRADO_II
        else:
            data["estado_nutricional"] = EstadoNutricionalAdulto.OBESIDAD_GRADO_III
        
        # Determinar sexo basado en datos (simplificado - en producción vendría del paciente)
        sexo = "M"  # Placeholder - debería venir de la tabla pacientes
        
        # Riesgo cardiovascular Framingham
        riesgo_porcentaje, riesgo_categoria = calcular_riesgo_framingham(
            data["edad_anos"],
            sexo,
            data["colesterol_total"],
            data["colesterol_hdl"],
            data["presion_sistolica"],
            data["fumador"],
            data["diabetes"]
        )
        data["riesgo_framingham_porcentaje"] = riesgo_porcentaje
        data["riesgo_framingham_categoria"] = riesgo_categoria
        
        # Tamizaje ECNT
        data["tamizaje_ecnt"] = evaluar_tamizaje_ecnt(
            data["glicemia_ayunas"],
            data["presion_sistolica"],
            data["presion_diastolica"],
            data["colesterol_total"],
            imc
        )
        
        # Salud mental laboral
        data["salud_mental_laboral"] = evaluar_salud_mental_laboral(
            data["estres_percibido"],
            data["carga_laboral"],
            data["satisfaccion_laboral"],
            data["conflictos_laborales"],
            data["cambios_recientes_trabajo"],
            data["sintomas_depresivos"],
            data["sintomas_ansiedad"]
        )
        
        # Estilos de vida saludable
        data["estilos_vida_saludable"] = evaluar_estilos_vida_saludable(
            data["actividad_fisica_min_semana"],
            data["porciones_frutas_verduras_dia"],
            data["cigarrillos_dia"],
            data["copas_alcohol_semana"],
            data["horas_sueno_promedio"],
            data["tecnicas_manejo_estres"]
        )
        
        # Factores protectores
        data["factores_protectores_identificados"] = identificar_factores_protectores_adulto(
            data["actividad_fisica_min_semana"],
            data["porciones_frutas_verduras_dia"],
            data["cigarrillos_dia"],
            data["copas_alcohol_semana"],
            data["tecnicas_manejo_estres"],
            data["soporte_social_adecuado"],
            data["satisfaccion_laboral"],
            data["relaciones_familiares_satisfactorias"],
            data["control_medico_preventivo_regular"]
        )
        
        # Nivel riesgo global
        data["nivel_riesgo_global"] = calcular_nivel_riesgo_global(
            riesgo_porcentaje,
            data["tamizaje_ecnt"],
            data["salud_mental_laboral"],
            data["riesgo_ocupacional"],
            data["violencia_intrafamiliar"],
            data["estilos_vida_saludable"],
            data["factores_protectores_identificados"]
        )
        
        # Próxima consulta
        data["proxima_consulta_recomendada_dias"] = calcular_proxima_consulta_dias_adulto(
            data["nivel_riesgo_global"],
            data["edad_anos"],
            data["factores_protectores_identificados"],
            riesgo_porcentaje
        )
        
        # Completitud evaluación
        campos_obligatorios = [
            "peso_kg", "talla_cm", "presion_sistolica", "presion_diastolica",
            "glicemia_ayunas", "colesterol_total", "colesterol_hdl",
            "estres_percibido", "carga_laboral", "satisfaccion_laboral"
        ]
        
        campos_opcionales = [
            "colesterol_ldl", "trigliceridos", "plan_promocion_prevencion",
            "educacion_estilos_vida", "observaciones_generales"
        ]
        
        campos_completados = sum(1 for campo in campos_obligatorios if data.get(campo) is not None)
        campos_opcionales_completados = sum(1 for campo in campos_opcionales if data.get(campo))
        
        completitud = ((campos_completados / len(campos_obligatorios)) * 70) + \
                     ((campos_opcionales_completados / len(campos_opcionales)) * 30)
        
        data["completitud_evaluacion"] = round(completitud, 1)
        
        return data

# =============================================================================
# MODELOS ESTADÍSTICAS Y REPORTES  
# =============================================================================

class EstadisticasAdultezResponse(BaseModel):
    """Estadísticas básicas del módulo adultez"""
    total_atenciones: int
    distribuciones: dict
    promedios: dict
    alertas: dict

class ReporteRiesgoCardiovascularResponse(BaseModel):
    """Reporte especializado riesgo cardiovascular"""
    adultos_evaluados: int
    riesgo_alto_muy_alto: int
    factores_riesgo_prevalentes: List[dict]
    oportunidades_prevencion: List[dict]
    recomendaciones: List[str]