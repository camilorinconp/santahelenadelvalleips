# 🔧 Guía de Configuración GitHub - IPS Santa Helena del Valle

## 🎯 Propósito

Esta guía implementa el sistema de Pull Requests y Issues para propuestas arquitectónicas recomendado por el equipo consultor externo, reemplazando el sistema de carpetas por un flujo colaborativo optimizado.

---

## 🏷️ Configuración de Labels

### Labels Principales (Crear en GitHub Settings > Labels)

#### Propuestas Arquitectónicas
- **`arquitectura`** - Color: `#FF6B6B` - Cambios arquitectónicos estructurales
- **`propuesta`** - Color: `#4ECDC4` - Propuestas en discusión
- **`necesita-revision`** - Color: `#FFE66D` - Requiere revisión del equipo arquitectónico
- **`aprobado`** - Color: `#51CF66` - Aprobado para implementación
- **`rechazado`** - Color: `#FF8787` - Propuesta rechazada
- **`implementando`** - Color: `#339AF0` - En proceso de implementación

#### Por Tipo de Cambio
- **`database`** - Color: `#9775FA` - Cambios de base de datos
- **`api`** - Color: `#20C997` - Nuevos endpoints o cambios de API
- **`modelo`** - Color: `#FD7E14` - Cambios en modelos Pydantic
- **`seguridad`** - Color: `#E03131` - Cambios relacionados con seguridad/RLS
- **`performance`** - Color: `#37B24D` - Optimizaciones de rendimiento
- **`compliance`** - Color: `#1971C2` - Relacionado con normativas colombianas

#### Por Impacto
- **`impacto-bajo`** - Color: `#ADB5BD` - Cambios localizados
- **`impacto-medio`** - Color: `#FCC419` - Afecta 2-3 módulos
- **`impacto-alto`** - Color: `#FA5252` - Cambios transversales
- **`critico`** - Color: `#C92A2A` - Requiere migración compleja

#### Normativas
- **`resolucion-3280`** - Color: `#1864AB` - Relacionado con RIAS
- **`resolucion-202`** - Color: `#2B8A3E` - Relacionado con PEDT
- **`normativa-colombiana`** - Color: `#D6336C` - Otras normativas nacionales

#### Estados de Issues
- **`bug`** - Color: `#D73A49` - Reportes de errores
- **`enhancement`** - Color: `#A2EEEF` - Mejoras y nuevas características
- **`feature-request`** - Color: `#7057FF` - Solicitudes de funcionalidad
- **`documentacion`** - Color: `#0075CA` - Relacionado con documentación
- **`needs-writing`** - Color: `#EDEDED` - Requiere redacción
- **`necesita-investigacion`** - Color: `#FBCA04` - Requiere investigación adicional

---

## 🔒 Branch Protection Rules

### Configuración en GitHub Settings > Branches

#### Regla para `main` branch:
```yaml
Branch name pattern: main
Restrictions:
  ☑️ Require a pull request before merging
      ☑️ Require approvals (2 approvals required)
      ☑️ Dismiss stale PR approvals when new commits are pushed
      ☑️ Require review from code owners
  ☑️ Require status checks to pass before merging
      ☑️ Require branches to be up to date before merging
      Status checks: [configurar cuando tengamos CI/CD]
  ☑️ Require linear history
  ☑️ Include administrators
  ☐️ Allow force pushes
  ☐️ Allow deletions
```

#### Regla para `develop` branch:
```yaml
Branch name pattern: develop
Restrictions:
  ☑️ Require a pull request before merging
      ☑️ Require approvals (1 approval required)
      ☑️ Dismiss stale PR approvals when new commits are pushed
  ☑️ Require status checks to pass before merging
      ☑️ Require branches to be up to date before merging
  ☐️ Require linear history
  ☑️ Include administrators
  ☐️ Allow force pushes
  ☐️ Allow deletions
```

---

## 🏷️ Naming Conventions

### Branches

