from fastapi import APIRouter, HTTPException, status, Depends
from supabase import Client
from models import Atencion, ControlCronicidad, ControlHipertensionDetalles, ControlDiabetesDetalles, ControlERCDetalles, ControlDislipidemiaDetalles, ControlCronicidadPolimorfica
from typing import Literal
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
def create_control_cronicidad(control: ControlCronicidadPolimorfica, db: Client = Depends(get_supabase_client)):
    # Paso 1: Insertar el detalle específico en su tabla correspondiente
    specific_detail_table = None
    specific_detail_model = None
    if control.tipo_cronicidad == "Hipertension":
        specific_detail_table = "control_hipertension_detalles"
        specific_detail_model = ControlHipertensionDetalles
    elif control.tipo_cronicidad == "Diabetes":
        specific_detail_table = "control_diabetes_detalles"
        specific_detail_model = ControlDiabetesDetalles
    elif control.tipo_cronicidad == "ERC":
        specific_detail_table = "control_erc_detalles"
        specific_detail_model = ControlERCDetalles
    elif control.tipo_cronicidad == "Dislipidemia":
        specific_detail_table = "control_dislipidemia_detalles"
        specific_detail_model = ControlDislipidemiaDetalles
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de cronicidad no soportado")

    # Asegurarse de que el ID del detalle específico sea generado si no viene
    if not control.detalles.id:
        control.detalles.id = uuid4()
    
    specific_detail_dict = control.detalles.model_dump(mode='json', exclude_unset=True)
    # Convertir UUIDs a string para la inserción en Supabase
    for key, value in specific_detail_dict.items():
        if isinstance(value, UUID):
            specific_detail_dict[key] = str(value)

    try:
        detail_response = db.table(specific_detail_table).insert(specific_detail_dict).execute()
        if not detail_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear el detalle de {control.tipo_cronicidad}")
        created_specific_detail_id = detail_response.data[0]['id']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al insertar el detalle específico: {e}")

    # Paso 2: Crear el registro general de ControlCronicidad
    # Excluir el campo 'detalles' ya que no va en la tabla principal de ControlCronicidad
    control_general_dict = control.model_dump(mode='json', exclude={'detalles'})
    control_general_dict['detalle_cronicidad_id'] = created_specific_detail_id
    
    # Asegurarse de que el ID del control general sea generado si no viene
    if not control_general_dict.get('id'):
        control_general_dict['id'] = str(uuid4())

    # Convertir UUIDs a string para la inserción en Supabase
    for key, value in control_general_dict.items():
        if isinstance(value, UUID):
            control_general_dict[key] = str(value)

    try:
        control_cronicidad_response = db.table("control_cronicidad").insert(control_general_dict).execute()
        if not control_cronicidad_response.data:
            # Rollback manual del detalle específico si falla la creación del control general
            db.table(specific_detail_table).delete().eq("id", created_specific_detail_id).execute()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el registro general de ControlCronicidad")
        created_control_cronicidad = control_cronicidad_response.data[0]
        created_control_cronicidad_id = created_control_cronicidad['id']
    except Exception as e:
        # Rollback manual del detalle específico si falla la creación del control general
        db.table(specific_detail_table).delete().eq("id", created_specific_detail_id).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al insertar el control de cronicidad general: {e}")

    # Paso 3: Crear la entrada genérica en la tabla de atenciones
    atencion_generica_dict = {
        "paciente_id": str(control.paciente_id),
        "medico_id": str(control.medico_id) if control.medico_id else None,
        "fecha_atencion": control.fecha_control.isoformat(),
        "entorno": "Institucional", # Asumido para cronicidad
        "tipo_atencion": f"Control Cronicidad - {control.tipo_cronicidad}",
        "detalle_id": created_control_cronicidad_id # Ahora apunta al ID del control general de cronicidad
    }
    try:
        atencion_response = db.table("atenciones").insert(atencion_generica_dict).execute()
        if not atencion_response.data:
            # Rollback manual del detalle específico y del control general
            db.table(specific_detail_table).delete().eq("id", created_specific_detail_id).execute()
            db.table("control_cronicidad").delete().eq("id", created_control_cronicidad_id).execute()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la atención genérica de vínculo")
    except Exception as e:
        # Rollback manual del detalle específico y del control general
        db.table(specific_detail_table).delete().eq("id", created_specific_detail_id).execute()
        db.table("control_cronicidad").delete().eq("id", created_control_cronicidad_id).execute()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear la atención genérica: {e}")

    # Retornar el control general creado (que ahora incluye el detalle_cronicidad_id)
    return ControlCronicidad(**created_control_cronicidad)

