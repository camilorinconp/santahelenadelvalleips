#!/usr/bin/env python3

from fastapi.testclient import TestClient
from main import app
from datetime import datetime
import random

client = TestClient(app)

# Test creating a patient first
paciente_data = {
    'tipo_documento': 'CC',
    'numero_documento': str(random.randint(1000000000, 9999999999)),
    'primer_nombre': 'Test',
    'primer_apellido': 'PrimeraInfancia',
    'fecha_nacimiento': '2020-01-15',
    'genero': 'MASCULINO'
}

response = client.post('/pacientes/', json=paciente_data)
print('Paciente response:', response.status_code)

if response.status_code == 201:
    paciente_id = response.json()['data'][0]['id']
    print('Paciente ID:', paciente_id)
    
    # Test creating atencion
    atencion_data = {
        'paciente_id': paciente_id,
        'codigo_atencion_primera_infancia_unico': f'PI-TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}-{random.randint(1000, 9999)}',
        'fecha_atencion': '2025-09-15',
        'entorno': 'INSTITUCION_SALUD',
        'peso_kg': 12.5,
        'talla_cm': 85.0,
        'perimetro_cefalico_cm': 47.5,
        'estado_nutricional': 'NORMAL'
    }
    
    response = client.post('/atenciones-primera-infancia/', json=atencion_data)
    print('Atencion response:', response.status_code)
    if response.status_code != 201:
        print('Error:', response.text)
    else:
        print('✅ Test manual exitoso - Primera Infancia consolidada funcional')
else:
    print('Error paciente:', response.text)