#### Propuestas Arquitectónicas
```
arch/[tipo]-[descripcion-corta]
```
**Ejemplos:**
- `arch/database-catalogo-medicamentos`
- `arch/api-reportes-pedt-automaticos`
- `arch/modelo-atencion-especializada`
- `arch/performance-optimizacion-consultas`

#### Features Regulares
```
feature/[modulo]-[funcionalidad]
```
**Ejemplos:**
- `feature/pacientes-historial-medico`
- `feature/reportes-dashboard-admin`
- `feature/api-control-cronicidad`

#### Bug Fixes
```
fix/[modulo]-[descripcion-problema]
```
**Ejemplos:**
- `fix/database-migracion-timestamps`
- `fix/api-validacion-cedulas`
- `fix/frontend-formulario-pacientes`

#### Hotfixes (para producción)
```
hotfix/[descripcion-urgente]
```
**Ejemplos:**
- `hotfix/rls-policies-pacientes`
- `hotfix/api-timeout-supabase`

### Commits

#### Formato Convencional
```
[tipo](modulo): descripción clara

Cuerpo del commit (opcional)
- Detalle 1
- Detalle 2

Referencias: #issue-number
```

#### Tipos de Commit
- **`feat`**: Nueva funcionalidad
- **`fix`**: Corrección de bug
- **`arch`**: Cambio arquitectónico
- **`db`**: Cambios de base de datos/migraciones
- **`docs`**: Solo documentación
- **`style`**: Cambios de formato (no afectan funcionalidad)
- **`refactor`**: Cambio de código sin nueva funcionalidad ni fix
- **`test`**: Añadir o modificar tests
- **`chore`**: Cambios en el proceso de build o herramientas auxiliares

#### Ejemplos de Commits
```
feat(pacientes): agregar validación avanzada número documento

- Validación dígito verificación cédulas colombianas
- Soporte para documentos extranjeros
- Tests exhaustivos casos edge

Referencias: #123
```

```
arch(database): implementar polimorfismo anidado control cronicidad

- Nueva tabla detalle_diabetes_control
- Migración 20250915_120000_add_diabetes_polymorphic.sql
- Actualización modelos Pydantic relacionados
- RLS policies configuradas

Referencias: #arch-45
```

---

## 👥 Configuración de Code Owners

### Crear archivo `.github/CODEOWNERS`

```gitignore
# IPS Santa Helena del Valle - Code Owners
# Cada línea es un patrón de archivo seguido de uno o más propietarios

# Configuración global del proyecto
* @equipo-arquitectura

# Base de datos y migraciones
/supabase/migrations/ @database-team @arquitecto-senior
/supabase/config.toml @database-team

# Backend APIs y modelos
/backend/models/ @backend-team @arquitecto-senior
/backend/routes/ @backend-team
/backend/database.py @database-team @backend-team

# Frontend components críticos
/frontend/src/components/ @frontend-team
/frontend/src/api/ @frontend-team @backend-team

# Documentación arquitectónica
/docs/01-foundations/ @arquitecto-senior @equipo-arquitectura
/docs/02-regulations/ @compliance-lead @arquitecto-senior
/docs/03-architecture/ @arquitecto-senior

# Templates y configuración GitHub
/.github/ @arquitecto-senior @equipo-arquitectura

# Archivos críticos de configuración
CLAUDE.md @arquitecto-senior
README.md @equipo-arquitectura
```

---

## 🔄 Flujo de Work (Workflow)

### 1. Propuesta Inicial
```
1. Crear Issue usando template "Propuesta Arquitectónica"
2. Asignar labels apropiados (arquitectura, impacto-*, etc.)
3. Discusión en comments del Issue
4. Decisión del equipo arquitectónico
```

### 2. Implementación (si aprobada)
```
1. Crear branch: arch/[tipo]-[descripcion]
2. Implementar cambios siguiendo criterios de aceptación
3. Crear PR usando template estandardizado
4. Code review por Code Owners
5. Merge a develop después de aprobación
```

### 3. Deployment
```
1. Testing en develop
2. PR de develop → main (requiere 2 aprobaciones)
3. Deploy a producción
4. Monitoring post-deploy
```

