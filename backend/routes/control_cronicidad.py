# =============================================================================
# Rutas Control Cronicidad - SPRINT #5: CENTRALIZACIÓN TOTAL COMPLETADA
# Fecha: 18 septiembre 2025 - APLICACIÓN PATRÓN RPC+SERVICE PERFECCIONADO
# Objetivo: Delegación TOTAL al service layer (referencia: AtencionVejezService Sprint #3)
# Base Normativa: Control enfermedades crónicas no transmisibles
#
# ARQUITECTURA SPRINT #5:
# ✅ CENTRALIZACIÓN TOTAL: 100% lógica delegada al service layer
# ✅ VALIDACIONES CENTRALIZADAS: Todas en ControlCronicidadService
# ✅ CERO LÓGICA EN ENDPOINTS: Solo delegación y manejo de errores
# ✅ PATRÓN RPC+SERVICE PERFECCIONADO: Consistencia total con Sprint #3/#4
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID
from datetime import date
from database import get_supabase_client
from models.control_cronicidad_model import (
    ControlCronicidadCrear,
    ControlCronicidadActualizar,
    ControlCronicidadResponse
)
from services.control_cronicidad_service import ControlCronicidadService

router = APIRouter(prefix="/control-cronicidad", tags=["Control de Cronicidad"])

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - SPRINT #5: CENTRALIZACIÓN TOTAL
# Patrón: Delegación completa al service layer, cero lógica en endpoints
# =============================================================================

@router.post("/", response_model=ControlCronicidadResponse, status_code=201)
async def crear_control_cronicidad(
    control_data: ControlCronicidadCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nuevo control de cronicidad - SPRINT #5 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Lógica polimórfica centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await ControlCronicidadService.crear_control_cronicidad_completo(control_data)

    except ValueError as e:
        # Errores de validación de negocio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en crear_control_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[ControlCronicidadResponse])
async def listar_controles_cronicidad(
    paciente_id: Optional[UUID] = Query(None, description="Filtrar por paciente"),
    tipo_cronicidad: Optional[str] = Query(None, description="Filtrar por tipo de cronicidad"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    db=Depends(get_supabase_client)
):
    """
    Listar controles de cronicidad con filtros - SPRINT #5 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de paginación centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await ControlCronicidadService.listar_controles_cronicidad(
            skip=offset,
            limit=limit,
            paciente_id=paciente_id,
            tipo_cronicidad=tipo_cronicidad
        )

    except ValueError as e:
        # Errores de validación de negocio (ej: parámetros inválidos)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en listar_controles_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{control_id}", response_model=ControlCronicidadResponse)
async def obtener_control_cronicidad(
    control_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Obtener control cronicidad por ID - SPRINT #5 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await ControlCronicidadService.obtener_control_cronicidad_por_id(control_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrado)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en obtener_control_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{control_id}", response_model=ControlCronicidadResponse)
async def actualizar_control_cronicidad(
    control_id: UUID,
    control_data: ControlCronicidadActualizar,
    db=Depends(get_supabase_client)
):
    """
    Actualizar control cronicidad - SPRINT #5 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Lógica de actualización centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Preparar datos para el servicio
        update_data = {k: v for k, v in control_data.model_dump(exclude_unset=True).items() if v is not None}

        # Delegar toda la lógica al servicio centralizado
        return await ControlCronicidadService.actualizar_control_cronicidad(control_id, update_data)

    except ValueError as e:
        # Errores de validación de negocio
        if "no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en actualizar_control_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{control_id}")
async def eliminar_control_cronicidad(
    control_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Eliminar control cronicidad - SPRINT #5 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Lógica de eliminación transaccional centralizada
    ✅ Validaciones de existencia centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await ControlCronicidadService.eliminar_control_cronicidad(control_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrado)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en eliminar_control_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# =============================================================================
# ENDPOINTS ESPECIALIZADOS - SPRINT #5: CENTRALIZACIÓN TOTAL
# =============================================================================

@router.get("/paciente/{paciente_id}/cronologicos", response_model=List[ControlCronicidadResponse])
async def obtener_controles_cronologicos_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Obtener historial cronológico de controles por paciente - SPRINT #5:
    ✅ Usa service layer para lógica de listado
    ✅ Filtro específico por paciente
    """
    try:
        # Usar service layer con filtro de paciente
        return await ControlCronicidadService.listar_controles_por_paciente(paciente_id)

    except Exception as e:
        print(f"Error en obtener_controles_cronologicos_paciente: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/estadisticas/resumen")
async def obtener_estadisticas_cronicidad(
    db=Depends(get_supabase_client)
):
    """
    Obtener estadísticas especializadas de controles cronicidad - SPRINT #5:
    ✅ Delegación completa al service layer
    ✅ Estadísticas centralizadas
    """
    try:
        # Delegar cálculos especializados al servicio
        return await ControlCronicidadService.obtener_estadisticas_cronicidad()

    except Exception as e:
        print(f"Error en obtener_estadisticas_cronicidad: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

