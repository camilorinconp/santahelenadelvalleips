# =============================================================================
# Modelo Atención Adolescencia y Juventud - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025  
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.3 y 3.3.4
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum

# =============================================================================
# ENUMS ESPECÍFICOS PARA ADOLESCENCIA Y JUVENTUD
# =============================================================================

class EstadoNutricionalAdolescencia(str, Enum):
    """Estado nutricional para adolescentes y jóvenes 12-29 años"""
    NORMAL = "NORMAL"
    DELGADEZ = "DELGADEZ"
    SOBREPESO = "SOBREPESO" 
    OBESIDAD_GRADO_I = "OBESIDAD_GRADO_I"
    OBESIDAD_GRADO_II = "OBESIDAD_GRADO_II"
    OBESIDAD_GRADO_III = "OBESIDAD_GRADO_III"

class DesarrolloPsicosocial(str, Enum):
    """Evaluación desarrollo psicosocial adolescente"""
    APROPIADO = "APROPIADO"
    RIESGO_LEVE = "RIESGO_LEVE"
    RIESGO_MODERADO = "RIESGO_MODERADO"
    RIESGO_ALTO = "RIESGO_ALTO"
    REQUIERE_INTERVENCION = "REQUIERE_INTERVENCION"

class RiesgoCardiovascular(str, Enum):
    """Nivel de riesgo cardiovascular temprano"""
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    MUY_ALTO = "MUY_ALTO"

class SaludSexualReproductiva(str, Enum):
    """Estado evaluación salud sexual y reproductiva"""
    NORMAL = "NORMAL"
    FACTORES_RIESGO = "FACTORES_RIESGO"
    REQUIERE_CONSEJERIA = "REQUIERE_CONSEJERIA"
    REQUIERE_TRATAMIENTO = "REQUIERE_TRATAMIENTO"
    NO_EVALUADO = "NO_EVALUADO"

class TrastornoAlimentario(str, Enum):
    """Riesgo de trastornos alimentarios"""
    SIN_RIESGO = "SIN_RIESGO"
    RIESGO_BAJO = "RIESGO_BAJO"
    RIESGO_MODERADO = "RIESGO_MODERADO"
    RIESGO_ALTO = "RIESGO_ALTO"
    DIAGNOSTICO_CONFIRMADO = "DIAGNOSTICO_CONFIRMADO"

class SaludMental(str, Enum):
    """Evaluación salud mental"""
    NORMAL = "NORMAL"
    SINTOMAS_LEVES = "SINTOMAS_LEVES"
    SINTOMAS_MODERADOS = "SINTOMAS_MODERADOS"
    SINTOMAS_SEVEROS = "SINTOMAS_SEVEROS"
    REQUIERE_ATENCION_ESPECIALIZADA = "REQUIERE_ATENCION_ESPECIALIZADA"

class ConsumoSustancias(str, Enum):
    """Evaluación consumo sustancias psicoactivas"""
    SIN_CONSUMO = "SIN_CONSUMO"
    CONSUMO_EXPERIMENTAL = "CONSUMO_EXPERIMENTAL"
    CONSUMO_OCASIONAL = "CONSUMO_OCASIONAL"
    CONSUMO_HABITUAL = "CONSUMO_HABITUAL"
    CONSUMO_PROBLEMATICO = "CONSUMO_PROBLEMATICO"

class ProyectoVida(str, Enum):
    """Evaluación proyecto de vida"""
    DEFINIDO = "DEFINIDO"
    EN_CONSTRUCCION = "EN_CONSTRUCCION"
    POCO_CLARO = "POCO_CLARO"
    AUSENTE = "AUSENTE"
    REQUIERE_ORIENTACION = "REQUIERE_ORIENTACION"

class NivelRiesgoIntegral(str, Enum):
    """Nivel de riesgo integral calculado"""
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    MUY_ALTO = "MUY_ALTO"
    CRITICO = "CRITICO"

class FactorProtector(str, Enum):
    """Factores protectores identificados"""
    FAMILIA_FUNCIONAL = "FAMILIA_FUNCIONAL"
    BUEN_RENDIMIENTO_ACADEMICO = "BUEN_RENDIMIENTO_ACADEMICO"
    ACTIVIDAD_FISICA_REGULAR = "ACTIVIDAD_FISICA_REGULAR"
    HABILIDADES_SOCIALES = "HABILIDADES_SOCIALES"
    PROYECTO_VIDA_CLARO = "PROYECTO_VIDA_CLARO"
    RED_APOYO_SOCIAL = "RED_APOYO_SOCIAL"
    AUTOESTIMA_ADECUADA = "AUTOESTIMA_ADECUADA"

