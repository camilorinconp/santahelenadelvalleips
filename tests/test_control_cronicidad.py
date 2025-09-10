import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_cc = None
control_cronicidad_id_test = None
control_hipertension_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_control_cronicidad_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_cc
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "CC_Test",
        "fecha_nacimiento": "1960-01-01",
        "genero": "M"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_cc = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    if control_hipertension_id_test:
        db_client.table("control_hipertension_detalles").delete().eq("id", control_hipertension_id_test).execute()
    if control_cronicidad_id_test:
        atencion_generica = db_client.table("atenciones").select("id").eq("detalle_id", control_cronicidad_id_test).execute()
        if atencion_generica.data:
            db_client.table("atenciones").delete().eq("id", atencion_generica.data[0]["id"]).execute()
        db_client.table("control_cronicidad").delete().eq("id", control_cronicidad_id_test).execute()
    if paciente_id_test_cc:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_cc).execute()

def test_01_create_control_cronicidad():
    """Verifica la creación de un control de cronicidad y su vínculo polimórfico."""
    global control_cronicidad_id_test
    assert paciente_id_test_cc is not None

    datos_control = {
        "paciente_id": paciente_id_test_cc,
        "medico_id": None,
        "fecha_control": date.today().isoformat(),
        "tipo_cronicidad": "Hipertensión",
        "estado_control": "Estable"
    }

    response = client.post("/control-cronicidad/", json=datos_control)
    assert response.status_code == 201, response.text
    data_detalle = response.json()
    control_cronicidad_id_test = data_detalle["id"]

    assert data_detalle["paciente_id"] == paciente_id_test_cc

    # Verificar que la atención genérica fue creada
    response_general = client.get("/atenciones/")
    assert response_general.status_code == 200
    atenciones_generales = response_general.json()
    
    atencion_creada = next((atencion for atencion in atenciones_generales if atencion.get("detalle_id") == control_cronicidad_id_test), None)
    
    assert atencion_creada is not None, "No se creó la atención genérica vinculada"
    assert atencion_creada["tipo_atencion"] == f"Control Cronicidad - {datos_control['tipo_cronicidad']}"
    assert atencion_creada["paciente_id"] == paciente_id_test_cc

def test_02_create_control_hipertension_detalles():
    """Verifica la creación de detalles para un control de cronicidad existente."""
    global control_hipertension_id_test
    assert control_cronicidad_id_test is not None

    datos_hipertension = {
        "control_cronicidad_id": control_cronicidad_id_test,
        "presion_arterial_sistolica": 125,
        "presion_arterial_diastolica": 85
    }

    response = client.post("/control-cronicidad/hipertension-detalles/", json=datos_hipertension)
    assert response.status_code == 201, response.text
    data = response.json()
    control_hipertension_id_test = data["id"]
    assert data["control_cronicidad_id"] == control_cronicidad_id_test
