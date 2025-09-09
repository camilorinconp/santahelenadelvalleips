import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_to = None
atencion_id_general_to = None
tamizaje_oncologico_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_tamizaje_oncologico_test_data():
    """Setup: Crea un paciente y una atención general para las pruebas. Teardown: los elimina."""
    global paciente_id_test_to, atencion_id_general_to
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "TO_Test",
        "fecha_nacimiento": "1970-01-01",
        "genero": "F"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_to = response_paciente.json()["data"][0]["id"]

    # Crear Atención general de prueba
    datos_atencion_general = {
        "paciente_id": paciente_id_test_to,
        "medico_id": None, # No necesitamos un médico real para esta prueba
        "fecha_atencion": "2024-04-01",
        "entorno": "Institucional",
        "descripcion": "Atención general para prueba de tamizaje oncologico"
    }
    response_atencion_general = client.post("/atenciones/", json=datos_atencion_general)
    assert response_atencion_general.status_code == 201, response_atencion_general.text
    atencion_id_general_to = response_atencion_general.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba en el orden correcto
    if tamizaje_oncologico_id_test:
        db_client.table("tamizaje_oncologico").delete().eq("id", tamizaje_oncologico_id_test).execute()
    if atencion_id_general_to:
        db_client.table("atenciones").delete().eq("id", atencion_id_general_to).execute()
    if paciente_id_test_to:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_to).execute()

def test_01_create_tamizaje_oncologico():
    """Verifica la creación de un nuevo registro de tamizaje oncologico."""
    global tamizaje_oncologico_id_test
    assert atencion_id_general_to is not None

    datos_tamizaje = {
        "atencion_id": atencion_id_general_to,
        "tipo_tamizaje": "Cuello Uterino",
        "fecha_tamizaje": "2024-04-01",
        "resultado_tamizaje": "Negativo",
        "citologia_resultado": "Normal",
        "adn_vph_resultado": "Negativo"
    }

    response = client.post("/tamizajes-oncologicos/", json=datos_tamizaje)
    
    assert response.status_code == 201, response.text
    data = response.json()
    tamizaje_oncologico_id_test = data["id"]
    
    assert data["atencion_id"] == atencion_id_general_to
    assert data["tipo_tamizaje"] == "Cuello Uterino"
    assert data["resultado_tamizaje"] == "Negativo"

def test_02_get_tamizaje_oncologico_by_id():
    """Verifica la obtención de un registro de tamizaje oncologico por su ID."""
    assert tamizaje_oncologico_id_test is not None

    response = client.get(f"/tamizajes-oncologicos/{tamizaje_oncologico_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == tamizaje_oncologico_id_test
    assert data["atencion_id"] == atencion_id_general_to

def test_03_get_all_tamizajes_oncologicos():
    """Verifica la obtención de todos los registros de tamizaje oncologico."""
    response = client.get("/tamizajes-oncologicos/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == tamizaje_oncologico_id_test for d in data)
