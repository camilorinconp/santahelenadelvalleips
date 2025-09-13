# =============================================================================
# Rutas REST - Entornos de Salud Pública Transversales
# Resolución 3280 de 2018 - Arquitectura Transversal RIAS
# =============================================================================

from fastapi import APIRouter, HTTPException, Depends, Query, status
from supabase import Client
from typing import List, Optional
from uuid import UUID
import math
from datetime import datetime

from database import get_supabase_client
from models.entorno_model import (
    TipoEntornoSaludPublica,
    NivelComplejidadIntervencionEntorno,
    EstadoActivacionEntorno,
    ModeloEntornoSaludPublicaCrear,
    ModeloEntornoSaludPublicaActualizar,
    ModeloEntornoSaludPublicaRespuesta,
    ModeloListaEntornosSaludPublica,
    ModeloFiltrosEntornoSaludPublica,
    ModeloEstadisticasEntornoSaludPublica
)

# Crear router
router = APIRouter(
    prefix="/entornos-salud-publica",
    tags=["Entornos de Salud Pública Transversales"],
    responses={404: {"description": "Entorno no encontrado"}}
)

# =============================================================================
# ENDPOINTS CRUD - Entornos de Salud Pública
# =============================================================================

@router.post("/", response_model=ModeloEntornoSaludPublicaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_entorno_salud_publica(
    entorno: ModeloEntornoSaludPublicaCrear,
    db: Client = Depends(get_supabase_client)
):
    """
    Crear un nuevo entorno de salud pública según clasificación Resolución 3280.
    
    Permite registrar cualquiera de los 5 entornos normativos:
    - ENTORNO_FAMILIAR_HOGAR_DOMESTICO
    - ENTORNO_EDUCATIVO_FORMATIVO_INSTITUCIONAL
    - ENTORNO_COMUNITARIO_TERRITORIAL_SOCIAL
    - ENTORNO_LABORAL_OCUPACIONAL_PRODUCTIVO
    - ENTORNO_INSTITUCIONAL_SERVICIOS_SALUD
    """
    try:
        # Verificar que el código de identificación no exista
        codigo_existente = db.table("entornos_salud_publica").select("id").eq(
            "codigo_identificacion_entorno_unico", 
            entorno.codigo_identificacion_entorno_unico
        ).execute()
        
        if codigo_existente.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un entorno con código {entorno.codigo_identificacion_entorno_unico}"
            )

        # Convertir modelo Pydantic a diccionario
        entorno_dict = entorno.model_dump(mode='json', exclude_unset=True)
        
        # Convertir enums a string values
        if entorno.tipo_entorno:
            entorno_dict["tipo_entorno"] = entorno.tipo_entorno.value
        if entorno.nivel_complejidad_intervencion:
            entorno_dict["nivel_complejidad_intervencion"] = entorno.nivel_complejidad_intervencion.value
        if entorno.estado_activacion:
            entorno_dict["estado_activacion"] = entorno.estado_activacion.value
        
        # Convertir UUID a string si existe
        if entorno.creado_por:
            entorno_dict["creado_por"] = str(entorno.creado_por)

        # Insertar en base de datos
        response = db.table("entornos_salud_publica").insert(entorno_dict).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el entorno de salud pública"
            )

        entorno_creado = response.data[0]
        return ModeloEntornoSaludPublicaRespuesta(**entorno_creado)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear entorno: {str(e)}"
        )


@router.get("/{entorno_id}", response_model=ModeloEntornoSaludPublicaRespuesta)
def obtener_entorno_salud_publica(
    entorno_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    """
    Obtener un entorno de salud pública específico por su ID.
    """
    try:
        response = db.table("entornos_salud_publica").select("*").eq("id", str(entorno_id)).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entorno con ID {entorno_id} no encontrado"
            )
        
        entorno_data = response.data[0]
        return ModeloEntornoSaludPublicaRespuesta(**entorno_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entorno: {str(e)}"
        )


@router.get("/", response_model=List[ModeloEntornoSaludPublicaRespuesta])
def listar_entornos_salud_publica(
    tipo_entorno: Optional[TipoEntornoSaludPublica] = Query(None, description="Filtrar por tipo de entorno"),
    estado_activacion: Optional[EstadoActivacionEntorno] = Query(None, description="Filtrar por estado"),
    db: Client = Depends(get_supabase_client)
):
    """
    Listar entornos de salud pública con filtros básicos.
    
    Permite filtrar por:
    - Tipo de entorno (los 5 tipos normativos)
    - Estado de activación
    """
    try:
        # Construir query base
        query = db.table("entornos_salud_publica").select("*")
        
        # Aplicar filtros si se proporcionan
        if tipo_entorno:
            query = query.eq("tipo_entorno", tipo_entorno.value)
        
        if estado_activacion:
            query = query.eq("estado_activacion", estado_activacion.value)
        
        # Ordenar por fecha de creación descendente
        query = query.order("creado_en", desc=True)
        
        # Ejecutar query
        response = query.execute()
        
        # Convertir resultados a modelos
        entornos = [
            ModeloEntornoSaludPublicaRespuesta(**entorno_data) 
            for entorno_data in response.data
        ]
        
        return entornos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar entornos: {str(e)}"
        )


# Endpoints adicionales pueden ser agregados en el futuro:
# - PUT para actualizar entornos
# - DELETE para eliminar entornos  
# - GET /estadisticas para análisis y reportes
# - GET /busqueda/avanzada para filtros complejos