# =============================================================================
# FUNCIONES CALCULADAS AUTOMÁTICAS
# =============================================================================

def calcular_riesgo_cardiovascular_temprano(
    presion_sistolica: float,
    presion_diastolica: float,
    imc: float,
    antecedentes_familiares: bool,
    fumador: bool,
    sedentarismo: bool
) -> RiesgoCardiovascular:
    """Calcula riesgo cardiovascular temprano según múltiples factores"""
    factores_riesgo = 0
    
    # Evaluación presión arterial
    if presion_sistolica >= 140 or presion_diastolica >= 90:
        factores_riesgo += 2
    elif presion_sistolica >= 130 or presion_diastolica >= 85:
        factores_riesgo += 1
    
    # Evaluación IMC
    if imc >= 30:
        factores_riesgo += 2
    elif imc >= 25:
        factores_riesgo += 1
    
    # Otros factores
    if antecedentes_familiares:
        factores_riesgo += 1
    if fumador:
        factores_riesgo += 2
    if sedentarismo:
        factores_riesgo += 1
    
    if factores_riesgo >= 6:
        return RiesgoCardiovascular.MUY_ALTO
    elif factores_riesgo >= 4:
        return RiesgoCardiovascular.ALTO
    elif factores_riesgo >= 2:
        return RiesgoCardiovascular.MODERADO
    else:
        return RiesgoCardiovascular.BAJO

def calcular_imc_edad(peso_kg: float, talla_cm: float, edad_anos: int) -> EstadoNutricionalAdolescencia:
    """Calcula estado nutricional según IMC adaptado por edad"""
    imc = peso_kg / ((talla_cm / 100) ** 2)
    
    # Puntos de corte ajustados por edad
    if edad_anos < 18:
        # Adolescentes
        if imc < 18.5:
            return EstadoNutricionalAdolescencia.DELGADEZ
        elif 18.5 <= imc < 25:
            return EstadoNutricionalAdolescencia.NORMAL
        elif 25 <= imc < 30:
            return EstadoNutricionalAdolescencia.SOBREPESO
        elif 30 <= imc < 35:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_I
        elif 35 <= imc < 40:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_II
        else:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_III
    else:
        # Jóvenes adultos
        if imc < 18.5:
            return EstadoNutricionalAdolescencia.DELGADEZ
        elif 18.5 <= imc < 25:
            return EstadoNutricionalAdolescencia.NORMAL
        elif 25 <= imc < 30:
            return EstadoNutricionalAdolescencia.SOBREPESO
        elif 30 <= imc < 35:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_I
        elif 35 <= imc < 40:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_II
        else:
            return EstadoNutricionalAdolescencia.OBESIDAD_GRADO_III

def evaluar_desarrollo_psicosocial(
    autoestima: int,  # Escala 1-10
    habilidades_sociales: int,  # Escala 1-10
    proyecto_vida: ProyectoVida,
    problemas_conductuales: bool,
    consumo_sustancias: ConsumoSustancias
) -> DesarrolloPsicosocial:
    """Evalúa desarrollo psicosocial integral"""
    puntuacion_base = (autoestima + habilidades_sociales) / 2
    
    # Ajustes por proyecto de vida
    if proyecto_vida == ProyectoVida.DEFINIDO:
        puntuacion_base += 1
    elif proyecto_vida == ProyectoVida.AUSENTE:
        puntuacion_base -= 2
    
    # Ajustes por problemas conductuales
    if problemas_conductuales:
        puntuacion_base -= 2
    
    # Ajustes por consumo sustancias
    if consumo_sustancias in [ConsumoSustancias.CONSUMO_HABITUAL, ConsumoSustancias.CONSUMO_PROBLEMATICO]:
        puntuacion_base -= 3
    elif consumo_sustancias == ConsumoSustancias.CONSUMO_OCASIONAL:
        puntuacion_base -= 1
    
    if puntuacion_base >= 8:
        return DesarrolloPsicosocial.APROPIADO
    elif puntuacion_base >= 6:
        return DesarrolloPsicosocial.RIESGO_LEVE
    elif puntuacion_base >= 4:
        return DesarrolloPsicosocial.RIESGO_MODERADO
    elif puntuacion_base >= 2:
        return DesarrolloPsicosocial.RIESGO_ALTO
    else:
        return DesarrolloPsicosocial.REQUIERE_INTERVENCION

