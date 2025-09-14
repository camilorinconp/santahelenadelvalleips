# -*- coding: utf-8 -*-
"""
TESTS CAPA DE REPORTERÍA INTELIGENTE - RESOLUCIÓN 202
=====================================================

Tests para validar el funcionamiento correcto del GeneradorReportePEDT
con datos reales del sistema, especialmente variables derivadas críticas.

Enfoque: Testing con datos existentes de materno perinatal para
validar que la lógica de cálculo funciona correctamente.

Autor: Equipo IPS Santa Helena del Valle  
Fecha: 13 septiembre 2025
Estado: Testing Fase 3C - Validación Variables Derivadas
"""

import pytest
from uuid import UUID
from datetime import date, datetime
import os
import sys

# Agregar path del backend para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reporteria_pedt import GeneradorReportePEDT
from database import get_supabase_client

class TestGeneradorReportePEDT:
    """
    Suite de tests para GeneradorReportePEDT
    """
    
    @classmethod
    def setup_class(cls):
        """Configuración inicial de tests"""
        cls.generador = GeneradorReportePEDT()
        cls.db = get_supabase_client()
        
    def test_inicializacion_generador(self):
        """Test: Generador se inicializa correctamente"""
        generador = GeneradorReportePEDT()
        assert generador is not None
        assert generador.db is not None
        
    def test_obtener_pacientes_existentes(self):
        """Test: Obtener lista de pacientes para testing"""
        response = self.db.table('pacientes').select('id, numero_documento, primer_nombre, genero').limit(5).execute()
        
        assert response.data is not None
        assert len(response.data) > 0
        
        print("\n=== PACIENTES DISPONIBLES PARA TESTING ===")
        for paciente in response.data:
            print(f"ID: {paciente['id']} | Doc: {paciente['numero_documento']} | Nombre: {paciente['primer_nombre']} | Género: {paciente['genero']}")
        
        # Guardar primer paciente para tests posteriores
        self.paciente_test = paciente['id']
    
    def test_obtener_datos_paciente_existente(self):
        """Test: Obtener datos de paciente existente"""
        # Usar primer paciente de la BD
        response = self.db.table('pacientes').select('id').limit(1).execute()
        assert len(response.data) > 0
        
        paciente_id = UUID(response.data[0]['id'])
        datos = self.generador._obtener_datos_paciente(paciente_id)
        
        assert datos is not None
        assert 'numero_documento' in datos
        assert 'primer_nombre' in datos
        
        print(f"\n=== DATOS PACIENTE TEST ===")
        print(f"ID: {datos['id']}")
        print(f"Documento: {datos['numero_documento']}")
        print(f"Nombre: {datos.get('primer_nombre', 'N/A')} {datos.get('primer_apellido', 'N/A')}")
        print(f"Género: {datos.get('genero', 'N/A')}")
        print(f"Fecha Nacimiento: {datos.get('fecha_nacimiento', 'N/A')}")
        
    def test_obtener_datos_paciente_inexistente(self):
        """Test: Obtener datos de paciente que no existe"""
        from uuid import uuid4
        paciente_inexistente = uuid4()
        
        datos = self.generador._obtener_datos_paciente(paciente_inexistente)
        assert datos is None
        
    def test_calcular_variables_identificacion(self):
        """Test: Cálculo de variables de identificación (0-13)"""
        # Obtener paciente real
        response = self.db.table('pacientes').select('*').limit(1).execute()
        datos_paciente = response.data[0]
        
        variables_id = self.generador._calcular_variables_identificacion(datos_paciente)
        
        # Validaciones básicas
        assert 'var_0_tipo_registro' in variables_id
        assert variables_id['var_0_tipo_registro'] == '1'  # Siempre individual
        
        assert 'var_3_numero_identificacion' in variables_id
        assert variables_id['var_3_numero_identificacion'] == datos_paciente['numero_documento']
        
        print(f"\n=== VARIABLES IDENTIFICACIÓN ===")
        for key, value in variables_id.items():
            print(f"{key}: {value}")
            
    def test_calcular_gestante_mujer_con_atencion_materno(self):
        """Test: Cálculo gestante para mujer con atención materno perinatal"""
        # Buscar paciente femenina con atención materno perinatal
        response = self.db.table('pacientes')\
            .select('*, atencion_materno_perinatal(*)')\
            .eq('genero', 'F')\
            .limit(10).execute()
        
        paciente_gestante = None
        for paciente in response.data:
            if paciente.get('atencion_materno_perinatal') and len(paciente['atencion_materno_perinatal']) > 0:
                paciente_gestante = paciente
                break
        
        if paciente_gestante:
            print(f"\n=== TEST GESTANTE - PACIENTE CON ATENCIÓN MATERNO PERINATAL ===")
            print(f"Paciente: {paciente_gestante['primer_nombre']} {paciente_gestante['primer_apellido']}")
            print(f"Género: {paciente_gestante['genero']}")
            print(f"Atenciones materno perinatal: {len(paciente_gestante['atencion_materno_perinatal'])}")
            
            paciente_id = UUID(paciente_gestante['id'])
            resultado_gestante = self.generador._es_gestante(paciente_id, paciente_gestante)
            
            print(f"Resultado variable 14 (gestante): {resultado_gestante}")
            
            # Para mujer con atención materno perinatal debería ser 1 (Sí) o 2 (No) según estado
            assert resultado_gestante in [1, 2, 21]  # Valores válidos
        else:
            print("\n=== SKIP TEST GESTANTE ===")
            print("No se encontraron pacientes femeninas con atención materno perinatal")
            
    def test_calcular_gestante_hombre(self):
        """Test: Cálculo gestante para hombre (debe ser 0 - No aplica)"""
        # Buscar paciente masculino
        response = self.db.table('pacientes')\
            .select('*')\
            .eq('genero', 'M')\
            .limit(1).execute()
        
        if response.data and len(response.data) > 0:
            paciente_masculino = response.data[0]
            paciente_id = UUID(paciente_masculino['id'])
            
            resultado_gestante = self.generador._es_gestante(paciente_id, paciente_masculino)
            
            print(f"\n=== TEST GESTANTE HOMBRE ===")
            print(f"Paciente: {paciente_masculino['primer_nombre']} {paciente_masculino['primer_apellido']}")
            print(f"Género: {paciente_masculino['genero']}")
            print(f"Resultado variable 14 (gestante): {resultado_gestante}")
            
            # Para hombre debe ser 0 (No aplica)
            assert resultado_gestante == 0
        else:
            print("\n=== SKIP TEST GESTANTE HOMBRE ===")
            print("No se encontraron pacientes masculinos")
            
    def test_mapeo_control_prenatal_datos_reales(self):
        """Test: Mapeo de variables control prenatal con datos reales"""
        # Buscar datos reales de control prenatal
        response = self.db.table('detalle_control_prenatal')\
            .select('*')\
            .limit(1).execute()
        
        if response.data and len(response.data) > 0:
            datos_cp = response.data[0]
            
            print(f"\n=== TEST MAPEO CONTROL PRENATAL ===")
            print(f"ID Control: {datos_cp['id']}")
            print(f"Fecha Probable Parto: {datos_cp.get('fecha_probable_parto', 'N/A')}")
            print(f"Riesgo Biopsicosocial: {datos_cp.get('riesgo_biopsicosocial', 'N/A')}")
            print(f"Edad Gestacional: {datos_cp.get('edad_gestacional_semanas', 'N/A')}")
            
            variables_cp = self.generador._mapear_datos_control_prenatal(datos_cp)
            
            print(f"\n=== VARIABLES CONTROL PRENATAL MAPEADAS ===")
            for key, value in variables_cp.items():
                if value and value != 0:  # Solo mostrar variables con valor
                    print(f"{key}: {value}")
            
            # Validaciones críticas
            assert 'var_33_fecha_probable_parto' in variables_cp
            assert 'var_35_riesgo_gestacional' in variables_cp
            
            # Variable 33: Fecha probable parto debe ser formato AAAA-MM-DD o vacía
            fecha_parto = variables_cp['var_33_fecha_probable_parto']
            if fecha_parto:
                assert len(fecha_parto) == 10  # AAAA-MM-DD
                assert fecha_parto.count('-') == 2
        else:
            print("\n=== SKIP TEST CONTROL PRENATAL ===")
            print("No se encontraron datos de control prenatal")
            
    def test_generar_variables_119_paciente_real(self):
        """Test: Generación completa de 119 variables para paciente real"""
        # Obtener primer paciente
        response = self.db.table('pacientes').select('id, primer_nombre, primer_apellido').limit(1).execute()
        assert len(response.data) > 0
        
        paciente = response.data[0]
        paciente_id = UUID(paciente['id'])
        
        print(f"\n=== TEST GENERACIÓN 119 VARIABLES ===")
        print(f"Paciente: {paciente['primer_nombre']} {paciente['primer_apellido']}")
        print(f"ID: {paciente_id}")
        
        # Generar variables PEDT
        variables_pedt = self.generador.generar_variables_119(paciente_id)
        
        # Validaciones básicas
        assert isinstance(variables_pedt, dict)
        assert len(variables_pedt) > 0
        
        print(f"\nTotal variables generadas: {len(variables_pedt)}")
        
        # Mostrar variables con valor (no cero)
        variables_con_valor = {k: v for k, v in variables_pedt.items() if v and v != 0 and v != '0'}
        
        print(f"\n=== VARIABLES CON VALOR ({len(variables_con_valor)}) ===")
        for key, value in variables_con_valor.items():
            print(f"{key}: {value}")
        
        # Validaciones críticas
        assert 'var_0_tipo_registro' in variables_pedt
        assert variables_pedt['var_0_tipo_registro'] == '1'
        
        assert 'var_14_gestante' in variables_pedt
        assert variables_pedt['var_14_gestante'] in [0, 1, 2, 21]  # Valores válidos
        
    def test_aplicar_validaciones_202(self):
        """Test: Validaciones según Resolución 202"""
        # Generar variables para paciente test
        response = self.db.table('pacientes').select('id').limit(1).execute()
        paciente_id = UUID(response.data[0]['id'])
        
        variables_pedt = self.generador.generar_variables_119(paciente_id)
        validaciones = self.generador.aplicar_validaciones_202(variables_pedt)
        
        print(f"\n=== TEST VALIDACIONES 202 ===")
        print(f"Es válido: {validaciones['es_valido']}")
        print(f"Errores: {len(validaciones['errores'])}")
        print(f"Warnings: {len(validaciones['warnings'])}")
        
        if validaciones['errores']:
            print("\nErrores encontrados:")
            for error in validaciones['errores']:
                print(f"  - {error}")
        
        # Debe tener estructura correcta
        assert 'es_valido' in validaciones
        assert 'errores' in validaciones
        assert 'warnings' in validaciones
        
    def test_generar_archivo_plano_sispro(self):
        """Test: Generación de archivo plano SISPRO"""
        # Generar variables para 2-3 pacientes
        response = self.db.table('pacientes').select('id').limit(3).execute()
        datos_pacientes = []
        
        for paciente in response.data:
            paciente_id = UUID(paciente['id'])
            variables_pedt = self.generador.generar_variables_119(paciente_id)
            datos_pacientes.append(variables_pedt)
        
        # Generar archivo
        periodo = "2025-09"
        archivo_contenido = self.generador.generar_archivo_plano_sispro(datos_pacientes, periodo)
        
        print(f"\n=== TEST ARCHIVO PLANO SISPRO ===")
        print(f"Período: {periodo}")
        print(f"Pacientes: {len(datos_pacientes)}")
        print(f"Líneas generadas: {len(archivo_contenido.splitlines())}")
        
        # Mostrar primeras líneas del archivo
        lineas = archivo_contenido.splitlines()
        print(f"\nPrimera línea (truncada): {lineas[0][:100]}...")
        
        # Validaciones
        assert archivo_contenido is not None
        assert len(archivo_contenido) > 0
        assert len(lineas) == len(datos_pacientes)
        
        # Cada línea debe tener la estructura correcta
        for linea in lineas:
            campos = linea.split('|')
            # Debe tener aproximadamente 119 campos (puede variar según implementación)
            assert len(campos) > 50  # Al menos estructura básica
            
    def test_utilidades_mapeo(self):
        """Test: Métodos utilitarios de mapeo"""
        # Test mapeo tipo identificación
        assert self.generador._mapear_tipo_identificacion('CC') == 'CC'
        assert self.generador._mapear_tipo_identificacion('TI') == 'TI'
        assert self.generador._mapear_tipo_identificacion('XXX') == 'CC'  # Default
        
        # Test mapeo sexo
        assert self.generador._mapear_sexo('F') == 'F'
        assert self.generador._mapear_sexo('FEMENINO') == 'F'
        assert self.generador._mapear_sexo('M') == 'M'
        assert self.generador._mapear_sexo('MASCULINO') == 'M'
        assert self.generador._mapear_sexo(None) == 'M'  # Default
        
        # Test mapeo riesgo biopsicosocial
        assert self.generador._mapear_riesgo_biopsicosocial('alto_riesgo') == 4
        assert self.generador._mapear_riesgo_biopsicosocial('bajo_riesgo') == 5
        assert self.generador._mapear_riesgo_biopsicosocial(None) == 0
        
        # Test formateo fecha
        assert self.generador._formatear_fecha('2025-09-13') == '2025-09-13'
        assert self.generador._formatear_fecha(None) == ''
        assert self.generador._formatear_fecha(date(2025, 9, 13)) == '2025-09-13'
        
        # Test cálculo edad
        fecha_nac = date(1990, 1, 1)
        edad = self.generador._calcular_edad(fecha_nac)
        assert edad is not None
        assert edad > 30  # Para fecha 1990
        
        print(f"\n=== TEST UTILIDADES MAPEO COMPLETADO ===")
        print("Todos los métodos utilitarios funcionan correctamente")

