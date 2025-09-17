# =============================================================================
# Rutas Atención Vejez - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 17 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
# Resolución 202 de 2021 - Variables 16-17 (Test Vejez)
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from database import get_supabase_client
from models.atencion_vejez_model import (
    AtencionVejezCrear,
    AtencionVejezActualizar,
    AtencionVejezResponse,
    EstadoFuncionalVejez,
    EstadoCognitivoVejez,
    SindromeFragilidad,
    RiesgoCaidaVejez,
    calcular_indice_katz,
    calcular_escala_lawton_brody,
    calcular_riesgo_fragilidad,
    interpretar_mini_mental,
    generar_alertas_vejez
)

router = APIRouter(prefix="/atencion-vejez", tags=["Atención Vejez"])

# =============================================================================
# FUNCIONES HELPER ESPECÍFICAS PARA VEJEZ
# =============================================================================

def calcular_campos_automaticos_vejez(atencion_data: dict) -> dict:
    """Calcular todos los campos automáticos específicos para vejez"""

    # 1. Calcular Índice de Katz (Actividades Básicas)
    indice_katz = calcular_indice_katz(
        atencion_data.get("katz_banarse", False),
        atencion_data.get("katz_vestirse", False),
        atencion_data.get("katz_usar_inodoro", False),
        atencion_data.get("katz_movilizarse", False),
        atencion_data.get("katz_continencia", False),
        atencion_data.get("katz_alimentarse", False)
    )
    atencion_data["indice_katz"] = indice_katz

    # 2. Calcular Escala Lawton-Brody (Actividades Instrumentales)
    escala_lawton = calcular_escala_lawton_brody(
        atencion_data.get("lawton_usar_telefono", 0),
        atencion_data.get("lawton_hacer_compras", 0),
        atencion_data.get("lawton_preparar_comida", 0),
        atencion_data.get("lawton_cuidar_casa", 0),
        atencion_data.get("lawton_lavar_ropa", 0),
        atencion_data.get("lawton_usar_transporte", 0),
        atencion_data.get("lawton_manejar_medicamentos", 0),
        atencion_data.get("lawton_manejar_dinero", 0)
    )
    atencion_data["escala_lawton_brody"] = escala_lawton

    # 3. Determinar Estado Funcional Global
    if indice_katz >= 5 and escala_lawton >= 7:
        estado_funcional = EstadoFuncionalVejez.INDEPENDIENTE
    elif indice_katz == 4 or (escala_lawton >= 4 and escala_lawton <= 6):
        estado_funcional = EstadoFuncionalVejez.DEPENDENCIA_LEVE
    elif indice_katz <= 3 and indice_katz >= 2:
        estado_funcional = EstadoFuncionalVejez.DEPENDENCIA_MODERADA
    else:
        estado_funcional = EstadoFuncionalVejez.DEPENDENCIA_SEVERA
    atencion_data["estado_funcional"] = estado_funcional.value

    # 4. Interpretar Estado Cognitivo
    mini_mental_puntaje = atencion_data.get("mini_mental_puntaje")
    if mini_mental_puntaje is not None:
        estado_cognitivo = interpretar_mini_mental(mini_mental_puntaje)
    else:
        estado_cognitivo = EstadoCognitivoVejez.RIESGO_NO_EVALUADO
    atencion_data["estado_cognitivo"] = estado_cognitivo.value

    # 5. Calcular Síndrome de Fragilidad
    sindrome_fragilidad = calcular_riesgo_fragilidad(
        atencion_data.get("fragilidad_perdida_peso", False),
        atencion_data.get("fragilidad_agotamiento", False),
        atencion_data.get("fragilidad_debilidad", False),
        atencion_data.get("fragilidad_lentitud", False),
        atencion_data.get("fragilidad_actividad_baja", False)
    )
    atencion_data["sindrome_fragilidad"] = sindrome_fragilidad.value

    # 6. Calcular IMC si hay datos
    peso = atencion_data.get("peso_actual")
    talla = atencion_data.get("talla")
    if peso and talla and talla > 0:
        imc = peso / (talla ** 2)
        atencion_data["imc"] = round(imc, 2)
    else:
        atencion_data["imc"] = None

    # 7. Evaluar Riesgo Nutricional
    from models.atencion_vejez_model import RiesgoNutricionalVejez
    imc = atencion_data.get("imc")
    if imc:
        if imc < 18.5:
            riesgo_nutricional = RiesgoNutricionalVejez.DESNUTRICION
        elif imc < 22:
            riesgo_nutricional = RiesgoNutricionalVejez.RIESGO_ALTO
        elif imc < 27:
            riesgo_nutricional = RiesgoNutricionalVejez.NORMAL
        else:
            riesgo_nutricional = RiesgoNutricionalVejez.RIESGO_MODERADO
    else:
        riesgo_nutricional = RiesgoNutricionalVejez.RIESGO_MODERADO
    atencion_data["riesgo_nutricional"] = riesgo_nutricional.value

    # 8. Calcular Riesgo de Caídas
    caidas = atencion_data.get("caidas_ultimo_ano", 0)
    medicamentos_riesgo = atencion_data.get("medicamentos_riesgo", 0)
    alteraciones_vision = atencion_data.get("alteraciones_vision", False)

    score_caidas = 0
    if caidas >= 2: score_caidas += 2
    elif caidas == 1: score_caidas += 1
    if medicamentos_riesgo >= 4: score_caidas += 2
    elif medicamentos_riesgo >= 2: score_caidas += 1
    if alteraciones_vision: score_caidas += 1
    if atencion_data.get("miedo_caerse", False): score_caidas += 1

    if score_caidas >= 5:
        riesgo_caida = RiesgoCaidaVejez.MUY_ALTO
    elif score_caidas >= 3:
        riesgo_caida = RiesgoCaidaVejez.ALTO
    elif score_caidas >= 1:
        riesgo_caida = RiesgoCaidaVejez.MODERADO
    else:
        riesgo_caida = RiesgoCaidaVejez.BAJO
    atencion_data["riesgo_caida"] = riesgo_caida.value

    # 9. Evaluar Riesgo de Maltrato
    from models.atencion_vejez_model import RiesgoMaltrato
    score_maltrato = 0
    if atencion_data.get("indicadores_maltrato_fisico", False): score_maltrato += 3
    if atencion_data.get("indicadores_maltrato_psicologico", False): score_maltrato += 2
    if atencion_data.get("indicadores_negligencia", False): score_maltrato += 2
    if atencion_data.get("indicadores_abandono", False): score_maltrato += 3
    if atencion_data.get("indicadores_abuso_financiero", False): score_maltrato += 2

    if score_maltrato >= 6:
        riesgo_maltrato = RiesgoMaltrato.SITUACION_CONFIRMADA
    elif score_maltrato >= 4:
        riesgo_maltrato = RiesgoMaltrato.ALTO_RIESGO
    elif score_maltrato >= 2:
        riesgo_maltrato = RiesgoMaltrato.INDICADORES_MODERADOS
    elif score_maltrato >= 1:
        riesgo_maltrato = RiesgoMaltrato.INDICADORES_LEVES
    else:
        riesgo_maltrato = RiesgoMaltrato.SIN_RIESGO
    atencion_data["riesgo_maltrato"] = riesgo_maltrato.value

    # 10. Evaluar Calidad de Vida
    from models.atencion_vejez_model import CalidadVidaVejez
    score_calidad = 0
    if estado_funcional == EstadoFuncionalVejez.INDEPENDIENTE: score_calidad += 3
    elif estado_funcional == EstadoFuncionalVejez.DEPENDENCIA_LEVE: score_calidad += 2
    elif estado_funcional == EstadoFuncionalVejez.DEPENDENCIA_MODERADA: score_calidad += 1

    if not atencion_data.get("sintomas_depresivos", False): score_calidad += 2
    if not atencion_data.get("aislamiento_social", False): score_calidad += 1
    if sindrome_fragilidad == SindromeFragilidad.ROBUSTO: score_calidad += 2

    if score_calidad >= 7:
        calidad_vida = CalidadVidaVejez.EXCELENTE
    elif score_calidad >= 5:
        calidad_vida = CalidadVidaVejez.BUENA
    elif score_calidad >= 3:
        calidad_vida = CalidadVidaVejez.REGULAR
    elif score_calidad >= 1:
        calidad_vida = CalidadVidaVejez.DEFICIENTE
    else:
        calidad_vida = CalidadVidaVejez.CRITICA
    atencion_data["calidad_vida"] = calidad_vida.value

    # 11. Planificación de Cuidados
    from models.atencion_vejez_model import PlanificacionCuidadosPaliativos
    if atencion_data.get("requiere_cuidados_paliativos", False):
        planificacion = PlanificacionCuidadosPaliativos.CUIDADOS_PALIATIVOS_ACTIVOS
    elif sindrome_fragilidad == SindromeFragilidad.FRAGIL:
        planificacion = PlanificacionCuidadosPaliativos.EVALUACION_ESPECIALIZADA
    elif estado_funcional in [EstadoFuncionalVejez.DEPENDENCIA_MODERADA, EstadoFuncionalVejez.DEPENDENCIA_SEVERA]:
        planificacion = PlanificacionCuidadosPaliativos.ORIENTACION_INICIAL
    else:
        planificacion = PlanificacionCuidadosPaliativos.NO_REQUIERE
    atencion_data["planificacion_cuidados"] = planificacion.value

    # 12. Generar Alertas Automáticas
    alertas = generar_alertas_vejez(
        EstadoFuncionalVejez(estado_funcional),
        EstadoCognitivoVejez(estado_cognitivo),
        sindrome_fragilidad,
        riesgo_caida,
        RiesgoMaltrato(riesgo_maltrato)
    )
    atencion_data["alertas_generadas"] = alertas

    return atencion_data