def identificar_factores_protectores(
    familia_funcional: bool,
    rendimiento_academico: str,
    actividad_fisica_regular: bool,
    habilidades_sociales: int,
    proyecto_vida: ProyectoVida,
    red_apoyo_social: bool,
    autoestima: int
) -> List[FactorProtector]:
    """Identifica factores protectores presentes"""
    factores = []
    
    if familia_funcional:
        factores.append(FactorProtector.FAMILIA_FUNCIONAL)
    
    if rendimiento_academico in ["SUPERIOR", "ALTO"]:
        factores.append(FactorProtector.BUEN_RENDIMIENTO_ACADEMICO)
    
    if actividad_fisica_regular:
        factores.append(FactorProtector.ACTIVIDAD_FISICA_REGULAR)
    
    if habilidades_sociales >= 7:
        factores.append(FactorProtector.HABILIDADES_SOCIALES)
    
    if proyecto_vida == ProyectoVida.DEFINIDO:
        factores.append(FactorProtector.PROYECTO_VIDA_CLARO)
    
    if red_apoyo_social:
        factores.append(FactorProtector.RED_APOYO_SOCIAL)
    
    if autoestima >= 7:
        factores.append(FactorProtector.AUTOESTIMA_ADECUADA)
    
    return factores

def calcular_nivel_riesgo_integral(
    riesgo_cardiovascular: RiesgoCardiovascular,
    desarrollo_psicosocial: DesarrolloPsicosocial,
    salud_mental: SaludMental,
    consumo_sustancias: ConsumoSustancias,
    trastorno_alimentario: TrastornoAlimentario,
    factores_protectores: List[FactorProtector]
) -> NivelRiesgoIntegral:
    """Calcula nivel de riesgo integral considerando todos los factores"""
    puntuacion_riesgo = 0
    
    # Ponderación riesgo cardiovascular
    riesgo_cv_scores = {
        RiesgoCardiovascular.BAJO: 0,
        RiesgoCardiovascular.MODERADO: 1,
        RiesgoCardiovascular.ALTO: 2,
        RiesgoCardiovascular.MUY_ALTO: 3
    }
    puntuacion_riesgo += riesgo_cv_scores[riesgo_cardiovascular]
    
    # Ponderación desarrollo psicosocial
    desarrollo_scores = {
        DesarrolloPsicosocial.APROPIADO: 0,
        DesarrolloPsicosocial.RIESGO_LEVE: 1,
        DesarrolloPsicosocial.RIESGO_MODERADO: 2,
        DesarrolloPsicosocial.RIESGO_ALTO: 3,
        DesarrolloPsicosocial.REQUIERE_INTERVENCION: 4
    }
    puntuacion_riesgo += desarrollo_scores[desarrollo_psicosocial]
    
    # Ponderación salud mental
    salud_mental_scores = {
        SaludMental.NORMAL: 0,
        SaludMental.SINTOMAS_LEVES: 1,
        SaludMental.SINTOMAS_MODERADOS: 2,
        SaludMental.SINTOMAS_SEVEROS: 3,
        SaludMental.REQUIERE_ATENCION_ESPECIALIZADA: 4
    }
    puntuacion_riesgo += salud_mental_scores[salud_mental]
    
    # Ponderación consumo sustancias
    consumo_scores = {
        ConsumoSustancias.SIN_CONSUMO: 0,
        ConsumoSustancias.CONSUMO_EXPERIMENTAL: 0,
        ConsumoSustancias.CONSUMO_OCASIONAL: 1,
        ConsumoSustancias.CONSUMO_HABITUAL: 3,
        ConsumoSustancias.CONSUMO_PROBLEMATICO: 4
    }
    puntuacion_riesgo += consumo_scores[consumo_sustancias]
    
    # Ponderación trastorno alimentario
    trastorno_scores = {
        TrastornoAlimentario.SIN_RIESGO: 0,
        TrastornoAlimentario.RIESGO_BAJO: 0,
        TrastornoAlimentario.RIESGO_MODERADO: 1,
        TrastornoAlimentario.RIESGO_ALTO: 2,
        TrastornoAlimentario.DIAGNOSTICO_CONFIRMADO: 3
    }
    puntuacion_riesgo += trastorno_scores[trastorno_alimentario]
    
    # Ajuste por factores protectores
    num_factores_protectores = len(factores_protectores)
    if num_factores_protectores >= 5:
        puntuacion_riesgo -= 2
    elif num_factores_protectores >= 3:
        puntuacion_riesgo -= 1
    
    # No puede ser negativo
    puntuacion_riesgo = max(0, puntuacion_riesgo)
    
    if puntuacion_riesgo >= 12:
        return NivelRiesgoIntegral.CRITICO
    elif puntuacion_riesgo >= 9:
        return NivelRiesgoIntegral.MUY_ALTO
    elif puntuacion_riesgo >= 6:
        return NivelRiesgoIntegral.ALTO
    elif puntuacion_riesgo >= 3:
        return NivelRiesgoIntegral.MODERADO
    else:
        return NivelRiesgoIntegral.BAJO

