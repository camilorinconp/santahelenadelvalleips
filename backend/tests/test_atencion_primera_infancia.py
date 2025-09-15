# =============================================================================
# Tests Consolidados Atención Primera Infancia - Arquitectura Vertical
# Tests independientes sin dependencias cruzadas
# Fecha: 15 septiembre 2025
# =============================================================================

import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date, datetime
from uuid import uuid4
import random

client = TestClient(app)

# =============================================================================
# FIXTURES Y UTILIDADES
# =============================================================================

def generar_numero_documento_unico():
    """Generar número de documento único para tests."""
    return str(random.randint(1000000000, 9999999999))

def crear_paciente_test(numero_documento: str = None):
    """Crear paciente de prueba y retornar su ID."""
    if numero_documento is None:
        numero_documento = generar_numero_documento_unico()
    
    paciente_data = {
        "tipo_documento": "CC",
        "numero_documento": numero_documento,
        "primer_nombre": "Test",
        "primer_apellido": "PrimeraInfancia",
        "fecha_nacimiento": "2020-01-15",
        "genero": "MASCULINO"
    }
    
    response = client.post("/pacientes/", json=paciente_data)
    assert response.status_code == 201
    
    return response.json()["data"][0]["id"]

def crear_atencion_test_data(paciente_id: str):
    """Crear datos de atención de test."""
    return {
        "paciente_id": paciente_id,
        "codigo_atencion_primera_infancia_unico": f"PI-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}",
        "fecha_atencion": date.today().isoformat(),
        "entorno": "INSTITUCION_SALUD",
        "peso_kg": 12.5,
        "talla_cm": 85.0,
        "perimetro_cefalico_cm": 47.5,
        "estado_nutricional": "NORMAL"
    }

# =============================================================================
# TESTS CRUD BÁSICO
# =============================================================================

