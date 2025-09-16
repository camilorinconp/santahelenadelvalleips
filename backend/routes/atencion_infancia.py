# =============================================================================
# Rutas Atención Infancia - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from database import get_supabase_client
from models.atencion_infancia_model import (
    AtencionInfanciaCrear,
    AtencionInfanciaActualizar, 
    AtencionInfanciaResponse,
    EstadoNutricionalInfancia,
    DesempenoEscolar,
    ResultadoTamizaje,
    FactorRiesgo,
    calcular_estado_nutricional,
    calcular_desarrollo_apropiado,
    calcular_riesgo_nutricional,
    calcular_proxima_consulta_dias,
    calcular_completitud_evaluacion,
    determinar_seguimiento_especializado
)

router = APIRouter(prefix="/atencion-infancia", tags=["Atención Infancia"])

# =============================================================================
# FUNCIÓN HELPER PARA CAMPOS CALCULADOS
# =============================================================================

def calcular_campos_automaticos(atencion_data: dict, edad_anos: int = 8) -> dict:
    """Calcular campos automáticos para respuesta de API"""
    
    # Calcular IMC
    peso = atencion_data.get('peso_kg', 0)
    talla = atencion_data.get('talla_cm', 0)
    imc = peso / ((talla / 100) ** 2) if talla > 0 else 0
    
    # Estado nutricional
    estado_nutricional = calcular_estado_nutricional(peso, talla, edad_anos)
    
    # Desarrollo apropiado
    desarrollo_apropiado = calcular_desarrollo_apropiado(
        atencion_data.get('desempeno_escolar', DesempenoEscolar.BASICO),
        atencion_data.get('tamizaje_visual', ResultadoTamizaje.NORMAL),
        atencion_data.get('tamizaje_auditivo', ResultadoTamizaje.NORMAL),
        atencion_data.get('dificultades_aprendizaje', False)
    )
    
    # Riesgo nutricional
    riesgo_nutricional = calcular_riesgo_nutricional(
        estado_nutricional,
        atencion_data.get('consume_comida_chatarra', False),
        atencion_data.get('actividad_fisica_semanal_horas')
    )
    
    # Seguimiento especializado
    requiere_seguimiento = determinar_seguimiento_especializado(
        atencion_data.get('tamizaje_visual', ResultadoTamizaje.NORMAL),
        atencion_data.get('tamizaje_auditivo', ResultadoTamizaje.NORMAL),
        atencion_data.get('tamizaje_salud_bucal', ResultadoTamizaje.NORMAL),
        atencion_data.get('dificultades_aprendizaje', False),
        atencion_data.get('numero_caries')
    )
    
    # Próxima consulta
    factores_riesgo = atencion_data.get('factores_riesgo_identificados', [])
    proxima_consulta_dias = calcular_proxima_consulta_dias(
        estado_nutricional,
        requiere_seguimiento,
        factores_riesgo
    )
    
    # Completitud
    completitud = calcular_completitud_evaluacion(atencion_data)
    
    # Percentiles estimados (simplificado)
    percentil_peso = 50 if estado_nutricional == EstadoNutricionalInfancia.NORMAL else 25
    percentil_talla = 50  # Simplificado
    
    return {
        'estado_nutricional': estado_nutricional,
        'indice_masa_corporal': round(imc, 1),
        'percentil_peso': percentil_peso,
        'percentil_talla': percentil_talla,
        'desarrollo_apropiado_edad': desarrollo_apropiado,
        'riesgo_nutricional': riesgo_nutricional,
        'requiere_seguimiento_especializado': requiere_seguimiento,
        'proxima_consulta_recomendada_dias': proxima_consulta_dias,
        'completitud_evaluacion': completitud
    }

# =============================================================================
# ENDPOINTS CRUD BÁSICOS
# =============================================================================

