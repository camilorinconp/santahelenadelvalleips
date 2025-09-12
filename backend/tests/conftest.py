"""
Configuración global para todos los tests
Este archivo se ejecuta automáticamente por pytest y configura el override del service_role
para que todos los tests puedan bypass RLS sin configuración manual.
"""

import pytest
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from supabase import create_client, Client

# Importar la app principal y el dependency que queremos overridear
from main import app
from database import get_supabase_client

# --- Global Test Setup: Override Supabase client with service_role key ---

# Cargar variables de entorno
load_dotenv()

# Configuración para usar service_role en todos los tests
SUPABASE_URL = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
SUPABASE_SERVICE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
)

# Crear cliente global con service_role para bypass RLS
supabase_service_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_supabase_client_override():
    """Override function that returns service_role client instead of regular client"""
    return supabase_service_client


# Configurar el override global al inicializar los tests
def pytest_configure(config):
    """
    Configuración global de pytest que se ejecuta una vez al inicio.
    Configura el override del service_role para todos los tests.
    """
    app.dependency_overrides[get_supabase_client] = get_supabase_client_override
    print("✅ Global service_role override configured for all tests")


def pytest_unconfigure(config):
    """
    Limpieza global de pytest que se ejecuta al finalizar.
    Remueve el override para que no afecte otros procesos.
    """
    if get_supabase_client in app.dependency_overrides:
        del app.dependency_overrides[get_supabase_client]
    print("🧹 Global service_role override removed")


@pytest.fixture(scope="session")
def test_client():
    """
    Fixture que proporciona el TestClient ya configurado con service_role override.
    Scope 'session' significa que se crea una vez para toda la sesión de tests.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session") 
def service_db_client():
    """
    Fixture que proporciona acceso directo al cliente de Supabase con service_role.
    Útil para tests que necesitan manipular datos directamente.
    """
    yield supabase_service_client


# Fixture para limpiar datos de test (opcional)
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """
    Fixture que se ejecuta automáticamente en cada test para limpieza.
    autouse=True significa que se ejecuta sin necesidad de ser llamado explícitamente.
    """
    yield  # El test se ejecuta aquí
    
    # Aquí podríamos agregar lógica de limpieza si fuera necesario
    # Por ejemplo, eliminar registros de test de la base de datos
    pass


# Utilidades adicionales para tests
def create_test_uuid():
    """Utility function to generate test UUIDs"""
    from uuid import uuid4
    return str(uuid4())


def create_test_patient_data(patient_id=None):
    """Utility function to create standard test patient data"""
    if patient_id is None:
        patient_id = create_test_uuid()
    
    return {
        "id": patient_id,
        "tipo_documento": "CC",
        "numero_documento": create_test_uuid()[:9],  # Unique document number
        "primer_nombre": "Test",
        "primer_apellido": "Patient",
        "fecha_nacimiento": "1990-01-01",
        "genero": "FEMENINO",
        "telefono": "1234567890",
        "direccion": "Calle Test 123",
        "ciudad": "Cali",
        "departamento": "Valle del Cauca"
    }


# Marcar que este archivo contiene configuración global
pytest_plugins = []