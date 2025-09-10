import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_api = None
atencion_primera_infancia_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_primera_infancia_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_api
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "API_Test_PI",
        "fecha_nacimiento": "2020-01-01",
        "genero": "F"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_api = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    if atencion_primera_infancia_id_test:
        atencion_generica = db_client.table("atenciones").select("id").eq("detalle_id", atencion_primera_infancia_id_test).execute()
        if atencion_generica.data:
            db_client.table("atenciones").delete().eq("id", atencion_generica.data[0]["id"]).execute()
        db_client.table("atencion_primera_infancia").delete().eq("id", atencion_primera_infancia_id_test).execute()
    if paciente_id_test_api:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_api).execute()

def test_01_create_atencion_primera_infancia():
    """Verifica la creación de una atención de primera infancia y su vínculo polimórfico."""
    global atencion_primera_infancia_id_test
    assert paciente_id_test_api is not None

    datos_api = {
        "paciente_id": paciente_id_test_api,
        "medico_id": None,
        "fecha_atencion": date.today().isoformat(),
        "entorno": "Institucional",
        "peso_kg": 10.5,
        "talla_cm": 80.0,
        "estado_nutricional": "Adecuado",
        "esquema_vacunacion_completo": True
    }

    response = client.post("/atenciones-primera-infancia/", json=datos_api)
    assert response.status_code == 201, response.text
    data_detalle = response.json()
    atencion_primera_infancia_id_test = data_detalle["id"]

    assert data_detalle["paciente_id"] == paciente_id_test_api
    assert data_detalle["peso_kg"] == 10.5

    # Verificar que la atención genérica fue creada
    response_general = client.get("/atenciones/")
    assert response_general.status_code == 200
    atenciones_generales = response_general.json()
    
    atencion_creada = next((atencion for atencion in atenciones_generales if atencion.get("detalle_id") == atencion_primera_infancia_id_test), None)
    
    assert atencion_creada is not None, "No se creó la atención genérica vinculada"
    assert atencion_creada["tipo_atencion"] == "Atencion Primera Infancia"
    assert atencion_creada["paciente_id"] == paciente_id_test_api

def test_02_get_atencion_primera_infancia_by_id():
    """Verifica la obtención de una atención de primera infancia por su ID."""
    assert atencion_primera_infancia_id_test is not None

    response = client.get(f"/atenciones-primera-infancia/{atencion_primera_infancia_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == atencion_primera_infancia_id_test

def test_03_get_all_atenciones_primera_infancia():
    """Verifica la obtención de todas las atenciones de primera infancia."""
    response = client.get("/atenciones-primera-infancia/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == atencion_primera_infancia_id_test for d in data)