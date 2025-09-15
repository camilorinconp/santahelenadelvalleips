#!/usr/bin/env python3
# ===================================================================
# SCRIPT: Importación Masiva Ocupaciones DANE
# ===================================================================
# Descripción: Script optimizado para importar 10,919 ocupaciones DANE
# Autor: Backend Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Propósito: Completar variables PEDT (60→119) para Resolución 202 de 2021
# ===================================================================

import asyncio
import asyncpg
import pandas as pd
import logging
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImportadorOcupacionesDane:
    """
    Importador optimizado para ocupaciones DANE con validación y procesamiento en lotes
    """
    
    def __init__(self):
        self.db_config = {
            'host': '127.0.0.1',
            'port': 54322,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'postgres'
        }
        self.lote_tamano = 1000  # Registros por lote
        self.estadisticas = {
            'total_procesados': 0,
            'exitosos': 0,
            'errores': 0,
            'tiempo_inicio': None,
            'tiempo_fin': None
        }
    
    async def conectar_database(self) -> asyncpg.Connection:
        """Establecer conexión con la database"""
        try:
            conn = await asyncpg.connect(**self.db_config)
            logger.info("✅ Conexión a database establecida exitosamente")
            return conn
        except Exception as e:
            logger.error(f"❌ Error conectando a database: {e}")
            raise
    
    def validar_archivo_csv(self, ruta_archivo: str) -> bool:
        """Validar que el archivo CSV existe y tiene la estructura esperada"""
        try:
            if not Path(ruta_archivo).exists():
                logger.error(f"❌ Archivo no encontrado: {ruta_archivo}")
                return False
            
            # Leer primeras filas para validar estructura
            df_sample = pd.read_csv(ruta_archivo, nrows=5)
            logger.info(f"📋 Estructura del archivo:")
            logger.info(f"   - Filas detectadas: {len(pd.read_csv(ruta_archivo))}")
            logger.info(f"   - Columnas: {len(df_sample.columns)}")
            logger.info(f"   - Primeras columnas: {list(df_sample.columns[:5])}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error validando archivo: {e}")
            return False
    
    def procesar_fila_ocupacion(self, fila: pd.Series) -> Dict:
        """
        Procesar una fila del CSV y convertirla al formato de nuestra tabla
        """
        try:
            # Mapeo inteligente de columnas CSV a nuestra estructura
            # NOTA: Ajustar según la estructura real del CSV DANE
            
            ocupacion = {
                'id': str(uuid.uuid4()),
                'codigo_ocupacion_dane': str(fila.get('codigo', fila.get('codigo_ocupacion', ''))).strip(),
                'nombre_ocupacion_normalizado': str(fila.get('nombre', fila.get('ocupacion', ''))).strip(),
                'categoria_ocupacional_nivel_1': str(fila.get('categoria_1', fila.get('gran_grupo', ''))).strip(),
                'categoria_ocupacional_nivel_2': str(fila.get('categoria_2', fila.get('subgrupo_principal', ''))).strip(),
                'categoria_ocupacional_nivel_3': str(fila.get('categoria_3', fila.get('subgrupo_secundario', ''))).strip(),
                'categoria_ocupacional_nivel_4': str(fila.get('categoria_4', '')).strip() or None,
                'descripcion_detallada': str(fila.get('descripcion', '')).strip() or None,
                'nivel_educativo_requerido': str(fila.get('educacion', '')).strip() or None,
                'activo': True,
                'fuente_dato': 'DANE',
                'version_catalogo': '2025',
                'creado_en': datetime.now(),
                'actualizado_en': datetime.now()
            }
            
            # Validar campos obligatorios
            if not ocupacion['codigo_ocupacion_dane']:
                raise ValueError("Código ocupación DANE vacío")
            
            if not ocupacion['nombre_ocupacion_normalizado']:
                raise ValueError("Nombre ocupación vacío")
            
            # Procesar metadatos adicionales en JSONB
            metadatos = {}
            
            # Agregar campos adicionales como metadatos
            for columna in fila.index:
                if columna not in ['codigo', 'nombre', 'ocupacion', 'categoria_1', 'categoria_2', 
                                  'categoria_3', 'categoria_4', 'descripcion', 'educacion']:
                    valor = fila[columna]
                    if pd.notna(valor) and str(valor).strip():
                        metadatos[columna] = str(valor).strip()
            
            if metadatos:
                ocupacion['metadatos_adicionales'] = json.dumps(metadatos, ensure_ascii=False)
            else:
                ocupacion['metadatos_adicionales'] = None
            
            return ocupacion
            
        except Exception as e:
            logger.warning(f"⚠️ Error procesando fila: {e}")
            return None
    
    async def insertar_lote_ocupaciones(self, conn: asyncpg.Connection, ocupaciones: List[Dict]) -> int:
        """
        Insertar un lote de ocupaciones de forma optimizada
        """
        if not ocupaciones:
            return 0
        
        try:
            # Query de inserción preparada
            insert_query = """
            INSERT INTO catalogo_ocupaciones_dane (
                id, codigo_ocupacion_dane, nombre_ocupacion_normalizado,
                categoria_ocupacional_nivel_1, categoria_ocupacional_nivel_2,
                categoria_ocupacional_nivel_3, categoria_ocupacional_nivel_4,
                descripcion_detallada, nivel_educativo_requerido,
                activo, fuente_dato, version_catalogo, metadatos_adicionales,
                creado_en, actualizado_en
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15
            ) ON CONFLICT (codigo_ocupacion_dane) DO UPDATE SET
                nombre_ocupacion_normalizado = EXCLUDED.nombre_ocupacion_normalizado,
                categoria_ocupacional_nivel_1 = EXCLUDED.categoria_ocupacional_nivel_1,
                categoria_ocupacional_nivel_2 = EXCLUDED.categoria_ocupacional_nivel_2,
                categoria_ocupacional_nivel_3 = EXCLUDED.categoria_ocupacional_nivel_3,
                categoria_ocupacional_nivel_4 = EXCLUDED.categoria_ocupacional_nivel_4,
                descripcion_detallada = EXCLUDED.descripcion_detallada,
                metadatos_adicionales = EXCLUDED.metadatos_adicionales,
                actualizado_en = NOW()
            """
            
            # Preparar datos para inserción masiva
            datos_insercion = []
            for ocupacion in ocupaciones:
                datos_insercion.append((
                    ocupacion['id'],
                    ocupacion['codigo_ocupacion_dane'],
                    ocupacion['nombre_ocupacion_normalizado'],
                    ocupacion['categoria_ocupacional_nivel_1'] or None,
                    ocupacion['categoria_ocupacional_nivel_2'] or None,
                    ocupacion['categoria_ocupacional_nivel_3'] or None,
                    ocupacion['categoria_ocupacional_nivel_4'],
                    ocupacion['descripcion_detallada'],
                    ocupacion['nivel_educativo_requerido'],
                    ocupacion['activo'],
                    ocupacion['fuente_dato'],
                    ocupacion['version_catalogo'],
                    ocupacion['metadatos_adicionales'],
                    ocupacion['creado_en'],
                    ocupacion['actualizado_en']
                ))
            
            # Ejecutar inserción en lote
            await conn.executemany(insert_query, datos_insercion)
            
            logger.info(f"✅ Lote insertado: {len(ocupaciones)} registros")
            return len(ocupaciones)
            
        except Exception as e:
            logger.error(f"❌ Error insertando lote: {e}")
            # Log detalles del primer registro para debug
            if ocupaciones:
                logger.debug(f"Primer registro del lote: {ocupaciones[0]}")
            return 0
    
    async def importar_desde_csv(self, ruta_archivo: str):
        """
        Proceso principal de importación desde CSV
        """
        logger.info("🚀 INICIANDO IMPORTACIÓN MASIVA OCUPACIONES DANE")
        logger.info("="*60)
        
        self.estadisticas['tiempo_inicio'] = time.time()
        
        # Validar archivo
        if not self.validar_archivo_csv(ruta_archivo):
            return
        
        # Conectar a database
        conn = await self.conectar_database()
        
        try:
            # Verificar tabla existe
            tabla_existe = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'catalogo_ocupaciones_dane')"
            )
            
            if not tabla_existe:
                logger.error("❌ Tabla catalogo_ocupaciones_dane no existe. Ejecutar migración primero.")
                return
            
            logger.info("📊 Iniciando procesamiento del archivo CSV...")
            
            # Leer CSV en chunks para manejo de memoria eficiente
            chunk_size = self.lote_tamano
            csv_chunks = pd.read_csv(ruta_archivo, chunksize=chunk_size)
            
            lote_numero = 1
            
            for chunk in csv_chunks:
                logger.info(f"📦 Procesando lote {lote_numero} ({len(chunk)} registros)...")
                
                # Procesar chunk
                ocupaciones_procesadas = []
                
                for index, fila in chunk.iterrows():
                    ocupacion = self.procesar_fila_ocupacion(fila)
                    if ocupacion:
                        ocupaciones_procesadas.append(ocupacion)
                        self.estadisticas['exitosos'] += 1
                    else:
                        self.estadisticas['errores'] += 1
                    
                    self.estadisticas['total_procesados'] += 1
                
                # Insertar lote
                if ocupaciones_procesadas:
                    insertados = await self.insertar_lote_ocupaciones(conn, ocupaciones_procesadas)
                    logger.info(f"   ✅ {insertados}/{len(ocupaciones_procesadas)} registros insertados")
                
                lote_numero += 1
                
                # Progress feedback cada 10 lotes
                if lote_numero % 10 == 0:
                    logger.info(f"📈 PROGRESO: {self.estadisticas['total_procesados']} registros procesados")
            
            # Verificar resultado final
            await self.verificar_importacion(conn)
            
        except Exception as e:
            logger.error(f"❌ Error durante importación: {e}")
            
        finally:
            await conn.close()
            logger.info("🔒 Conexión database cerrada")
            
        self.estadisticas['tiempo_fin'] = time.time()
        self.imprimir_resumen_final()
    
    async def verificar_importacion(self, conn: asyncpg.Connection):
        """Verificar que la importación fue exitosa"""
        try:
            # Contar registros totales
            total_registros = await conn.fetchval("SELECT COUNT(*) FROM catalogo_ocupaciones_dane")
            
            # Contar por categorías
            categorias_nivel_1 = await conn.fetchval(
                "SELECT COUNT(DISTINCT categoria_ocupacional_nivel_1) FROM catalogo_ocupaciones_dane WHERE categoria_ocupacional_nivel_1 IS NOT NULL"
            )
            
            # Verificar índices
            indices_count = await conn.fetchval(
                "SELECT COUNT(*) FROM pg_indexes WHERE tablename = 'catalogo_ocupaciones_dane'"
            )
            
            logger.info("📊 VERIFICACIÓN IMPORTACIÓN:")
            logger.info(f"   - Registros totales: {total_registros}")
            logger.info(f"   - Categorías nivel 1: {categorias_nivel_1}")
            logger.info(f"   - Índices creados: {indices_count}")
            
            # Test de búsqueda
            test_busqueda = await conn.fetchval(
                "SELECT nombre_ocupacion_normalizado FROM catalogo_ocupaciones_dane WHERE activo = true LIMIT 1"
            )
            logger.info(f"   - Test búsqueda: {test_busqueda}")
            
            if total_registros > 5000:  # Esperamos al menos 5k ocupaciones
                logger.info("✅ IMPORTACIÓN EXITOSA - Catálogo listo para uso")
                return True
            else:
                logger.warning(f"⚠️ Solo {total_registros} registros importados, esperábamos >5000")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error verificando importación: {e}")
            return False
    
    def imprimir_resumen_final(self):
        """Imprimir resumen final de la importación"""
        duracion = self.estadisticas['tiempo_fin'] - self.estadisticas['tiempo_inicio']
        
        logger.info("\n" + "="*60)
        logger.info("📋 RESUMEN FINAL IMPORTACIÓN")
        logger.info("="*60)
        logger.info(f"⏱️ Tiempo total: {duracion:.2f} segundos")
        logger.info(f"📊 Total procesados: {self.estadisticas['total_procesados']}")
        logger.info(f"✅ Exitosos: {self.estadisticas['exitosos']}")
        logger.info(f"❌ Errores: {self.estadisticas['errores']}")
        logger.info(f"⚡ Velocidad: {self.estadisticas['total_procesados']/duracion:.2f} registros/segundo")
        
        if self.estadisticas['exitosos'] > 5000:
            logger.info("🎉 ¡IMPORTACIÓN COMPLETADA EXITOSAMENTE!")
            logger.info("🚀 Variables PEDT listas para implementación (60→119)")
        else:
            logger.warning("⚠️ Importación incompleta, revisar archivo fuente")