@router.post("/", response_model=AtencionInfanciaResponse, status_code=201)
async def crear_atencion_infancia(
    atencion_data: AtencionInfanciaCrear,
    db=Depends(get_supabase_client)
):
    """Crear nueva atención de infancia con patrón polimórfico de 3 pasos"""
    
    # Validar que el paciente existe
    paciente_response = db.table("pacientes").select("id, fecha_nacimiento").eq("id", str(atencion_data.paciente_id)).execute()
    if not paciente_response.data:
        raise HTTPException(status_code=400, detail="El paciente especificado no existe")
    
    # Calcular edad del paciente
    fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
    edad_anos = (date.today() - fecha_nacimiento).days // 365
    
    # Validar rango de edad para infancia (6-11 años)
    if edad_anos < 6 or edad_anos > 11:
        raise HTTPException(status_code=400, detail=f"Edad {edad_anos} años fuera del rango de infancia (6-11 años)")
    
    try:
        # PASO 1: Crear atención de infancia (sin atencion_id por ahora)
        atencion_dict = atencion_data.model_dump()
        atencion_dict['id'] = str(uuid4())
        atencion_dict['paciente_id'] = str(atencion_data.paciente_id)
        atencion_dict['medico_id'] = str(atencion_data.medico_id) if atencion_data.medico_id else None
        atencion_dict['fecha_atencion'] = atencion_data.fecha_atencion.isoformat()
        
        # Convertir listas de enums a strings
        if 'factores_riesgo_identificados' in atencion_dict and atencion_dict['factores_riesgo_identificados']:
            atencion_dict['factores_riesgo_identificados'] = [str(factor) for factor in atencion_dict['factores_riesgo_identificados']]
        
        response_infancia = db.table("atencion_infancia").insert(atencion_dict).execute()
        
        if not response_infancia.data:
            raise HTTPException(status_code=500, detail="Error al crear atención de infancia")
        
        infancia_id = response_infancia.data[0]['id']
        
        # PASO 2: Crear atención general que referencie a la atención de infancia
        atencion_general_data = {
            "id": str(uuid4()),
            "paciente_id": str(atencion_data.paciente_id),
            "medico_id": str(atencion_data.medico_id) if atencion_data.medico_id else None,
            "tipo_atencion": "Atención Infancia",
            "detalle_id": infancia_id,
            "fecha_atencion": atencion_data.fecha_atencion.isoformat(),
            "entorno": atencion_data.entorno,
            "descripcion": f"Atención integral para infancia - {edad_anos} años",
            "creado_en": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        response_atencion = db.table("atenciones").insert(atencion_general_data).execute()
        
        if not response_atencion.data:
            # Rollback: eliminar atención de infancia creada
            db.table("atencion_infancia").delete().eq("id", infancia_id).execute()
            raise HTTPException(status_code=500, detail="Error al crear atención general")
        
        atencion_id = response_atencion.data[0]['id']
        
        # PASO 3: Actualizar atención de infancia con atencion_id
        update_response = db.table("atencion_infancia").update({"atencion_id": atencion_id}).eq("id", infancia_id).execute()
        
        if not update_response.data:
            # Rollback: eliminar ambos registros
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            db.table("atencion_infancia").delete().eq("id", infancia_id).execute()
            raise HTTPException(status_code=500, detail="Error al vincular atención general con infancia")
        
        # Obtener registro completo para respuesta
        final_response = db.table("atencion_infancia").select("*").eq("id", infancia_id).execute()
        atencion_completa = final_response.data[0]
        
        # Agregar campos calculados
        campos_calculados = calcular_campos_automaticos(atencion_completa, edad_anos)
        atencion_completa.update(campos_calculados)
        
        return AtencionInfanciaResponse(**atencion_completa)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[AtencionInfanciaResponse])
