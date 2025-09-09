from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import ControlCronicidad, ControlHipertensionDetalles
from database import get_supabase_client
from typing import List
from uuid import UUID
from datetime import datetime

router = APIRouter(
    prefix="/control-cronicidad",
    tags=["Control de Cronicidad"],
)

# --- Endpoints para ControlCronicidad (Tabla Padre) ---

# Crear un nuevo registro de control de cronicidad
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ControlCronicidad)
def create_control_cronicidad(control: ControlCronicidad, db: Client = Depends(get_supabase_client)):
    control_dict = control.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in control_dict or control_dict["creado_en"] is None:
        control_dict["creado_en"] = datetime.now().isoformat()
    
    try:
        response = db.table("control_cronicidad").insert(control_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el registro de control de cronicidad")
    
    return response.data[0]

# Obtener todos los registros de control de cronicidad
@router.get("/", response_model=List[ControlCronicidad])
def get_all_control_cronicidad(db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").execute()
    return response.data

# Obtener un registro de control de cronicidad por ID
@router.get("/{control_id}", response_model=ControlCronicidad)
def get_control_cronicidad_by_id(control_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de control de cronicidad no encontrado")
    return response.data

# --- Endpoints para ControlHipertensionDetalles (Tabla Hijo) ---

# Crear un nuevo registro de detalles de hipertensión
@router.post("/hipertension-detalles/", status_code=status.HTTP_201_CREATED, response_model=ControlHipertensionDetalles)
def create_hipertension_detalles(detalles: ControlHipertensionDetalles, db: Client = Depends(get_supabase_client)):
    detalles_dict = detalles.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in detalles_dict or detalles_dict["creado_en"] is None:
        detalles_dict["creado_en"] = datetime.now().isoformat()
    
    try:
        response = db.table("control_hipertension_detalles").insert(detalles_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear los detalles de hipertensión")
    
    return response.data[0]

# Obtener todos los registros de detalles de hipertensión
@router.get("/hipertension-detalles/", response_model=List[ControlHipertensionDetalles])
def get_all_hipertension_detalles(db: Client = Depends(get_supabase_client)):
    response = db.table("control_hipertension_detalles").select("*").execute()
    return response.data

# Obtener un registro de detalles de hipertensión por ID
@router.get("/hipertension-detalles/{detalles_id}", response_model=ControlHipertensionDetalles)
def get_hipertension_detalles_by_id(detalles_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_hipertension_detalles").select("*").eq("id", str(detalles_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalles de hipertensión no encontrados")
    return response.data

# Obtener detalles de hipertensión por control_cronicidad_id
@router.get("/hipertension-detalles/control/{control_cronicidad_id}", response_model=List[ControlHipertensionDetalles])
def get_hipertension_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_hipertension_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de hipertensión para este control de cronicidad")
    return response.data
