from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import TamizajeOncologico
from database import get_supabase_client
from typing import List
from uuid import UUID
from datetime import datetime # Added this import

router = APIRouter(
    prefix="/tamizajes-oncologicos",
    tags=["Tamizajes Oncologicos"],
)

# Crear un nuevo registro de tamizaje oncologico
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TamizajeOncologico)
def create_tamizaje_oncologico(tamizaje: TamizajeOncologico, db: Client = Depends(get_supabase_client)):
    tamizaje_dict = tamizaje.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in tamizaje_dict or tamizaje_dict["creado_en"] is None:
        tamizaje_dict["creado_en"] = datetime.now().isoformat() # Asegura que creado_en siempre tenga un valor
    
    try:
        response = db.table("tamizaje_oncologico").insert(tamizaje_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el registro de tamizaje oncologico")
    
    return response.data[0]

# Obtener todos los registros de tamizaje oncologico
@router.get("/", response_model=List[TamizajeOncologico])
def get_all_tamizajes_oncologicos(db: Client = Depends(get_supabase_client)):
    response = db.table("tamizaje_oncologico").select("*").execute()
    return response.data

# Obtener un registro de tamizaje oncologico por ID
@router.get("/{tamizaje_id}", response_model=TamizajeOncologico)
def get_tamizaje_oncologico_by_id(tamizaje_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("tamizaje_oncologico").select("*").eq("id", str(tamizaje_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de tamizaje oncologico no encontrado")
    return response.data