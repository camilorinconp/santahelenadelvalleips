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

def test_02_get_intervencion_by_id():
    """Verifica la obtención de una intervención por su ID."""
    assert intervencion_id_test is not None
    response = client.get(f"/intervenciones-colectivas/{intervencion_id_test}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == intervencion_id_test
    assert data["tema"] == "Jornada de Salud Preventiva"

def test_03_get_intervenciones_colectivas_all():
    """Verifica que se puedan obtener todas las intervenciones colectivas."""
    assert intervencion_id_test is not None
    response = client.get("/intervenciones-colectivas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(d['id'] == intervencion_id_test for d in data)

def test_04_get_intervenciones_colectivas_filtered():
    """Verifica que se puedan filtrar las intervenciones por entorno."""
    assert intervencion_id_test is not None
    # Crear una segunda intervención en otro entorno para asegurar que el filtro funciona
    datos_intervencion_2 = {
        "fecha_intervencion": date.today().isoformat(),
        "entorno": "Educativo",
        "tema": "Charla sobre higiene",
        "poblacion_objetivo": "Estudiantes Colegio XYZ",
        "responsable_id": medico_id_test_ic
    }
    response_create = client.post("/intervenciones-colectivas/", json=datos_intervencion_2)
    assert response_create.status_code == 201

    # Probar el filtro
    response = client.get("/intervenciones-colectivas/?entorno=Comunitario")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Todos los resultados deben ser del entorno 'Comunitario'
    assert all(d['entorno'] == 'Comunitario' for d in data)
    # Nuestra intervención original debe estar en los resultados
    assert any(d['id'] == intervencion_id_test for d in data)

    # Limpiar el dato extra creado
    id_extra = response_create.json()["id"]
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    db_client.table("intervenciones_colectivas").delete().eq("id", id_extra).execute()


def test_05_update_intervencion_colectiva():
    """Verifica la actualización de una intervención colectiva."""
    assert intervencion_id_test is not None
    
    datos_actualizacion = {
        "fecha_intervencion": date.today().isoformat(),
        "entorno": "Comunitario",
        "tema": "Jornada de Salud Preventiva (Actualizada)",
        "poblacion_objetivo": "Familias de la vereda El Carmen y vereda La Esperanza",
        "responsable_id": medico_id_test_ic,
        "resumen": "Se incluyó vacunación."
    }

    response = client.put(f"/intervenciones-colectivas/{intervencion_id_test}", json=datos_actualizacion)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["tema"] == "Jornada de Salud Preventiva (Actualizada)"
    assert data["resumen"] == "Se incluyó vacunación."

def test_06_delete_intervencion_colectiva():
    """Verifica la eliminación de una intervención colectiva."""
    global intervencion_id_test
    assert intervencion_id_test is not None
    
    response = client.delete(f"/intervenciones-colectivas/{intervencion_id_test}")
    assert response.status_code == 204, response.text
    
    # Verificar que ya no se puede obtener
    response_get = client.get(f"/intervenciones-colectivas/{intervencion_id_test}")
    assert response_get.status_code == 404
    
    # Limpiar la variable global para que el teardown no intente borrarlo de nuevo
    intervencion_id_test = None