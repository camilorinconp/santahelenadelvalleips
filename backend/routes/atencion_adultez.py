# =============================================================================
# Rutas Atención Adultez - Arquitectura Vertical
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 17 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.5 (Adultez 30-59 años)
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from database import get_supabase_client
from models.atencion_adultez_model import (
    AtencionAdultezCrear,
    AtencionAdultezActualizar,
    AtencionAdultezResponse,
    EstadisticasAdultezResponse,
    EstadoNutricionalAdulto,
    RiesgoCardiovascularFramingham,
    TamizajeECNT,
    SaludMentalLaboral
)

router = APIRouter(prefix="/atencion-adultez", tags=["Atención Adultez"])

# =============================================================================
# FUNCIONES HELPER
# =============================================================================

def calcular_campos_automaticos(atencion_data: dict) -> dict:
    """Calcular todos los campos automáticos para respuesta API"""
    return AtencionAdultezResponse.calcular_campos_automaticos(atencion_data)

def agregar_metadatos_auditoria(data: dict) -> dict:
    """Agregar metadatos de auditoría"""
    now = datetime.now()
    data["created_at"] = now
    data["updated_at"] = now
    return data

# =============================================================================
# ENDPOINTS CRUD BÁSICOS - PATRÓN VERTICAL CONSOLIDADO
# =============================================================================

