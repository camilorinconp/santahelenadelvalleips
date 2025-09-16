# =============================================================================
# Tests Atención Adolescencia y Juventud - Suite Completa
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.3 y 3.3.4
# =============================================================================

import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_adolescencia = None
paciente_id_test_juventud = None
atencion_adolescencia_id_test = None
atencion_juventud_id_test = None
atencion_riesgo_alto_id = None

# =============================================================================
# SETUP Y TEARDOWN
# =============================================================================

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_adolescencia_test_data():
    """Setup: Crea pacientes de 16 y 24 años para las pruebas. Teardown: los elimina."""
    global paciente_id_test_adolescencia, paciente_id_test_juventud
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente adolescente (16 años)
    fecha_nacimiento_adolescente = date.today() - timedelta(days=16 * 365)
    datos_paciente_adolescente = {
        "tipo_documento": "TI",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Carlos",
        "primer_apellido": "Adolescente_Test",
        "fecha_nacimiento": fecha_nacimiento_adolescente.isoformat(),
        "genero": "M"
    }
    response_paciente_adol = client.post("/pacientes/", json=datos_paciente_adolescente)
    assert response_paciente_adol.status_code == 201, response_paciente_adol.text
    paciente_id_test_adolescencia = response_paciente_adol.json()["data"][0]["id"]

    # Crear Paciente joven (24 años)
    fecha_nacimiento_joven = date.today() - timedelta(days=24 * 365)
    datos_paciente_joven = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10], 
        "primer_nombre": "Ana",
        "primer_apellido": "Juventud_Test",
        "fecha_nacimiento": fecha_nacimiento_joven.isoformat(),
        "genero": "F"
    }
    response_paciente_joven = client.post("/pacientes/", json=datos_paciente_joven)
    assert response_paciente_joven.status_code == 201, response_paciente_joven.text
    paciente_id_test_juventud = response_paciente_joven.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    
    # Eliminar atenciones creadas
    test_ids = [atencion_adolescencia_id_test, atencion_juventud_id_test, atencion_riesgo_alto_id]
    for atencion_id in test_ids:
        if atencion_id:
            db_client.table("atencion_adolescencia").delete().eq("id", atencion_id).execute()
    
    # Eliminar pacientes de prueba
    if paciente_id_test_adolescencia:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_adolescencia).execute()
    if paciente_id_test_juventud:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_juventud).execute()

# =============================================================================
# GRUPO 1: TESTS CRUD BÁSICOS
# =============================================================================

