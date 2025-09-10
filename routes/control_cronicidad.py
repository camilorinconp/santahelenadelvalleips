from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import ControlCronicidad, ControlHipertensionDetalles, ControlDiabetesDetalles, ControlERCDetalles, ControlDislipidemiaDetalles
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

# --- Endpoints para ControlDiabetesDetalles (Tabla Hijo) ---

# Crear un nuevo registro de detalles de diabetes
@router.post("/diabetes-detalles/", status_code=status.HTTP_201_CREATED, response_model=ControlDiabetesDetalles)
def create_diabetes_detalles(detalles: ControlDiabetesDetalles, db: Client = Depends(get_supabase_client)):
    detalles_dict = detalles.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in detalles_dict or detalles_dict["creado_en"] is None:
        detalles_dict["creado_en"] = datetime.now().isoformat()
    
    try:
        response = db.table("control_diabetes_detalles").insert(detalles_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear los detalles de diabetes")
    
    return response.data[0]

# Obtener todos los registros de detalles de diabetes
@router.get("/diabetes-detalles/", response_model=List[ControlDiabetesDetalles])
def get_all_diabetes_detalles(db: Client = Depends(get_supabase_client)):
    response = db.table("control_diabetes_detalles").select("*").execute()
    return response.data

# Obtener un registro de detalles de diabetes por ID
@router.get("/diabetes-detalles/{detalles_id}", response_model=ControlDiabetesDetalles)
def get_diabetes_detalles_by_id(detalles_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_diabetes_detalles").select("*").eq("id", str(detalles_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalles de diabetes no encontrados")
    return response.data

# Obtener detalles de diabetes por control_cronicidad_id
@router.get("/diabetes-detalles/control/{control_cronicidad_id}", response_model=List[ControlDiabetesDetalles])
def get_diabetes_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_diabetes_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de diabetes para este control de cronicidad")
    return response.data

# --- Endpoints para ControlERCDetalles (Tabla Hijo) ---

# Crear un nuevo registro de detalles de ERC
@router.post("/erc-detalles/", status_code=status.HTTP_201_CREATED, response_model=ControlERCDetalles)
def create_erc_detalles(detalles: ControlERCDetalles, db: Client = Depends(get_supabase_client)):
    detalles_dict = detalles.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in detalles_dict or detalles_dict["creado_en"] is None:
        detalles_dict["creado_en"] = datetime.now().isoformat()
    
    try:
        response = db.table("control_erc_detalles").insert(detalles_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear los detalles de ERC")
    
    return response.data[0]

# Obtener todos los registros de detalles de ERC
@router.get("/erc-detalles/", response_model=List[ControlERCDetalles])
def get_all_erc_detalles(db: Client = Depends(get_supabase_client)):
    response = db.table("control_erc_detalles").select("*").execute()
    return response.data

# Obtener un registro de detalles de ERC por ID
@router.get("/erc-detalles/{detalles_id}", response_model=ControlERCDetalles)
def get_erc_detalles_by_id(detalles_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_erc_detalles").select("*").eq("id", str(detalles_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalles de ERC no encontrados")
    return response.data

# Obtener detalles de ERC por control_cronicidad_id
@router.get("/erc-detalles/control/{control_cronicidad_id}", response_model=List[ControlERCDetalles])
def get_erc_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_erc_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de ERC para este control de cronicidad")
    return response.data

# --- Endpoints para ControlDislipidemiaDetalles (Tabla Hijo) ---

# Crear un nuevo registro de detalles de dislipidemia
@router.post("/dislipidemia-detalles/", status_code=status.HTTP_201_CREATED, response_model=ControlDislipidemiaDetalles)
def create_dislipidemia_detalles(detalles: ControlDislipidemiaDetalles, db: Client = Depends(get_supabase_client)):
    detalles_dict = detalles.model_dump(mode='json', exclude_unset=True)
    if "creado_en" not in detalles_dict or detalles_dict["creado_en"] is None:
        detalles_dict["creado_en"] = datetime.now().isoformat()
    
    try:
        response = db.table("control_dislipidemia_detalles").insert(detalles_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear los detalles de dislipidemia")
    
    return response.data[0]

# Obtener todos los registros de detalles de dislipidemia
@router.get("/dislipidemia-detalles/", response_model=List[ControlDislipidemiaDetalles])
def get_all_dislipidemia_detalles(db: Client = Depends(get_supabase_client)):
    response = db.table("control_dislipidemia_detalles").select("*").execute()
    return response.data

# Obtener un registro de detalles de dislipidemia por ID
@router.get("/dislipidemia-detalles/{detalles_id}", response_model=ControlDislipidemiaDetalles)
def get_dislipidemia_detalles_by_id(detalles_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_dislipidemia_detalles").select("*").eq("id", str(detalles_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalles de dislipidemia no encontrados")
    return response.data

# Obtener detalles de dislipidemia por control_cronicidad_id
@router.get("/dislipidemia-detalles/control/{control_cronicidad_id}", response_model=List[ControlDislipidemiaDetalles])
def get_dislipidemia_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_dislipidemia_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de dislipidemia para este control de cronicidad")
    return response.data
