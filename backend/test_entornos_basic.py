#!/usr/bin/env python3
"""
Test básico para endpoints de entornos de salud pública
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_entorno_salud_publica():
    """Test básico de creación de entorno"""
    
    entorno_data = {
        "codigo_identificacion_entorno_unico": f"ENT-TEST-{uuid.uuid4().hex[:8]}",
        "tipo_entorno": "ENTORNO_FAMILIAR_HOGAR_DOMESTICO",
        "nombre_descriptivo_entorno": "Entorno Test Familiar",
        "descripcion_caracterizacion_entorno": "Entorno de prueba para testing",
        "nivel_complejidad_intervencion": "BASICO_PROMOCION_PREVENCION",
        "estado_activacion": "ACTIVO_OPERATIVO",
        "departamento_ubicacion": "Valle del Cauca",
        "municipio_ubicacion": "Cali",
        "zona_territorial": "urbana",
        "poblacion_objetivo_estimada": 1000
    }
    
    response = client.post("/entornos-salud-publica/", json=entorno_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["codigo_identificacion_entorno_unico"] == entorno_data["codigo_identificacion_entorno_unico"]
    assert response_data["tipo_entorno"] == entorno_data["tipo_entorno"]
    assert response_data["nombre_descriptivo_entorno"] == entorno_data["nombre_descriptivo_entorno"]
    assert "id" in response_data
    assert "creado_en" in response_data

def test_listar_entornos_salud_publica():
    """Test básico de listado de entornos"""
    
    response = client.get("/entornos-salud-publica/")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

if __name__ == "__main__":
    print("Ejecutando tests básicos de entornos de salud pública...")
    test_crear_entorno_salud_publica()
    test_listar_entornos_salud_publica()
    print("Tests completados exitosamente!")