@router.post("/", response_model=AtencionAdultezResponse, status_code=201)
async def crear_atencion_adultez(
    atencion_data: AtencionAdultezCrear,
    db=Depends(get_supabase_client)
):
    """
    Crear nueva atención adultez con patrón polimórfico 3 pasos:
    1. Crear en tabla específica atencion_adultez
    2. Crear atención general con referencia
    3. Actualizar atencion_adultez con atencion_id
    """
    try:
        # PASO 1: Preparar datos y crear registro específico (sin atencion_id)
        atencion_dict = atencion_data.model_dump()
        atencion_dict["id"] = str(uuid4())
        atencion_dict = agregar_metadatos_auditoria(atencion_dict)

        # Calcular campos automáticos
        atencion_dict = calcular_campos_automaticos(atencion_dict)

        # Crear en tabla atencion_adultez (sin atencion_id)
        atencion_dict_sin_atencion = atencion_dict.copy()
        if 'atencion_id' in atencion_dict_sin_atencion:
            del atencion_dict_sin_atencion['atencion_id']

        response_adultez = db.table("atencion_adultez").insert(atencion_dict_sin_atencion).execute()

        if not response_adultez.data:
            raise HTTPException(status_code=500, detail="Error creando atención adultez")

        adultez_id = response_adultez.data[0]["id"]

        # PASO 2: Crear atención general
        atencion_general = {
            "id": str(uuid4()),
            "paciente_id": str(atencion_data.paciente_id),
            "tipo_atencion": "atencion_adultez",
            "detalle_id": adultez_id,
            "fecha_atencion": atencion_data.fecha_atencion.isoformat(),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        response_general = db.table("atenciones").insert(atencion_general).execute()

        if not response_general.data:
            raise HTTPException(status_code=500, detail="Error creando atención general")

        atencion_general_id = response_general.data[0]["id"]

        # PASO 3: Actualizar registro específico con atencion_id
        update_response = db.table("atencion_adultez").update(
            {"atencion_id": atencion_general_id}
        ).eq("id", adultez_id).execute()

        if not update_response.data:
            raise HTTPException(status_code=500, detail="Error actualizando atencion_id")

        # Retornar respuesta final con campos calculados
        final_data = update_response.data[0]
        final_data = calcular_campos_automaticos(final_data)

        return AtencionAdultezResponse(**final_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{atencion_id}", response_model=AtencionAdultezResponse)
async def obtener_atencion_adultez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener atención adultez por ID"""
    response = db.table("atencion_adultez").select("*").eq("id", str(atencion_id)).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Atención adultez no encontrada")

    # Calcular campos automáticos para respuesta
    atencion_data = calcular_campos_automaticos(response.data[0])
    return AtencionAdultezResponse(**atencion_data)

@router.get("/", response_model=List[AtencionAdultezResponse])
async def listar_atenciones_adultez(
    paciente_id: Optional[UUID] = Query(None, description="Filtrar por paciente"),
    limite: int = Query(100, description="Límite de resultados"),
    offset: int = Query(0, description="Offset para paginación"),
    db=Depends(get_supabase_client)
):
    """Listar atenciones adultez con filtros opcionales"""
    query = db.table("atencion_adultez").select("*")

    if paciente_id:
        query = query.eq("paciente_id", str(paciente_id))

    response = query.range(offset, offset + limite - 1).execute()

    # Calcular campos automáticos para todas las respuestas
    atenciones_procesadas = []
    for atencion in response.data:
        atencion_procesada = calcular_campos_automaticos(atencion)
        atenciones_procesadas.append(AtencionAdultezResponse(**atencion_procesada))

    return atenciones_procesadas

@router.put("/{atencion_id}", response_model=AtencionAdultezResponse)
async def actualizar_atencion_adultez(
    atencion_id: UUID,
    atencion_data: AtencionAdultezActualizar,
    db=Depends(get_supabase_client)
):
    """Actualizar atención adultez existente"""
    # Preparar datos de actualización
    update_dict = atencion_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.now()

    response = db.table("atencion_adultez").update(update_dict).eq("id", str(atencion_id)).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Atención adultez no encontrada")

    # Calcular campos automáticos para respuesta
    atencion_actualizada = calcular_campos_automaticos(response.data[0])
    return AtencionAdultezResponse(**atencion_actualizada)

@router.delete("/{atencion_id}")
async def eliminar_atencion_adultez(
    atencion_id: UUID,
    db=Depends(get_supabase_client)
):
    """Eliminar atención adultez"""
    # Primero obtener el atencion_id para eliminar también de atenciones
    atencion_response = db.table("atencion_adultez").select("atencion_id").eq("id", str(atencion_id)).execute()

    if not atencion_response.data:
        raise HTTPException(status_code=404, detail="Atención adultez no encontrada")

    atencion_general_id = atencion_response.data[0].get("atencion_id")

    # Eliminar de tabla específica
    delete_response = db.table("atencion_adultez").delete().eq("id", str(atencion_id)).execute()

    if not delete_response.data:
        raise HTTPException(status_code=404, detail="Error eliminando atención adultez")

    # Eliminar de tabla general si existe referencia
    if atencion_general_id:
        db.table("atenciones").delete().eq("id", atencion_general_id).execute()

    return {"message": "Atención adultez eliminada exitosamente"}

# =============================================================================
# ENDPOINTS ESPECIALIZADOS - ANÁLISIS Y REPORTES
# =============================================================================

@router.get("/estadisticas/", response_model=EstadisticasAdultezResponse)
async def obtener_estadisticas_adultez(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin para estadísticas"),
    db=Depends(get_supabase_client)
):
    """Obtener estadísticas de atenciones adultez"""
    query = db.table("atencion_adultez").select("*")

    if fecha_inicio:
        query = query.gte("fecha_atencion", fecha_inicio.isoformat())
    if fecha_fin:
        query = query.lte("fecha_atencion", fecha_fin.isoformat())

    response = query.execute()

    # Calcular estadísticas
    total_atenciones = len(response.data)

    # Distribución por estado nutricional
    distribuciones = {}
    for atencion in response.data:
        estado = atencion.get("estado_nutricional_calculado", "DESCONOCIDO")
        distribuciones[estado] = distribuciones.get(estado, 0) + 1

    return EstadisticasAdultezResponse(
        total_atenciones=total_atenciones,
        distribucion_estado_nutricional=distribuciones,
        periodo_inicio=fecha_inicio,
        periodo_fin=fecha_fin
    )

@router.get("/riesgo-cardiovascular/{nivel}", response_model=List[AtencionAdultezResponse])
async def obtener_por_riesgo_cardiovascular(
    nivel: RiesgoCardiovascularFramingham,
    db=Depends(get_supabase_client)
):
    """Obtener atenciones por nivel de riesgo cardiovascular"""
    response = db.table("atencion_adultez").select("*").eq("riesgo_cardiovascular_calculado", nivel.value).execute()

    atenciones_procesadas = []
    for atencion in response.data:
        atencion_procesada = calcular_campos_automaticos(atencion)
        atenciones_procesadas.append(AtencionAdultezResponse(**atencion_procesada))

    return atenciones_procesadas

@router.get("/paciente/{paciente_id}/cronologico", response_model=List[AtencionAdultezResponse])
async def obtener_atenciones_cronologicas_paciente(
    paciente_id: UUID,
    db=Depends(get_supabase_client)
):
    """Obtener todas las atenciones adultez de un paciente en orden cronológico"""
    response = db.table("atencion_adultez").select("*").eq("paciente_id", str(paciente_id)).order("fecha_atencion").execute()

    atenciones_procesadas = []
    for atencion in response.data:
        atencion_procesada = calcular_campos_automaticos(atencion)
        atenciones_procesadas.append(AtencionAdultezResponse(**atencion_procesada))

    return atenciones_procesadas