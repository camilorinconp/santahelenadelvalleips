#!/usr/bin/env python3
# =============================================================================
# Script para Procesar Resolución 202 de 2021 - Anexos Técnicos Excel
# Convierte múltiples pestañas de Excel a CSVs individuales y analiza estructura
# =============================================================================

import pandas as pd
import os
from pathlib import Path

def process_resolucion_202_excel(excel_file_path, output_dir="resolucion_202_data"):
    """
    Procesa archivo Excel de Resolución 202 con múltiples pestañas
    
    Args:
        excel_file_path (str): Ruta al archivo Excel
        output_dir (str): Directorio donde guardar los CSVs
    """
    
    try:
        print("🔍 PROCESANDO RESOLUCIÓN 202 DE 2021 - ANEXOS TÉCNICOS")
        print(f"📁 Archivo: {excel_file_path}")
        
        # Crear directorio de salida si no existe
        Path(output_dir).mkdir(exist_ok=True)
        
        # Leer todas las hojas del Excel
        excel_data = pd.read_excel(excel_file_path, sheet_name=None, engine='openpyxl')
        
        print(f"📊 ENCONTRADAS {len(excel_data)} PESTAÑAS:")
        
        analysis_report = []
        
        for sheet_name, df in excel_data.items():
            print(f"\n📋 PROCESANDO PESTAÑA: {sheet_name}")
            print(f"   - Filas: {len(df)}")
            print(f"   - Columnas: {len(df.columns)}")
            
            # Mostrar primeras columnas para entender estructura
            if not df.empty:
                print(f"   - Primeras columnas: {list(df.columns[:5])}")
                
                # Guardar como CSV
                csv_filename = f"{output_dir}/{sheet_name.replace(' ', '_').replace('/', '_')}.csv"
                df.to_csv(csv_filename, index=False, encoding='utf-8')
                print(f"   ✅ Guardado como: {csv_filename}")
                
                # Análisis de contenido
                analysis_report.append({
                    'pestaña': sheet_name,
                    'filas': len(df),
                    'columnas': len(df.columns),
                    'columnas_list': list(df.columns),
                    'csv_file': csv_filename
                })
            else:
                print(f"   ⚠️  Pestaña vacía")
        
        # Generar reporte de análisis
        print("\n" + "="*80)
        print("📋 REPORTE DE ANÁLISIS COMPLETO")
        print("="*80)
        
        for report in analysis_report:
            print(f"\n🏷️  PESTAÑA: {report['pestaña']}")
            print(f"   📊 Dimensiones: {report['filas']} filas x {report['columnas']} columnas")
            print(f"   📁 Archivo CSV: {report['csv_file']}")
            print(f"   🔧 Columnas principales:")
            
            for i, col in enumerate(report['columnas_list'][:10]):  # Mostrar primeras 10
                print(f"      {i+1:2d}. {col}")
            
            if len(report['columnas_list']) > 10:
                print(f"      ... y {len(report['columnas_list']) - 10} columnas más")
        
        # Crear archivo resumen
        summary_file = f"{output_dir}/RESUMEN_ANALISIS.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("ANÁLISIS RESOLUCIÓN 202 DE 2021 - ANEXOS TÉCNICOS\n")
            f.write("="*60 + "\n\n")
            
            for report in analysis_report:
                f.write(f"PESTAÑA: {report['pestaña']}\n")
                f.write(f"Dimensiones: {report['filas']} filas x {report['columnas']} columnas\n")
                f.write(f"Archivo CSV: {report['csv_file']}\n")
                f.write("Columnas:\n")
                for i, col in enumerate(report['columnas_list']):
                    f.write(f"  {i+1:2d}. {col}\n")
                f.write("\n" + "-"*40 + "\n\n")
        
        print(f"\n✅ PROCESO COMPLETADO")
        print(f"📁 Archivos generados en: {output_dir}/")
        print(f"📋 Resumen guardado en: {summary_file}")
        
        return analysis_report
        
    except Exception as e:
        print(f"❌ ERROR al procesar archivo: {str(e)}")
        return None

def analyze_pedt_structure(csv_files_dir="resolucion_202_data"):
    """
    Análisis específico para identificar campos de Protección Específica y Detección Temprana
    """
    print("\n" + "="*80)
    print("🔍 ANÁLISIS ESPECÍFICO: PROTECCIÓN ESPECÍFICA Y DETECCIÓN TEMPRANA")
    print("="*80)
    
    csv_files = list(Path(csv_files_dir).glob("*.csv"))
    
    pedt_keywords = [
        'vacun', 'inmuni', 'tamiz', 'screening', 'deteccion', 'temprana',
        'proteccion', 'especifica', 'control', 'prenatal', 'parto',
        'recien_nacido', 'crecimiento', 'desarrollo', 'cronicidad'
    ]
    
    relevant_files = []
    
    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            print(f"\n📁 Analizando: {csv_file.name}")
            
            try:
                df = pd.read_csv(csv_file)
                
                # Buscar palabras clave en nombres de columnas
                relevant_columns = []
                for col in df.columns:
                    col_lower = col.lower()
                    for keyword in pedt_keywords:
                        if keyword in col_lower:
                            relevant_columns.append(col)
                            break
                
                if relevant_columns:
                    print(f"   ✅ RELEVANTE - Encontradas {len(relevant_columns)} columnas PEDT:")
                    for col in relevant_columns:
                        print(f"      - {col}")
                    
                    relevant_files.append({
                        'file': csv_file.name,
                        'relevant_columns': relevant_columns,
                        'total_columns': len(df.columns),
                        'rows': len(df)
                    })
                else:
                    print(f"   ⚪ Sin columnas PEDT obvias")
                    
            except Exception as e:
                print(f"   ❌ Error leyendo {csv_file.name}: {str(e)}")
    
    return relevant_files

if __name__ == "__main__":
    print("PROCESADOR DE RESOLUCIÓN 202 DE 2021")
    print("="*50)
    
    # Solicitar ruta del archivo Excel
    excel_path = input("📁 Ingresa la ruta completa al archivo Excel de Resolución 202: ").strip()
    
    if not os.path.exists(excel_path):
        print(f"❌ ERROR: No se encuentra el archivo {excel_path}")
        exit(1)
    
    # Procesar archivo
    analysis = process_resolucion_202_excel(excel_path)
    
    if analysis:
        # Análisis específico PEDT
        pedt_analysis = analyze_pedt_structure()
        
        print("\n" + "="*80)
        print("🎯 PRÓXIMOS PASOS RECOMENDADOS:")
        print("="*80)
        print("1. Revisar los archivos CSV generados")
        print("2. Identificar campos específicos para nuestros modelos Pydantic")
        print("3. Mapear contra nuestra estructura actual de BD")
        print("4. Implementar campos faltantes")
        print("5. Crear módulo de reportes SISPRO")