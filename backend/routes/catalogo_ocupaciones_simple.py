# ===================================================================
# ROUTES: Catálogo de Ocupaciones DANE (Versión Simplificada)
# ===================================================================
# Descripción: API endpoints simplificados para búsqueda ocupaciones
# Autor: Backend Team - IPS Santa Helena del Valle  
# Fecha: 14 septiembre 2025
# Propósito: Soporte básico para variables PEDT con Supabase Client
# ===================================================================

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import logging
from uuid import UUID

# Importaciones locales
from models.catalogo_ocupaciones_model import (
    OcupacionAutocompletadoResponse,
    OcupacionEstadisticasResponse
)
from database import get_supabase_client
from supabase import Client

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/ocupaciones",
    tags=["Catálogo Ocupaciones DANE"],
    responses={
        404: {"description": "Ocupación no encontrada"},
        422: {"description": "Error de validación"}
    }
)

# ===================================================================
# ENDPOINTS PRINCIPALES
# ===================================================================

@router.get("/buscar", response_model=List[OcupacionAutocompletadoResponse])
async def buscar_ocupaciones_autocompletado(
    q: str = Query(
        ..., 
        min_length=3, 
        description="Término de búsqueda (mínimo 3 caracteres)",
        examples=["enfer"]
    ),
    limit: int = Query(
        10, 
        ge=1, 
        le=50, 
        description="Límite de resultados"
    ),
    supabase: Client = Depends(get_supabase_client)
):
    """
    **Búsqueda inteligente de ocupaciones para autocompletado**
    
    Funcionalidades:
    - Búsqueda por nombre (coincidencia parcial)
    - Búsqueda por código DANE
    - Optimizado para autocompletado en tiempo real
    
    Ejemplos de búsqueda:
    - `enfer` → Encuentra "Enfermera Profesional", "Enfermera Auxiliar", etc.
    - `2221` → Encuentra ocupaciones con código que inicia con 2221
    - `medic` → Encuentra "Médicos Generales", "Médicos Especialistas", etc.
    """
    
    try:
        logger.info(f"Búsqueda ocupaciones: '{q}' (límite: {limit})")
        
        # Búsqueda usando Supabase client
        # Búsqueda por nombre (coincidencia parcial)
        query_nombre = supabase.table("catalogo_ocupaciones_dane") \
            .select("id, codigo_ocupacion_dane, nombre_ocupacion_normalizado, categoria_ocupacional_nivel_1") \
            .eq("activo", True) \
            .ilike("nombre_ocupacion_normalizado", f"%{q}%") \
            .order("nombre_ocupacion_normalizado") \
            .limit(limit)
        
        response_nombre = query_nombre.execute()
        ocupaciones = []
        
        # Convertir resultados
        if response_nombre.data:
            for row in response_nombre.data:
                # Calcular relevancia básica
                nombre_lower = row['nombre_ocupacion_normalizado'].lower()
                q_lower = q.lower()
                
                if nombre_lower.startswith(q_lower):
                    relevancia = 1.0
                elif q_lower in nombre_lower:
                    relevancia = 0.8
                else:
                    relevancia = 0.5
                
                ocupaciones.append(OcupacionAutocompletadoResponse(
                    id=row['id'],
                    codigo_ocupacion_dane=row['codigo_ocupacion_dane'],
                    nombre_ocupacion_normalizado=row['nombre_ocupacion_normalizado'],
                    categoria_ocupacional_nivel_1=row['categoria_ocupacional_nivel_1'],
                    relevancia=relevancia
                ))
        
        # Si no hay suficientes resultados, buscar por código
        if len(ocupaciones) < limit:
            query_codigo = supabase.table("catalogo_ocupaciones_dane") \
                .select("id, codigo_ocupacion_dane, nombre_ocupacion_normalizado, categoria_ocupacional_nivel_1") \
                .eq("activo", True) \
                .ilike("codigo_ocupacion_dane", f"{q}%") \
                .order("codigo_ocupacion_dane") \
                .limit(limit - len(ocupaciones))
            
            response_codigo = query_codigo.execute()
            
            if response_codigo.data:
                for row in response_codigo.data:
                    # Evitar duplicados
                    if not any(ocp.id == row['id'] for ocp in ocupaciones):
                        ocupaciones.append(OcupacionAutocompletadoResponse(
                            id=row['id'],
                            codigo_ocupacion_dane=row['codigo_ocupacion_dane'],
                            nombre_ocupacion_normalizado=row['nombre_ocupacion_normalizado'],
                            categoria_ocupacional_nivel_1=row['categoria_ocupacional_nivel_1'],
                            relevancia=0.9  # Alta relevancia para código exacto
                        ))
        
        # Ordenar por relevancia
        ocupaciones.sort(key=lambda x: x.relevancia, reverse=True)
        
        logger.info(f"Encontradas {len(ocupaciones)} ocupaciones para '{q}'")
        return ocupaciones
        
    except Exception as e:
        logger.error(f"Error en búsqueda ocupaciones: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno buscando ocupaciones: {str(e)}"
        )


