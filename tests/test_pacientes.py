import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Usar un número de documento único para cada ejecución de prueba para evitar conflictos
from uuid import uuid4
documento_unico = str(uuid4())[:10]

paciente_id_creado = None

@pytest.mark.parametrize("test_order", range(1))
def test_01_crear_paciente(test_order):
    global paciente_id_creado
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": documento_unico,
        "primer_nombre": "Test",
        "primer_apellido": "Paciente",
        "fecha_nacimiento": "2000-01-01",
        "genero": "O"
    }
    response = client.post("/pacientes/", json=datos_paciente)
    assert response.status_code == 201, response.text
    data = response.json()["data"][0]
    assert data["numero_documento"] == documento_unico
    paciente_id_creado = data["id"]
    assert paciente_id_creado is not None

@pytest.mark.parametrize("test_order", range(1))
def test_02_actualizar_paciente(test_order):
    assert paciente_id_creado is not None, "Crear paciente debe ejecutarse primero"
    datos_actualizados = {
        "tipo_documento": "CC",
        "numero_documento": documento_unico,
        "primer_nombre": "TestActualizado",
        "primer_apellido": "Paciente",
        "fecha_nacimiento": "2000-01-01",
        "genero": "O"
    }
    response = client.put(f"/pacientes/{paciente_id_creado}", json=datos_actualizados)
    assert response.status_code == 200, response.text
    data = response.json()["data"][0]
    assert data["primer_nombre"] == "TestActualizado"

@pytest.mark.parametrize("test_order", range(1))
def test_03_eliminar_paciente(test_order):
    assert paciente_id_creado is not None, "Crear paciente debe ejecutarse primero"
    response = client.delete(f"/pacientes/{paciente_id_creado}")
    assert response.status_code == 204, response.text

@pytest.mark.parametrize("test_order", range(1))
def test_04_verificar_eliminacion(test_order):
    assert paciente_id_creado is not None, "Crear paciente debe ejecutarse primero"
    response = client.get(f"/pacientes/{paciente_id_creado}")
    assert response.status_code == 404, response.text