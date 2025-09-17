# 🎯 CONTEXTO DE DESARROLLO ACTIVO
**📅 Última Actualización**: 17 septiembre 2025, 09:15 AM
**👤 Último Desarrollador**: Claude (Equipo Principal)
**🎯 Sprint Actual**: Vejez (60+ años) → 83% Compliance

---

## ⚡ INICIO INMEDIATO (2 minutos)

### 🏃 Comandos de Arranque
```bash
cd /Users/user/proyecto_salud
git log --oneline -3                    # Verificar último commit
cd backend && source venv/bin/activate  # Entorno Python
cd ../supabase && supabase status       # Verificar BD
cd ../backend && python -c "from main import app; print('✅ API OK')"
```

### 📊 Estado Sistema (30 segundos de lectura)
- **✅ Último Commit**: 5337393 - MILESTONE ADULTEZ COMPLETADO
- **✅ Compliance**: 67% (4/6 momentos curso de vida)
- **✅ Tests Core**: Primera Infancia 14/14, Pacientes 4/4 PASSING
- **✅ BD**: 41 migraciones aplicadas, Supabase operativo

---

## 🎯 TRABAJO ACTUAL DEFINIDO

### Objetivo Sprint: Módulo Vejez (60+ años)
**Tiempo Estimado**: 6-8 horas de desarrollo
**Resultado**: 83% compliance Resolución 3280

### 📋 Tareas Ready-to-Code (en orden)
1. **[3h] Modelo**: Crear `atencion_vejez_model.py`
   - 📖 **Referencia**: `backend/models/atencion_adultez_model.py`
   - 🎯 **ENUMs nuevos**: deterioro_cognitivo, riesgo_caidas, autonomia_funcional

2. **[2h] Rutas**: Crear `atencion_vejez.py`
   - 📖 **Referencia**: `backend/routes/atencion_adultez.py`

3. **[30min] BD**: Migración `20250917120000_create_atencion_vejez_table.sql`
   - 📖 **Referencia**: `supabase/migrations/20250917000000_create_atencion_adultez_table.sql`

4. **[30min] Integración**: Registrar en `main.py`
5. **[1h] Validación**: Tests básicos CRUD

### 🚨 Blockers Conocidos
- **Tests Adolescencia**: Fallan por sincronización → `supabase db reset` si es necesario
- **Migración Adultez**: Si tabla no existe → Aplicar migración manual

---

## 📚 DOCUMENTACIÓN CONTEXTUAL (según necesidad)

### 🔥 Para CONTINUAR desarrollo inmediato
- **📖 Este archivo** - Contexto dinámico actualizado

### 🏗️ Para ENTENDER arquitectura (si es necesario)
- **📖 `backend/docs/01-foundations/architecture-overview.md`** - Hub central navegable ⭐
- **📖 `backend/PROJECT-STATUS.md`** - Estado completo del proyecto

### 🔧 Para RESOLVER problemas técnicos (si surgen)
- **📖 `backend/CLAUDE.md`** - Contexto técnico backend
- **📖 `supabase/CLAUDE.md`** - Resolución problemas BD
- **📖 `backend/docs/04-development/testing-guide.md`** - Debug tests

### 📋 Para COMPLIANCE normativo (si es relevante)
- **📖 `backend/docs/02-regulations/resolucion-3280-master.md`** - Autoridad normativa

---

## 🔄 MANTENIMIENTO DE ESTE ARCHIVO

### ✅ Al FINALIZAR sesión de desarrollo:
1. Actualizar "Último Desarrollador" y fecha
2. Mover tareas completadas de "Ready-to-Code" a "✅ Completado"
3. Redefinir próximo "Objetivo Sprint" si es necesario
4. Commit: `git add DEV-CONTEXT.md && git commit -m "chore: Update dev context"`

### ✅ Al DETECTAR problemas:
1. Agregar a "Blockers Conocidos" con solución
2. Nunca duplicar información que ya existe en documentación técnica

---

## 🎯 PRÓXIMO MILESTONE (después de Vejez)
**Meta**: 100% Compliance Resolución 3280
1. **Materno-Perinatal**: Completar campos faltantes → 100% compliance
2. **Frontend Especializado**: Interfaces por módulo
3. **Reportería RIPS**: Integración automática ADRES

---

**🚀 FILOSOFÍA**: Este archivo es tu **cockpit de desarrollo**. Todo lo que necesitas para continuar está aquí o referenciado desde aquí.

**📖 REGLA DE ORO**: Si necesitas leer más de 2 documentos para retomar el desarrollo, este archivo necesita mejorarse.