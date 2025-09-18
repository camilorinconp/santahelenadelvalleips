# =============================================================================
# Tests Atención Vejez - Arquitectura Vertical
# Tests independientes sin dependencias cruzadas
# Fecha: 17 septiembre 2025
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
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

def crear_paciente_test(numero_documento: str = None, edad_anos: int = 72):
    """Crear paciente de prueba y retornar su ID."""
    if numero_documento is None:
        numero_documento = generar_numero_documento_unico()

    # Calcular fecha de nacimiento para la edad deseada
    fecha_nacimiento = date.today().replace(year=date.today().year - edad_anos)

    paciente_data = {
        "tipo_documento": "CC",
        "numero_documento": numero_documento,
        "primer_nombre": "Test",
        "primer_apellido": "Vejez",
        "fecha_nacimiento": fecha_nacimiento.isoformat(),
        "genero": "MASCULINO"
    }

    response = client.post("/pacientes/", json=paciente_data)
    assert response.status_code == 201

    return response.json()["data"][0]["id"]

def crear_medico_test():
    """Crear médico de prueba y retornar su ID."""
    medico_data = {
        "nombre": "Dr. Test Vejez",
        "especialidad": "GERIATRIA",
        "numero_registro_medico": f"GM{random.randint(100000, 999999)}"
    }

    # Nota: Asumiendo que existe endpoint de médicos
    # Si no existe, usar UUID aleatorio
    return str(uuid4())

def crear_atencion_vejez_test_data(paciente_id: str):
    """Crear datos de atención vejez conforme Resolución 3280 - Art. 3.3.6 (Vejez 60+ años)."""
    return {
        # === CAMPOS BÁSICOS OBLIGATORIOS ===
        "paciente_id": paciente_id,
        "medico_id": crear_medico_test(),
        "fecha_atencion": date.today().isoformat(),
        "edad_anos": 72,  # Obligatorio: 60+ años
        "entorno": "CONSULTA_EXTERNA",

        # === ANTROPOMETRÍA Y SIGNOS VITALES ===
        "peso_kg": 65.0,
        "talla_cm": 165.0,
        "peso_perdido_6_meses_kg": 2.0,
        "presion_sistolica": 140.0,
        "presion_diastolica": 90.0,
        "frecuencia_cardiaca": 78,

        # === EVALUACIÓN COGNITIVA (Mini Mental State - Anexo 28) ===
        "mini_mental_score": 26,  # Resolución 3280: "Minimental State"
        "clock_test_score": 8,
        "memoria_inmediata": True,
        "orientacion_tiempo_lugar": True,
        "cambios_cognitivos_reportados": False,
        "dificultad_actividades_complejas": False,

        # === EVALUACIÓN RIESGO DE CAÍDAS ===
        "caidas_ultimo_ano": 1,
        "mareo_al_levantarse": False,
        "medicamentos_que_causan_mareo": 1,
        "problemas_vision": True,
        "problemas_audicion": False,
        "fuerza_muscular_disminuida": True,
        "equilibrio_alterado": False,
        "tiempo_up_and_go": 12.5,

        # === EVALUACIÓN AUTONOMÍA FUNCIONAL ===
        # Resolución 3280: "El índice de Barthel (Anexo 25)" y "La escala de Lawton-Brody (Anexo 26)"
        "barthel_score": 85,  # Índice de Barthel obligatorio
        "lawton_score": 6,    # Escala de Lawton-Brody obligatoria
        "independiente_bano": True,
        "independiente_vestirse": True,
        "independiente_comer": True,
        "independiente_movilidad": True,
        "maneja_medicamentos": False,
        "maneja_finanzas": True,
        "usa_transporte": False,

        # === EVALUACIÓN SALUD MENTAL ===
        "yesavage_score": 3,
        "estado_animo_deprimido": False,
        "perdida_interes_actividades": False,
        "trastornos_sueno": True,
        "sensacion_inutilidad": False,
        "ansiedad_frecuente": False,
        "aislamiento_social": False,
        "cambios_recientes_perdidas": False,

        # Soporte social
        "vive_solo": False,
        "tiene_cuidador": False,
        "frecuencia_visitas_familiares": 3,
        "participa_actividades_comunitarias": True,
        "tiene_amigos_cercanos": True,
        "ayuda_disponible_emergencia": True,
        "satisfaccion_relaciones_sociales": 7,

        # Polifarmacia
        "numero_medicamentos": 4,
        "medicamentos_alto_riesgo": 1,
        "automedicacion": False,
        "dificultad_manejo_medicamentos": True,
        "efectos_adversos_reportados": False,
        "interacciones_conocidas": False,

        # Incontinencia
        "incontinencia_urinaria": False,
        "incontinencia_fecal": False,

        # Estilos de vida
        "actividad_fisica_min_semana": 90,
        "porciones_frutas_verduras_dia": 4,
        "cigarrillos_dia": 0,
        "copas_alcohol_semana": 2,
        "actividades_estimulacion_cognitiva": True,

        # Factores ambientales
        "hogar_adaptado_seguro": True,
        "proposito_vida_claro": True,
        "participacion_social_activa": True,
        "control_medico_regular": True,

        # Observaciones
        "observaciones_generales": "Adulto mayor con factores de riesgo moderados",
        "entorno": "CONSULTA_EXTERNA"
    }

