## 📋 Descripción
<!-- Descripción clara y concisa de los cambios implementados -->
<!-- ¿Qué problema resuelve este PR? ¿Por qué es necesario? -->

## 🎯 Tipo de Cambio
<!-- Marcar la opción que aplique -->
- [ ] 🐛 **Bug fix** - Corrige un problema existente
- [ ] ✨ **Nueva funcionalidad** - Agrega nueva funcionalidad al proyecto
- [ ] 🔧 **Mejora** - Mejora funcionalidad existente sin cambios breaking
- [ ] 💥 **Breaking change** - Cambio que causa incompatibilidad con versiones anteriores
- [ ] 📝 **Solo documentación** - Cambios únicamente en documentación
- [ ] 🎨 **Refactoring** - Cambios de código que no afectan funcionalidad
- [ ] ⚡ **Performance** - Mejoras de rendimiento
- [ ] 🔒 **Seguridad** - Corrección de vulnerabilidad o mejora de seguridad

## 🏥 Compliance con Resolución 3280
<!-- Marcar solo si aplica a compliance normativo -->
- [ ] Este PR implementa requerimientos específicos de la Resolución 3280
- [ ] **RIAS afectada**: [ RIAMP | RPMS | Ambas | N/A ]
- [ ] **Sección normativa**: [ej. Art. 4.3.1 - Control Prenatal]
- [ ] Todos los campos obligatorios han sido implementados
- [ ] Validaciones específicas según normativa incluidas
- [ ] Indicadores afectados identificados y actualizados

## 🔍 Cambios Realizados
<!-- Lista detallada de los cambios implementados -->

### **Backend Changes**:
- [ ] Modelos Pydantic actualizados
- [ ] Nuevos endpoints API implementados
- [ ] Lógica de negocio agregada/modificada
- [ ] Validaciones de datos implementadas

### **Frontend Changes**:
- [ ] Nuevos componentes React creados
- [ ] Formularios actualizados/creados
- [ ] Validaciones de UI implementadas
- [ ] Estilos y UX mejorados

### **Database Changes**:
- [ ] Nuevas tablas creadas
- [ ] Columnas agregadas/modificadas
- [ ] Índices optimizados
- [ ] RLS policies actualizadas
- [ ] **Archivo de migración**: `[timestamp]_descripcion.sql`

## 🧪 Testing
<!-- Información detallada sobre testing -->

### **Cobertura de Tests**:
- [ ] **Tests unitarios**: ≥ 90% cobertura para código nuevo
- [ ] **Tests de integración**: Flujos principales cubiertos
- [ ] **Tests E2E**: Casos críticos validados (si aplica)
- [ ] **Tests de compliance**: Validaciones normativas verificadas

### **Comandos de Testing Ejecutados**:
```bash
# Backend
cd backend && pytest -v --cov=. --cov-report=term-missing

# Frontend  
cd frontend && npm test -- --coverage --watchAll=false

# Resultados:
# - Backend: X% cobertura
# - Frontend: Y% cobertura
```

### **Testing Manual Completado**:
- [ ] Flujo completo probado en interfaz
- [ ] Validaciones de formularios verificadas
- [ ] Casos edge probados
- [ ] Performance validado (< 200ms para endpoints críticos)

## 🗄️ Cambios en Base de Datos
<!-- Solo si aplica -->
- [ ] **Migración requerida**: Sí / No
- [ ] **Migración es reversible**: Sí / No / N/A
- [ ] **Afecta datos existentes**: Sí / No
- [ ] **Requiere downtime**: Sí / No

### **Validación de Migración**:
```bash
# Comandos ejecutados:
supabase db reset  # Aplicar todas las migraciones desde cero
pytest -v         # Validar que tests siguen pasando

# Resultados: ✅ Migración exitosa
```

## 📊 Performance
<!-- Solo si hay cambios que afectan performance -->
- [ ] **Tiempo de respuesta API**: < 200ms (endpoints críticos)
- [ ] **Tiempo de carga frontend**: < 2s (páginas principales)
- [ ] **Queries optimizadas**: Sí / No / N/A
- [ ] **Nuevos índices agregados**: Sí / No

## 🔒 Consideraciones de Seguridad
<!-- Solo si hay implicaciones de seguridad -->
- [ ] No se exponen datos sensibles en logs
- [ ] Validaciones de entrada implementadas
- [ ] RLS policies actualizadas apropiadamente
- [ ] No se introducen vulnerabilidades conocidas

## 📸 Screenshots/Evidencia
<!-- Capturas de pantalla si hay cambios visuales -->
<!-- GIFs o videos para funcionalidades complejas -->

## 📋 Checklist del Desarrollador
<!-- Lista de verificación antes de solicitar review -->
- [ ] ✅ El código sigue las convenciones del proyecto
- [ ] ✅ He realizado self-review del código
- [ ] ✅ He comentado el código en áreas complejas
- [ ] ✅ He actualizado la documentación relevante
- [ ] ✅ Mis cambios no generan nuevos warnings
- [ ] ✅ He agregado tests que prueban mi funcionalidad
- [ ] ✅ Todos los tests (nuevos y existentes) pasan localmente
- [ ] ✅ He ejecutado linting y formatting
- [ ] ✅ He sincronizado con la rama main antes del PR

## 🔗 Issues Relacionados
<!-- Enlaces a issues que este PR cierra o está relacionado -->
- Closes #123
- Related to #456
- Part of Epic #789

## 📚 Referencias
<!-- Documentación relevante -->
- **Resolución 3280**: [Sección específica si aplica]
- **Documentación técnica**: [Enlaces internos]
- **Recursos externos**: [Si aplica]

## 🎯 Plan de Deployment
<!-- Consideraciones especiales para el deploy -->
- [ ] **Deploy inmediato**: Sí / No
- [ ] **Requiere coordinación**: Sí / No
- [ ] **Rollback plan**: Preparado / N/A
- [ ] **Post-deploy verification**: [Lista de verificaciones necesarias]

## 💬 Notas para el Reviewer
<!-- Información adicional que puede ser útil durante el code review -->
<!-- Áreas específicas donde necesitas feedback -->
<!-- Decisiones arquitectónicas tomadas y su justificación -->

## 📅 Timeline
<!-- Si hay consideraciones de tiempo específicas -->
- **Creado**: [Fecha]
- **Ready for Review**: [Fecha]
- **Target Merge**: [Fecha objetivo]
- **Target Deploy**: [Fecha objetivo]

---

### **Checklist del Reviewer** 
<!-- Para ser usado por quien hace el code review -->
- [ ] Código bien estructurado y legible
- [ ] Tests apropiados y suficientes
- [ ] Documentación actualizada
- [ ] Performance aceptable
- [ ] Seguridad validada
- [ ] Compliance normativo verificado (si aplica)
- [ ] Ready for merge

**Reviewers solicitados**: @usuario1, @usuario2  
**Prioridad**: [ Baja | Media | Alta | Crítica ]