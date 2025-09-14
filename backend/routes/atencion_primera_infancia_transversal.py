# =============================================================================
# Rutas API REST - Atención Integral Primera Infancia Transversal 
# Resolución 3280 de 2018 - RPMS (Ruta de Promoción y Mantenimiento de Salud)
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from supabase import Client
from uuid import UUID
from datetime import datetime

from database import get_supabase_client
from models import (
    AtencionIntegralPrimeraInfanciaTransversal,
    AtencionPrimeraInfanciaCrear,
    AtencionPrimeraInfanciaActualizar,
    AtencionPrimeraInfanciaRespuesta,
    EstadoNutricionalPrimeraInfancia,
    ResultadoTamizajeDesarrollo,
    EstadoEsquemaVacunacion
)

# =============================================================================
# CONFIGURACIÓN DEL ROUTER
# =============================================================================

router = APIRouter(
    prefix="/atencion-primera-infancia-transversal", 
    tags=["Atención Primera Infancia Transversal"],
    responses={404: {"description": "Atención de primera infancia no encontrada"}}
)

# =============================================================================
# ENDPOINTS CRUD - PRIMERA INFANCIA TRANSVERSAL
# =============================================================================

@router.post("/", response_model=AtencionPrimeraInfanciaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_atencion_primera_infancia_transversal(
    atencion: AtencionPrimeraInfanciaCrear,
    db: Client = Depends(get_supabase_client)
):
    """
    Crear nueva atención integral de primera infancia con arquitectura transversal.
    
    Integra referencias a:
    - Entorno de desarrollo del menor
    - Familia integral de pertenencia  
    - Atención integral coordinada transversal
    """
    try:
        # Preparar datos para inserción con generación automática de código
        atencion_data = atencion.model_dump(exclude_unset=True)
        
        # Convertir datetime a string ISO para Supabase
        if "fecha_atencion_primera_infancia" in atencion_data:
            if isinstance(atencion_data["fecha_atencion_primera_infancia"], datetime):
                atencion_data["fecha_atencion_primera_infancia"] = atencion_data["fecha_atencion_primera_infancia"].isoformat()
        
        # Ejecutar inserción en Supabase (el trigger generará el código automáticamente)
        result = db.table("atencion_primera_infancia").insert(atencion_data).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la atención de primera infancia: No se recibieron datos de respuesta"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear atención de primera infancia: {str(e)}"
        )


@router.get("/", response_model=List[AtencionPrimeraInfanciaRespuesta])
def listar_atenciones_primera_infancia_transversal(
    skip: int = 0,
    limit: int = 100,
    entorno_id: Optional[UUID] = None,
    familia_id: Optional[UUID] = None, 
    estado_nutricional: Optional[EstadoNutricionalPrimeraInfancia] = None,
    estado_vacunacion: Optional[EstadoEsquemaVacunacion] = None,
    resultado_desarrollo: Optional[ResultadoTamizajeDesarrollo] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones de primera infancia con filtros transversales.
    
    Permite filtrar por:
    - entorno_id: Entorno de desarrollo asociado
    - familia_id: Familia integral de pertenencia
    - estado_nutricional: Estado nutricional del menor
    - estado_vacunacion: Estado del esquema de vacunación
    - resultado_desarrollo: Resultado del tamizaje de desarrollo
    """
    try:
        query = db.table("atencion_primera_infancia").select("*")
        
        # Aplicar filtros opcionales
        if entorno_id:
            query = query.eq("entorno_desarrollo_asociado_id", str(entorno_id))
        if familia_id:
            query = query.eq("familia_integral_pertenencia_id", str(familia_id))
        if estado_nutricional:
            query = query.eq("estado_nutricional_evaluacion", estado_nutricional)
        if estado_vacunacion:
            query = query.eq("esquema_vacunacion_estado_actual", estado_vacunacion)
        if resultado_desarrollo:
            query = query.eq("tamizaje_desarrollo_integral_resultado", resultado_desarrollo)
            
        # Aplicar paginación y orden por fecha
        query = query.order("fecha_atencion_primera_infancia", desc=True).range(skip, skip + limit - 1)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones de primera infancia: {str(e)}"
        )


@router.get("/{atencion_id}", response_model=AtencionPrimeraInfanciaRespuesta)
def obtener_atencion_primera_infancia_por_id(
    atencion_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una atención de primera infancia específica por su ID.
    """
    try:
        result = db.table("atencion_primera_infancia").select("*").eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención de primera infancia con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener atención de primera infancia: {str(e)}"
        )


@router.get("/codigo/{codigo_atencion}", response_model=AtencionPrimeraInfanciaRespuesta)  
def obtener_atencion_primera_infancia_por_codigo(
    codigo_atencion: str,
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una atención de primera infancia por su código único.
    """
    try:
        result = db.table("atencion_primera_infancia").select("*").eq("codigo_atencion_primera_infancia_unico", codigo_atencion).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención de primera infancia con código {codigo_atencion} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener atención por código: {str(e)}"
        )


@router.put("/{atencion_id}", response_model=AtencionPrimeraInfanciaRespuesta)
def actualizar_atencion_primera_infancia_transversal(
    atencion_id: UUID,
    atencion_actualizada: AtencionPrimeraInfanciaActualizar,
    db: Client = Depends(get_supabase_client)
):
    """
    Actualizar una atención de primera infancia existente.
    
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
        result = db.table("atencion_primera_infancia").update(datos_actualizacion).eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención de primera infancia con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar atención de primera infancia: {str(e)}"
        )


