import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_amp = None
atencion_materno_perinatal_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_materno_perinatal_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_amp
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "AMP_Test",
        "fecha_nacimiento": "1990-05-15",
        "genero": "F"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_amp = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    if atencion_materno_perinatal_id_test:
        atencion_generica = db_client.table("atenciones").select("id").eq("detalle_id", atencion_materno_perinatal_id_test).execute()
        if atencion_generica.data:
            db_client.table("atenciones").delete().eq("id", atencion_generica.data[0]["id"]).execute()
        db_client.table("atencion_materno_perinatal").delete().eq("id", atencion_materno_perinatal_id_test).execute()
    if paciente_id_test_amp:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_amp).execute()

def test_01_create_atencion_materno_perinatal():
    """Verifica la creación de una atención materno perinatal y su vínculo polimórfico."""
    global atencion_materno_perinatal_id_test
    assert paciente_id_test_amp is not None

    datos_amp = {
        "paciente_id": paciente_id_test_amp,
        "medico_id": None,
        "fecha_atencion": date.today().isoformat(),
        "entorno": "Institucional",
        "estado_gestacional_semanas": 20,
        "fecha_probable_parto": "2024-09-10",
        "numero_controles_prenatales": 3
    }

    response = client.post("/atenciones-materno-perinatal/", json=datos_amp)
    assert response.status_code == 201, response.text
    data_detalle = response.json()
    atencion_materno_perinatal_id_test = data_detalle["id"]

    assert data_detalle["paciente_id"] == paciente_id_test_amp
    assert data_detalle["estado_gestacional_semanas"] == 20

    # Verificar que la atención genérica fue creada
    response_general = client.get("/atenciones/")
    assert response_general.status_code == 200
    atenciones_generales = response_general.json()
    
    atencion_creada = next((atencion for atencion in atenciones_generales if atencion.get("detalle_id") == atencion_materno_perinatal_id_test), None)
    
    assert atencion_creada is not None, "No se creó la atención genérica vinculada"
    assert atencion_creada["tipo_atencion"] == "Atencion Materno Perinatal"
    assert atencion_creada["paciente_id"] == paciente_id_test_amp

def test_02_get_atencion_materno_perinatal_by_id():
    """Verifica la obtención de una atención materno perinatal por su ID."""
    assert atencion_materno_perinatal_id_test is not None

    response = client.get(f"/atenciones-materno-perinatal/{atencion_materno_perinatal_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == atencion_materno_perinatal_id_test

def test_03_get_all_atenciones_materno_perinatal():
    """Verifica la obtención de todas las atenciones materno perinatales."""
    response = client.get("/atenciones-materno-perinatal/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == atencion_materno_perinatal_id_test for d in data)