class TestCRUDBasico:
    """Suite de tests para operaciones CRUD básicas"""

    def test_crear_atencion_adolescencia_exitosa(self):
        """Test crear atención adolescencia con datos válidos"""
        global atencion_adolescencia_id_test
        
        datos_atencion = {
            "paciente_id": paciente_id_test_adolescencia,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 16,
            "peso_kg": 60.5,
            "talla_cm": 165.0,
            "presion_sistolica": 110.0,
            "presion_diastolica": 70.0,
            "frecuencia_cardiaca": 75,
            "autoestima": 7,
            "habilidades_sociales": 8,
            "proyecto_vida": "EN_CONSTRUCCION",
            "problemas_conductuales": False,
            "salud_sexual_reproductiva": "NORMAL",
            "salud_mental": "NORMAL",
            "episodios_depresivos": False,
            "ansiedad_clinica": False,
            "consumo_sustancias": "SIN_CONSUMO",
            "trastorno_alimentario": "SIN_RIESGO",
            "antecedentes_familiares_cardiovasculares": False,
            "fumador": False,
            "sedentarismo": True,
            "familia_funcional": True,
            "rendimiento_academico": "ALTO",
            "actividad_fisica_regular": False,
            "red_apoyo_social": True,
            "observaciones_generales": "Adolescente con buen estado general",
            "entorno": "CONSULTA_EXTERNA"
        }
        
        response = client.post("/atencion-adolescencia/", json=datos_atencion)
        assert response.status_code == 201, response.text
        
        data = response.json()
        atencion_adolescencia_id_test = data["id"]
        
        # Verificar campos básicos
        assert data["edad_anos"] == 16
        assert data["peso_kg"] == 60.5
        assert data["talla_cm"] == 165.0
        assert data["proyecto_vida"] == "EN_CONSTRUCCION"
        
        # Verificar campos calculados automáticamente
        assert "imc" in data
        assert data["imc"] == pytest.approx(22.22, abs=0.01)
        assert "estado_nutricional" in data
        assert "riesgo_cardiovascular_temprano" in data
        assert "desarrollo_psicosocial_apropiado" in data
        assert "factores_protectores_identificados" in data
        assert "nivel_riesgo_integral" in data
        assert "proxima_consulta_recomendada_dias" in data
        assert "completitud_evaluacion" in data
        
        # Verificar metadatos
        assert "created_at" in data
        assert "updated_at" in data
        assert data["atencion_id"] is not None

    def test_crear_atencion_juventud_exitosa(self):
        """Test crear atención juventud con datos válidos"""
        global atencion_juventud_id_test
        
        datos_atencion = {
            "paciente_id": paciente_id_test_juventud,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 24,
            "peso_kg": 65.0,
            "talla_cm": 160.0,
            "presion_sistolica": 115.0,
            "presion_diastolica": 75.0,
            "frecuencia_cardiaca": 70,
            "autoestima": 8,
            "habilidades_sociales": 7,
            "proyecto_vida": "DEFINIDO",
            "problemas_conductuales": False,
            "salud_sexual_reproductiva": "NORMAL",
            "inicio_vida_sexual": True,
            "uso_anticonceptivos": True,
            "salud_mental": "NORMAL",
            "episodios_depresivos": False,
            "ansiedad_clinica": False,
            "consumo_sustancias": "SIN_CONSUMO",
            "trastorno_alimentario": "SIN_RIESGO",
            "antecedentes_familiares_cardiovasculares": False,
            "fumador": False,
            "sedentarismo": False,
            "familia_funcional": True,
            "rendimiento_academico": "SUPERIOR",
            "actividad_fisica_regular": True,
            "red_apoyo_social": True,
            "entorno": "CONSULTA_EXTERNA"
        }
        
        response = client.post("/atencion-adolescencia/", json=datos_atencion)
        assert response.status_code == 201, response.text
        
        data = response.json()
        atencion_juventud_id_test = data["id"]
        
        # Verificar cálculos específicos para jóvenes
        assert data["edad_anos"] == 24
        assert len(data["factores_protectores_identificados"]) >= 4  # Debería tener muchos factores protectores
        assert data["nivel_riesgo_integral"] == "BAJO"  # Con tantos factores protectores

    def test_obtener_atencion_por_id(self):
        """Test obtener atención existente por ID"""
        response = client.get(f"/atencion-adolescencia/{atencion_adolescencia_id_test}")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert data["id"] == atencion_adolescencia_id_test
        assert data["edad_anos"] == 16
        assert "factores_protectores_identificados" in data

    def test_actualizar_atencion_adolescencia(self):
        """Test actualizar atención existente"""
        datos_actualizacion = {
            "autoestima": 9,
            "proyecto_vida": "DEFINIDO",
            "actividad_fisica_regular": True,
            "observaciones_generales": "Mejora notable en autoestima y proyecto de vida"
        }
        
        response = client.put(f"/atencion-adolescencia/{atencion_adolescencia_id_test}", json=datos_actualizacion)
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert data["autoestima"] == 9
        assert data["proyecto_vida"] == "DEFINIDO"
        assert data["actividad_fisica_regular"] == True
        
        # Verificar que campos calculados se actualizaron
        assert len(data["factores_protectores_identificados"]) > 0

    def test_eliminar_atencion_adolescencia(self):
        """Test eliminar atención (soft delete)"""
        # Crear atención temporal para eliminar
        datos_temp = {
            "paciente_id": paciente_id_test_adolescencia,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 16,
            "peso_kg": 55.0,
            "talla_cm": 160.0,
            "presion_sistolica": 105.0,
            "presion_diastolica": 65.0,
            "frecuencia_cardiaca": 80,
            "autoestima": 6,
            "habilidades_sociales": 6,
            "proyecto_vida": "EN_CONSTRUCCION",
            "problemas_conductuales": False,
            "salud_sexual_reproductiva": "NORMAL",
            "salud_mental": "NORMAL",
            "episodios_depresivos": False,
            "ansiedad_clinica": False,
            "consumo_sustancias": "SIN_CONSUMO",
            "trastorno_alimentario": "SIN_RIESGO",
            "antecedentes_familiares_cardiovasculares": False,
            "fumador": False,
            "sedentarismo": True,
            "familia_funcional": True,
            "rendimiento_academico": "BASICO",
            "actividad_fisica_regular": False,
            "red_apoyo_social": True
        }
        
        response_create = client.post("/atencion-adolescencia/", json=datos_temp)
        temp_id = response_create.json()["id"]
        
        # Eliminar
        response_delete = client.delete(f"/atencion-adolescencia/{temp_id}")
        assert response_delete.status_code == 204
        
        # Verificar que ya no existe
        response_get = client.get(f"/atencion-adolescencia/{temp_id}")
        assert response_get.status_code == 404

