import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date, datetime
from database import get_supabase_client

# --- Variables globales para IDs creados ---
paciente_id_test_cc = None
atencion_id_general_cc = None
control_cronicidad_id_test = None
control_hipertension_id_test = None
control_diabetes_id_test = None
control_erc_id_test = None
control_dislipidemia_id_test = None

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_control_cronicidad_test_data():
    """Setup: Crea un paciente y una atención general para las pruebas. Teardown: los elimina."""
    global paciente_id_test_cc, atencion_id_general_cc
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

    # Crear Atención general de prueba
    datos_atencion_general = {
        "paciente_id": paciente_id_test_cc,
        "medico_id": None, # No necesitamos un médico real para esta prueba
        "fecha_atencion": "2024-05-01",
        "entorno": "Institucional",
        "descripcion": "Atención general para prueba de control de cronicidad"
    }
    response_atencion_general = client.post("/atenciones/", json=datos_atencion_general)
    assert response_atencion_general.status_code == 201, response_atencion_general.text
    atencion_id_general_cc = response_atencion_general.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba en el orden correcto
    if control_hipertension_id_test:
        db_client.table("control_hipertension_detalles").delete().eq("id", control_hipertension_id_test).execute()
    if control_diabetes_id_test:
        db_client.table("control_diabetes_detalles").delete().eq("id", control_diabetes_id_test).execute()
    if control_erc_id_test:
        db_client.table("control_erc_detalles").delete().eq("id", control_erc_id_test).execute()
    if control_dislipidemia_id_test:
        db_client.table("control_dislipidemia_detalles").delete().eq("id", control_dislipidemia_id_test).execute()
    if control_cronicidad_id_test:
        db_client.table("control_cronicidad").delete().eq("id", control_cronicidad_id_test).execute()
    if atencion_id_general_cc:
        db_client.table("atenciones").delete().eq("id", atencion_id_general_cc).execute()
    if paciente_id_test_cc:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_cc).execute()

def test_01_create_control_cronicidad():
    """Verifica la creación de un nuevo registro de control de cronicidad (padre)."""
    global control_cronicidad_id_test
    assert atencion_id_general_cc is not None

    datos_control_cronicidad = {
        "atencion_id": atencion_id_general_cc,
        "tipo_cronicidad": "Hipertensión",
        "fecha_control": "2024-05-01",
        "estado_control": "Estable",
        "adherencia_tratamiento": "Buena",
        "peso_kg": 75.5,
        "talla_cm": 170.0,
        "imc": 26.1,
        "observaciones": "Paciente con buen control de TA."
    }

    response = client.post("/control-cronicidad/", json=datos_control_cronicidad)
    
    assert response.status_code == 201, response.text
    data = response.json()
    control_cronicidad_id_test = data["id"]
    
    assert data["atencion_id"] == atencion_id_general_cc
    assert data["tipo_cronicidad"] == "Hipertensión"

def test_02_create_control_hipertension_detalles():
    """Verifica la creación de detalles específicos para control de hipertensión."""
    global control_hipertension_id_test
    assert control_cronicidad_id_test is not None

    datos_hipertension = {
        "control_cronicidad_id": control_cronicidad_id_test,
        "presion_arterial_sistolica": 120,
        "presion_arterial_diastolica": 80,
        "presion_arterial_sistolica_anterior": 130,
        "presion_arterial_diastolica_anterior": 85,
        "fecha_ta_anterior": "2024-04-01"
    }

    response = client.post("/control-cronicidad/hipertension-detalles/", json=datos_hipertension)
    
    assert response.status_code == 201, response.text
    data = response.json()
    control_hipertension_id_test = data["id"]
    
    assert data["control_cronicidad_id"] == control_cronicidad_id_test
    assert data["presion_arterial_sistolica"] == 120

def test_03_create_control_diabetes_detalles():
    """Verifica la creación de detalles específicos para control de diabetes."""
    global control_diabetes_id_test
    assert control_cronicidad_id_test is not None

    datos_diabetes = {
        "control_cronicidad_id": control_cronicidad_id_test,
        "ultima_hba1c": 6.5,
        "fecha_ultima_hba1c": "2024-03-15",
        "fuente_ultima_hba1c": "Laboratorio",
        "rango_hba1c_ultima": "Normal",
        "anterior_hba1c": 7.0,
        "fecha_anterior_hba1c": "2023-09-15",
        "fuente_anterior_hba1c": "Laboratorio",
        "rango_hba1c_anterior": "Alto",
        "diferencia_hba1c": -0.5,
        "seguimiento_hba1c": "Mejora"
    }

    response = client.post("/control-cronicidad/diabetes-detalles/", json=datos_diabetes)
    
    assert response.status_code == 201, response.text
    data = response.json()
    control_diabetes_id_test = data["id"]
    
    assert data["control_cronicidad_id"] == control_cronicidad_id_test
    assert data["ultima_hba1c"] == 6.5

