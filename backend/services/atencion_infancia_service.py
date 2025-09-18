# =============================================================================
# Servicio Atención Infancia - Sprint #4: CENTRALIZACIÓN TOTAL
# Fecha: 18 septiembre 2025
# Objetivo: Aplicar patrón RPC+Service perfeccionado (referencia: AtencionVejezService Sprint #3)
# Evolución: Sprint Piloto #1 → Sprint #2 → Sprint #3 → Sprint #4 (Infancia)
# Base Normativa: Resolución 3280 de 2018 - Art. 3.3.2 (Infancia 6-11 años)
#
# PATRÓN SPRINT #4:
# ✅ CENTRALIZACIÓN TOTAL: 100% lógica de negocio en service layer
# ✅ CRUD COMPLETO CENTRALIZADO: Create, Read, Update, Delete + validaciones
# ✅ ZERO BUSINESS LOGIC EN ENDPOINTS: Solo delegación y manejo errores
# ✅ REFERENCIA MÁXIMA: AtencionVejezService como template arquitectónico
# =============================================================================

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from uuid import UUID, uuid4
from models.atencion_infancia_model import (
    AtencionInfanciaCrear,
    AtencionInfanciaActualizar,
    AtencionInfanciaResponse,
    EstadoNutricionalInfancia,
    DesempenoEscolar,
    ResultadoTamizaje,
    FactorRiesgo,
    calcular_estado_nutricional,
    calcular_desarrollo_apropiado,
    calcular_riesgo_nutricional,
    calcular_proxima_consulta_dias,
    calcular_completitud_evaluacion,
    determinar_seguimiento_especializado
)
from database import get_supabase_client