# =============================================================================
# GRUPO 2: TESTS ENDPOINTS ESPECIALIZADOS
# =============================================================================

class TestEndpointsEspecializados:
    """Suite de tests para endpoints especializados"""

    def test_listar_atenciones_con_filtros(self):
        """Test listar atenciones con filtros de edad"""
        response = client.get("/atencion-adolescencia/?edad_minima=15&edad_maxima=18")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)
        
        # Verificar que todas las edades están en el rango
        for atencion in data:
            assert 15 <= atencion["edad_anos"] <= 18

    def test_obtener_por_rango_edad(self):
        """Test obtener atenciones por rango específico de edad"""
        response = client.get("/atencion-adolescencia/por-rango-edad/16/20")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)
        
        for atencion in data:
            assert 16 <= atencion["edad_anos"] <= 20

    def test_obtener_atenciones_cronologicas_paciente(self):
        """Test obtener historial cronológico de un paciente"""
        response = client.get(f"/atencion-adolescencia/paciente/{paciente_id_test_adolescencia}/cronologicas")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # Al menos la atención creada en los tests
        
        # Verificar que todas son del mismo paciente
        for atencion in data:
            assert atencion["paciente_id"] == paciente_id_test_adolescencia

    def test_obtener_por_nivel_riesgo(self):
        """Test obtener atenciones por nivel de riesgo específico"""
        response = client.get("/atencion-adolescencia/por-nivel-riesgo/BAJO")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)
        
        # Todas deben tener nivel de riesgo BAJO
        for atencion in data:
            assert atencion["nivel_riesgo_integral"] == "BAJO"

# =============================================================================
# GRUPO 3: TESTS ESTADÍSTICAS Y REPORTES
# =============================================================================

class TestEstadisticasReportes:
    """Suite de tests para estadísticas y reportes"""

    def test_obtener_estadisticas_basicas(self):
        """Test obtener estadísticas básicas del módulo"""
        response = client.get("/atencion-adolescencia/estadisticas/basicas?dias_atras=30")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert "total_atenciones" in data
        assert "distribuciones" in data
        assert "promedios" in data
        assert "alertas" in data
        
        # Verificar estructura de distribuciones
        distribuciones = data["distribuciones"]
        assert "por_edad" in distribuciones
        assert "por_estado_nutricional" in distribuciones
        assert "por_nivel_riesgo" in distribuciones
        assert "por_desarrollo_psicosocial" in distribuciones
        assert "por_salud_mental" in distribuciones
        
        # Verificar promedios
        promedios = data["promedios"]
        assert "edad_anos" in promedios
        assert "imc" in promedios
        assert "autoestima" in promedios
        assert "factores_protectores_promedio" in promedios

    def test_generar_reporte_desarrollo_psicosocial(self):
        """Test generar reporte especializado de desarrollo psicosocial"""
        response = client.get("/atencion-adolescencia/reportes/desarrollo-psicosocial?dias_atras=90")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert "adolescentes_evaluados" in data
        assert "desarrollo_apropiado" in data
        assert "factores_riesgo_prevalentes" in data
        assert "factores_protectores_prevalentes" in data
        assert "recomendaciones" in data
        
        # Verificar estructura de factores de riesgo
        assert isinstance(data["factores_riesgo_prevalentes"], list)
        if data["factores_riesgo_prevalentes"]:
            factor_riesgo = data["factores_riesgo_prevalentes"][0]
            assert "factor" in factor_riesgo
            assert "casos" in factor_riesgo
            assert "porcentaje" in factor_riesgo
        
        # Verificar recomendaciones
        assert isinstance(data["recomendaciones"], list)

    def test_obtener_alertas_riesgo_alto(self):
        """Test obtener adolescentes con alertas de riesgo alto"""
        response = client.get("/atencion-adolescencia/alertas/riesgo-alto")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)
        
        # Verificar que solo incluye riesgo alto o superior
        for atencion in data:
            assert atencion["nivel_riesgo_integral"] in ["ALTO", "MUY_ALTO", "CRITICO"]

