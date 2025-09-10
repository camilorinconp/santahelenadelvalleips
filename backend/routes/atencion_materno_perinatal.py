from typing import List
from uuid import UUID, uuid4

router = APIRouter(
    prefix="/atenciones-materno-perinatal",
    tags=["Atenciones Materno Perinatal"],
)

# Crear una nueva atención materno perinatal (con lógica polimórfica)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionMaternoPerinatal)
def create_atencion_materno_perinatal(atencion_detalle: AtencionMaternoPerinatal, db: Client = Depends(get_supabase_client)):
    # Paso 1: Crear la entrada genérica en la tabla de atenciones
    # Extraer solo los campos relevantes para la tabla 'atenciones' del modelo de detalle
    atencion_generica_dict = {
        "paciente_id": str(atencion_detalle.paciente_id),
        "medico_id": str(atencion_detalle.medico_id) if atencion_detalle.medico_id else None,
        "fecha_atencion": atencion_detalle.fecha_atencion.isoformat(),
        "entorno": atencion_detalle.entorno,
        "tipo_atencion": "Atencion Materno Perinatal",
        "detalle_id": str(uuid4())  # Placeholder, se actualizará después de crear el detalle
    }
    try:
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica de vínculo")
        created_atencion_id = atencion_response.data[0]['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica: {e}")

    # Paso 2: Insertar el detalle en la tabla especializada, vinculándolo con el ID de la atención general
    atencion_detalle.atencion_id = created_atencion_id # Populate the atencion_id in the detail model
    detalle_dict = atencion_detalle.model_dump(mode='json', exclude_unset=True)
    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)
        elif isinstance(value, date):
            detalle_dict[key] = value.isoformat()
        elif isinstance(value, datetime):
            detalle_dict[key] = value.isoformat()

    try:
        detalle_response = db.table("atencion_materno_perinatal").insert(detalle_dict).execute()
        if not detalle_response.data:
            # Rollback manual: Si falla la inserción en el detalle, borrar la atención genérica recién creada
            db.table("atenciones").delete().eq("id", created_atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el detalle de la atención")
        created_detalle = detalle_response.data[0]
    except Exception as e:
        # Rollback manual: Si falla la inserción en el detalle, borrar la atención genérica recién creada
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear el detalle de la atención: {e}")

    # Paso 3: Actualizar la atención genérica con el ID del detalle real
    try:
        db.table("atenciones").update({"detalle_id": created_detalle['id']}).eq("id", created_atencion_id).execute()
    except Exception as e:
        # Rollback manual: Si falla la actualización del detalle_id, borrar ambos registros
        db.table("atenciones").delete().eq("id", created_atencion_id).execute()
        db.table("atencion_materno_perinatal").delete().eq("id", created_detalle['id']).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar el detalle_id en la atención genérica: {e}")

    return created_detalle

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