@router.get("/", response_model=List[ControlCronicidadPolimorfica])
def get_all_control_cronicidad(db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").execute()
    if not response.data:
        return []

    all_controls = []
    for control_data in response.data:
        tipo_cronicidad = control_data.get('tipo_cronicidad')
        detalle_cronicidad_id = control_data.get('detalle_cronicidad_id')

        if not tipo_cronicidad or not detalle_cronicidad_id:
            all_controls.append(ControlCronicidad(**control_data))
            continue

        specific_detail_table = None
        specific_detail_model = None
        if tipo_cronicidad == "Hipertension":
            specific_detail_table = "control_hipertension_detalles"
            specific_detail_model = ControlHipertensionDetalles
        elif tipo_cronicidad == "Diabetes":
            specific_detail_table = "control_diabetes_detalles"
            specific_detail_model = ControlDiabetesDetalles
        elif tipo_cronicidad == "ERC":
            specific_detail_table = "control_erc_detalles"
            specific_detail_model = ControlERCDetalles
        elif tipo_cronicidad == "Dislipidemia":
            specific_detail_table = "control_dislipidemia_detalles"
            specific_detail_model = ControlDislipidemiaDetalles
        else:
            all_controls.append(ControlCronicidad(**control_data))
            continue

        try:
            detail_response = db.table(specific_detail_table).select("*").eq("id", str(detalle_cronicidad_id)).single().execute()
            if detail_response.data:
                combined_data = {**control_data, "detalles": detail_response.data[0]}
                if tipo_cronicidad == "Hipertension":
                    all_controls.append(ControlCronicidadHipertension(**combined_data))
                elif tipo_cronicidad == "Diabetes":
                    all_controls.append(ControlCronicidadDiabetes(**combined_data))
                elif tipo_cronicidad == "ERC":
                    all_controls.append(ControlCronicidadERC(**combined_data))
                elif tipo_cronicidad == "Dislipidemia":
                    all_controls.append(ControlCronicidadDislipidemia(**combined_data))
                else:
                    all_controls.append(ControlCronicidad(**control_data))
            else:
                all_controls.append(ControlCronicidad(**control_data))
        except Exception as e:
            print(f"Error al obtener detalles específicos para {tipo_cronicidad}: {e}")
            all_controls.append(ControlCronicidad(**control_data))

    return all_controls

@router.get("/{control_id}", response_model=ControlCronicidadPolimorfica)
def get_control_cronicidad_by_id(control_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de control de cronicidad no encontrado")
    
    control_data = response.data[0]
    tipo_cronicidad = control_data.get('tipo_cronicidad')
    detalle_cronicidad_id = control_data.get('detalle_cronicidad_id')

    if not tipo_cronicidad or not detalle_cronicidad_id:
        # Si no hay tipo o detalle_id, retornar el modelo base o manejar como error
        return ControlCronicidad(**control_data)

    specific_detail_table = None
    specific_detail_model = None
    if tipo_cronicidad == "Hipertension":
        specific_detail_table = "control_hipertension_detalles"
        specific_detail_model = ControlHipertensionDetalles
    elif tipo_cronicidad == "Diabetes":
        specific_detail_table = "control_diabetes_detalles"
        specific_detail_model = ControlDiabetesDetalles
    elif tipo_cronicidad == "ERC":
        specific_detail_table = "control_erc_detalles"
        specific_detail_model = ControlERCDetalles
    elif tipo_cronicidad == "Dislipidemia":
        specific_detail_table = "control_dislipidemia_detalles"
        specific_detail_model = ControlDislipidemiaDetalles
    else:
        # Si el tipo no es reconocido, retornar el modelo base sin detalles específicos
        return ControlCronicidad(**control_data)

    try:
        detail_response = db.table(specific_detail_table).select("*").eq("id", str(detalle_cronicidad_id)).single().execute()
        if not detail_response.data:
            # Si el detalle no se encuentra, retornar el control general sin detalles específicos
            return ControlCronicidad(**control_data)
        
        # Combinar los datos del control general con los detalles específicos
        combined_data = {**control_data, "detalles": detail_response.data[0]}
        
        # Retornar la instancia del modelo polimórfico correcto
        if tipo_cronicidad == "Hipertension":
            return ControlCronicidadHipertension(**combined_data)
        elif tipo_cronicidad == "Diabetes":
            return ControlCronicidadDiabetes(**combined_data)
        elif tipo_cronicidad == "ERC":
            return ControlCronicidadERC(**combined_data)
        elif tipo_cronicidad == "Dislipidemia":
            return ControlCronicidadDislipidemia(**combined_data)
        else:
            return ControlCronicidad(**control_data) # Fallback

    except Exception as e:
        # En caso de error al buscar detalles, retornar el control general sin detalles específicos
        print(f"Error al obtener detalles específicos para {tipo_cronicidad}: {e}")
        return ControlCronicidad(**control_data)

# --- Endpoints para Detalles (Tablas Hijo) ---



@router.get("/hipertension-detalles/control/{control_cronicidad_id}", response_model=List[ControlHipertensionDetalles])
def get_hipertension_detalles_by_control_id(control_cronicidad_id: UUID, db: Client = Depends(get_supabase_client)):
    response = db.table("control_hipertension_detalles").select("*").eq("control_cronicidad_id", str(control_cronicidad_id)).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron detalles de hipertensión para este control")
    return response.data

