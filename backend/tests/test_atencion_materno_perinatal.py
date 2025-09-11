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
        "fecha_nacimiento": "1990-01-01",
        "genero": "F" # Materno Perinatal usually for females
    }
    client.post("/pacientes/", json=patient_data)
    return patient_id

def create_test_atencion_materno_perinatal_data(patient_id: str, fecha_atencion: str):
    return {
        "paciente_id": patient_id,
        "fecha_atencion": fecha_atencion,
        "entorno": "Hospital",
        "estado_gestacional_semanas": 30,
        "fecha_probable_parto": "2024-03-15",
        "numero_controles_prenatales": 5,
        "riesgo_biopsicosocial": "Bajo",
        "resultado_tamizaje_vih": "Negativo",
        "resultado_tamizaje_sifilis": "Negativo",
        "resultado_tamizaje_hepatitis_b": "Negativo",
        "resultado_tamizaje_toxoplasmosis": "Negativo",
        "resultado_tamizaje_estreptococo_b": "No realizado",
        "vacunacion_tdap_completa": True,
        "vacunacion_influenza_completa": True,
        "suplementacion_hierro": True,
        "suplementacion_acido_folico": True,
        "suplementacion_calcio": True,
        "condicion_diabetes_preexistente": False,
        "condicion_hipertension_preexistente": False,
        "condicion_tiroidea_preexistente": False,
        "condicion_epilepsia_preexistente": False,
        "num_gestaciones": 1,
        "num_partos": 0,
        "num_cesareas": 0,
        "num_abortos": 0,
        "num_muertes_perinatales": 0,
        "antecedente_preeclampsia": False,
        "antecedente_hemorragia_postparto": False,
        "antecedente_embarazo_multiple": False,
        "signo_alarma_sangrado": False,
        "signo_alarma_cefalea": False,
        "signo_alarma_vision_borrosa": False,
        "tipo_parto": "N/A",
        "fecha_parto": None,
        "hora_parto": None,
        "complicaciones_parto": None,
        "manejo_alumbramiento": None,
        "peso_recien_nacido_kg": None,
        "talla_recien_nacido_cm": None,
        "apgar_min1": None,
        "apgar_min5": None,
        "adaptacion_neonatal_observaciones": None,
        "tamizaje_auditivo_neonatal": None,
        "tamizaje_metabolico_neonatal": None,
        "tamizaje_cardiopatias_congenitas": None,
        "profilaxis_vitamina_k": None,
        "profilaxis_ocular": None,
        "vacunacion_bcg": None,
        "vacunacion_hepatitis_b": None,
        "alimentacion_egreso": None,
        "estado_puerperio_observaciones": None,
        "signo_alarma_fiebre_postparto": None,
        "signo_alarma_sangrado_excesivo_postparto": None,
        "metodo_anticonceptivo_postparto": None
    }

def test_create_atencion_materno_perinatal():
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_materno_perinatal_data(patient_id, "2023-01-20")
    response = client.post("/atenciones-materno-perinatal/", json=atencion_data)
    assert response.status_code == 201
    assert response.json()["paciente_id"] == patient_id
    assert response.json()["fecha_atencion"] == "2023-01-20"
    assert "id" in response.json()

def test_get_all_atenciones_materno_perinatal():
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_materno_perinatal_data(patient_id, "2023-02-05")
    create_response = client.post("/atenciones-materno-perinatal/", json=atencion_data)
    assert create_response.status_code == 201

    response = client.get("/atenciones-materno-perinatal/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(item["id"] == create_response.json()["id"] for item in response.json())

def test_get_atencion_materno_perinatal_by_id():
    patient_id = create_test_patient(str(uuid4()))
    atencion_data = create_test_atencion_materno_perinatal_data(patient_id, "2024-03-01")
    create_response = client.post("/atenciones-materno-perinatal/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]

    response = client.get(f"/atenciones-materno-perinatal/{atencion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == atencion_id
    assert response.json()["paciente_id"] == patient_id