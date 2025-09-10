from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion, TamizajeOncologico
from database import get_supabase_client
from typing import List
from uuid import UUID, uuid4
from datetime import datetime

router = APIRouter(
    prefix="/tamizajes-oncologicos",
    tags=["Tamizajes Oncologicos"],
)

# Crear un nuevo registro de tamizaje oncologico (con lógica polimórfica)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TamizajeOncologico)
def create_tamizaje_oncologico(atencion_detalle: TamizajeOncologico, db: Client = Depends(get_supabase_client)):
    # Paso 1: Crear la entrada genérica en la tabla de atenciones
    atencion_generica_dict = {
        "paciente_id": str(atencion_detalle.paciente_id),
        "medico_id": str(atencion_detalle.medico_id) if atencion_detalle.medico_id else None,
        "fecha_atencion": atencion_detalle.fecha_tamizaje.isoformat(),
        "entorno": "Institucional", # Asumido para tamizaje
        "tipo_atencion": f"Tamizaje Oncologico - {atencion_detalle.tipo_tamizaje}",
        "detalle_id": str(uuid4()) # Placeholder, se actualizará después
    }
    try:
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica de vínculo")
        created_atencion_id = atencion_response.data[0]['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica: {e}")

    # Paso 2: Insertar el detalle del tamizaje con el ID de la atención recién creada
    atencion_detalle.atencion_id = created_atencion_id
    detalle_dict = atencion_detalle.model_dump(mode='json', exclude_unset=True)
    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)

    try:
        detalle_response = db.table("tamizaje_oncologico").insert(detalle_dict).execute()
        if not detalle_response.data:
            db.table("atenciones").delete().eq("id", created_atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el registro de tamizaje")
        created_detalle = detalle_response.data[0]
    except Exception as e:
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear el detalle del tamizaje: {e}")

    # Paso 3: Actualizar la atención genérica con el ID del detalle real
    db.table("atenciones").update({"detalle_id": created_detalle['id']}).eq("id", created_atencion_id).execute()

    return created_detalle

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