async def listar_atenciones_infancia(
    paciente_id: Optional[UUID] = Query(None, description="Filtrar por paciente"),
    desempeno_escolar: Optional[DesempenoEscolar] = Query(None, description="Filtrar por desempeño escolar"),
    estado_nutricional: Optional[EstadoNutricionalInfancia] = Query(None, description="Filtrar por estado nutricional"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    db=Depends(get_supabase_client)
):
    """Listar atenciones de infancia con filtros opcionales"""
    
    try:
        query = db.table("atencion_infancia").select("*")
        
        # Aplicar filtros
        if paciente_id:
            query = query.eq("paciente_id", str(paciente_id))
        if desempeno_escolar:
            query = query.eq("desempeno_escolar", desempeno_escolar.value)
        
        # Ordenar por fecha descendente
        query = query.order("fecha_atencion", desc=True)
        
        # Aplicar paginación
        query = query.range(offset, offset + limit - 1)
        
        response = query.execute()
        
        atenciones_con_calculos = []
        for atencion in response.data:
            # Calcular edad estimada (simplificado)
            edad_anos = 8  # Promedio para infancia
            campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
            atencion.update(campos_calculados)
            
            # Filtro post-query para estado nutricional (campo calculado)
            if estado_nutricional and campos_calculados['estado_nutricional'] != estado_nutricional:
                continue
                
            atenciones_con_calculos.append(AtencionInfanciaResponse(**atencion))
        
        return atenciones_con_calculos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener atenciones: {str(e)}")

@router.get("/{atencion_id}", response_model=AtencionInfanciaResponse)
async def obtener_atencion_infancia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener atención de infancia por ID"""
    
    try:
        response = db.table("atencion_infancia").select("*").eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Atención de infancia no encontrada")
        
        atencion = response.data[0]
        
        # Calcular edad del paciente
        paciente_response = db.table("pacientes").select("fecha_nacimiento").eq("id", atencion['paciente_id']).execute()
        if paciente_response.data:
            fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
            edad_anos = (date.today() - fecha_nacimiento).days // 365
        else:
            edad_anos = 8  # Default
        
        # Agregar campos calculados
        campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
        atencion.update(campos_calculados)
        
        return AtencionInfanciaResponse(**atencion)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener atención: {str(e)}")

@router.put("/{atencion_id}", response_model=AtencionInfanciaResponse)
async def actualizar_atencion_infancia(
    atencion_id: UUID,
    atencion_data: AtencionInfanciaActualizar,
    db=Depends(get_supabase_client)
):
    """Actualizar atención de infancia existente"""
    
    try:
        # Verificar que existe
        existing_response = db.table("atencion_infancia").select("*").eq("id", str(atencion_id)).execute()
        if not existing_response.data:
            raise HTTPException(status_code=404, detail="Atención de infancia no encontrada")
        
        # Preparar datos para actualización
        update_data = {k: v for k, v in atencion_data.model_dump(exclude_unset=True).items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Convertir listas de enums a strings
        if 'factores_riesgo_identificados' in update_data and update_data['factores_riesgo_identificados']:
            update_data['factores_riesgo_identificados'] = [str(factor) for factor in update_data['factores_riesgo_identificados']]
        
        update_data['updated_at'] = datetime.now().isoformat()
        
        # Realizar actualización
        response = db.table("atencion_infancia").update(update_data).eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Error al actualizar atención")
        
        atencion_actualizada = response.data[0]
        
        # Calcular edad del paciente
        paciente_response = db.table("pacientes").select("fecha_nacimiento").eq("id", atencion_actualizada['paciente_id']).execute()
        if paciente_response.data:
            fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
            edad_anos = (date.today() - fecha_nacimiento).days // 365
        else:
            edad_anos = 8  # Default
        
        # Agregar campos calculados
        campos_calculados = calcular_campos_automaticos(atencion_actualizada, edad_anos)
        atencion_actualizada.update(campos_calculados)
        
        return AtencionInfanciaResponse(**atencion_actualizada)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar atención: {str(e)}")

@router.delete("/{atencion_id}", status_code=204)
async def eliminar_atencion_infancia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Eliminar atención de infancia"""
    
    try:
        # Verificar que existe
        existing_response = db.table("atencion_infancia").select("atencion_id").eq("id", str(atencion_id)).execute()
        if not existing_response.data:
            raise HTTPException(status_code=404, detail="Atención de infancia no encontrada")
        
        atencion_general_id = existing_response.data[0].get('atencion_id')
        
        # Eliminar atención de infancia
        delete_response = db.table("atencion_infancia").delete().eq("id", str(atencion_id)).execute()
        
        if not delete_response.data:
            raise HTTPException(status_code=500, detail="Error al eliminar atención de infancia")
        
        # Eliminar atención general asociada si existe
        if atencion_general_id:
            db.table("atenciones").delete().eq("id", atencion_general_id).execute()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar atención: {str(e)}")

# =============================================================================
# ENDPOINTS ESPECIALIZADOS
# =============================================================================

@router.get("/desempeno/{desempeno_escolar}", response_model=List[AtencionInfanciaResponse])
async def listar_por_desempeno_escolar(
    desempeno_escolar: DesempenoEscolar,
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_supabase_client)
):
    """Listar atenciones por desempeño escolar específico"""
    
    try:
        response = db.table("atencion_infancia") \
            .select("*") \
            .eq("desempeno_escolar", desempeno_escolar.value) \
            .order("fecha_atencion", desc=True) \
            .limit(limit) \
            .execute()
        
        atenciones_con_calculos = []
        for atencion in response.data:
            edad_anos = 8  # Promedio
            campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
            atencion.update(campos_calculados)
            atenciones_con_calculos.append(AtencionInfanciaResponse(**atencion))
        
        return atenciones_con_calculos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener atenciones por desempeño: {str(e)}")

