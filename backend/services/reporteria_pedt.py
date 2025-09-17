# -*- coding: utf-8 -*-
"""
CAPA DE REPORTERÍA INTELIGENTE - RESOLUCIÓN 202 DE 2021
========================================================

Implementación de la "Capa de Reportería Inteligente" que calcula las 119 variables 
PEDT (Protección Específica y Detección Temprana) requeridas por la Resolución 202
de 2021 a partir de la arquitectura transversal existente.

Principio: 90% de las variables son DERIVADAS (se calculan desde BD existente),
solo ~15% requieren campos físicos nuevos.

Autor: Equipo IPS Santa Helena del Valle
Fecha: 13 septiembre 2025
Estado: Implementación Fase 3C - Base Funcional
"""

from typing import Dict, Any, List, Optional, Union
from uuid import UUID
from datetime import date, datetime
import logging
from supabase import Client

from database import get_supabase_client

# Configuración logging
logger = logging.getLogger(__name__)

class GeneradorReportePEDT:
    """
    Generador de reportes PEDT según Resolución 202 de 2021
    
    Esta clase implementa la lógica para calcular las 119 variables PEDT
    requeridas por el SISPRO, aprovechando al máximo la arquitectura 
    transversal existente (entornos, familias, atenciones integrales).
    
    Estrategia: Variables derivadas vs. campos físicos nuevos
    - 85% variables derivadas: Se calculan desde BD existente
    - 15% campos físicos: Requieren migración BD (próxima fase)
    """
    
    def __init__(self, db_client: Optional[Client] = None):
        """
        Inicializa el generador con conexión a Supabase
        
        Args:
            db_client: Cliente Supabase opcional. Si None, usa get_supabase_client()
        """
        self.db = db_client or get_supabase_client()
        logger.info("GeneradorReportePEDT inicializado correctamente")
    
    def generar_variables_119(self, paciente_id: UUID) -> Dict[str, Any]:
        """
        Genera las 119 variables PEDT para un paciente específico
        
        Args:
            paciente_id: UUID del paciente en tabla pacientes
            
        Returns:
            Dict con las 119 variables según especificación Controles_RPED_202.csv
            
        Raises:
            ValueError: Si paciente no existe o datos insuficientes
        """
        try:
            # Obtener datos base del paciente
            datos_paciente = self._obtener_datos_paciente(paciente_id)
            if not datos_paciente:
                raise ValueError(f"Paciente {paciente_id} no encontrado")
            
            # Inicializar diccionario de variables PEDT
            variables_pedt = {}
            
            # GRUPO 1: IDENTIFICACIÓN (Variables 0-13)
            variables_pedt.update(self._calcular_variables_identificacion(datos_paciente))
            
            # GRUPO 2: GESTACIÓN (Variables 14-15) 
            variables_pedt.update(self._calcular_variables_gestacion(paciente_id, datos_paciente))
            
            # GRUPO 3: TEST VEJEZ (Variables 16-17)
            variables_pedt.update(self._calcular_variables_test_vejez(paciente_id, datos_paciente))
            
            # GRUPO 4: TUBERCULOSIS (Variable 18)
            variables_pedt.update(self._calcular_variables_tuberculosis(paciente_id, datos_paciente))
            
            # GRUPO 5: RIESGO CARDIOVASCULAR (Variables 19-21)
            variables_pedt.update(self._calcular_variables_riesgo_cardiovascular(paciente_id, datos_paciente))
            
            # GRUPO 6: SALUD MENTAL (Variables 22-25)
            variables_pedt.update(self._calcular_variables_salud_mental(paciente_id, datos_paciente))
            
            # GRUPO 7: CONTROL PRENATAL (Variables 26-45)
            variables_pedt.update(self._calcular_variables_control_prenatal(paciente_id, datos_paciente))
            
            # GRUPO 8: CRECIMIENTO Y DESARROLLO (Variables 46-55)
            variables_pedt.update(self._calcular_variables_crecimiento_desarrollo(paciente_id, datos_paciente))
            
            # GRUPO 9: CONSULTAS CURSO VIDA (Variables 56-63)
            variables_pedt.update(self._calcular_variables_consultas_curso_vida(paciente_id, datos_paciente))
            
            # GRUPO 10: VACUNACIÓN (Variables 64-95)
            variables_pedt.update(self._calcular_variables_vacunacion(paciente_id, datos_paciente))
            
            # GRUPO 11: SALUD ORAL (Variables 96-99)
            variables_pedt.update(self._calcular_variables_salud_oral(paciente_id, datos_paciente))
            
            # GRUPO 12: ATENCIÓN PARTO (Variables 100-107)
            variables_pedt.update(self._calcular_variables_atencion_parto(paciente_id, datos_paciente))
            
            # GRUPO 13: TAMIZAJES DIAGNÓSTICOS (Variables 108-119)
            variables_pedt.update(self._calcular_variables_tamizajes(paciente_id, datos_paciente))
            
            logger.info(f"Variables PEDT generadas exitosamente para paciente {paciente_id}")
            return variables_pedt
            
        except Exception as e:
            logger.error(f"Error generando variables PEDT para paciente {paciente_id}: {str(e)}")
            raise
    
    def _obtener_datos_paciente(self, paciente_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos base del paciente desde tabla pacientes
        
        Returns:
            Dict con datos del paciente o None si no existe
        """
        try:
            response = self.db.table('pacientes').select('*').eq('id', str(paciente_id)).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo datos paciente {paciente_id}: {str(e)}")
            return None
    
    def _calcular_variables_identificacion(self, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula variables de identificación (0-13)
        
        Estas son variables derivadas directamente desde tabla pacientes
        """
        return {
            'var_0_tipo_registro': '1',  # Siempre individual para RIAS
            'var_1_consecutivo': datos_paciente.get('numero_documento', ''),
            'var_2_tipo_identificacion': self._mapear_tipo_identificacion(datos_paciente.get('tipo_documento')),
            'var_3_numero_identificacion': datos_paciente.get('numero_documento', ''),
            'var_4_primer_apellido': datos_paciente.get('primer_apellido', ''),
            'var_5_segundo_apellido': datos_paciente.get('segundo_apellido', ''),
            'var_6_primer_nombre': datos_paciente.get('primer_nombre', ''),
            'var_7_segundo_nombre': datos_paciente.get('segundo_nombre', ''),
            'var_8_fecha_nacimiento': self._formatear_fecha(datos_paciente.get('fecha_nacimiento')),
            'var_9_sexo': self._mapear_sexo(datos_paciente.get('genero')),
            'var_10_pertenencia_etnica': datos_paciente.get('pertenencia_etnica', 6),  # Default: Sin pertenencia
            'var_11_ocupacion': datos_paciente.get('ocupacion', 9999),  # Default: Sin información
            'var_12_nivel_educativo': datos_paciente.get('nivel_educativo', 12),  # Default: Sin información
            'var_13_codigo_ips': datos_paciente.get('codigo_ips_primaria', '')
        }
    
    def _calcular_variables_gestacion(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula variables de gestación (14-15)
        
        VARIABLE DERIVADA CRÍTICA:
        - Variable 14: Se calcula verificando si existe atencion_materno_perinatal activa
        - Variable 15: Se deriva de datos de control prenatal
        """
        # Variable 14: Gestante
        gestante = self._es_gestante(paciente_id, datos_paciente)
        
        # Variable 15: Sífilis gestacional o congénita
        sifilis_gestacional = self._calcular_sifilis_gestacional(paciente_id) if gestante == 1 else 0
        
        return {
            'var_14_gestante': gestante,
            'var_15_sifilis_gestacional': sifilis_gestacional
        }
    
    def _es_gestante(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> int:
        """
        Calcula si la paciente está gestante (Variable 14)
        
        Lógica:
        - Si es hombre: 0 (No aplica)
        - Si es mujer y tiene atencion_materno_perinatal activa: 1 (Sí)
        - Si es mujer sin atencion_materno_perinatal: 2 (No)
        - Si no se puede evaluar: 21 (Riesgo no evaluado)
        
        Returns:
            int: Código según especificación Resolución 202
        """
        try:
            # Si es hombre, no aplica
            if datos_paciente.get('genero', '').upper() in ['M', 'MASCULINO']:
                return 0
            
            # Verificar si tiene atención materno perinatal activa
            response = self.db.table('atencion_materno_perinatal')\
                .select('id, estado')\
                .eq('paciente_id', str(paciente_id))\
                .eq('estado', 'activa')\
                .execute()
            
            if response.data and len(response.data) > 0:
                return 1  # Sí es gestante
            else:
                return 2  # No es gestante
                
        except Exception as e:
            logger.error(f"Error calculando gestante para paciente {paciente_id}: {str(e)}")
            return 21  # Riesgo no evaluado
    
    def _calcular_sifilis_gestacional(self, paciente_id: UUID) -> int:
        """
        Calcula sífilis gestacional (Variable 15)

        Implementa lógica específica basada en atención materno perinatal
        """
        try:
            # Buscar atenciones materno perinatales del paciente con resultados de sífilis
            mp_response = self.db.table("atencion_materno_perinatal").select(
                "resultado_tamizaje_sifilis, fecha_atencion"
            ).eq("paciente_id", str(paciente_id)).order("fecha_atencion", desc=True).limit(1).execute()

            if mp_response.data:
                resultado = mp_response.data[0].get("resultado_tamizaje_sifilis")
                if resultado == "POSITIVO":
                    return 1  # Sífilis gestacional detectada
                elif resultado == "NEGATIVO":
                    return 2  # Descartada
                elif resultado in ["REACTIVO", "NO_REACTIVO"]:
                    return 1 if resultado == "REACTIVO" else 2

            return 0  # No aplica / No se ha realizado
        except Exception as e:
            logger.warning(f"Error consultando sífilis gestacional: {e}")
            return 0
    
    def _calcular_variables_test_vejez(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables para población ≥60 años (16-17)
        """
        edad = self._calcular_edad(datos_paciente.get('fecha_nacimiento'))
        
        if edad and edad >= 60:
            # TODO: Implementar cuando se agreguen campos específicos
            return {
                'var_16_minimental': 0,  # Default: No se ha realizado
                'var_17_hipotiroidismo': 0  # Default: No se ha realizado
            }
        else:
            return {
                'var_16_minimental': 0,  # No aplica por edad
                'var_17_hipotiroidismo': 0  # No aplica por edad
            }
    
    def _calcular_variables_tuberculosis(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variable tuberculosis (18)
        """
        # TODO: Implementar lógica específica sintomático respiratorio
        return {
            'var_18_sintomatico_respiratorio': 0  # Default: No se ha realizado
        }
    
    def _calcular_variables_riesgo_cardiovascular(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables riesgo cardiovascular (19-21)
        """
        # TODO: Implementar cuando se agreguen campos específicos
        return {
            'var_19_consumo_tabaco': 0,  # Default: No se ha realizado
            'var_20_hipertension_arterial': 0,  # Default: No se ha realizado
            'var_21_diabetes': 0  # Default: No se ha realizado
        }
    
    def _calcular_variables_salud_mental(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables salud mental (22-25)
        """
        # TODO: Implementar lógica específica salud mental
        return {
            'var_22_victima_maltrato': 0,
            'var_23_violencia_sexual': 0,
            'var_24_atencion_salud_mental': 0,
            'var_25_interdisciplinaria_salud_mental': 0
        }
    
    def _calcular_variables_control_prenatal(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables control prenatal (26-45)
        
        VARIABLES DERIVADAS CRÍTICAS:
        Estas se mapean directamente desde detalle_control_prenatal existente
        """
        # Verificar si es gestante
        if self._es_gestante(paciente_id, datos_paciente) != 1:
            # No es gestante, todas las variables son 0 (No aplica)
            variables_cp = {}
            for i in range(26, 46):
                variables_cp[f'var_{i}_control_prenatal'] = 0
            return variables_cp
        
        try:
            # Obtener datos de control prenatal más reciente
            response = self.db.table('detalle_control_prenatal')\
                .select('*')\
                .eq('atencion_materno_perinatal_id', 
                    f"(SELECT id FROM atencion_materno_perinatal WHERE paciente_id = '{paciente_id}' AND estado = 'activa')")\
                .order('fecha_atencion', desc=True)\
                .limit(1)\
                .execute()
            
            if response.data and len(response.data) > 0:
                datos_cp = response.data[0]
                return self._mapear_datos_control_prenatal(datos_cp)
            else:
                # Gestante pero sin datos de control prenatal aún
                variables_cp = {}
                for i in range(26, 46):
                    variables_cp[f'var_{i}_control_prenatal'] = 0
                return variables_cp
                
        except Exception as e:
            logger.error(f"Error calculando variables control prenatal para {paciente_id}: {str(e)}")
            # Error en consulta, valores por defecto
            variables_cp = {}
            for i in range(26, 46):
                variables_cp[f'var_{i}_control_prenatal'] = 0
            return variables_cp
    
    def _mapear_datos_control_prenatal(self, datos_cp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapea datos de detalle_control_prenatal a variables PEDT 26-45
        
        MAPEO DIRECTO desde BD existente:
        - Variable 33: fecha_probable_parto (ya existe)
        - Variable 35: riesgo_biopsicosocial (ya existe como ENUM)
        """
        return {
            'var_26_fecha_ultima_regla': self._formatear_fecha(datos_cp.get('fecha_ultima_regla')),
            'var_27_edad_gestacional': datos_cp.get('edad_gestacional_semanas', 0),
            'var_28_altura_uterina': datos_cp.get('altura_uterina_cm', 0),
            'var_29_peso_actual': datos_cp.get('peso_actual_kg', 0),
            'var_30_imc_pregestacional': datos_cp.get('imc_pregestacional', 0),
            'var_31_tension_sistolica': datos_cp.get('tension_arterial_sistolica', 0),
            'var_32_tension_diastolica': datos_cp.get('tension_arterial_diastolica', 0),
            'var_33_fecha_probable_parto': self._formatear_fecha(datos_cp.get('fecha_probable_parto')),  # MAPEO DIRECTO
            'var_34_numero_embarazos': datos_cp.get('numero_embarazos_previos', 0),
            'var_35_riesgo_gestacional': self._mapear_riesgo_biopsicosocial(datos_cp.get('riesgo_biopsicosocial')),  # MAPEO DIRECTO ENUM
            # Variables 36-45: Suministros y otros controles
            'var_36_acido_folico': datos_cp.get('suministro_acido_folico', 0),
            'var_37_sulfato_ferroso': datos_cp.get('suministro_sulfato_ferroso', 0),
            'var_38_carbonato_calcio': datos_cp.get('suministro_carbonato_calcio', 0),
            # Resto de variables por defecto hasta implementar campos específicos
            **{f'var_{i}_control_prenatal_detalle': 0 for i in range(39, 46)}
        }
    
    def _calcular_variables_crecimiento_desarrollo(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables crecimiento y desarrollo primera infancia (46-55)
        Implementa lógica específica basada en atención primera infancia y datos EAD-3/ASQ-3
        """
        edad = self._calcular_edad(datos_paciente.get('fecha_nacimiento'))

        if edad and edad <= 10:
            # Buscar atenciones de primera infancia con datos EAD-3/ASQ-3
            try:
                pi_response = self.db.table("atencion_primera_infancia").select(
                    "peso_kg, talla_cm, estado_nutricional, desarrollo_fisico_motor_observaciones, "
                    "desarrollo_cognitivo_observaciones, esquema_vacunacion_completo, "
                    "ead_resultado_global, asq_resultado_global, fecha_atencion"
                ).eq("paciente_id", str(paciente_id)).order("fecha_atencion", desc=True).limit(1).execute()

                if pi_response.data:
                    datos_pi = pi_response.data[0]
                    return {
                        'var_46_peso_actual': datos_pi.get('peso_kg', 0),
                        'var_47_talla_actual': datos_pi.get('talla_cm', 0),
                        'var_48_estado_nutricional': self._mapear_estado_nutricional(datos_pi.get('estado_nutricional')),
                        'var_49_desarrollo_motor': self._evaluar_desarrollo_motor(datos_pi.get('desarrollo_fisico_motor_observaciones')),
                        'var_50_desarrollo_cognitivo': self._evaluar_desarrollo_cognitivo(datos_pi.get('desarrollo_cognitivo_observaciones')),
                        'var_51_esquema_vacunacion': 1 if datos_pi.get('esquema_vacunacion_completo') else 0,
                        'var_52_ead_resultado': self._mapear_ead_resultado(datos_pi.get('ead_resultado_global')),
                        'var_53_asq_resultado': self._mapear_asq_resultado(datos_pi.get('asq_resultado_global')),
                        'var_54_desarrollo_global': self._calcular_desarrollo_global(datos_pi),
                        'var_55_alertas_desarrollo': self._identificar_alertas_desarrollo(datos_pi)
                    }
                else:
                    # Sin datos de primera infancia
                    return {**{f'var_{i}_crecimiento_desarrollo': 0 for i in range(46, 56)}}

            except Exception as e:
                logger.warning(f"Error consultando datos primera infancia: {e}")
                return {**{f'var_{i}_crecimiento_desarrollo': 0 for i in range(46, 56)}}
        else:
            # No aplica por edad
            return {**{f'var_{i}_crecimiento_desarrollo': 0 for i in range(46, 56)}}
    
    def _calcular_variables_consultas_curso_vida(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables consultas por curso de vida (56-63)
        """
        # TODO: Implementar lógica específica consultas por edad
        return {
            **{f'var_{i}_consulta_curso_vida': 0 for i in range(56, 64)}
        }
    
    def _calcular_variables_vacunacion(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables vacunación esquema PAI (64-95)
        """
        edad = self._calcular_edad(datos_paciente.get('fecha_nacimiento'))
        
        if edad and edad <= 6:
            # TODO: Implementar cuando se agregue tabla vacunas
            return {
                **{f'var_{i}_vacuna': 0 for i in range(64, 96)}
            }
        else:
            # No aplica por edad
            return {
                **{f'var_{i}_vacuna': 0 for i in range(64, 96)}
            }
    
    def _calcular_variables_salud_oral(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables salud oral (96-99)
        """
        # TODO: Implementar campos salud oral
        return {
            **{f'var_{i}_salud_oral': 0 for i in range(96, 100)}
        }
    
    def _calcular_variables_atencion_parto(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables atención del parto (100-107)
        """
        # TODO: Implementar cuando se agreguen campos parto
        return {
            **{f'var_{i}_atencion_parto': 0 for i in range(100, 108)}
        }
    
    def _calcular_variables_tamizajes(self, paciente_id: UUID, datos_paciente: Dict[str, Any]) -> Dict[str, Any]:
        """
        Variables tamizajes y pruebas diagnósticas (108-119)
        """
        # TODO: Implementar cuando se agreguen campos tamizajes
        return {
            **{f'var_{i}_tamizaje': 0 for i in range(108, 120)}
        }
    
    # MÉTODOS UTILITARIOS
    
    def _mapear_tipo_identificacion(self, tipo_doc: str) -> str:
        """Mapea tipo documento a códigos SISPRO"""
        mapeo = {
            'CC': 'CC',
            'TI': 'TI', 
            'CE': 'CE',
            'RC': 'RC',
            'PA': 'PA',
            'MS': 'MS'
        }
        return mapeo.get(tipo_doc, 'CC')  # Default CC
    
    def _mapear_sexo(self, sexo: str) -> str:
        """Mapea sexo a códigos SISPRO"""
        if not sexo:
            return 'M'
        
        sexo_upper = sexo.upper()
        if sexo_upper in ['F', 'FEMENINO', 'MUJER']:
            return 'F'
        elif sexo_upper in ['M', 'MASCULINO', 'HOMBRE']:
            return 'M'
        else:
            return 'M'  # Default
    
    def _mapear_riesgo_biopsicosocial(self, riesgo: str) -> int:
        """
        Mapea ENUM riesgo biopsicosocial a códigos Resolución 202
        
        Según equipo consultor externo:
        - 4: Alto riesgo
        - 5: Bajo riesgo
        """
        if not riesgo:
            return 0  # No aplica
        
        riesgo_lower = riesgo.lower()
        if 'alto' in riesgo_lower:
            return 4
        elif 'bajo' in riesgo_lower:
            return 5
        else:
            return 0  # No aplica
    
    def _formatear_fecha(self, fecha: Union[str, date, datetime, None]) -> str:
        """Formatea fecha a AAAA-MM-DD requerido por SISPRO"""
        if not fecha:
            return ''
        
        if isinstance(fecha, str):
            try:
                # Intentar parsear diferentes formatos
                if len(fecha) == 10 and '-' in fecha:
                    return fecha  # Ya está en formato correcto
                # TODO: Agregar más formatos si es necesario
                return fecha
            except:
                return ''
        
        if isinstance(fecha, (date, datetime)):
            return fecha.strftime('%Y-%m-%d')
        
        return ''
    
    def _calcular_edad(self, fecha_nacimiento: Union[str, date, datetime, None]) -> Optional[int]:
        """Calcula edad en años"""
        if not fecha_nacimiento:
            return None
        
        try:
            if isinstance(fecha_nacimiento, str):
                fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            elif isinstance(fecha_nacimiento, datetime):
                fecha_nac = fecha_nacimiento.date()
            elif isinstance(fecha_nacimiento, date):
                fecha_nac = fecha_nacimiento
            else:
                return None
            
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            return edad
            
        except:
            return None
    
    def aplicar_validaciones_202(self, variables_pedt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica validaciones según Controles_RPED_202.csv
        
        Args:
            variables_pedt: Dict con 119 variables calculadas
            
        Returns:
            Dict con validaciones aplicadas y errores identificados
        """
        validaciones = {
            'es_valido': True,
            'errores': [],
            'warnings': []
        }
        
        # TODO: Implementar validaciones específicas de Resolución 202
        # Por ahora validaciones básicas
        
        # Validación: Variables obligatorias
        variables_obligatorias = [
            'var_1_consecutivo', 'var_2_tipo_identificacion', 
            'var_3_numero_identificacion', 'var_8_fecha_nacimiento'
        ]
        
        for var_obligatoria in variables_obligatorias:
            if not variables_pedt.get(var_obligatoria):
                validaciones['errores'].append(f"Variable {var_obligatoria} es obligatoria")
                validaciones['es_valido'] = False
        
        return validaciones
    
    def generar_archivo_plano_sispro(self, datos_pacientes: List[Dict[str, Any]], 
                                   periodo: str = None) -> str:
        """
        Genera archivo plano para reporte SISPRO
        
        Args:
            datos_pacientes: Lista de dict con variables PEDT de cada paciente
            periodo: Período del reporte (AAAA-MM)
            
        Returns:
            str: Contenido del archivo plano
        """
        if not periodo:
            periodo = datetime.now().strftime('%Y-%m')
        
        lineas = []
        
        for datos_paciente in datos_pacientes:
            # Construir línea del archivo según especificación SISPRO
            # TODO: Implementar formato exacto según especificación
            linea = self._construir_linea_sispro(datos_paciente)
            lineas.append(linea)
        
        archivo_contenido = '\n'.join(lineas)
        
        logger.info(f"Archivo plano SISPRO generado: {len(lineas)} registros para período {periodo}")
        return archivo_contenido
    
    def _construir_linea_sispro(self, variables_pedt: Dict[str, Any]) -> str:
        """
        Construye una línea del archivo SISPRO con las 119 variables
        
        Returns:
            str: Línea formateada según especificación
        """
        # TODO: Implementar formato exacto según Anexos.csv
        # Por ahora formato básico separado por pipes
        campos = []
        
        for i in range(119):
            var_key = f'var_{i}'
            valor = variables_pedt.get(var_key, '0')  # Default 0 si no existe
            campos.append(str(valor))
        
        return '|'.join(campos)

    # =====================================================
    # MÉTODOS AUXILIARES PARA MAPEO DE DATOS ESPECÍFICOS
    # =====================================================

    def _mapear_estado_nutricional(self, estado: str) -> int:
        """Mapea estado nutricional a código PEDT"""
        mapeo = {
            'NORMAL': 1,
            'DESNUTRICION_AGUDA': 2,
            'SOBREPESO': 3,
            'OBESIDAD': 4,
            'RIESGO_DESNUTRICION': 5
        }
        return mapeo.get(estado, 0)

    def _evaluar_desarrollo_motor(self, observaciones: str) -> int:
        """Evalúa desarrollo motor basado en observaciones"""
        if not observaciones:
            return 0

        observaciones_lower = observaciones.lower()
        if 'normal' in observaciones_lower or 'adecuado' in observaciones_lower:
            return 1
        elif 'riesgo' in observaciones_lower or 'alerta' in observaciones_lower:
            return 2
        elif 'retraso' in observaciones_lower or 'alterado' in observaciones_lower:
            return 3
        return 0

    def _evaluar_desarrollo_cognitivo(self, observaciones: str) -> int:
        """Evalúa desarrollo cognitivo basado en observaciones"""
        if not observaciones:
            return 0

        observaciones_lower = observaciones.lower()
        if 'normal' in observaciones_lower or 'adecuado' in observaciones_lower:
            return 1
        elif 'riesgo' in observaciones_lower or 'alerta' in observaciones_lower:
            return 2
        elif 'retraso' in observaciones_lower or 'alterado' in observaciones_lower:
            return 3
        return 0

    def _mapear_ead_resultado(self, resultado: str) -> int:
        """Mapea resultado EAD-3 a código PEDT"""
        if not resultado:
            return 0

        mapeo = {
            'NORMAL': 1,
            'ALERTA': 2,
            'MEDIO': 2,
            'ALTO': 3
        }
        return mapeo.get(resultado, 0)

    def _mapear_asq_resultado(self, resultado: str) -> int:
        """Mapea resultado ASQ-3 a código PEDT"""
        if not resultado:
            return 0

        mapeo = {
            'NORMAL': 1,
            'SEGUIMIENTO': 2,
            'REFERIR': 3
        }
        return mapeo.get(resultado, 0)

    def _calcular_desarrollo_global(self, datos_pi: Dict[str, Any]) -> int:
        """Calcula desarrollo global basado en múltiples indicadores"""
        ead = self._mapear_ead_resultado(datos_pi.get('ead_resultado_global'))
        asq = self._mapear_asq_resultado(datos_pi.get('asq_resultado_global'))

        # Si ambos están normales
        if ead == 1 and asq == 1:
            return 1  # Normal
        # Si alguno tiene alerta
        elif ead == 2 or asq == 2:
            return 2  # Seguimiento
        # Si alguno requiere referencia
        elif ead == 3 or asq == 3:
            return 3  # Intervención

        return 0  # No evaluado

    def _identificar_alertas_desarrollo(self, datos_pi: Dict[str, Any]) -> int:
        """Identifica si hay alertas de desarrollo que requieren acción"""
        alertas = 0

        # Verificar alertas en EAD-3
        if datos_pi.get('ead_resultado_global') in ['ALERTA', 'ALTO']:
            alertas += 1

        # Verificar alertas en ASQ-3
        if datos_pi.get('asq_resultado_global') in ['REFERIR']:
            alertas += 1

        # Verificar estado nutricional
        if datos_pi.get('estado_nutricional') in ['DESNUTRICION_AGUDA', 'OBESIDAD']:
            alertas += 1

        return min(alertas, 3)  # Máximo 3 alertas

    def _mapear_riesgo_biopsicosocial(self, riesgo: str) -> int:
        """Mapea riesgo biopsicosocial a código PEDT"""
        if not riesgo:
            return 0

        mapeo = {
            'BAJO': 1,
            'MEDIO': 2,
            'ALTO': 3,
            'MUY_ALTO': 4
        }
        return mapeo.get(riesgo, 0)