from uuid import uuid4
from datetime import date

# Tests now use global configuration from conftest.py

def create_test_patient(patient_id: str, test_client):
    patient_data = {
        "id": patient_id,
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:9], # Unique document number
        "primer_nombre": "Test",
        "primer_apellido": "Patient",
        "fecha_nacimiento": "2000-01-01",
        "genero": "MASCULINO"  # Updated for consistency
    }
    response = test_client.post("/pacientes/", json=patient_data)
    if response.status_code != 201:
        raise Exception(f"Failed to create test patient: {response.text}")
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

# ================== Tests Básicos Existentes (Actualizados) ==================

def test_create_atencion_primera_infancia(test_client):
    """Test crear atención primera infancia usando fixture global"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2023-01-15")
    response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert response.status_code == 201
    assert response.json()["paciente_id"] == patient_id
    assert response.json()["fecha_atencion"] == "2023-01-15"
    assert "id" in response.json()

def test_get_all_atenciones_primera_infancia(test_client):
    """Test obtener todas las atenciones primera infancia"""
    # Create a new attention for this test
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2023-02-01")
    create_response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201

    response = test_client.get("/atenciones-primera-infancia/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Check if the newly created attention is in the list
    assert any(item["id"] == create_response.json()["id"] for item in response.json())

def test_get_atencion_primera_infancia_by_id(test_client):
    """Test obtener atención primera infancia por ID"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2024-02-20")
    create_response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]

    response = test_client.get(f"/atenciones-primera-infancia/{atencion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == atencion_id
    assert response.json()["paciente_id"] == patient_id

# ================== Tests Nuevos CRUD Completo ==================

def test_get_atenciones_primera_infancia_by_paciente(test_client):
    """Test obtener atenciones de primera infancia por paciente"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    
    # Crear 2 atenciones para el mismo paciente
    atencion_data1 = create_test_atencion_data(patient_id, "2023-01-15")
    atencion_data2 = create_test_atencion_data(patient_id, "2023-02-15")
    
    response1 = test_client.post("/atenciones-primera-infancia/", json=atencion_data1)
    response2 = test_client.post("/atenciones-primera-infancia/", json=atencion_data2)
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Obtener atenciones por paciente
    response = test_client.get(f"/atenciones-primera-infancia/paciente/{patient_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    
    # Verificar que ambas atenciones están en la respuesta
    atencion_ids = [item["id"] for item in response.json()]
    assert response1.json()["id"] in atencion_ids
    assert response2.json()["id"] in atencion_ids

def test_update_atencion_primera_infancia_put(test_client):
    """Test actualizar atención primera infancia completa (PUT)"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2023-01-15")
    
    # Crear atención
    create_response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]
    
    # Datos actualizados
    updated_data = create_test_atencion_data(patient_id, "2023-01-20")
    updated_data.update({
        "peso_kg": 11.0,
        "talla_cm": 82.0,
        "estado_nutricional": "Sobrepeso",
        "esquema_vacunacion_completo": False,
        "vacunas_pendientes": "Triple viral"
    })
    
    # Actualizar
    response = test_client.put(f"/atenciones-primera-infancia/{atencion_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["id"] == atencion_id
    assert response.json()["peso_kg"] == 11.0
    assert response.json()["talla_cm"] == 82.0
    assert response.json()["estado_nutricional"] == "Sobrepeso"
    assert response.json()["fecha_atencion"] == "2023-01-20"
    assert response.json()["esquema_vacunacion_completo"] == False
    assert response.json()["vacunas_pendientes"] == "Triple viral"

def test_patch_atencion_primera_infancia(test_client):
    """Test actualización parcial de atención primera infancia (PATCH)"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2023-01-15")
    
    # Crear atención
    create_response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]
    
    # Actualización parcial - solo algunos campos
    patch_data = {
        "peso_kg": 12.5,
        "estado_nutricional": "Desnutrición leve",
        "desarrollo_fisico_motor_observaciones": "Ligero retraso en marcha"
    }
    
    # Actualizar parcialmente
    response = test_client.patch(f"/atenciones-primera-infancia/{atencion_id}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["id"] == atencion_id
    assert response.json()["peso_kg"] == 12.5
    assert response.json()["estado_nutricional"] == "Desnutrición leve"
    assert response.json()["desarrollo_fisico_motor_observaciones"] == "Ligero retraso en marcha"
    
    # Verificar que otros campos no cambiaron
    assert response.json()["talla_cm"] == 80.0  # Valor original
    assert response.json()["fecha_atencion"] == "2023-01-15"  # Valor original

def test_delete_atencion_primera_infancia(test_client):
    """Test eliminar atención primera infancia"""
    patient_id = create_test_patient(str(uuid4()), test_client)
    atencion_data = create_test_atencion_data(patient_id, "2023-01-15")
    
    # Crear atención
    create_response = test_client.post("/atenciones-primera-infancia/", json=atencion_data)
    assert create_response.status_code == 201
    atencion_id = create_response.json()["id"]
    
    # Verificar que existe
    get_response = test_client.get(f"/atenciones-primera-infancia/{atencion_id}")
    assert get_response.status_code == 200
    
    # Eliminar
    delete_response = test_client.delete(f"/atenciones-primera-infancia/{atencion_id}")
    assert delete_response.status_code == 204
    
    # Verificar que ya no existe
    get_after_delete = test_client.get(f"/atenciones-primera-infancia/{atencion_id}")
    assert get_after_delete.status_code == 404

def test_get_primera_infancia_stats(test_client):
    """Test obtener estadísticas de primera infancia"""
    patient_id1 = create_test_patient(str(uuid4()), test_client)
    patient_id2 = create_test_patient(str(uuid4()), test_client)
    
    # Crear atenciones con diferentes características
    atencion_data1 = create_test_atencion_data(patient_id1, "2023-01-15")
    atencion_data1.update({
        "estado_nutricional": "Normal",
        "esquema_vacunacion_completo": True
    })
    
    atencion_data2 = create_test_atencion_data(patient_id2, "2023-02-15")
    atencion_data2.update({
        "estado_nutricional": "Sobrepeso",
        "esquema_vacunacion_completo": False
    })
    
    # Crear las atenciones
    test_client.post("/atenciones-primera-infancia/", json=atencion_data1)
    test_client.post("/atenciones-primera-infancia/", json=atencion_data2)
    
    # Obtener estadísticas
    response = test_client.get("/atenciones-primera-infancia/stats/general")
    assert response.status_code == 200
    
    stats = response.json()
    assert "total_atenciones" in stats
    assert "estados_nutricionales" in stats
    assert "vacunacion" in stats
    assert stats["total_atenciones"] >= 2
    
    # Verificar estructura de vacunación
    assert "completa" in stats["vacunacion"]
    assert "incompleta" in stats["vacunacion"]
    assert "sin_especificar" in stats["vacunacion"]

# ================== Tests de Casos de Error ==================

def test_get_atencion_primera_infancia_not_found(test_client):
    """Test obtener atención que no existe"""
    fake_id = str(uuid4())
    response = test_client.get(f"/atenciones-primera-infancia/{fake_id}")
    assert response.status_code == 404

def test_update_atencion_primera_infancia_not_found(test_client):
    """Test actualizar atención que no existe"""
    fake_id = str(uuid4())
    patient_id = create_test_patient(str(uuid4()), test_client)
    update_data = create_test_atencion_data(patient_id, "2023-01-15")
    
    response = test_client.put(f"/atenciones-primera-infancia/{fake_id}", json=update_data)
    assert response.status_code == 404

def test_delete_atencion_primera_infancia_not_found(test_client):
    """Test eliminar atención que no existe"""
    fake_id = str(uuid4())
    response = test_client.delete(f"/atenciones-primera-infancia/{fake_id}")
    assert response.status_code == 404
