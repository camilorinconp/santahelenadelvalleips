from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion, ControlCronicidad, ControlHipertensionDetalles, ControlDiabetesDetalles, ControlERCDetalles, ControlDislipidemiaDetalles
from database import get_supabase_client
from typing import List
from uuid import UUID, uuid4
from datetime import datetime

router = APIRouter(
    prefix="/control-cronicidad",
    tags=["Control de Cronicidad"],
)

# --- Endpoints para ControlCronicidad (Tabla Padre) ---

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ControlCronicidad)
def create_control_cronicidad(control: ControlCronicidad, db: Client = Depends(get_supabase_client)):
    # La lógica correcta es crear primero la atención genérica y luego el detalle.
    # Este endpoint asume que la atención ya existe, lo cual es propenso a errores.
    # Se corrige la lógica para que sea más robusta, similar a otras rutas.

    # Paso 1: Crear la entrada genérica en la tabla de atenciones
    atencion_generica_dict = {
        "paciente_id": str(control.paciente_id),
        "medico_id": str(control.medico_id) if control.medico_id else None,
        "fecha_atencion": control.fecha_control.isoformat(),
        "entorno": "Institucional", # Asumido para cronicidad
        "tipo_atencion": f"Control Cronicidad - {control.tipo_cronicidad}",
        "detalle_id": str(uuid4())  # Placeholder, se actualizará después
    }
    try:
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica de vínculo")
        created_atencion = atencion_response.data[0]
        created_atencion_id = created_atencion['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica: {e}")

    # Paso 2: Insertar el registro de cronicidad con el ID de la atención recién creada
    control.atencion_id = created_atencion_id
    control_dict = control.model_dump(mode='json', exclude_unset=True)
    for key, value in control_dict.items():
        if isinstance(value, UUID):
            control_dict[key] = str(value)

    try:
        control_response = db.table("control_cronicidad").insert(control_dict).execute()
        if not control_response.data:
            # Rollback manual
            db.table("atenciones").delete().eq("id", created_atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el registro de control de cronicidad")
        created_control = control_response.data[0]
    except Exception as e:
        # Rollback manual
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear el control de cronicidad: {e}")

    # Paso 3: Actualizar la atención genérica con el ID del detalle real
    db.table("atenciones").update({"detalle_id": created_control['id']}).eq("id", created_atencion_id).execute()

    return created_control

@router.get("/", response_model=List[ControlCronicidad])
def get_all_control_cronicidad(db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").execute()
    return response.data

@router.get("/{control_id}", response_model=ControlCronicidad)
def get_control_cronicidad_by_id(control_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de control de cronicidad no encontrado")
    return response.data

# --- Endpoints para Detalles (Tablas Hijo) ---

@router.post("/hipertension-detalles/", status_code=status.HTTP_201_CREATED, response_model=ControlHipertensionDetalles)
def create_hipertension_detalles(detalles: ControlHipertensionDetalles, db: Client = Depends(get_supabase_client)):
    detalles_dict = detalles.model_dump(mode='json', exclude_unset=True)
    try:
        response = db.table("control_hipertension_detalles").insert(detalles_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear los detalles de hipertensión")
    return response.data[0]

@router.get("/hipertension-detalles/control/{control_cronicidad_id}", response_model=List[ControlHipertensionDetalles])
def get_hipertension_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_hipertension_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de hipertensión para este control")
    return response.data

# ... (endpoints para diabetes, erc y dislipidemia detalles se mantienen igual)