import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date

# Importar el modelo Medico
from models.medico_model import Medico
from database import get_supabase_client # <-- ¡Esta línea faltaba!
from database import get_supabase_client # <-- ¡Esta línea faltaba!
from database import get_supabase_client # <-- ¡Esta línea faltaba!
from database import get_supabase_client # <-- ¡Esta línea faltaba!
from database import get_supabase_client # <-- ¡Esta línea faltaba!
from database import get_supabase_client # <-- ¡Esta línea faltaba!

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_doc_unico = str(uuid4())
paciente_id_creado = None
medico_id_creado = None
atencion_id_creada = None


# --- Pruebas para Atenciones ---

def test_00_setup_crear_medico_y_paciente():
    """Setup: Crea un médico y un paciente para las pruebas de atención."""
    global paciente_id_creado, medico_id_creado

    # Crear Medico
    datos_medico = {
        "primer_nombre": f"DrTest-{str(uuid4())[:8]}",
        "primer_apellido": "MedicoTest",
        "registro_profesional": f"REG-{str(uuid4())[:8]}",
        "especialidad": "General"
    }
    # Insertar directamente en la base de datos (no hay endpoint POST para medicos aún)
    # Esto requiere que la tabla 'medicos' permita inserciones (RLS)
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    response_medico = db_client.table("medicos").insert(datos_medico).execute()
    assert response_medico.data is not None, response_medico.text
    medico_id_creado = response_medico.data[0]["id"]
    assert medico_id_creado is not None

    # Crear Paciente
    dia_unico = int(paciente_doc_unico[:8], 16) % 28 + 1
    fecha_nacimiento_unica = date(1990, 1, dia_unico).isoformat()

    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": paciente_doc_unico,
        "primer_nombre": f"Test-{paciente_doc_unico[:8]}",
        "primer_apellido": "Paciente",
        "fecha_nacimiento": fecha_nacimiento_unica,
        "genero": f"O-{paciente_doc_unico[:4]}"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    data_paciente = response_paciente.json()["data"][0]
    paciente_id_creado = data_paciente["id"]
    assert paciente_id_creado is not None


def test_01_crear_atencion():
    """Crea una atención asociada al paciente y médico recién creados."""
    global atencion_id_creada
    assert paciente_id_creado is not None
    assert medico_id_creado is not None

    datos_atencion = {
        "paciente_id": paciente_id_creado,
        "medico_id": medico_id_creado, # Usar el ID del médico creado
        "fecha_atencion": "2025-09-08",
        "entorno": "Institucional",
        "descripcion": "Consulta de control general"
    }
    response = client.post("/atenciones/", json=datos_atencion)
    assert response.status_code == 201, response.text
    data = response.json()["data"][0]
    atencion_id_creada = data["id"]
    assert atencion_id_creada is not None
    assert data["paciente_id"] == paciente_id_creado
    assert data["medico_id"] == medico_id_creado

def test_02_obtener_atencion_por_id():
    """Verifica que la atención creada se pueda obtener por su ID."""
    assert atencion_id_creada is not None
    response = client.get(f"/atenciones/{atencion_id_creada}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == atencion_id_creada

def test_03_obtener_atenciones_por_paciente_id():
    """Verifica que se puedan listar las atenciones de un paciente."""
    assert paciente_id_creado is not None
    response = client.get(f"/atenciones/paciente/{paciente_id_creado}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert data[0]["paciente_id"] == paciente_id_creado

# --- Limpieza (Opcional, pero buena práctica para pruebas de integración) ---
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    """Elimina los datos de prueba después de que todas las pruebas hayan terminado."""
    yield
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    # Eliminar en el orden correcto para no violar las foreign keys
    if atencion_id_creada:
        db_client.table("atenciones").delete().eq("id", atencion_id_creada).execute()
    if paciente_id_creado:
        db_client.table("pacientes").delete().eq("id", paciente_id_creado).execute()
    if medico_id_creado:
        db_client.table("medicos").delete().eq("id", medico_id_creado).execute()
