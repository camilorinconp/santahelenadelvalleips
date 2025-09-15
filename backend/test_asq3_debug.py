#!/usr/bin/env python3

from fastapi.testclient import TestClient
from main import app
from datetime import datetime
import random

client = TestClient(app)

# Crear paciente
paciente_data = {
    'tipo_documento': 'CC',
    'numero_documento': str(random.randint(1000000000, 9999999999)),
    'primer_nombre': 'Test',
    'primer_apellido': 'ASQ3',
    'fecha_nacimiento': '2020-01-15',
    'genero': 'MASCULINO'
}

print("1. Creando paciente...")
response = client.post('/pacientes/', json=paciente_data)
if response.status_code == 201:
    paciente_id = response.json()['data'][0]['id']
    print(f"Paciente ID: {paciente_id}")
    
    # Crear atención
    atencion_data = {
        'paciente_id': paciente_id,
        'codigo_atencion_primera_infancia_unico': f'PI-ASQ3-{datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}',
        'fecha_atencion': '2025-09-15',
        'entorno': 'INSTITUCION_SALUD',
        'peso_kg': 12.5,
        'talla_cm': 85.0,
        'perimetro_cefalico_cm': 47.5,
        'estado_nutricional': 'NORMAL'
    }
    
    print("2. Creando atención...")
    response = client.post('/atenciones-primera-infancia/', json=atencion_data)
    if response.status_code == 201:
        atencion_id = response.json()['id']
        print(f"Atencion ID: {atencion_id}")
        
        # Aplicar ASQ-3
        datos_asq3 = {
            "asq3_comunicacion_puntaje": 45,
            "asq3_motor_grueso_puntaje": 50,
            "asq3_motor_fino_puntaje": 40,
            "asq3_resolucion_problemas_puntaje": 55,
            "asq3_personal_social_puntaje": 48
        }
        
        print("3. Aplicando ASQ-3...")
        response = client.patch(f'/atenciones-primera-infancia/{atencion_id}/asq3', json=datos_asq3)
        print(f"ASQ-3 response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print("✅ ASQ-3 aplicado exitosamente")
            data = response.json()
            print(f"ASQ-3 aplicado: {data.get('asq3_aplicado')}")
            print(f"Comunicación: {data.get('asq3_comunicacion_puntaje')}")
    else:
        print(f"Error creando atención: {response.text}")
else:
    print(f"Error creando paciente: {response.text}")