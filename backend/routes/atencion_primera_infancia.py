# =============================================================================
# Rutas Consolidadas Atención Primera Infancia - Arquitectura Vertical
# Versión básica unificada sin complejidades innecesarias
# Fecha: 15 septiembre 2025
# =============================================================================

from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.atencion_primera_infancia_model import (
    AtencionPrimeraInfancia,
    AtencionPrimeraInfanciaCrear,
    AtencionPrimeraInfanciaActualizar,
    AtencionPrimeraInfanciaResponse,
    calcular_ead3_puntaje_total,
    evaluar_desarrollo_apropiado_edad
)
from database import get_supabase_client
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from core.monitoring import apm_collector, health_metrics, PerformanceTimer
import time

router = APIRouter(
    prefix="/atenciones-primera-infancia",
    tags=["Atención Primera Infancia"],
)

# =============================================================================
# CRUD BÁSICO CONSOLIDADO
# =============================================================================

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionPrimeraInfanciaResponse)
def crear_atencion_primera_infancia(
    atencion_data: AtencionPrimeraInfanciaCrear, 
    db: Client = Depends(get_supabase_client)
):
    """
    Crear nueva atención Primera Infancia básica.
    
    Funcionalidad consolidada que incluye:
    - Validaciones básicas de datos
    - Inserción en tabla unificada
    - Respuesta con campos calculados
    """
    try:
        # Validar que el paciente existe
        paciente_response = db.table("pacientes").select("id").eq("id", str(atencion_data.paciente_id)).execute()
        if not paciente_response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El paciente especificado no existe"
            )
        
        # Convertir a diccionario para inserción, excluyendo campos calculados
        detalle_dict = atencion_data.model_dump(
            mode='json', 
            exclude_unset=True,
            exclude={
                'desarrollo_apropiado_edad',
                'porcentaje_esquema_vacunacion', 
                'proxima_consulta_recomendada_dias',
                'alertas_desarrollo_generadas',
                'alertas_nutricionales_generadas',
                'alertas_vacunacion_generadas'
            }
        )
        
        # Procesar campos especiales
        for key, value in detalle_dict.items():
            if isinstance(value, UUID):
                detalle_dict[key] = str(value)
            elif isinstance(value, date):
                detalle_dict[key] = value.isoformat()
            elif isinstance(value, datetime):
                detalle_dict[key] = value.isoformat()
        
        # Insertar en base de datos
        response = db.table("atencion_primera_infancia").insert(detalle_dict).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear atención Primera Infancia"
            )
        
        created_atencion = response.data[0]
        
        # Agregar campos calculados
        created_atencion["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(created_atencion)
        created_atencion["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(created_atencion)
        created_atencion["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(created_atencion)
        
        return AtencionPrimeraInfanciaResponse(**created_atencion)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear atención: {e}"
        )

@router.get("/{atencion_id}", response_model=AtencionPrimeraInfanciaResponse)
def obtener_atencion_primera_infancia(
    atencion_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """Obtener atención Primera Infancia por ID con campos calculados."""
    try:
        response = db.table("atencion_primera_infancia").select("*").eq("id", str(atencion_id)).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atención Primera Infancia no encontrada"
            )
        
        atencion_data = response.data[0]
        
        # Agregar campos calculados
        atencion_data["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(atencion_data)
        atencion_data["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(atencion_data)
        atencion_data["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(atencion_data)
        
        return AtencionPrimeraInfanciaResponse(**atencion_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener atención: {e}"
        )

@router.get("/", response_model=List[AtencionPrimeraInfanciaResponse])
def listar_atenciones_primera_infancia(
    limite: int = 50,
    offset: int = 0,
    paciente_id: Optional[UUID] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Client = Depends(get_supabase_client)
):
    """
    Listar atenciones Primera Infancia con filtros básicos.
    """
    try:
        # Construir consulta
        query = db.table("atencion_primera_infancia").select("*")
        
        # Aplicar filtros
        if paciente_id:
            query = query.eq("paciente_id", str(paciente_id))
        if fecha_desde:
            query = query.gte("fecha_atencion", fecha_desde.isoformat())
        if fecha_hasta:
            query = query.lte("fecha_atencion", fecha_hasta.isoformat())
        
        # Aplicar paginación y ordenamiento
        response = query.order("fecha_atencion", desc=True).range(offset, offset + limite - 1).execute()
        
        # Procesar respuesta y agregar campos calculados
        atenciones_procesadas = []
        for atencion_data in response.data:
            atencion_data["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(atencion_data)
            atencion_data["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(atencion_data)
            atencion_data["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(atencion_data)
            
            atenciones_procesadas.append(AtencionPrimeraInfanciaResponse(**atencion_data))
        
        return atenciones_procesadas
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar atenciones: {e}"
        )

@router.put("/{atencion_id}", response_model=AtencionPrimeraInfanciaResponse)
def actualizar_atencion_primera_infancia(
    atencion_id: UUID,
    atencion_update: AtencionPrimeraInfanciaActualizar,
    db: Client = Depends(get_supabase_client)
):
    """Actualizar atención Primera Infancia completa."""
    try:
        # Verificar que existe
        existing = db.table("atencion_primera_infancia").select("id").eq("id", str(atencion_id)).single().execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atención Primera Infancia no encontrada"
            )
        
        # Preparar datos de actualización
        update_dict = atencion_update.model_dump(mode='json', exclude_unset=True, exclude={'id'})
        
        # Procesar campos especiales
        for key, value in update_dict.items():
            if isinstance(value, UUID):
                update_dict[key] = str(value)
            elif isinstance(value, date):
                update_dict[key] = value.isoformat()
            elif isinstance(value, datetime):
                update_dict[key] = value.isoformat()
        
        # Calcular puntaje total EAD-3 si se actualizaron los componentes
        if any(field in update_dict for field in ['ead3_motricidad_gruesa_puntaje', 'ead3_motricidad_fina_puntaje', 
                                                  'ead3_audicion_lenguaje_puntaje', 'ead3_personal_social_puntaje']):
            # Obtener datos actuales para cálculo
            current_data = db.table("atencion_primera_infancia").select("*").eq("id", str(atencion_id)).single().execute().data
            
            puntaje_total = calcular_ead3_puntaje_total(
                update_dict.get('ead3_motricidad_gruesa_puntaje') or current_data.get('ead3_motricidad_gruesa_puntaje'),
                update_dict.get('ead3_motricidad_fina_puntaje') or current_data.get('ead3_motricidad_fina_puntaje'),
                update_dict.get('ead3_audicion_lenguaje_puntaje') or current_data.get('ead3_audicion_lenguaje_puntaje'),
                update_dict.get('ead3_personal_social_puntaje') or current_data.get('ead3_personal_social_puntaje')
            )
            if puntaje_total:
                update_dict['ead3_puntaje_total'] = puntaje_total
        
        # Actualizar timestamp
        update_dict['updated_at'] = datetime.now().isoformat()
        
        # Actualizar en base de datos
        response = db.table("atencion_primera_infancia").update(update_dict).eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar atención Primera Infancia"
            )
        
        updated_atencion = response.data[0]
        
        # Agregar campos calculados
        updated_atencion["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(updated_atencion)
        updated_atencion["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(updated_atencion)
        updated_atencion["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(updated_atencion)
        
        return AtencionPrimeraInfanciaResponse(**updated_atencion)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar atención: {e}"
        )

@router.delete("/{atencion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_atencion_primera_infancia(
    atencion_id: UUID, 
    db: Client = Depends(get_supabase_client)
):
    """Eliminar atención Primera Infancia."""
    try:
        # Verificar que existe
        existing = db.table("atencion_primera_infancia").select("id").eq("id", str(atencion_id)).single().execute()
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atención Primera Infancia no encontrada"
            )
        
        # Eliminar
        response = db.table("atencion_primera_infancia").delete().eq("id", str(atencion_id)).execute()
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar atención: {e}"
        )

# =============================================================================
# ENDPOINTS ESPECIALIZADOS BÁSICOS
# =============================================================================

@router.patch("/{atencion_id}/ead3", response_model=AtencionPrimeraInfanciaResponse)
def aplicar_ead3(
    atencion_id: UUID,
    datos_ead3: dict,
    db: Client = Depends(get_supabase_client)
):
    """
    Aplicar Escala Abreviada de Desarrollo (EAD-3) básica.
    
    Versión simplificada sin validaciones complejas.
    """
    try:
        # Validar campos básicos
        required_fields = [
            'ead3_motricidad_gruesa_puntaje',
            'ead3_motricidad_fina_puntaje', 
            'ead3_audicion_lenguaje_puntaje',
            'ead3_personal_social_puntaje'
        ]
        
        for field in required_fields:
            if field not in datos_ead3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Campo requerido faltante: {field}"
                )
            
            if not (0 <= datos_ead3[field] <= 100):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Puntaje {field} debe estar entre 0 y 100"
                )
        
        # Calcular puntaje total
        puntaje_total = calcular_ead3_puntaje_total(
            datos_ead3['ead3_motricidad_gruesa_puntaje'],
            datos_ead3['ead3_motricidad_fina_puntaje'],
            datos_ead3['ead3_audicion_lenguaje_puntaje'],
            datos_ead3['ead3_personal_social_puntaje']
        )
        
        # Preparar datos para actualización
        update_data = {
            **datos_ead3,
            'ead3_aplicada': True,
            'ead3_puntaje_total': puntaje_total,
            'fecha_aplicacion_ead3': date.today().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # 📊 APM: Track database operation + business metric
        start_time = time.time()
        response = db.table("atencion_primera_infancia").update(update_data).eq("id", str(atencion_id)).execute()
        db_time = time.time() - start_time
        
        # Track database performance
        apm_collector.track_database_operation(
            table="atencion_primera_infancia",
            operation="UPDATE_EAD3",
            response_time=db_time,
            record_count=len(response.data) if response.data else 0
        )
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atención no encontrada o error al aplicar EAD-3"
            )
        
        # 🏥 Track healthcare business metric - EAD3 application
        health_metrics.track_medical_attention(
            attention_type="primera_infancia",
            duration_minutes=0,  # Evaluation time
            ead3_applied=True,
            asq3_applied=False
        )
        
        updated_atencion = response.data[0]
        
        # Agregar campos calculados
        updated_atencion["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(updated_atencion)
        updated_atencion["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(updated_atencion)
        updated_atencion["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(updated_atencion)
        
        return AtencionPrimeraInfanciaResponse(**updated_atencion)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al aplicar EAD-3: {e}"
        )

@router.patch("/{atencion_id}/asq3", response_model=AtencionPrimeraInfanciaResponse)
def aplicar_asq3(
    atencion_id: UUID,
    datos_asq3: dict,
    db: Client = Depends(get_supabase_client)
):
    """
    Aplicar Ages and Stages Questionnaire (ASQ-3) básico.
    """
    try:
        # Preparar datos para actualización
        update_data = {
            **datos_asq3,
            'asq3_aplicado': True,
            'fecha_aplicacion_asq3': date.today().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Actualizar en base de datos
        response = db.table("atencion_primera_infancia").update(update_data).eq("id", str(atencion_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atención no encontrada o error al aplicar ASQ-3"
            )
        
        updated_atencion = response.data[0]
        
        # Agregar campos calculados
        updated_atencion["desarrollo_apropiado_edad"] = _calcular_desarrollo_apropiado(updated_atencion)
        updated_atencion["porcentaje_esquema_vacunacion"] = _calcular_porcentaje_vacunacion(updated_atencion)
        updated_atencion["proxima_consulta_recomendada_dias"] = _calcular_proxima_consulta(updated_atencion)
        
        return AtencionPrimeraInfanciaResponse(**updated_atencion)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al aplicar ASQ-3: {e}"
        )

# =============================================================================
# ESTADÍSTICAS BÁSICAS
# =============================================================================

@router.get("/estadisticas/basicas", response_model=dict)
def obtener_estadisticas_basicas(db: Client = Depends(get_supabase_client)):
    """
    Obtener estadísticas básicas de Primera Infancia.
    """
    try:
        # Total de atenciones
        total_response = db.table("atencion_primera_infancia").select("id", count="exact").execute()
        total = total_response.count or 0
        
        # Con EAD-3 aplicada
        ead3_response = db.table("atencion_primera_infancia").select("id", count="exact").eq("ead3_aplicada", True).execute()
        con_ead3 = ead3_response.count or 0
        
        # Con ASQ-3 aplicado
        asq3_response = db.table("atencion_primera_infancia").select("id", count="exact").eq("asq3_aplicado", True).execute()
        con_asq3 = asq3_response.count or 0
        
        # Esquema vacunación completo
        vacunacion_response = db.table("atencion_primera_infancia").select("id", count="exact").eq("esquema_vacunacion_completo", True).execute()
        vacunacion_completa = vacunacion_response.count or 0
        
        return {
            "resumen_general": {
                "total_atenciones": total,
                "porcentaje_ead3_aplicada": round((con_ead3 / total * 100) if total > 0 else 0, 2),
                "porcentaje_asq3_aplicado": round((con_asq3 / total * 100) if total > 0 else 0, 2),
                "porcentaje_vacunacion_completa": round((vacunacion_completa / total * 100) if total > 0 else 0, 2)
            },
            "fecha_calculo": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {e}"
        )

# =============================================================================
# FUNCIONES AUXILIARES PARA CAMPOS CALCULADOS
# =============================================================================

def _calcular_desarrollo_apropiado(atencion_data: dict) -> bool:
    """Calcular si el desarrollo es apropiado (lógica básica)."""
    try:
        # Si tiene EAD-3 completa, evaluar
        if atencion_data.get('ead3_aplicada') and atencion_data.get('ead3_puntaje_total'):
            return atencion_data['ead3_puntaje_total'] > 200  # Criterio básico
        
        # Sin información suficiente, asumir normal
        return True
        
    except Exception:
        return True

def _calcular_porcentaje_vacunacion(atencion_data: dict) -> float:
    """Calcular porcentaje básico de vacunación."""
    try:
        vacunas_esperadas = 4  # BCG, Hepatitis B, Pentavalente, SRP
        vacunas_aplicadas = 0
        
        if atencion_data.get('bcg_aplicada'):
            vacunas_aplicadas += 1
        if atencion_data.get('hepatitis_b_rn_aplicada'):
            vacunas_aplicadas += 1
        if atencion_data.get('pentavalente_dosis_completas', 0) >= 3:
            vacunas_aplicadas += 1
        if atencion_data.get('srp_aplicada'):
            vacunas_aplicadas += 1
        
        return round((vacunas_aplicadas / vacunas_esperadas * 100), 2)
        
    except Exception:
        return 0.0

def _calcular_proxima_consulta(atencion_data: dict) -> int:
    """Calcular días hasta próxima consulta (lógica básica)."""
    try:
        # Lógica simple: consultas cada 6 meses hasta los 2 años, después anuales
        return 180  # 6 meses por defecto
        
    except Exception:
        return 180