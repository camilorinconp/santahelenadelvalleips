# =============================================================================
# Rutas Atención Adolescencia y Juventud - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.3 y 3.3.4
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from database import get_supabase_client
from models.atencion_adolescencia_model import (
    AtencionAdolescenciaCrear,
    AtencionAdolescenciaActualizar,
    AtencionAdolescenciaResponse,
    EstadisticasAdolescenciaResponse,
    ReporteDesarrolloAdolescenciaResponse,
    EstadoNutricionalAdolescencia,
    DesarrolloPsicosocial,
    RiesgoCardiovascular,
    SaludMental,
    ConsumoSustancias,
    NivelRiesgoIntegral,
    FactorProtector
)

router = APIRouter(prefix="/atencion-adolescencia", tags=["Atención Adolescencia y Juventud"])

# =============================================================================
# FUNCIONES HELPER
# =============================================================================

def calcular_campos_automaticos(atencion_data: dict) -> dict:
    """Calcular todos los campos automáticos para respuesta API"""
    return AtencionAdolescenciaResponse.calcular_campos_automaticos(atencion_data)

def agregar_metadatos_auditoria(data: dict) -> dict:
    """Agregar metadatos de auditoría"""
    now = datetime.now()
    data["created_at"] = now
    data["updated_at"] = now
    return data

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - PATRÓN VERTICAL CONSOLIDADO
# =============================================================================