@router.get("/estadisticas", response_model=OcupacionEstadisticasResponse)
async def obtener_estadisticas_catalogo(
    supabase: Client = Depends(get_supabase_client)
):
    """
    **Estadísticas generales del catálogo de ocupaciones**
    
    Información útil para dashboard y monitoreo:
    - Total de ocupaciones y activas
    - Número de categorías por nivel
    - Fecha de última actualización
    """
    
    try:
        # Obtener conteo total
        response_total = supabase.table("catalogo_ocupaciones_dane") \
            .select("*", count="exact") \
            .execute()
        
        total_ocupaciones = response_total.count or 0
        
        # Obtener conteo activas
        response_activas = supabase.table("catalogo_ocupaciones_dane") \
            .select("*", count="exact") \
            .eq("activo", True) \
            .execute()
        
        ocupaciones_activas = response_activas.count or 0
        
        # Obtener categorías únicas nivel 1
        response_cat1 = supabase.table("catalogo_ocupaciones_dane") \
            .select("categoria_ocupacional_nivel_1") \
            .not_.is_("categoria_ocupacional_nivel_1", "null") \
            .execute()
        
        categorias_nivel_1 = len(set(row['categoria_ocupacional_nivel_1'] 
                                   for row in response_cat1.data 
                                   if row['categoria_ocupacional_nivel_1'])) if response_cat1.data else 0
        
        # Obtener última actualización
        response_ultima = supabase.table("catalogo_ocupaciones_dane") \
            .select("actualizado_en") \
            .order("actualizado_en", desc=True) \
            .limit(1) \
            .execute()
        
        ultima_actualizacion = None
        if response_ultima.data:
            ultima_actualizacion = response_ultima.data[0]['actualizado_en']
        
        return OcupacionEstadisticasResponse(
            total_ocupaciones=total_ocupaciones,
            ocupaciones_activas=ocupaciones_activas,
            categorias_nivel_1=categorias_nivel_1,
            categorias_nivel_2=0,  # Simplificado por ahora
            ultima_actualizacion=ultima_actualizacion,
            version_catalogo="2025"
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno obteniendo estadísticas"
        )


@router.get("/validar-codigo/{codigo}")
async def validar_codigo_dane(
    codigo: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    **Validar si un código DANE existe en el catálogo**
    
    Retorna información básica si el código es válido.
    """
    
    try:
        response = supabase.table("catalogo_ocupaciones_dane") \
            .select("codigo_ocupacion_dane, nombre_ocupacion_normalizado, activo") \
            .eq("codigo_ocupacion_dane", codigo) \
            .execute()
        
        if not response.data:
            return {
                "valido": False,
                "codigo": codigo,
                "mensaje": "Código DANE no encontrado en el catálogo"
            }
        
        ocupacion = response.data[0]
        return {
            "valido": True,
            "codigo": ocupacion['codigo_ocupacion_dane'],
            "nombre": ocupacion['nombre_ocupacion_normalizado'],
            "activo": ocupacion['activo'],
            "mensaje": "Código DANE válido"
        }
        
    except Exception as e:
        logger.error(f"Error validando código {codigo}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno validando código"
        )


@router.get("/health")
async def health_check_ocupaciones(
    supabase: Client = Depends(get_supabase_client)
):
    """
    **Health check del servicio de ocupaciones**
    
    Verifica que el catálogo está operativo y responde correctamente.
    """
    
    try:
        # Test básico de conectividad
        response = supabase.table("catalogo_ocupaciones_dane") \
            .select("*", count="exact") \
            .limit(1) \
            .execute()
        
        total_ocupaciones = response.count or 0
        
        # Test de búsqueda básica
        test_search = supabase.table("catalogo_ocupaciones_dane") \
            .select("id") \
            .eq("activo", True) \
            .limit(1) \
            .execute()
        
        busqueda_operativa = len(test_search.data) > 0 if test_search.data else False
        
        return {
            "status": "healthy",
            "timestamp": "2025-09-14T12:00:00Z",
            "catalogo": {
                "total_ocupaciones": total_ocupaciones,
                "tabla_accesible": True
            },
            "funcionalidad": {
                "busqueda_basica": "operativa" if busqueda_operativa else "error",
                "supabase_client": "conectado"
            }
        }
        
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Servicio no disponible: {str(e)}"
        )


# ===================================================================
# METADATA DEL ROUTER
# ===================================================================

router_metadata = {
    "name": "Catálogo Ocupaciones DANE (Simplificado)",
    "description": """
    **API básica para el catálogo de ocupaciones DANE**
    
    Funcionalidades implementadas:
    - 🔍 Búsqueda básica con autocompletado
    - 📊 Estadísticas del catálogo  
    - ✅ Validación de códigos DANE
    - ⚡ Health check del servicio
    
    **Optimizado para:**
    - Autocompletado en formularios de pacientes
    - Validación de ocupaciones en tiempo real
    - Integración con variables PEDT
    """,
    "version": "1.0.0"
}