def agregar_metadatos_auditoria(data: dict) -> dict:
    """Agregar metadatos de auditoría"""
    now = datetime.now()
    data["creado_en"] = now.isoformat()
    data["updated_at"] = now.isoformat()
    return data

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - PATRÓN VERTICAL CONSOLIDADO
# =============================================================================

@router.post("/", response_model=AtencionVejezResponse, status_code=201)
async def crear_atencion_vejez(
    atencion_data: AtencionVejezCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nueva atención vejez con patrón polimórfico 3 pasos:
    1. Crear en tabla específica atencion_vejez
    2. Crear atención general con referencia
    3. Actualizar atencion_vejez con atencion_id
    """
    try:
        # PASO 1: Preparar datos y crear registro específico (sin atencion_id)
        atencion_dict = atencion_data.model_dump()
        atencion_dict["id"] = str(uuid4())
        atencion_dict = agregar_metadatos_auditoria(atencion_dict)

        # Calcular campos automáticos específicos para vejez
        atencion_dict = calcular_campos_automaticos_vejez(atencion_dict)

        # Crear en tabla atencion_vejez (sin atencion_id)
        atencion_dict_sin_atencion = atencion_dict.copy()
        if 'atencion_id' in atencion_dict_sin_atencion:
            del atencion_dict_sin_atencion['atencion_id']

        response_vejez = db.table("atencion_vejez").insert(atencion_dict_sin_atencion).execute()

        if not response_vejez.data:
            raise HTTPException(status_code=500, detail="Error creando atención vejez")

        vejez_id = response_vejez.data[0]["id"]

        # PASO 2: Crear atención general
        atencion_general = {
            "id": str(uuid4()),
            "paciente_id": str(atencion_data.paciente_id),
            "medico_id": str(atencion_data.medico_id),
            "tipo_atencion": "VEJEZ",
            "detalle_id": vejez_id,
            "fecha_atencion": atencion_data.fecha_atencion.isoformat(),
            "creado_en": datetime.now().isoformat()
        }

        response_general = db.table("atenciones").insert(atencion_general).execute()

        if not response_general.data:
            # Rollback: eliminar registro de vejez
            db.table("atencion_vejez").delete().eq("id", vejez_id).execute()
            raise HTTPException(status_code=500, detail="Error creando atención general")

        atencion_id = response_general.data[0]["id"]

        # PASO 3: Actualizar vejez con atencion_id
        update_response = db.table("atencion_vejez").update({
            "atencion_id": atencion_id,
            "updated_at": datetime.now().isoformat()
        }).eq("id", vejez_id).execute()

        if not update_response.data:
            # Rollback completo
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            db.table("atencion_vejez").delete().eq("id", vejez_id).execute()
            raise HTTPException(status_code=500, detail="Error actualizando referencia")

        # Obtener registro completo para respuesta
        final_response = db.table("atencion_vejez").select("*").eq("id", vejez_id).execute()

        if not final_response.data:
            raise HTTPException(status_code=500, detail="Error obteniendo registro final")

        return AtencionVejezResponse.model_validate(final_response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{atencion_id}", response_model=AtencionVejezResponse)
async def obtener_atencion_vejez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener atención de vejez por ID"""
    try:
        response = db.table("atencion_vejez").select("*").eq("id", str(atencion_id)).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Atención de vejez no encontrada")

        return AtencionVejezResponse.model_validate(response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.put("/{atencion_id}", response_model=AtencionVejezResponse)
async def actualizar_atencion_vejez(
    atencion_id: UUID,
    atencion_data: AtencionVejezActualizar,
    db=Depends(get_supabase_client)
):
    """Actualizar atención de vejez"""
    try:
        # Verificar que existe
        existing = db.table("atencion_vejez").select("*").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Atención de vejez no encontrada")

        # Preparar datos actualizados (solo campos no nulos)
        update_data = {k: v for k, v in atencion_data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now().isoformat()

        # Combinar con datos existentes para recalcular campos automáticos
        existing_data = existing.data[0]
        combined_data = {**existing_data, **update_data}
        combined_data = calcular_campos_automaticos_vejez(combined_data)

        # Actualizar solo campos específicos (excluir metadatos de auditoría calculados)
        campos_actualizables = {k: v for k, v in combined_data.items()
                              if k not in ["id", "paciente_id", "medico_id", "creado_en"]}

        response = db.table("atencion_vejez").update(campos_actualizables).eq("id", str(atencion_id)).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Error actualizando atención")

        return AtencionVejezResponse.model_validate(response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.delete("/{atencion_id}")
async def eliminar_atencion_vejez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Eliminar atención de vejez (soft delete)"""
    try:
        # Primero obtener atencion_id asociado
        vejez_data = db.table("atencion_vejez").select("atencion_id").eq("id", str(atencion_id)).execute()

        if not vejez_data.data:
            raise HTTPException(status_code=404, detail="Atención de vejez no encontrada")

        general_atencion_id = vejez_data.data[0].get("atencion_id")

        # Eliminar de tabla específica
        response_vejez = db.table("atencion_vejez").delete().eq("id", str(atencion_id)).execute()

        # Eliminar de tabla general si existe referencia
        if general_atencion_id:
            db.table("atenciones").delete().eq("id", general_atencion_id).execute()

        return {"message": "Atención de vejez eliminada exitosamente"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# =============================================================================
# ENDPOINTS ESPECIALIZADOS PARA VEJEZ
# =============================================================================

@router.get("/paciente/{paciente_id}/cronologico", response_model=List[AtencionVejezResponse])
async def obtener_atenciones_cronologicas_vejez(
    paciente_id: UUID,
    limite: int = Query(10, le=50, description="Límite de registros"),
    db=Depends(get_supabase_client)
):
    """Obtener atenciones de vejez por paciente en orden cronológico"""
    try:
        response = db.table("atencion_vejez") \
                    .select("*") \
                    .eq("paciente_id", str(paciente_id)) \
                    .order("fecha_atencion", desc=True) \
                    .limit(limite) \
                    .execute()

        return [AtencionVejezResponse.model_validate(item) for item in response.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/estado-funcional/{estado}", response_model=List[AtencionVejezResponse])
async def obtener_por_estado_funcional(
    estado: EstadoFuncionalVejez,
    limite: int = Query(20, le=100),
    db=Depends(get_supabase_client)
):
    """Obtener atenciones por estado funcional específico"""
    try:
        response = db.table("atencion_vejez") \
                    .select("*") \
                    .eq("estado_funcional", estado.value) \
                    .order("fecha_atencion", desc=True) \
                    .limit(limite) \
                    .execute()

        return [AtencionVejezResponse.model_validate(item) for item in response.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/fragilidad/{nivel}", response_model=List[AtencionVejezResponse])
async def obtener_por_fragilidad(
    nivel: SindromeFragilidad,
    limite: int = Query(20, le=100),
    db=Depends(get_supabase_client)
):
    """Obtener atenciones por nivel de fragilidad específico"""
    try:
        response = db.table("atencion_vejez") \
                    .select("*") \
                    .eq("sindrome_fragilidad", nivel.value) \
                    .order("fecha_atencion", desc=True) \
                    .limit(limite) \
                    .execute()

        return [AtencionVejezResponse.model_validate(item) for item in response.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# =============================================================================
# ENDPOINTS DE ESTADÍSTICAS Y REPORTES
# =============================================================================

@router.get("/estadisticas/basicas")
async def obtener_estadisticas_vejez(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio filtro"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin filtro"),
    db=Depends(get_supabase_client)
):
    """Obtener estadísticas básicas de atenciones de vejez"""
    try:
        # Query base
        query = db.table("atencion_vejez").select("*")

        # Aplicar filtros de fecha si se proporcionan
        if fecha_inicio:
            query = query.gte("fecha_atencion", fecha_inicio.isoformat())
        if fecha_fin:
            query = query.lte("fecha_atencion", fecha_fin.isoformat())

        response = query.execute()
        atenciones = response.data

        if not atenciones:
            return {"message": "No hay datos disponibles para el período seleccionado"}

        # Calcular estadísticas
        total_atenciones = len(atenciones)

        # Distribución por estado funcional
        dist_funcional = {}
        for atencion in atenciones:
            estado = atencion.get("estado_funcional", "No especificado")
            dist_funcional[estado] = dist_funcional.get(estado, 0) + 1

        # Distribución por fragilidad
        dist_fragilidad = {}
        for atencion in atenciones:
            fragilidad = atencion.get("sindrome_fragilidad", "No especificado")
            dist_fragilidad[fragilidad] = dist_fragilidad.get(fragilidad, 0) + 1

        # Distribución por riesgo caída
        dist_caidas = {}
        for atencion in atenciones:
            riesgo = atencion.get("riesgo_caida", "No especificado")
            dist_caidas[riesgo] = dist_caidas.get(riesgo, 0) + 1

        # Métricas específicas vejez
        mini_mental_aplicados = sum(1 for a in atenciones if a.get("mini_mental_aplicado"))
        con_cuidador = sum(1 for a in atenciones if not a.get("vive_solo", True))
        requieren_cuidados_paliativos = sum(1 for a in atenciones if a.get("requiere_cuidados_paliativos"))

        # Promedios
        indices_katz = [a.get("indice_katz") for a in atenciones if a.get("indice_katz") is not None]
        promedio_katz = sum(indices_katz) / len(indices_katz) if indices_katz else 0

        return {
            "total_atenciones": total_atenciones,
            "distribucion_estado_funcional": dist_funcional,
            "distribucion_fragilidad": dist_fragilidad,
            "distribucion_riesgo_caidas": dist_caidas,
            "metricas_especificas": {
                "mini_mental_aplicados": mini_mental_aplicados,
                "porcentaje_mini_mental": round((mini_mental_aplicados / total_atenciones) * 100, 1) if total_atenciones > 0 else 0,
                "con_cuidador": con_cuidador,
                "porcentaje_con_cuidador": round((con_cuidador / total_atenciones) * 100, 1) if total_atenciones > 0 else 0,
                "requieren_cuidados_paliativos": requieren_cuidados_paliativos,
                "promedio_indice_katz": round(promedio_katz, 2)
            },
            "periodo_analizado": {
                "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else "Sin filtro",
                "fecha_fin": fecha_fin.isoformat() if fecha_fin else "Sin filtro"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando estadísticas: {str(e)}")

@router.get("/reportes/valoracion-geriatrica")
async def reporte_valoracion_geriatrica(
    fecha_inicio: date = Query(..., description="Fecha inicio del reporte"),
    fecha_fin: date = Query(..., description="Fecha fin del reporte"),
    db=Depends(get_supabase_client)
):
    """Reporte de valoración geriátrica integral por período"""
    try:
        response = db.table("atencion_vejez") \
                    .select("*") \
                    .gte("fecha_atencion", fecha_inicio.isoformat()) \
                    .lte("fecha_atencion", fecha_fin.isoformat()) \
                    .execute()

        atenciones = response.data

        if not atenciones:
            return {"message": "No hay atenciones en el período especificado"}

        # Análisis por dimensiones geriátricas
        resultados = {
            "periodo": f"{fecha_inicio} al {fecha_fin}",
            "total_valoraciones": len(atenciones),
            "dimension_funcional": {
                "independientes": sum(1 for a in atenciones if a.get("estado_funcional") == "INDEPENDIENTE"),
                "dependencia_leve": sum(1 for a in atenciones if a.get("estado_funcional") == "DEPENDENCIA_LEVE"),
                "dependencia_moderada": sum(1 for a in atenciones if a.get("estado_funcional") == "DEPENDENCIA_MODERADA"),
                "dependencia_severa": sum(1 for a in atenciones if a.get("estado_funcional") == "DEPENDENCIA_SEVERA")
            },
            "dimension_cognitiva": {
                "normal": sum(1 for a in atenciones if a.get("estado_cognitivo") == "NORMAL"),
                "deterioro_leve": sum(1 for a in atenciones if a.get("estado_cognitivo") == "DETERIORO_LEVE"),
                "deterioro_moderado": sum(1 for a in atenciones if a.get("estado_cognitivo") == "DETERIORO_MODERADO"),
                "deterioro_severo": sum(1 for a in atenciones if a.get("estado_cognitivo") == "DETERIORO_SEVERO"),
                "no_evaluado": sum(1 for a in atenciones if a.get("estado_cognitivo") == "RIESGO_NO_EVALUADO")
            },
            "dimension_fragilidad": {
                "robusto": sum(1 for a in atenciones if a.get("sindrome_fragilidad") == "ROBUSTO"),
                "pre_fragil": sum(1 for a in atenciones if a.get("sindrome_fragilidad") == "PRE_FRAGIL"),
                "fragil": sum(1 for a in atenciones if a.get("sindrome_fragilidad") == "FRAGIL"),
                "fragilidad_severa": sum(1 for a in atenciones if a.get("sindrome_fragilidad") == "FRAGILIDAD_SEVERA")
            },
            "alertas_criticas": {
                "total_con_alertas": sum(1 for a in atenciones if a.get("alertas_generadas")),
                "tipos_alerta": self._analizar_tipos_alerta([a.get("alertas_generadas", []) for a in atenciones])
            }
        }

        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

def _analizar_tipos_alerta(alertas_list: List[List[str]]) -> Dict[str, int]:
    """Analiza tipos de alertas generadas"""
    conteo_alertas = {}
    for alertas in alertas_list:
        if alertas:
            for alerta in alertas:
                if "CRÍTICA" in alerta:
                    tipo = "Crítica"
                elif "ALERTA" in alerta:
                    tipo = "Moderada"
                else:
                    tipo = "Información"
                conteo_alertas[tipo] = conteo_alertas.get(tipo, 0) + 1
    return conteo_alertas