class AtencionInfanciaService:
    """
    Servicio centralizado para lógica de negocio de atención infancia.

    APLICA PATRÓN PERFECCIONADO SPRINT #3:
    - Centralización TOTAL de lógica de negocio
    - Separación de inquietudes (Separation of Concerns)
    - Business Logic centralizada y reutilizable
    - Validaciones de negocio centralizadas
    - CRUD completo en service layer

    REFERENCIA ARQUITECTÓNICA:
    - AtencionVejezService (Sprint #3) - PATRÓN MÁXIMO
    - ControlCronicidadService (Sprint #2) - Base consolidada
    """

    @staticmethod
    def validar_datos_infancia(atencion_data: AtencionInfanciaCrear) -> None:
        """
        Validar datos específicos de atención infancia según Resolución 3280.

        Args:
            atencion_data: Datos de entrada para validar

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación edad infancia (6-11 años) - Se validará en el endpoint con data del paciente
        # Aquí validamos los datos de la atención en sí

        # Validación consistencia antropométrica
        if atencion_data.peso_kg and atencion_data.talla_cm:
            imc = atencion_data.peso_kg / (atencion_data.talla_cm / 100) ** 2
            if imc < 10 or imc > 40:
                raise ValueError("IMC calculado fuera de rango válido para infancia (10-40)")

        # Validación coherencia datos escolares
        if atencion_data.desempeno_escolar != DesempenoEscolar.NO_ESCOLARIZADO:
            if not atencion_data.grado_escolar:
                raise ValueError("Grado escolar requerido cuando hay desempeño escolar registrado")

        # Validación coherencia tamizajes
        if atencion_data.tamizaje_visual == ResultadoTamizaje.ALTERADO:
            if not atencion_data.dificultades_aprendizaje:
                # Solo advertencia, no error crítico
                pass

        # Validación actividad física razonable
        if atencion_data.actividad_fisica_semanal_horas and atencion_data.actividad_fisica_semanal_horas > 35:
            raise ValueError("Actividad física semanal no puede exceder 35 horas para infancia")

        # Validación fecha atención no futura
        if atencion_data.fecha_atencion > date.today():
            raise ValueError("La fecha de atención no puede ser futura")

    @staticmethod
    def calcular_indicadores_infancia(atencion_data: AtencionInfanciaCrear, edad_anos: int) -> Dict[str, Any]:
        """
        Calcular indicadores y métricas específicas de infancia.

        Args:
            atencion_data: Datos de atención infancia
            edad_anos: Edad del paciente en años

        Returns:
            Dict con indicadores calculados
        """
        indicadores = {}

        # Calcular IMC si hay datos
        if atencion_data.peso_kg and atencion_data.talla_cm:
            imc = atencion_data.peso_kg / (atencion_data.talla_cm / 100) ** 2
            indicadores["indice_masa_corporal"] = round(imc, 1)

            # Estado nutricional usando función del modelo
            estado_nutricional = calcular_estado_nutricional(
                atencion_data.peso_kg, atencion_data.talla_cm, edad_anos
            )
            indicadores["estado_nutricional"] = estado_nutricional

            # Percentiles estimados (simplificado para el service)
            percentil_peso = 50 if estado_nutricional == EstadoNutricionalInfancia.NORMAL else 25
            percentil_talla = 50  # Simplificado
            indicadores["percentil_peso"] = percentil_peso
            indicadores["percentil_talla"] = percentil_talla

            # Riesgo nutricional
            riesgo_nutricional = calcular_riesgo_nutricional(
                estado_nutricional,
                atencion_data.consume_comida_chatarra or False,
                atencion_data.actividad_fisica_semanal_horas
            )
            indicadores["riesgo_nutricional"] = riesgo_nutricional

        # Desarrollo apropiado para edad
        desarrollo_apropiado = calcular_desarrollo_apropiado(
            atencion_data.desempeno_escolar or DesempenoEscolar.BASICO,
            atencion_data.tamizaje_visual or ResultadoTamizaje.NORMAL,
            atencion_data.tamizaje_auditivo or ResultadoTamizaje.NORMAL,
            atencion_data.dificultades_aprendizaje or False
        )
        indicadores["desarrollo_apropiado_edad"] = desarrollo_apropiado

        # Seguimiento especializado
        requiere_seguimiento = determinar_seguimiento_especializado(
            atencion_data.tamizaje_visual or ResultadoTamizaje.NORMAL,
            atencion_data.tamizaje_auditivo or ResultadoTamizaje.NORMAL,
            atencion_data.tamizaje_salud_bucal or ResultadoTamizaje.NORMAL,
            atencion_data.dificultades_aprendizaje or False,
            atencion_data.numero_caries
        )
        indicadores["requiere_seguimiento_especializado"] = requiere_seguimiento

        # Próxima consulta recomendada
        factores_riesgo = atencion_data.factores_riesgo_identificados or []
        proxima_consulta_dias = calcular_proxima_consulta_dias(
            indicadores.get("estado_nutricional", EstadoNutricionalInfancia.NORMAL),
            requiere_seguimiento,
            factores_riesgo
        )
        indicadores["proxima_consulta_recomendada_dias"] = proxima_consulta_dias

        # Completitud de evaluación
        atencion_dict = atencion_data.model_dump()
        completitud = calcular_completitud_evaluacion(atencion_dict)
        indicadores["completitud_evaluacion"] = completitud

        return indicadores

    @staticmethod
    def generar_recomendaciones_infancia(atencion_data: AtencionInfanciaCrear, indicadores: Dict[str, Any]) -> List[str]:
        """
        Generar recomendaciones específicas basadas en la evaluación de infancia.

        Args:
            atencion_data: Datos de atención infancia
            indicadores: Indicadores calculados

        Returns:
            Lista de recomendaciones personalizadas
        """
        recomendaciones = []

        # Recomendaciones por estado nutricional
        estado_nutricional = indicadores.get("estado_nutricional")
        if estado_nutricional == EstadoNutricionalInfancia.DELGADEZ:
            recomendaciones.append("Plan nutricional para recuperación ponderal en infancia")
            recomendaciones.append("Seguimiento nutricional cada 2 semanas")
        elif estado_nutricional == EstadoNutricionalInfancia.SOBREPESO:
            recomendaciones.append("Plan de actividad física adaptado para infancia")
            recomendaciones.append("Educación nutricional familiar")
        elif estado_nutricional == EstadoNutricionalInfancia.OBESIDAD:
            recomendaciones.append("Referencia a nutricionista pediátrico")
            recomendaciones.append("Plan integral de manejo de obesidad infantil")

        # Recomendaciones por desempeño escolar
        if atencion_data.desempeno_escolar == DesempenoEscolar.BAJO:
            recomendaciones.append("Evaluación psicopedagógica para identificar dificultades")
            recomendaciones.append("Apoyo académico especializado")
        elif atencion_data.desempeno_escolar == DesempenoEscolar.NO_ESCOLARIZADO:
            recomendaciones.append("Gestión para vinculación al sistema educativo")
            recomendaciones.append("Evaluación de barreras de acceso a educación")

        # Recomendaciones por tamizajes alterados
        if atencion_data.tamizaje_visual == ResultadoTamizaje.ALTERADO:
            recomendaciones.append("Referencia a oftalmología pediátrica")
            recomendaciones.append("Adaptaciones escolares para problemas visuales")

        if atencion_data.tamizaje_auditivo == ResultadoTamizaje.ALTERADO:
            recomendaciones.append("Referencia a audiología pediátrica")
            recomendaciones.append("Evaluación de impacto en rendimiento escolar")

        if atencion_data.tamizaje_salud_bucal == ResultadoTamizaje.ALTERADO:
            recomendaciones.append("Atención odontológica inmediata")
            recomendaciones.append("Educación en higiene oral familiar")

        # Recomendaciones por dificultades de aprendizaje
        if atencion_data.dificultades_aprendizaje:
            recomendaciones.append("Evaluación neuropsicológica")
            recomendaciones.append("Plan de apoyo educativo personalizado")

        # Recomendaciones por factores de riesgo
        factores_riesgo = atencion_data.factores_riesgo_identificados or []
        if FactorRiesgo.VIOLENCIA_ESCOLAR in factores_riesgo:
            recomendaciones.append("Activación de ruta de protección integral")
            recomendaciones.append("Seguimiento por trabajo social")

        if FactorRiesgo.SEDENTARISMO in factores_riesgo:
            recomendaciones.append("Plan de actividad física progresiva")
            recomendaciones.append("Vincular a programas deportivos escolares")

        # Recomendaciones por actividad física
        if not atencion_data.actividad_fisica_semanal_horas or atencion_data.actividad_fisica_semanal_horas < 3:
            recomendaciones.append("Promoción de actividad física diaria")
            recomendaciones.append("Vincular a programas deportivos comunitarios")

        # Recomendaciones por hábitos alimentarios
        if atencion_data.consume_comida_chatarra:
            recomendaciones.append("Educación nutricional para reducir alimentos ultraprocesados")
            recomendaciones.append("Promoción de loncheras saludables")

        return recomendaciones

    @staticmethod
    async def crear_atencion_infancia_completa(atencion_data: AtencionInfanciaCrear) -> AtencionInfanciaResponse:
        """
        Crear atención infancia completa con lógica de negocio centralizada.

        REPLICA PATRÓN PERFECCIONADO SPRINT #3:
        - Validaciones centralizadas
        - Operaciones atómicas (sin RPC por ahora, mejora futura)
        - Cálculo de indicadores centralizado
        - Generación de recomendaciones automática

        Args:
            atencion_data: Datos para crear la atención

        Returns:
            Atención infancia creada con indicadores calculados

        Raises:
            ValueError: Si validaciones fallan
            Exception: Si error en creación
        """
        # PASO 1: Validaciones de negocio centralizadas
        AtencionInfanciaService.validar_datos_infancia(atencion_data)

        # PASO 2: Obtener y validar datos del paciente
        db = get_supabase_client()

        paciente_response = db.table("pacientes").select("id, fecha_nacimiento").eq("id", str(atencion_data.paciente_id)).execute()
        if not paciente_response.data:
            raise ValueError("El paciente especificado no existe")

        # Calcular edad del paciente
        fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
        edad_anos = (date.today() - fecha_nacimiento).days // 365

        # Validar rango de edad para infancia (6-11 años)
        if edad_anos < 6 or edad_anos > 11:
            raise ValueError(f"Edad {edad_anos} años fuera del rango de infancia (6-11 años)")

        # PASO 3: Calcular indicadores pre-creación
        indicadores = AtencionInfanciaService.calcular_indicadores_infancia(atencion_data, edad_anos)

        # PASO 4: Generar recomendaciones
        recomendaciones = AtencionInfanciaService.generar_recomendaciones_infancia(atencion_data, indicadores)

        # PASO 5: Preparar datos para creación (patrón polimórfico 3 pasos)
        try:
            # Generar IDs únicos
            infancia_id = str(uuid4())
            atencion_general_id = str(uuid4())

            # Preparar datos de infancia
            atencion_dict = atencion_data.model_dump()
            atencion_dict['id'] = infancia_id
            atencion_dict['paciente_id'] = str(atencion_data.paciente_id)
            atencion_dict['medico_id'] = str(atencion_data.medico_id) if atencion_data.medico_id else None
            atencion_dict['fecha_atencion'] = atencion_data.fecha_atencion.isoformat()

            # Convertir listas de enums a strings para Supabase
            if 'factores_riesgo_identificados' in atencion_dict and atencion_dict['factores_riesgo_identificados']:
                atencion_dict['factores_riesgo_identificados'] = [str(factor) for factor in atencion_dict['factores_riesgo_identificados']]

            # Agregar observaciones con recomendaciones
            observaciones_final = atencion_data.observaciones_profesional_infancia or ""
            if recomendaciones:
                observaciones_final += "\n\nRECOMENDACIONES AUTOMÁTICAS:\n"
                observaciones_final += "\n".join(f"- {rec}" for rec in recomendaciones)

            atencion_dict['observaciones_profesional_infancia'] = observaciones_final

            # PASO 6A: Crear atención de infancia
            response_infancia = db.table("atencion_infancia").insert(atencion_dict).execute()

            if not response_infancia.data:
                raise Exception("Error al crear atención de infancia")

            # PASO 6B: Crear atención general polimórfica
            atencion_general_data = {
                "id": atencion_general_id,
                "paciente_id": str(atencion_data.paciente_id),
                "medico_id": str(atencion_data.medico_id) if atencion_data.medico_id else None,
                "tipo_atencion": "Atención Infancia",
                "detalle_id": infancia_id,
                "fecha_atencion": atencion_data.fecha_atencion.isoformat(),
                "entorno": atencion_data.entorno,
                "descripcion": f"Atención integral para infancia - {edad_anos} años",
                "creado_en": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            response_atencion = db.table("atenciones").insert(atencion_general_data).execute()

            if not response_atencion.data:
                # Rollback: eliminar atención de infancia creada
                db.table("atencion_infancia").delete().eq("id", infancia_id).execute()
                raise Exception("Error al crear atención general")

            # PASO 6C: Actualizar atención de infancia con referencia
            update_response = db.table("atencion_infancia").update({"atencion_id": atencion_general_id}).eq("id", infancia_id).execute()

            if not update_response.data:
                # Rollback: eliminar ambos registros
                db.table("atenciones").delete().eq("id", atencion_general_id).execute()
                db.table("atencion_infancia").delete().eq("id", infancia_id).execute()
                raise Exception("Error al vincular atención general con infancia")

            # PASO 7: Obtener registro completo con indicadores
            final_response = db.table("atencion_infancia").select("*").eq("id", infancia_id).execute()
            atencion_completa = final_response.data[0]

            # Agregar indicadores calculados
            atencion_completa.update(indicadores)

            return AtencionInfanciaResponse(**atencion_completa)

        except Exception as e:
            raise Exception(f"Error creando atención infancia: {str(e)}")

    @staticmethod
    async def obtener_atencion_infancia_por_id(atencion_id: UUID) -> AtencionInfanciaResponse:
        """
        Obtener atención infancia por ID con validaciones de negocio centralizadas.

        Args:
            atencion_id: ID de la atención a buscar

        Returns:
            Atención infancia encontrada

        Raises:
            ValueError: Si la atención no existe
            Exception: Si error en consulta
        """
        db = get_supabase_client()

        response = db.table("atencion_infancia").select("*").eq("id", str(atencion_id)).execute()

        if not response.data:
            raise ValueError("Atención de infancia no encontrada")

        atencion = response.data[0]

        # Calcular edad del paciente
        paciente_response = db.table("pacientes").select("fecha_nacimiento").eq("id", atencion['paciente_id']).execute()
        if paciente_response.data:
            fecha_nacimiento = datetime.fromisoformat(paciente_response.data[0]['fecha_nacimiento'].replace('Z', '+00:00')).date()
            edad_anos = (date.today() - fecha_nacimiento).days // 365
        else:
            edad_anos = 8  # Default para infancia

        # Recrear objeto para calcular indicadores
        atencion_data = AtencionInfanciaCrear(**atencion)
        indicadores = AtencionInfanciaService.calcular_indicadores_infancia(atencion_data, edad_anos)

        # Agregar indicadores calculados
        atencion.update(indicadores)

        return AtencionInfanciaResponse(**atencion)

    @staticmethod
    async def listar_atenciones_infancia(
        skip: int = 0,
        limit: int = 50,
        paciente_id: Optional[UUID] = None,
        desempeno_escolar: Optional[DesempenoEscolar] = None
    ) -> List[AtencionInfanciaResponse]:
        """
        Listar atenciones infancia con filtros y validaciones centralizadas.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar
            paciente_id: Filtro opcional por paciente
            desempeno_escolar: Filtro opcional por desempeño

        Returns:
            Lista de atenciones infancia

        Raises:
            ValueError: Si parámetros inválidos
            Exception: Si error en consulta
        """
        # Validaciones de negocio centralizadas
        if skip < 0:
            raise ValueError("skip debe ser mayor o igual a 0")
        if limit < 1 or limit > 100:
            raise ValueError("limit debe estar entre 1 y 100")

        db = get_supabase_client()

        query = db.table("atencion_infancia").select("*")

        # Aplicar filtros
        if paciente_id:
            query = query.eq("paciente_id", str(paciente_id))
        if desempeno_escolar:
            query = query.eq("desempeno_escolar", desempeno_escolar.value)

        # Ordenar y paginar
        query = query.order("fecha_atencion", desc=True).range(skip, skip + limit - 1)

        response = query.execute()

        atenciones_con_indicadores = []
        for atencion in response.data:
            # Edad estimada (simplificado para listing)
            edad_anos = 8  # Promedio para infancia

            # Recrear objeto para calcular indicadores
            atencion_data = AtencionInfanciaCrear(**atencion)
            indicadores = AtencionInfanciaService.calcular_indicadores_infancia(atencion_data, edad_anos)

            atencion.update(indicadores)
            atenciones_con_indicadores.append(AtencionInfanciaResponse(**atencion))

        return atenciones_con_indicadores

    @staticmethod
    def validar_datos_actualizacion_infancia(atencion_data: dict) -> None:
        """
        Validar datos específicos para actualización de atención infancia.

        Args:
            atencion_data: Datos de actualización

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación IMC si se proporcionan peso y talla
        peso = atencion_data.get("peso_kg")
        talla = atencion_data.get("talla_cm")
        if peso and talla:
            imc = peso / (talla / 100) ** 2
            if imc < 10 or imc > 40:
                raise ValueError("IMC calculado fuera de rango válido para infancia (10-40)")

        # Validación coherencia escolar
        desempeno = atencion_data.get("desempeno_escolar")
        grado = atencion_data.get("grado_escolar")
        if desempeno and desempeno != "NO_ESCOLARIZADO" and not grado:
            raise ValueError("Grado escolar requerido cuando hay desempeño escolar registrado")

        # Validación actividad física
        actividad = atencion_data.get("actividad_fisica_semanal_horas")
        if actividad and actividad > 35:
            raise ValueError("Actividad física semanal no puede exceder 35 horas para infancia")

    @staticmethod
    async def actualizar_atencion_infancia(atencion_id: UUID, atencion_data: dict) -> AtencionInfanciaResponse:
        """
        Actualizar atención infancia con validaciones de negocio centralizadas.

        Args:
            atencion_id: ID de la atención a actualizar
            atencion_data: Datos de actualización

        Returns:
            Atención infancia actualizada

        Raises:
            ValueError: Si validaciones fallan o atención no existe
            Exception: Si error en actualización
        """
        db = get_supabase_client()

        # Verificar que existe
        existing = db.table("atencion_infancia").select("*").eq("id", str(atencion_id)).execute()
        if not existing.data:
            raise ValueError("Atención de infancia no encontrada")

        # Filtrar datos no nulos
        update_data = {k: v for k, v in atencion_data.items() if v is not None}

        if not update_data:
            raise ValueError("No hay campos para actualizar")

        # Validaciones de negocio centralizadas
        AtencionInfanciaService.validar_datos_actualizacion_infancia(update_data)

        # Convertir listas de enums si es necesario
        if 'factores_riesgo_identificados' in update_data and update_data['factores_riesgo_identificados']:
            update_data['factores_riesgo_identificados'] = [str(factor) for factor in update_data['factores_riesgo_identificados']]

        update_data['updated_at'] = datetime.now().isoformat()

        # Actualizar
        response = db.table("atencion_infancia").update(update_data).eq("id", str(atencion_id)).execute()

        if not response.data:
            raise Exception("Error actualizando atención de infancia")

        # Devolver con indicadores recalculados
        return await AtencionInfanciaService.obtener_atencion_infancia_por_id(atencion_id)

    @staticmethod
    async def eliminar_atencion_infancia(atencion_id: UUID) -> Dict[str, str]:
        """
        Eliminar atención infancia y su atención general asociada con lógica centralizada.

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
        infancia_record = db.table("atencion_infancia").select("atencion_id").eq("id", str(atencion_id)).execute()

        if not infancia_record.data:
            raise ValueError("Atención de infancia no encontrada")

        atencion_general_id = infancia_record.data[0].get("atencion_id")

        # Eliminar de atencion_infancia
        delete_infancia = db.table("atencion_infancia").delete().eq("id", str(atencion_id)).execute()

        # Eliminar de atenciones si existe referencia
        if atencion_general_id:
            db.table("atenciones").delete().eq("id", atencion_general_id).execute()

        return {"message": "Atención de infancia eliminada correctamente"}

    @staticmethod
    async def obtener_estadisticas_infancia() -> Dict[str, Any]:
        """
        Obtener estadísticas especializadas de atenciones infancia.

        Returns:
            Dict con estadísticas detalladas
        """
        db = get_supabase_client()

        # Estadísticas básicas
        total_response = db.table("atencion_infancia").select("id", count="exact").execute()
        total = total_response.count if total_response.count else 0

        # Distribución por desempeño escolar
        desempeno_response = db.table("atencion_infancia").select("desempeno_escolar").execute()
        desempeno_dist = {}
        for item in desempeno_response.data:
            desempeno = item.get("desempeno_escolar", "NO_REGISTRADO")
            desempeno_dist[desempeno] = desempeno_dist.get(desempeno, 0) + 1

        # Distribución por tamizajes
        tamizajes_response = db.table("atencion_infancia").select("tamizaje_visual, tamizaje_auditivo, tamizaje_salud_bucal").execute()
        tamizajes_alterados = {"visual": 0, "auditivo": 0, "salud_bucal": 0}
        for item in tamizajes_response.data:
            if item.get("tamizaje_visual") == "ALTERADO":
                tamizajes_alterados["visual"] += 1
            if item.get("tamizaje_auditivo") == "ALTERADO":
                tamizajes_alterados["auditivo"] += 1
            if item.get("tamizaje_salud_bucal") == "ALTERADO":
                tamizajes_alterados["salud_bucal"] += 1

        return {
            "total_atenciones": total,
            "distribucion_desempeno_escolar": desempeno_dist,
            "tamizajes_alterados": tamizajes_alterados,
            "fecha_calculo": datetime.now().isoformat()
        }