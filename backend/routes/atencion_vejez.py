# =============================================================================
# Rutas Atención Vejez - SINCRONIZADO CON MIGRACIÓN REAL
# Fecha: 17 septiembre 2025 - CORRECCIÓN CRÍTICA
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
# Migración Base: 20250917120000_create_atencion_vejez_table.sql
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
# FUNCIONES HELPER
# =============================================================================

def agregar_metadatos_auditoria(data: dict) -> dict:
    """Agregar metadatos de auditoría"""
    # Esta tabla no tiene campos creado_en/updated_at según migración real
    return data

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - SINCRONIZADOS CON MIGRACIÓN REAL
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
    """Obtener atención vejez por ID"""
    try:
        response = db.table("atencion_vejez").select("*").eq("id", str(atencion_id)).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Atención vejez no encontrada")

        return AtencionVejezResponse(**response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[AtencionVejezResponse])
async def listar_atenciones_vejez(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db=Depends(get_supabase_client)
):
    """Listar todas las atenciones vejez con paginación"""
    try:
        response = db.table("atencion_vejez").select("*").range(skip, skip + limit - 1).execute()

        return [AtencionVejezResponse(**item) for item in response.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/paciente/{paciente_id}", response_model=List[AtencionVejezResponse])
async def listar_atenciones_vejez_por_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """Listar atenciones vejez de un paciente específico"""
    try:
        response = db.table("atencion_vejez").select("*").eq("paciente_id", str(paciente_id)).order("fecha_atencion", desc=True).execute()

        return [AtencionVejezResponse(**item) for item in response.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put("/{atencion_id}", response_model=AtencionVejezResponse)
async def actualizar_atencion_vejez(
    atencion_id: UUID,
    atencion_data: AtencionVejezActualizar,
    db=Depends(get_supabase_client)
):
    """Actualizar atención vejez existente"""
    try:
        # Verificar que existe
        existing = db.table("atencion_vejez").select("id").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Atención vejez no encontrada")

        # Preparar datos para actualización
        update_data = {k: v for k, v in atencion_data.model_dump(exclude_unset=True).items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Actualizar
        response = db.table("atencion_vejez").update(update_data).eq("id", str(atencion_id)).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Error actualizando atención vejez")

        return AtencionVejezResponse(**response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{atencion_id}")
async def eliminar_atencion_vejez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Eliminar atención vejez y su atención general asociada"""
    try:
        # Obtener atencion_id general antes de eliminar
        vejez_record = db.table("atencion_vejez").select("atencion_id").eq("id", str(atencion_id)).execute()

        if not vejez_record.data:
            raise HTTPException(status_code=404, detail="Atención vejez no encontrada")

        atencion_general_id = vejez_record.data[0].get("atencion_id")

        # Eliminar de atencion_vejez
        delete_vejez = db.table("atencion_vejez").delete().eq("id", str(atencion_id)).execute()

        # Eliminar de atenciones si existe referencia
        if atencion_general_id:
            db.table("atenciones").delete().eq("id", atencion_general_id).execute()

        return {"message": "Atención vejez eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
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