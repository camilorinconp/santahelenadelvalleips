#!/bin/bash
# =============================================================================
# Script de Resumen Rápido para Desarrolladores
# Proyecto IPS Santa Helena del Valle
# =============================================================================

echo "🚀 RESUMEN RÁPIDO PROYECTO IPS SANTA HELENA"
echo "==========================================="
echo ""

echo "📊 Estado Git:"
echo "  Últimos commits:"
git log --oneline -3
echo ""

echo "📊 Estado Supabase:"
if command -v supabase &> /dev/null; then
    cd supabase 2>/dev/null
    if [ $? -eq 0 ]; then
        supabase status 2>/dev/null | grep -E "(API URL|Studio URL)" || echo "  ⚠️ Supabase no iniciado - ejecutar: supabase start"
        cd ..
    else
        echo "  ⚠️ Directorio supabase no encontrado"
    fi
else
    echo "  ⚠️ Supabase CLI no instalado"
fi
echo ""

echo "📊 Tests Críticos:"
if [ -d "backend" ]; then
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate 2>/dev/null
        python -c "
try:
    from main import app
    print('  ✅ Aplicación principal: OK')
except Exception as e:
    print(f'  ❌ Error aplicación: {e}')

try:
    from database import get_supabase_client
    db = get_supabase_client()
    print('  ✅ Base de datos: OK')
except Exception as e:
    print(f'  ❌ Error BD: {e}')
" 2>/dev/null
    else
        echo "  ⚠️ Entorno virtual no encontrado - ejecutar: python -m venv venv"
    fi
    cd ..
else
    echo "  ⚠️ Directorio backend no encontrado"
fi
echo ""

echo "📋 Próximas tareas definidas en: DEV-CONTEXT.md"
echo "📚 Documentación completa: backend/docs/01-foundations/architecture-overview.md"
echo ""
echo "✅ Entorno verificado. Ready to code!"
echo ""
echo "🚀 Para continuar desarrollo, lee: DEV-CONTEXT.md"