# =============================================================================
# GRUPO 4: TESTS CASOS EDGE Y VALIDACIONES
# =============================================================================

class TestCasosEdge:
    """Suite de tests para casos edge y validaciones"""

    def test_crear_atencion_datos_invalidos_edad(self):
        """Test crear atención con edad inválida"""
        datos_invalidos = {
            "paciente_id": paciente_id_test_adolescencia,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 10,  # Edad inválida para adolescencia
            "peso_kg": 60.0,
            "talla_cm": 165.0,
            "presion_sistolica": 110.0,
            "presion_diastolica": 70.0,
            "frecuencia_cardiaca": 75,
            "autoestima": 7,
            "habilidades_sociales": 8,
            "proyecto_vida": "EN_CONSTRUCCION",
            "problemas_conductuales": False,
            "salud_sexual_reproductiva": "NORMAL",
            "salud_mental": "NORMAL",
            "episodios_depresivos": False,
            "ansiedad_clinica": False,
            "consumo_sustancias": "SIN_CONSUMO",
            "trastorno_alimentario": "SIN_RIESGO",
            "antecedentes_familiares_cardiovasculares": False,
            "fumador": False,
            "sedentarismo": True,
            "familia_funcional": True,
            "rendimiento_academico": "BASICO",
            "actividad_fisica_regular": False,
            "red_apoyo_social": True
        }
        
        response = client.post("/atencion-adolescencia/", json=datos_invalidos)
        assert response.status_code == 422  # Validation error

    def test_crear_atencion_presion_arterial_invalida(self):
        """Test crear atención con presión arterial inconsistente"""
        datos_invalidos = {
            "paciente_id": paciente_id_test_adolescencia,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 16,
            "peso_kg": 60.0,
            "talla_cm": 165.0,
            "presion_sistolica": 70.0,  # Menor que diastólica
            "presion_diastolica": 110.0,  # Mayor que sistólica
            "frecuencia_cardiaca": 75,
            "autoestima": 7,
            "habilidades_sociales": 8,
            "proyecto_vida": "EN_CONSTRUCCION",
            "problemas_conductuales": False,
            "salud_sexual_reproductiva": "NORMAL",
            "salud_mental": "NORMAL",
            "episodios_depresivos": False,
            "ansiedad_clinica": False,
            "consumo_sustancias": "SIN_CONSUMO",
            "trastorno_alimentario": "SIN_RIESGO",
            "antecedentes_familiares_cardiovasculares": False,
            "fumador": False,
            "sedentarismo": True,
            "familia_funcional": True,
            "rendimiento_academico": "BASICO",
            "actividad_fisica_regular": False,
            "red_apoyo_social": True
        }
        
        response = client.post("/atencion-adolescencia/", json=datos_invalidos)
        assert response.status_code in [422, 500]  # Error de validación o server

    def test_obtener_atencion_no_existente(self):
        """Test obtener atención con ID inexistente"""
        id_inexistente = str(uuid4())
        response = client.get(f"/atencion-adolescencia/{id_inexistente}")
        assert response.status_code == 404

    def test_actualizar_atencion_no_existente(self):
        """Test actualizar atención inexistente"""
        id_inexistente = str(uuid4())
        datos_update = {"autoestima": 8}
        
        response = client.put(f"/atencion-adolescencia/{id_inexistente}", json=datos_update)
        assert response.status_code == 404

    def test_rango_edad_invalido(self):
        """Test rango de edad inválido (inicio > fin)"""
        response = client.get("/atencion-adolescencia/por-rango-edad/25/15")  # Rango inválido
        assert response.status_code == 400

