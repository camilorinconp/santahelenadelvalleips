# =============================================================================
# Modelo Atención Vejez - SINCRONIZADO CON MIGRACIÓN REAL
# Fecha: 17 septiembre 2025 - CORRECCIÓN CRÍTICA
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
# Migración Base: 20250917120000_create_atencion_vejez_table.sql
# =============================================================================

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from uuid import UUID

# =============================================================================
# MODELOS SINCRONIZADOS CON MIGRACIÓN REAL
# =============================================================================

class AtencionVejezCrear(BaseModel):
    """Modelo para crear nueva atención de vejez - SINCRONIZADO CON BD REAL"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # === CAMPOS BÁSICOS OBLIGATORIOS ===
    paciente_id: UUID = Field(..., description="ID del paciente (60+ años)")
    medico_id: UUID = Field(..., description="ID del médico tratante")
    fecha_atencion: date = Field(..., description="Fecha de la atención geriátrica")
    edad_anos: int = Field(..., ge=60, le=120, description="Edad en años (60+ obligatorio)")
    entorno: str = Field("CONSULTA_EXTERNA", description="Entorno de atención")

    # === ANTROPOMETRÍA Y SIGNOS VITALES ===
    peso_kg: Optional[float] = Field(None, gt=0, le=200, description="Peso en kilogramos")
    talla_cm: Optional[float] = Field(None, gt=0, le=250, description="Talla en centímetros")
    peso_perdido_6_meses_kg: Optional[float] = Field(None, ge=0, le=50, description="Peso perdido en 6 meses")
    presion_sistolica: Optional[float] = Field(None, ge=70, le=250, description="Presión sistólica")
    presion_diastolica: Optional[float] = Field(None, ge=40, le=150, description="Presión diastólica")
    frecuencia_cardiaca: Optional[int] = Field(None, ge=40, le=150, description="Frecuencia cardíaca")

    # === EVALUACIÓN COGNITIVA (Mini Mental State - Anexo 28 Resolución 3280) ===
    mini_mental_score: Optional[int] = Field(None, ge=0, le=30, description="Puntaje Mini Mental State")
    clock_test_score: Optional[int] = Field(None, ge=0, le=10, description="Puntaje test del reloj")
    memoria_inmediata: bool = Field(True, description="Memoria inmediata conservada")
    orientacion_tiempo_lugar: bool = Field(True, description="Orientación temporal y espacial")
    cambios_cognitivos_reportados: bool = Field(False, description="Cambios cognitivos reportados")
    dificultad_actividades_complejas: bool = Field(False, description="Dificultad en actividades complejas")

    # === EVALUACIÓN RIESGO DE CAÍDAS ===
    caidas_ultimo_ano: Optional[int] = Field(None, ge=0, le=50, description="Número de caídas último año")
    mareo_al_levantarse: bool = Field(False, description="Mareo al levantarse")
    medicamentos_que_causan_mareo: Optional[int] = Field(None, ge=0, le=20, description="Medicamentos que causan mareo")
    problemas_vision: bool = Field(False, description="Problemas de visión")
    problemas_audicion: bool = Field(False, description="Problemas de audición")
    fuerza_muscular_disminuida: bool = Field(False, description="Fuerza muscular disminuida")
    equilibrio_alterado: bool = Field(False, description="Equilibrio alterado")
    tiempo_up_and_go: Optional[float] = Field(None, ge=0, le=120, description="Tiempo Up and Go en segundos")

    # === EVALUACIÓN AUTONOMÍA FUNCIONAL ===
    # Resolución 3280: "El índice de Barthel (Anexo 25)" y "La escala de Lawton-Brody (Anexo 26)"
    barthel_score: Optional[int] = Field(None, ge=0, le=100, description="Índice de Barthel (obligatorio Res. 3280)")
    lawton_score: Optional[int] = Field(None, ge=0, le=8, description="Escala Lawton-Brody (obligatorio Res. 3280)")
    independiente_bano: bool = Field(True, description="Independiente para el baño")
    independiente_vestirse: bool = Field(True, description="Independiente para vestirse")
    independiente_comer: bool = Field(True, description="Independiente para comer")
    independiente_movilidad: bool = Field(True, description="Independiente para movilidad")
    maneja_medicamentos: bool = Field(True, description="Maneja medicamentos independientemente")
    maneja_finanzas: bool = Field(True, description="Maneja finanzas independientemente")
    usa_transporte: bool = Field(True, description="Usa transporte independientemente")

    # === EVALUACIÓN SALUD MENTAL ===
    yesavage_score: Optional[int] = Field(None, ge=0, le=15, description="Escala Yesavage depresión")
    estado_animo_deprimido: bool = Field(False, description="Estado de ánimo deprimido")
    perdida_interes_actividades: bool = Field(False, description="Pérdida de interés en actividades")
    trastornos_sueno: bool = Field(False, description="Trastornos del sueño")
    sensacion_inutilidad: bool = Field(False, description="Sensación de inutilidad")
    ansiedad_frecuente: bool = Field(False, description="Ansiedad frecuente")
    aislamiento_social: bool = Field(False, description="Aislamiento social")
    cambios_recientes_perdidas: bool = Field(False, description="Cambios recientes o pérdidas")

    # === EVALUACIÓN SOPORTE SOCIAL ===
    vive_solo: bool = Field(False, description="Vive solo")
    tiene_cuidador: bool = Field(False, description="Tiene cuidador")
    frecuencia_visitas_familiares: Optional[int] = Field(None, ge=0, le=30, description="Visitas familiares por mes")
    participa_actividades_comunitarias: bool = Field(False, description="Participa en actividades comunitarias")
    tiene_amigos_cercanos: bool = Field(False, description="Tiene amigos cercanos")
    ayuda_disponible_emergencia: bool = Field(False, description="Ayuda disponible en emergencias")
    satisfaccion_relaciones_sociales: Optional[int] = Field(None, ge=1, le=10, description="Satisfacción relaciones sociales (1-10)")

    # === EVALUACIÓN POLIFARMACIA ===
    numero_medicamentos: Optional[int] = Field(None, ge=0, le=30, description="Número total de medicamentos")
    medicamentos_alto_riesgo: Optional[int] = Field(None, ge=0, le=10, description="Medicamentos de alto riesgo")
    automedicacion: bool = Field(False, description="Práctica de automedicación")
    dificultad_manejo_medicamentos: bool = Field(False, description="Dificultad para manejar medicamentos")
    efectos_adversos_reportados: bool = Field(False, description="Efectos adversos reportados")
    interacciones_conocidas: bool = Field(False, description="Interacciones medicamentosas conocidas")

    # === INCONTINENCIA ===
    incontinencia_urinaria: bool = Field(False, description="Incontinencia urinaria")
    incontinencia_fecal: bool = Field(False, description="Incontinencia fecal")

    # === ESTILOS DE VIDA ===
    actividad_fisica_min_semana: Optional[int] = Field(None, ge=0, le=500, description="Minutos actividad física por semana")
    porciones_frutas_verduras_dia: Optional[int] = Field(None, ge=0, le=20, description="Porciones frutas y verduras por día")
    cigarrillos_dia: Optional[int] = Field(None, ge=0, le=100, description="Cigarrillos por día")
    copas_alcohol_semana: Optional[int] = Field(None, ge=0, le=50, description="Copas de alcohol por semana")
    actividades_estimulacion_cognitiva: bool = Field(False, description="Realiza actividades de estimulación cognitiva")

    # === FACTORES AMBIENTALES Y SOCIALES ===
    hogar_adaptado_seguro: bool = Field(False, description="Hogar adaptado y seguro")
    proposito_vida_claro: bool = Field(False, description="Propósito de vida claro")
    participacion_social_activa: bool = Field(False, description="Participación social activa")
    control_medico_regular: bool = Field(False, description="Control médico regular")


class AtencionVejezActualizar(BaseModel):
    """Modelo para actualizar atención de vejez - SINCRONIZADO CON BD REAL"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # Todos los campos opcionales para actualización
    edad_anos: Optional[int] = Field(None, ge=60, le=120)
    entorno: Optional[str] = None
    peso_kg: Optional[float] = Field(None, gt=0, le=200)
    talla_cm: Optional[float] = Field(None, gt=0, le=250)
    peso_perdido_6_meses_kg: Optional[float] = Field(None, ge=0, le=50)
    presion_sistolica: Optional[float] = Field(None, ge=70, le=250)
    presion_diastolica: Optional[float] = Field(None, ge=40, le=150)
    frecuencia_cardiaca: Optional[int] = Field(None, ge=40, le=150)
    mini_mental_score: Optional[int] = Field(None, ge=0, le=30)
    clock_test_score: Optional[int] = Field(None, ge=0, le=10)
    memoria_inmediata: Optional[bool] = None
    orientacion_tiempo_lugar: Optional[bool] = None
    cambios_cognitivos_reportados: Optional[bool] = None
    dificultad_actividades_complejas: Optional[bool] = None
    barthel_score: Optional[int] = Field(None, ge=0, le=100)
    lawton_score: Optional[int] = Field(None, ge=0, le=8)
    yesavage_score: Optional[int] = Field(None, ge=0, le=15)
    numero_medicamentos: Optional[int] = Field(None, ge=0, le=30)


class AtencionVejezResponse(BaseModel):
    """Modelo de respuesta - SINCRONIZADO CON BD REAL"""
    model_config = ConfigDict(from_attributes=True)

    # Campos básicos
    id: UUID
    paciente_id: UUID
    medico_id: UUID
    fecha_atencion: date
    edad_anos: int
    entorno: str

    # Campos de evaluación (opcionales en respuesta)
    peso_kg: Optional[float] = None
    talla_cm: Optional[float] = None
    mini_mental_score: Optional[int] = None
    barthel_score: Optional[int] = None
    lawton_score: Optional[int] = None
    yesavage_score: Optional[int] = None
    numero_medicamentos: Optional[int] = None

    # Campos calculados automáticamente (si están disponibles)
    imc: Optional[float] = None