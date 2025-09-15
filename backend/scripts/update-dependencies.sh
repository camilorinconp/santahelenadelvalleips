#!/bin/bash
# Script para actualización controlada de dependencias - IPS Santa Helena del Valle
# Uso: ./scripts/update-dependencies.sh

set -e  # Salir si algún comando falla

echo "🔄 Iniciando actualización controlada de dependencias..."

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: No se encontró requirements.txt. Ejecutar desde directorio backend/"
    exit 1
fi

# Crear backup de archivos actuales
echo "📦 Creando backup de dependencias actuales..."
cp requirements.txt requirements.txt.backup.$(date +%Y%m%d_%H%M%S)
cp requirements-lock.txt requirements-lock.txt.backup.$(date +%Y%m%d_%H%M%S)

# Función para rollback en caso de error
rollback() {
    echo "🔄 Realizando rollback..."
    mv requirements.txt.backup.* requirements.txt 2>/dev/null || true
    mv requirements-lock.txt.backup.* requirements-lock.txt 2>/dev/null || true
    echo "✅ Rollback completado"
    exit 1
}

# Trap para rollback automático en caso de error
trap rollback ERR

echo "🔍 Dependencias actuales:"
pip list --format=freeze | head -10

# Actualizar pip primero
echo "⬆️  Actualizando pip..."
python -m pip install --upgrade pip

# Actualizar dependencias críticas una por una
echo "⬆️  Actualizando dependencias críticas..."

CRITICAL_DEPS=(
    "fastapi"
    "pydantic" 
    "supabase"
    "pytest"
    "uvicorn"
)

for dep in "${CRITICAL_DEPS[@]}"; do
    echo "🔄 Actualizando $dep..."
    current_version=$(pip show $dep | grep Version | cut -d: -f2 | tr -d ' ')
    echo "  Versión actual: $current_version"
    
    # Actualizar a la última versión
    pip install --upgrade $dep
    
    new_version=$(pip show $dep | grep Version | cut -d: -f2 | tr -d ' ')
    echo "  Nueva versión: $new_version"
    
    if [ "$current_version" != "$new_version" ]; then
        echo "  ✅ $dep actualizado: $current_version → $new_version"
    else
        echo "  ℹ️  $dep ya estaba actualizado"
    fi
done

# Actualizar requirements-lock.txt con todas las sub-dependencias
echo "🔄 Generando nuevo requirements-lock.txt..."
pip freeze > requirements-lock.txt

# Ejecutar tests críticos para validar compatibilidad
echo "🧪 Ejecutando tests críticos para validar compatibilidad..."
pytest tests/test_atencion_primera_infancia.py -x -q

if [ $? -ne 0 ]; then
    echo "❌ Tests críticos fallaron con nuevas versiones"
    rollback
fi

# Ejecutar tests completos (opcional, más tiempo)
read -p "¿Ejecutar suite completa de tests? (y/N): " -n 1 -r
echo
if [[ $RYAN =~ ^[Yy]$ ]]; then
    echo "🧪 Ejecutando suite completa de tests..."
    pytest -v
    
    if [ $? -ne 0 ]; then
        echo "❌ Suite completa de tests falló"
        read -p "¿Continuar de todas formas? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            rollback
        fi
    fi
fi

# Verificar que no se rompió ninguna funcionalidad crítica
echo "🔍 Verificando importaciones críticas..."
python -c "
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    from supabase import create_client
    import pytest
    print('✅ Todas las importaciones críticas funcionan correctamente')
except ImportError as e:
    print(f'❌ Error en importaciones: {e}')
    exit(1)
"

# Actualizar archivo requirements.txt con versiones exactas
echo "📝 Actualizando requirements.txt con versiones exactas..."
python -c "
import pkg_resources
import re

# Leer requirements actuales
with open('requirements.txt', 'r') as f:
    lines = f.readlines()

# Actualizar con versiones exactas
updated_lines = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        # Extraer nombre del paquete
        pkg_name = re.split('[=<>!]', line)[0].strip()
        try:
            # Obtener versión instalada
            installed_version = pkg_resources.get_distribution(pkg_name).version
            updated_lines.append(f'{pkg_name}=={installed_version}\n')
        except pkg_resources.DistributionNotFound:
            # Mantener línea original si no se encuentra
            updated_lines.append(line + '\n')
    else:
        updated_lines.append(line + '\n')

# Escribir archivo actualizado
with open('requirements.txt', 'w') as f:
    f.writelines(updated_lines)

print('✅ requirements.txt actualizado con versiones exactas')
"

# Limpiar archivos de backup antiguos (mantener solo los 5 más recientes)
echo "🧹 Limpiando backups antiguos..."
ls -1t requirements*.backup.* 2>/dev/null | tail -n +6 | xargs rm -f

echo ""
echo "🎉 ¡Actualización de dependencias completada exitosamente!"
echo ""
echo "📊 Resumen:"
echo "  - ✅ Dependencias críticas actualizadas"
echo "  - ✅ Tests críticos pasando"
echo "  - ✅ requirements.txt con versiones exactas"
echo "  - ✅ requirements-lock.txt generado"
echo ""
echo "📋 Próximos pasos recomendados:"
echo "  1. Ejecutar suite completa de tests: pytest -v"
echo "  2. Probar aplicación manualmente"  
echo "  3. Commitear cambios si todo funciona correctamente"
echo "  4. Deployar en staging para validación final"
echo ""

# Mostrar diferencias principales
echo "🔍 Principales cambios detectados:"
if [ -f "requirements.txt.backup.*" ]; then
    diff requirements.txt.backup.* requirements.txt || true
fi

echo "✅ Script completado exitosamente"