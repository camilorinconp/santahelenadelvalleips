# =============================================================================
# Servicio Atención Vejez - Sprint #3: CENTRALIZACIÓN TOTAL
# Fecha: 17 septiembre 2025
# Objetivo: Aplicar sugerencias del Asesor Externo - CENTRALIZACIÓN TOTAL
# Evolución: Sprint Piloto #1 → Sprint #2 → Sprint #3 (Perfeccionado)
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.6 (Vejez 60+ años)
#
# MEJORAS SPRINT #3:
# ✅ CRUD COMPLETO CENTRALIZADO: Todas las operaciones en service layer
# ✅ VALIDACIONES TOTALES: Create, Read, Update, Delete + validaciones específicas
# ✅ CONSISTENCY TOTAL: Patrón idéntico a control_cronicidad perfeccionado
# ✅ ZERO BUSINESS LOGIC EN ENDPOINTS: Delegación 100% centralizada
# =============================================================================

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from uuid import UUID
from models.atencion_vejez_model_fixed import AtencionVejezCrear, AtencionVejezActualizar, AtencionVejezResponse
from database import get_supabase_client

class AtencionVejezService:
    """
    Servicio centralizado para lógica de negocio de atención vejez.

    RESUELVE:
    - Fragmentación de lógica identificada en auditoría backend
    - Separación de inquietudes (Separation of Concerns)
    - Reutilización de código entre endpoints

    PATRONES IMPLEMENTADOS:
    - Service Layer Pattern
    - Business Logic centralized
    - RPC Transactional operations
    """

    @staticmethod
    def validar_datos_vejez(atencion_data: AtencionVejezCrear) -> None:
        """
        Validar datos específicos de atención vejez según Resolución 3280.

        Args:
            atencion_data: Datos de entrada para validar

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación edad mínima vejez (60+ años)
        if atencion_data.edad_anos < 60:
            raise ValueError("La atención vejez requiere edad mínima de 60 años")

        # Validación consistencia antropométrica
        if atencion_data.peso_kg and atencion_data.talla_cm:
            imc = atencion_data.peso_kg / (atencion_data.talla_cm / 100) ** 2
            if imc < 10 or imc > 60:
                raise ValueError("IMC calculado fuera de rango válido (10-60)")

        # Validación coherencia evaluación cognitiva
        if atencion_data.mini_mental_score is not None:
            if atencion_data.mini_mental_score < 10 and not atencion_data.cambios_cognitivos_reportados:
                raise ValueError("Puntaje Mini Mental bajo debe ir acompañado de cambios cognitivos reportados")

        # Validación coherencia riesgo caídas
        if atencion_data.caidas_ultimo_ano and atencion_data.caidas_ultimo_ano > 0:
            if atencion_data.tiempo_up_and_go and atencion_data.tiempo_up_and_go < 10:
                raise ValueError("Historial de caídas inconsistente con tiempo up-and-go normal")

    @staticmethod
    def calcular_indicadores_vejez(atencion_data: AtencionVejezCrear) -> Dict[str, Any]:
        """
        Calcular indicadores y métricas específicas de vejez.

        Args:
            atencion_data: Datos de atención vejez

        Returns:
            Dict con indicadores calculados
        """
        indicadores = {}

        # Calcular IMC si hay datos
        if atencion_data.peso_kg and atencion_data.talla_cm:
            imc = atencion_data.peso_kg / (atencion_data.talla_cm / 100) ** 2
            indicadores["imc_calculado"] = round(imc, 2)

        # Calcular score riesgo caídas
        riesgo_caidas_score = 0
        if atencion_data.caidas_ultimo_ano:
            riesgo_caidas_score += atencion_data.caidas_ultimo_ano
        if atencion_data.mareo_al_levantarse:
            riesgo_caidas_score += 2
        if atencion_data.problemas_vision:
            riesgo_caidas_score += 2
        if atencion_data.equilibrio_alterado:
            riesgo_caidas_score += 3

        indicadores["riesgo_caidas_score"] = riesgo_caidas_score

        # Calcular score autonomía funcional
        autonomia_score = 0
        campos_autonomia = [
            atencion_data.independiente_bano,
            atencion_data.independiente_vestirse,
            atencion_data.independiente_comer,
            atencion_data.independiente_movilidad,
            atencion_data.maneja_medicamentos,
            atencion_data.maneja_finanzas,
            atencion_data.usa_transporte
        ]
        autonomia_score = sum(1 for campo in campos_autonomia if campo)
        indicadores["autonomia_funcional_score"] = autonomia_score

        # Identificar síndromes geriátricos
        sindromes = []
        if atencion_data.peso_perdido_6_meses_kg and atencion_data.peso_perdido_6_meses_kg >= 4.5:
            sindromes.append("FRAGILIDAD")
        if atencion_data.incontinencia_urinaria or atencion_data.incontinencia_fecal:
            sindromes.append("INCONTINENCIA")
        if riesgo_caidas_score >= 6:
            sindromes.append("INESTABILIDAD_CAIDAS")
        if atencion_data.numero_medicamentos and atencion_data.numero_medicamentos >= 10:
            sindromes.append("IATROGENIA")

        indicadores["sindromes_geriatricos"] = sindromes

        return indicadores

    @staticmethod
    def generar_recomendaciones_vejez(atencion_data: AtencionVejezCrear) -> List[str]:
        """
        Generar recomendaciones específicas basadas en la evaluación.

        Args:
            atencion_data: Datos de atención vejez

        Returns:
            Lista de recomendaciones personalizadas
        """
        recomendaciones = []

        # Recomendaciones por deterioro cognitivo
        if atencion_data.mini_mental_score and atencion_data.mini_mental_score < 21:
            recomendaciones.append("Referir a neurología para evaluación cognitiva especializada")
            recomendaciones.append("Implementar actividades de estimulación cognitiva diarias")

        # Recomendaciones por riesgo caídas
        if atencion_data.caidas_ultimo_ano and atencion_data.caidas_ultimo_ano > 2:
            recomendaciones.append("Evaluación por fisioterapia para programa de prevención caídas")
            recomendaciones.append("Revisión ambiental del hogar para adaptaciones de seguridad")

        # Recomendaciones por polifarmacia
        if atencion_data.numero_medicamentos and atencion_data.numero_medicamentos >= 5:
            recomendaciones.append("Revisión farmacológica con médico geriatra")
            recomendaciones.append("Educación en manejo seguro de medicamentos")

        # Recomendaciones por estado nutricional
        if atencion_data.peso_kg and atencion_data.talla_cm:
            imc = atencion_data.peso_kg / (atencion_data.talla_cm / 100) ** 2
            if imc < 22:
                recomendaciones.append("Evaluación nutricional para plan de recuperación ponderal")
            elif imc > 30:
                recomendaciones.append("Plan nutricional para reducción de peso supervisada")

        # Recomendaciones por aislamiento social
        if atencion_data.vive_solo and not atencion_data.ayuda_disponible_emergencia:
            recomendaciones.append("Activar red de apoyo social y familiar")
            recomendaciones.append("Vincular a programas comunitarios para adultos mayores")

        # Recomendaciones por salud mental
        if atencion_data.estado_animo_deprimido and atencion_data.perdida_interes_actividades:
            recomendaciones.append("Evaluación por psicología o psiquiatría")
            recomendaciones.append("Implementar actividades de propósito de vida")

        return recomendaciones

    @staticmethod
    async def crear_atencion_vejez_completa(atencion_data: AtencionVejezCrear) -> AtencionVejezResponse:
        """
        Crear atención vejez completa usando RPC transaccional y lógica de negocio centralizada.

        Args:
            atencion_data: Datos para crear la atención

        Returns:
            Atención vejez creada con indicadores calculados

        Raises:
            ValueError: Si validaciones fallan
            Exception: Si error en creación
        """
        # PASO 1: Validaciones de negocio centralizadas
        AtencionVejezService.validar_datos_vejez(atencion_data)

        # PASO 2: Calcular indicadores pre-creación
        indicadores = AtencionVejezService.calcular_indicadores_vejez(atencion_data)

        # PASO 3: Generar recomendaciones
        recomendaciones = AtencionVejezService.generar_recomendaciones_vejez(atencion_data)

        # PASO 4: Preparar datos para RPC
        db = get_supabase_client()

        # Agregar recomendaciones al plan si no existe
        plan_final = atencion_data.plan_promocion_prevencion or ""
        if recomendaciones:
            plan_final += "\n\nRECOMENDACIONES AUTOMÁTICAS:\n"
            plan_final += "\n".join(f"- {rec}" for rec in recomendaciones)

        # Preparar parámetros para RPC
        rpc_params = {
            "p_paciente_id": str(atencion_data.paciente_id),
            "p_medico_id": str(atencion_data.medico_id),
            "p_fecha_atencion": atencion_data.fecha_atencion.isoformat(),
            "p_entorno": atencion_data.entorno,
            "p_edad_anos": atencion_data.edad_anos,

            # Antropometría
            "p_peso_kg": atencion_data.peso_kg,
            "p_talla_cm": atencion_data.talla_cm,
            "p_peso_perdido_6_meses_kg": atencion_data.peso_perdido_6_meses_kg,
            "p_presion_sistolica": atencion_data.presion_sistolica,
            "p_presion_diastolica": atencion_data.presion_diastolica,
            "p_frecuencia_cardiaca": atencion_data.frecuencia_cardiaca,

            # Evaluación cognitiva
            "p_mini_mental_score": atencion_data.mini_mental_score,
            "p_clock_test_score": atencion_data.clock_test_score,
            "p_memoria_inmediata": atencion_data.memoria_inmediata,
            "p_orientacion_tiempo_lugar": atencion_data.orientacion_tiempo_lugar,
            "p_cambios_cognitivos_reportados": atencion_data.cambios_cognitivos_reportados,
            "p_dificultad_actividades_complejas": atencion_data.dificultad_actividades_complejas,

            # Evaluación riesgo caídas
            "p_caidas_ultimo_ano": atencion_data.caidas_ultimo_ano or 0,
            "p_mareo_al_levantarse": atencion_data.mareo_al_levantarse,
            "p_medicamentos_que_causan_mareo": atencion_data.medicamentos_que_causan_mareo or 0,
            "p_problemas_vision": atencion_data.problemas_vision,
            "p_problemas_audicion": atencion_data.problemas_audicion,
            "p_fuerza_muscular_disminuida": atencion_data.fuerza_muscular_disminuida,
            "p_equilibrio_alterado": atencion_data.equilibrio_alterado,
            "p_tiempo_up_and_go": atencion_data.tiempo_up_and_go,

            # Autonomía funcional
            "p_barthel_score": atencion_data.barthel_score,
            "p_lawton_score": atencion_data.lawton_score,
            "p_independiente_bano": atencion_data.independiente_bano,
            "p_independiente_vestirse": atencion_data.independiente_vestirse,
            "p_independiente_comer": atencion_data.independiente_comer,
            "p_independiente_movilidad": atencion_data.independiente_movilidad,
            "p_maneja_medicamentos": atencion_data.maneja_medicamentos,
            "p_maneja_finanzas": atencion_data.maneja_finanzas,
            "p_usa_transporte": atencion_data.usa_transporte,

            # Salud mental
            "p_yesavage_score": atencion_data.yesavage_score,
            "p_estado_animo_deprimido": atencion_data.estado_animo_deprimido,
            "p_perdida_interes_actividades": atencion_data.perdida_interes_actividades,
            "p_trastornos_sueno": atencion_data.trastornos_sueno,
            "p_sensacion_inutilidad": atencion_data.sensacion_inutilidad,
            "p_ansiedad_frecuente": atencion_data.ansiedad_frecuente,
            "p_aislamiento_social": atencion_data.aislamiento_social,
            "p_cambios_recientes_perdidas": atencion_data.cambios_recientes_perdidas,

            # Soporte social
            "p_vive_solo": atencion_data.vive_solo,
            "p_tiene_cuidador": atencion_data.tiene_cuidador,
            "p_frecuencia_visitas_familiares": atencion_data.frecuencia_visitas_familiares or 0,
            "p_participa_actividades_comunitarias": atencion_data.participa_actividades_comunitarias,
            "p_tiene_amigos_cercanos": atencion_data.tiene_amigos_cercanos,
            "p_ayuda_disponible_emergencia": atencion_data.ayuda_disponible_emergencia,
            "p_satisfaccion_relaciones_sociales": atencion_data.satisfaccion_relaciones_sociales or 5,

            # Polifarmacia
            "p_numero_medicamentos": atencion_data.numero_medicamentos or 0,
            "p_medicamentos_alto_riesgo": atencion_data.medicamentos_alto_riesgo or 0,
            "p_automedicacion": atencion_data.automedicacion,
            "p_dificultad_manejo_medicamentos": atencion_data.dificultad_manejo_medicamentos,
            "p_efectos_adversos_reportados": atencion_data.efectos_adversos_reportados,
            "p_interacciones_conocidas": atencion_data.interacciones_conocidas,

            # Incontinencia
            "p_incontinencia_urinaria": atencion_data.incontinencia_urinaria,
            "p_incontinencia_fecal": atencion_data.incontinencia_fecal,

            # Estilos de vida
            "p_actividad_fisica_min_semana": atencion_data.actividad_fisica_min_semana or 0,
            "p_porciones_frutas_verduras_dia": atencion_data.porciones_frutas_verduras_dia or 0,
            "p_cigarrillos_dia": atencion_data.cigarrillos_dia or 0,
            "p_copas_alcohol_semana": atencion_data.copas_alcohol_semana or 0,
            "p_actividades_estimulacion_cognitiva": atencion_data.actividades_estimulacion_cognitiva,

            # Factores ambientales
            "p_hogar_adaptado_seguro": atencion_data.hogar_adaptado_seguro,
            "p_proposito_vida_claro": atencion_data.proposito_vida_claro,
            "p_participacion_social_activa": atencion_data.participacion_social_activa,
            "p_control_medico_regular": atencion_data.control_medico_regular,

            # Observaciones con recomendaciones integradas
            "p_observaciones_generales": atencion_data.observaciones_generales,
            "p_plan_promocion_prevencion": plan_final,
            "p_educacion_cuidado_vejez": atencion_data.educacion_cuidado_vejez
        }

        # PASO 5: Ejecutar RPC transaccional
        response = db.rpc("crear_atencion_vejez_completa", rpc_params).execute()

        if not response.data or len(response.data) == 0:
            raise Exception("Error ejecutando RPC transaccional para atención vejez")

        # PASO 6: Obtener registro completo
        rpc_result = response.data[0]
        vejez_id = rpc_result["vejez_id"]

        vejez_complete = db.table("atencion_vejez").select("*").eq("id", vejez_id).execute()

        if not vejez_complete.data:
            raise Exception("Error obteniendo atención vejez creada")

        return AtencionVejezResponse(**vejez_complete.data[0])

    @staticmethod
    async def obtener_atencion_vejez_por_id(atencion_id: UUID) -> AtencionVejezResponse:
        """
        Obtener atención vejez por ID con validaciones de negocio centralizadas.

        Args:
            atencion_id: ID de la atención a buscar

        Returns:
            Atención vejez encontrada

        Raises:
            ValueError: Si la atención no existe
            Exception: Si error en consulta
        """
        db = get_supabase_client()

        response = db.table("atencion_vejez").select("*").eq("id", str(atencion_id)).execute()

        if not response.data:
            raise ValueError("Atención vejez no encontrada")

        return AtencionVejezResponse(**response.data[0])

    @staticmethod
    async def listar_atenciones_vejez(skip: int = 0, limit: int = 100) -> List[AtencionVejezResponse]:
        """
        Listar atenciones vejez con paginación y validaciones centralizadas.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de atenciones vejez

        Raises:
            ValueError: Si parámetros inválidos
            Exception: Si error en consulta
        """
        # Validaciones de negocio centralizadas
        if skip < 0:
            raise ValueError("skip debe ser mayor o igual a 0")
        if limit < 1 or limit > 1000:
            raise ValueError("limit debe estar entre 1 y 1000")

        db = get_supabase_client()

        response = db.table("atencion_vejez").select("*").range(skip, skip + limit - 1).execute()

        return [AtencionVejezResponse(**item) for item in response.data]

    @staticmethod
    async def listar_atenciones_vejez_por_paciente(paciente_id: UUID) -> List[AtencionVejezResponse]:
        """
        Listar atenciones vejez por paciente con validaciones centralizadas.

        Args:
            paciente_id: ID del paciente

        Returns:
            Lista de atenciones vejez del paciente

        Raises:
            Exception: Si error en consulta
        """
        db = get_supabase_client()

        response = db.table("atencion_vejez").select("*").eq("paciente_id", str(paciente_id)).order("fecha_atencion", desc=True).execute()

        return [AtencionVejezResponse(**item) for item in response.data]

    @staticmethod
    def validar_datos_actualizacion_vejez(atencion_data: dict) -> None:
        """
        Validar datos específicos para actualización de atención vejez.

        Args:
            atencion_data: Datos de actualización

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación edad vejez si se proporciona
        if "edad_anos" in atencion_data and atencion_data["edad_anos"] is not None:
            if atencion_data["edad_anos"] < 60:
                raise ValueError("La atención vejez requiere edad mínima de 60 años")

        # Validación IMC si se proporcionan peso y talla
        peso = atencion_data.get("peso_kg")
        talla = atencion_data.get("talla_cm")
        if peso and talla:
            imc = peso / (talla / 100) ** 2
            if imc < 10 or imc > 60:
                raise ValueError("IMC calculado fuera de rango válido (10-60)")

        # Validación coherencia Mini Mental
        mini_mental = atencion_data.get("mini_mental_score")
        cambios_cognitivos = atencion_data.get("cambios_cognitivos_reportados")
        if mini_mental is not None and mini_mental < 10 and not cambios_cognitivos:
            raise ValueError("Puntaje Mini Mental bajo debe ir acompañado de cambios cognitivos reportados")

    @staticmethod
    async def actualizar_atencion_vejez(atencion_id: UUID, atencion_data: dict) -> AtencionVejezResponse:
        """
        Actualizar atención vejez con validaciones de negocio centralizadas.

        Args:
            atencion_id: ID de la atención a actualizar
            atencion_data: Datos de actualización

        Returns:
            Atención vejez actualizada

        Raises:
            ValueError: Si validaciones fallan o atención no existe
            Exception: Si error en actualización
        """
        db = get_supabase_client()

        # Verificar que existe
        existing = db.table("atencion_vejez").select("id").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise ValueError("Atención vejez no encontrada")

        # Filtrar datos no nulos
        update_data = {k: v for k, v in atencion_data.items() if v is not None}

        if not update_data:
            raise ValueError("No hay campos para actualizar")

        # Validaciones de negocio centralizadas
        AtencionVejezService.validar_datos_actualizacion_vejez(update_data)

        # Actualizar
        response = db.table("atencion_vejez").update(update_data).eq("id", str(atencion_id)).execute()

        if not response.data:
            raise Exception("Error actualizando atención vejez")

        return AtencionVejezResponse(**response.data[0])

    @staticmethod
    async def eliminar_atencion_vejez(atencion_id: UUID) -> Dict[str, str]:
        """
        Eliminar atención vejez y su atención general asociada con lógica centralizada.

        Args:
            atencion_id: ID de la atención a eliminar

        Returns:
            Mensaje de confirmación

        Raises:
            ValueError: Si atención no existe
            Exception: Si error en eliminación
        """
        db = get_supabase_client()

        # Obtener atencion_id general antes de eliminar
        vejez_record = db.table("atencion_vejez").select("atencion_id").eq("id", str(atencion_id)).execute()

        if not vejez_record.data:
            raise ValueError("Atención vejez no encontrada")

        atencion_general_id = vejez_record.data[0].get("atencion_id")

        # Eliminar de atencion_vejez
        delete_vejez = db.table("atencion_vejez").delete().eq("id", str(atencion_id)).execute()

        # Eliminar de atenciones si existe referencia
        if atencion_general_id:
            db.table("atenciones").delete().eq("id", atencion_general_id).execute()

        return {"message": "Atención vejez eliminada correctamente"}

    @staticmethod
    async def obtener_estadisticas_vejez() -> Dict[str, Any]:
        """
        Obtener estadísticas especializadas de atenciones vejez.

        Returns:
            Dict con estadísticas detalladas
        """
        db = get_supabase_client()

        # Estadísticas básicas
        total_response = db.table("atencion_vejez").select("id", count="exact").execute()
        total = total_response.count if total_response.count else 0

        # Distribución por deterioro cognitivo
        deterioro_response = db.table("atencion_vejez").select("deterioro_cognitivo").execute()
        deterioro_dist = {}
        for item in deterioro_response.data:
            deterioro = item.get("deterioro_cognitivo", "NO_REGISTRADO")
            deterioro_dist[deterioro] = deterioro_dist.get(deterioro, 0) + 1

        # Distribución por riesgo caídas
        caidas_response = db.table("atencion_vejez").select("riesgo_caidas").execute()
        caidas_dist = {}
        for item in caidas_response.data:
            riesgo = item.get("riesgo_caidas", "NO_REGISTRADO")
            caidas_dist[riesgo] = caidas_dist.get(riesgo, 0) + 1

        return {
            "total_atenciones": total,
            "distribucion_deterioro_cognitivo": deterioro_dist,
            "distribucion_riesgo_caidas": caidas_dist,
            "fecha_calculo": datetime.now().isoformat()
        }