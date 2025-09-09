from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import AtencionMaternoPerinatal
from database import get_supabase_client
from typing import List
from uuid import UUID

router = APIRouter(
    prefix="/atenciones-materno-perinatal",
    tags=["Atenciones Materno Perinatal"],
)

# Crear una nueva atención materno perinatal
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionMaternoPerinatal)
def create_atencion_materno_perinatal(atencion: AtencionMaternoPerinatal, db: Client = Depends(get_supabase_client)):
    atencion_dict = atencion.model_dump(mode='json', exclude_unset=True)
    
    try:
        response = db.table("atencion_materno_perinatal").insert(atencion_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención materno perinatal")
    
    return response.data[0]

# Obtener todas las atenciones materno perinatales
@router.get("/", response_model=List[AtencionMaternoPerinatal])
def get_atenciones_materno_perinatal(db: Client = Depends(get_supabase_client)):
    response = db.table("atencion_materno_perinatal").select("*").execute()
    return response.data

# Obtener una atención materno perinatal por ID
@router.get("/{atencion_id}", response_model=AtencionMaternoPerinatal)
def get_atencion_materno_perinatal_by_id(atencion_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("atencion_materno_perinatal").select("*").eq("id", str(atencion_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atención materno perinatal no encontrada")
    return response.data