from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date

client = TestClient(app)

def create_test_patient(patient_id: str):
    patient_data = {
        "id": patient_id,
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:9], # Unique document number
        "primer_nombre": "Test",
        "primer_apellido": "Patient",
        "fecha_nacimiento": "2000-01-01",
        "genero": "M"
    }
    client.post("/pacientes/", json=patient_data)
    return patient_id

def create_test_atencion_data(patient_id: str, fecha_atencion: str):
    return {
        "paciente_id": patient_id,
        "fecha_atencion": fecha_atencion,
        "entorno": "Hogar",
        "peso_kg": 10.5,
        "talla_cm": 80.0,
        "perimetro_cefalico_cm": 45.0,
        "estado_nutricional": "Normal",
        "practicas_alimentarias_observaciones": "Lactancia materna exclusiva",
        "suplementacion_hierro": True,
        "suplementacion_vitamina_a": True,
        "suplementacion_micronutrientes_polvo": False,
        "desparasitacion_intestinal": True,
        "desarrollo_fisico_motor_observaciones": "Normal",
        "desarrollo_socioemocional_observaciones": "Normal",
        "desarrollo_cognitivo_observaciones": "Normal",
        "hitos_desarrollo_acordes_edad": True,
        "salud_visual_observaciones": "Normal",
        "salud_visual_tamizaje_resultado": "Normal",
        "salud_auditiva_comunicativa_observaciones": "Normal",
        "salud_auditiva_tamizaje_resultado": "Normal",
        "salud_bucal_observaciones": "Normal",
        "salud_bucal_higiene_oral": "Buena",
        "salud_sexual_observaciones": "N/A",
        "salud_mental_observaciones": "Normal",
        "esquema_vacunacion_completo": True,
        "vacunas_pendientes": "Ninguna"
    }

def test_create_atencion_primera_infancia():
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_data(patient_id, "2023-01-15")
    response = client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert response.status_code == 201
    assert response.json()["paciente_id"] == patient_id
    assert response.json()["fecha_atencion"] == "2023-01-15"
    assert "id" in response.json()

def test_get_all_atenciones_primera_infancia():
    # Create a new attention for this test
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_data(patient_id, "2023-02-01")
    create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201

    response = client.get("/atenciones-primera-infancia/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Check if the newly created attention is in the list
    assert any(item["id"] == create_response.json()["id"] for item in response.json())

def test_get_atencion_primera_infancia_by_id():
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_data(patient_id, "2024-02-20")
    create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]

    response = client.get(f"/atenciones-primera-infancia/{atencion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == atencion_id
    assert response.json()["paciente_id"] == patient_id
