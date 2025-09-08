from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.paciente_model import Paciente
from database import get_supabase_client

# Crear el router
router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"],
)

# Obtener todos los pacientes
@router.get("/")
def get_pacientes(db: Client = Depends(get_supabase_client)):
    response = db.table("pacientes").select("*").execute()
    return {"data": response.data}

# Obtener un paciente por su ID
@router.get("/{paciente_id}")
def get_paciente(paciente_id: str, db: Client = Depends(get_supabase_client)):
    response = db.table("pacientes").select("*").eq("id", paciente_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    return {"data": response.data[0]}

# Crear un nuevo paciente
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_paciente(paciente: Paciente, db: Client = Depends(get_supabase_client)):
    response = db.table("pacientes").insert(paciente.model_dump(exclude_unset=True)).execute()
    return {"data": response.data}