def calcular_proxima_consulta_recomendada_dias(
    nivel_riesgo: NivelRiesgoIntegral,
    edad_anos: int,
    factores_protectores: List[FactorProtector]
) -> int:
    """Calcula días hasta próxima consulta según riesgo y edad"""
    base_dias = {
        NivelRiesgoIntegral.CRITICO: 15,
        NivelRiesgoIntegral.MUY_ALTO: 30,
        NivelRiesgoIntegral.ALTO: 60,
        NivelRiesgoIntegral.MODERADO: 90,
        NivelRiesgoIntegral.BAJO: 180
    }
    
    dias = base_dias[nivel_riesgo]
    
    # Ajuste por edad (adolescentes requieren mayor seguimiento)
    if edad_anos < 16:
        dias = int(dias * 0.8)
    elif edad_anos > 25:
        dias = int(dias * 1.2)
    
    # Ajuste por factores protectores
    if len(factores_protectores) >= 5:
        dias = int(dias * 1.3)
    elif len(factores_protectores) <= 1:
        dias = int(dias * 0.7)
    
    return dias

# =============================================================================
# MODELOS PYDANTIC - PATRÓN CREAR/ACTUALIZAR/RESPONSE
# =============================================================================

class AtencionAdolescenciaBase(BaseModel):
    """Modelo base para atención adolescencia y juventud"""
    # Datos básicos del paciente
    paciente_id: UUID = Field(description="ID del paciente")
    medico_id: UUID = Field(description="ID del médico que atiende")
    fecha_atencion: date = Field(description="Fecha de la atención")
    edad_anos: int = Field(ge=12, le=29, description="Edad en años (12-29)")
    
    # Datos antropométricos
    peso_kg: float = Field(gt=0, le=200, description="Peso en kilogramos")
    talla_cm: float = Field(gt=0, le=250, description="Talla en centímetros")
    
    # Signos vitales
    presion_sistolica: float = Field(ge=70, le=200, description="Presión sistólica")
    presion_diastolica: float = Field(ge=40, le=120, description="Presión diastólica")
    frecuencia_cardiaca: int = Field(ge=50, le=150, description="Frecuencia cardíaca")
    
    # Evaluación desarrollo psicosocial
    autoestima: int = Field(ge=1, le=10, description="Nivel autoestima (1-10)")
    habilidades_sociales: int = Field(ge=1, le=10, description="Habilidades sociales (1-10)")
    proyecto_vida: ProyectoVida = Field(description="Evaluación proyecto de vida")
    problemas_conductuales: bool = Field(description="Presencia problemas conductuales")
    
    # Salud sexual y reproductiva
    salud_sexual_reproductiva: SaludSexualReproductiva = Field(description="Estado SSR")
    inicio_vida_sexual: Optional[bool] = Field(default=None, description="Ha iniciado vida sexual")
    uso_anticonceptivos: Optional[bool] = Field(default=None, description="Usa métodos anticonceptivos")
    
    # Evaluación salud mental
    salud_mental: SaludMental = Field(description="Estado salud mental")
    episodios_depresivos: bool = Field(description="Antecedentes episodios depresivos")
    ansiedad_clinica: bool = Field(description="Presenta ansiedad clínica")
    
    # Consumo sustancias
    consumo_sustancias: ConsumoSustancias = Field(description="Nivel consumo sustancias")
    tipo_sustancias: Optional[str] = Field(default=None, description="Tipos de sustancias consumidas")
    
    # Trastornos alimentarios
    trastorno_alimentario: TrastornoAlimentario = Field(description="Riesgo trastorno alimentario")
    relacion_comida: Optional[str] = Field(default=None, description="Descripción relación con la comida")
    
    # Factores de riesgo y protección
    antecedentes_familiares_cardiovasculares: bool = Field(description="Antecedentes familiares CV")
    fumador: bool = Field(description="Es fumador")
    sedentarismo: bool = Field(description="Presenta sedentarismo")
    familia_funcional: bool = Field(description="Familia funcional")
    rendimiento_academico: str = Field(description="Nivel rendimiento académico")
    actividad_fisica_regular: bool = Field(description="Realiza actividad física regular")
    red_apoyo_social: bool = Field(description="Tiene red de apoyo social")
    
    # Observaciones y planes
    observaciones_generales: Optional[str] = Field(default=None, description="Observaciones generales")
    plan_intervencion: Optional[str] = Field(default=None, description="Plan de intervención")
    educacion_autocuidado: Optional[str] = Field(default=None, description="Educación en autocuidado brindada")
    
    # Metadatos
    entorno: str = Field(default="CONSULTA_EXTERNA", description="Entorno de atención")

