# =============================================================================
# Rutas API REST - Familia Integral de Salud Pública
# Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from supabase import Client
from uuid import UUID

from database import get_supabase_client
from models.familia_integral_model import (
    ModeloFamiliaIntegralSaludPublicaCrear,
    ModeloFamiliaIntegralSaludPublicaRespuesta,
    ModeloFamiliaIntegralSaludPublicaActualizar
)

# =============================================================================
# CONFIGURACIÓN DEL ROUTER
# =============================================================================

router = APIRouter(
    prefix="/familia-integral-salud-publica",
    tags=["Familia Integral Salud Pública"],
    responses={404: {"description": "Familia no encontrada"}}
)

# =============================================================================
# ENDPOINTS CRUD - FAMILIA INTEGRAL
# =============================================================================

@router.post("/", response_model=ModeloFamiliaIntegralSaludPublicaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_familia_integral_salud_publica(
    familia: ModeloFamiliaIntegralSaludPublicaCrear, 
    db: Client = Depends(get_supabase_client)
):
    """
    Crear una nueva familia integral de salud pública.
    
    Registra una familia como sujeto de atención integral según la Resolución 3280 Art. 1364-1370:
    'La familia se asuma como sujeto de atención integral en salud'
    """
    try:
        # Preparar datos para inserción
        familia_data = familia.model_dump(exclude_unset=True)
        
        # Ejecutar inserción en Supabase
        result = db.table("familia_integral_salud_publica").insert(familia_data).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la familia: No se recibieron datos de respuesta"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear familia: {str(e)}"
        )