# =============================================================================
# TESTS CRUD BÁSICO
# =============================================================================

class TestAtencionVejezBasica:
    """Suite de tests para funcionalidad básica de Vejez."""

    def test_crear_atencion_vejez_basica(self):
        """Test crear atención Vejez básica."""
        # Crear paciente independiente
        paciente_id = crear_paciente_test()

        # Crear atención
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["paciente_id"] == paciente_id
        assert data["peso_kg"] == 65.0
        assert data["talla_cm"] == 165.0
        assert data["edad_anos"] == 72

        # Verificar campos calculados automáticamente
        assert "imc" in data
        assert "estado_nutricional" in data
        assert "deterioro_cognitivo" in data
        assert "riesgo_caidas" in data
        assert "autonomia_funcional" in data
        assert "salud_mental_vejez" in data
        assert "soporte_social" in data
        assert "polifarmacia_riesgo" in data
        assert "sindromes_geriatricos_identificados" in data
        assert "factores_protectores_identificados" in data
        assert "nivel_riesgo_global" in data
        assert "proxima_consulta_recomendada_dias" in data
        assert "completitud_evaluacion" in data

    def test_obtener_atencion_vejez_por_id(self):
        """Test obtener atención vejez por ID."""
        # Crear paciente y atención independientes
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]

        # Obtener por ID
        response = client.get(f"/atencion-vejez/{atencion_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == atencion_id
        assert data["paciente_id"] == paciente_id
        assert data["edad_anos"] == 72

    def test_listar_atenciones_vejez(self):
        """Test listar atenciones vejez."""
        response = client.get("/atencion-vejez/")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_listar_atenciones_vejez_por_paciente(self):
        """Test listar atenciones vejez filtradas por paciente."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201

        # Listar por paciente
        response = client.get(f"/atencion-vejez/?paciente_id={paciente_id}")
        assert response.status_code == 200

        data = response.json()
        assert len(data) >= 1
        assert all(atencion["paciente_id"] == paciente_id for atencion in data)

    def test_actualizar_atencion_vejez(self):
        """Test actualizar atención vejez."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]

        # Actualizar
        update_data = {
            "peso_kg": 63.0,
            "presion_sistolica": 130.0,
            "mini_mental_score": 28,
            "observaciones_generales": "Mejora en estado general del paciente"
        }

        response = client.put(f"/atencion-vejez/{atencion_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["peso_kg"] == 63.0
        assert data["presion_sistolica"] == 130.0
        assert data["mini_mental_score"] == 28
        assert "Mejora en estado general" in data["observaciones_generales"]

    def test_eliminar_atencion_vejez(self):
        """Test eliminar atención vejez."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]

        # Eliminar
        response = client.delete(f"/atencion-vejez/{atencion_id}")
        assert response.status_code == 200

        data = response.json()
        assert "eliminada exitosamente" in data["message"]

        # Verificar que no existe
        get_response = client.get(f"/atencion-vejez/{atencion_id}")
        assert get_response.status_code == 404

# =============================================================================
# TESTS FUNCIONALIDAD ESPECIALIZADA VEJEZ
# =============================================================================

class TestEvaluacionesEspecializadasVejez:
    """Tests para evaluaciones especializadas de vejez."""

    def test_evaluacion_deterioro_cognitivo_normal(self):
        """Test evaluación deterioro cognitivo normal."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican cognición normal
        atencion_data.update({
            "mini_mental_score": 28,
            "clock_test_score": 9,
            "memoria_inmediata": True,
            "orientacion_tiempo_lugar": True,
            "cambios_cognitivos_reportados": False,
            "dificultad_actividades_complejas": False
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["deterioro_cognitivo"] == "NORMAL"

    def test_evaluacion_deterioro_cognitivo_leve(self):
        """Test evaluación deterioro cognitivo leve."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican deterioro leve
        atencion_data.update({
            "mini_mental_score": 22,
            "clock_test_score": 7,
            "memoria_inmediata": True,
            "orientacion_tiempo_lugar": True,
            "cambios_cognitivos_reportados": True,
            "dificultad_actividades_complejas": False
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["deterioro_cognitivo"] in ["DETERIORO_LEVE", "DETERIORO_MODERADO"]

    def test_evaluacion_riesgo_caidas_bajo(self):
        """Test evaluación riesgo de caídas bajo."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican riesgo bajo
        atencion_data.update({
            "caidas_ultimo_ano": 0,
            "mareo_al_levantarse": False,
            "medicamentos_que_causan_mareo": 0,
            "problemas_vision": False,
            "problemas_audicion": False,
            "fuerza_muscular_disminuida": False,
            "equilibrio_alterado": False,
            "tiempo_up_and_go": 8.0
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["riesgo_caidas"] == "BAJO"

    def test_evaluacion_riesgo_caidas_alto(self):
        """Test evaluación riesgo de caídas alto."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican riesgo alto
        atencion_data.update({
            "caidas_ultimo_ano": 3,
            "mareo_al_levantarse": True,
            "medicamentos_que_causan_mareo": 4,
            "problemas_vision": True,
            "problemas_audicion": True,
            "fuerza_muscular_disminuida": True,
            "equilibrio_alterado": True,
            "tiempo_up_and_go": 25.0
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["riesgo_caidas"] in ["ALTO", "MUY_ALTO", "CRITICO", "REQUIERE_ATENCION_INMEDIATA"]

    def test_evaluacion_autonomia_funcional_independiente(self):
        """Test evaluación autonomía funcional independiente."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican independencia
        atencion_data.update({
            "barthel_score": 100,
            "lawton_score": 8,
            "independiente_bano": True,
            "independiente_vestirse": True,
            "independiente_comer": True,
            "independiente_movilidad": True,
            "maneja_medicamentos": True,
            "maneja_finanzas": True,
            "usa_transporte": True
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["autonomia_funcional"] == "INDEPENDIENTE"

    def test_evaluacion_autonomia_funcional_dependencia(self):
        """Test evaluación autonomía funcional con dependencia."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        # Datos que indican dependencia
        atencion_data.update({
            "barthel_score": 30,
            "lawton_score": 2,
            "independiente_bano": False,
            "independiente_vestirse": False,
            "independiente_comer": True,
            "independiente_movilidad": False,
            "maneja_medicamentos": False,
            "maneja_finanzas": False,
            "usa_transporte": False
        })

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 201

        data = response.json()
        assert data["autonomia_funcional"] in ["DEPENDENCIA_MODERADA", "DEPENDENCIA_SEVERA", "DEPENDENCIA_TOTAL"]

# =============================================================================
# TESTS ESTADÍSTICAS Y REPORTES
# =============================================================================

class TestEstadisticasVejez:
    """Tests para estadísticas y reportes de vejez."""

    def test_obtener_estadisticas_vejez(self):
        """Test obtener estadísticas básicas de vejez."""
        response = client.get("/atencion-vejez/estadisticas/")
        assert response.status_code == 200

        data = response.json()
        assert "total_atenciones" in data
        assert "distribuciones" in data
        assert "promedios" in data
        assert "alertas" in data

    def test_filtrar_por_deterioro_cognitivo(self):
        """Test filtrar atenciones por deterioro cognitivo."""
        response = client.get("/atencion-vejez/deterioro-cognitivo/NORMAL")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_filtrar_por_riesgo_caidas(self):
        """Test filtrar atenciones por riesgo de caídas."""
        response = client.get("/atencion-vejez/riesgo-caidas/BAJO")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_reporte_sindromes_geriatricos(self):
        """Test reporte de síndromes geriátricos."""
        response = client.get("/atencion-vejez/sindromes-geriatricos")
        assert response.status_code == 200

        data = response.json()
        assert "adultos_mayores_evaluados" in data
        assert "sindromes_prevalentes" in data
        assert "factores_riesgo_criticos" in data
        assert "oportunidades_intervencion" in data
        assert "recomendaciones" in data

    def test_atenciones_cronologicas_paciente(self):
        """Test obtener atenciones cronológicas de un paciente."""
        # Crear paciente y atención
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)

        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201

        # Obtener atenciones cronológicas
        response = client.get(f"/atencion-vejez/paciente/{paciente_id}/cronologico")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

# =============================================================================
# TESTS VALIDACIÓN DE DATOS
# =============================================================================

class TestValidacionDatosVejez:
    """Tests para validación de datos específicos de vejez."""

    def test_validacion_edad_minima(self):
        """Test validación edad mínima para vejez (60 años)."""
        paciente_id = crear_paciente_test(edad_anos=59)
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        atencion_data["edad_anos"] = 59

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 422  # Validation error

    def test_validacion_edad_maxima(self):
        """Test validación edad máxima para vejez (120 años)."""
        paciente_id = crear_paciente_test(edad_anos=121)
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        atencion_data["edad_anos"] = 121

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 422  # Validation error

    def test_validacion_mini_mental_score(self):
        """Test validación rango Mini-Mental Score."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        atencion_data["mini_mental_score"] = 35  # Fuera de rango (0-30)

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 422  # Validation error

    def test_validacion_barthel_score(self):
        """Test validación rango Barthel Score."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        atencion_data["barthel_score"] = 105  # Fuera de rango (0-100)

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 422  # Validation error

    def test_validacion_numero_medicamentos(self):
        """Test validación número de medicamentos."""
        paciente_id = crear_paciente_test()
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        atencion_data["numero_medicamentos"] = -1  # Valor negativo

        response = client.post("/atencion-vejez/", json=atencion_data)
        assert response.status_code == 422  # Validation error

# =============================================================================
# TESTS DE INTEGRACIÓN
# =============================================================================

class TestIntegracionVejez:
    """Tests de integración para el módulo vejez."""

    def test_flujo_completo_atencion_vejez(self):
        """Test flujo completo de atención vejez."""
        # 1. Crear paciente
        paciente_id = crear_paciente_test()

        # 2. Crear atención inicial
        atencion_data = crear_atencion_vejez_test_data(paciente_id)
        create_response = client.post("/atencion-vejez/", json=atencion_data)
        assert create_response.status_code == 201
        atencion_id = create_response.json()["id"]

        # 3. Obtener atención
        get_response = client.get(f"/atencion-vejez/{atencion_id}")
        assert get_response.status_code == 200

        # 4. Actualizar atención
        update_data = {"mini_mental_score": 25}
        update_response = client.put(f"/atencion-vejez/{atencion_id}", json=update_data)
        assert update_response.status_code == 200

        # 5. Verificar cálculos automáticos
        final_data = update_response.json()
        assert final_data["mini_mental_score"] == 25
        assert "deterioro_cognitivo" in final_data
        assert "nivel_riesgo_global" in final_data

        # 6. Eliminar atención
        delete_response = client.delete(f"/atencion-vejez/{atencion_id}")
        assert delete_response.status_code == 200