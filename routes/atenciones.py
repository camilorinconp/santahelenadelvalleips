from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion
from database import get_supabase_client
from uuid import UUID

router = APIRouter(
    prefix="/atenciones",
    tags=["Atenciones"],
)

# Crear una nueva atención
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_atencion(atencion: Atencion, db: Client = Depends(get_supabase_client)):
    atencion_dict = atencion.model_dump(mode='json', exclude_unset=True)
    response = db.table("atenciones").insert(atencion_dict).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención")
    return {"data": response.data}

# Obtener todas las atenciones
@router.get("/")
def get_atenciones(db: Client = Depends(get_supabase_client)):
    response = db.table("atenciones").select("*").execute()
    return {"data": response.data}

# Obtener atenciones por ID de paciente
@router.get("/paciente/{paciente_id}")
def get_atenciones_by_paciente(paciente_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("atenciones").select("*").eq("paciente_id", str(paciente_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron atenciones para el paciente {paciente_id}")
    return {"data": response.data}

# Obtener una atención por su ID
@router.get("/{atencion_id}")
def get_atencion(atencion_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("atenciones").select("*").eq("id", str(atencion_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atención no encontrada")
    return {"data": response.data}