async def main():
    """Función principal"""
    print("🏥 IMPORTADOR OCUPACIONES DANE - IPS SANTA HELENA DEL VALLE")
    print("="*65)
    
    # Buscar archivo CSV automáticamente
    posibles_rutas = [
        "docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv",
        "../docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv",
        "assets/ocupaciones_dane_sample.csv",
        "assets/ocupaciones_dane_2025.csv",
        "../assets/ocupaciones_dane.csv", 
        "../../assets/ocupaciones_dane_2025.csv",
        "ocupaciones_dane.csv"
    ]
    
    ruta_encontrada = None
    for ruta in posibles_rutas:
        if Path(ruta).exists():
            ruta_encontrada = ruta
            break
    
    if not ruta_encontrada:
        print("❌ No se encontró archivo CSV de ocupaciones DANE")
        print("📁 Rutas buscadas:")
        for ruta in posibles_rutas:
            print(f"   - {ruta}")
        print("\n💡 Coloca el archivo CSV en una de estas ubicaciones o especifica la ruta:")
        ruta_manual = input("📂 Ingresa ruta completa al archivo CSV (Enter para salir): ").strip()
        
        if not ruta_manual:
            print("👋 Importación cancelada")
            return
            
        ruta_encontrada = ruta_manual
    
    # Ejecutar importación
    importador = ImportadorOcupacionesDane()
    await importador.importar_desde_csv(ruta_encontrada)

if __name__ == "__main__":
    # Ejecutar importación
    asyncio.run(main())