# =============================================================================
# GRUPO 5: TESTS FUNCIONALIDAD INTEGRADA
# =============================================================================

class TestFuncionalidadIntegrada:
    """Suite de tests para funcionalidad completa integrada"""

    def test_crear_atencion_riesgo_alto(self):
        """Test crear atención de adolescente con múltiples factores de riesgo"""
        global atencion_riesgo_alto_id
        
        datos_riesgo_alto = {
            "paciente_id": paciente_id_test_adolescencia,
            "medico_id": str(uuid4()),
            "fecha_atencion": date.today().isoformat(),
            "edad_anos": 17,
            "peso_kg": 90.0,  # Obesidad
            "talla_cm": 165.0,
            "presion_sistolica": 145.0,  # Hipertensión
            "presion_diastolica": 95.0,
            "frecuencia_cardiaca": 85,
            "autoestima": 3,  # Baja autoestima
            "habilidades_sociales": 3,  # Pocas habilidades sociales
            "proyecto_vida": "AUSENTE",  # Sin proyecto de vida
            "problemas_conductuales": True,  # Problemas conductuales
            "salud_sexual_reproductiva": "REQUIERE_CONSEJERIA",
            "inicio_vida_sexual": True,
            "uso_anticonceptivos": False,  # Riesgo reproductivo
            "salud_mental": "SINTOMAS_SEVEROS",  # Problemas graves salud mental
            "episodios_depresivos": True,
            "ansiedad_clinica": True,
            "consumo_sustancias": "CONSUMO_HABITUAL",  # Consumo problemático
            "tipo_sustancias": "Alcohol y marihuana",
            "trastorno_alimentario": "RIESGO_ALTO",
            "relacion_comida": "Episodios de atracón frecuentes",
            "antecedentes_familiares_cardiovasculares": True,
            "fumador": True,  # Múltiples factores de riesgo CV
            "sedentarismo": True,
            "familia_funcional": False,  # Familia disfuncional
            "rendimiento_academico": "BAJO",
            "actividad_fisica_regular": False,
            "red_apoyo_social": False,  # Sin apoyo social
            "observaciones_generales": "Adolescente con múltiples factores de riesgo. Requiere intervención multidisciplinaria urgente.",
            "plan_intervencion": "1. Referencia psicología urgente 2. Consejería nutricional 3. Programa de cessación tabáquica 4. Seguimiento cada 15 días"
        }
        
        response = client.post("/atencion-adolescencia/", json=datos_riesgo_alto)
        assert response.status_code == 201, response.text
        
        data = response.json()
        atencion_riesgo_alto_id = data["id"]
        
        # Verificar cálculos de riesgo alto
        assert data["imc"] > 30  # Obesidad
        assert data["estado_nutricional"] in ["OBESIDAD_GRADO_I", "OBESIDAD_GRADO_II", "OBESIDAD_GRADO_III"]
        assert data["riesgo_cardiovascular_temprano"] in ["ALTO", "MUY_ALTO"]
        assert data["desarrollo_psicosocial_apropiado"] in ["RIESGO_ALTO", "REQUIERE_INTERVENCION"]
        assert data["nivel_riesgo_integral"] in ["MUY_ALTO", "CRITICO"]
        assert data["proxima_consulta_recomendada_dias"] <= 30  # Seguimiento frecuente
        assert len(data["factores_protectores_identificados"]) == 0  # Sin factores protectores

    def test_flujo_completo_adolescente_mejoria(self):
        """Test flujo completo: adolescente de riesgo alto que mejora con seguimiento"""
        # Obtener atención de riesgo alto
        response_inicial = client.get(f"/atencion-adolescencia/{atencion_riesgo_alto_id}")
        assert response_inicial.status_code == 200
        
        data_inicial = response_inicial.json()
        nivel_riesgo_inicial = data_inicial["nivel_riesgo_integral"]
        
        # Simular seguimiento con mejoras
        datos_mejoria = {
            "autoestima": 6,  # Mejora en autoestima
            "habilidades_sociales": 6,  # Mejora en habilidades
            "proyecto_vida": "EN_CONSTRUCCION",  # Inicia construcción proyecto
            "salud_mental": "SINTOMAS_MODERADOS",  # Mejora parcial
            "consumo_sustancias": "CONSUMO_OCASIONAL",  # Reduce consumo
            "actividad_fisica_regular": True,  # Inicia actividad física
            "observaciones_generales": "Mejora notable tras 3 meses de intervención multidisciplinaria"
        }
        
        response_update = client.put(f"/atencion-adolescencia/{atencion_riesgo_alto_id}", json=datos_mejoria)
        assert response_update.status_code == 200
        
        data_mejorada = response_update.json()
        nivel_riesgo_final = data_mejorada["nivel_riesgo_integral"]
        
        # Verificar mejoras
        assert data_mejorada["autoestima"] > data_inicial["autoestima"]
        assert len(data_mejorada["factores_protectores_identificados"]) > len(data_inicial["factores_protectores_identificados"])
        
        # El nivel de riesgo puede haberse reducido (no siempre garantizado por múltiples factores)
        niveles_riesgo = ["BAJO", "MODERADO", "ALTO", "MUY_ALTO", "CRITICO"]
        assert niveles_riesgo.index(nivel_riesgo_final) <= niveles_riesgo.index(nivel_riesgo_inicial)

