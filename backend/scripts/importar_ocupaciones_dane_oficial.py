#!/usr/bin/env python3
# ===================================================================
# SCRIPT: Importación Masiva Ocupaciones DANE Oficial (Resolución 202)
# ===================================================================
# Descripción: Script adaptado para archivo oficial Resolución 202 de 2021
# Autor: Backend Team - IPS Santa Helena del Valle
# Fecha: 14 septiembre 2025
# Propósito: Completar variables PEDT (60→119) con datos oficiales DANE
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
import re

# Cargar variables de entorno
load_dotenv()

# Configuración logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImportadorOcupacionesDaneOficial:
    """
    Importador especializado para archivo oficial DANE de Resolución 202 de 2021
    """
    
    def __init__(self):
        self.db_config = {
            'host': '127.0.0.1',
            'port': 54322,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'postgres'
        }
        self.lote_tamano = 1000
        self.estadisticas = {
            'total_procesados': 0,
            'exitosos': 0,
            'errores': 0,
            'tiempo_inicio': 0,
            'tiempo_fin': 0
        }
    
    def limpiar_texto(self, texto: str) -> str:
        """
        Limpiar y normalizar texto de ocupación
        """
        if pd.isna(texto) or not texto:
            return ''
        
        # Convertir a string y limpiar
        texto_limpio = str(texto).strip()
        
        # Reemplazar caracteres especiales comunes
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ü': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'Ñ': 'N', 'Ü': 'U'
        }
        
        for original, replacement in replacements.items():
            texto_limpio = texto_limpio.replace(original, replacement)
        
        return texto_limpio
    
    def extraer_categoria_nivel_1(self, codigo: str) -> str:
        """
        Extraer categoría ocupacional nivel 1 basado en código CIUO-08
        """
        if not codigo or len(codigo) < 1:
            return 'Sin Clasificar'
        
        primer_digito = codigo[0]
        
        categorias = {
            '0': 'Ocupaciones militares',
            '1': 'Directores y gerentes',
            '2': 'Profesionales científicos e intelectuales',
            '3': 'Técnicos y profesionales de nivel medio',
            '4': 'Personal de apoyo administrativo',
            '5': 'Trabajadores de servicios y vendedores',
            '6': 'Agricultores y trabajadores calificados',
            '7': 'Artesanos y trabajadores relacionados',
            '8': 'Operadores de instalaciones y máquinas',
            '9': 'Ocupaciones elementales'
        }
        
        return categorias.get(primer_digito, 'Otras ocupaciones')
    
    def procesar_fila_ocupacion(self, fila: pd.Series) -> Optional[Dict]:
        """
        Procesar una fila del CSV oficial y convertir a formato esperado
        """
        try:
            # El archivo oficial tiene formato: Código CIUO 08 A.C.;Descripción;;;
            codigo_raw = str(fila.iloc[0]) if len(fila) > 0 else ''
            descripcion_raw = str(fila.iloc[1]) if len(fila) > 1 else ''
            
            # Limpiar y validar código
            codigo = self.limpiar_texto(codigo_raw)
            descripcion = self.limpiar_texto(descripcion_raw)
            
            # Corregir código si viene como flotante (ej: 110.0 → 0110)
            if codigo and codigo != 'nan':
                try:
                    # Si es número flotante, convertir a entero y formatear con ceros
                    codigo_num = int(float(codigo))
                    codigo = f"{codigo_num:04d}"  # Formatear con 4 dígitos con ceros a la izquierda
                except (ValueError, TypeError):
                    pass  # Mantener código original si no es numérico
            
            # Debug: log primeras filas para entender formato
            if self.estadisticas['total_procesados'] < 5:
                logger.info(f"DEBUG fila {self.estadisticas['total_procesados']}: codigo='{codigo}', descripcion='{descripcion}'")
            
            # Saltar filas de header o vacías
            if not codigo or not descripcion or codigo in ['Código CIUO 08 A.C.', 'C�digo CIUO 08 A.C.', 'nan']:
                return None
            
            # Validar código CIUO (4 dígitos)
            if not re.match(r'^\d{4}$', codigo):
                logger.debug(f"Código no válido: {codigo}")
                return None
            
            # Construir ocupación
            ocupacion = {
                'id': str(uuid.uuid4()),
                'codigo_ocupacion_dane': codigo,
                'nombre_ocupacion_normalizado': descripcion[:200],  # Truncar si es muy largo
                'categoria_ocupacional_nivel_1': self.extraer_categoria_nivel_1(codigo),
                'categoria_ocupacional_nivel_2': None,
                'categoria_ocupacional_nivel_3': None,
                'categoria_ocupacional_nivel_4': codigo[:2],  # Submajor group
                'descripcion_detallada': descripcion if len(descripcion) <= 500 else descripcion[:497] + '...',
                'nivel_educativo_requerido': None,
                'activo': True,
                'fuente_dato': 'Resolución 202 de 2021 - DANE CIUO-08',
                'version_catalogo': '2021',
                'metadatos_adicionales': json.dumps({
                    'ciuo_08': codigo,
                    'fuente': 'Lineamientos técnicos Resolución 202 de 2021',
                    'fecha_actualizacion': 'Abril 2017',
                    'version': '10'
                }),
                'creado_en': datetime.now(),
                'actualizado_en': datetime.now()
            }
            
            return ocupacion
            
        except Exception as e:
            logger.debug(f"Error procesando fila: {e}")
            return None
    
    async def conectar_database(self) -> asyncpg.Connection:
        """
        Conectar a la base de datos PostgreSQL
        """
        try:
            conn = await asyncpg.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            logger.info("✅ Conexión a database establecida exitosamente")
            return conn
        except Exception as e:
            logger.error(f"❌ Error conectando a database: {e}")
            raise
    
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
                    ocupacion['categoria_ocupacional_nivel_1'],
                    ocupacion['categoria_ocupacional_nivel_2'],
                    ocupacion['categoria_ocupacional_nivel_3'],
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
            if ocupaciones:
                logger.debug(f"Primer registro del lote: {ocupaciones[0]}")
            return 0
    
    async def importar_desde_csv(self, ruta_archivo: str):
        """
        Proceso principal de importación desde CSV oficial
        """
        logger.info("🚀 INICIANDO IMPORTACIÓN MASIVA OCUPACIONES DANE OFICIAL")
        logger.info("="*70)
        
        self.estadisticas['tiempo_inicio'] = time.time()
        
        # Verificar archivo existe
        if not Path(ruta_archivo).exists():
            logger.error(f"❌ Archivo no encontrado: {ruta_archivo}")
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
            
            logger.info(f"📊 Leyendo archivo: {ruta_archivo}")
            
            # Probar diferentes codificaciones
            encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']
            df = None
            
            for encoding in encodings:
                try:
                    logger.info(f"🔧 Probando codificación: {encoding}")
                    df = pd.read_csv(
                        ruta_archivo,
                        sep=';',  # Separador del archivo oficial
                        encoding=encoding,
                        header=None,  # No usar headers automáticos
                        skiprows=6,  # Saltar hasta la línea de datos
                        na_values=['', ' ', 'nan', 'NaN'],
                        on_bad_lines='skip'  # Saltar líneas problemáticas
                    )
                    logger.info(f"✅ Codificación exitosa: {encoding}")
                    break
                except UnicodeDecodeError:
                    logger.debug(f"❌ Codificación {encoding} falló")
                    continue
            
            if df is None:
                logger.error("❌ No se pudo leer el archivo con ninguna codificación")
                return
            
            logger.info(f"📋 Estructura del archivo:")
            logger.info(f"   - Filas detectadas: {len(df)}")
            logger.info(f"   - Columnas: {len(df.columns)}")
            
            # Procesar en lotes
            lote_numero = 1
            total_filas = len(df)
            
            for inicio in range(0, total_filas, self.lote_tamano):
                fin = min(inicio + self.lote_tamano, total_filas)
                chunk = df.iloc[inicio:fin]
                
                logger.info(f"📦 Procesando lote {lote_numero} (filas {inicio+1}-{fin})...")
                
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
                    progreso = (inicio / total_filas) * 100
                    logger.info(f"📈 PROGRESO: {progreso:.1f}% - {self.estadisticas['exitosos']} ocupaciones procesadas")
            
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
            
            # Verificar algunos códigos específicos
            test_busqueda = await conn.fetchval(
                "SELECT nombre_ocupacion_normalizado FROM catalogo_ocupaciones_dane WHERE activo = true LIMIT 1"
            )
            
            logger.info(f"📊 VERIFICACIÓN IMPORTACIÓN:")
            logger.info(f"   - Registros totales: {total_registros}")
            logger.info(f"   - Categorías nivel 1: {categorias_nivel_1}")
            logger.info(f"   - Test búsqueda: {test_busqueda}")
            
            if total_registros > 5000:  # Esperamos al menos 5k ocupaciones
                logger.info("✅ IMPORTACIÓN EXITOSA - Catálogo DANE oficial listo")
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
        
        logger.info("\n" + "="*70)
        logger.info("📋 RESUMEN FINAL IMPORTACIÓN OCUPACIONES DANE OFICIAL")
        logger.info("="*70)
        logger.info(f"⏱️ Tiempo total: {duracion:.2f} segundos")
        logger.info(f"📊 Total procesados: {self.estadisticas['total_procesados']}")
        logger.info(f"✅ Exitosos: {self.estadisticas['exitosos']}")
        logger.info(f"❌ Errores: {self.estadisticas['errores']}")
        logger.info(f"⚡ Velocidad: {self.estadisticas['total_procesados']/duracion:.2f} registros/segundo")
        
        if self.estadisticas['exitosos'] > 5000:
            logger.info("🎉 ¡IMPORTACIÓN COMPLETADA EXITOSAMENTE!")
            logger.info("🚀 Variables PEDT listas: Base sólida para 119/119 variables")
            logger.info("📊 Catálogo oficial DANE disponible para autocompletado")
        else:
            logger.warning("⚠️ Importación incompleta, revisar formato archivo")

async def main():
    """Función principal"""
    print("🏥 IMPORTADOR OCUPACIONES DANE OFICIAL - IPS SANTA HELENA DEL VALLE")
    print("="*75)
    
    # Archivo oficial de Resolución 202
    archivo_oficial = "docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv"
    
    if not Path(archivo_oficial).exists():
        logger.error(f"❌ Archivo oficial no encontrado: {archivo_oficial}")
        logger.info("📍 Ubicación esperada: docs/02-regulations/resolucion-202-data/Tabla ocupaciones.csv")
        return
    
    importador = ImportadorOcupacionesDaneOficial()
    await importador.importar_desde_csv(archivo_oficial)

if __name__ == "__main__":
    asyncio.run(main())