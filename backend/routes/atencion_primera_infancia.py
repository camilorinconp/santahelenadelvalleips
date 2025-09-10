from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion, AtencionPrimeraInfancia
from database import get_supabase_client
from typing import List
from uuid import UUID

router = APIRouter(
    prefix="/atenciones-primera-infancia",
    tags=["Atenciones Primera Infancia"],
)

# Crear una nueva atención de primera infancia (con lógica polimórfica)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionPrimeraInfancia)
def create_atencion_primera_infancia(atencion_detalle: AtencionPrimeraInfancia, db: Client = Depends(get_supabase_client)):
    # Paso 1: Insertar los detalles en la tabla especializada
    detalle_dict = atencion_detalle.model_dump(mode='json', exclude_unset=True)
    # Convertir UUIDs a string para la inserción en Supabase si no son None
    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)

    try:
        detalle_response = db.table("atencion_primera_infancia").insert(detalle_dict).execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear el detalle de la atención: {e}")

    if not detalle_response.data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención de primera infancia")
    
    created_detalle = detalle_response.data[0]
    created_detalle_id = created_detalle['id']

    # Paso 2: Crear la entrada genérica en la tabla de atenciones
    atencion_generica_dict = {
        "paciente_id": atencion_detalle.paciente_id,
        "medico_id": atencion_detalle.medico_id,
        from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion, AtencionPrimeraInfancia
from database import get_supabase_client
from typing import List
from uuid import UUID, uuid4

router = APIRouter(
    prefix="/atenciones-primera-infancia",
    tags=["Atenciones Primera Infancia"],
)

# Crear una nueva atención de primera infancia (con lógica polimórfica)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionPrimeraInfancia)
def create_atencion_primera_infancia(atencion_detalle: AtencionPrimeraInfancia, db: Client = Depends(get_supabase_client)):
    # Paso 1: Crear la entrada genérica en la tabla de atenciones
    atencion_generica_dict = {
        "paciente_id": str(atencion_detalle.paciente_id),
        "medico_id": str(atencion_detalle.medico_id) if atencion_detalle.medico_id else None,
        "fecha_atencion": atencion_detalle.fecha_atencion.isoformat(),
        "entorno": atencion_detalle.entorno,
        "tipo_atencion": "Atencion Primera Infancia",
        "detalle_id": str(uuid4())  # Placeholder, se actualizará después
    }
    try:
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica de vínculo")
        created_atencion_id = atencion_response.data[0]['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica: {e}")

    # Paso 2: Insertar el detalle en la tabla especializada, vinculándolo con el ID de la atención general
    atencion_detalle.atencion_id = created_atencion_id
    detalle_dict = atencion_detalle.model_dump(mode='json', exclude_unset=True)
    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)
        elif isinstance(value, date):
            detalle_dict[key] = value.isoformat()
        elif isinstance(value, datetime):
            detalle_dict[key] = value.isoformat()

    try:
        detalle_response = db.table("atencion_primera_infancia").insert(detalle_dict).execute()
        if not detalle_response.data:
            # Rollback manual: Si falla la inserción en el detalle, borrar la atención genérica recién creada
            db.table("atenciones").delete().eq("id", created_atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención de primera infancia")
        created_detalle = detalle_response.data[0]
    except Exception as e:
        # Rollback manual: Si falla la inserción en el detalle, borrar la atención genérica recién creada
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear la atención genérica: {e}")

    # Paso 3: Actualizar la atención genérica con el ID del detalle real
    try:
        db.table("atenciones").update({"detalle_id": created_detalle['id']}).eq("id", created_atencion_id).execute()
    except Exception as e:
        # Rollback manual: Si falla la actualización del detalle_id, borrar ambos registros
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        db.table("atencion_primera_infancia").delete().eq("id", created_detalle['id']).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar el detalle_id en la atención genérica: {e}")

    return created_detalle
        "entorno": atencion_detalle.entorno,
        "tipo_atencion": "Atencion Primera Infancia",
        "detalle_id": created_detalle_id
    }
    # Convertir UUIDs a string para la inserción
    for key, value in atencion_generica_dict.items():
        if isinstance(value, UUID):
            atencion_generica_dict[key] = str(value)

    try:
        db.table("atenciones").insert(atencion_generica_dict).execute()
    except Exception as e:
        # Rollback manual: Si falla la inserción en atenciones, borrar el detalle recién creado
        db.table("atencion_primera_infancia").delete().eq("id", created_detalle_id).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica de vínculo: {e}")

    return created_detalle

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
