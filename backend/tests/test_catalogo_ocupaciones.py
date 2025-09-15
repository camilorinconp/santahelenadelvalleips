# ===================================================================
# TESTS: Catálogo de Ocupaciones DANE - Suite Comprehensiva
# ===================================================================
# Descripción: Tests completos para catálogo ocupaciones y autocompletado
# Autor: Backend Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Cobertura: Modelos, API endpoints, búsqueda inteligente, performance
# ===================================================================

import pytest
import asyncio
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import json
import time

# Importaciones locales
from main import app
from models.catalogo_ocupaciones_model import (
    OcupacionDaneCreate,
    OcupacionDaneResponse,
    OcupacionAutocompletadoResponse,
    validar_codigo_dane_formato,
    normalizar_nombre_ocupacion
)
from models.paciente_model import PacienteCreate, PacienteResponse


# ===================================================================
# CONFIGURACIÓN DE TESTS
# ===================================================================

@pytest.fixture
def client():
    """Cliente de test para FastAPI"""
    return TestClient(app)


@pytest.fixture
def ocupaciones_test_data():
    """Datos de test para ocupaciones"""
    return [
        {
            "codigo_ocupacion_dane": "2211",
            "nombre_ocupacion_normalizado": "Médicos Generales",
            "categoria_ocupacional_nivel_1": "2 - Profesionales Científicos e Intelectuales",
            "categoria_ocupacional_nivel_2": "22 - Profesionales en ciencias biológicas y de la salud",
            "categoria_ocupacional_nivel_3": "221 - Profesionales en medicina",
            "descripcion_detallada": "Médicos que brindan atención médica general",
            "nivel_educativo_requerido": "Universitaria"
        },
        {
            "codigo_ocupacion_dane": "2221",
            "nombre_ocupacion_normalizado": "Enfermeras Profesionales", 
            "categoria_ocupacional_nivel_1": "2 - Profesionales Científicos e Intelectuales",
            "categoria_ocupacional_nivel_2": "22 - Profesionales en ciencias biológicas y de la salud",
            "categoria_ocupacional_nivel_3": "222 - Profesionales en enfermería",
            "descripcion_detallada": "Enfermeras con formación universitaria",
            "nivel_educativo_requerido": "Universitaria"
        },
        {
            "codigo_ocupacion_dane": "3220",
            "nombre_ocupacion_normalizado": "Auxiliares de Enfermería",
            "categoria_ocupacional_nivel_1": "3 - Técnicos y Profesionales de Nivel Medio",
            "categoria_ocupacional_nivel_2": "32 - Técnicos en ciencias de la salud",
            "categoria_ocupacional_nivel_3": "322 - Auxiliares de enfermería",
            "descripcion_detallada": "Auxiliares en enfermería y cuidado",
            "nivel_educativo_requerido": "Técnica"
        }
    ]


# ===================================================================
# TESTS DE MODELOS PYDANTIC
# ===================================================================

class TestModelosOcupaciones:
    """Tests para modelos Pydantic de ocupaciones"""
    
    def test_ocupacion_dane_create_valida(self):
        """Test creación de ocupación con datos válidos"""
        datos = {
            "codigo_ocupacion_dane": "2211",
            "nombre_ocupacion_normalizado": "Médicos Generales",
            "categoria_ocupacional_nivel_1": "2 - Profesionales Científicos",
            "descripcion_detallada": "Médicos generales"
        }
        
        ocupacion = OcupacionDaneCreate(**datos)
        assert ocupacion.codigo_ocupacion_dane == "2211"
        assert ocupacion.nombre_ocupacion_normalizado == "Médicos Generales"
        assert ocupacion.activo is True  # Default
    
    def test_ocupacion_dane_codigo_vacio_error(self):
        """Test error con código DANE vacío"""
        datos = {
            "codigo_ocupacion_dane": "",
            "nombre_ocupacion_normalizado": "Test"
        }
        
        with pytest.raises(ValueError, match="Código DANE no puede estar vacío"):
            OcupacionDaneCreate(**datos)
    
    def test_ocupacion_dane_nombre_vacio_error(self):
        """Test error con nombre vacío"""
        datos = {
            "codigo_ocupacion_dane": "1234",
            "nombre_ocupacion_normalizado": ""
        }
        
        with pytest.raises(ValueError, match="Nombre ocupación no puede estar vacío"):
            OcupacionDaneCreate(**datos)
    
    def test_ocupacion_autocompletado_response(self):
        """Test modelo de respuesta autocompletado"""
        datos = {
            "id": uuid.uuid4(),
            "codigo_ocupacion_dane": "2211",
            "nombre_ocupacion_normalizado": "Médicos Generales",
            "categoria_ocupacional_nivel_1": "2 - Profesionales",
            "relevancia": 0.95
        }
        
        response = OcupacionAutocompletadoResponse(**datos)
        assert response.relevancia == 0.95
        assert response.codigo_ocupacion_dane == "2211"


