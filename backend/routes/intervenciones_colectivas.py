from fastapi import APIRouter, HTTPException, status, Depends, Query
from supabase import Client
from models import IntervencionColectiva
from database import get_supabase_client
from typing import List, Optional
from uuid import UUID

router = APIRouter(
    prefix="/intervenciones-colectivas",
    tags=["Intervenciones Colectivas"],
)

# Crear una nueva intervención colectiva
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IntervencionColectiva)
def create_intervencion_colectiva(intervencion: IntervencionColectiva, db: Client = Depends(get_supabase_client)):
    intervencion_dict = intervencion.model_dump(mode='json', exclude_unset=True)
    
    try:
        response = db.table("intervenciones_colectivas").insert(intervencion_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la intervención colectiva")
    
    return response.data[0]

# Obtener todas las intervenciones colectivas
@router.get("/", response_model=List[IntervencionColectiva])
def get_intervenciones_colectivas(entorno: Optional[str] = None, db: Client = Depends(get_supabase_client)):
    query = db.table("intervenciones_colectivas").select("*")
    if entorno:
        query = query.eq("entorno", entorno)
    response = query.execute()
    return response.data
    return response.data

# Obtener una intervención colectiva por ID
@router.get("/{intervencion_id}", response_model=IntervencionColectiva)
def get_intervencion_colectiva_by_id(intervencion_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("intervenciones_colectivas").select("*").eq("id", str(intervencion_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intervención no encontrada")
    return response.data[0]

# Actualizar una intervención colectiva
@router.put("/{intervencion_id}", response_model=IntervencionColectiva)
def update_intervencion_colectiva(intervencion_id: UUID, intervencion: IntervencionColectiva, db: Client = Depends(get_supabase_client)):
    intervencion_dict = intervencion.model_dump(mode='json', exclude_unset=True)
    response = db.table("intervenciones_colectivas").update(intervencion_dict).eq("id", str(intervencion_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intervención no encontrada para actualizar")
    return response.data[0]

# Eliminar una intervención colectiva
@router.delete("/{intervencion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intervencion_colectiva(intervencion_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("intervenciones_colectivas").delete().eq("id", str(intervencion_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intervención no encontrada para eliminar")
    return
