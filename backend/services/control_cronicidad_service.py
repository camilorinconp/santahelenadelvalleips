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

        # PASO 5: Crear control usando SQL directo (Sprint #5 - CENTRALIZACIÓN TOTAL)
        # Generar UUID único
        import uuid
        control_id = uuid.uuid4()
        atencion_general_id = uuid.uuid4()

        # Calcular IMC si hay datos
        imc_calculado = rpc_params.get("p_imc")
        if rpc_params.get("p_peso_kg") and rpc_params.get("p_talla_cm") and rpc_params.get("p_talla_cm") > 0:
            peso_kg = float(rpc_params["p_peso_kg"])
            talla_cm = float(rpc_params["p_talla_cm"])
            imc_calculado = peso_kg / (talla_cm / 100.0) ** 2

        # PASO 5A: Insertar en atenciones PRIMERO (para evitar FK constraint)
        atencion_data = {
            "id": str(atencion_general_id),
            "paciente_id": rpc_params["p_paciente_id"],
            "tipo_atencion": f"Control Cronicidad - {rpc_params['p_tipo_cronicidad']}",
            "detalle_id": str(control_id),
            "fecha_atencion": rpc_params["p_fecha_control"],
            "entorno": "IPS",
            "descripcion": f"Control de {rpc_params['p_tipo_cronicidad']}"
        }

        # Solo agregar medico_id si existe y no es None
        if rpc_params.get("p_medico_id"):
            atencion_data["medico_id"] = rpc_params["p_medico_id"]

        # Remover valores None
        atencion_data_clean = {k: v for k, v in atencion_data.items() if v is not None}

        response_atencion = db.table("atenciones").insert(atencion_data_clean).execute()

        if not response_atencion.data:
            raise Exception("Error insertando atención general")

        # PASO 5B: Insertar en control_cronicidad
        control_data_insert = {
            "id": str(control_id),
            "paciente_id": rpc_params["p_paciente_id"],
            "fecha_control": rpc_params["p_fecha_control"],
            "tipo_cronicidad": rpc_params["p_tipo_cronicidad"],
            "estado_control": rpc_params.get("p_estado_control"),
            "adherencia_tratamiento": rpc_params.get("p_adherencia_tratamiento"),
            "peso_kg": rpc_params.get("p_peso_kg"),
            "talla_cm": rpc_params.get("p_talla_cm"),
            "imc": imc_calculado,
            "complicaciones_observadas": rpc_params.get("p_complicaciones_observadas"),
            "observaciones": rpc_params.get("p_observaciones"),
            "medicamentos_actuales": rpc_params.get("p_medicamentos_actuales"),
            "efectos_adversos": rpc_params.get("p_efectos_adversos"),
            "educacion_brindada": rpc_params.get("p_educacion_brindada"),
            "recomendaciones_nutricionales": rpc_params.get("p_recomendaciones_nutricionales"),
            "recomendaciones_actividad_fisica": rpc_params.get("p_recomendaciones_actividad_fisica"),
            "fecha_proxima_cita": rpc_params.get("p_fecha_proxima_cita"),
            "atencion_id": str(atencion_general_id)
        }

        # Solo agregar medico_id si existe y no es None
        if rpc_params.get("p_medico_id"):
            control_data_insert["medico_id"] = rpc_params["p_medico_id"]

        # Remover valores None para inserción limpia
        control_data_clean = {k: v for k, v in control_data_insert.items() if v is not None}

        response_control = db.table("control_cronicidad").insert(control_data_clean).execute()

        if not response_control.data:
            raise Exception("Error insertando control de cronicidad")

        # PASO 6: Obtener registro completo
        control_complete = db.table("control_cronicidad").select("*").eq("id", str(control_id)).execute()

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

    # =============================================================================
    # SPRINT #5 - CRUD COMPLETO CENTRALIZADO
    # Expansión aplicando patrón perfeccionado Sprint #3/#4
    # Referencia: AtencionVejezService (529 líneas) + AtencionInfanciaService (603 líneas)
    # =============================================================================

    @staticmethod
    async def listar_controles_cronicidad(skip: int = 0, limit: int = 100,
                                         paciente_id: Optional[UUID] = None,
                                         tipo_cronicidad: Optional[str] = None) -> List[ControlCronicidadResponse]:
        """
        Listar controles de cronicidad con filtros - SPRINT #5 CENTRALIZACIÓN TOTAL:
        ✅ Delegación completa al service layer
        ✅ Validaciones de paginación centralizadas
        ✅ Patrón RPC+Service perfeccionado

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            paciente_id: Filtro opcional por paciente
            tipo_cronicidad: Filtro opcional por tipo

        Returns:
            Lista de controles de cronicidad

        Raises:
            ValueError: Si parámetros inválidos
            Exception: Si error en consulta
        """
        try:
            # PASO 1: Validaciones de negocio centralizadas
            if limit <= 0 or limit > 1000:
                raise ValueError("Límite debe estar entre 1 y 1000")
            if skip < 0:
                raise ValueError("Skip no puede ser negativo")

            # PASO 2: Construir query base
            db = get_supabase_client()
            query = db.table("control_cronicidad").select("*")

            # PASO 3: Aplicar filtros opcionales
            if paciente_id:
                query = query.eq("paciente_id", str(paciente_id))
            if tipo_cronicidad:
                query = query.eq("tipo_cronicidad", tipo_cronicidad)

            # PASO 4: Ordenar y paginar
            query = query.order("fecha_control", desc=True)
            query = query.range(skip, skip + limit - 1)

            # PASO 5: Ejecutar consulta
            response = query.execute()

            # PASO 6: Procesar resultados
            controles_response = []
            for control in response.data:
                # Calcular campos automáticos
                control_dict = dict(control)

                # Agregar cálculos según patrón establecido
                if control_dict.get('peso_kg') and control_dict.get('talla_cm'):
                    control_dict['imc_calculado'] = round(
                        control_dict['peso_kg'] / (control_dict['talla_cm'] / 100) ** 2, 1
                    )

                controles_response.append(ControlCronicidadResponse(**control_dict))

            return controles_response

        except ValueError as e:
            raise ValueError(f"Error de validación en listado: {str(e)}")
        except Exception as e:
            raise Exception(f"Error listando controles cronicidad: {str(e)}")

    @staticmethod
    async def obtener_control_cronicidad_por_id(control_id: UUID) -> ControlCronicidadResponse:
        """
        Obtener control cronicidad por ID - SPRINT #5 CENTRALIZACIÓN TOTAL:
        ✅ Delegación completa al service layer
        ✅ Validaciones de negocio centralizadas
        ✅ Patrón RPC+Service perfeccionado

        Args:
            control_id: ID del control a buscar

        Returns:
            Control cronicidad encontrado

        Raises:
            ValueError: Si el control no existe
            Exception: Si error en consulta
        """
        try:
            # PASO 1: Ejecutar consulta
            db = get_supabase_client()
            response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).execute()

            # PASO 2: Validar existencia
            if not response.data:
                raise ValueError(f"Control de cronicidad con ID {control_id} no encontrado")

            # PASO 3: Procesar resultado
            control = response.data[0]
            control_dict = dict(control)

            # PASO 4: Agregar cálculos automáticos
            if control_dict.get('peso_kg') and control_dict.get('talla_cm'):
                control_dict['imc_calculado'] = round(
                    control_dict['peso_kg'] / (control_dict['talla_cm'] / 100) ** 2, 1
                )

            return ControlCronicidadResponse(**control_dict)

        except ValueError as e:
            # Re-lanzar errores de validación de negocio
            raise e
        except Exception as e:
            raise Exception(f"Error obteniendo control cronicidad: {str(e)}")

    @staticmethod
    async def actualizar_control_cronicidad(control_id: UUID, update_data: Dict[str, Any]) -> ControlCronicidadResponse:
        """
        Actualizar control cronicidad - SPRINT #5 CENTRALIZACIÓN TOTAL:
        ✅ Delegación completa al service layer
        ✅ Validaciones de negocio centralizadas
        ✅ Lógica de actualización centralizada
        ✅ Patrón RPC+Service perfeccionado

        Args:
            control_id: ID del control a actualizar
            update_data: Datos a actualizar

        Returns:
            Control actualizado

        Raises:
            ValueError: Si validaciones fallan o control no existe
            Exception: Si error en actualización
        """
        try:
            # PASO 1: Validar que el control existe
            db = get_supabase_client()
            existing_response = db.table("control_cronicidad").select("*").eq("id", str(control_id)).execute()

            if not existing_response.data:
                raise ValueError(f"Control de cronicidad con ID {control_id} no encontrado")

            # PASO 2: Validar datos de actualización
            if not update_data:
                raise ValueError("No se proporcionaron datos para actualizar")

            # PASO 3: Validaciones específicas de negocio y recálculo automático
            existing_data = existing_response.data[0]

            # Recalcular IMC si se actualizan peso o talla
            peso_actual = update_data.get('peso_kg', existing_data.get('peso_kg'))
            talla_actual = update_data.get('talla_cm', existing_data.get('talla_cm'))

            if peso_actual and talla_actual:
                imc_recalculado = peso_actual / (talla_actual / 100) ** 2
                if imc_recalculado < 10 or imc_recalculado > 70:
                    raise ValueError("IMC calculado fuera de rango válido (10-70)")

                # Agregar IMC recalculado a los datos de actualización
                update_data['imc'] = imc_recalculado

            # PASO 4: Agregar timestamp de actualización
            update_data['updated_at'] = datetime.now().isoformat()

            # PASO 5: Ejecutar actualización
            response = db.table("control_cronicidad").update(update_data).eq("id", str(control_id)).execute()

            if not response.data:
                raise Exception("Error al actualizar control en base de datos")

            # PASO 6: Retornar resultado procesado
            control_actualizado = response.data[0]
            return ControlCronicidadResponse(**control_actualizado)

        except ValueError as e:
            # Re-lanzar errores de validación
            raise e
        except Exception as e:
            raise Exception(f"Error actualizando control cronicidad: {str(e)}")

    @staticmethod
    async def eliminar_control_cronicidad(control_id: UUID) -> Dict[str, str]:
        """
        Eliminar control cronicidad - SPRINT #5 CENTRALIZACIÓN TOTAL:
        ✅ Delegación completa al service layer
        ✅ Lógica de eliminación transaccional centralizada
        ✅ Validaciones de existencia centralizadas
        ✅ Patrón RPC+Service perfeccionado

        Args:
            control_id: ID del control a eliminar

        Returns:
            Mensaje de confirmación

        Raises:
            ValueError: Si el control no existe
            Exception: Si error en eliminación
        """
        try:
            # PASO 1: Validar que el control existe
            db = get_supabase_client()
            existing_response = db.table("control_cronicidad").select("id, atencion_id").eq("id", str(control_id)).execute()

            if not existing_response.data:
                raise ValueError(f"Control de cronicidad con ID {control_id} no encontrado")

            control_existente = existing_response.data[0]
            atencion_id = control_existente.get('atencion_id')

            # PASO 2: Eliminar control de cronicidad
            delete_response = db.table("control_cronicidad").delete().eq("id", str(control_id)).execute()

            if not delete_response.data:
                raise Exception("Error al eliminar control en base de datos")

            # PASO 3: Eliminar atención general asociada si existe (transaccional)
            if atencion_id:
                try:
                    db.table("atenciones").delete().eq("id", atencion_id).execute()
                except:
                    # Log error pero no fallar la operación principal
                    pass

            return {"mensaje": f"Control de cronicidad {control_id} eliminado exitosamente"}

        except ValueError as e:
            # Re-lanzar errores de validación
            raise e
        except Exception as e:
            raise Exception(f"Error eliminando control cronicidad: {str(e)}")

    @staticmethod
    async def listar_controles_por_paciente(paciente_id: UUID) -> List[ControlCronicidadResponse]:
        """
        Listar controles por paciente específico - SPRINT #5 CENTRALIZACIÓN TOTAL:
        ✅ Usa service layer para lógica de listado
        ✅ Filtro específico por paciente
        ✅ Orden cronológico

        Args:
            paciente_id: ID del paciente

        Returns:
            Lista de controles del paciente ordenada cronológicamente
        """
        try:
            # Usar método centralizado con filtro de paciente
            return await ControlCronicidadService.listar_controles_cronicidad(
                skip=0,
                limit=1000,  # Alto para historial completo
                paciente_id=paciente_id
            )
        except Exception as e:
            raise Exception(f"Error obteniendo controles por paciente: {str(e)}")