@router.post("/", response_model=AtencionAdolescenciaResponse, status_code=201)
async def crear_atencion_adolescencia(
    atencion_data: AtencionAdolescenciaCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nueva atención adolescencia/juventud con patrón polimórfico 3 pasos:
    1. Crear en tabla específica atencion_adolescencia
    2. Crear atención general con referencia
    3. Actualizar atencion_adolescencia con atencion_id
    """
    try:
        # PASO 1: Preparar datos y crear registro específico (sin atencion_id)
        atencion_dict = atencion_data.model_dump()
        atencion_dict["id"] = str(uuid4())
        atencion_dict = agregar_metadatos_auditoria(atencion_dict)
        
        # Calcular campos automáticos
        atencion_dict = calcular_campos_automaticos(atencion_dict)
        
        # Crear en tabla atencion_adolescencia (sin atencion_id)
        atencion_dict_sin_atencion = atencion_dict.copy()
        if 'atencion_id' in atencion_dict_sin_atencion:
            del atencion_dict_sin_atencion['atencion_id']
            
        response_adolescencia = db.table("atencion_adolescencia").insert(atencion_dict_sin_atencion).execute()
        
        if not response_adolescencia.data:
            raise HTTPException(status_code=500, detail="Error creando atención adolescencia")
        
        adolescencia_id = response_adolescencia.data[0]["id"]
        
        # PASO 2: Crear atención general con referencia
        atencion_general = {
            "id": str(uuid4()),
            "paciente_id": str(atencion_data.paciente_id),
            "medico_id": str(atencion_data.medico_id),
            "tipo_atencion": "ADOLESCENCIA_JUVENTUD",
            "subtipo_atencion": f"ADOLESCENCIA_{atencion_data.edad_anos}_ANOS" if atencion_data.edad_anos < 18 else f"JUVENTUD_{atencion_data.edad_anos}_ANOS",
            "fecha_atencion": atencion_data.fecha_atencion.isoformat(),
            "detalle_id": adolescencia_id,
            "entorno": atencion_data.entorno,
            "observaciones": atencion_data.observaciones_generales or "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        response_general = db.table("atenciones").insert(atencion_general).execute()
        
        if not response_general.data:
            # Rollback: eliminar registro adolescencia
            db.table("atencion_adolescencia").delete().eq("id", adolescencia_id).execute()
            raise HTTPException(status_code=500, detail="Error creando atención general")
        
        atencion_id = response_general.data[0]["id"]
        
        # PASO 3: Actualizar adolescencia con atencion_id
        update_response = db.table("atencion_adolescencia").update({
            "atencion_id": atencion_id,
            "updated_at": datetime.now().isoformat()
        }).eq("id", adolescencia_id).execute()
        
        if not update_response.data:
            # Rollback: eliminar ambos registros
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            db.table("atencion_adolescencia").delete().eq("id", adolescencia_id).execute()
            raise HTTPException(status_code=500, detail="Error actualizando referencia")
        
        # Construir respuesta con datos calculados
        atencion_dict["atencion_id"] = atencion_id
        atencion_dict["id"] = adolescencia_id
        
        return AtencionAdolescenciaResponse(**atencion_dict)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando atención adolescencia: {str(e)}")

@router.get("/{atencion_id}", response_model=AtencionAdolescenciaResponse)
async def obtener_atencion_adolescencia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener atención adolescencia por ID"""
    try:
        response = db.table("atencion_adolescencia").select("*").eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Atención adolescencia no encontrada")
        
        atencion_data = response.data[0]
        atencion_data = calcular_campos_automaticos(atencion_data)
        
        return AtencionAdolescenciaResponse(**atencion_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo atención: {str(e)}")

@router.get("/", response_model=List[AtencionAdolescenciaResponse])
async def listar_atenciones_adolescencia(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Máximo registros a retornar"),
    edad_minima: Optional[int] = Query(None, ge=12, le=29, description="Edad mínima"),
    edad_maxima: Optional[int] = Query(None, ge=12, le=29, description="Edad máxima"),
    nivel_riesgo: Optional[NivelRiesgoIntegral] = Query(None, description="Filtrar por nivel de riesgo"),
    db=Depends(get_supabase_client)
):
    """Listar atenciones adolescencia con filtros opcionales"""
    try:
        query = db.table("atencion_adolescencia").select("*")
        
        # Aplicar filtros
        if edad_minima is not None:
            query = query.gte("edad_anos", edad_minima)
        if edad_maxima is not None:
            query = query.lte("edad_anos", edad_maxima)
            
        response = query.range(skip, skip + limit - 1).order("created_at", desc=True).execute()
        
        atenciones = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            
            # Filtro post-cálculo por nivel de riesgo
            if nivel_riesgo is None or atencion_data["nivel_riesgo_integral"] == nivel_riesgo:
                atenciones.append(AtencionAdolescenciaResponse(**atencion_data))
        
        return atenciones
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando atenciones: {str(e)}")

@router.put("/{atencion_id}", response_model=AtencionAdolescenciaResponse)
async def actualizar_atencion_adolescencia(
    atencion_id: UUID,
    atencion_data: AtencionAdolescenciaActualizar,
    db=Depends(get_supabase_client)
):
    """Actualizar atención adolescencia existente"""
    try:
        # Verificar que existe
        existing = db.table("atencion_adolescencia").select("*").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Atención adolescencia no encontrada")
        
        # Preparar datos para actualización (solo campos no nulos)
        update_data = {k: v for k, v in atencion_data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        update_data["updated_at"] = datetime.now().isoformat()
        
        # Actualizar en base de datos
        response = db.table("atencion_adolescencia").update(update_data).eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Error actualizando atención")
        
        # Obtener datos actualizados y calcular campos
        updated_data = response.data[0]
        updated_data = calcular_campos_automaticos(updated_data)
        
        return AtencionAdolescenciaResponse(**updated_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando atención: {str(e)}")

@router.delete("/{atencion_id}", status_code=204)
async def eliminar_atencion_adolescencia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Eliminar atención adolescencia (soft delete)"""
    try:
        # Verificar que existe y obtener atencion_id relacionado
        existing = db.table("atencion_adolescencia").select("atencion_id").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Atención adolescencia no encontrada")
        
        related_atencion_id = existing.data[0].get("atencion_id")
        
        # Eliminar registro específico
        delete_response = db.table("atencion_adolescencia").delete().eq("id", str(atencion_id)).execute()
        if not delete_response.data:
            raise HTTPException(status_code=500, detail="Error eliminando atención adolescencia")
        
        # Eliminar atención general relacionada si existe
        if related_atencion_id:
            db.table("atenciones").delete().eq("id", related_atencion_id).execute()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando atención: {str(e)}")

# =============================================================================
# ENDPOINTS ESPECIALIZADOS - FUNCIONALIDAD AVANZADA
# =============================================================================

@router.get("/por-rango-edad/{edad_inicio}/{edad_fin}", response_model=List[AtencionAdolescenciaResponse])
async def obtener_por_rango_edad(
    edad_inicio: int,
    edad_fin: int,
    db=Depends(get_supabase_client)
):
    """Obtener atenciones por rango específico de edad"""
    try:
        if edad_inicio > edad_fin:
            raise HTTPException(status_code=400, detail="Edad inicio debe ser menor o igual a edad fin")
        
        response = db.table("atencion_adolescencia").select("*").gte("edad_anos", edad_inicio).lte("edad_anos", edad_fin).execute()
        
        atenciones = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            atenciones.append(AtencionAdolescenciaResponse(**atencion_data))
        
        return atenciones
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo atenciones por edad: {str(e)}")

@router.get("/paciente/{paciente_id}/cronologicas", response_model=List[AtencionAdolescenciaResponse])
async def obtener_atenciones_cronologicas_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener todas las atenciones de un paciente ordenadas cronológicamente"""
    try:
        response = db.table("atencion_adolescencia").select("*").eq("paciente_id", str(paciente_id)).order("fecha_atencion", desc=True).execute()
        
        atenciones = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            atenciones.append(AtencionAdolescenciaResponse(**atencion_data))
        
        return atenciones
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial paciente: {str(e)}")

@router.get("/por-nivel-riesgo/{nivel_riesgo}", response_model=List[AtencionAdolescenciaResponse])
async def obtener_por_nivel_riesgo(
    nivel_riesgo: NivelRiesgoIntegral,
    limite_dias: Optional[int] = Query(30, ge=1, le=365, description="Atenciones en los últimos X días"),
    db=Depends(get_supabase_client)
):
    """Obtener atenciones por nivel de riesgo específico"""
    try:
        fecha_limite = datetime.now() - timedelta(days=limite_dias)
        
        response = db.table("atencion_adolescencia").select("*").gte("fecha_atencion", fecha_limite.date().isoformat()).execute()
        
        atenciones_filtradas = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            if atencion_data["nivel_riesgo_integral"] == nivel_riesgo:
                atenciones_filtradas.append(AtencionAdolescenciaResponse(**atencion_data))
        
        return atenciones_filtradas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo atenciones por riesgo: {str(e)}")

@router.get("/alertas/riesgo-alto", response_model=List[AtencionAdolescenciaResponse])
async def obtener_alertas_riesgo_alto(
    incluir_muy_alto: bool = Query(True, description="Incluir riesgo MUY_ALTO"),
    incluir_critico: bool = Query(True, description="Incluir riesgo CRÍTICO"),
    db=Depends(get_supabase_client)
):
    """Obtener adolescentes con alertas de riesgo alto para seguimiento prioritario"""
    try:
        # Obtener todas las atenciones recientes
        fecha_limite = datetime.now() - timedelta(days=90)  # Últimos 3 meses
        response = db.table("atencion_adolescencia").select("*").gte("fecha_atencion", fecha_limite.date().isoformat()).execute()
        
        alertas = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            nivel_riesgo = atencion_data["nivel_riesgo_integral"]
            
            if (nivel_riesgo == NivelRiesgoIntegral.ALTO or
                (incluir_muy_alto and nivel_riesgo == NivelRiesgoIntegral.MUY_ALTO) or
                (incluir_critico and nivel_riesgo == NivelRiesgoIntegral.CRITICO)):
                alertas.append(AtencionAdolescenciaResponse(**atencion_data))
        
        # Ordenar por nivel de riesgo (crítico primero)
        alertas.sort(key=lambda x: ["BAJO", "MODERADO", "ALTO", "MUY_ALTO", "CRITICO"].index(x.nivel_riesgo_integral))
        
        return alertas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo alertas: {str(e)}")

# =============================================================================
# ENDPOINTS ESTADÍSTICAS Y REPORTES
# =============================================================================

@router.get("/estadisticas/basicas", response_model=EstadisticasAdolescenciaResponse)
async def obtener_estadisticas_basicas(
    dias_atras: int = Query(30, ge=1, le=365, description="Período en días para estadísticas"),
    db=Depends(get_supabase_client)
):
    """Obtener estadísticas básicas del módulo adolescencia"""
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias_atras)
        
        response = db.table("atencion_adolescencia").select("*").gte("fecha_atencion", fecha_inicio.date().isoformat()).execute()
        
        if not response.data:
            return EstadisticasAdolescenciaResponse(
                total_atenciones=0,
                distribuciones={},
                promedios={},
                alertas={}
            )
        
        # Calcular campos para todas las atenciones
        atenciones_calculadas = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            atenciones_calculadas.append(atencion_data)
        
        total = len(atenciones_calculadas)
        
        # Distribuciones
        distribuciones = {
            "por_edad": {},
            "por_estado_nutricional": {},
            "por_nivel_riesgo": {},
            "por_desarrollo_psicosocial": {},
            "por_salud_mental": {}
        }
        
        # Promedios
        edades = [a["edad_anos"] for a in atenciones_calculadas]
        imcs = [a["imc"] for a in atenciones_calculadas]
        autoestimas = [a["autoestima"] for a in atenciones_calculadas]
        
        promedios = {
            "edad_anos": round(sum(edades) / len(edades), 1) if edades else 0,
            "imc": round(sum(imcs) / len(imcs), 2) if imcs else 0,
            "autoestima": round(sum(autoestimas) / len(autoestimas), 1) if autoestimas else 0,
            "factores_protectores_promedio": round(sum(len(a["factores_protectores_identificados"]) for a in atenciones_calculadas) / total, 1) if total > 0 else 0
        }
        
        # Calcular distribuciones
        for atencion in atenciones_calculadas:
            # Por edad
            grupo_edad = "12-15" if atencion["edad_anos"] <= 15 else "16-19" if atencion["edad_anos"] <= 19 else "20-24" if atencion["edad_anos"] <= 24 else "25-29"
            distribuciones["por_edad"][grupo_edad] = distribuciones["por_edad"].get(grupo_edad, 0) + 1
            
            # Por estado nutricional
            estado_nut = atencion["estado_nutricional"]
            distribuciones["por_estado_nutricional"][estado_nut] = distribuciones["por_estado_nutricional"].get(estado_nut, 0) + 1
            
            # Por nivel de riesgo
            nivel_riesgo = atencion["nivel_riesgo_integral"]
            distribuciones["por_nivel_riesgo"][nivel_riesgo] = distribuciones["por_nivel_riesgo"].get(nivel_riesgo, 0) + 1
            
            # Por desarrollo psicosocial
            desarrollo = atencion["desarrollo_psicosocial_apropiado"]
            distribuciones["por_desarrollo_psicosocial"][desarrollo] = distribuciones["por_desarrollo_psicosocial"].get(desarrollo, 0) + 1
            
            # Por salud mental
            salud_mental = atencion["salud_mental"]
            distribuciones["por_salud_mental"][salud_mental] = distribuciones["por_salud_mental"].get(salud_mental, 0) + 1
        
        # Alertas
        riesgo_alto_count = sum(1 for a in atenciones_calculadas if a["nivel_riesgo_integral"] in ["ALTO", "MUY_ALTO", "CRITICO"])
        problemas_salud_mental = sum(1 for a in atenciones_calculadas if a["salud_mental"] in ["SINTOMAS_MODERADOS", "SINTOMAS_SEVEROS", "REQUIERE_ATENCION_ESPECIALIZADA"])
        obesidad_count = sum(1 for a in atenciones_calculadas if "OBESIDAD" in a["estado_nutricional"])
        
        alertas = {
            "adolescentes_riesgo_alto": riesgo_alto_count,
            "porcentaje_riesgo_alto": round((riesgo_alto_count / total) * 100, 1) if total > 0 else 0,
            "problemas_salud_mental": problemas_salud_mental,
            "porcentaje_problemas_mental": round((problemas_salud_mental / total) * 100, 1) if total > 0 else 0,
            "casos_obesidad": obesidad_count,
            "porcentaje_obesidad": round((obesidad_count / total) * 100, 1) if total > 0 else 0
        }
        
        return EstadisticasAdolescenciaResponse(
            total_atenciones=total,
            distribuciones=distribuciones,
            promedios=promedios,
            alertas=alertas
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando estadísticas: {str(e)}")

@router.get("/reportes/desarrollo-psicosocial", response_model=ReporteDesarrolloAdolescenciaResponse)
async def generar_reporte_desarrollo_psicosocial(
    dias_atras: int = Query(90, ge=1, le=365, description="Período en días para reporte"),
    db=Depends(get_supabase_client)
):
    """Generar reporte especializado de desarrollo psicosocial"""
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias_atras)
        
        response = db.table("atencion_adolescencia").select("*").gte("fecha_atencion", fecha_inicio.date().isoformat()).execute()
        
        if not response.data:
            return ReporteDesarrolloAdolescenciaResponse(
                adolescentes_evaluados=0,
                desarrollo_apropiado=0,
                factores_riesgo_prevalentes=[],
                factores_protectores_prevalentes=[],
                recomendaciones=[]
            )
        
        # Calcular campos para todas las atenciones
        atenciones_calculadas = []
        for atencion_data in response.data:
            atencion_data = calcular_campos_automaticos(atencion_data)
            atenciones_calculadas.append(atencion_data)
        
        total = len(atenciones_calculadas)
        desarrollo_apropiado = sum(1 for a in atenciones_calculadas if a["desarrollo_psicosocial_apropiado"] == "APROPIADO")
        
        # Análisis factores de riesgo
        factores_riesgo = {
            "consumo_sustancias": sum(1 for a in atenciones_calculadas if a["consumo_sustancias"] != "SIN_CONSUMO"),
            "problemas_salud_mental": sum(1 for a in atenciones_calculadas if a["salud_mental"] != "NORMAL"),
            "sedentarismo": sum(1 for a in atenciones_calculadas if a["sedentarismo"]),
            "problemas_conductuales": sum(1 for a in atenciones_calculadas if a["problemas_conductuales"]),
            "proyecto_vida_ausente": sum(1 for a in atenciones_calculadas if a["proyecto_vida"] in ["POCO_CLARO", "AUSENTE"])
        }
        
        factores_riesgo_prevalentes = [
            {"factor": k, "casos": v, "porcentaje": round((v/total)*100, 1)}
            for k, v in sorted(factores_riesgo.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Análisis factores protectores
        todos_factores_protectores = []
        for a in atenciones_calculadas:
            todos_factores_protectores.extend(a["factores_protectores_identificados"])
        
        from collections import Counter
        factores_protectores_count = Counter(todos_factores_protectores)
        
        factores_protectores_prevalentes = [
            {"factor": k, "casos": v, "porcentaje": round((v/total)*100, 1)}
            for k, v in factores_protectores_count.most_common()
        ]
        
        # Generar recomendaciones basadas en datos
        recomendaciones = []
        
        if factores_riesgo["sedentarismo"] > total * 0.6:
            recomendaciones.append("Implementar programas de actividad física dirigidos a adolescentes")
        
        if factores_riesgo["problemas_salud_mental"] > total * 0.3:
            recomendaciones.append("Fortalecer programas de salud mental y apoyo psicológico")
        
        if factores_riesgo["proyecto_vida_ausente"] > total * 0.4:
            recomendaciones.append("Desarrollar talleres de orientación vocacional y proyecto de vida")
        
        if desarrollo_apropiado < total * 0.7:
            recomendaciones.append("Intensificar intervenciones de desarrollo psicosocial")
        
        if factores_riesgo["consumo_sustancias"] > total * 0.2:
            recomendaciones.append("Implementar programas de prevención de consumo de sustancias")
        
        return ReporteDesarrolloAdolescenciaResponse(
            adolescentes_evaluados=total,
            desarrollo_apropiado=desarrollo_apropiado,
            factores_riesgo_prevalentes=factores_riesgo_prevalentes[:5],  # Top 5
            factores_protectores_prevalentes=factores_protectores_prevalentes[:5],  # Top 5
            recomendaciones=recomendaciones
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

# =============================================================================
# ENDPOINTS LEGACY Y COMPATIBILIDAD
# =============================================================================

@router.get("/atenciones-adolescencia/", response_model=List[AtencionAdolescenciaResponse])
async def listar_atenciones_legacy(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_supabase_client)
):
    """Endpoint legacy para compatibilidad con versiones anteriores"""
    return await listar_atenciones_adolescencia(skip=skip, limit=limit, db=db)