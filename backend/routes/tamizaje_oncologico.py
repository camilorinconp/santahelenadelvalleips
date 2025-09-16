# =============================================================================
# Rutas Tamizaje Oncológico - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# =============================================================================

from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.tamizaje_oncologico_model import (
    TamizajeOncologicoCrear,
    TamizajeOncologicoActualizar,
    TamizajeOncologicoResponse,
    TamizajeOncologico,
    calcular_nivel_riesgo,
    calcular_adherencia_tamizaje,
    calcular_proxima_cita_tamizaje,
    calcular_completitud_tamizaje
)
from database import get_supabase_client
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from core.monitoring import apm_collector, health_metrics, PerformanceTimer
import time

router = APIRouter(
    prefix="/tamizaje-oncologico",
    tags=["Tamizaje Oncológico"],
)

# =============================================================================
# CRUD BÁSICO CONSOLIDADO
# =============================================================================

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TamizajeOncologicoResponse)
def crear_tamizaje_oncologico(
    tamizaje_data: TamizajeOncologicoCrear,
    db: Client = Depends(get_supabase_client)
):
    """
    Crear nuevo tamizaje oncológico siguiendo patrón polimórfico.
    
    Funcionalidad consolidada que incluye:
    - Validaciones básicas de datos
    - Patrón polimórfico: detalle primero, luego atención general
    - Respuesta con campos calculados automáticos
    """
    try:
        # 📊 APM: Track database operation timing
        start_time = time.time()
        
        # Validar que el paciente existe
        paciente_response = db.table("pacientes").select("id").eq("id", str(tamizaje_data.paciente_id)).execute()
        if not paciente_response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El paciente especificado no existe"
            )
        
        # Preparar datos del tamizaje
        tamizaje_dict = tamizaje_data.model_dump(mode='json', exclude_unset=True)
        
        # Procesar campos especiales
        for key, value in tamizaje_dict.items():
            if isinstance(value, UUID):
                tamizaje_dict[key] = str(value)
            elif isinstance(value, date):
                tamizaje_dict[key] = value.isoformat()
            elif isinstance(value, datetime):
                tamizaje_dict[key] = value.isoformat()
        
        # Paso 1: Crear tamizaje oncológico (sin atencion_id por ahora)
        tamizaje_dict_sin_atencion = tamizaje_dict.copy()
        if 'atencion_id' in tamizaje_dict_sin_atencion:
            del tamizaje_dict_sin_atencion['atencion_id']
            
        response_tamizaje = db.table("tamizaje_oncologico").insert(tamizaje_dict_sin_atencion).execute()
        
        if not response_tamizaje.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear tamizaje oncológico"
            )
        
        tamizaje_creado = response_tamizaje.data[0]
        tamizaje_id = tamizaje_creado["id"]
        
        # Paso 2: Crear atención general que referencie al tamizaje
        atencion_data = {
            "paciente_id": str(tamizaje_data.paciente_id),
            "medico_id": str(tamizaje_data.medico_id) if tamizaje_data.medico_id else None,
            "tipo_atencion": f"Tamizaje Oncológico - {tamizaje_data.tipo_tamizaje}",
            "detalle_id": tamizaje_id,
            "fecha_atencion": tamizaje_data.fecha_tamizaje.isoformat(),
            "entorno": "IPS",
            "descripcion": f"Tamizaje de {tamizaje_data.tipo_tamizaje}"
        }
        
        response_atencion = db.table("atenciones").insert(atencion_data).execute()
        
        if not response_atencion.data:
            # Si falla la atención, eliminar el tamizaje creado
            db.table("tamizaje_oncologico").delete().eq("id", tamizaje_id).execute()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear atención general para tamizaje oncológico"
            )
        
        atencion_creada = response_atencion.data[0]
        atencion_id = atencion_creada["id"]
        
        # Paso 3: Actualizar tamizaje con atencion_id
        update_response = db.table("tamizaje_oncologico").update({"atencion_id": atencion_id}).eq("id", tamizaje_id).execute()
        
        if not update_response.data:
            # Si falla la actualización, limpiar ambas inserciones
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            db.table("tamizaje_oncologico").delete().eq("id", tamizaje_id).execute()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al vincular tamizaje con atención general"
            )
        
        tamizaje_final = update_response.data[0]
        
        db_time = time.time() - start_time
        apm_collector.track_database_operation(
            table="tamizaje_oncologico",
            operation="CREATE",
            response_time=db_time,
            record_count=1
        )
        
        # 🏥 Track healthcare business metric
        health_metrics.track_medical_attention(
            attention_type="tamizaje_oncologico",
            duration_minutes=45,  # Tiempo promedio de tamizaje
            ead3_applied=False,
            asq3_applied=False
        )
        
        # Agregar campos calculados
        tamizaje_final["nivel_riesgo"] = calcular_nivel_riesgo(tamizaje_final["tipo_tamizaje"], tamizaje_final)
        tamizaje_final["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
            tamizaje_final["tipo_tamizaje"], 
            datetime.fromisoformat(tamizaje_final["fecha_tamizaje"]).date()
        )
        tamizaje_final["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
            tamizaje_final["tipo_tamizaje"], 
            tamizaje_final["nivel_riesgo"]
        )
        tamizaje_final["completitud_tamizaje"] = calcular_completitud_tamizaje(
            tamizaje_final["tipo_tamizaje"], 
            tamizaje_final
        )
        
        return TamizajeOncologicoResponse(**tamizaje_final)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear tamizaje oncológico: {e}"
        )

