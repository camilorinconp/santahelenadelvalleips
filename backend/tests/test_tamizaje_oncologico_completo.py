# =============================================================================
# Tests Tamizaje Oncológico - Arquitectura Vertical Consolidada
# Implementación Growth Tier siguiendo patrón establecido
# Fecha: 16 septiembre 2025
# =============================================================================

import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from database import get_supabase_client

client = TestClient(app)

# --- Variables globales para IDs creados ---
paciente_id_test_to = None
tamizaje_oncologico_id_test = None
tamizaje_mama_id_test = None

# =============================================================================
# SETUP Y TEARDOWN
# =============================================================================

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_tamizaje_oncologico_test_data():
    """Setup: Crea un paciente para las pruebas. Teardown: lo elimina."""
    global paciente_id_test_to
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()

    # Crear Paciente de prueba
    datos_paciente = {
        "tipo_documento": "CC",
        "numero_documento": str(uuid4())[:10],
        "primer_nombre": "Paciente",
        "primer_apellido": "TO_Test",
        "fecha_nacimiento": "1975-01-01",
        "genero": "F"
    }
    response_paciente = client.post("/pacientes/", json=datos_paciente)
    assert response_paciente.status_code == 201, response_paciente.text
    paciente_id_test_to = response_paciente.json()["data"][0]["id"]

    yield # Ejecutar las pruebas

    # Teardown: Limpiar datos de prueba
    db_client = app.dependency_overrides.get(get_supabase_client, get_supabase_client)()
    if tamizaje_mama_id_test:
        # Buscar atención asociada antes de eliminar
        try:
            atencion_response = db_client.table("atenciones").select("id").eq("detalle_id", tamizaje_mama_id_test).execute()
            if atencion_response.data:
                for atencion in atencion_response.data:
                    db_client.table("atenciones").delete().eq("id", atencion["id"]).execute()
        except:
            pass
        db_client.table("tamizaje_oncologico").delete().eq("id", tamizaje_mama_id_test).execute()
    if tamizaje_oncologico_id_test:
        # Buscar atención asociada antes de eliminar
        try:
            atencion_response = db_client.table("atenciones").select("id").eq("detalle_id", tamizaje_oncologico_id_test).execute()
            if atencion_response.data:
                for atencion in atencion_response.data:
                    db_client.table("atenciones").delete().eq("id", atencion["id"]).execute()
        except:
            pass
        db_client.table("tamizaje_oncologico").delete().eq("id", tamizaje_oncologico_id_test).execute()
    if paciente_id_test_to:
        db_client.table("pacientes").delete().eq("id", paciente_id_test_to).execute()

# =============================================================================
# TESTS CRUD BÁSICO
# =============================================================================

