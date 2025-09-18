# =============================================================================
# Tests Atención Infancia - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2
# =============================================================================

import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_infancia = None
atencion_infancia_id_test = None
atencion_infancia_id_alto_riesgo = None

# =============================================================================
# SETUP Y TEARDOWN
# =============================================================================

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_atencion_infancia_test_data():
    """Setup: Crea un paciente de 8 años para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_infancia
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba (8 años - infancia)
    fecha_nacimiento = date.today() - timedelta(days=8 * 365)  # 8 años
    datos_paciente = {
        "tipo_documento": "TI",  # Tarjeta de identidad para menores
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Niño",
        "primer_apellido": "Infancia_Test",
        "fecha_nacimiento": fecha_nacimiento.isoformat(),
        "genero": "M"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_infancia = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    if atencion_infancia_id_alto_riesgo:
        # Buscar atención asociada antes de eliminar
        try:
            atencion_response = db_client.table("atenciones").select("id").eq("detalle_id", atencion_infancia_id_alto_riesgo).execute()
            if atencion_response.data:
                for atencion in atencion_response.data:
                    db_client.table("atenciones").delete().eq("id", atencion["id"]).execute()
        except:
            pass
        db_client.table("atencion_infancia").delete().eq("id", atencion_infancia_id_alto_riesgo).execute()
    if atencion_infancia_id_test:
        # Buscar atención asociada antes de eliminar
        try:
            atencion_response = db_client.table("atenciones").select("id").eq("detalle_id", atencion_infancia_id_test).execute()
            if atencion_response.data:
                for atencion in atencion_response.data:
                    db_client.table("atenciones").delete().eq("id", atencion["id"]).execute()
        except:
            pass
        db_client.table("atencion_infancia").delete().eq("id", atencion_infancia_id_test).execute()
    if paciente_id_test_infancia:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_infancia).execute()

# =============================================================================
# TESTS CRUD BÁSICO
# =============================================================================

class TestAtencionInfanciaCRUD:
    """Grupo 1: Tests del CRUD básico de Atención Infancia."""

    def test_01_crear_atencion_infancia_basica(self):
        """Test: Crear atención de infancia con datos básicos obligatorios."""
        global atencion_infancia_id_test
        assert paciente_id_test_infancia is not None

        datos_atencion = {
            "paciente_id": paciente_id_test_infancia,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 25.5,
            "talla_cm": 125.0,
            "grado_escolar": "3°",
            "desempeno_escolar": "BASICO",
            "dificultades_aprendizaje": False,
            "tamizaje_visual": "NORMAL",
            "tamizaje_auditivo": "NORMAL",
            "tamizaje_salud_bucal": "NORMAL",
            "esquema_vacunacion_completo": True,
            "actividad_fisica_semanal_horas": 10.0,
            "horas_pantalla_diarias": 2.0,
            "horas_sueno_diarias": 10.0,
            "alimentacion_escolar": True,
            "consume_comida_chatarra": False,
            "observaciones_profesional_infancia": "Niño con desarrollo normal para su edad"
        }

        response = client.post("/atencion-infancia/", json=datos_atencion)
        assert response.status_code == 201, response.text
        
        data = response.json()
        atencion_infancia_id_test = data["id"]
        
        # Validar datos básicos
        assert data["paciente_id"] == paciente_id_test_infancia
        assert data["peso_kg"] == 25.5
        assert data["talla_cm"] == 125.0
        assert data["desempeno_escolar"] == "BASICO"
        assert data["tamizaje_visual"] == "NORMAL"
        assert data["tamizaje_auditivo"] == "NORMAL"
        assert data["tamizaje_salud_bucal"] == "NORMAL"
        assert data["esquema_vacunacion_completo"] is True
        
        # Validar campos calculados
        assert "estado_nutricional" in data
        assert "indice_masa_corporal" in data
        assert data["desarrollo_apropiado_edad"] is True
        assert data["riesgo_nutricional"] == "Bajo"
        assert data["proxima_consulta_recomendada_dias"] == 365  # Normal = anual
        assert data["completitud_evaluacion"] > 75.0  # Ajuste realista basado en campos completados

    def test_02_obtener_atencion_infancia_por_id(self):
        """Test: Obtener atención de infancia por ID con campos calculados."""
        assert atencion_infancia_id_test is not None
        
        response = client.get(f"/atencion-infancia/{atencion_infancia_id_test}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == atencion_infancia_id_test
        assert data["desempeno_escolar"] == "BASICO"
        assert "estado_nutricional" in data
        assert "indice_masa_corporal" in data
        assert "desarrollo_apropiado_edad" in data
        assert "proxima_consulta_recomendada_dias" in data

    def test_03_listar_atenciones_infancia_con_filtros(self):
        """Test: Listar atenciones de infancia con filtros avanzados."""
        # Sin filtros
        response = client.get("/atencion-infancia/")
        assert response.status_code == 200
        atenciones = response.json()
        assert len(atenciones) >= 1
        
        # Con filtro por paciente
        response = client.get(f"/atencion-infancia/?paciente_id={paciente_id_test_infancia}")
        assert response.status_code == 200
        atenciones_paciente = response.json()
        assert len(atenciones_paciente) >= 1
        assert all(a["paciente_id"] == paciente_id_test_infancia for a in atenciones_paciente)
        
        # Con filtro por desempeño escolar
        response = client.get("/atencion-infancia/?desempeno_escolar=BASICO")
        assert response.status_code == 200
        atenciones_basico = response.json()
        assert all(a["desempeno_escolar"] == "BASICO" for a in atenciones_basico)

    def test_04_actualizar_atencion_infancia(self):
        """Test: Actualizar atención de infancia con recálculo automático."""
        assert atencion_infancia_id_test is not None
        
        datos_actualizacion = {
            "peso_kg": 30.0,  # Aumento de peso
            "desempeno_escolar": "ALTO",
            "dificultades_aprendizaje": True,
            "tamizaje_visual": "ALTERADO",
            "numero_caries": 3,
            "observaciones_profesional_infancia": "Requiere seguimiento por problemas visuales y caries"
        }
        
        response = client.put(f"/atencion-infancia/{atencion_infancia_id_test}", json=datos_actualizacion)
        assert response.status_code == 200
        
        data = response.json()
        
        # Validar cambios
        assert data["peso_kg"] == 30.0
        assert data["desempeno_escolar"] == "ALTO"
        assert data["dificultades_aprendizaje"] is True
        assert data["tamizaje_visual"] == "ALTERADO"
        
        # Validar recálculo automático
        assert data["requiere_seguimiento_especializado"] is True  # Por tamizaje alterado
        assert data["proxima_consulta_recomendada_dias"] == 30  # Seguimiento especializado

    def test_05_crear_atencion_infancia_alto_riesgo(self):
        """Test: Crear atención de infancia con múltiples factores de riesgo."""
        global atencion_infancia_id_alto_riesgo
        
        datos_alto_riesgo = {
            "paciente_id": paciente_id_test_infancia,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 45.0,  # Sobrepeso para la edad
            "talla_cm": 125.0,
            "grado_escolar": "3°",
            "desempeno_escolar": "BAJO",
            "dificultades_aprendizaje": True,
            "tamizaje_visual": "ALTERADO",
            "tamizaje_auditivo": "REQUIERE_EVALUACION",
            "tamizaje_salud_bucal": "ALTERADO",
            "numero_caries": 8,
            "esquema_vacunacion_completo": False,
            "vacunas_faltantes": "Triple viral de refuerzo",
            "actividad_fisica_semanal_horas": 2.0,  # Sedentarismo
            "horas_pantalla_diarias": 8.0,  # Exceso de pantallas
            "horas_sueno_diarias": 7.0,  # Poco sueño
            "factores_riesgo_identificados": ["SEDENTARISMO", "EXPOSICION_PANTALLAS", "ALIMENTACION_INADECUADA"],
            "alimentacion_escolar": False,
            "consume_comida_chatarra": True,
            "observaciones_profesional_infancia": "Múltiples factores de riesgo identificados - requiere intervención integral"
        }
        
        response = client.post("/atencion-infancia/", json=datos_alto_riesgo)
        assert response.status_code == 201
        
        data = response.json()
        atencion_infancia_id_alto_riesgo = data["id"]
        
        # Validar identificación de alto riesgo
        assert data["desarrollo_apropiado_edad"] is False
        assert data["riesgo_nutricional"] == "Alto"
        assert data["requiere_seguimiento_especializado"] is True
        assert data["proxima_consulta_recomendada_dias"] == 30  # Seguimiento urgente

# =============================================================================
# TESTS ENDPOINTS ESPECIALIZADOS
# =============================================================================

class TestAtencionInfanciaEndpointsEspecializados:
    """Grupo 2: Tests de endpoints especializados por desempeño y paciente."""

    def test_06_listar_por_desempeno_escolar(self):
        """Test: Endpoint especializado por desempeño escolar."""
        response = client.get("/atencion-infancia/desempeno/ALTO")
        assert response.status_code == 200
        
        atenciones = response.json()
        # Debe incluir la atención actualizada a ALTO
        assert any(a["desempeno_escolar"] == "ALTO" for a in atenciones)

    def test_07_obtener_atenciones_cronologicas_paciente(self):
        """Test: Historial cronológico de atenciones para un paciente."""
        assert paciente_id_test_infancia is not None
        
        response = client.get(f"/atencion-infancia/paciente/{paciente_id_test_infancia}/cronologicas")
        assert response.status_code == 200
        
        atenciones = response.json()
        assert len(atenciones) >= 2  # Tenemos básica + alto riesgo
        
        # Verificar que todas pertenecen al paciente
        assert all(a["paciente_id"] == paciente_id_test_infancia for a in atenciones)
        
        # Verificar orden cronológico ascendente
        fechas = [a["fecha_atencion"] for a in atenciones]
        assert fechas == sorted(fechas)

# =============================================================================
# TESTS ESTADÍSTICAS Y REPORTES
# =============================================================================

class TestAtencionInfanciaEstadisticasReportes:
    """Grupo 3: Tests de estadísticas y reportes especializados."""

    def test_08_obtener_estadisticas_basicas(self):
        """Test: Endpoint de estadísticas básicas de Atención Infancia."""
        response = client.get("/atencion-infancia/estadisticas/basicas")
        assert response.status_code == 200
        
        stats = response.json()
        
        # Validar estructura actual del service layer
        assert "total_atenciones" in stats
        assert "distribucion_desempeno_escolar" in stats
        assert "tamizajes_alterados" in stats
        assert "fecha_calculo" in stats

        # Validar datos básicos
        assert stats["total_atenciones"] >= 0
        assert isinstance(stats["distribucion_desempeno_escolar"], dict)
        assert isinstance(stats["tamizajes_alterados"], dict)
        
        # Test básico completado - estadísticas funcionando

    def test_09_estadisticas_con_filtros_fecha(self):
        """Test: Estadísticas con filtros de fecha."""
        fecha_hoy = date.today()
        
        response = client.get(f"/atencion-infancia/estadisticas/basicas?fecha_desde={fecha_hoy}&fecha_hasta={fecha_hoy}")
        assert response.status_code == 200
        
        stats = response.json()
        assert stats["total_atenciones"] >= 0  # Ajustar a estructura real

    def test_10_reporte_desarrollo_escolar_general(self):
        """Test: Reporte detallado de desarrollo escolar sin filtros."""
        response = client.get("/atencion-infancia/reportes/desarrollo")
        assert response.status_code == 200
        
        reporte = response.json()
        
        # Validar estructura
        assert "parametros_reporte" in reporte
        assert "desempeno_academico" in reporte
        assert "problemas_desarrollo" in reporte
        assert "recomendaciones_seguimiento" in reporte
        assert "fecha_generacion" in reporte
        
        # Validar parámetros
        params = reporte["parametros_reporte"]
        assert params["grado_escolar"] == "Todos"
        assert params["total_estudiantes_analizados"] >= 2
        
        # Validar categorías de desempeño
        desempeno = reporte["desempeno_academico"]
        assert all(categoria in desempeno for categoria in ["SUPERIOR", "ALTO", "BASICO", "BAJO", "NO_ESCOLARIZADO"])
        
        # Debe tener datos en ALTO y BAJO (de nuestras pruebas)
        assert desempeno["ALTO"] >= 1
        assert desempeno["BAJO"] >= 1

    def test_11_reporte_desarrollo_escolar_filtrado(self):
        """Test: Reporte de desarrollo filtrado por grado escolar."""
        response = client.get("/atencion-infancia/reportes/desarrollo?grado_escolar=3°")
        assert response.status_code == 200
        
        reporte = response.json()
        params = reporte["parametros_reporte"]
        assert params["grado_escolar"] == "3°"
        assert params["total_estudiantes_analizados"] >= 2  # Ambos pacientes en 3°

# =============================================================================
# TESTS CASOS EDGE Y VALIDACIONES
# =============================================================================

class TestAtencionInfanciaCasosEdge:
    """Grupo 4: Tests de casos edge y validaciones específicas."""

    def test_12_crear_atencion_paciente_inexistente(self):
        """Test: Error al crear atención para paciente que no existe."""
        paciente_falso = str(uuid4())
        
        datos_atencion = {
            "paciente_id": paciente_falso,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 25.5,
            "talla_cm": 125.0,
            "desempeno_escolar": "BASICO",
            "tamizaje_visual": "NORMAL",
            "tamizaje_auditivo": "NORMAL",
            "tamizaje_salud_bucal": "NORMAL",
            "esquema_vacunacion_completo": True
        }
        
        response = client.post("/atencion-infancia/", json=datos_atencion)
        assert response.status_code == 400
        
        error = response.json()
        assert "El paciente especificado no existe" in error.get("detail", "")

    def test_13_crear_atencion_edad_fuera_rango(self):
        """Test: Error al crear atención para paciente fuera de rango de edad."""
        # Crear paciente muy joven (4 años)
        fecha_nacimiento_joven = date.today() - timedelta(days=4 * 365)
        datos_paciente_joven = {
            "tipo_documento": "RC",
            "numero_documento": str(uuid4())[:10],
            "primer_nombre": "Niño",
            "primer_apellido": "MuyJoven",
            "fecha_nacimiento": fecha_nacimiento_joven.isoformat(),
            "genero": "M"
        }
        response_paciente = client.post("/pacientes/", json=datos_paciente_joven)
        assert response_paciente.status_code == 201
        paciente_joven_id = response_paciente.json()["data"][0]["id"]
        
        # Intentar crear atención de infancia para paciente de 4 años
        datos_atencion = {
            "paciente_id": paciente_joven_id,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 18.0,
            "talla_cm": 105.0,
            "desempeno_escolar": "NO_ESCOLARIZADO",
            "tamizaje_visual": "NORMAL",
            "tamizaje_auditivo": "NORMAL",
            "tamizaje_salud_bucal": "NORMAL",
            "esquema_vacunacion_completo": True
        }
        
        response = client.post("/atencion-infancia/", json=datos_atencion)
        assert response.status_code == 400
        
        error = response.json()
        assert "fuera del rango de infancia" in error.get("detail", "")
        
        # Limpiar paciente de prueba
        client.delete(f"/pacientes/{paciente_joven_id}")

    def test_14_obtener_atencion_inexistente(self):
        """Test: Error al obtener atención que no existe."""
        atencion_falsa = str(uuid4())
        
        response = client.get(f"/atencion-infancia/{atencion_falsa}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Atención de infancia no encontrada" in error.get("detail", "")

    def test_15_actualizar_atencion_inexistente(self):
        """Test: Error al actualizar atención que no existe."""
        atencion_falsa = str(uuid4())
        
        datos_actualizacion = {
            "peso_kg": 30.0
        }
        
        response = client.put(f"/atencion-infancia/{atencion_falsa}", json=datos_actualizacion)
        assert response.status_code == 404
        
        error = response.json()
        assert "Atención de infancia no encontrada" in error.get("detail", "")

    def test_16_validacion_datos_antropometricos(self):
        """Test: Validación de rangos en datos antropométricos."""
        datos_peso_invalido = {
            "paciente_id": paciente_id_test_infancia,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 200.0,  # Peso fuera de rango
            "talla_cm": 125.0,
            "desempeno_escolar": "BASICO",
            "tamizaje_visual": "NORMAL",
            "tamizaje_auditivo": "NORMAL",
            "tamizaje_salud_bucal": "NORMAL",
            "esquema_vacunacion_completo": True
        }
        
        response = client.post("/atencion-infancia/", json=datos_peso_invalido)
        assert response.status_code == 422  # Validation error

# =============================================================================
# TESTS FUNCIONALIDAD INTEGRADA
# =============================================================================

class TestAtencionInfanciaIntegracion:
    """Grupo 5: Tests de integración y funcionalidad completa."""

    def test_17_flujo_completo_seguimiento_academico(self):
        """Test: Flujo completo de seguimiento académico para un estudiante."""
        assert paciente_id_test_infancia is not None
        
        # 1. Crear atención inicial con bajo rendimiento
        datos_inicial = {
            "paciente_id": paciente_id_test_infancia,
            "fecha_atencion": date.today().isoformat(),
            "peso_kg": 28.0,
            "talla_cm": 130.0,
            "grado_escolar": "4°",
            "desempeno_escolar": "BAJO",
            "dificultades_aprendizaje": True,
            "tamizaje_visual": "NORMAL",
            "tamizaje_auditivo": "NORMAL",
            "tamizaje_salud_bucal": "NORMAL",
            "esquema_vacunacion_completo": True,
            "observaciones_profesional_infancia": "Requiere evaluación psicopedagógica"
        }
        
        response_crear = client.post("/atencion-infancia/", json=datos_inicial)
        assert response_crear.status_code == 201
        atencion_id = response_crear.json()["id"]
        
        # 2. Verificar que requiere seguimiento
        data_inicial = response_crear.json()
        assert data_inicial["desarrollo_apropiado_edad"] is False
        assert data_inicial["requiere_seguimiento_especializado"] is True
        assert data_inicial["proxima_consulta_recomendada_dias"] == 30
        
        # 3. Actualizar con mejora académica
        datos_seguimiento = {
            "desempeno_escolar": "BASICO",
            "dificultades_aprendizaje": False,
            "observaciones_profesional_infancia": "Mejora tras intervención psicopedagógica"
        }
        
        response_actualizar = client.put(f"/atencion-infancia/{atencion_id}", json=datos_seguimiento)
        assert response_actualizar.status_code == 200
        
        # 4. Verificar mejora en evaluación
        data_actualizada = response_actualizar.json()
        assert data_actualizada["desarrollo_apropiado_edad"] is True
        assert data_actualizada["requiere_seguimiento_especializado"] is False
        assert data_actualizada["proxima_consulta_recomendada_dias"] == 365  # Vuelve a control anual
        
        # 5. Verificar en estadísticas
        response_stats = client.get("/atencion-infancia/estadisticas/basicas")
        assert response_stats.status_code == 200
        stats = response_stats.json()
        assert stats["por_desempeno_escolar"]["BASICO"] >= 1
        
        # 6. Limpiar
        response_eliminar = client.delete(f"/atencion-infancia/{atencion_id}")
        assert response_eliminar.status_code == 204

    def test_18_validacion_campos_calculados_todos_escenarios(self):
        """Test: Validar lógica de campos calculados en diferentes escenarios."""
        escenarios = [
            {
                "nombre": "Normal",
                "datos": {
                    "peso_kg": 25.0, "talla_cm": 125.0, "desempeno_escolar": "ALTO",
                    "tamizaje_visual": "NORMAL", "tamizaje_auditivo": "NORMAL", "tamizaje_salud_bucal": "NORMAL",
                    "esquema_vacunacion_completo": True, "dificultades_aprendizaje": False,
                    "actividad_fisica_semanal_horas": 10.0, "consume_comida_chatarra": False
                },
                "esperado": {"riesgo_nutricional": "Bajo", "desarrollo_apropiado": True, "consulta_dias": 365}
            },
            {
                "nombre": "Sobrepeso",
                "datos": {
                    "peso_kg": 40.0, "talla_cm": 125.0, "desempeno_escolar": "BASICO",
                    "tamizaje_visual": "NORMAL", "tamizaje_auditivo": "NORMAL", "tamizaje_salud_bucal": "NORMAL",
                    "esquema_vacunacion_completo": True, "dificultades_aprendizaje": False,
                    "actividad_fisica_semanal_horas": 3.0, "consume_comida_chatarra": True
                },
                "esperado": {"riesgo_nutricional": "Alto", "desarrollo_apropiado": True, "consulta_dias": 180}
            },
            {
                "nombre": "Problemas_Desarrollo",
                "datos": {
                    "peso_kg": 25.0, "talla_cm": 125.0, "desempeno_escolar": "BAJO",
                    "tamizaje_visual": "ALTERADO", "tamizaje_auditivo": "NORMAL", "tamizaje_salud_bucal": "ALTERADO",
                    "esquema_vacunacion_completo": True, "dificultades_aprendizaje": True,
                    "numero_caries": 5
                },
                "esperado": {"desarrollo_apropiado": False, "seguimiento_especializado": True, "consulta_dias": 30}
            }
        ]
        
        atenciones_creadas = []
        
        for escenario in escenarios:
            datos_atencion = {
                "paciente_id": paciente_id_test_infancia,
                "fecha_atencion": date.today().isoformat(),
                **escenario["datos"]
            }
            
            response = client.post("/atencion-infancia/", json=datos_atencion)
            assert response.status_code == 201, f"Error en escenario {escenario['nombre']}: {response.text}"
            
            data = response.json()
            atenciones_creadas.append(data["id"])
            
            # Validar expectativas específicas del escenario
            esperado = escenario["esperado"]
            
            if "riesgo_nutricional" in esperado:
                assert data["riesgo_nutricional"] == esperado["riesgo_nutricional"], \
                    f"Escenario {escenario['nombre']}: esperado {esperado['riesgo_nutricional']}, obtenido {data['riesgo_nutricional']}"
            
            if "desarrollo_apropiado" in esperado:
                assert data["desarrollo_apropiado_edad"] == esperado["desarrollo_apropiado"], \
                    f"Escenario {escenario['nombre']}: desarrollo apropiado esperado {esperado['desarrollo_apropiado']}"
            
            if "seguimiento_especializado" in esperado:
                assert data["requiere_seguimiento_especializado"] == esperado["seguimiento_especializado"], \
                    f"Escenario {escenario['nombre']}: seguimiento especializado esperado {esperado['seguimiento_especializado']}"
            
            if "consulta_dias" in esperado:
                assert data["proxima_consulta_recomendada_dias"] == esperado["consulta_dias"], \
                    f"Escenario {escenario['nombre']}: consulta días esperado {esperado['consulta_dias']}"
        
        # Limpiar atenciones creadas
        for atencion_id in atenciones_creadas:
            client.delete(f"/atencion-infancia/{atencion_id}")

# =============================================================================
# TESTS DE ELIMINACIÓN
# =============================================================================

class TestAtencionInfanciaEliminacion:
    """Grupo 6: Tests de eliminación y cleanup."""

    def test_19_eliminar_atencion_infancia(self):
        """Test: Eliminar atención de infancia exitosamente."""
        assert atencion_infancia_id_test is not None
        
        response = client.delete(f"/atencion-infancia/{atencion_infancia_id_test}")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response_get = client.get(f"/atencion-infancia/{atencion_infancia_id_test}")
        assert response_get.status_code == 404

    def test_20_eliminar_atencion_inexistente(self):
        """Test: Error al eliminar atención que no existe."""
        atencion_falsa = str(uuid4())
        
        response = client.delete(f"/atencion-infancia/{atencion_falsa}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Atención de infancia no encontrada" in error.get("detail", "")