# =============================================================================
# Servicio Control Cronicidad - Sprint #2
# Fecha: 17 septiembre 2025
# Objetivo: Replicar patrón RPC+Service exitoso del Sprint Piloto #1
# Base Normativa: Control de enfermedades crónicas no transmisibles
# =============================================================================

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from uuid import UUID
from models.control_cronicidad_model import ControlCronicidadCrear, ControlCronicidadResponse
from database import get_supabase_client

class ControlCronicidadService:
    """
    Servicio centralizado para lógica de negocio de control de cronicidad.

    REPLICA PATRÓN EXITOSO DEL SPRINT PILOTO #1:
    - Separación de inquietudes (Separation of Concerns)
    - Business Logic centralizada y reutilizable
    - RPC Transactional operations
    - Validaciones de negocio centralizadas
    """

    @staticmethod
    def validar_datos_control_cronicidad(control_data: ControlCronicidadCrear) -> None:
        """
        Validar datos específicos de control de cronicidad.

        Args:
            control_data: Datos de entrada para validar

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación tipo de cronicidad válido
        tipos_validos = ["Hipertension", "Diabetes", "ERC", "Dislipidemia"]
        if control_data.tipo_cronicidad not in tipos_validos:
            raise ValueError(f"Tipo de cronicidad debe ser uno de: {', '.join(tipos_validos)}")

        # Validación consistencia antropométrica
        if control_data.peso_kg and control_data.talla_cm:
            imc = control_data.peso_kg / (control_data.talla_cm / 100) ** 2
            if imc < 10 or imc > 70:
                raise ValueError("IMC calculado fuera de rango válido (10-70)")

        # Validación fecha control no futura
        if control_data.fecha_control > date.today():
            raise ValueError("La fecha de control no puede ser futura")

        # Validación próxima cita posterior a control actual
        if control_data.fecha_proxima_cita and control_data.fecha_proxima_cita <= control_data.fecha_control:
            raise ValueError("La fecha de próxima cita debe ser posterior a la fecha de control actual")

        # Validación estado control consistente con adherencia
        if control_data.estado_control == "Controlado" and control_data.adherencia_tratamiento == "Mala":
            raise ValueError("Estado controlado inconsistente con mala adherencia al tratamiento")

    @staticmethod
    def calcular_indicadores_cronicidad(control_data: ControlCronicidadCrear) -> Dict[str, Any]:
        """
        Calcular indicadores y métricas específicas de control de cronicidad.

        Args:
            control_data: Datos de control de cronicidad

        Returns:
            Dict con indicadores calculados
        """
        indicadores = {}

        # Calcular IMC si hay datos
        if control_data.peso_kg and control_data.talla_cm:
            imc = control_data.peso_kg / (control_data.talla_cm / 100) ** 2
            indicadores["imc_calculado"] = round(imc, 2)

            # Clasificación IMC
            if imc < 18.5:
                indicadores["clasificacion_imc"] = "BAJO_PESO"
            elif imc < 25:
                indicadores["clasificacion_imc"] = "NORMAL"
            elif imc < 30:
                indicadores["clasificacion_imc"] = "SOBREPESO"
            else:
                indicadores["clasificacion_imc"] = "OBESIDAD"

        # Evaluar riesgo cardiovascular
        riesgo_cardiovascular = "BAJO"
        factores_riesgo = 0

        if control_data.tipo_cronicidad in ["Hipertension", "Diabetes"]:
            factores_riesgo += 1

        if control_data.peso_kg and control_data.talla_cm:
            imc = control_data.peso_kg / (control_data.talla_cm / 100) ** 2
            if imc >= 30:
                factores_riesgo += 2
            elif imc >= 25:
                factores_riesgo += 1

        if control_data.adherencia_tratamiento == "Mala":
            factores_riesgo += 2

        if factores_riesgo >= 4:
            riesgo_cardiovascular = "MUY_ALTO"
        elif factores_riesgo >= 3:
            riesgo_cardiovascular = "ALTO"
        elif factores_riesgo >= 2:
            riesgo_cardiovascular = "MODERADO"

        indicadores["riesgo_cardiovascular"] = riesgo_cardiovascular
        indicadores["factores_riesgo_count"] = factores_riesgo

        # Evaluar control adecuado
        control_adecuado = True
        if control_data.estado_control in ["No controlado"]:
            control_adecuado = False
        if control_data.adherencia_tratamiento in ["Mala", "Regular"]:
            control_adecuado = False
        if control_data.complicaciones_observadas:
            control_adecuado = False

        indicadores["control_adecuado"] = control_adecuado

        return indicadores

    @staticmethod
    def generar_recomendaciones_cronicidad(control_data: ControlCronicidadCrear) -> List[str]:
        """
        Generar recomendaciones específicas basadas en el tipo de cronicidad y estado.

        Args:
            control_data: Datos de control de cronicidad

        Returns:
            Lista de recomendaciones personalizadas
        """
        recomendaciones = []

        # Recomendaciones por tipo de cronicidad
        if control_data.tipo_cronicidad == "Hipertension":
            recomendaciones.append("Reducir consumo de sodio a menos de 2.3g por día")
            recomendaciones.append("Realizar actividad física moderada 150 minutos por semana")
            recomendaciones.append("Monitorear presión arterial en casa diariamente")

        elif control_data.tipo_cronicidad == "Diabetes":
            recomendaciones.append("Monitorear glucosa según indicación médica")
            recomendaciones.append("Mantener dieta con control de carbohidratos")
            recomendaciones.append("Revisar pies diariamente para prevenir complicaciones")

        elif control_data.tipo_cronicidad == "ERC":
            recomendaciones.append("Controlar ingesta de proteínas según indicación médica")
            recomendaciones.append("Monitorear función renal cada 3-6 meses")
            recomendaciones.append("Evitar medicamentos nefrotóxicos")

        elif control_data.tipo_cronicidad == "Dislipidemia":
            recomendaciones.append("Seguir dieta baja en grasas saturadas y trans")
            recomendaciones.append("Incrementar consumo de omega-3")
            recomendaciones.append("Control lipídico cada 3-6 meses")

        # Recomendaciones por adherencia al tratamiento
        if control_data.adherencia_tratamiento == "Mala":
            recomendaciones.append("Revisar barreras para adherencia al tratamiento")
            recomendaciones.append("Considerar simplificación del esquema terapéutico")
            recomendaciones.append("Programar seguimiento más frecuente")

        # Recomendaciones por IMC
        if control_data.peso_kg and control_data.talla_cm:
            imc = control_data.peso_kg / (control_data.talla_cm / 100) ** 2
            if imc >= 30:
                recomendaciones.append("Plan de reducción de peso supervisado")
                recomendaciones.append("Referir a nutricionista para manejo de obesidad")
            elif imc >= 25:
                recomendaciones.append("Modificaciones dietéticas para control de peso")

        # Recomendaciones por estado de control
        if control_data.estado_control == "No controlado":
            recomendaciones.append("Revisar y ajustar esquema terapéutico")
            recomendaciones.append("Identificar factores que impiden control adecuado")
            recomendaciones.append("Programar cita de control en 4 semanas")

        return recomendaciones

    @staticmethod
    async def crear_control_cronicidad_completo(control_data: ControlCronicidadCrear) -> ControlCronicidadResponse:
        """
        Crear control de cronicidad completo usando RPC transaccional y lógica de negocio centralizada.

        Args:
            control_data: Datos para crear el control

        Returns:
            Control de cronicidad creado con indicadores calculados

        Raises:
            ValueError: Si validaciones fallan
            Exception: Si error en creación
        """
        # PASO 1: Validaciones de negocio centralizadas
        ControlCronicidadService.validar_datos_control_cronicidad(control_data)

        # PASO 2: Calcular indicadores pre-creación
        indicadores = ControlCronicidadService.calcular_indicadores_cronicidad(control_data)

        # PASO 3: Generar recomendaciones
        recomendaciones = ControlCronicidadService.generar_recomendaciones_cronicidad(control_data)

        # PASO 4: Preparar datos para RPC
        db = get_supabase_client()

        # Agregar recomendaciones a observaciones si no existen
        observaciones_final = control_data.observaciones or ""
        if recomendaciones:
            observaciones_final += "\n\nRECOMENDACIONES AUTOMÁTICAS:\n"
            observaciones_final += "\n".join(f"- {rec}" for rec in recomendaciones)

        # Preparar parámetros para RPC
        rpc_params = {
            "p_paciente_id": str(control_data.paciente_id),
            "p_medico_id": str(control_data.medico_id) if control_data.medico_id else None,
            "p_fecha_control": control_data.fecha_control.isoformat(),
            "p_tipo_cronicidad": control_data.tipo_cronicidad,
            "p_estado_control": control_data.estado_control,
            "p_adherencia_tratamiento": control_data.adherencia_tratamiento,

            # Antropometría
            "p_peso_kg": control_data.peso_kg,
            "p_talla_cm": control_data.talla_cm,
            "p_imc": indicadores.get("imc_calculado"),

            # Observaciones clínicas
            "p_complicaciones_observadas": control_data.complicaciones_observadas,
            "p_observaciones": observaciones_final,

            # Seguimiento farmacológico
            "p_medicamentos_actuales": control_data.medicamentos_actuales,
            "p_efectos_adversos": control_data.efectos_adversos,

            # Educación y recomendaciones
            "p_educacion_brindada": control_data.educacion_brindada,
            "p_recomendaciones_nutricionales": control_data.recomendaciones_nutricionales,
            "p_recomendaciones_actividad_fisica": control_data.recomendaciones_actividad_fisica,

            # Próxima cita
            "p_fecha_proxima_cita": control_data.fecha_proxima_cita.isoformat() if control_data.fecha_proxima_cita else None
        }

        # PASO 5: Ejecutar RPC transaccional
        response = db.rpc("crear_control_cronicidad_completo", rpc_params).execute()

        if not response.data or len(response.data) == 0:
            raise Exception("Error ejecutando RPC transaccional para control de cronicidad")

        # PASO 6: Obtener registro completo
        rpc_result = response.data[0]
        control_id = rpc_result["control_id"]

        control_complete = db.table("control_cronicidad").select("*").eq("id", control_id).execute()

        if not control_complete.data:
            raise Exception("Error obteniendo control de cronicidad creado")

        return ControlCronicidadResponse(**control_complete.data[0])

    @staticmethod
    async def obtener_estadisticas_cronicidad() -> Dict[str, Any]:
        """
        Obtener estadísticas especializadas de controles de cronicidad.

        Returns:
            Dict con estadísticas detalladas
        """
        db = get_supabase_client()

        # Estadísticas básicas
        total_response = db.table("control_cronicidad").select("id", count="exact").execute()
        total = total_response.count if total_response.count else 0

        # Distribución por tipo de cronicidad
        tipos_response = db.table("control_cronicidad").select("tipo_cronicidad").execute()
        tipos_dist = {}
        for item in tipos_response.data:
            tipo = item.get("tipo_cronicidad", "NO_REGISTRADO")
            tipos_dist[tipo] = tipos_dist.get(tipo, 0) + 1

        # Distribución por estado de control
        estados_response = db.table("control_cronicidad").select("estado_control").execute()
        estados_dist = {}
        for item in estados_response.data:
            estado = item.get("estado_control", "NO_REGISTRADO")
            estados_dist[estado] = estados_dist.get(estado, 0) + 1

        return {
            "total_controles": total,
            "distribucion_tipos_cronicidad": tipos_dist,
            "distribucion_estados_control": estados_dist,
            "fecha_calculo": datetime.now().isoformat()
        }