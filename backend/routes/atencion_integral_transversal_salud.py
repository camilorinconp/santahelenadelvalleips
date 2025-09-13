# =============================================================================
# Rutas API REST - Atención Integral Transversal de Salud
# Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from supabase import Client
from uuid import UUID
from datetime import datetime, timedelta

from database import get_supabase_client
from models.atencion_integral_model import (
    ModeloAtencionIntegralTransversalSaludCrear,
    ModeloAtencionIntegralTransversalSaludRespuesta,
    ModeloAtencionIntegralTransversalSaludActualizar
)

# =============================================================================
# CONFIGURACIÓN DEL ROUTER
# =============================================================================

router = APIRouter(
    prefix="/atencion-integral-transversal-salud",
    tags=["Atención Integral Transversal Salud"],
    responses={404: {"description": "Atención integral no encontrada"}}
)

# =============================================================================
# ENDPOINTS CRUD - ATENCIÓN INTEGRAL TRANSVERSAL
# =============================================================================

@router.post("/", response_model=ModeloAtencionIntegralTransversalSaludRespuesta, status_code=status.HTTP_201_CREATED)
def crear_atencion_integral_transversal_salud(
    atencion: ModeloAtencionIntegralTransversalSaludCrear, 
    db: Client = Depends(get_supabase_client)
):
    """
    Crear una nueva atención integral transversal de salud.
    
    Implementa atención integral como eje transversal según la Resolución 3280 Art. 1364-1370:
    'Atención integral que reconoce al individuo, familia y comunidad como sujetos de atención'
    """
    try:
        # Preparar datos para inserción
        atencion_data = atencion.model_dump(exclude_unset=True)
        
        # Convertir datetime a string ISO para Supabase
        if "fecha_inicio_atencion_integral" in atencion_data:
            if isinstance(atencion_data["fecha_inicio_atencion_integral"], datetime):
                atencion_data["fecha_inicio_atencion_integral"] = atencion_data["fecha_inicio_atencion_integral"].isoformat()
        
        # Ejecutar inserción en Supabase
        result = db.table("atencion_integral_transversal_salud").insert(atencion_data).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la atención integral: No se recibieron datos de respuesta"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear atención integral: {str(e)}"
        )