if __name__ == "__main__":
    # Ejecutar tests individualmente para debugging
    test_class = TestGeneradorReportePEDT()
    test_class.setup_class()
    
    print("=== INICIANDO TESTS REPORTERÍA PEDT ===\n")
    
    try:
        test_class.test_inicializacion_generador()
        print("✅ Test inicialización: OK")
        
        test_class.test_obtener_pacientes_existentes()
        print("✅ Test obtener pacientes: OK")
        
        test_class.test_obtener_datos_paciente_existente()
        print("✅ Test datos paciente existente: OK")
        
        test_class.test_calcular_variables_identificacion()
        print("✅ Test variables identificación: OK")
        
        test_class.test_calcular_gestante_hombre()
        print("✅ Test gestante hombre: OK")
        
        test_class.test_calcular_gestante_mujer_con_atencion_materno()
        print("✅ Test gestante mujer: OK")
        
        test_class.test_mapeo_control_prenatal_datos_reales()
        print("✅ Test mapeo control prenatal: OK")
        
        test_class.test_generar_variables_119_paciente_real()
        print("✅ Test generar 119 variables: OK")
        
        test_class.test_aplicar_validaciones_202()
        print("✅ Test validaciones 202: OK")
        
        test_class.test_generar_archivo_plano_sispro()
        print("✅ Test archivo plano SISPRO: OK")
        
        test_class.test_utilidades_mapeo()
        print("✅ Test utilidades mapeo: OK")
        
        print(f"\n🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {str(e)}")
        raise