class AtencionAdolescenciaCrear(AtencionAdolescenciaBase):
    """Modelo para crear nueva atención adolescencia"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "paciente_id": "123e4567-e89b-12d3-a456-426614174000",
                "medico_id": "123e4567-e89b-12d3-a456-426614174001", 
                "fecha_atencion": "2025-09-16",
                "edad_anos": 16,
                "peso_kg": 60.5,
                "talla_cm": 165.0,
                "presion_sistolica": 110.0,
                "presion_diastolica": 70.0,
                "frecuencia_cardiaca": 75,
                "autoestima": 7,
                "habilidades_sociales": 8,
                "proyecto_vida": "EN_CONSTRUCCION",
                "problemas_conductuales": False,
                "salud_sexual_reproductiva": "NORMAL",
                "salud_mental": "NORMAL",
                "episodios_depresivos": False,
                "ansiedad_clinica": False,
                "consumo_sustancias": "SIN_CONSUMO",
                "trastorno_alimentario": "SIN_RIESGO",
                "antecedentes_familiares_cardiovasculares": False,
                "fumador": False,
                "sedentarismo": True,
                "familia_funcional": True,
                "rendimiento_academico": "ALTO",
                "actividad_fisica_regular": False,
                "red_apoyo_social": True,
                "observaciones_generales": "Adolescente con buen estado general",
                "entorno": "CONSULTA_EXTERNA"
            }
        }
    )

class AtencionAdolescenciaActualizar(BaseModel):
    """Modelo para actualizar atención adolescencia (campos opcionales)"""
    # Todos los campos opcionales para updates parciales
    peso_kg: Optional[float] = Field(default=None, gt=0, le=200)
    talla_cm: Optional[float] = Field(default=None, gt=0, le=250)
    presion_sistolica: Optional[float] = Field(default=None, ge=70, le=200)
    presion_diastolica: Optional[float] = Field(default=None, ge=40, le=120)
    frecuencia_cardiaca: Optional[int] = Field(default=None, ge=50, le=150)
    autoestima: Optional[int] = Field(default=None, ge=1, le=10)
    habilidades_sociales: Optional[int] = Field(default=None, ge=1, le=10)
    proyecto_vida: Optional[ProyectoVida] = None
    problemas_conductuales: Optional[bool] = None
    salud_sexual_reproductiva: Optional[SaludSexualReproductiva] = None
    inicio_vida_sexual: Optional[bool] = None
    uso_anticonceptivos: Optional[bool] = None
    salud_mental: Optional[SaludMental] = None
    episodios_depresivos: Optional[bool] = None
    ansiedad_clinica: Optional[bool] = None
    consumo_sustancias: Optional[ConsumoSustancias] = None
    tipo_sustancias: Optional[str] = None
    trastorno_alimentario: Optional[TrastornoAlimentario] = None
    relacion_comida: Optional[str] = None
    antecedentes_familiares_cardiovasculares: Optional[bool] = None
    fumador: Optional[bool] = None
    sedentarismo: Optional[bool] = None
    familia_funcional: Optional[bool] = None
    rendimiento_academico: Optional[str] = None
    actividad_fisica_regular: Optional[bool] = None
    red_apoyo_social: Optional[bool] = None
    observaciones_generales: Optional[str] = None
    plan_intervencion: Optional[str] = None
    educacion_autocuidado: Optional[str] = None

class AtencionAdolescenciaResponse(AtencionAdolescenciaBase):
    """Modelo response con campos calculados automáticamente"""
    id: UUID = Field(description="ID único de la atención")
    atencion_id: Optional[UUID] = Field(default=None, description="ID de la atención general")
    
    # Campos calculados automáticamente
    imc: float = Field(description="Índice de masa corporal calculado")
    estado_nutricional: EstadoNutricionalAdolescencia = Field(description="Estado nutricional calculado")
    riesgo_cardiovascular_temprano: RiesgoCardiovascular = Field(description="Riesgo cardiovascular calculado")
    desarrollo_psicosocial_apropiado: DesarrolloPsicosocial = Field(description="Desarrollo psicosocial evaluado")
    factores_protectores_identificados: List[FactorProtector] = Field(description="Factores protectores encontrados")
    nivel_riesgo_integral: NivelRiesgoIntegral = Field(description="Nivel de riesgo integral calculado")
    proxima_consulta_recomendada_dias: int = Field(description="Días hasta próxima consulta recomendada")
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
        data["estado_nutricional"] = calcular_imc_edad(
            data["peso_kg"], 
            data["talla_cm"], 
            data["edad_anos"]
        )
        
        # Riesgo cardiovascular
        data["riesgo_cardiovascular_temprano"] = calcular_riesgo_cardiovascular_temprano(
            data["presion_sistolica"],
            data["presion_diastolica"], 
            imc,
            data["antecedentes_familiares_cardiovasculares"],
            data["fumador"],
            data["sedentarismo"]
        )
        
        # Desarrollo psicosocial
        data["desarrollo_psicosocial_apropiado"] = evaluar_desarrollo_psicosocial(
            data["autoestima"],
            data["habilidades_sociales"],
            data["proyecto_vida"],
            data["problemas_conductuales"],
            data["consumo_sustancias"]
        )
        
        # Factores protectores
        data["factores_protectores_identificados"] = identificar_factores_protectores(
            data["familia_funcional"],
            data["rendimiento_academico"],
            data["actividad_fisica_regular"],
            data["habilidades_sociales"],
            data["proyecto_vida"],
            data["red_apoyo_social"],
            data["autoestima"]
        )
        
        # Nivel riesgo integral
        data["nivel_riesgo_integral"] = calcular_nivel_riesgo_integral(
            data["riesgo_cardiovascular_temprano"],
            data["desarrollo_psicosocial_apropiado"],
            data["salud_mental"],
            data["consumo_sustancias"],
            data["trastorno_alimentario"],
            data["factores_protectores_identificados"]
        )
        
        # Próxima consulta
        data["proxima_consulta_recomendada_dias"] = calcular_proxima_consulta_recomendada_dias(
            data["nivel_riesgo_integral"],
            data["edad_anos"],
            data["factores_protectores_identificados"]
        )
        
        # Completitud evaluación
        campos_obligatorios = [
            "peso_kg", "talla_cm", "presion_sistolica", "presion_diastolica",
            "autoestima", "habilidades_sociales", "salud_mental", "consumo_sustancias",
            "trastorno_alimentario", "proyecto_vida"
        ]
        
        campos_opcionales = [
            "inicio_vida_sexual", "uso_anticonceptivos", "tipo_sustancias",
            "relacion_comida", "observaciones_generales", "plan_intervencion"
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

class EstadisticasAdolescenciaResponse(BaseModel):
    """Estadísticas básicas del módulo adolescencia"""
    total_atenciones: int
    distribuciones: dict
    promedios: dict
    alertas: dict

class ReporteDesarrolloAdolescenciaResponse(BaseModel):
    """Reporte desarrollo psicosocial adolescencia"""
    adolescentes_evaluados: int
    desarrollo_apropiado: int
    factores_riesgo_prevalentes: List[dict]
    factores_protectores_prevalentes: List[dict] 
    recomendaciones: List[str]