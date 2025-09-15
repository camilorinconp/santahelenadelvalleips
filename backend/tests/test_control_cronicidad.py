import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_cc = None
control_cronicidad_id_test = None
control_hipertension_id_test = None

# =============================================================================
# SETUP Y TEARDOWN
# =============================================================================

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_control_cronicidad_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_cc
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "CC_Test",
        "fecha_nacimiento": "1960-01-01",
        "genero": "M"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_cc = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    if control_hipertension_id_test:
        db_client.table("control_hipertension_detalles").delete().eq("id", control_hipertension_id_test).execute()
    if control_cronicidad_id_test:
        # Buscar atención asociada antes de eliminar
        try:
            atencion_response = db_client.table("atenciones").select("id").eq("detalle_id", control_cronicidad_id_test).execute()
            if atencion_response.data:
                for atencion in atencion_response.data:
                    db_client.table("atenciones").delete().eq("id", atencion["id"]).execute()
        except:
            pass
        db_client.table("control_cronicidad").delete().eq("id", control_cronicidad_id_test).execute()
    if paciente_id_test_cc:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_cc).execute()

# =============================================================================
# TESTS CRUD BÁSICO
# =============================================================================

class TestControlCronicidadCRUD:
    """Grupo 1: Tests del CRUD básico de Control de Cronicidad."""

    def test_01_crear_control_cronicidad_hipertension(self):
        """Test: Crear control de cronicidad tipo Hipertensión con campos calculados."""
        global control_cronicidad_id_test
        assert paciente_id_test_cc is not None

        datos_control = {
            "paciente_id": paciente_id_test_cc,
            "fecha_control": date.today().isoformat(),
            "tipo_cronicidad": "Hipertension",
            "estado_control": "Controlado",
            "adherencia_tratamiento": "Buena",
            "peso_kg": 70.5,
            "talla_cm": 170.0,
            "observaciones": "Control rutinario, paciente estable"
        }

        response = client.post("/control-cronicidad/", json=datos_control)
        assert response.status_code == 201, response.text
        
        data = response.json()
        control_cronicidad_id_test = data["id"]
        
        # Validar datos básicos
        assert data["paciente_id"] == paciente_id_test_cc
        assert data["tipo_cronicidad"] == "Hipertension"
        assert data["estado_control"] == "Controlado"
        assert data["adherencia_tratamiento"] == "Buena"
        
        # Validar cálculo automático de IMC
        assert data["imc"] == 24.39  # 70.5 / (1.7^2)
        
        # Validar campos calculados
        assert data["control_adecuado"] is True  # Controlado = True
        assert data["riesgo_cardiovascular"] == "Bajo"  # Buen control + IMC normal
        assert data["adherencia_score"] == 85.0  # Buena = 85
        assert data["proxima_cita_recomendada_dias"] == 90  # HTA controlada = 3 meses

    def test_02_obtener_control_cronicidad_por_id(self):
        """Test: Obtener control de cronicidad específico con campos calculados."""
        assert control_cronicidad_id_test is not None
        
        response = client.get(f"/control-cronicidad/{control_cronicidad_id_test}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == control_cronicidad_id_test
        assert data["tipo_cronicidad"] == "Hipertension"
        assert "control_adecuado" in data
        assert "riesgo_cardiovascular" in data
        assert "adherencia_score" in data
        assert "proxima_cita_recomendada_dias" in data

    def test_03_listar_controles_cronicidad_con_filtros(self):
        """Test: Listar controles con filtros avanzados."""
        # Sin filtros
        response = client.get("/control-cronicidad/")
        assert response.status_code == 200
        controles = response.json()
        assert len(controles) >= 1
        
        # Con filtro por paciente
        response = client.get(f"/control-cronicidad/?paciente_id={paciente_id_test_cc}")
        assert response.status_code == 200
        controles_paciente = response.json()
        assert len(controles_paciente) >= 1
        assert all(c["paciente_id"] == paciente_id_test_cc for c in controles_paciente)
        
        # Con filtro por tipo
        response = client.get("/control-cronicidad/?tipo_cronicidad=Hipertension")
        assert response.status_code == 200
        controles_hta = response.json()
        assert all(c["tipo_cronicidad"] == "Hipertension" for c in controles_hta)

    def test_04_actualizar_control_cronicidad(self):
        """Test: Actualizar control de cronicidad con recálculo automático."""
        assert control_cronicidad_id_test is not None
        
        datos_actualizacion = {
            "peso_kg": 75.0,  # Cambiar peso
            "estado_control": "No controlado",  # Empeorar control
            "adherencia_tratamiento": "Regular",  # Reducir adherencia
            "observaciones": "Paciente con dificultades en adherencia"
        }
        
        response = client.put(f"/control-cronicidad/{control_cronicidad_id_test}", json=datos_actualizacion)
        assert response.status_code == 200
        
        data = response.json()
        
        # Validar cambios
        assert data["peso_kg"] == 75.0
        assert data["estado_control"] == "No controlado"
        assert data["adherencia_tratamiento"] == "Regular"
        
        # Validar recálculo de IMC (75 / (1.7^2) ≈ 25.96, tolerancia ±0.02 por precisión de cálculo)
        assert abs(data["imc"] - 25.96) < 0.02
        
        # Validar recálculo de campos calculados
        assert data["control_adecuado"] is False  # No controlado = False
        assert data["riesgo_cardiovascular"] == "Moderado"  # Control malo + sobrepeso
        assert data["adherencia_score"] == 60.0  # Regular = 60
        assert data["proxima_cita_recomendada_dias"] == 30  # No controlado = 1 mes

    def test_05_crear_control_diabetes_con_calculo_diferente(self):
        """Test: Crear control tipo Diabetes para verificar lógica específica."""
        datos_diabetes = {
            "paciente_id": paciente_id_test_cc,
            "fecha_control": date.today().isoformat(),
            "tipo_cronicidad": "Diabetes",
            "estado_control": "En proceso",
            "adherencia_tratamiento": "Mala",
            "peso_kg": 85.0,
            "talla_cm": 170.0,
            "observaciones": "Paciente con diabetes mal controlada"
        }
        
        response = client.post("/control-cronicidad/", json=datos_diabetes)
        assert response.status_code == 201
        
        data = response.json()
        
        # Validar tipo específico
        assert data["tipo_cronicidad"] == "Diabetes"
        
        # Validar lógica específica para diabetes (En proceso + Mala adherencia + Obesidad = Moderado/Alto)
        assert data["riesgo_cardiovascular"] in ["Moderado", "Alto"]  # Lógica puede variar
        assert data["adherencia_score"] == 30.0  # Mala = 30
        assert data["proxima_cita_recomendada_dias"] == 60  # En proceso = 60 días (2 meses)

# =============================================================================
# TESTS ENDPOINTS ESPECIALIZADOS  
# =============================================================================

class TestControlCronicidadEndpointsEspecializados:
    """Grupo 2: Tests de endpoints especializados por tipo y paciente."""

    def test_06_listar_por_tipo_cronicidad_valido(self):
        """Test: Endpoint especializado por tipo de cronicidad."""
        response = client.get("/control-cronicidad/tipo/Hipertension")
        assert response.status_code == 200
        
        controles = response.json()
        # Debe tener al menos el control que creamos
        assert len(controles) >= 1
        assert all(c["tipo_cronicidad"] == "Hipertension" for c in controles)

    def test_07_listar_por_tipo_cronicidad_invalido(self):
        """Test: Endpoint con tipo de cronicidad inválido."""
        response = client.get("/control-cronicidad/tipo/TipoInvalido")
        assert response.status_code == 400
        
        error = response.json()
        assert "Tipo de cronicidad no válido" in error.get("detail", error.get("error", {}).get("message", ""))

    def test_08_obtener_controles_cronologicos_paciente(self):
        """Test: Historial cronológico de controles de un paciente."""
        assert paciente_id_test_cc is not None
        
        response = client.get(f"/control-cronicidad/paciente/{paciente_id_test_cc}/cronologicos")
        assert response.status_code == 200
        
        controles = response.json()
        assert len(controles) >= 2  # Tenemos Hipertensión + Diabetes
        
        # Verificar orden cronológico ascendente
        fechas = [c["fecha_control"] for c in controles]
        assert fechas == sorted(fechas)
        
        # Verificar que todos pertenecen al paciente
        assert all(c["paciente_id"] == paciente_id_test_cc for c in controles)

    def test_09_obtener_controles_cronologicos_con_filtro_tipo(self):
        """Test: Historial cronológico filtrado por tipo específico."""
        assert paciente_id_test_cc is not None
        
        response = client.get(f"/control-cronicidad/paciente/{paciente_id_test_cc}/cronologicos?tipo_cronicidad=Diabetes")
        assert response.status_code == 200
        
        controles = response.json()
        assert len(controles) >= 1
        assert all(c["tipo_cronicidad"] == "Diabetes" for c in controles)

# =============================================================================
# TESTS ESTADÍSTICAS Y REPORTES
# =============================================================================

class TestControlCronicidadEstadisticasReportes:
    """Grupo 3: Tests de estadísticas y reportes."""

    def test_10_obtener_estadisticas_basicas(self):
        """Test: Endpoint de estadísticas básicas de Control Cronicidad."""
        response = client.get("/control-cronicidad/estadisticas/basicas")
        assert response.status_code == 200
        
        stats = response.json()
        
        # Validar estructura
        assert "resumen_general" in stats
        assert "por_tipo_cronicidad" in stats
        assert "control_metabolico" in stats
        assert "fecha_calculo" in stats
        
        # Validar resumen general
        resumen = stats["resumen_general"]
        assert "total_controles" in resumen
        assert "porcentaje_controlados" in resumen
        assert "porcentaje_buena_adherencia" in resumen
        assert resumen["total_controles"] >= 2  # Tenemos al menos 2 controles
        
        # Validar por tipo
        por_tipo = stats["por_tipo_cronicidad"]
        assert "Hipertension" in por_tipo
        assert "Diabetes" in por_tipo
        assert "ERC" in por_tipo
        assert "Dislipidemia" in por_tipo
        assert por_tipo["Hipertension"] >= 1
        assert por_tipo["Diabetes"] >= 1
        
        # Validar control metabólico
        control = stats["control_metabolico"]
        assert "controlados" in control
        assert "no_controlados" in control
        assert "en_proceso" in control

    def test_11_reporte_adherencia_sin_filtros(self):
        """Test: Reporte de adherencia sin filtros."""
        response = client.get("/control-cronicidad/reportes/adherencia")
        assert response.status_code == 200
        
        reporte = response.json()
        
        # Validar estructura
        assert "parametros_reporte" in reporte
        assert "adherencia_absolutos" in reporte
        assert "adherencia_porcentajes" in reporte
        assert "fecha_generacion" in reporte
        
        # Validar parámetros
        params = reporte["parametros_reporte"]
        assert params["tipo_cronicidad"] == "Todos"
        assert params["total_controles_analizados"] >= 2
        
        # Validar categorías de adherencia
        absolutos = reporte["adherencia_absolutos"]
        assert "Buena" in absolutos
        assert "Regular" in absolutos
        assert "Mala" in absolutos
        assert "No especificada" in absolutos
        
        # Validar que tenemos datos
        assert absolutos["Buena"] >= 1  # Primer control
        assert absolutos["Regular"] >= 1  # Actualización
        assert absolutos["Mala"] >= 1  # Control diabetes
        
        # Validar porcentajes suman lógicamente
        porcentajes = reporte["adherencia_porcentajes"]
        total_porcentaje = sum(porcentajes.values())
        assert 99.0 <= total_porcentaje <= 101.0  # Tolerancia por redondeo

    def test_12_reporte_adherencia_con_filtros(self):
        """Test: Reporte de adherencia con filtros específicos."""
        # Filtro por tipo
        response = client.get("/control-cronicidad/reportes/adherencia?tipo_cronicidad=Hipertension")
        assert response.status_code == 200
        
        reporte = response.json()
        params = reporte["parametros_reporte"]
        assert params["tipo_cronicidad"] == "Hipertension"
        assert params["total_controles_analizados"] >= 1
        
        # Filtro por fechas
        fecha_hoy = date.today().isoformat()
        response = client.get(f"/control-cronicidad/reportes/adherencia?fecha_desde={fecha_hoy}&fecha_hasta={fecha_hoy}")
        assert response.status_code == 200
        
        reporte_fechas = response.json()
        params_fechas = reporte_fechas["parametros_reporte"]
        assert params_fechas["fecha_desde"] == fecha_hoy
        assert params_fechas["fecha_hasta"] == fecha_hoy

# =============================================================================
# TESTS CASOS EDGE Y VALIDACIONES
# =============================================================================

class TestControlCronicidadCasosEdge:
    """Grupo 4: Tests de casos edge y validaciones."""

    def test_13_crear_control_paciente_inexistente(self):
        """Test: Error al crear control para paciente que no existe."""
        paciente_falso = str(uuid4())
        
        datos_control = {
            "paciente_id": paciente_falso,
            "fecha_control": date.today().isoformat(),
            "tipo_cronicidad": "Hipertension",
            "estado_control": "Controlado"
        }
        
        response = client.post("/control-cronicidad/", json=datos_control)
        assert response.status_code == 400
        
        error = response.json()
        assert "El paciente especificado no existe" in error.get("detail", error.get("error", {}).get("message", ""))

    def test_14_obtener_control_inexistente(self):
        """Test: Error al obtener control que no existe."""
        control_falso = str(uuid4())
        
        response = client.get(f"/control-cronicidad/{control_falso}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Control de cronicidad no encontrado" in error.get("detail", error.get("error", {}).get("message", ""))

    def test_15_actualizar_control_inexistente(self):
        """Test: Error al actualizar control que no existe."""
        control_falso = str(uuid4())
        
        datos_actualizacion = {
            "estado_control": "Controlado"
        }
        
        response = client.put(f"/control-cronicidad/{control_falso}", json=datos_actualizacion)
        assert response.status_code == 404
        
        error = response.json()
        assert "Control de cronicidad no encontrado" in error.get("detail", error.get("error", {}).get("message", ""))

    def test_16_eliminar_control_cronicidad(self):
        """Test: Eliminar control de cronicidad exitosamente."""
        assert control_cronicidad_id_test is not None
        
        response = client.delete(f"/control-cronicidad/{control_cronicidad_id_test}")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response_get = client.get(f"/control-cronicidad/{control_cronicidad_id_test}")
        assert response_get.status_code == 404

    def test_17_eliminar_control_inexistente(self):
        """Test: Error al eliminar control que no existe."""
        control_falso = str(uuid4())
        
        response = client.delete(f"/control-cronicidad/{control_falso}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Control de cronicidad no encontrado" in error.get("detail", error.get("error", {}).get("message", ""))

# =============================================================================
# TESTS FUNCIONALIDAD INTEGRADA
# =============================================================================

class TestControlCronicidadIntegracion:
    """Grupo 5: Tests de integración y funcionalidad completa."""

    def test_18_flujo_completo_control_cronicidad(self):
        """Test: Flujo completo de gestión de control de cronicidad."""
        assert paciente_id_test_cc is not None
        
        # 1. Crear control inicial
        datos_inicial = {
            "paciente_id": paciente_id_test_cc,
            "fecha_control": date.today().isoformat(),
            "tipo_cronicidad": "ERC",
            "estado_control": "En proceso",
            "adherencia_tratamiento": "Regular",
            "peso_kg": 80.0,
            "talla_cm": 175.0,
            "observaciones": "Primera consulta ERC"
        }
        
        response_crear = client.post("/control-cronicidad/", json=datos_inicial)
        assert response_crear.status_code == 201
        control_id = response_crear.json()["id"]
        
        # 2. Verificar que aparece en listados
        response_lista = client.get("/control-cronicidad/tipo/ERC")
        assert response_lista.status_code == 200
        assert any(c["id"] == control_id for c in response_lista.json())
        
        # 3. Actualizar seguimiento
        datos_seguimiento = {
            "estado_control": "Controlado",
            "adherencia_tratamiento": "Buena",
            "observaciones": "Mejoría notable en función renal"
        }
        
        response_actualizar = client.put(f"/control-cronicidad/{control_id}", json=datos_seguimiento)
        assert response_actualizar.status_code == 200
        
        # 4. Verificar cambios en campos calculados
        control_actualizado = response_actualizar.json()
        assert control_actualizado["control_adecuado"] is True
        assert control_actualizado["adherencia_score"] == 85.0
        assert control_actualizado["proxima_cita_recomendada_dias"] == 120  # ERC controlada = 4 meses
        
        # 5. Verificar en estadísticas
        response_stats = client.get("/control-cronicidad/estadisticas/basicas")
        assert response_stats.status_code == 200
        stats = response_stats.json()
        assert stats["por_tipo_cronicidad"]["ERC"] >= 1
        
        # 6. Limpiar
        response_eliminar = client.delete(f"/control-cronicidad/{control_id}")
        assert response_eliminar.status_code == 204

    def test_19_validacion_campos_calculados_todos_tipos(self):
        """Test: Validar lógica de campos calculados para todos los tipos."""
        tipos_cronicidad = ["Hipertension", "Diabetes", "ERC", "Dislipidemia"]
        controles_creados = []
        
        for tipo in tipos_cronicidad:
            datos_control = {
                "paciente_id": paciente_id_test_cc,
                "fecha_control": date.today().isoformat(),
                "tipo_cronicidad": tipo,
                "estado_control": "Controlado",
                "adherencia_tratamiento": "Buena",
                "peso_kg": 70.0,
                "talla_cm": 170.0,
                "observaciones": f"Control de {tipo}"
            }
            
            response = client.post("/control-cronicidad/", json=datos_control)
            assert response.status_code == 201
            
            data = response.json()
            controles_creados.append(data["id"])
            
            # Validar campos calculados básicos
            assert data["tipo_cronicidad"] == tipo
            assert data["control_adecuado"] is True  # Controlado
            assert data["adherencia_score"] == 85.0  # Buena
            assert data["riesgo_cardiovascular"] == "Bajo"  # Todo bien
            
            # Validar próxima cita según tipo
            if tipo in ["Diabetes", "Hipertension"]:
                assert data["proxima_cita_recomendada_dias"] == 90  # 3 meses
            else:
                assert data["proxima_cita_recomendada_dias"] == 120  # 4 meses
        
        # Verificar que todos aparecen en estadísticas
        response_stats = client.get("/control-cronicidad/estadisticas/basicas")
        assert response_stats.status_code == 200
        stats = response_stats.json()
        
        for tipo in tipos_cronicidad:
            assert stats["por_tipo_cronicidad"][tipo] >= 1
        
        # Limpiar controles creados
        for control_id in controles_creados:
            client.delete(f"/control-cronicidad/{control_id}")