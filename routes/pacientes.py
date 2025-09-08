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
    # Forzar la serialización a JSON para manejar tipos de datos complejos como 'date'
    paciente_dict = paciente.model_dump(mode='json', exclude_unset=True)
    response = db.table("pacientes").insert(paciente_dict).execute()
    return {"data": response.data}

# Actualizar un paciente
@router.put("/{paciente_id}")
def update_paciente(paciente_id: str, paciente: Paciente, db: Client = Depends(get_supabase_client)):
    # Forzar la serialización a JSON para manejar tipos de datos complejos como 'date'
    paciente_dict = paciente.model_dump(mode='json', exclude_unset=True)
    response = db.table("pacientes").update(paciente_dict).eq("id", paciente_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado para actualizar")
    return {"data": response.data}

# Eliminar un paciente
@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paciente(paciente_id: str, db: Client = Depends(get_supabase_client)):
    response = db.table("pacientes").delete().eq("id", paciente_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado para eliminar")
    return
