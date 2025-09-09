import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_amp = None
atencion_id_general_amp = None
atencion_materno_perinatal_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_materno_perinatal_test_data():
    """Setup: Crea un paciente y una atención general para las pruebas. Teardown: los elimina."""
    global paciente_id_test_amp, atencion_id_general_amp
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

    # Crear Atención general de prueba
    datos_atencion_general = {
        "paciente_id": paciente_id_test_amp,
        "medico_id": None, # No necesitamos un médico real para esta prueba
        "fecha_atencion": "2024-03-10",
        "entorno": "Institucional",
        "descripcion": "Atención general para prueba materno perinatal"
    }
    response_atencion_general = client.post("/atenciones/", json=datos_atencion_general)
    assert response_atencion_general.status_code == 201, response_atencion_general.text
    atencion_id_general_amp = response_atencion_general.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba en el orden correcto
    if atencion_materno_perinatal_id_test:
        db_client.table("atencion_materno_perinatal").delete().eq("id", atencion_materno_perinatal_id_test).execute()
    if atencion_id_general_amp:
        db_client.table("atenciones").delete().eq("id", atencion_id_general_amp).execute()
    if paciente_id_test_amp:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_amp).execute()

def test_01_create_atencion_materno_perinatal():
    """Verifica la creación de una nueva atención materno perinatal especializada."""
    global atencion_materno_perinatal_id_test
    assert atencion_id_general_amp is not None

    datos_amp = {
        "atencion_id": atencion_id_general_amp,
        "estado_gestacional_semanas": 20,
        "fecha_probable_parto": "2024-09-10",
        "numero_controles_prenatales": 3,
        "riesgo_biopsicosocial": "Bajo",
        "resultado_tamizaje_vih": "Negativo",
        "resultado_tamizaje_sifilis": "Negativo",
        "tipo_parto": "Vaginal",
        "fecha_parto": "2024-09-10",
        "peso_recien_nacido_kg": 3.2,
        "talla_recien_nacido_cm": 50.0,
        "apgar_recien_nacido": 9,
        "tamizaje_auditivo_neonatal": True,
        "tamizaje_metabolico_neonatal": True,
        "estado_puerperio_observaciones": "Sin complicaciones"
    }

    response = client.post("/atenciones-materno-perinatal/", json=datos_amp)
    
    assert response.status_code == 201, response.text
    data = response.json()
    atencion_materno_perinatal_id_test = data["id"]
    
    assert data["atencion_id"] == atencion_id_general_amp
    assert data["estado_gestacional_semanas"] == 20
    assert data["tipo_parto"] == "Vaginal"

def test_02_get_atencion_materno_perinatal_by_id():
    """Verifica la obtención de una atención materno perinatal por su ID."""
    assert atencion_materno_perinatal_id_test is not None

    response = client.get(f"/atenciones-materno-perinatal/{atencion_materno_perinatal_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == atencion_materno_perinatal_id_test
    assert data["atencion_id"] == atencion_id_general_amp

def test_03_get_all_atenciones_materno_perinatal():
    """Verifica la obtención de todas las atenciones materno perinatales."""
    response = client.get("/atenciones-materno-perinatal/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == atencion_materno_perinatal_id_test for d in data)
