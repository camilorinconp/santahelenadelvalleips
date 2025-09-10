import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_to = None
tamizaje_oncologico_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_tamizaje_oncologico_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_to
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

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    if tamizaje_oncologico_id_test:
        atencion_generica = db_client.table("atenciones").select("id").eq("detalle_id", tamizaje_oncologico_id_test).execute()
        if atencion_generica.data:
            db_client.table("atenciones").delete().eq("id", atencion_generica.data[0]["id"]).execute()
        db_client.table("tamizaje_oncologico").delete().eq("id", tamizaje_oncologico_id_test).execute()
    if paciente_id_test_to:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_to).execute()

def test_01_create_tamizaje_oncologico():
    """Verifica la creación de un nuevo registro de tamizaje oncologico y su vínculo polimórfico."""
    global tamizaje_oncologico_id_test
    assert paciente_id_test_to is not None

    datos_to = {
        "paciente_id": paciente_id_test_to,
        "medico_id": None,
        "fecha_tamizaje": date.today().isoformat(),
        "tipo_tamizaje": "Citología",
        "resultado": "Negativo para lesión intraepitelial o malignidad"
    }

    response = client.post("/tamizajes-oncologicos/", json=datos_to)
    assert response.status_code == 201, response.text
    data_detalle = response.json()
    tamizaje_oncologico_id_test = data_detalle["id"]

    assert data_detalle["paciente_id"] == paciente_id_test_to
    assert data_detalle["tipo_tamizaje"] == "Citología"

    # Verificar que la atención genérica fue creada
    response_general = client.get("/atenciones/")
    assert response_general.status_code == 200
    atenciones_generales = response_general.json()
    
    atencion_creada = next((atencion for atencion in atenciones_generales if atencion.get("detalle_id") == tamizaje_oncologico_id_test), None)
    
    assert atencion_creada is not None, "No se creó la atención genérica vinculada"
    assert atencion_creada["tipo_atencion"] == "Tamizaje Oncologico - Citología"
    assert atencion_creada["paciente_id"] == paciente_id_test_to

def test_02_get_tamizaje_oncologico_by_id():
    """Verifica la obtención de un registro de tamizaje oncologico por su ID."""
    assert tamizaje_oncologico_id_test is not None

    response = client.get(f"/tamizajes-oncologicos/{tamizaje_oncologico_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == tamizaje_oncologico_id_test

def test_03_get_all_tamizajes_oncologicos():
    """Verifica la obtención de todos los registros de tamizaje oncologico."""
    response = client.get("/tamizajes-oncologicos/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == tamizaje_oncologico_id_test for d in data)