@router.delete("/{atencion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_atencion_primera_infancia_transversal(
    atencion_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """
    Eliminar una atención de primera infancia (soft delete recomendado en producción).
    """
    try:
        result = db.table("atencion_primera_infancia").delete().eq("id", str(atencion_id)).execute()
        
        if result.data and len(result.data) > 0:
            return  # 204 No Content - eliminación exitosa
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atención de primera infancia con ID {atencion_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar atención de primera infancia: {str(e)}"
        )


# =============================================================================
# ENDPOINTS ESPECIALIZADOS TRANSVERSALES
# =============================================================================

@router.get("/menor/{menor_id}/historial", response_model=List[AtencionPrimeraInfanciaRespuesta])
def obtener_historial_atencion_menor(
    menor_id: UUID,
    incluir_familia: bool = False,
    incluir_entorno: bool = False,
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener historial completo de atenciones de primera infancia de un menor.
    
    Permite incluir información de contexto familiar y del entorno.
    """
    try:
        # Query base usando sujeto_atencion_menor_id o paciente_id como fallback
        query = db.table("atencion_primera_infancia").select("*")
        
        # Intentar con el nuevo campo primero, luego con el legacy
        result_new = query.eq("sujeto_atencion_menor_id", str(menor_id)).execute()
        
        if not result_new.data:
            # Fallback al campo legacy
            result_legacy = db.table("atencion_primera_infancia").select("*").eq("paciente_id", str(menor_id)).execute()
            result = result_legacy
        else:
            result = result_new
        
        query = query.order("fecha_atencion_primera_infancia", desc=True)
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial del menor: {str(e)}"
        )


@router.get("/entorno/{entorno_id}/atenciones", response_model=List[AtencionPrimeraInfanciaRespuesta])
def listar_atenciones_por_entorno(
    entorno_id: UUID,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones de primera infancia por entorno de desarrollo.
    
    Útil para análisis territorial de salud infantil.
    """
    try:
        query = db.table("atencion_primera_infancia").select("*").eq("entorno_desarrollo_asociado_id", str(entorno_id))
        
        if fecha_desde:
            query = query.gte("fecha_atencion_primera_infancia", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_atencion_primera_infancia", fecha_hasta.isoformat())
            
        query = query.order("fecha_atencion_primera_infancia", desc=True)
        
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


@router.get("/familia/{familia_id}/menores", response_model=List[AtencionPrimeraInfanciaRespuesta])
def listar_atenciones_menores_familia(
    familia_id: UUID,
    incluir_resumen_familiar: bool = True,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones de primera infancia de todos los menores de una familia.
    
    Permite análisis de salud infantil a nivel familiar.
    """
    try:
        query = db.table("atencion_primera_infancia").select("*").eq("familia_integral_pertenencia_id", str(familia_id))
        query = query.order("fecha_atencion_primera_infancia", desc=True)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones de menores de la familia: {str(e)}"
        )


# =============================================================================
# ENDPOINTS DE REPORTERÍA Y ANÁLISIS 
# =============================================================================

@router.get("/reportes/estado-nutricional", response_model=List[dict])
def reporte_estado_nutricional(
    entorno_id: Optional[UUID] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de estados nutricionales de primera infancia.
    
    Permite filtrar por entorno y rango de fechas.
    """
    try:
        query = db.table("atencion_primera_infancia").select("estado_nutricional_evaluacion")
        
        # Aplicar filtros opcionales
        if entorno_id:
            query = query.eq("entorno_desarrollo_asociado_id", str(entorno_id))
        if fecha_desde:
            query = query.gte("fecha_atencion_primera_infancia", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_atencion_primera_infancia", fecha_hasta.isoformat())
            
        result = query.execute()
        
        # Agrupar resultados por estado nutricional
        conteo = {}
        for atencion in result.data:
            estado = atencion["estado_nutricional_evaluacion"] or "NO_EVALUADO"
            conteo[estado] = conteo.get(estado, 0) + 1
            
        return [{"estado_nutricional": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte nutricional: {str(e)}"
        )


@router.get("/reportes/cobertura-vacunacion", response_model=List[dict])  
def reporte_cobertura_vacunacion(
    entorno_id: Optional[UUID] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de cobertura de vacunación por entorno.
    """
    try:
        query = db.table("atencion_primera_infancia").select("esquema_vacunacion_estado_actual")
        
        if entorno_id:
            query = query.eq("entorno_desarrollo_asociado_id", str(entorno_id))
            
        result = query.execute()
        
        # Agrupar resultados por estado de vacunación
        conteo = {}
        for atencion in result.data:
            estado = atencion["esquema_vacunacion_estado_actual"] or "NO_EVALUADO"
            conteo[estado] = conteo.get(estado, 0) + 1
            
        return [{"estado_vacunacion": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte de vacunación: {str(e)}"
        )


@router.get("/reportes/desarrollo-integral", response_model=List[dict])
def reporte_desarrollo_integral(
    familia_id: Optional[UUID] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de desarrollo integral por familia o general.
    """
    try:
        query = db.table("atencion_primera_infancia").select("tamizaje_desarrollo_integral_resultado")
        
        if familia_id:
            query = query.eq("familia_integral_pertenencia_id", str(familia_id))
            
        result = query.execute()
        
        # Agrupar resultados por resultado de desarrollo
        conteo = {}
        for atencion in result.data:
            resultado = atencion["tamizaje_desarrollo_integral_resultado"] or "NO_EVALUADO"
            conteo[resultado] = conteo.get(resultado, 0) + 1
            
        return [{"resultado_desarrollo": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte de desarrollo: {str(e)}"
        )