@router.get("/{tamizaje_id}", response_model=TamizajeOncologicoResponse)
def obtener_tamizaje_oncologico(
    tamizaje_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """Obtener tamizaje oncológico por ID con campos calculados."""
    try:
        response = db.table("tamizaje_oncologico").select("*").eq("id", str(tamizaje_id)).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tamizaje oncológico no encontrado"
            )
        
        tamizaje_data = response.data[0]
        
        # Agregar campos calculados
        tamizaje_data["nivel_riesgo"] = calcular_nivel_riesgo(tamizaje_data["tipo_tamizaje"], tamizaje_data)
        tamizaje_data["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
            tamizaje_data["tipo_tamizaje"], 
            datetime.fromisoformat(tamizaje_data["fecha_tamizaje"]).date()
        )
        tamizaje_data["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
            tamizaje_data["tipo_tamizaje"], 
            tamizaje_data["nivel_riesgo"]
        )
        tamizaje_data["completitud_tamizaje"] = calcular_completitud_tamizaje(
            tamizaje_data["tipo_tamizaje"], 
            tamizaje_data
        )
        
        return TamizajeOncologicoResponse(**tamizaje_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tamizaje oncológico: {e}"
        )

@router.get("/", response_model=List[TamizajeOncologicoResponse])
def listar_tamizajes_oncologicos(
    limite: int = 50,
    offset: int = 0,
    paciente_id: Optional[UUID] = None,
    tipo_tamizaje: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    resultado_tamizaje: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar tamizajes oncológicos con filtros avanzados.
    """
    try:
        # Construir consulta
        query = db.table("tamizaje_oncologico").select("*")
        
        # Aplicar filtros
        if paciente_id:
            query = query.eq("paciente_id", str(paciente_id))
        if tipo_tamizaje:
            query = query.eq("tipo_tamizaje", tipo_tamizaje)
        if resultado_tamizaje:
            query = query.eq("resultado_tamizaje", resultado_tamizaje)
        if fecha_desde:
            query = query.gte("fecha_tamizaje", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_tamizaje", fecha_hasta.isoformat())
        
        # Aplicar paginación y ordenamiento
        response = query.order("fecha_tamizaje", desc=True).range(offset, offset + limite - 1).execute()
        
        # Procesar respuesta y agregar campos calculados
        tamizajes_procesados = []
        for tamizaje_data in response.data:
            tamizaje_data["nivel_riesgo"] = calcular_nivel_riesgo(tamizaje_data["tipo_tamizaje"], tamizaje_data)
            tamizaje_data["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                datetime.fromisoformat(tamizaje_data["fecha_tamizaje"]).date()
            )
            tamizaje_data["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data["nivel_riesgo"]
            )
            tamizaje_data["completitud_tamizaje"] = calcular_completitud_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data
            )
            
            tamizajes_procesados.append(TamizajeOncologicoResponse(**tamizaje_data))
        
        return tamizajes_procesados
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar tamizajes oncológicos: {e}"
        )

@router.put("/{tamizaje_id}", response_model=TamizajeOncologicoResponse)
def actualizar_tamizaje_oncologico(
    tamizaje_id: UUID,
    tamizaje_update: TamizajeOncologicoActualizar,
    db: Client = Depends(get_supabase_client)
):
    """Actualizar tamizaje oncológico."""
    try:
        # Verificar que existe
        existing = db.table("tamizaje_oncologico").select("*").eq("id", str(tamizaje_id)).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tamizaje oncológico no encontrado"
            )
        
        # Preparar datos de actualización
        update_dict = tamizaje_update.model_dump(mode='json', exclude_unset=True)
        
        # Procesar campos especiales
        for key, value in update_dict.items():
            if isinstance(value, UUID):
                update_dict[key] = str(value)
            elif isinstance(value, date):
                update_dict[key] = value.isoformat()
            elif isinstance(value, datetime):
                update_dict[key] = value.isoformat()
        
        # Actualizar timestamp
        update_dict['updated_at'] = datetime.now().isoformat()
        
        # Actualizar en base de datos
        response = db.table("tamizaje_oncologico").update(update_dict).eq("id", str(tamizaje_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar tamizaje oncológico"
            )
        
        updated_tamizaje = response.data[0]
        
        # Agregar campos calculados
        updated_tamizaje["nivel_riesgo"] = calcular_nivel_riesgo(updated_tamizaje["tipo_tamizaje"], updated_tamizaje)
        updated_tamizaje["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
            updated_tamizaje["tipo_tamizaje"], 
            datetime.fromisoformat(updated_tamizaje["fecha_tamizaje"]).date()
        )
        updated_tamizaje["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
            updated_tamizaje["tipo_tamizaje"], 
            updated_tamizaje["nivel_riesgo"]
        )
        updated_tamizaje["completitud_tamizaje"] = calcular_completitud_tamizaje(
            updated_tamizaje["tipo_tamizaje"], 
            updated_tamizaje
        )
        
        return TamizajeOncologicoResponse(**updated_tamizaje)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar tamizaje oncológico: {e}"
        )

@router.delete("/{tamizaje_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tamizaje_oncologico(
    tamizaje_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """Eliminar tamizaje oncológico y su atención general asociada."""
    try:
        # Verificar que existe y obtener atencion_id
        existing = db.table("tamizaje_oncologico").select("id, atencion_id").eq("id", str(tamizaje_id)).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tamizaje oncológico no encontrado"
            )
        
        atencion_id = existing.data[0].get("atencion_id")
        
        # Eliminar tamizaje oncológico (esto eliminará la atención asociada por CASCADE)
        response = db.table("tamizaje_oncologico").delete().eq("id", str(tamizaje_id)).execute()
        
        # Si existe atención asociada y no se eliminó automáticamente, eliminarla manualmente
        if atencion_id:
            try:
                db.table("atenciones").delete().eq("id", atencion_id).execute()
            except:
                # No importa si falla, podría haberse eliminado por CASCADE
                pass
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar tamizaje oncológico: {e}"
        )

# =============================================================================
# ENDPOINTS ESPECIALIZADOS POR TIPO DE TAMIZAJE
# =============================================================================

@router.get("/tipo/{tipo_tamizaje}", response_model=List[TamizajeOncologicoResponse])
def listar_por_tipo_tamizaje(
    tipo_tamizaje: str,
    limite: int = 50,
    offset: int = 0,
    db: Client = Depends(get_supabase_client)
):
    """Listar tamizajes por tipo específico."""
    tipos_validos = ["Cuello Uterino", "Mama", "Prostata", "Colon y Recto"]
    
    if tipo_tamizaje not in tipos_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de tamizaje no válido. Tipos válidos: {tipos_validos}"
        )
    
    try:
        response = db.table("tamizaje_oncologico")\
            .select("*")\
            .eq("tipo_tamizaje", tipo_tamizaje)\
            .order("fecha_tamizaje", desc=True)\
            .range(offset, offset + limite - 1)\
            .execute()
        
        tamizajes_procesados = []
        for tamizaje_data in response.data:
            tamizaje_data["nivel_riesgo"] = calcular_nivel_riesgo(tamizaje_data["tipo_tamizaje"], tamizaje_data)
            tamizaje_data["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                datetime.fromisoformat(tamizaje_data["fecha_tamizaje"]).date()
            )
            tamizaje_data["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data["nivel_riesgo"]
            )
            tamizaje_data["completitud_tamizaje"] = calcular_completitud_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data
            )
            
            tamizajes_procesados.append(TamizajeOncologicoResponse(**tamizaje_data))
        
        return tamizajes_procesados
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tamizajes por tipo: {e}"
        )

@router.get("/paciente/{paciente_id}/cronologicos", response_model=List[TamizajeOncologicoResponse])
def obtener_tamizajes_cronologicos_paciente(
    paciente_id: UUID,
    tipo_tamizaje: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """Obtener historial cronológico de tamizajes de un paciente."""
    try:
        query = db.table("tamizaje_oncologico")\
            .select("*")\
            .eq("paciente_id", str(paciente_id))
        
        if tipo_tamizaje:
            query = query.eq("tipo_tamizaje", tipo_tamizaje)
        
        response = query.order("fecha_tamizaje", desc=False).execute()  # Cronológico ascendente
        
        tamizajes_procesados = []
        for tamizaje_data in response.data:
            tamizaje_data["nivel_riesgo"] = calcular_nivel_riesgo(tamizaje_data["tipo_tamizaje"], tamizaje_data)
            tamizaje_data["adherencia_tamizaje"] = calcular_adherencia_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                datetime.fromisoformat(tamizaje_data["fecha_tamizaje"]).date()
            )
            tamizaje_data["proxima_cita_recomendada_dias"] = calcular_proxima_cita_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data["nivel_riesgo"]
            )
            tamizaje_data["completitud_tamizaje"] = calcular_completitud_tamizaje(
                tamizaje_data["tipo_tamizaje"], 
                tamizaje_data
            )
            
            tamizajes_procesados.append(TamizajeOncologicoResponse(**tamizaje_data))
        
        return tamizajes_procesados
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener historial cronológico: {e}"
        )

# =============================================================================
# ESTADÍSTICAS Y REPORTES
# =============================================================================

@router.get("/estadisticas/basicas", response_model=dict)
def obtener_estadisticas_basicas(db: Client = Depends(get_supabase_client)):
    """Obtener estadísticas básicas de Tamizaje Oncológico."""
    try:
        # Total de tamizajes
        total_response = db.table("tamizaje_oncologico").select("id", count="exact").execute()
        total = total_response.count or 0
        
        # Por tipo de tamizaje
        tipos = ["Cuello Uterino", "Mama", "Prostata", "Colon y Recto"]
        estadisticas_por_tipo = {}
        
        for tipo in tipos:
            tipo_response = db.table("tamizaje_oncologico")\
                .select("id", count="exact")\
                .eq("tipo_tamizaje", tipo)\
                .execute()
            estadisticas_por_tipo[tipo] = tipo_response.count or 0
        
        # Tamizajes por resultado
        positivos = db.table("tamizaje_oncologico")\
            .select("id", count="exact")\
            .in_("resultado_tamizaje", ["Positivo", "Anormal"])\
            .execute().count or 0
        
        negativos = db.table("tamizaje_oncologico")\
            .select("id", count="exact")\
            .eq("resultado_tamizaje", "Negativo")\
            .execute().count or 0
        
        # Tamizajes con seguimiento requerido
        seguimiento_especializado = db.table("tamizaje_oncologico")\
            .select("id", count="exact")\
            .eq("requiere_seguimiento_especializado", True)\
            .execute().count or 0
        
        return {
            "resumen_general": {
                "total_tamizajes": total,
                "porcentaje_positivos": round((positivos / total * 100) if total > 0 else 0, 2),
                "porcentaje_seguimiento_especializado": round((seguimiento_especializado / total * 100) if total > 0 else 0, 2)
            },
            "por_tipo_tamizaje": estadisticas_por_tipo,
            "resultados": {
                "positivos_anormales": positivos,
                "negativos": negativos,
                "pendientes": total - positivos - negativos
            },
            "seguimiento": {
                "requiere_especializado": seguimiento_especializado,
                "seguimiento_normal": total - seguimiento_especializado
            },
            "fecha_calculo": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {e}"
        )

@router.get("/reportes/adherencia", response_model=dict)
def reporte_adherencia_tamizaje(
    tipo_tamizaje: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Client = Depends(get_supabase_client)
):
    """Reporte de adherencia a tamizajes oncológicos."""
    try:
        query = db.table("tamizaje_oncologico").select("*")
        
        if tipo_tamizaje:
            query = query.eq("tipo_tamizaje", tipo_tamizaje)
        if fecha_desde:
            query = query.gte("fecha_tamizaje", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_tamizaje", fecha_hasta.isoformat())
        
        response = query.execute()
        tamizajes = response.data
        
        # Análisis de adherencia
        adherencia_stats = {
            "Buena": 0,
            "Regular": 0,
            "Mala": 0,
            "No evaluada": 0
        }
        
        for tamizaje in tamizajes:
            fecha_tamizaje = datetime.fromisoformat(tamizaje["fecha_tamizaje"]).date()
            adherencia = calcular_adherencia_tamizaje(tamizaje["tipo_tamizaje"], fecha_tamizaje)
            
            if adherencia in adherencia_stats:
                adherencia_stats[adherencia] += 1
            else:
                adherencia_stats["No evaluada"] += 1
        
        total_tamizajes = len(tamizajes)
        
        return {
            "parametros_reporte": {
                "tipo_tamizaje": tipo_tamizaje or "Todos",
                "fecha_desde": fecha_desde.isoformat() if fecha_desde else None,
                "fecha_hasta": fecha_hasta.isoformat() if fecha_hasta else None,
                "total_tamizajes_analizados": total_tamizajes
            },
            "adherencia_absolutos": adherencia_stats,
            "adherencia_porcentajes": {
                key: round((value / total_tamizajes * 100) if total_tamizajes > 0 else 0, 2)
                for key, value in adherencia_stats.items()
            },
            "fecha_generacion": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte de adherencia: {e}"
        )

# =============================================================================
# COMPATIBILIDAD CON IMPLEMENTACIÓN ANTERIOR
# =============================================================================

# Mantener endpoint anterior para compatibilidad
@router.post("/tamizajes-oncologicos/", status_code=status.HTTP_201_CREATED, response_model=TamizajeOncologico, include_in_schema=False)
def create_tamizaje_oncologico_legacy(atencion_detalle: TamizajeOncologico, db: Client = Depends(get_supabase_client)):
    """Endpoint legacy para compatibilidad con tests existentes."""
    # Convertir a nuevo formato
    tamizaje_data = TamizajeOncologicoCrear(
        paciente_id=atencion_detalle.paciente_id,
        medico_id=atencion_detalle.medico_id,
        tipo_tamizaje=atencion_detalle.tipo_tamizaje,
        fecha_tamizaje=atencion_detalle.fecha_tamizaje,
        resultado_tamizaje=getattr(atencion_detalle, 'resultado', None),
        observaciones=atencion_detalle.observaciones,
        citologia_resultado=atencion_detalle.citologia_resultado,
        adn_vph_resultado=atencion_detalle.adn_vph_resultado,
        colposcopia_realizada=atencion_detalle.colposcopia_realizada,
        biopsia_realizada_cuello=atencion_detalle.biopsia_realizada_cuello,
        mamografia_resultado=atencion_detalle.mamografia_resultado,
        examen_clinico_mama_observaciones=atencion_detalle.examen_clinico_mama_observaciones,
        biopsia_realizada_mama=atencion_detalle.biopsia_realizada_mama,
        psa_resultado=atencion_detalle.psa_resultado,
        tacto_rectal_resultado=atencion_detalle.tacto_rectal_resultado,
        biopsia_realizada_prostata=atencion_detalle.biopsia_realizada_prostata,
        sangre_oculta_heces_resultado=atencion_detalle.sangre_oculta_heces_resultado,
        colonoscopia_realizada=atencion_detalle.colonoscopia_realizada,
        biopsia_realizada_colon=atencion_detalle.biopsia_realizada_colon
    )
    
    # Usar la nueva implementación
    response = crear_tamizaje_oncologico(tamizaje_data, db)
    
    # Convertir respuesta al formato legacy
    return TamizajeOncologico(**response.model_dump())

@router.get("/tamizajes-oncologicos/", response_model=List[TamizajeOncologico], include_in_schema=False)
def get_all_tamizajes_oncologicos_legacy(db: Client = Depends(get_supabase_client)):
    """Endpoint legacy para compatibilidad con tests existentes."""
    response = db.table("tamizaje_oncologico").select("*").execute()
    return [TamizajeOncologico(**item) for item in response.data]

@router.get("/tamizajes-oncologicos/{tamizaje_id}", response_model=TamizajeOncologico, include_in_schema=False)
def get_tamizaje_oncologico_by_id_legacy(tamizaje_id: UUID, db: Client = Depends(get_supabase_client)):
    """Endpoint legacy para compatibilidad con tests existentes."""
    response = db.table("tamizaje_oncologico").select("*").eq("id", str(tamizaje_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de tamizaje oncologico no encontrado")
    return TamizajeOncologico(**response.data[0])