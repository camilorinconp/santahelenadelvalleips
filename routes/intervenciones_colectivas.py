from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.intervencion_colectiva_model import IntervencionColectiva
from database import get_supabase_client
from typing import List

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
def get_intervenciones_colectivas(db: Client = Depends(get_supabase_client)):
    response = db.table("intervenciones_colectivas").select("*").execute()
    return response.data
