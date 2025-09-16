from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from datetime import date

client = TestClient(app)

# Crear paciente de prueba
datos_paciente = {
    'tipo_documento': 'CC',
    'numero_documento': str(uuid4())[:10],
    'primer_nombre': 'Test',
    'primer_apellido': 'Legacy',
    'fecha_nacimiento': '1980-01-01',
    'genero': 'F'
}
response_paciente = client.post('/pacientes/', json=datos_paciente)
print(f'Paciente creado: {response_paciente.status_code}')

if response_paciente.status_code == 201:
    paciente_id = response_paciente.json()['data'][0]['id']
    
    # Intentar usar endpoint legacy que funcionó en tests
    datos_legacy = {
        'paciente_id': paciente_id,
        'fecha_tamizaje': date.today().isoformat(),
        'tipo_tamizaje': 'Citología',  # Este era el tipo en el test anterior
        'resultado': 'Negativo para lesión intraepitelial o malignidad'
    }
    
    response_legacy = client.post('/tamizaje-oncologico/tamizajes-oncologicos/', json=datos_legacy)
    print(f'Legacy endpoint response: {response_legacy.status_code}')
    if response_legacy.status_code != 201:
        print(f'Error legacy: {response_legacy.text[:200]}')
    else:
        print('✅ Endpoint legacy funcionando!')
        tamizaje_id = response_legacy.json()['id']
        print(f'Tamizaje creado con ID: {tamizaje_id}')
        client.delete(f'/tamizaje-oncologico/{tamizaje_id}')
    
    client.delete(f'/pacientes/{paciente_id}')