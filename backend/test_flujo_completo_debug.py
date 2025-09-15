#!/usr/bin/env python3

from fastapi.testclient import TestClient
from main import app
from datetime import datetime
import random

client = TestClient(app)

def crear_paciente_test():
    paciente_data = {
        'tipo_documento': 'CC',
        'numero_documento': str(random.randint(1000000000, 9999999999)),
        'primer_nombre': 'Test',
        'primer_apellido': 'Flujo',
        'fecha_nacimiento': '2020-01-15',
        'genero': 'MASCULINO'
    }
    
    response = client.post('/pacientes/', json=paciente_data)
    assert response.status_code == 201
    return response.json()['data'][0]['id']

def crear_atencion_test_data(paciente_id):
    return {
        'paciente_id': paciente_id,
        'codigo_atencion_primera_infancia_unico': f'PI-FLUJO-{datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}',
        'fecha_atencion': '2025-09-15',
        'entorno': 'INSTITUCION_SALUD',
        'peso_kg': 12.5,
        'talla_cm': 85.0,
        'perimetro_cefalico_cm': 47.5,
        'estado_nutricional': 'NORMAL'
    }

print("=== TEST FLUJO COMPLETO ===")

# 1. Crear paciente
print("1. Creando paciente...")
paciente_id = crear_paciente_test()
print(f"Paciente ID: {paciente_id}")

# 2. Crear atención básica
print("2. Creando atención...")
atencion_data = crear_atencion_test_data(paciente_id)
create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
assert create_response.status_code == 201
atencion_id = create_response.json()["id"]
print(f"Atención ID: {atencion_id}")

# 3. Aplicar EAD-3
print("3. Aplicando EAD-3...")
datos_ead3 = {
    "ead3_motricidad_gruesa_puntaje": 75,
    "ead3_motricidad_fina_puntaje": 80,
    "ead3_audicion_lenguaje_puntaje": 70,
    "ead3_personal_social_puntaje": 85
}
ead3_response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/ead3", json=datos_ead3)
assert ead3_response.status_code == 200
print("✅ EAD-3 aplicado")

# 4. Aplicar ASQ-3
print("4. Aplicando ASQ-3...")
datos_asq3 = {
    "asq3_comunicacion_puntaje": 45,
    "asq3_motor_grueso_puntaje": 50,
    "asq3_motor_fino_puntaje": 40,
    "asq3_resolucion_problemas_puntaje": 55,
    "asq3_personal_social_puntaje": 48
}
asq3_response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/asq3", json=datos_asq3)
assert asq3_response.status_code == 200
print("✅ ASQ-3 aplicado")

# 5. Actualizar datos adicionales
print("5. Actualizando datos adicionales...")
update_data = {
    "esquema_vacunacion_completo": True,
    "bcg_aplicada": True,
    "hepatitis_b_rn_aplicada": True,
    "pentavalente_dosis_completas": 3,
    "srp_aplicada": True,
    "tamizaje_visual_realizado": True,
    "tamizaje_visual_resultado_general": "NORMAL",
    "observaciones_profesional_primera_infancia": "Desarrollo normal, continuar seguimiento rutinario"
}
update_response = client.put(f"/atenciones-primera-infancia/{atencion_id}", json=update_data)
print(f"Update response: {update_response.status_code}")
if update_response.status_code != 200:
    print(f"Error: {update_response.text}")
else:
    print("✅ Datos actualizados")

# 6. Verificar estado final
print("6. Verificando estado final...")
final_response = client.get(f"/atenciones-primera-infancia/{atencion_id}")
assert final_response.status_code == 200

final_data = final_response.json()
print(f"EAD-3 aplicada: {final_data.get('ead3_aplicada')}")
print(f"ASQ-3 aplicado: {final_data.get('asq3_aplicado')}")
print(f"Esquema vacunación: {final_data.get('esquema_vacunacion_completo')}")
print(f"Desarrollo apropiado: {final_data.get('desarrollo_apropiado_edad')}")
print(f"Porcentaje vacunación: {final_data.get('porcentaje_esquema_vacunacion')}")

print("✅ FLUJO COMPLETO EXITOSO")