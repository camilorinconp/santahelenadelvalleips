import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_creado = None
medico_id_creado = None
atencion_id_creada = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atenciones():
    """Setup: Crea un médico y un paciente para las pruebas. Teardown: los elimina."""
    global paciente_id_creado, medico_id_creado
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Medico
    datos_medico = {
        "primer_nombre": f"DrTestAtt-{str(uuid4())[:4]}",
        "primer_apellido": "AtencionTest",
        "registro_profesional": f"REG-ATT-{str(uuid4())[:8]}",
        "especialidad": "General"
    }
    response_medico = db_client.table("medicos").insert(datos_medico).execute()
    assert response_medico.data, "No se pudo crear el médico de prueba"
    medico_id_creado = response_medico.data[0]["id"]

    # Crear Paciente
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "PacienteAtencion",
        "primer_apellido": "Test",
        "fecha_nacimiento": "1985-01-01",
        "genero": "M"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_creado = response_paciente.json()["data"][0]["id"]

    yield

    # Teardown
    if atencion_id_creada:
        db_client.table("atenciones").delete().eq("id", atencion_id_creada).execute()
    if paciente_id_creado:
        db_client.table("pacientes").delete().eq("id", paciente_id_creado).execute()
    if medico_id_creado:
        db_client.table("medicos").delete().eq("id", medico_id_creado).execute()

def test_01_crear_atencion_generica():
    """Crea una atención genérica que no tiene una tabla de detalle."""
    global atencion_id_creada
    assert paciente_id_creado is not None

    # Para una atención genérica, el detalle_id puede ser un UUID nulo o aleatorio
    # ya que no apunta a una tabla de detalle real.
    detalle_id_fake = str(uuid4())

    datos_atencion = {
        "paciente_id": paciente_id_creado,
        "medico_id": medico_id_creado,
        "fecha_atencion": date.today().isoformat(),
        "entorno": "Institucional",
        "tipo_atencion": "Consulta General",
        "detalle_id": detalle_id_fake
    }
    response = client.post("/atenciones/", json=datos_atencion)
    assert response.status_code == 201, response.text
    data = response.json()
    atencion_id_creada = data["id"]
    
    assert data["paciente_id"] == paciente_id_creado
    assert data["tipo_atencion"] == "Consulta General"

def test_02_obtener_atencion_por_id():
    """Verifica que la atención creada se pueda obtener por su ID."""
    assert atencion_id_creada is not None
    response = client.get(f"/atenciones/{atencion_id_creada}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == atencion_id_creada

def test_03_obtener_atenciones_por_paciente_id():
    """Verifica que se puedan listar las atenciones de un paciente."""
    assert paciente_id_creado is not None
    response = client.get(f"/atenciones/paciente/{paciente_id_creado}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["paciente_id"] == paciente_id_creado