@router.get("/", response_model=List[ModeloFamiliaIntegralSaludPublicaRespuesta])
def listar_familias_integral_salud_publica(
    skip: int = 0,
    limit: int = 100,
    tipo_estructura: Optional[str] = None,
    ciclo_vital: Optional[str] = None,
    estado_seguimiento: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar familias integrales de salud pública con filtros opcionales.
    
    Permite filtrar por:
    - tipo_estructura: Tipo de estructura familiar
    - ciclo_vital: Ciclo vital familiar actual  
    - estado_seguimiento: Estado del seguimiento familiar
    """
    try:
        query = db.table("familia_integral_salud_publica").select("*")
        
        # Aplicar filtros opcionales
        if tipo_estructura:
            query = query.eq("tipo_estructura_familiar", tipo_estructura)
        if ciclo_vital:
            query = query.eq("ciclo_vital_familiar", ciclo_vital)
        if estado_seguimiento:
            query = query.eq("estado_seguimiento_familia", estado_seguimiento)
            
        # Aplicar paginación y orden
        query = query.order("creado_en", desc=True).range(skip, skip + limit - 1)
        
        result = query.execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar familias: {str(e)}"
        )


@router.get("/{familia_id}", response_model=ModeloFamiliaIntegralSaludPublicaRespuesta)
def obtener_familia_integral_por_id(
    familia_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una familia integral específica por su ID.
    """
    try:
        result = db.table("familia_integral_salud_publica").select("*").eq("id", str(familia_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Familia con ID {familia_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener familia: {str(e)}"
        )


@router.get("/codigo/{codigo_familia}", response_model=ModeloFamiliaIntegralSaludPublicaRespuesta)
def obtener_familia_integral_por_codigo(
    codigo_familia: str, 
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener una familia integral específica por su código identificador único.
    """
    try:
        result = db.table("familia_integral_salud_publica").select("*").eq("codigo_identificacion_familia_unico", codigo_familia).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Familia con código {codigo_familia} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener familia por código: {str(e)}"
        )


@router.put("/{familia_id}", response_model=ModeloFamiliaIntegralSaludPublicaRespuesta)
def actualizar_familia_integral_salud_publica(
    familia_id: UUID,
    familia_actualizada: ModeloFamiliaIntegralSaludPublicaActualizar,
    db: Client = Depends(get_supabase_client)
):
    """
    Actualizar una familia integral existente.
    
    Solo actualiza los campos proporcionados (actualización parcial).
    """
    try:
        # Preparar datos para actualización (solo campos no nulos)
        datos_actualizacion = familia_actualizada.model_dump(exclude_unset=True, exclude_none=True)
        
        if not datos_actualizacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron datos para actualizar"
            )
        
        # Ejecutar actualización
        result = db.table("familia_integral_salud_publica").update(datos_actualizacion).eq("id", str(familia_id)).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Familia con ID {familia_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar familia: {str(e)}"
        )


@router.delete("/{familia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_familia_integral_salud_publica(
    familia_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """
    Eliminar una familia integral (soft delete recomendado en producción).
    
    En entornos de producción se recomienda implementar soft delete 
    cambiando el estado en lugar de eliminar físicamente el registro.
    """
    try:
        result = db.table("familia_integral_salud_publica").delete().eq("id", str(familia_id)).execute()
        
        if result.data and len(result.data) > 0:
            return  # 204 No Content - eliminación exitosa
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Familia con ID {familia_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar familia: {str(e)}"
        )


# =============================================================================
# ENDPOINTS ESPECIALIZADOS - REPORTES Y ANÁLISIS
# =============================================================================

@router.get("/reportes/por-tipo-estructura", response_model=List[dict])
def reporte_familias_por_tipo_estructura(
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de familias agrupadas por tipo de estructura familiar.
    
    Útil para análisis epidemiológico y planificación de intervenciones.
    """
    try:
        result = db.rpc("get_familias_por_tipo_estructura").execute()
        
        if result.data:
            return result.data
        else:
            # Si no existe la función RPC, hacer consulta manual
            result = db.table("familia_integral_salud_publica").select("tipo_estructura_familiar").execute()
            
            # Agrupar manualmente los resultados
            conteo = {}
            for familia in result.data:
                tipo = familia["tipo_estructura_familiar"]
                conteo[tipo] = conteo.get(tipo, 0) + 1
                
            return [{"tipo_estructura": k, "cantidad": v} for k, v in conteo.items()]
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte: {str(e)}"
        )


@router.get("/reportes/por-ciclo-vital", response_model=List[dict])
def reporte_familias_por_ciclo_vital(
    db: Client = Depends(get_supabase_client)
):
    """
    Generar reporte de familias agrupadas por ciclo vital familiar.
    
    Permite identificar necesidades específicas por etapa vital.
    """
    try:
        result = db.table("familia_integral_salud_publica").select("ciclo_vital_familiar").execute()
        
        # Agrupar resultados por ciclo vital
        conteo = {}
        for familia in result.data:
            ciclo = familia["ciclo_vital_familiar"]
            conteo[ciclo] = conteo.get(ciclo, 0) + 1
            
        return [{"ciclo_vital": k, "cantidad": v} for k, v in conteo.items()]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte por ciclo vital: {str(e)}"
        )


@router.get("/buscar/por-jefe-hogar", response_model=List[ModeloFamiliaIntegralSaludPublicaRespuesta])
def buscar_familias_por_jefe_hogar(
    nombre_jefe: str,
    db: Client = Depends(get_supabase_client)
):
    """
    Buscar familias por nombre del jefe de hogar.
    
    Permite búsqueda parcial (contiene texto) para facilitar localización de familias.
    """
    try:
        result = db.table("familia_integral_salud_publica").select("*").ilike("nombre_apellidos_jefe_hogar", f"%{nombre_jefe}%").execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en búsqueda por jefe de hogar: {str(e)}"
        )


@router.get("/entorno/{entorno_id}/familias", response_model=List[ModeloFamiliaIntegralSaludPublicaRespuesta])
def listar_familias_por_entorno(
    entorno_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar todas las familias asociadas a un entorno específico de salud pública.
    
    Permite ver qué familias están adscritas a un entorno particular para 
    intervenciones territoriales coordenadas.
    """
    try:
        result = db.table("familia_integral_salud_publica").select("*").eq("entorno_salud_publica_id", str(entorno_id)).execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar familias por entorno: {str(e)}"
        )