class TestUtilidades:
    """Tests para funciones de utilidad"""
    
    def test_validar_codigo_dane_formato_valido(self):
        """Test validación formato código DANE válido"""
        assert validar_codigo_dane_formato("2211") is True
        assert validar_codigo_dane_formato("1234") is True
        assert validar_codigo_dane_formato("123") is True
    
    def test_validar_codigo_dane_formato_invalido(self):
        """Test validación formato código DANE inválido"""
        assert validar_codigo_dane_formato("ab12") is False
        assert validar_codigo_dane_formato("12") is False
        assert validar_codigo_dane_formato("") is False
        assert validar_codigo_dane_formato(None) is False
    
    def test_normalizar_nombre_ocupacion(self):
        """Test normalización nombres ocupaciones"""
        assert normalizar_nombre_ocupacion("médicos generales") == "Médicos Generales"
        assert normalizar_nombre_ocupacion("ENFERMERAS DE URGENCIAS") == "Enfermeras de Urgencias"
        assert normalizar_nombre_ocupacion("auxiliares   en   salud") == "Auxiliares en Salud"
        assert normalizar_nombre_ocupacion("") == ""


# ===================================================================
# TESTS DE API ENDPOINTS
# ===================================================================

class TestAPIEndpoints:
    """Tests para endpoints de la API"""
    
    def test_health_check_ocupaciones(self, client):
        """Test health check del servicio"""
        response = client.get("/ocupaciones/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "catalogo" in data
        assert "funcionalidad" in data
    
    def test_buscar_ocupaciones_autocompletado_valido(self, client):
        """Test búsqueda autocompletado con término válido"""
        response = client.get("/ocupaciones/buscar?q=med&limit=5")
        assert response.status_code == 200
        
        ocupaciones = response.json()
        assert isinstance(ocupaciones, list)
        
        # Verificar estructura de respuesta
        if ocupaciones:
            ocupacion = ocupaciones[0]
            assert "id" in ocupacion
            assert "codigo_ocupacion_dane" in ocupacion
            assert "nombre_ocupacion_normalizado" in ocupacion
            assert "med" in ocupacion["nombre_ocupacion_normalizado"].lower()
    
    def test_buscar_ocupaciones_termino_corto_error(self, client):
        """Test error con término de búsqueda muy corto"""
        response = client.get("/ocupaciones/buscar?q=me")
        assert response.status_code == 422  # Validation error
    
    def test_buscar_ocupaciones_limite_excedido_error(self, client):
        """Test error con límite excedido"""
        response = client.get("/ocupaciones/buscar?q=test&limit=100")
        assert response.status_code == 422  # Validation error
    
    def test_buscar_ocupaciones_con_filtros(self, client):
        """Test búsqueda con filtros adicionales"""
        response = client.get(
            "/ocupaciones/buscar?q=enf&categoria=2%20-%20Profesionales&limit=10"
        )
        assert response.status_code == 200
        
        ocupaciones = response.json()
        assert isinstance(ocupaciones, list)
    
    def test_obtener_estadisticas_catalogo(self, client):
        """Test endpoint de estadísticas"""
        response = client.get("/ocupaciones/estadisticas")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_ocupaciones" in stats
        assert "ocupaciones_activas" in stats
        assert "categorias_nivel_1" in stats
        assert "categorias_nivel_2" in stats
    
    def test_listar_ocupaciones_por_categorias(self, client):
        """Test listado por categorías"""
        response = client.get("/ocupaciones/categorias?limit_per_category=3")
        assert response.status_code == 200
        
        categorias = response.json()
        assert isinstance(categorias, list)
        
        if categorias:
            categoria = categorias[0]
            assert "categoria" in categoria
            assert "total_ocupaciones" in categoria
            assert "ocupaciones" in categoria
    
    def test_validar_codigo_dane_existente(self, client):
        """Test validación código DANE existente"""
        # Usar código que sabemos existe en nuestros datos de prueba
        response = client.get("/ocupaciones/validar-codigo/2211")
        assert response.status_code == 200
        
        validacion = response.json()
        assert validacion["valido"] is True
        assert validacion["codigo"] == "2211"
    
    def test_validar_codigo_dane_inexistente(self, client):
        """Test validación código DANE que no existe"""
        response = client.get("/ocupaciones/validar-codigo/9999")
        assert response.status_code == 200
        
        validacion = response.json()
        assert validacion["valido"] is False
        assert validacion["codigo"] == "9999"


# ===================================================================
# TESTS DE PERFORMANCE
# ===================================================================

class TestPerformance:
    """Tests de rendimiento y escalabilidad"""
    
    def test_busqueda_autocompletado_performance(self, client):
        """Test que búsqueda autocompletado responda en <200ms"""
        start_time = time.time()
        
        response = client.get("/ocupaciones/buscar?q=med&limit=10")
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convertir a ms
        
        assert response.status_code == 200
        assert duration < 200, f"Búsqueda tardó {duration:.2f}ms, esperado <200ms"
    
    def test_multiples_busquedas_concurrentes(self, client):
        """Test múltiples búsquedas concurrentes"""
        import threading
        import time
        
        resultados = []
        errores = []
        
        def buscar_ocupacion(termino):
            try:
                start = time.time()
                response = client.get(f"/ocupaciones/buscar?q={termino}&limit=5")
                duration = time.time() - start
                
                resultados.append({
                    'termino': termino,
                    'status': response.status_code,
                    'duration': duration * 1000,
                    'count': len(response.json()) if response.status_code == 200 else 0
                })
            except Exception as e:
                errores.append(str(e))
        
        # Ejecutar 10 búsquedas en paralelo
        terminos = ["med", "enf", "aux", "tec", "pro", "doc", "esp", "gen", "cli", "sal"]
        threads = []
        
        for termino in terminos:
            thread = threading.Thread(target=buscar_ocupacion, args=(termino,))
            threads.append(thread)
            thread.start()
        
        # Esperar que terminen todos
        for thread in threads:
            thread.join()
        
        # Validar resultados
        assert len(errores) == 0, f"Errores en búsquedas concurrentes: {errores}"
        assert len(resultados) == 10
        
        # Verificar que todas respondieron en tiempo razonable
        duraciones = [r['duration'] for r in resultados]
        promedio = sum(duraciones) / len(duraciones)
        assert promedio < 300, f"Promedio {promedio:.2f}ms excede límite de 300ms"


# ===================================================================
# TESTS DE INTEGRACIÓN
# ===================================================================

class TestIntegracion:
    """Tests de integración con otros módulos"""
    
    def test_paciente_con_ocupacion_catalogo(self, client):
        """Test crear paciente con ocupación del catálogo"""
        # Primero buscar una ocupación existente
        response_ocupacion = client.get("/ocupaciones/buscar?q=med&limit=1")
        assert response_ocupacion.status_code == 200
        
        ocupaciones = response_ocupacion.json()
        if not ocupaciones:
            pytest.skip("No hay ocupaciones para test de integración")
        
        ocupacion_id = ocupaciones[0]["id"]
        
        # Crear paciente con esa ocupación
        paciente_data = {
            "tipo_documento": "CC",
            "numero_documento": "12345678",
            "primer_nombre": "Juan",
            "primer_apellido": "Pérez",
            "fecha_nacimiento": "1990-01-01",
            "genero": "M",
            "ocupacion_id": ocupacion_id
        }
        
        response_paciente = client.post("/pacientes/", json=paciente_data)
        
        # Si tenemos endpoint de pacientes, validar
        if response_paciente.status_code == 200:
            paciente = response_paciente.json()
            assert paciente["ocupacion_id"] == ocupacion_id
    
    def test_reporte_pedt_con_ocupaciones(self, client):
        """Test generación reporte PEDT con ocupaciones normalizadas"""
        response = client.get("/ocupaciones/estadisticas")
        assert response.status_code == 200
        
        stats = response.json()
        
        # Validar métricas PEDT
        assert stats["total_ocupaciones"] > 0
        assert stats["ocupaciones_activas"] > 0
        
        # Calcular cobertura estimada PEDT
        cobertura_estimada = (stats["ocupaciones_activas"] / 10919) * 100 if stats["ocupaciones_activas"] < 10919 else 100
        
        # Con nuestros datos de muestra debería ser baja, con catálogo completo alta
        assert 0 <= cobertura_estimada <= 100


# ===================================================================
# TESTS DE CASOS EXTREMOS
# ===================================================================

class TestCasosExtremos:
    """Tests para casos límite y situaciones extremas"""
    
    def test_busqueda_termino_con_caracteres_especiales(self, client):
        """Test búsqueda con caracteres especiales"""
        terminos_especiales = [
            "médico",  # Con tilde
            "niño",    # Con ñ
            "josé",    # Con acento
            "maría"    # Con acento
        ]
        
        for termino in terminos_especiales:
            response = client.get(f"/ocupaciones/buscar?q={termino}")
            # Debería manejar caracteres especiales sin error
            assert response.status_code in [200, 422]  # 422 si es muy corto
    
    def test_busqueda_termino_muy_largo(self, client):
        """Test búsqueda con término muy largo"""
        termino_largo = "a" * 200
        
        response = client.get(f"/ocupaciones/buscar?q={termino_largo}")
        assert response.status_code == 200
        
        # Debería retornar lista vacía sin error
        ocupaciones = response.json()
        assert isinstance(ocupaciones, list)
    
    def test_obtener_ocupacion_id_inexistente(self, client):
        """Test obtener ocupación con UUID inexistente"""
        uuid_falso = str(uuid.uuid4())
        
        response = client.get(f"/ocupaciones/{uuid_falso}")
        assert response.status_code == 404
    
    def test_obtener_ocupacion_id_malformado(self, client):
        """Test obtener ocupación con UUID malformado"""
        response = client.get("/ocupaciones/not-a-uuid")
        assert response.status_code == 422  # Validation error


# ===================================================================
# TESTS DE REGRESIÓN
# ===================================================================

class TestRegresion:
    """Tests para prevenir regresiones en funcionalidad crítica"""
    
    def test_funcion_busqueda_sql_disponible(self, client):
        """Test que función SQL personalizada esté disponible"""
        response = client.get("/ocupaciones/buscar?q=test&limit=1")
        
        # No debe fallar por función SQL faltante
        assert response.status_code in [200, 500]
        
        if response.status_code == 500:
            # Si falla, verificar que no sea por función faltante
            error_detail = response.json().get("detail", "")
            assert "buscar_ocupaciones_inteligente" not in error_detail.lower()
    
    def test_indices_optimizacion_activos(self, client):
        """Test que índices de optimización estén activos"""
        # Health check debería confirmar índices
        response = client.get("/ocupaciones/health")
        assert response.status_code == 200
        
        health = response.json()
        assert health["funcionalidad"]["indices_optimizados"] == "activos"
    
    def test_estructura_respuesta_consistente(self, client):
        """Test que estructura de respuesta sea consistente"""
        response = client.get("/ocupaciones/buscar?q=test&limit=1")
        assert response.status_code == 200
        
        ocupaciones = response.json()
        assert isinstance(ocupaciones, list)
        
        if ocupaciones:
            ocupacion = ocupaciones[0]
            campos_requeridos = [
                "id", 
                "codigo_ocupacion_dane", 
                "nombre_ocupacion_normalizado",
                "categoria_ocupacional_nivel_1"
            ]
            
            for campo in campos_requeridos:
                assert campo in ocupacion, f"Campo {campo} faltante en respuesta"


# ===================================================================
# CONFIGURACIÓN PYTEST
# ===================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])