# =============================================================================
# GRUPO 6: TESTS COMPATIBILIDAD LEGACY
# =============================================================================

class TestCompatibilidadLegacy:
    """Suite de tests para compatibilidad con endpoints legacy"""

    def test_endpoint_legacy_listar(self):
        """Test endpoint legacy para listar atenciones"""
        response = client.get("/atencion-adolescencia/atenciones-adolescencia/?skip=0&limit=50")
        assert response.status_code == 200, response.text
        
        data = response.json()
        assert isinstance(data, list)

    def test_endpoint_legacy_datos_consistentes(self):
        """Test que endpoint legacy retorna datos consistentes con endpoint principal"""
        response_principal = client.get("/atencion-adolescencia/?skip=0&limit=10")
        response_legacy = client.get("/atencion-adolescencia/atenciones-adolescencia/?skip=0&limit=10")
        
        assert response_principal.status_code == 200
        assert response_legacy.status_code == 200
        
        data_principal = response_principal.json()
        data_legacy = response_legacy.json()
        
        # Los datos deben ser idénticos
        assert len(data_principal) == len(data_legacy)
        
        if data_principal:
            assert data_principal[0]["id"] == data_legacy[0]["id"]

# =============================================================================
# FUNCIONES HELPER PARA TESTS
# =============================================================================

def assert_campos_calculados_presentes(data):
    """Helper para verificar que todos los campos calculados están presentes"""
    campos_requeridos = [
        "imc", "estado_nutricional", "riesgo_cardiovascular_temprano",
        "desarrollo_psicosocial_apropiado", "factores_protectores_identificados",
        "nivel_riesgo_integral", "proxima_consulta_recomendada_dias", "completitud_evaluacion"
    ]
    
    for campo in campos_requeridos:
        assert campo in data, f"Campo calculado faltante: {campo}"

def assert_estructura_atencion_completa(data):
    """Helper para verificar estructura completa de atención"""
    # Campos básicos
    assert "id" in data
    assert "paciente_id" in data
    assert "edad_anos" in data
    assert "fecha_atencion" in data
    
    # Campos antropométricos
    assert "peso_kg" in data
    assert "talla_cm" in data
    assert "presion_sistolica" in data
    
    # Campos psicosociales
    assert "autoestima" in data
    assert "proyecto_vida" in data
    assert "salud_mental" in data
    
    # Campos calculados
    assert_campos_calculados_presentes(data)
    
    # Metadatos
    assert "created_at" in data
    assert "updated_at" in data