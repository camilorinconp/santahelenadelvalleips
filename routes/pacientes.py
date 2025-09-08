from fastapi import APIRouter, HTTPException, status
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from models.paciente_model import Paciente

# Cargar las variables de entorno
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Inicializar el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Crear el router
router = APIRouter()

# Obtener todos los pacientes
# Obtener todos los pacientes
@router.get("/pacientes", tags=["Pacientes"])
def get_pacientes():
    response = supabase.table("pacientes").select("*").execute()
    return {"data": response.data}

# Obtener un paciente por su ID
@router.get("/pacientes/{paciente_id}", tags=["Pacientes"])
def get_paciente(paciente_id: str):
    response = supabase.table("pacientes").select("*").eq("id", paciente_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    return {"data": response.data[0]}

# Crear un nuevo paciente
@router.post("/pacientes", tags=["Pacientes"], status_code=status.HTTP_201_CREATED)
def create_paciente(paciente: Paciente):
    response = supabase.table("pacientes").insert(paciente.model_dump(exclude_unset=True)).execute()
    return {"data": response.data}