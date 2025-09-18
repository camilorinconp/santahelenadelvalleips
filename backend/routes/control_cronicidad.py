# =============================================================================
# Rutas Control Cronicidad - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 15 septiembre 2025
# =============================================================================

from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.control_cronicidad_model import (
    ControlCronicidadCrear,
    ControlCronicidadActualizar,
    ControlCronicidadResponse,
    ControlCronicidad,
    calcular_imc,
    evaluar_control_adecuado
)
from models.control_hipertension_model import ControlHipertensionDetalles
from models.control_diabetes_model import ControlDiabetesDetalles
from models.control_erc_model import ControlERCDetalles
from models.control_dislipidemia_model import ControlDislipidemiaDetalles
from database import get_supabase_client
from services.control_cronicidad_service import ControlCronicidadService
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from core.monitoring import apm_collector, health_metrics, PerformanceTimer
import time

router = APIRouter(
    prefix="/control-cronicidad",
    tags=["Control de Cronicidad"],
)

# =============================================================================
# CRUD BÁSICO CONSOLIDADO
# =============================================================================

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ControlCronicidadResponse)
async def crear_control_cronicidad(
    control_data: ControlCronicidadCrear,
    db: Client = Depends(get_supabase_client)
):
    """
    Crear nuevo control de cronicidad - SPRINT #2 COMPLETO:
    ✅ RPC Transaccional: Operaciones atómicas (replica patrón Sprint Piloto #1)
    ✅ Capa de Servicio: Lógica centralizada (ControlCronicidadService)
    ✅ Validaciones: Business logic separada de infrastructure
    ✅ Recomendaciones: Generación automática basada en tipo de cronicidad
    """
    try:
        # 📊 APM: Track database operation timing
        start_time = time.time()

        # Delegar toda la lógica compleja al servicio centralizado
        control_result = await ControlCronicidadService.crear_control_cronicidad_completo(control_data)

        db_time = time.time() - start_time
        apm_collector.track_database_operation(
            table="control_cronicidad",
            operation="CREATE",
            response_time=db_time,
            record_count=1
        )

        # 🏥 Track healthcare business metric
        health_metrics.track_medical_attention(
            attention_type="control_cronicidad",
            duration_minutes=30,  # Tiempo promedio de consulta
            ead3_applied=False,
            asq3_applied=False
        )

        return control_result

    except ValueError as e:
        # Errores de validación de negocio
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/{control_id}", response_model=ControlCronicidadResponse)
def obtener_control_cronicidad(
    control_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """Obtener control de cronicidad por ID con campos calculados."""
    try:
        response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control de cronicidad no encontrado"
            )
        
        control_data = response.data[0]
        
        # Agregar campos calculados
        control_data["control_adecuado"] = _evaluar_control_adecuado_basico(control_data)
        control_data["riesgo_cardiovascular"] = _calcular_riesgo_cardiovascular(control_data)
        control_data["adherencia_score"] = _calcular_adherencia_score(control_data)
        control_data["proxima_cita_recomendada_dias"] = _calcular_proxima_cita_cronicidad(control_data)
        
        return ControlCronicidadResponse(**control_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener control de cronicidad: {e}"
        )