@router.get("/paciente/{paciente_id}/cronologicas", response_model=List[AtencionInfanciaResponse])
async def obtener_atenciones_cronologicas_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener historial cronológico de atenciones de infancia para un paciente"""
    
    try:
        response = db.table("atencion_infancia") \
            .select("*") \
            .eq("paciente_id", str(paciente_id)) \
            .order("fecha_atencion", desc=False) \
            .execute()
        
        if not response.data:
            return []
        
        # Calcular edad del paciente
        paciente_response = db.table("pacientes").select("fecha_nacimiento").eq("id", str(paciente_id)).execute()
        if paciente_response.data:
            fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
            edad_anos = (date.today() - fecha_nacimiento).days // 365
        else:
            edad_anos = 8
        
        atenciones_con_calculos = []
        for atencion in response.data:
            campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
            atencion.update(campos_calculados)
            atenciones_con_calculos.append(AtencionInfanciaResponse(**atencion))
        
        return atenciones_con_calculos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial cronológico: {str(e)}")

# =============================================================================
# ENDPOINTS DE ESTADÍSTICAS Y REPORTES
# =============================================================================

@router.get("/estadisticas/basicas")
async def obtener_estadisticas_basicas(
    fecha_desde: Optional[date] = Query(None, description="Fecha de inicio del período"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha de fin del período"),
    db=Depends(get_supabase_client)
):
    """Obtener estadísticas básicas de atenciones de infancia"""
    
    try:
        query = db.table("atencion_infancia").select("*")
        
        # Aplicar filtros de fecha si se proporcionan
        if fecha_desde:
            query = query.gte("fecha_atencion", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_atencion", fecha_hasta.isoformat())
        
        response = query.execute()
        atenciones = response.data
        
        if not atenciones:
            return {
                "resumen_general": {
                    "total_atenciones": 0,
                    "promedio_edad": 0,
                    "porcentaje_desarrollo_apropiado": 0,
                    "porcentaje_seguimiento_especializado": 0
                },
                "por_desempeno_escolar": {},
                "estado_nutricional": {},
                "factores_riesgo": {},
                "fecha_calculo": datetime.now().isoformat()
            }
        
        # Calcular estadísticas
        total_atenciones = len(atenciones)
        desarrollo_apropiado_count = 0
        seguimiento_especializado_count = 0
        
        desempeno_stats = {}
        nutricional_stats = {}
        factores_riesgo_stats = {}
        
        for atencion in atenciones:
            edad_anos = 8  # Simplificado
            campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
            
            if campos_calculados['desarrollo_apropiado_edad']:
                desarrollo_apropiado_count += 1
            if campos_calculados['requiere_seguimiento_especializado']:
                seguimiento_especializado_count += 1
            
            # Estadísticas por desempeño escolar
            desempeno = atencion.get('desempeno_escolar', 'NO_ESPECIFICADO')
            desempeno_stats[desempeno] = desempeno_stats.get(desempeno, 0) + 1
            
            # Estadísticas por estado nutricional
            estado_nut = campos_calculados['estado_nutricional']
            nutricional_stats[estado_nut] = nutricional_stats.get(estado_nut, 0) + 1
            
            # Estadísticas de factores de riesgo
            factores = atencion.get('factores_riesgo_identificados', [])
            for factor in factores:
                factores_riesgo_stats[factor] = factores_riesgo_stats.get(factor, 0) + 1
        
        return {
            "resumen_general": {
                "total_atenciones": total_atenciones,
                "promedio_edad": 8.0,  # Simplificado para infancia
                "porcentaje_desarrollo_apropiado": round((desarrollo_apropiado_count / total_atenciones) * 100, 1),
                "porcentaje_seguimiento_especializado": round((seguimiento_especializado_count / total_atenciones) * 100, 1)
            },
            "por_desempeno_escolar": desempeno_stats,
            "estado_nutricional": nutricional_stats,
            "factores_riesgo": factores_riesgo_stats,
            "fecha_calculo": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular estadísticas: {str(e)}")

@router.get("/reportes/desarrollo")
async def reporte_desarrollo_escolar(
    grado_escolar: Optional[str] = Query(None, description="Filtrar por grado escolar"),
    db=Depends(get_supabase_client)
):
    """Generar reporte detallado de desarrollo escolar"""
    
    try:
        query = db.table("atencion_infancia").select("*")
        
        if grado_escolar:
            query = query.eq("grado_escolar", grado_escolar)
        
        response = query.execute()
        atenciones = response.data
        
        reporte = {
            "parametros_reporte": {
                "grado_escolar": grado_escolar or "Todos",
                "total_estudiantes_analizados": len(atenciones)
            },
            "desempeno_academico": {
                "SUPERIOR": 0,
                "ALTO": 0,
                "BASICO": 0,
                "BAJO": 0,
                "NO_ESCOLARIZADO": 0
            },
            "problemas_desarrollo": {
                "dificultades_aprendizaje": 0,
                "problemas_visuales": 0,
                "problemas_auditivos": 0,
                "problemas_nutricionales": 0
            },
            "recomendaciones_seguimiento": [],
            "fecha_generacion": datetime.now().isoformat()
        }
        
        for atencion in atenciones:
            # Desempeño académico
            desempeno = atencion.get('desempeno_escolar', 'NO_ESCOLARIZADO')
            reporte["desempeno_academico"][desempeno] += 1
            
            # Problemas de desarrollo
            if atencion.get('dificultades_aprendizaje'):
                reporte["problemas_desarrollo"]["dificultades_aprendizaje"] += 1
            
            if atencion.get('tamizaje_visual') == 'ALTERADO':
                reporte["problemas_desarrollo"]["problemas_visuales"] += 1
            
            if atencion.get('tamizaje_auditivo') == 'ALTERADO':
                reporte["problemas_desarrollo"]["problemas_auditivos"] += 1
            
            # Calcular problemas nutricionales
            edad_anos = 8
            campos_calculados = calcular_campos_automaticos(atencion, edad_anos)
            if campos_calculados['estado_nutricional'] != EstadoNutricionalInfancia.NORMAL:
                reporte["problemas_desarrollo"]["problemas_nutricionales"] += 1
        
        # Generar recomendaciones
        total = len(atenciones)
        if total > 0:
            if reporte["problemas_desarrollo"]["dificultades_aprendizaje"] / total > 0.2:
                reporte["recomendaciones_seguimiento"].append("Alto porcentaje de dificultades de aprendizaje - revisar métodos pedagógicos")
            
            if reporte["problemas_desarrollo"]["problemas_visuales"] / total > 0.15:
                reporte["recomendaciones_seguimiento"].append("Incrementar frecuencia de tamizajes visuales")
            
            if reporte["desempeno_academico"]["BAJO"] / total > 0.25:
                reporte["recomendaciones_seguimiento"].append("Implementar programas de refuerzo académico")
        
        return reporte
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar reporte de desarrollo: {str(e)}")