class TestAtencionPrimeraInfanciaConsolidada:
    """Suite de tests para funcionalidad consolidada de Primera Infancia."""
    
    def test_crear_atencion_basica(self):
        """Test crear atención Primera Infancia básica."""
        # Crear paciente independiente
        paciente_id = crear_paciente_test()
        
        # Crear atención
        atencion_data = crear_atencion_test_data(paciente_id)
        
        response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["paciente_id"] == paciente_id
        assert data["peso_kg"] == 12.5
        assert data["talla_cm"] == 85.0
        assert data["estado_nutricional"] == "NORMAL"
        
        # Verificar campos calculados
        assert "desarrollo_apropiado_edad" in data
        assert "porcentaje_esquema_vacunacion" in data
        assert "proxima_consulta_recomendada_dias" in data
    
    def test_obtener_atencion_por_id(self):
        """Test obtener atención por ID."""
        # Crear paciente y atención independientes
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Obtener por ID
        response = client.get(f"/atenciones-primera-infancia/{atencion_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == atencion_id
        assert data["paciente_id"] == paciente_id
    
    def test_listar_atenciones(self):
        """Test listar atenciones con filtros."""
        response = client.get("/atenciones-primera-infancia/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_listar_atenciones_por_paciente(self):
        """Test listar atenciones filtradas por paciente."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        
        # Listar por paciente
        response = client.get(f"/atenciones-primera-infancia/?paciente_id={paciente_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 1
        assert all(atencion["paciente_id"] == paciente_id for atencion in data)
    
    def test_actualizar_atencion(self):
        """Test actualizar atención."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Actualizar
        update_data = {
            "peso_kg": 13.0,
            "talla_cm": 87.0,
            "observaciones_profesional_primera_infancia": "Desarrollo normal para la edad"
        }
        
        response = client.put(f"/atenciones-primera-infancia/{atencion_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["peso_kg"] == 13.0
        assert data["talla_cm"] == 87.0
        assert "Desarrollo normal" in data["observaciones_profesional_primera_infancia"]
    
    def test_eliminar_atencion(self):
        """Test eliminar atención."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Eliminar
        response = client.delete(f"/atenciones-primera-infancia/{atencion_id}")
        assert response.status_code == 204
        
        # Verificar que no existe
        get_response = client.get(f"/atenciones-primera-infancia/{atencion_id}")
        assert get_response.status_code == 404

# =============================================================================
# TESTS FUNCIONALIDAD ESPECIALIZADA
# =============================================================================

class TestEAD3ASQ3Consolidado:
    """Tests para aplicación de EAD-3 y ASQ-3 básicos."""
    
    def test_aplicar_ead3_basico(self):
        """Test aplicar EAD-3 básico."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Aplicar EAD-3
        datos_ead3 = {
            "ead3_motricidad_gruesa_puntaje": 75,
            "ead3_motricidad_fina_puntaje": 80,
            "ead3_audicion_lenguaje_puntaje": 70,
            "ead3_personal_social_puntaje": 85
        }
        
        response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/ead3", json=datos_ead3)
        assert response.status_code == 200
        
        data = response.json()
        assert data["ead3_aplicada"] == True
        assert data["ead3_puntaje_total"] == 310  # Suma de puntajes
        assert data["fecha_aplicacion_ead3"] is not None
        assert data["desarrollo_apropiado_edad"] == True  # 310 > 200
    
    def test_aplicar_ead3_validaciones(self):
        """Test validaciones EAD-3."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Test puntaje fuera de rango
        datos_ead3_invalidos = {
            "ead3_motricidad_gruesa_puntaje": 150,  # Fuera de rango
            "ead3_motricidad_fina_puntaje": 80,
            "ead3_audicion_lenguaje_puntaje": 70,
            "ead3_personal_social_puntaje": 85
        }
        
        response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/ead3", json=datos_ead3_invalidos)
        assert response.status_code == 400
        response_data = response.json()
        # Adaptado al formato de error personalizado
        error_message = response_data.get("error", {}).get("message", "")
        assert "debe estar entre 0 y 100" in error_message
        
        # Test campo faltante
        datos_ead3_incompletos = {
            "ead3_motricidad_gruesa_puntaje": 75,
            "ead3_motricidad_fina_puntaje": 80
            # Faltan campos requeridos
        }
        
        response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/ead3", json=datos_ead3_incompletos)
        assert response.status_code == 400
        response_data = response.json()
        error_message = response_data.get("error", {}).get("message", "")
        assert "Campo requerido faltante" in error_message
    
    def test_aplicar_asq3_basico(self):
        """Test aplicar ASQ-3 básico."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_test_data(paciente_id)
        
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # Aplicar ASQ-3
        datos_asq3 = {
            "asq3_comunicacion_puntaje": 45,
            "asq3_motor_grueso_puntaje": 50,
            "asq3_motor_fino_puntaje": 40,
            "asq3_resolucion_problemas_puntaje": 55,
            "asq3_personal_social_puntaje": 48
        }
        
        response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/asq3", json=datos_asq3)
        assert response.status_code == 200
        
        data = response.json()
        assert data["asq3_aplicado"] == True
        assert data["asq3_comunicacion_puntaje"] == 45
        assert data["fecha_aplicacion_asq3"] is not None

# =============================================================================
# TESTS ESTADÍSTICAS Y FUNCIONALIDAD AUXILIAR
# =============================================================================

class TestEstadisticasConsolidadas:
    """Tests para estadísticas básicas."""
    
    def test_estadisticas_basicas(self):
        """Test endpoint de estadísticas básicas."""
        response = client.get("/atenciones-primera-infancia/estadisticas/basicas")
        assert response.status_code == 200
        
        data = response.json()
        assert "resumen_general" in data
        assert "total_atenciones" in data["resumen_general"]
        assert "porcentaje_ead3_aplicada" in data["resumen_general"]
        assert "porcentaje_asq3_aplicado" in data["resumen_general"]
        assert "porcentaje_vacunacion_completa" in data["resumen_general"]
        assert "fecha_calculo" in data

# =============================================================================
# TESTS CASOS EDGE Y ERRORES
# =============================================================================

class TestCasosEdgeConsolidados:
    """Tests para casos edge y manejo de errores."""
    
    def test_atencion_no_encontrada(self):
        """Test manejar atención no encontrada."""
        atencion_id_falso = str(uuid4())
        
        response = client.get(f"/atenciones-primera-infancia/{atencion_id_falso}")
        assert response.status_code == 404
        response_data = response.json()
        error_message = response_data.get("error", {}).get("message", "")
        assert "no encontrada" in error_message
    
    def test_crear_atencion_paciente_inexistente(self):
        """Test crear atención con paciente inexistente."""
        paciente_id_falso = str(uuid4())
        atencion_data = crear_atencion_test_data(paciente_id_falso)
        
        response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        # Debe fallar por foreign key constraint
        assert response.status_code == 400
    
    def test_aplicar_ead3_atencion_inexistente(self):
        """Test aplicar EAD-3 a atención inexistente."""
        atencion_id_falso = str(uuid4())
        
        datos_ead3 = {
            "ead3_motricidad_gruesa_puntaje": 75,
            "ead3_motricidad_fina_puntaje": 80,
            "ead3_audicion_lenguaje_puntaje": 70,
            "ead3_personal_social_puntaje": 85
        }
        
        response = client.patch(f"/atenciones-primera-infancia/{atencion_id_falso}/ead3", json=datos_ead3)
        assert response.status_code == 404
        response_data = response.json()
        error_message = response_data.get("error", {}).get("message", "")
        assert "no encontrada" in error_message

# =============================================================================
# TESTS FUNCIONALIDAD INTEGRADA
# =============================================================================

class TestFuncionalidadIntegrada:
    """Tests para funcionalidad completa integrada."""
    
    def test_flujo_completo_atencion(self):
        """Test flujo completo de atención Primera Infancia."""
        # 1. Crear paciente
        paciente_id = crear_paciente_test()
        
        # 2. Crear atención básica
        atencion_data = crear_atencion_test_data(paciente_id)
        create_response = client.post("/atenciones-primera-infancia/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]
        
        # 3. Aplicar EAD-3
        datos_ead3 = {
            "ead3_motricidad_gruesa_puntaje": 75,
            "ead3_motricidad_fina_puntaje": 80,
            "ead3_audicion_lenguaje_puntaje": 70,
            "ead3_personal_social_puntaje": 85
        }
        ead3_response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/ead3", json=datos_ead3)
        assert ead3_response.status_code == 200
        
        # 4. Aplicar ASQ-3
        datos_asq3 = {
            "asq3_comunicacion_puntaje": 45,
            "asq3_motor_grueso_puntaje": 50,
            "asq3_motor_fino_puntaje": 40,
            "asq3_resolucion_problemas_puntaje": 55,
            "asq3_personal_social_puntaje": 48
        }
        asq3_response = client.patch(f"/atenciones-primera-infancia/{atencion_id}/asq3", json=datos_asq3)
        assert asq3_response.status_code == 200
        
        # 5. Actualizar datos adicionales
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
        assert update_response.status_code == 200
        
        # 6. Verificar estado final
        final_response = client.get(f"/atenciones-primera-infancia/{atencion_id}")
        assert final_response.status_code == 200
        
        final_data = final_response.json()
        assert final_data["ead3_aplicada"] == True
        assert final_data["asq3_aplicado"] == True
        assert final_data["esquema_vacunacion_completo"] == True
        assert final_data["desarrollo_apropiado_edad"] == True
        assert final_data["porcentaje_esquema_vacunacion"] == 100.0
        assert "rutinario" in final_data["observaciones_profesional_primera_infancia"]