from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models.atencion_materno_perinatal_model import AtencionMaternoPerinatal, DetalleControlPrenatal
from database import get_supabase_client
from typing import List
from uuid import UUID, uuid4
from datetime import date, datetime

router = APIRouter(
    prefix="/atenciones-materno-perinatal",
    tags=["Atenciones Materno Perinatal"],
)

# Crear una nueva atención materno perinatal (con lógica polimórfica)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AtencionMaternoPerinatal)
def create_atencion_materno_perinatal(atencion_detalle: AtencionMaternoPerinatal, db: Client = Depends(get_supabase_client)):
    # Este endpoint crea la atención principal. La lógica para los sub-detalles se manejará en endpoints específicos.
    
    # Convertir el modelo Pydantic a un diccionario, asegurándose de que los UUID y fechas sean strings
    detalle_dict = atencion_detalle.model_dump(mode='json', exclude_unset=True)
    
    # Asegurarse de que los campos de ID (si se envían) y fechas se manejen correctamente
    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)
        elif isinstance(value, (date, datetime)):
            detalle_dict[key] = value.isoformat()

    try:
        # 1. Crear la entrada genérica en la tabla 'atenciones' PRIMERO
        atencion_generica_dict = {
            "paciente_id": str(atencion_detalle.paciente_id),
            "medico_id": str(atencion_detalle.medico_id) if atencion_detalle.medico_id else None,
            "fecha_atencion": atencion_detalle.fecha_atencion.isoformat(),
            "entorno": atencion_detalle.entorno,
            "tipo_atencion": "Atencion Materno Perinatal",
            "detalle_id": None  # Se actualizará después
        }
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica")
        
        created_atencion = atencion_response.data[0]
        atencion_id = created_atencion['id']
        
        # 2. Agregar atencion_id al detalle y crear la atención materno perinatal
        detalle_dict["atencion_id"] = atencion_id
        detalle_response = db.table("atencion_materno_perinatal").insert(detalle_dict).execute()
        if not detalle_response.data:
            # Rollback: borrar la atención genérica
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la atención materno perinatal")
        
        created_detalle = detalle_response.data[0]
        
        # 3. Actualizar la atención genérica con el detalle_id
        update_response = db.table("atenciones").update({"detalle_id": created_detalle['id']}).eq("id", atencion_id).execute()
        if not update_response.data:
            # Rollback: borrar ambos registros
            db.table("atencion_materno_perinatal").delete().eq("id", created_detalle['id']).execute()
            db.table("atenciones").delete().eq("id", atencion_id).execute()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar la atención genérica con el detalle")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la base de datos: {e}")

    return AtencionMaternoPerinatal(**created_detalle)


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

# --- Endpoints para Sub-Detalles (Polimorfismo Anidado) ---

@router.post("/{atencion_materno_perinatal_id}/control-prenatal", status_code=status.HTTP_201_CREATED, response_model=DetalleControlPrenatal)
def create_detalle_control_prenatal(
    atencion_materno_perinatal_id: UUID,
    detalle: DetalleControlPrenatal,
    db: Client = Depends(get_supabase_client)
):
    # 1. Insertar el detalle en su tabla específica
    detalle.atencion_materno_perinatal_id = atencion_materno_perinatal_id
    
    detalle_dict = detalle.model_dump(mode='json', exclude_unset=True, exclude={'id'})

    for key, value in detalle_dict.items():
        if isinstance(value, UUID):
            detalle_dict[key] = str(value)
        elif isinstance(value, (date, datetime)):
            detalle_dict[key] = value.isoformat()

    try:
        detalle_response = db.table("detalle_control_prenatal").insert(detalle_dict).execute()
        if not detalle_response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el detalle de control prenatal")
        created_detalle = detalle_response.data[0]
        created_detalle_id = created_detalle['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al insertar el detalle: {e}")

    # 2. Actualizar la tabla padre (atencion_materno_perinatal) para vincular el nuevo detalle
    try:
        update_data = {
            "sub_tipo_atencion": "CONTROL_PRENATAL",
            "sub_detalle_id": created_detalle_id
        }
        update_response = db.table("atencion_materno_perinatal").update(update_data).eq("id", str(atencion_materno_perinatal_id)).execute()

        if not update_response.data:
            # Rollback: si la actualización falla, borrar el detalle recién creado
            db.table("detalle_control_prenatal").delete().eq("id", created_detalle_id).execute()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atención materno perinatal no encontrada para actualizar")

    except Exception as e:
        # Rollback
        db.table("detalle_control_prenatal").delete().eq("id", created_detalle_id).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar la atención materno perinatal: {e}")

    return DetalleControlPrenatal(**created_detalle)

@router.get("/{atencion_materno_perinatal_id}/control-prenatal", response_model=DetalleControlPrenatal)
def get_detalle_control_prenatal_by_atencion_id(
    atencion_materno_perinatal_id: UUID,
    db: Client = Depends(get_supabase_client)
):
    response = db.table("detalle_control_prenatal").select("*").eq("atencion_materno_perinatal_id", str(atencion_materno_perinatal_id)).maybe_single().execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró un detalle de control prenatal para esta atención")

    return response.data
