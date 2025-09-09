import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs ---
medico_id_test_ic = None
intervencion_id_test = None

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_test_intervencion():
    """Setup: Crea un médico para las pruebas. Teardown: lo elimina."""
    global medico_id_test_ic
    
    # Setup: Crear un médico de prueba
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    datos_medico = {
        "primer_nombre": f"DrTestIC-{str(uuid4())[:8]}",
        "primer_apellido": "IntervencionTest",
        "registro_profesional": f"REG-IC-{str(uuid4())[:8]}",
        "especialidad": f"Comunitaria-{str(uuid4())[:8]}"
    }
    response_medico = db_client.table("medicos").insert(datos_medico).execute()
    assert response_medico.data, "No se pudo crear el médico de prueba para las intervenciones colectivas"
    medico_id_test_ic = response_medico.data[0]["id"]
    
    yield # Las pruebas se ejecutan aquí
    
    # Teardown: Limpiar datos de prueba
    if intervencion_id_test:
        db_client.table("intervenciones_colectivas").delete().eq("id", intervencion_id_test).execute()
    if medico_id_test_ic:
        db_client.table("medicos").delete().eq("id", medico_id_test_ic).execute()

def test_01_crear_intervencion_colectiva():
    """Verifica la creación de una nueva intervención colectiva."""
    global intervencion_id_test
    assert medico_id_test_ic is not None

    datos_intervencion = {
        "fecha_intervencion": date.today().isoformat(),
        "entorno": "Comunitario",
        "tema": "Jornada de Salud Preventiva",
        "poblacion_objetivo": "Familias de la vereda El Carmen",
        "responsable_id": medico_id_test_ic,
        "resumen": "Se realizaron charlas sobre nutrición y se tomaron muestras de presión arterial."
    }

    response = client.post("/intervenciones-colectivas/", json=datos_intervencion)
    
    assert response.status_code == 201, response.text
    data = response.json()
    intervencion_id_test = data["id"]
    
    assert data["tema"] == "Jornada de Salud Preventiva"
    assert data["entorno"] == "Comunitario"
    assert data["responsable_id"] == medico_id_test_ic

def test_02_get_intervenciones_colectivas():
    """Verifica que se puedan obtener todas las intervenciones colectivas."""
    assert intervencion_id_test is not None

    response = client.get("/intervenciones-colectivas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verificar que nuestra intervención creada está en la lista
    assert any(d['id'] == intervencion_id_test for d in data)
