# 🔄 Flujo de Trabajo de Desarrollo - Proyecto IPS Santa Helena del Valle

**Versión**: v1.0  
**Última actualización**: 12 de septiembre, 2025  
**Audiencia**: Todo el equipo de desarrollo

## 📋 Tabla de Contenido

1. [Flujo Principal de Desarrollo](#flujo-principal-de-desarrollo)
2. [Convenciones de Git](#convenciones-de-git)
3. [Gestión de Ramas](#gestión-de-ramas)
4. [Testing y Calidad](#testing-y-calidad)
5. [Base de Datos y Migraciones](#base-de-datos-y-migraciones)
6. [Code Review](#code-review)
7. [Deployment](#deployment)
8. [Comandos Útiles](#comandos-útiles)

---

## 🚀 Flujo Principal de Desarrollo

### **Paso 1: Preparación del Entorno**
```bash
# 1. Sincronizar con main
git checkout main
git pull origin main

# 2. Crear rama de feature
git checkout -b feature/nombre-descriptivo-funcionalidad

# 3. Verificar entorno limpio
cd backend && pytest -v  # Todas las pruebas deben pasar
cd ../frontend && npm test -- --watchAll=false --passWithNoTests
```

### **Paso 2: Desarrollo Incremental**
```bash
# Regla de Oro: Commits frecuentes y pequeños
# Cada commit debe representar una unidad lógica completa

# Ejemplo de desarrollo típico:
git add models/nueva_funcionalidad_model.py
git commit -m "feat(models): agregar modelo DetallePuerperio según Resolución 3280"

git add routes/nueva_funcionalidad.py  
git commit -m "feat(api): implementar endpoints CRUD para DetallePuerperio"

git add tests/test_nueva_funcionalidad.py
git commit -m "test(puerperio): agregar 12 tests unitarios y de integración"
```

### **Paso 3: Validación Continua**
```bash
# Antes de cada commit importante
./scripts/pre-commit-check.sh  # (si existe)

# O manualmente:
cd backend
pytest -v --cov=. --cov-report=term-missing
ruff check .  # Linting
ruff format .  # Formatting

cd ../frontend  
npm run lint
npm test -- --watchAll=false --coverage
```

### **Paso 4: Sincronización de Base de Datos**
```bash
# Si hay cambios en esquema de DB
supabase db diff -f add_detalle_puerperio_complete

# Validar migración localmente
supabase db reset
pytest -v  # Confirmar que todo sigue funcionando

# Commit de migración junto con código
git add supabase/migrations/[timestamp]_add_detalle_puerperio_complete.sql
git add backend/models/detalle_puerperio_model.py
git commit -m "feat(db): implementar tabla detalle_puerperio con 23 campos Resolución 3280

- Agregar tabla detalle_puerperio con ENUMs específicos
- Implementar modelo Pydantic con validaciones
- Incluir RLS policies para seguridad
- 15 tests de cobertura completa

Refs: RIAMP-Hito-1.4"
```

### **Paso 5: Pull Request**
```bash
# Push de la rama
git push origin feature/nombre-descriptivo-funcionalidad

# Crear PR con template estándar (ver templates/)
# Solicitar code review
# Esperar aprobación antes de merge
```

---

## 📝 Convenciones de Git

### **Formato de Mensajes de Commit (Conventional Commits)**
```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[pie opcional]
```

#### **Tipos Permitidos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan el código)
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Cambios en herramientas, configuración, dependencias

#### **Alcances Típicos**:
- `riamp`: Funcionalidades de Ruta Materno Perinatal
- `rpms`: Funcionalidades de Ruta Promoción y Mantenimiento
- `models`: Modelos de datos Pydantic
- `api`: Endpoints y rutas de la API
- `db`: Base de datos y migraciones  
- `frontend`: Componentes y páginas React
- `tests`: Suite de pruebas

#### **Ejemplos de Commits Bien Formados**:
```bash
# Funcionalidad nueva
git commit -m "feat(riamp): implementar control prenatal completo según Resolución 3280

- Agregar 47 campos requeridos por normativa
- Implementar Escala Herrera-Hurtado para riesgo biopsicosocial
- Validaciones automáticas por semana gestacional
- Incluir 25 tests unitarios con 98% cobertura

Closes #123"

# Corrección de bug
git commit -m "fix(db): corregir RLS policy para tabla pacientes

La política anterior bloqueaba consultas legítimas en desarrollo.
Ajustar condición para permitir acceso anónimo en local.

Refs: #145"

# Documentación
git commit -m "docs(architecture): actualizar guía con patrón polimórfico

- Documenta estrategia de polimorfismo anidado
- Agrega ejemplos de uso para nuevas RIAS
- Incluye ADRs de decisiones arquitectónicas"
```

### **Reglas de Mensajes de Commit**:
1. **Primera línea**: Máximo 72 caracteres
2. **Línea vacía**: Entre título y cuerpo
3. **Cuerpo**: Explicar QUÉ y POR QUÉ (no cómo)
4. **Referencias**: Incluir números de issues relevantes
5. **Breaking changes**: Indicar en el pie con `BREAKING CHANGE:`

---

## 🌿 Gestión de Ramas

### **Estrategia de Branching (GitHub Flow Adaptado)**

```
main ← rama principal, siempre deployable
├── feature/riamp-control-prenatal-complete
├── feature/rpms-primera-infancia-base  
├── hotfix/fix-rls-policies-production
└── docs/update-architecture-guide
```

#### **Tipos de Ramas**:

**`main`** - Rama principal
- Siempre en estado deployable
- Solo se actualiza vía Pull Requests aprobados
- Protegida contra push directo
- Todos los tests deben pasar

**`feature/nombre-descriptivo`** - Nuevas funcionalidades
- Una rama por funcionalidad completa
- Nomenclatura descriptiva en kebab-case
- Se deriva de `main`, se fusiona a `main`
- Vida útil: 1-3 semanas máximo

**`hotfix/descripcion-breve`** - Correcciones urgentes  
- Para bugs críticos en producción
- Se deriva de `main`, se fusiona a `main`
- Deploy inmediato después de merge

**`docs/tema-documentacion`** - Solo documentación
- Cambios que no afectan código
- Review expedito, merge directo permitido

#### **Reglas de Ramas**:
1. **Una funcionalidad = Una rama**
2. **Sincronizar frecuentemente** con main
3. **Eliminar ramas** después del merge
4. **No commits directos** a main
5. **Tests pasando** antes de abrir PR

### **Resolución de Conflictos**
```bash
# Sincronizar antes de resolver conflictos
git checkout main
git pull origin main
git checkout feature/mi-funcionalidad
git rebase main  # Preferir rebase sobre merge

# Si hay conflictos:
git status  # Ver archivos en conflicto
# Resolver manualmente cada conflicto
git add .
git rebase --continue

# Validar que todo funciona después del rebase
pytest -v
npm test -- --watchAll=false
```

---

## 🧪 Testing y Calidad

### **Pirámide de Testing Objetivo**
```
     /\      5% E2E Tests (Cypress/Playwright)
    /  \     
   /____\    20% Integration Tests (FastAPI TestClient)  
  /______\   
 /________\  75% Unit Tests (Pytest + React Testing Library)
```

### **Cobertura Mínima por Componente**:
- **Modelos críticos** (pacientes, atenciones): 95%+
- **Endpoints API**: 90%+  
- **Componentes React**: 85%+
- **Utilidades**: 90%+
- **Total del proyecto**: 88%+

### **Comandos de Testing Estándar**:
```bash
# Backend - Tests completos
cd backend
pytest -v --cov=. --cov-report=html --cov-fail-under=88

# Backend - Solo tests rápidos  
pytest -v -m "not integration"

# Backend - Tests específicos
pytest tests/test_atencion_materno_perinatal.py -v

# Frontend - Tests completos
cd frontend  
npm test -- --coverage --watchAll=false

# Frontend - Tests en watch mode
npm test

# Frontend - Tests específicos
npm test -- --testNamePattern="Pacientes"
```

### **Quality Gates - Checklist Pre-Commit**:
```bash
#!/bin/bash
# scripts/pre-commit-check.sh

echo "🔍 Running quality checks..."

# Backend checks
cd backend
echo "Running backend linting..."
ruff check . || exit 1

echo "Running backend formatting..."  
ruff format --check . || exit 1

echo "Running backend tests..."
pytest -v --cov=. --cov-fail-under=88 || exit 1

# Frontend checks  
cd ../frontend
echo "Running frontend linting..."
npm run lint || exit 1

echo "Running frontend tests..."
npm test -- --watchAll=false --coverage || exit 1

# Database checks
cd ../
echo "Checking database migrations..."
supabase db diff --check || echo "⚠️ Uncommitted database changes detected"

echo "✅ All quality checks passed!"
```

---

## 🗄️ Base de Datos y Migraciones

### **Convenciones para Migraciones**:
```bash
# Formato de nombre
YYYYMMDD_HHMMSS_descripcion_clara.sql

# Ejemplos:
20241215_143000_add_riamp_control_prenatal_complete_fields.sql
20241216_091500_create_rpms_primera_infancia_tables.sql
20241216_154500_refactor_atencion_polymorphic_structure.sql
```

### **Flujo Estándar de Migraciones**:
```bash
# 1. Desarrollar cambios en Supabase Studio local
# http://127.0.0.1:54323

# 2. Generar migración  
supabase db diff -f descripcion_clara_del_cambio

# 3. Revisar archivo generado
cat supabase/migrations/[timestamp]_descripcion_clara_del_cambio.sql

# 4. Probar migración en limpio
supabase db reset
pytest -v  # Validar que modelos siguen funcionando

# 5. Si hay errores, ajustar y repetir
# 6. Commit junto con cambios de código relacionados
```

### **Reglas de Migraciones**:
1. **Siempre reversibles**: Incluir `DROP` statements cuando sea posible
2. **Una responsabilidad**: Cada migración un solo cambio lógico
3. **Comentarios descriptivos**: Explicar el propósito del cambio
4. **Datos existentes**: Considerar impacto en data existente
5. **RLS policies**: Actualizar políticas de seguridad si es necesario

### **Template de Migración**:
```sql
-- Descripción: Agregar campos completos para control prenatal según Resolución 3280
-- Fecha: 2024-12-15
-- Responsable: Equipo Principal
-- Issue: #123 - Implementar RIAMP Hito 1.1

-- =============================================================================
-- FORWARD MIGRATION
-- =============================================================================

-- 1. Agregar nuevos campos
ALTER TABLE detalle_control_prenatal 
ADD COLUMN riesgo_biopsicosocial riesgo_biopsicosocial_enum,
ADD COLUMN signos_vitales_maternos JSONB DEFAULT '{}'::jsonb,
ADD COLUMN resultados_paraclinicos JSONB DEFAULT '{}'::jsonb;

-- 2. Crear índices para performance
CREATE INDEX idx_control_prenatal_riesgo 
ON detalle_control_prenatal(riesgo_biopsicosocial);

-- 3. Actualizar RLS policies si es necesario  
-- (policies específicas aquí)

-- 4. Comentarios en tablas
COMMENT ON COLUMN detalle_control_prenatal.riesgo_biopsicosocial 
IS 'Riesgo según Escala Herrera-Hurtado - Resolución 3280 Art. 4.3.1';

-- =============================================================================  
-- ROLLBACK INSTRUCTIONS (manual)
-- =============================================================================
-- ALTER TABLE detalle_control_prenatal 
-- DROP COLUMN IF EXISTS riesgo_biopsicosocial,
-- DROP COLUMN IF EXISTS signos_vitales_maternos,
-- DROP COLUMN IF EXISTS resultados_paraclinicos;
-- DROP INDEX IF EXISTS idx_control_prenatal_riesgo;
```

---

## 👥 Code Review

### **Checklist del Reviewee (Antes de abrir PR)**:
- [ ] ✅ Todos los tests pasan localmente
- [ ] ✅ Cobertura de tests >= 88%
- [ ] ✅ Linting y formatting aplicados  
- [ ] ✅ Migraciones probadas desde cero
- [ ] ✅ Documentación actualizada si es necesario
- [ ] ✅ Mensaje de commit sigue convenciones
- [ ] ✅ PR incluye descripción clara del cambio

### **Template de Pull Request**:
```markdown
## 📋 Descripción
Breve descripción de los cambios implementados y por qué son necesarios.

## 🎯 Tipo de Cambio
- [ ] 🐛 Bug fix (cambio que corrige un issue)
- [ ] ✨ Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] 💥 Breaking change (funcionalidad que causa incompatibilidad)
- [ ] 📝 Solo documentación

## 🔍 Checklist de Resolución 3280
- [ ] Campos obligatorios según normativa implementados
- [ ] Validaciones específicas incluidas
- [ ] Tests de compliance agregados
- [ ] Documentación técnica actualizada

## 🧪 Testing
- [ ] Tests unitarios: cobertura >= 90%
- [ ] Tests de integración incluidos
- [ ] Tests manuales completados
- [ ] Performance validado (< 200ms endpoints críticos)

## 🗄️ Cambios en Base de Datos  
- [ ] Migración creada y validada
- [ ] Schema sincronizado correctamente
- [ ] RLS policies actualizadas
- [ ] Índices agregados si es necesario

## 📸 Screenshots (si aplica)
[Capturas de pantalla de la interfaz si hay cambios visuales]

## 📚 Documentación Relacionada
- Issue: #123
- Resolución 3280: Sección X.Y.Z  
- Arquitectura: [link a docs/01-ARCHITECTURE-GUIDE.md]

## 🔗 Referencias
- [Link a issue principal]
- [Links a documentación relevante]
```

### **Checklist del Reviewer**:
#### **Funcionalidad**:
- [ ] El código hace lo que dice que hace
- [ ] Maneja correctamente casos edge y errores
- [ ] Performance acceptable (< 200ms para endpoints)
- [ ] No introduce vulnerabilidades de seguridad

#### **Calidad del Código**:
- [ ] Código legible y autodocumentado
- [ ] Sigue patrones establecidos en el proyecto
- [ ] No código duplicado injustificado
- [ ] Nombres de variables/funciones descriptivos

#### **Testing**:
- [ ] Tests cubren casos principales y edge cases
- [ ] Tests son determinísticos y estables
- [ ] Cobertura adecuada para cambios realizados

#### **Compliance**:
- [ ] Cumple con requerimientos Resolución 3280
- [ ] Campos obligatorios implementados correctamente
- [ ] Validaciones según normativa incluidas

---

## 🚀 Deployment

### **Flujo de Deployment Estándar**:
```bash
# 1. Merge a main (vía PR aprobado)
git checkout main
git pull origin main

# 2. Deploy de migraciones de DB
supabase db push  # Solo si hay nuevas migraciones

# 3. Validar que producción está funcionando
# - Ejecutar smoke tests
# - Verificar endpoints críticos
# - Validar dashboard si aplica

# 4. Tag de versión (para releases importantes)
git tag -a v0.5.0-riamp-prenatal-complete -m "Release: Control prenatal completo según Resolución 3280"
git push origin v0.5.0-riamp-prenatal-complete
```

### **Ambientes**:
- **Local**: Desarrollo diario con Supabase local
- **Staging**: Supabase cloud branch para testing
- **Production**: Supabase cloud main para usuarios finales

### **Rollback Plan**:
```bash
# En caso de issues críticos en producción
# 1. Rollback de base de datos (manual, usar backups)
# 2. Revert del commit problemático
git revert [commit-hash]
git push origin main

# 3. Deploy inmediato del revert
# 4. Investigar issue en rama separada
```

---

## ⚡ Comandos Útiles

### **Setup Inicial (Nueva Instalación)**:
```bash
# Clonar y setup completo
git clone [repo-url]
cd proyecto_salud

# Backend setup  
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Database setup
supabase start
supabase db reset  # Aplicar todas las migraciones
```

### **Desarrollo Diario**:
```bash
# Iniciar todos los servicios
# Terminal 1: Database
supabase start

# Terminal 2: Backend  
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 3: Frontend
cd frontend && npm start

# Terminal 4: Tests en watch mode (opcional)
cd backend && pytest -v --cov=. -f
```

### **Troubleshooting Común**:
```bash
# Problema: Tests fallando por DB desincronizada
supabase stop
supabase start
supabase db reset
pytest -v

# Problema: Conflictos en package-lock.json
cd frontend
rm -rf node_modules package-lock.json
npm install

# Problema: Cache de schema Supabase
supabase stop && supabase start
# O en producción: Pause/Resume proyecto en dashboard

# Problema: Migraciones locales vs remoto
supabase db pull  # Traer esquema remoto
supabase db diff  # Ver diferencias
```

### **Scripts de Automatización (Futuros)**:
```bash
# scripts/dev-setup.sh - Setup completo para nuevo desarrollador
# scripts/pre-commit-check.sh - Validaciones pre-commit
# scripts/run-all-tests.sh - Tests completos del proyecto
# scripts/backup-local-db.sh - Backup de base de datos local
# scripts/sync-with-production.sh - Sincronización con producción
```

---

## 🎯 Métricas de Desarrollo

### **Objetivos por Sprint** (2 semanas):
- **Velocity**: 20-30 story points
- **Bugs introducidos**: < 2 por sprint
- **Cobertura de tests**: Mantener >= 88%
- **Code review time**: < 24 horas
- **Time to production**: < 48 horas post-merge

### **Métricas de Calidad**:
- **Mean Time to Recovery**: < 30 minutos
- **Failed deployments**: < 5%
- **Test suite runtime**: < 5 minutos
- **Build time**: < 10 minutos

---

**Última revisión**: 2025-09-12  
**Próxima revisión**: Al completar Hito 1.1 (Control Prenatal Completo)  
**Responsable**: Tech Lead / Equipo Principal de Desarrollo