class TestTamizajeOncologicoCRUD:
    """Grupo 1: Tests del CRUD básico de Tamizaje Oncológico."""

    def test_01_crear_tamizaje_cuello_uterino(self):
        """Test: Crear tamizaje de cuello uterino con campos calculados."""
        global tamizaje_oncologico_id_test
        assert paciente_id_test_to is not None

        datos_tamizaje = {
            "paciente_id": paciente_id_test_to,
            "fecha_tamizaje": date.today().isoformat(),
            "tipo_tamizaje": "Cuello Uterino",
            "resultado_tamizaje": "Negativo",
            "citologia_resultado": "Normal",
            "adn_vph_resultado": "Negativo",
            "colposcopia_realizada": False,
            "biopsia_realizada_cuello": False,
            "observaciones": "Tamizaje rutinario, resultados normales"
        }

        response = client.post("/tamizaje-oncologico/", json=datos_tamizaje)
        assert response.status_code == 201, response.text
        
        data = response.json()
        tamizaje_oncologico_id_test = data["id"]
        
        # Validar datos básicos
        assert data["paciente_id"] == paciente_id_test_to
        assert data["tipo_tamizaje"] == "Cuello Uterino"
        assert data["resultado_tamizaje"] == "Negativo"
        assert data["citologia_resultado"] == "Normal"
        assert data["adn_vph_resultado"] == "Negativo"
        
        # Validar campos calculados
        assert data["nivel_riesgo"] == "Bajo"  # Normal + Negativo = Bajo
        assert data["adherencia_tamizaje"] == "Buena"  # Fecha actual = Buena
        assert data["proxima_cita_recomendada_dias"] == 365  # Cuello Uterino bajo riesgo = 1 año
        assert data["completitud_tamizaje"] == 100.0  # Citología + VPH = 100%

    def test_02_obtener_tamizaje_por_id(self):
        """Test: Obtener tamizaje por ID con campos calculados."""
        assert tamizaje_oncologico_id_test is not None
        
        response = client.get(f"/tamizaje-oncologico/{tamizaje_oncologico_id_test}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == tamizaje_oncologico_id_test
        assert data["tipo_tamizaje"] == "Cuello Uterino"
        assert "nivel_riesgo" in data
        assert "adherencia_tamizaje" in data
        assert "proxima_cita_recomendada_dias" in data
        assert "completitud_tamizaje" in data

    def test_03_listar_tamizajes_con_filtros(self):
        """Test: Listar tamizajes con filtros avanzados."""
        # Sin filtros
        response = client.get("/tamizaje-oncologico/")
        assert response.status_code == 200
        tamizajes = response.json()
        assert len(tamizajes) >= 1
        
        # Con filtro por paciente
        response = client.get(f"/tamizaje-oncologico/?paciente_id={paciente_id_test_to}")
        assert response.status_code == 200
        tamizajes_paciente = response.json()
        assert len(tamizajes_paciente) >= 1
        assert all(t["paciente_id"] == paciente_id_test_to for t in tamizajes_paciente)
        
        # Con filtro por tipo
        response = client.get("/tamizaje-oncologico/?tipo_tamizaje=Cuello Uterino")
        assert response.status_code == 200
        tamizajes_cuello = response.json()
        assert all(t["tipo_tamizaje"] == "Cuello Uterino" for t in tamizajes_cuello)

    def test_04_actualizar_tamizaje_oncologico(self):
        """Test: Actualizar tamizaje oncológico con recálculo automático."""
        assert tamizaje_oncologico_id_test is not None
        
        datos_actualizacion = {
            "resultado_tamizaje": "Anormal",
            "citologia_resultado": "LSIL",  # Lesión de bajo grado
            "adn_vph_resultado": "Positivo",
            "colposcopia_realizada": True,
            "observaciones": "Requiere seguimiento por LSIL y VPH positivo"
        }
        
        response = client.put(f"/tamizaje-oncologico/{tamizaje_oncologico_id_test}", json=datos_actualizacion)
        assert response.status_code == 200
        
        data = response.json()
        
        # Validar cambios
        assert data["resultado_tamizaje"] == "Anormal"
        assert data["citologia_resultado"] == "LSIL"
        assert data["adn_vph_resultado"] == "Positivo"
        assert data["colposcopia_realizada"] is True
        
        # Validar recálculo de campos
        assert data["nivel_riesgo"] == "Moderado"  # LSIL + VPH+ = Moderado
        assert data["proxima_cita_recomendada_dias"] == 90  # Riesgo moderado = 3 meses

    def test_05_crear_tamizaje_mama_alto_riesgo(self):
        """Test: Crear tamizaje de mama con alto riesgo para verificar lógica específica."""
        global tamizaje_mama_id_test
        
        datos_mama = {
            "paciente_id": paciente_id_test_to,
            "fecha_tamizaje": date.today().isoformat(),
            "tipo_tamizaje": "Mama",
            "resultado_tamizaje": "Anormal",
            "mamografia_resultado": "BI-RADS 5",  # Alto riesgo
            "examen_clinico_mama_observaciones": "Masa palpable en cuadrante superior externo",
            "biopsia_realizada_mama": True,
            "observaciones": "Requiere evaluación oncológica urgente"
        }
        
        response = client.post("/tamizaje-oncologico/", json=datos_mama)
        assert response.status_code == 201
        
        data = response.json()
        tamizaje_mama_id_test = data["id"]
        
        # Validar tipo específico
        assert data["tipo_tamizaje"] == "Mama"
        
        # Validar lógica específica para mama
        assert data["nivel_riesgo"] == "Alto"  # BI-RADS 5 = Alto
        assert data["proxima_cita_recomendada_dias"] == 30  # Alto riesgo = 1 mes
        assert data["completitud_tamizaje"] == 100.0  # Mamografía + examen clínico = 100%

# =============================================================================
# TESTS ENDPOINTS ESPECIALIZADOS  
# =============================================================================

class TestTamizajeOncologicoEndpointsEspecializados:
    """Grupo 2: Tests de endpoints especializados por tipo y paciente."""

    def test_06_listar_por_tipo_tamizaje_valido(self):
        """Test: Endpoint especializado por tipo de tamizaje."""
        response = client.get("/tamizaje-oncologico/tipo/Cuello Uterino")
        assert response.status_code == 200
        
        tamizajes = response.json()
        # Debe tener al menos el tamizaje que creamos
        assert len(tamizajes) >= 1
        assert all(t["tipo_tamizaje"] == "Cuello Uterino" for t in tamizajes)

    def test_07_listar_por_tipo_tamizaje_invalido(self):
        """Test: Endpoint con tipo de tamizaje inválido."""
        response = client.get("/tamizaje-oncologico/tipo/TipoInvalido")
        assert response.status_code == 400
        
        error = response.json()
        assert "Tipo de tamizaje no válido" in error.get("detail", "")

    def test_08_obtener_tamizajes_cronologicos_paciente(self):
        """Test: Historial cronológico de tamizajes de un paciente."""
        assert paciente_id_test_to is not None
        
        response = client.get(f"/tamizaje-oncologico/paciente/{paciente_id_test_to}/cronologicos")
        assert response.status_code == 200
        
        tamizajes = response.json()
        assert len(tamizajes) >= 2  # Tenemos Cuello Uterino + Mama
        
        # Verificar orden cronológico ascendente
        fechas = [t["fecha_tamizaje"] for t in tamizajes]
        assert fechas == sorted(fechas)
        
        # Verificar que todos pertenecen al paciente
        assert all(t["paciente_id"] == paciente_id_test_to for t in tamizajes)

    def test_09_obtener_tamizajes_cronologicos_con_filtro_tipo(self):
        """Test: Historial cronológico filtrado por tipo específico."""
        assert paciente_id_test_to is not None
        
        response = client.get(f"/tamizaje-oncologico/paciente/{paciente_id_test_to}/cronologicos?tipo_tamizaje=Mama")
        assert response.status_code == 200
        
        tamizajes = response.json()
        assert len(tamizajes) >= 1
        assert all(t["tipo_tamizaje"] == "Mama" for t in tamizajes)

# =============================================================================
# TESTS ESTADÍSTICAS Y REPORTES
# =============================================================================

class TestTamizajeOncologicoEstadisticasReportes:
    """Grupo 3: Tests de estadísticas y reportes."""

    def test_10_obtener_estadisticas_basicas(self):
        """Test: Endpoint de estadísticas básicas de Tamizaje Oncológico."""
        response = client.get("/tamizaje-oncologico/estadisticas/basicas")
        assert response.status_code == 200
        
        stats = response.json()
        
        # Validar estructura
        assert "resumen_general" in stats
        assert "por_tipo_tamizaje" in stats
        assert "resultados" in stats
        assert "seguimiento" in stats
        assert "fecha_calculo" in stats
        
        # Validar resumen general
        resumen = stats["resumen_general"]
        assert "total_tamizajes" in resumen
        assert "porcentaje_positivos" in resumen
        assert "porcentaje_seguimiento_especializado" in resumen
        assert resumen["total_tamizajes"] >= 2  # Tenemos al menos 2 tamizajes
        
        # Validar por tipo
        por_tipo = stats["por_tipo_tamizaje"]
        assert "Cuello Uterino" in por_tipo
        assert "Mama" in por_tipo
        assert "Prostata" in por_tipo
        assert "Colon y Recto" in por_tipo
        assert por_tipo["Cuello Uterino"] >= 1
        assert por_tipo["Mama"] >= 1
        
        # Validar resultados
        resultados = stats["resultados"]
        assert "positivos_anormales" in resultados
        assert "negativos" in resultados
        assert "pendientes" in resultados

    def test_11_reporte_adherencia_sin_filtros(self):
        """Test: Reporte de adherencia sin filtros."""
        response = client.get("/tamizaje-oncologico/reportes/adherencia")
        assert response.status_code == 200
        
        reporte = response.json()
        
        # Validar estructura
        assert "parametros_reporte" in reporte
        assert "adherencia_absolutos" in reporte
        assert "adherencia_porcentajes" in reporte
        assert "fecha_generacion" in reporte
        
        # Validar parámetros
        params = reporte["parametros_reporte"]
        assert params["tipo_tamizaje"] == "Todos"
        assert params["total_tamizajes_analizados"] >= 2
        
        # Validar categorías de adherencia
        absolutos = reporte["adherencia_absolutos"]
        assert "Buena" in absolutos
        assert "Regular" in absolutos
        assert "Mala" in absolutos
        assert "No evaluada" in absolutos
        
        # Validar que tenemos datos
        assert absolutos["Buena"] >= 1  # Tamizajes recientes
        
        # Validar porcentajes suman lógicamente
        porcentajes = reporte["adherencia_porcentajes"]
        total_porcentaje = sum(porcentajes.values())
        assert 99.0 <= total_porcentaje <= 101.0  # Tolerancia por redondeo

    def test_12_reporte_adherencia_con_filtros(self):
        """Test: Reporte de adherencia con filtros específicos."""
        # Filtro por tipo
        response = client.get("/tamizaje-oncologico/reportes/adherencia?tipo_tamizaje=Cuello Uterino")
        assert response.status_code == 200
        
        reporte = response.json()
        params = reporte["parametros_reporte"]
        assert params["tipo_tamizaje"] == "Cuello Uterino"
        assert params["total_tamizajes_analizados"] >= 1
        
        # Filtro por fechas
        fecha_hoy = date.today().isoformat()
        response = client.get(f"/tamizaje-oncologico/reportes/adherencia?fecha_desde={fecha_hoy}&fecha_hasta={fecha_hoy}")
        assert response.status_code == 200
        
        reporte_fechas = response.json()
        params_fechas = reporte_fechas["parametros_reporte"]
        assert params_fechas["fecha_desde"] == fecha_hoy
        assert params_fechas["fecha_hasta"] == fecha_hoy

# =============================================================================
# TESTS CASOS EDGE Y VALIDACIONES
# =============================================================================

class TestTamizajeOncologicoCasosEdge:
    """Grupo 4: Tests de casos edge y validaciones."""

    def test_13_crear_tamizaje_paciente_inexistente(self):
        """Test: Error al crear tamizaje para paciente que no existe."""
        paciente_falso = str(uuid4())
        
        datos_tamizaje = {
            "paciente_id": paciente_falso,
            "fecha_tamizaje": date.today().isoformat(),
            "tipo_tamizaje": "Cuello Uterino",
            "resultado_tamizaje": "Negativo"
        }
        
        response = client.post("/tamizaje-oncologico/", json=datos_tamizaje)
        assert response.status_code == 400
        
        error = response.json()
        assert "El paciente especificado no existe" in error.get("detail", "")

    def test_14_obtener_tamizaje_inexistente(self):
        """Test: Error al obtener tamizaje que no existe."""
        tamizaje_falso = str(uuid4())
        
        response = client.get(f"/tamizaje-oncologico/{tamizaje_falso}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Tamizaje oncológico no encontrado" in error.get("detail", "")

    def test_15_actualizar_tamizaje_inexistente(self):
        """Test: Error al actualizar tamizaje que no existe."""
        tamizaje_falso = str(uuid4())
        
        datos_actualizacion = {
            "resultado_tamizaje": "Positivo"
        }
        
        response = client.put(f"/tamizaje-oncologico/{tamizaje_falso}", json=datos_actualizacion)
        assert response.status_code == 404
        
        error = response.json()
        assert "Tamizaje oncológico no encontrado" in error.get("detail", "")

    def test_16_eliminar_tamizaje_oncologico(self):
        """Test: Eliminar tamizaje oncológico exitosamente."""
        assert tamizaje_oncologico_id_test is not None
        
        response = client.delete(f"/tamizaje-oncologico/{tamizaje_oncologico_id_test}")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response_get = client.get(f"/tamizaje-oncologico/{tamizaje_oncologico_id_test}")
        assert response_get.status_code == 404

    def test_17_eliminar_tamizaje_inexistente(self):
        """Test: Error al eliminar tamizaje que no existe."""
        tamizaje_falso = str(uuid4())
        
        response = client.delete(f"/tamizaje-oncologico/{tamizaje_falso}")
        assert response.status_code == 404
        
        error = response.json()
        assert "Tamizaje oncológico no encontrado" in error.get("detail", "")

# =============================================================================
# TESTS FUNCIONALIDAD INTEGRADA
# =============================================================================

class TestTamizajeOncologicoIntegracion:
    """Grupo 5: Tests de integración y funcionalidad completa."""

    def test_18_flujo_completo_tamizaje_prostata(self):
        """Test: Flujo completo de gestión de tamizaje prostático."""
        assert paciente_id_test_to is not None
        
        # 1. Crear tamizaje inicial
        datos_inicial = {
            "paciente_id": paciente_id_test_to,
            "fecha_tamizaje": date.today().isoformat(),
            "tipo_tamizaje": "Prostata",
            "resultado_tamizaje": "Negativo",
            "psa_resultado": 2.5,
            "tacto_rectal_resultado": "Normal",
            "biopsia_realizada_prostata": False,
            "observaciones": "Tamizaje rutinario, resultados normales"
        }
        
        response_crear = client.post("/tamizaje-oncologico/", json=datos_inicial)
        assert response_crear.status_code == 201
        tamizaje_id = response_crear.json()["id"]
        
        # 2. Verificar que aparece en listados
        response_lista = client.get("/tamizaje-oncologico/tipo/Prostata")
        assert response_lista.status_code == 200
        assert any(t["id"] == tamizaje_id for t in response_lista.json())
        
        # 3. Actualizar con resultados alarmantes
        datos_seguimiento = {
            "resultado_tamizaje": "Anormal",
            "psa_resultado": 12.0,  # PSA elevado
            "tacto_rectal_resultado": "Anormal",
            "biopsia_realizada_prostata": True,
            "observaciones": "PSA elevado, tacto anormal - biopsia realizada"
        }
        
        response_actualizar = client.put(f"/tamizaje-oncologico/{tamizaje_id}", json=datos_seguimiento)
        assert response_actualizar.status_code == 200
        
        # 4. Verificar cambios en campos calculados
        tamizaje_actualizado = response_actualizar.json()
        assert tamizaje_actualizado["nivel_riesgo"] == "Alto"  # PSA > 10 = Alto
        assert tamizaje_actualizado["proxima_cita_recomendada_dias"] == 30  # Alto riesgo = 1 mes
        assert tamizaje_actualizado["completitud_tamizaje"] == 100.0  # PSA + tacto = 100%
        
        # 5. Verificar en estadísticas
        response_stats = client.get("/tamizaje-oncologico/estadisticas/basicas")
        assert response_stats.status_code == 200
        stats = response_stats.json()
        assert stats["por_tipo_tamizaje"]["Prostata"] >= 1
        
        # 6. Limpiar
        response_eliminar = client.delete(f"/tamizaje-oncologico/{tamizaje_id}")
        assert response_eliminar.status_code == 204

    def test_19_validacion_campos_calculados_todos_tipos(self):
        """Test: Validar lógica de campos calculados para todos los tipos."""
        tipos_tamizaje = ["Cuello Uterino", "Mama", "Prostata", "Colon y Recto"]
        tamizajes_creados = []
        
        for tipo in tipos_tamizaje:
            datos_tamizaje = {
                "paciente_id": paciente_id_test_to,
                "fecha_tamizaje": date.today().isoformat(),
                "tipo_tamizaje": tipo,
                "resultado_tamizaje": "Negativo",
                "observaciones": f"Tamizaje de {tipo}"
            }
            
            # Añadir campos específicos por tipo
            if tipo == "Cuello Uterino":
                datos_tamizaje.update({
                    "citologia_resultado": "Normal",
                    "adn_vph_resultado": "Negativo"
                })
            elif tipo == "Mama":
                datos_tamizaje.update({
                    "mamografia_resultado": "BI-RADS 1",
                    "examen_clinico_mama_observaciones": "Normal"
                })
            elif tipo == "Prostata":
                datos_tamizaje.update({
                    "psa_resultado": 2.0,
                    "tacto_rectal_resultado": "Normal"
                })
            elif tipo == "Colon y Recto":
                datos_tamizaje.update({
                    "sangre_oculta_heces_resultado": "Negativo"
                })
            
            response = client.post("/tamizaje-oncologico/", json=datos_tamizaje)
            assert response.status_code == 201
            
            data = response.json()
            tamizajes_creados.append(data["id"])
            
            # Validar campos calculados básicos
            assert data["tipo_tamizaje"] == tipo
            assert data["nivel_riesgo"] == "Bajo"  # Todos normales/negativos
            assert data["adherencia_tamizaje"] == "Buena"  # Fecha actual
            assert data["completitud_tamizaje"] == 100.0  # Campos requeridos completados
            
            # Validar próxima cita según tipo
            if tipo in ["Cuello Uterino", "Prostata"]:
                assert data["proxima_cita_recomendada_dias"] == 365  # 1 año
            elif tipo == "Mama":
                assert data["proxima_cita_recomendada_dias"] == 730  # 2 años
            elif tipo == "Colon y Recto":
                assert data["proxima_cita_recomendada_dias"] == 1095  # 3 años
        
        # Verificar que todos aparecen en estadísticas
        response_stats = client.get("/tamizaje-oncologico/estadisticas/basicas")
        assert response_stats.status_code == 200
        stats = response_stats.json()
        
        for tipo in tipos_tamizaje:
            assert stats["por_tipo_tamizaje"][tipo] >= 1
        
        # Limpiar tamizajes creados
        for tamizaje_id in tamizajes_creados:
            client.delete(f"/tamizaje-oncologico/{tamizaje_id}")

# =============================================================================
# TESTS COMPATIBILIDAD LEGACY
# =============================================================================

class TestTamizajeOncologicoCompatibilidad:
    """Grupo 6: Tests de compatibilidad con implementación anterior."""

    def test_20_endpoint_legacy_crear_tamizaje(self):
        """Test: Endpoint legacy para crear tamizaje (compatibilidad)."""
        datos_legacy = {
            "paciente_id": paciente_id_test_to,
            "fecha_tamizaje": date.today().isoformat(),
            "tipo_tamizaje": "Citología",
            "resultado": "Negativo para lesión intraepitelial o malignidad"
        }

        response = client.post("/tamizaje-oncologico/tamizajes-oncologicos/", json=datos_legacy)
        assert response.status_code == 201
        
        data = response.json()
        assert data["paciente_id"] == paciente_id_test_to
        assert data["tipo_tamizaje"] == "Citología"
        
        # Limpiar
        client.delete(f"/tamizaje-oncologico/{data['id']}")

    def test_21_endpoint_legacy_listar_tamizajes(self):
        """Test: Endpoint legacy para listar tamizajes (compatibilidad)."""
        response = client.get("/tamizaje-oncologico/tamizajes-oncologicos/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)