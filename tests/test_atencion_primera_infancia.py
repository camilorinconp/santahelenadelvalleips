import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_api = None
atencion_id_general_test = None
atencion_primera_infancia_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_primera_infancia_test_data():
    """Setup: Crea un paciente y una atención general para las pruebas. Teardown: los elimina."""
    global paciente_id_test_api, atencion_id_general_test
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "API_Test",
        "fecha_nacimiento": "2020-01-01",
        "genero": "M"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_api = response_paciente.json()["data"][0]["id"]

    # Crear Atención general de prueba
    datos_atencion_general = {
        "paciente_id": paciente_id_test_api,
        "medico_id": None, # No necesitamos un médico real para esta prueba
        "fecha_atencion": "2024-01-01",
        "entorno": "Institucional",
        "descripcion": "Atención general para prueba de primera infancia"
    }
    response_atencion_general = client.post("/atenciones/", json=datos_atencion_general)
    assert response_atencion_general.status_code == 201, response_atencion_general.text
    atencion_id_general_test = response_atencion_general.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba en el orden correcto
    if atencion_primera_infancia_id_test:
        db_client.table("atencion_primera_infancia").delete().eq("id", atencion_primera_infancia_id_test).execute()
    if atencion_id_general_test:
        db_client.table("atenciones").delete().eq("id", atencion_id_general_test).execute()
    if paciente_id_test_api:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_api).execute()

def test_01_create_atencion_primera_infancia():
    """Verifica la creación de una atención de primera infancia especializada."""
    global atencion_primera_infancia_id_test
    assert atencion_id_general_test is not None

    datos_api = {
        "atencion_id": atencion_id_general_test,
        "peso_kg": 10.5,
        "talla_cm": 80.0,
        "estado_nutricional": "Adecuado",
        "esquema_vacunacion_completo": True
    }

    response = client.post("/atenciones-primera-infancia/", json=datos_api)
    assert response.status_code == 201, response.text
    data = response.json()
    atencion_primera_infancia_id_test = data["id"]

    assert data["atencion_id"] == atencion_id_general_test
    assert data["peso_kg"] == 10.5
    assert data["estado_nutricional"] == "Adecuado"

def test_02_get_atencion_primera_infancia_by_id():
    """Verifica la obtención de una atención de primera infancia por su ID."""
    assert atencion_primera_infancia_id_test is not None

    response = client.get(f"/atenciones-primera-infancia/{atencion_primera_infancia_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == atencion_primera_infancia_id_test
    assert data["atencion_id"] == atencion_id_general_test

def test_03_get_all_atenciones_primera_infancia():
    """Verifica la obtención de todas las atenciones de primera infancia."""
    response = client.get("/atenciones-primera-infancia/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == atencion_primera_infancia_id_test for d in data)