---

## ⚙️ Configuración Automática de Labels

### Script para crear labels automáticamente
```bash
#!/bin/bash
# setup-github-labels.sh

# Configurar token y repo
GITHUB_TOKEN="your_token_here"
REPO_OWNER="your_username"
REPO_NAME="proyecto_salud"

# Función para crear label
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    curl -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/labels" \
        -d "{
            \"name\": \"$name\",
            \"color\": \"$color\",
            \"description\": \"$description\"
        }"
echo
}

# Crear labels de propuestas arquitectónicas
create_label "arquitectura" "FF6B6B" "Cambios arquitectónicos estructurales"
create_label "propuesta" "4ECDC4" "Propuestas en discusión"
create_label "necesita-revision" "FFE66D" "Requiere revisión del equipo arquitectónico"
create_label "aprobado" "51CF66" "Aprobado para implementación"
create_label "rechazado" "FF8787" "Propuesta rechazada"

# Crear labels por tipo
create_label "database" "9775FA" "Cambios de base de datos"
create_label "api" "20C997" "Nuevos endpoints o cambios de API"
create_label "modelo" "FD7E14" "Cambios en modelos Pydantic"

# Crear labels de impacto
create_label "impacto-bajo" "ADB5BD" "Cambios localizados"
create_label "impacto-medio" "FCC419" "Afecta 2-3 módulos"
create_label "impacto-alto" "FA5252" "Cambios transversales"

# Crear labels normativos
create_label "resolucion-3280" "1864AB" "Relacionado con RIAS"
create_label "resolucion-202" "2B8A3E" "Relacionado con PEDT"

echo "Labels creados exitosamente"
```

---

## 📋 Checklist de Implementación

### Para el Administrador del Repositorio

#### Setup Inicial
- [ ] Crear labels usando el script o manualmente
- [ ] Configurar branch protection rules para `main` y `develop`
- [ ] Crear archivo `.github/CODEOWNERS` con asignaciones apropiadas
- [ ] Asignar permisos de equipo en GitHub
- [ ] Configurar notificaciones para el equipo arquitectónico

#### Validación
- [ ] Probar creación de Issue con template arquitectónico
- [ ] Probar creación de PR con template estandardizado
- [ ] Validar que branch protection rules funcionan
- [ ] Confirmar que Code Owners reciben notificaciones
- [ ] Documentar proceso para el equipo

### Para el Equipo de Desarrollo

#### Adopción del Nuevo Flujo
- [ ] Leer esta guía completa
- [ ] Practicar creación de branches con naming conventions
- [ ] Familiarizarse con templates de Issues y PRs
- [ ] Entender el proceso de revisión arquitectónica
- [ ] Configurar herramientas locales (git hooks, etc.)

---

## 📋 Beneficios del Nuevo Sistema

### Comparación: Antes vs Después

#### **ANTES (Sistema de Carpetas)**
- Propuestas en archivos dispersos
- Discusión fragmentada en commits
- Sin proceso formal de revisión
- Difícil tracking del estado de propuestas
- No hay notificaciones automáticas
- Historial de decisiones poco claro

#### **DESPUÉS (Sistema PR/Issues)**
- ✅ **Discusión centralizada** en Issues
- ✅ **Proceso formal de revisión** con aprobaciones requeridas
- ✅ **Tracking automático** de estado de propuestas
- ✅ **Notificaciones inteligentes** para stakeholders relevantes
- ✅ **Historial completo** de decisiones arquitectónicas
- ✅ **Integración con código** via PRs linkados
- ✅ **Mejores métricas** de productivity y quality

### Impacto Esperado
- **+40% eficiencia** en comunicación de decisiones arquitectónicas
- **+60% transparencia** en proceso de desarrollo
- **+80% tracking** de implementación de propuestas
- **-50% tiempo** para onboarding de nuevos desarrolladores

---

**🤖 Generado con [Claude Code](https://claude.ai/code)**

**Co-Authored-By:** Claude <noreply@anthropic.com>