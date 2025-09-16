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
    'primer_apellido': 'Migration',
    'fecha_nacimiento': '1980-01-01',
    'genero': 'F'
}
response_paciente = client.post('/pacientes/', json=datos_paciente)
print(f'Paciente creado: {response_paciente.status_code}')

if response_paciente.status_code == 201:
    paciente_id = response_paciente.json()['data'][0]['id']
    
    # Intentar crear tamizaje oncológico
    datos_tamizaje = {
        'paciente_id': paciente_id,
        'fecha_tamizaje': date.today().isoformat(),
        'tipo_tamizaje': 'Cuello Uterino',
        'resultado_tamizaje': 'Negativo'
    }
    
    response_tamizaje = client.post('/tamizaje-oncologico/', json=datos_tamizaje)
    print(f'Tamizaje response: {response_tamizaje.status_code}')
    if response_tamizaje.status_code != 201:
        print(f'Error: {response_tamizaje.text[:200]}')
    else:
        print('✅ Tamizaje creado exitosamente - Migración aplicada')
        tamizaje_id = response_tamizaje.json()['id']
        client.delete(f'/tamizaje-oncologico/{tamizaje_id}')
    
    client.delete(f'/pacientes/{paciente_id}')