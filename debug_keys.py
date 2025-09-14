import os
from dotenv import load_dotenv
import json
import base64

load_dotenv()

def decode_jwt_payload(token):
    try:
        parts = token.split('.')
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except:
        return None

main_key = os.getenv('SUPABASE_KEY')
service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

print('=== ANÁLISIS DE TOKENS ===')
main_payload = decode_jwt_payload(main_key)
service_payload = decode_jwt_payload(service_key)

if main_payload:
    print('MAIN KEY - iss:', main_payload.get('iss'), 'role:', main_payload.get('role'))
if service_payload:
    print('SERVICE KEY - iss:', service_payload.get('iss'), 'role:', service_payload.get('role'))

print()
if main_payload and service_payload:
    if main_payload.get('iss') != service_payload.get('iss'):
        print('❌ PROBLEMA: Las claves pertenecen a proyectos diferentes')
        print(f'  Main key proyecto: {main_payload.get("iss")}')
        print(f'  Service key proyecto: {service_payload.get("iss")}')
    else:
        print('✅ Las claves pertenecen al mismo proyecto')