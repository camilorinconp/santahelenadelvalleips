from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import AtencionPrimeraInfancia
from database import get_supabase_client
from typing import List
from uuid import UUID

router = APIRouter(
    prefix="/atenciones-primera-infancia",
    tags=["Atenciones Primera Infancia"],
)

# Crear una nueva atención de primera infancia
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionPrimeraInfancia)
def create_atencion_primera_infancia(atencion: AtencionPrimeraInfancia, db: Client = Depends(get_supabase_client)):
    atencion_dict = atencion.model_dump(mode='json', exclude_unset=True)
    
    try:
        response = db.table("atencion_primera_infancia").insert(atencion_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención de primera infancia")
    
    return response.data[0]

# Obtener todas las atenciones de primera infancia
@router.get("/", response_model=List[AtencionPrimeraInfancia])
def get_atenciones_primera_infancia(db: Client = Depends(get_supabase_client)):
    response = db.table("atencion_primera_infancia").select("*").execute()
    return response.data

# Obtener una atención de primera infancia por ID
@router.get("/{atencion_id}", response_model=AtencionPrimeraInfancia)
def get_atencion_primera_infancia_by_id(atencion_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("atencion_primera_infancia").select("*").eq("id", str(atencion_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atención de primera infancia no encontrada")
    return response.data