@router.get("/", response_model=List[ControlCronicidadResponse])
def listar_controles_cronicidad(
    limite: int = 50,
    offset: int = 0,
    paciente_id: Optional[UUID] = None,
    tipo_cronicidad: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    estado_control: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar controles de cronicidad con filtros avanzados.
    """
    try:
        # Construir consulta
        query = db.table("control_cronicidad").select("*")
        
        # Aplicar filtros
        if paciente_id:
            query = query.eq("paciente_id", str(paciente_id))
        if tipo_cronicidad:
            query = query.eq("tipo_cronicidad", tipo_cronicidad)
        if estado_control:
            query = query.eq("estado_control", estado_control)
        if fecha_desde:
            query = query.gte("fecha_control", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_control", fecha_hasta.isoformat())
        
        # Aplicar paginación y ordenamiento
        response = query.order("fecha_control", desc=True).range(offset, offset + limite - 1).execute()
        
        # Procesar respuesta y agregar campos calculados
        controles_procesados = []
        for control_data in response.data:
            control_data["control_adecuado"] = _evaluar_control_adecuado_basico(control_data)
            control_data["riesgo_cardiovascular"] = _calcular_riesgo_cardiovascular(control_data)
            control_data["adherencia_score"] = _calcular_adherencia_score(control_data)
            control_data["proxima_cita_recomendada_dias"] = _calcular_proxima_cita_cronicidad(control_data)
            
            controles_procesados.append(ControlCronicidadResponse(**control_data))
        
        return controles_procesados
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar controles de cronicidad: {e}"
        )

@router.put("/{control_id}", response_model=ControlCronicidadResponse)
def actualizar_control_cronicidad(
    control_id: UUID,
    control_update: ControlCronicidadActualizar,
    db: Client = Depends(get_supabase_client)
):
    """Actualizar control de cronicidad."""
    try:
        # Verificar que existe
        existing = db.table("control_cronicidad").select("*").eq("id", str(control_id)).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control de cronicidad no encontrado"
            )
        
        # Preparar datos de actualización
        update_dict = control_update.model_dump(mode='json', exclude_unset=True)
        
        # Recalcular IMC si se actualizó peso o talla
        existing_data = existing.data[0]
        nuevo_peso = update_dict.get('peso_kg') or existing_data.get('peso_kg')
        nueva_talla = update_dict.get('talla_cm') or existing_data.get('talla_cm')
        
        if nuevo_peso and nueva_talla:
            update_dict['imc'] = calcular_imc(nuevo_peso, nueva_talla)
        
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
        response = db.table("control_cronicidad").update(update_dict).eq("id", str(control_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar control de cronicidad"
            )
        
        updated_control = response.data[0]
        
        # Agregar campos calculados
        updated_control["control_adecuado"] = _evaluar_control_adecuado_basico(updated_control)
        updated_control["riesgo_cardiovascular"] = _calcular_riesgo_cardiovascular(updated_control)
        updated_control["adherencia_score"] = _calcular_adherencia_score(updated_control)
        updated_control["proxima_cita_recomendada_dias"] = _calcular_proxima_cita_cronicidad(updated_control)
        
        return ControlCronicidadResponse(**updated_control)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar control de cronicidad: {e}"
        )

@router.delete("/{control_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_control_cronicidad(
    control_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """Eliminar control de cronicidad y su atención general asociada."""
    try:
        # Verificar que existe y obtener atencion_id
        existing = db.table("control_cronicidad").select("id, atencion_id").eq("id", str(control_id)).execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control de cronicidad no encontrado"
            )
        
        atencion_id = existing.data[0].get("atencion_id")
        
        # Eliminar control de cronicidad (esto eliminará la atención asociada por CASCADE)
        response = db.table("control_cronicidad").delete().eq("id", str(control_id)).execute()
        
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
            detail=f"Error al eliminar control de cronicidad: {e}"
        )

# =============================================================================
# ENDPOINTS ESPECIALIZADOS POR TIPO DE CRONICIDAD
# =============================================================================

@router.get("/tipo/{tipo_cronicidad}", response_model=List[ControlCronicidadResponse])
def listar_por_tipo_cronicidad(
    tipo_cronicidad: str,
    limite: int = 50,
    offset: int = 0,
    db: Client = Depends(get_supabase_client)
):
    """Listar controles por tipo específico de cronicidad."""
    tipos_validos = ["Hipertension", "Diabetes", "ERC", "Dislipidemia"]
    
    if tipo_cronicidad not in tipos_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de cronicidad no válido. Tipos válidos: {tipos_validos}"
        )
    
    try:
        response = db.table("control_cronicidad")\
            .select("*")\
            .eq("tipo_cronicidad", tipo_cronicidad)\
            .order("fecha_control", desc=True)\
            .range(offset, offset + limite - 1)\
            .execute()
        
        controles_procesados = []
        for control_data in response.data:
            control_data["control_adecuado"] = _evaluar_control_adecuado_basico(control_data)
            control_data["riesgo_cardiovascular"] = _calcular_riesgo_cardiovascular(control_data)
            control_data["adherencia_score"] = _calcular_adherencia_score(control_data)
            control_data["proxima_cita_recomendada_dias"] = _calcular_proxima_cita_cronicidad(control_data)
            
            controles_procesados.append(ControlCronicidadResponse(**control_data))
        
        return controles_procesados
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener controles por tipo: {e}"
        )

@router.get("/paciente/{paciente_id}/cronologicos", response_model=List[ControlCronicidadResponse])
def obtener_controles_cronologicos_paciente(
    paciente_id: UUID,
    tipo_cronicidad: Optional[str] = None,
    db: Client = Depends(get_supabase_client)
):
    """Obtener historial cronológico de controles de un paciente."""
    try:
        query = db.table("control_cronicidad")\
            .select("*")\
            .eq("paciente_id", str(paciente_id))
        
        if tipo_cronicidad:
            query = query.eq("tipo_cronicidad", tipo_cronicidad)
        
        response = query.order("fecha_control", desc=False).execute()  # Cronológico ascendente
        
        controles_procesados = []
        for control_data in response.data:
            control_data["control_adecuado"] = _evaluar_control_adecuado_basico(control_data)
            control_data["riesgo_cardiovascular"] = _calcular_riesgo_cardiovascular(control_data)
            control_data["adherencia_score"] = _calcular_adherencia_score(control_data)
            control_data["proxima_cita_recomendada_dias"] = _calcular_proxima_cita_cronicidad(control_data)
            
            controles_procesados.append(ControlCronicidadResponse(**control_data))
        
        return controles_procesados
        
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
    """Obtener estadísticas básicas de Control de Cronicidad."""
    try:
        # Total de controles
        total_response = db.table("control_cronicidad").select("id", count="exact").execute()
        total = total_response.count or 0
        
        # Por tipo de cronicidad
        tipos = ["Hipertension", "Diabetes", "ERC", "Dislipidemia"]
        estadisticas_por_tipo = {}
        
        for tipo in tipos:
            tipo_response = db.table("control_cronicidad")\
                .select("id", count="exact")\
                .eq("tipo_cronicidad", tipo)\
                .execute()
            estadisticas_por_tipo[tipo] = tipo_response.count or 0
        
        # Controles controlados vs no controlados
        controlados = db.table("control_cronicidad")\
            .select("id", count="exact")\
            .eq("estado_control", "Controlado")\
            .execute().count or 0
        
        no_controlados = db.table("control_cronicidad")\
            .select("id", count="exact")\
            .eq("estado_control", "No controlado")\
            .execute().count or 0
        
        # Adherencia al tratamiento
        buena_adherencia = db.table("control_cronicidad")\
            .select("id", count="exact")\
            .eq("adherencia_tratamiento", "Buena")\
            .execute().count or 0
        
        return {
            "resumen_general": {
                "total_controles": total,
                "porcentaje_controlados": round((controlados / total * 100) if total > 0 else 0, 2),
                "porcentaje_buena_adherencia": round((buena_adherencia / total * 100) if total > 0 else 0, 2)
            },
            "por_tipo_cronicidad": estadisticas_por_tipo,
            "control_metabolico": {
                "controlados": controlados,
                "no_controlados": no_controlados,
                "en_proceso": total - controlados - no_controlados
            },
            "fecha_calculo": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {e}"
        )

@router.get("/reportes/adherencia", response_model=dict)
def reporte_adherencia_tratamiento(
    tipo_cronicidad: Optional[str] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Client = Depends(get_supabase_client)
):
    """Reporte de adherencia al tratamiento."""
    try:
        query = db.table("control_cronicidad").select("*")
        
        if tipo_cronicidad:
            query = query.eq("tipo_cronicidad", tipo_cronicidad)
        if fecha_desde:
            query = query.gte("fecha_control", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_control", fecha_hasta.isoformat())
        
        response = query.execute()
        controles = response.data
        
        # Análisis de adherencia
        adherencia_stats = {
            "Buena": 0,
            "Regular": 0,
            "Mala": 0,
            "No especificada": 0
        }
        
        for control in controles:
            adherencia = control.get("adherencia_tratamiento", "No especificada")
            if adherencia in adherencia_stats:
                adherencia_stats[adherencia] += 1
            else:
                adherencia_stats["No especificada"] += 1
        
        total_controles = len(controles)
        
        return {
            "parametros_reporte": {
                "tipo_cronicidad": tipo_cronicidad or "Todos",
                "fecha_desde": fecha_desde.isoformat() if fecha_desde else None,
                "fecha_hasta": fecha_hasta.isoformat() if fecha_hasta else None,
                "total_controles_analizados": total_controles
            },
            "adherencia_absolutos": adherencia_stats,
            "adherencia_porcentajes": {
                key: round((value / total_controles * 100) if total_controles > 0 else 0, 2)
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
# FUNCIONES AUXILIARES PARA CAMPOS CALCULADOS
# =============================================================================

def _evaluar_control_adecuado_basico(control_data: dict) -> bool:
    """Evaluar si el control es adecuado (lógica básica)."""
    try:
        estado_control = control_data.get('estado_control', '')
        return estado_control == "Controlado"
    except Exception:
        return False

def _calcular_riesgo_cardiovascular(control_data: dict) -> str:
    """Calcular nivel de riesgo cardiovascular básico."""
    try:
        imc = control_data.get('imc', 0)
        edad_estimada = 50  # Simplificado
        
        factores_riesgo = 0
        
        if imc > 30:  # Obesidad
            factores_riesgo += 2
        elif imc > 25:  # Sobrepeso
            factores_riesgo += 1
            
        if control_data.get('estado_control') == "No controlado":
            factores_riesgo += 2
            
        if control_data.get('adherencia_tratamiento') == "Mala":
            factores_riesgo += 1
            
        if factores_riesgo <= 1:
            return "Bajo"
        elif factores_riesgo <= 3:
            return "Moderado"
        else:
            return "Alto"
            
    except Exception:
        return "No evaluado"

def _calcular_adherencia_score(control_data: dict) -> float:
    """Calcular score de adherencia 0-100."""
    try:
        adherencia = control_data.get('adherencia_tratamiento', '')
        
        if adherencia == "Buena":
            return 85.0
        elif adherencia == "Regular":
            return 60.0
        elif adherencia == "Mala":
            return 30.0
        else:
            return 50.0  # Valor neutro cuando no se especifica
            
    except Exception:
        return 50.0

def _calcular_proxima_cita_cronicidad(control_data: dict) -> int:
    """Calcular días recomendados para próxima cita."""
    try:
        tipo_cronicidad = control_data.get('tipo_cronicidad', '')
        estado_control = control_data.get('estado_control', '')
        
        # Lógica básica según tipo y control
        if estado_control == "No controlado":
            return 30  # Seguimiento más frecuente
        elif estado_control == "En proceso":
            return 60  # Seguimiento intermedio
        elif tipo_cronicidad in ["Diabetes", "Hipertension"]:
            return 90  # Cada 3 meses para DM/HTA controlada
        else:
            return 120  # Cada 4 meses para otras cronicidades
            
    except Exception:
        return 90  # Default: 3 meses