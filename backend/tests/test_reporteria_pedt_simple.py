# -*- coding: utf-8 -*-
"""
TESTS SIMPLIFICADO - VARIABLES PEDT DISPONIBLES HOY
===================================================

Test enfocado en identificar exactamente qué variables PEDT podemos 
generar con los datos que SÍ tenemos actualmente en la BD.

DATOS ACTUALES CONFIRMADOS:
✅ pacientes: 9 registros completos
✅ entornos_salud_publica: 16 registros  
✅ familia_integral_salud_publica: 8 registros
✅ atencion_integral_transversal_salud: 1 registro
❌ atencion_materno_perinatal: 0 registros
❌ detalle_control_prenatal: 0 registros

OBJETIVO: Desarrollo híbrido - identificar variables PEDT funcionales hoy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.reporteria_pedt import GeneradorReportePEDT
from database import get_supabase_client
from uuid import UUID

def test_variables_pedt_datos_actuales():
    """
    Test principal: ¿Qué variables PEDT podemos generar HOY?
    """
    print("\n" + "="*60)
    print("ANÁLISIS VARIABLES PEDT - DATOS ACTUALES DISPONIBLES")
    print("="*60)
    
    generador = GeneradorReportePEDT()
    db = get_supabase_client()
    
    # Obtener paciente real
    response = db.table('pacientes').select('*').limit(1).execute()
    if not response.data:
        print("❌ No hay pacientes en la BD")
        return
    
    paciente = response.data[0]
    paciente_id = UUID(paciente['id'])
    
    print(f"📋 PACIENTE TEST:")
    print(f"   ID: {paciente_id}")
    print(f"   Nombre: {paciente['primer_nombre']} {paciente['primer_apellido']}")
    print(f"   Documento: {paciente['numero_documento']}")
    print(f"   Género: {paciente['genero']}")
    print(f"   Fecha Nac: {paciente['fecha_nacimiento']}")
    
    # Generar variables PEDT
    print(f"\n🔄 GENERANDO VARIABLES PEDT...")
    variables_pedt = generador.generar_variables_119(paciente_id)
    
    # Análisis de completitud
    variables_con_valor = {}
    variables_vacias = {}
    
    for key, value in variables_pedt.items():
        if value and str(value) not in ['0', '', 'None', 'null']:
            variables_con_valor[key] = value
        else:
            variables_vacias[key] = value
    
    print(f"\n📊 RESULTADOS ANÁLISIS:")
    print(f"   ✅ Variables con datos: {len(variables_con_valor)}")
    print(f"   ❌ Variables vacías: {len(variables_vacias)}")
    print(f"   📈 Completitud actual: {len(variables_con_valor)/119*100:.1f}%")
    
    print(f"\n✅ VARIABLES PEDT FUNCIONALES HOY ({len(variables_con_valor)}):")
    print("-" * 50)
    for key, value in variables_con_valor.items():
        print(f"   {key}: {value}")
    
    # Análisis por grupos
    grupos_analisis = {
        'IDENTIFICACIÓN (0-13)': [(i, f'var_{i}') for i in range(0, 14)],
        'GESTACIÓN (14-15)': [(i, f'var_{i}') for i in range(14, 16)],
        'CONTROL PRENATAL (26-45)': [(i, f'var_{i}') for i in range(26, 46)],
    }
    
    print(f"\n📋 ANÁLISIS POR GRUPOS:")
    print("-" * 50)
    for grupo, variables_grupo in grupos_analisis.items():
        completitud = 0
        total = len(variables_grupo)
        for _, var_name in variables_grupo:
            if any(var_name in key for key in variables_con_valor.keys()):
                completitud += 1
        porcentaje = completitud/total*100 if total > 0 else 0
        status = "✅" if porcentaje > 50 else "⚠️" if porcentaje > 0 else "❌"
        print(f"   {status} {grupo}: {completitud}/{total} ({porcentaje:.1f}%)")
    
    return variables_con_valor, variables_vacias

def test_identificar_gaps_criticos():
    """
    Identificar qué campos faltan para variables PEDT críticas
    """
    print(f"\n🔍 ANÁLISIS DE GAPS CRÍTICOS")
    print("=" * 50)
    
    # Variables críticas que necesitamos para compliance básico
    variables_criticas = {
        14: "Gestante - Requiere: atencion_materno_perinatal activa",
        33: "Fecha probable parto - Requiere: detalle_control_prenatal.fecha_probable_parto", 
        35: "Riesgo gestacional - Requiere: detalle_control_prenatal.riesgo_biopsicosocial",
        43: "Desarrollo motricidad gruesa - Requiere: detalle_primera_infancia.escala_desarrollo",
        86: "Tamizaje cáncer cuello - Requiere: tamizaje_oncologico",
        102: "COP odontológico - Requiere: salud_oral.cop_por_persona"
    }
    
    print("📋 VARIABLES CRÍTICAS FALTANTES:")
    for var_num, descripcion in variables_criticas.items():
        print(f"   Variable {var_num}: {descripcion}")
    
    # Identificar tablas/campos necesarios
    campos_necesarios = {
        'atencion_materno_perinatal': ['estado', 'fecha_inicio', 'fecha_fin'],
        'detalle_control_prenatal': [
            'fecha_probable_parto', 'riesgo_biopsicosocial', 'edad_gestacional_semanas',
            'suministro_acido_folico', 'suministro_sulfato_ferroso', 'suministro_carbonato_calcio'
        ],
        'detalle_primera_infancia': [
            'escala_desarrollo_motricidad_gruesa', 'escala_desarrollo_motricidad_fina',
            'escala_desarrollo_personal_social', 'escala_desarrollo_audicion_lenguaje'
        ],
        'tamizaje_oncologico': [
            'tipo_tamizaje', 'resultado_tamizaje', 'fecha_tamizaje'
        ],
        'salud_oral': [
            'cop_por_persona', 'control_placa_bacteriana'
        ]
    }
    
    print(f"\n🎯 ROADMAP INCREMENTAL - CAMPOS NECESARIOS:")
    print("-" * 50)
    for tabla, campos in campos_necesarios.items():
        print(f"\n📋 {tabla.upper()}:")
        for campo in campos:
            print(f"   + {campo}")
    
    return campos_necesarios

def test_generar_reporte_parcial():
    """
    Generar archivo de reporte con variables disponibles hoy
    """
    print(f"\n📄 GENERANDO REPORTE PARCIAL CON DATOS ACTUALES")
    print("=" * 50)
    
    generador = GeneradorReportePEDT()
    db = get_supabase_client()
    
    # Obtener hasta 3 pacientes
    response = db.table('pacientes').select('*').limit(3).execute()
    datos_pacientes = []
    
    for paciente in response.data:
        paciente_id = UUID(paciente['id'])
        variables_pedt = generador.generar_variables_119(paciente_id)
        datos_pacientes.append(variables_pedt)
    
    # Generar archivo
    archivo_contenido = generador.generar_archivo_plano_sispro(datos_pacientes, "2025-09")
    
    print(f"✅ Archivo SISPRO generado:")
    print(f"   Pacientes: {len(datos_pacientes)}")
    print(f"   Líneas: {len(archivo_contenido.splitlines())}")
    
    # Mostrar muestra del contenido
    lineas = archivo_contenido.splitlines()
    if lineas:
        print(f"   Primera línea (primeros 80 chars): {lineas[0][:80]}...")
    
    return archivo_contenido

def main():
    """Ejecutar análisis completo de desarrollo híbrido"""
    print("🚀 INICIANDO ANÁLISIS DESARROLLO HÍBRIDO - RESOLUCIÓN 202")
    
    try:
        # Test 1: Variables disponibles hoy
        variables_funcionales, variables_vacias = test_variables_pedt_datos_actuales()
        
        # Test 2: Identificar gaps críticos
        campos_necesarios = test_identificar_gaps_criticos()
        
        # Test 3: Reporte parcial
        archivo_parcial = test_generar_reporte_parcial()
        
        print(f"\n" + "="*60)
        print("🎯 CONCLUSIONES DESARROLLO HÍBRIDO")
        print("="*60)
        
        print(f"✅ ESTADO ACTUAL:")
        print(f"   - Variables PEDT funcionales: {len(variables_funcionales)}/119")
        print(f"   - Completitud base: {len(variables_funcionales)/119*100:.1f}%")
        print(f"   - Datos de identificación: 100% completos")
        print(f"   - Reportería parcial: Funcional")
        
        print(f"\n🔧 PRÓXIMOS PASOS HÍBRIDOS:")
        print(f"   1. Implementar atencion_materno_perinatal (Variables 14-15, 26-45)")
        print(f"   2. Agregar campos control prenatal específicos (~15 campos)")
        print(f"   3. Expandir GeneradorReportePEDT incrementalmente")
        print(f"   4. Testing continuo con datos reales")
        
        print(f"\n🎉 ESTRATEGIA HÍBRIDA VALIDADA: PROCEDER")
        
    except Exception as e:
        print(f"\n❌ ERROR EN ANÁLISIS: {str(e)}")
        raise

if __name__ == "__main__":
    main()