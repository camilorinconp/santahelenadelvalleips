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
    'primer_apellido': 'Update',
    'fecha_nacimiento': '2020-01-15',
    'genero': 'MASCULINO'
}

print("1. Creando paciente...")
response = client.post('/pacientes/', json=paciente_data)
print(f"Paciente response: {response.status_code}")

if response.status_code == 201:
    paciente_id = response.json()['data'][0]['id']
    print(f"Paciente ID: {paciente_id}")
    
    # Crear atención
    atencion_data = {
        'paciente_id': paciente_id,
        'codigo_atencion_primera_infancia_unico': f'PI-UPDATE-{datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}',
        'fecha_atencion': '2025-09-15',
        'entorno': 'INSTITUCION_SALUD',
        'peso_kg': 12.5,
        'talla_cm': 85.0,
        'perimetro_cefalico_cm': 47.5,
        'estado_nutricional': 'NORMAL'
    }
    
    print("2. Creando atención...")
    response = client.post('/atenciones-primera-infancia/', json=atencion_data)
    print(f"Atencion creation response: {response.status_code}")
    
    if response.status_code == 201:
        atencion_id = response.json()['id']
        print(f"Atencion ID: {atencion_id}")
        
        # Actualizar
        update_data = {
            "peso_kg": 13.0,
            "talla_cm": 87.0,
            "observaciones_profesional_primera_infancia": "Desarrollo normal para la edad"
        }
        
        print("3. Actualizando atención...")
        response = client.put(f'/atenciones-primera-infancia/{atencion_id}', json=update_data)
        print(f"Update response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
    else:
        print(f"Error creando atención: {response.text}")
else:
    print(f"Error creando paciente: {response.text}")