@router.get("/", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_atenciones_integral_transversal_salud(
    skip: int = 0,
    limit: int = 100,
    tipo_abordaje: Optional[str] = None,
    modalidad: Optional[str] = None,
    nivel_complejidad: Optional[str] = None,
    estado: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones integrales transversales con filtros opcionales.
    
    Permite filtrar por:
    - tipo_abordaje: Tipo de abordaje (individual, familiar, comunitario, etc.)
    - modalidad: Modalidad de atención (presencial, virtual, mixta, etc.)
    - nivel_complejidad: Nivel de complejidad de la atención
    - estado: Estado de la atención (en_proceso, completada, etc.)
    - fecha_desde/fecha_hasta: Rango de fechas de inicio
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("*")
        
        # Aplicar filtros opcionales
        if tipo_abordaje:
            query = query.eq("tipo_abordaje_atencion", tipo_abordaje)
        if modalidad:
            query = query.eq("modalidad_atencion", modalidad)
        if nivel_complejidad:
            query = query.eq("nivel_complejidad_atencion", nivel_complejidad)
        if estado:
            query = query.eq("estado_atencion_integral", estado)
        if fecha_desde:
            query = query.gte("fecha_inicio_atencion_integral", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_inicio_atencion_integral", fecha_hasta.isoformat())
            
        # Aplicar paginación y orden
        query = query.order("fecha_inicio_atencion_integral", desc=True).range(skip, skip + limit - 1)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones integrales: {str(e)}"
        )


@router.get("/{atencion_id}", response_model=ModeloAtencionIntegralTransversalSaludRespuesta)
def obtener_atencion_integral_por_id(
    atencion_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una atención integral específica por su ID.
    """
    try:
        result = db.table("atencion_integral_transversal_salud").select("*").eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención integral con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener atención integral: {str(e)}"
        )


@router.get("/codigo/{codigo_atencion}", response_model=ModeloAtencionIntegralTransversalSaludRespuesta)
def obtener_atencion_integral_por_codigo(
    codigo_atencion: str, 
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una atención integral específica por su código identificador único.
    """
    try:
        result = db.table("atencion_integral_transversal_salud").select("*").eq("codigo_atencion_integral_unico", codigo_atencion).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención integral con código {codigo_atencion} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener atención integral por código: {str(e)}"
        )


@router.put("/{atencion_id}", response_model=ModeloAtencionIntegralTransversalSaludRespuesta)
def actualizar_atencion_integral_transversal_salud(
    atencion_id: UUID,
    atencion_actualizada: ModeloAtencionIntegralTransversalSaludActualizar,
    db: Client = Depends(get_supabase_client)
):
    """
    Actualizar una atención integral existente.
    
    Solo actualiza los campos proporcionados (actualización parcial).
    """
    try:
        # Preparar datos para actualización (solo campos no nulos)
        datos_actualizacion = atencion_actualizada.model_dump(exclude_unset=True, exclude_none=True)
        
        if not datos_actualizacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        # Ejecutar actualización
        result = db.table("atencion_integral_transversal_salud").update(datos_actualizacion).eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención integral con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar atención integral: {str(e)}"
        )


@router.delete("/{atencion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_atencion_integral_transversal_salud(
    atencion_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """
    Eliminar una atención integral (soft delete recomendado en producción).
    
    En entornos de producción se recomienda implementar soft delete 
    cambiando el estado en lugar de eliminar físicamente el registro.
    """
    try:
        result = db.table("atencion_integral_transversal_salud").delete().eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return  # 204 No Content - eliminación exitosa
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención integral con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar atención integral: {str(e)}"
        )


# =============================================================================
# ENDPOINTS ESPECIALIZADOS - FUNCIONALIDADES AVANZADAS
# =============================================================================

@router.get("/paciente/{paciente_id}/atenciones", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_atenciones_por_paciente(
    paciente_id: UUID,
    activas_solamente: bool = False,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar todas las atenciones integrales de un paciente específico.
    
    Permite ver el historial completo de atenciones integrales de un individuo
    para continuidad en el cuidado y seguimiento longitudinal.
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("*").eq("sujeto_atencion_individual_id", str(paciente_id))
        
        if activas_solamente:
            query = query.eq("estado_atencion_integral", "EN_PROCESO")
            
        query = query.order("fecha_inicio_atencion_integral", desc=True)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones por paciente: {str(e)}"
        )


@router.get("/familia/{familia_id}/atenciones", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_atenciones_por_familia(
    familia_id: UUID,
    activas_solamente: bool = False,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar todas las atenciones integrales de una familia específica.
    
    Enfoque familiar de atención integral según Resolución 3280.
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("*").eq("familia_integral_id", str(familia_id))
        
        if activas_solamente:
            query = query.eq("estado_atencion_integral", "EN_PROCESO")
            
        query = query.order("fecha_inicio_atencion_integral", desc=True)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones por familia: {str(e)}"
        )


@router.get("/entorno/{entorno_id}/atenciones", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_atenciones_por_entorno(
    entorno_id: UUID,
    activas_solamente: bool = False,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar todas las atenciones integrales asociadas a un entorno específico.
    
    Permite coordinación territorial de atenciones en entornos de salud pública.
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("*").eq("entorno_asociado_id", str(entorno_id))
        
        if activas_solamente:
            query = query.eq("estado_atencion_integral", "EN_PROCESO")
            
        query = query.order("fecha_inicio_atencion_integral", desc=True)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones por entorno: {str(e)}"
        )


@router.get("/profesional/{profesional_id}/atenciones-coordinadas", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_atenciones_coordinadas_por_profesional(
    profesional_id: UUID,
    activas_solamente: bool = True,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar todas las atenciones integrales coordinadas por un profesional específico.
    
    Útil para gestión de carga de trabajo y seguimiento de casos asignados.
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("*").eq("profesional_coordinador_id", str(profesional_id))
        
        if activas_solamente:
            query = query.eq("estado_atencion_integral", "EN_PROCESO")
            
        query = query.order("fecha_inicio_atencion_integral", desc=True)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones coordinadas por profesional: {str(e)}"
        )


@router.post("/{atencion_id}/finalizar", response_model=ModeloAtencionIntegralTransversalSaludRespuesta)
def finalizar_atencion_integral(
    atencion_id: UUID,
    fecha_finalizacion_real: Optional[datetime] = None,
    observaciones_cierre: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Finalizar una atención integral, cambiando su estado a COMPLETADA.
    
    Registra la fecha real de finalización y permite agregar observaciones de cierre.
    """
    try:
        datos_finalizacion = {
            "estado_atencion_integral": "COMPLETADA",
            "fecha_finalizacion_real": (fecha_finalizacion_real or datetime.now()).isoformat(),
            "fecha_ultima_evaluacion": datetime.now().isoformat()
        }
        
        if observaciones_cierre:
            # Agregar observaciones de cierre a las observaciones existentes
            datos_finalizacion["observaciones_adicionales_atencion"] = observaciones_cierre
        
        result = db.table("atencion_integral_transversal_salud").update(datos_finalizacion).eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención integral con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al finalizar atención integral: {str(e)}"
        )


@router.get("/reportes/por-tipo-abordaje", response_model=List[dict])
def reporte_atenciones_por_tipo_abordaje(
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de atenciones integrales agrupadas por tipo de abordaje.
    
    Útil para análisis de modalidades de atención más frecuentes.
    """
    try:
        query = db.table("atencion_integral_transversal_salud").select("tipo_abordaje_atencion")
        
        # Aplicar filtros de fecha si se proporcionan
        if fecha_desde:
            query = query.gte("fecha_inicio_atencion_integral", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_inicio_atencion_integral", fecha_hasta.isoformat())
            
        result = query.execute()
        
        # Agrupar resultados por tipo de abordaje
        conteo = {}
        for atencion in result.data:
            tipo = atencion["tipo_abordaje_atencion"]
            conteo[tipo] = conteo.get(tipo, 0) + 1
            
        return [{"tipo_abordaje": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte por tipo de abordaje: {str(e)}"
        )


@router.get("/reportes/por-complejidad", response_model=List[dict])
def reporte_atenciones_por_complejidad(
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de atenciones integrales agrupadas por nivel de complejidad.
    
    Permite identificar la distribución de complejidad de casos atendidos.
    """
    try:
        result = db.table("atencion_integral_transversal_salud").select("nivel_complejidad_atencion").execute()
        
        # Agrupar resultados por complejidad
        conteo = {}
        for atencion in result.data:
            complejidad = atencion["nivel_complejidad_atencion"]
            conteo[complejidad] = conteo.get(complejidad, 0) + 1
            
        return [{"nivel_complejidad": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte por complejidad: {str(e)}"
        )


@router.get("/vencimientos/proximas-evaluaciones", response_model=List[ModeloAtencionIntegralTransversalSaludRespuesta])
def listar_proximas_evaluaciones(
    dias_adelantados: int = 7,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones integrales que tienen evaluaciones próximas a vencer.
    
    Útil para programación de agenda y seguimiento proactivo.
    """
    try:
        fecha_limite = datetime.now() + timedelta(days=dias_adelantados)
        
        result = db.table("atencion_integral_transversal_salud")\
                  .select("*")\
                  .eq("estado_atencion_integral", "EN_PROCESO")\
                  .lte("proxima_fecha_seguimiento", fecha_limite.isoformat())\
                  .order("proxima_fecha_seguimiento")\
                  .execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar próximas evaluaciones: {str(e)}"
        )