def test_04_create_control_erc_detalles():
    """Verifica la creación de detalles específicos para control de ERC."""
    global control_erc_id_test
    assert control_cronicidad_id_test is not None

    datos_erc = {
        "control_cronicidad_id": control_cronicidad_id_test,
        "ultima_creatinina": 1.2,
        "fecha_ultima_creatinina": "2024-04-20",
        "fuente_ultima_creatinina": "Laboratorio",
        "tasa_filtracion_glomerular_cockroft_gault": 75.0,
        "estadio_erc_cockroft_gault": "G2"
    }

    response = client.post("/control-cronicidad/erc-detalles/", json=datos_erc)
    
    assert response.status_code == 201, response.text
    data = response.json()
    control_erc_id_test = data["id"]
    
    assert data["control_cronicidad_id"] == control_cronicidad_id_test
    assert data["ultima_creatinina"] == 1.2

def test_05_create_control_dislipidemia_detalles():
    """Verifica la creación de detalles específicos para control de dislipidemia."""
    global control_dislipidemia_id_test
    assert control_cronicidad_id_test is not None

    datos_dislipidemia = {
        "control_cronicidad_id": control_cronicidad_id_test,
        "ultimo_ct": 200.0,
        "fecha_ultimo_ct": "2024-04-10",
        "fuente_ultimo_ct": "Laboratorio",
        "ultimo_ldl": 120.0,
        "ultimo_hdl": 45.0,
        "ultimo_tg": 150.0
    }

    response = client.post("/control-cronicidad/dislipidemia-detalles/", json=datos_dislipidemia)
    
    assert response.status_code == 201, response.text
    data = response.json()
    control_dislipidemia_id_test = data["id"]
    
    assert data["control_cronicidad_id"] == control_cronicidad_id_test
    assert data["ultimo_ct"] == 200.0

def test_06_get_control_cronicidad_by_id():
    """Verifica la obtención de un registro de control de cronicidad por su ID."""
    assert control_cronicidad_id_test is not None

    response = client.get(f"/control-cronicidad/{control_cronicidad_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == control_cronicidad_id_test
    assert data["atencion_id"] == atencion_id_general_cc

def test_07_get_hipertension_detalles_by_id():
    """Verifica la obtención de detalles de hipertensión por su ID."""
    assert control_hipertension_id_test is not None

    response = client.get(f"/control-cronicidad/hipertension-detalles/{control_hipertension_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == control_hipertension_id_test
    assert data["control_cronicidad_id"] == control_cronicidad_id_test

def test_08_get_diabetes_detalles_by_id():
    """Verifica la obtención de detalles de diabetes por su ID."""
    assert control_diabetes_id_test is not None

    response = client.get(f"/control-cronicidad/diabetes-detalles/{control_diabetes_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == control_diabetes_id_test
    assert data["control_cronicidad_id"] == control_diabetes_id_test

def test_09_get_erc_detalles_by_id():
    """Verifica la obtención de detalles de ERC por su ID."""
    assert control_erc_id_test is not None

    response = client.get(f"/control-cronicidad/erc-detalles/{control_erc_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == control_erc_id_test
    assert data["control_cronicidad_id"] == control_erc_id_test

def test_10_get_dislipidemia_detalles_by_id():
    """Verifica la obtención de detalles de dislipidemia por su ID."""
    assert control_dislipidemia_id_test is not None

    response = client.get(f"/control-cronicidad/dislipidemia-detalles/{control_dislipidemia_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == control_dislipidemia_id_test
    assert data["control_cronicidad_id"] == control_dislipidemia_id_test

def test_11_get_all_control_cronicidad():
    """Verifica la obtención de todos los registros de control de cronicidad."""
    response = client.get("/control-cronicidad/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["id"] == control_cronicidad_id_test for d in data)

def test_12_get_hipertension_detalles_by_control_id():
    """Verifica la obtención de detalles de hipertensión por control_cronicidad_id."""
    assert control_cronicidad_id_test is not None

    response = client.get(f"/control-cronicidad/hipertension-detalles/control/{control_cronicidad_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["control_cronicidad_id"] == control_cronicidad_id_test for d in data)

def test_13_get_diabetes_detalles_by_control_id():
    """Verifica la obtención de detalles de diabetes por control_cronicidad_id."""
    assert control_cronicidad_id_test is not None

    response = client.get(f"/control-cronicidad/diabetes-detalles/control/{control_cronicidad_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["control_cronicidad_id"] == control_cronicidad_id_test for d in data)

def test_14_get_erc_detalles_by_control_id():
    """Verifica la obtención de detalles de ERC por control_cronicidad_id."""
    assert control_cronicidad_id_test is not None

    response = client.get(f"/control-cronicidad/erc-detalles/control/{control_cronicidad_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["control_cronicidad_id"] == control_cronicidad_id_test for d in data)

def test_15_get_dislipidemia_detalles_by_control_id():
    """Verifica la obtención de detalles de dislipidemia por control_cronicidad_id."""
    assert control_cronicidad_id_test is not None

    response = client.get(f"/control-cronicidad/dislipidemia-detalles/control/{control_cronicidad_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d["control_cronicidad_id"] == control_cronicidad_id_test for d in data)
