# =============================================================================
# Rutas Atención Vejez - SPRINT #3: CENTRALIZACIÓN TOTAL COMPLETADA
# Fecha: 17 septiembre 2025 - APLICACIÓN SUGERENCIAS ASESOR EXTERNO
# Objetivo: Perfeccionar patrón RPC+Service con centralización TOTAL de lógica
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
# Migración Base: 20250917120000_create_atencion_vejez_table.sql
#
# ARQUITECTURA SPRINT #3:
# ✅ CENTRALIZACIÓN TOTAL: 100% lógica delegada al service layer
# ✅ VALIDACIONES CENTRALIZADAS: Todas en AtencionVejezService
# ✅ CERO LÓGICA EN ENDPOINTS: Solo delegación y manejo de errores
# ✅ PATRÓN RPC+SERVICE PERFECCIONADO: Consistencia total con control_cronicidad
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from database import get_supabase_client
from models.atencion_vejez_model_fixed import (
    AtencionVejezCrear,
    AtencionVejezActualizar,
    AtencionVejezResponse
)
from services.atencion_vejez_service import AtencionVejezService

router = APIRouter(prefix="/atencion-vejez", tags=["Atención Vejez"])

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - SPRINT #3: CENTRALIZACIÓN TOTAL
# Patrón: Delegación completa al service layer, cero lógica en endpoints
# =============================================================================

@router.post("/", response_model=AtencionVejezResponse, status_code=201)
async def crear_atencion_vejez(
    atencion_data: AtencionVejezCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nueva atención vejez - SPRINT PILOTO #1 COMPLETO:
    ✅ RPC Transaccional: Operaciones atómicas (Auditoría Backend - Crítico #1)
    ✅ Capa de Servicio: Lógica centralizada (Auditoría Backend - Alto #2)
    ✅ Validaciones: Business logic separada de infrastructure
    ✅ Recomendaciones: Generación automática basada en evaluación
    """
    try:
        # Delegar toda la lógica compleja al servicio centralizado
        return await AtencionVejezService.crear_atencion_vejez_completa(atencion_data)

    except ValueError as e:
        # Errores de validación de negocio
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en crear_atencion_vejez: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/{atencion_id}", response_model=AtencionVejezResponse)
async def obtener_atencion_vejez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Obtener atención vejez por ID - SPRINT #3 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionVejezService.obtener_atencion_vejez_por_id(atencion_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrada)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en obtener_atencion_vejez: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[AtencionVejezResponse])
async def listar_atenciones_vejez(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db=Depends(get_supabase_client)
):
    """
    Listar atenciones vejez con paginación - SPRINT #3 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de paginación centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionVejezService.listar_atenciones_vejez(skip, limit)

    except ValueError as e:
        # Errores de validación de negocio (ej: parámetros inválidos)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en listar_atenciones_vejez: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/paciente/{paciente_id}", response_model=List[AtencionVejezResponse])
async def listar_atenciones_vejez_por_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Listar atenciones vejez por paciente - SPRINT #3 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Lógica de filtrado centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionVejezService.listar_atenciones_vejez_por_paciente(paciente_id)

    except Exception as e:
        print(f"Error en listar_atenciones_vejez_por_paciente: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{atencion_id}", response_model=AtencionVejezResponse)
async def actualizar_atencion_vejez(
    atencion_id: UUID,
    atencion_data: AtencionVejezActualizar,
    db=Depends(get_supabase_client)
):
    """
    Actualizar atención vejez - SPRINT #3 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Validaciones de negocio centralizadas
    ✅ Lógica de actualización centralizada
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Preparar datos para el servicio
        update_data = {k: v for k, v in atencion_data.model_dump(exclude_unset=True).items() if v is not None}

        # Delegar toda la lógica al servicio centralizado
        return await AtencionVejezService.actualizar_atencion_vejez(atencion_id, update_data)

    except ValueError as e:
        # Errores de validación de negocio
        if "no encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en actualizar_atencion_vejez: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{atencion_id}")
async def eliminar_atencion_vejez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """
    Eliminar atención vejez - SPRINT #3 CENTRALIZACIÓN TOTAL:
    ✅ Delegación completa al service layer
    ✅ Lógica de eliminación transaccional centralizada
    ✅ Validaciones de existencia centralizadas
    ✅ Patrón RPC+Service perfeccionado
    """
    try:
        # Delegar toda la lógica al servicio centralizado
        return await AtencionVejezService.eliminar_atencion_vejez(atencion_id)

    except ValueError as e:
        # Errores de validación de negocio (ej: no encontrada)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error en eliminar_atencion_vejez: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# =============================================================================
# ENDPOINTS ESPECIALIZADOS PARA VEJEZ
# =============================================================================

@router.get("/estadisticas/resumen")
async def obtener_estadisticas_vejez(
    db=Depends(get_supabase_client)
):
    """Obtener estadísticas especializadas de atenciones vejez usando lógica centralizada"""
    try:
        # Delegar cálculos especializados al servicio
        return await AtencionVejezService.obtener_estadisticas_vejez()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")