# =============================================================================
# Rutas Atención Infancia - SPRINT #4: CENTRALIZACIÓN TOTAL COMPLETADA
# Fecha: 18 septiembre 2025 - APLICACIÓN PATRÓN RPC+SERVICE PERFECCIONADO
# Objetivo: Delegación TOTAL al service layer (referencia: AtencionVejezService Sprint #3)
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2 (Infancia 6-11 años)
#
# ARQUITECTURA SPRINT #4:
# ✅ CENTRALIZACIÓN TOTAL: 100% lógica delegada al service layer
# ✅ VALIDACIONES CENTRALIZADAS: Todas en AtencionInfanciaService
# ✅ CERO LÓGICA EN ENDPOINTS: Solo delegación y manejo de errores
# ✅ PATRÓN RPC+SERVICE PERFECCIONADO: Consistencia total con Sprint #3
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID
from datetime import date
from database import get_supabase_client
from models.atencion_infancia_model import (
    AtencionInfanciaCrear,
    AtencionInfanciaActualizar,
    AtencionInfanciaResponse,
    DesempenoEscolar
)
from services.atencion_infancia_service import AtencionInfanciaService

router = APIRouter(prefix="/atencion-infancia", tags=["Atención Infancia"])

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - SPRINT #4: CENTRALIZACIÓN TOTAL
# Patrón: Delegación completa al service layer, cero lógica en endpoints
# =============================================================================

@router.post("/", response_model=AtencionInfanciaResponse, status_code=201)
async def crear_atencion_infancia(
    atencion_data: AtencionInfanciaCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nueva atención infancia - SPRINT #4 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Lógica polimórfica centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionInfanciaService.crear_atencion_infancia_completa(atencion_data)

    except ValueError as e:
        # Errores de validación de negocio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en crear_atencion_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[AtencionInfanciaResponse])
async def listar_atenciones_infancia(
    paciente_id: Optional[UUID] = Query(None, description="Filtrar por paciente"),
    desempeno_escolar: Optional[DesempenoEscolar] = Query(None, description="Filtrar por desempeño escolar"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    db=Depends(get_supabase_client)
):
    """
    Listar atenciones infancia con filtros - SPRINT #4 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de paginación centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionInfanciaService.listar_atenciones_infancia(
            skip=offset,
            limit=limit,
            paciente_id=paciente_id,
            desempeno_escolar=desempeno_escolar
        )

    except ValueError as e:
        # Errores de validación de negocio (ej: parámetros inválidos)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en listar_atenciones_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{atencion_id}", response_model=AtencionInfanciaResponse)
async def obtener_atencion_infancia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Obtener atención infancia por ID - SPRINT #4 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionInfanciaService.obtener_atencion_infancia_por_id(atencion_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrada)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en obtener_atencion_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{atencion_id}", response_model=AtencionInfanciaResponse)
async def actualizar_atencion_infancia(
    atencion_id: UUID,
    atencion_data: AtencionInfanciaActualizar,
    db=Depends(get_supabase_client)
):
    """
    Actualizar atención infancia - SPRINT #4 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Lógica de actualización centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Preparar datos para el servicio
        update_data = {k: v for k, v in atencion_data.model_dump(exclude_unset=True).items() if v is not None}

        # Delegar toda la lógica al servicio centralizado
        return await AtencionInfanciaService.actualizar_atencion_infancia(atencion_id, update_data)

    except ValueError as e:
        # Errores de validación de negocio
        if "no encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en actualizar_atencion_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{atencion_id}")
async def eliminar_atencion_infancia(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Eliminar atención infancia - SPRINT #4 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Lógica de eliminación transaccional centralizada
    ✅ Validaciones de existencia centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionInfanciaService.eliminar_atencion_infancia(atencion_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrada)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en eliminar_atencion_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# =============================================================================
# ENDPOINTS ESPECIALIZADOS - SPRINT #4: CENTRALIZACIÓN TOTAL
# =============================================================================

@router.get("/paciente/{paciente_id}/cronologicas", response_model=List[AtencionInfanciaResponse])
async def obtener_atenciones_cronologicas_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Obtener historial cronológico de atenciones por paciente - SPRINT #4:
    ✅ Usa service layer para lógica de listado
    ✅ Filtro específico por paciente
    """
    try:
        # Usar service layer con filtro de paciente
        return await AtencionInfanciaService.listar_atenciones_infancia(
            skip=0,
            limit=100,  # Límite alto para historial completo
            paciente_id=paciente_id
        )

    except Exception as e:
        print(f"Error en obtener_atenciones_cronologicas_paciente: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/estadisticas/resumen")
async def obtener_estadisticas_infancia(
    db=Depends(get_supabase_client)
):
    """
    Obtener estadísticas especializadas de atenciones infancia - SPRINT #4:
    ✅ Delegación completa al service layer
    ✅ Estadísticas centralizadas
    """
    try:
        # Delegar cálculos especializados al servicio
        return await AtencionInfanciaService.obtener_estadisticas_infancia()

    except Exception as e:
        print(f"Error en obtener_estadisticas_infancia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")