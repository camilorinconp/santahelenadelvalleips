# Proyecto IPS Santa Helena del Valle - Visión General

## 📋 Resumen Ejecutivo

Sistema integral para la gestión de Rutas Integrales de Atención en Salud (RIAS) según la Resolución 3280 de 2018, desarrollado como una solución completa con backend API (FastAPI), frontend web (React) y base de datos PostgreSQL gestionada con Supabase.

**Fecha de última actualización:** 12 de septiembre, 2025  
**Versión actual:** v0.4.0-riamp-partial

## 🎯 Estado Actual del Proyecto

### ✅ **Completado (85%)**

#### **Infraestructura y Arquitectura Base**
- **Backend API**: FastAPI con arquitectura polimórfica de datos implementada
- **Frontend SPA**: React con TypeScript y Material-UI completamente configurado
- **Base de Datos**: PostgreSQL con Supabase, migraciones versionadas funcionando
- **Testing**: Suite de pruebas con 25 tests pasando (90% cobertura en áreas implementadas)
- **Documentación**: CLAUDE.md en las 3 carpetas principales

#### **Funcionalidades Operativas**
- **Gestión de Pacientes**: CRUD completo funcionando
- **Gestión de Médicos**: Modelo y endpoints básicos
- **Atenciones Base**: Sistema polimórfico principal implementado
- **RIAMP Parcial**: Estructura base para atención materno-perinatal

### 🚧 **En Desarrollo (40%)**

#### **RIAMP (Ruta Integral Atención Materno Perinatal)**
- **Control Prenatal**: Modelo con campos básicos, necesita completar 47 campos adicionales según Resolución 3280
- **Atención del Parto**: Estructura base creada, faltan validaciones específicas y partograma
- **Puerperio**: Modelo inicial, necesita refinamiento completo
- **Recién Nacido**: Estructura básica, falta implementación de protocolos específicos

### ❌ **Pendiente (0%)**

#### **RPMS (Ruta Integral Promoción y Mantenimiento de Salud)**
- **Primera Infancia (0-5 años)**: No implementado
- **Infancia (6-11 años)**: No implementado  
- **Adolescencia (12-17 años)**: No implementado
- **Juventud (18-28 años)**: No implementado
- **Adultez (29-59 años)**: No implementado
- **Vejez (60+ años)**: No implementado

#### **Funcionalidades Críticas Pendientes**
- **Indicadores Automatizados**: Cálculo de métricas obligatorias Resolución 3280
- **Dashboard de Reportería**: Visualización de indicadores en tiempo real
- **Sistema de Alertas**: Notificaciones por incumplimiento de protocolos
- **Autenticación y Roles**: Gestión de usuarios y permisos

## 🏗️ Arquitectura Actual

### **Polimorfismo de Datos (Fortaleza Clave)**
```
atenciones (tabla principal)
├── atencion_materno_perinatal
│   ├── detalle_control_prenatal
│   ├── detalle_parto  
│   ├── detalle_recien_nacido
│   └── detalle_puerperio
├── control_cronicidad (pendiente completar)
├── tamizaje_oncologico (pendiente completar)
└── [otras RIAS pendientes]
```

### **Stack Tecnológico**
- **Backend**: Python 3.12 + FastAPI + Pydantic + Pytest
- **Frontend**: React 19 + TypeScript + Material-UI + React Query
- **Base de Datos**: PostgreSQL 17 + Supabase CLI
- **Despliegue**: Local development + Supabase cloud

## 🎯 Próximos 3 Hitos Críticos

### **Hito 1: RIAMP Completa (Prioridad: ALTA)**
**Objetivo**: Cumplir 100% con Resolución 3280 para población materno-perinatal  
**Timeline Estimado**: 4-6 semanas  
**Entregables**:
- 47 campos adicionales en control prenatal con validaciones
- Partograma digital completo
- Protocolos de recién nacido según normativa
- 15 indicadores RIAMP automatizados

### **Hito 2: RPMS Primera Infancia (Prioridad: ALTA)**
**Objetivo**: Implementar ruta completa para niños 0-5 años  
**Timeline Estimado**: 6-8 semanas después de Hito 1  
**Entregables**:
- Modelos de datos para valoración del desarrollo
- Sistema de alertas por edad y periodicidad
- Esquema de vacunación integrado
- Dashboard específico primera infancia

### **Hito 3: Indicadores y Dashboard (Prioridad: MEDIA)**  
**Objetivo**: Sistema de monitoreo y reportería completo  
**Timeline Estimado**: 4-6 semanas después de Hito 2  
**Entregables**:
- Dashboard ejecutivo con indicadores obligatorios
- Reportes automatizados para entes de control
- Sistema de alertas por incumplimiento
- APIs de integración con otros sistemas

## 📊 Métricas de Calidad Actual

### **Código y Testing**
- **Cobertura de Pruebas**: 90% en áreas implementadas
- **Tests Totales**: 25 tests automatizados pasando
- **Deuda Técnica**: Baja (arquitectura sólida establecida)
- **Documentación**: 95% actualizada

### **Cumplimiento Normativo**
- **Resolución 3280**: 40% implementado (solo RIAMP parcial)
- **Campos Obligatorios**: 60% capturados para RIAMP
- **Indicadores Requeridos**: 0% automatizados
- **RIPS Compliance**: Pendiente implementar

### **Performance**
- **Respuesta API**: < 100ms para operaciones CRUD básicas
- **Base de Datos**: 22 migraciones aplicadas sin issues
- **Frontend**: Carga inicial < 2 segundos

## 🔧 Comandos Rápidos de Desarrollo

### **Setup Inicial**
```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Frontend  
cd frontend && npm install

# Base de datos
supabase start
```

### **Desarrollo Diario**
```bash
# Backend server
cd backend && uvicorn main:app --reload

# Frontend server
cd frontend && npm start

# Tests
cd backend && pytest -v
```

### **Base de Datos**
```bash
# Crear migración
supabase db diff -f descripcion_cambio

# Aplicar migraciones
supabase db push

# Reset local
supabase db reset
```

## 🚨 Issues Críticos Conocidos

### **Técnicos**
1. **Cache de Schema Supabase**: A veces requiere restart después de migraciones
2. **RLS Policies**: Necesitan refinamiento para producción
3. **Frontend Forms**: Validaciones de campos opcionales con valores null

### **Funcionales**
1. **Resolución 3280**: 60% de los campos requeridos aún no capturados
2. **Indicadores**: Cálculos manuales, necesitan automatización
3. **Interoperabilidad**: RIPS no implementados

## 📚 Documentación Clave

### **Normativa y Arquitectura**
- `backend/docs/resolucion_3280_de_2018_limpio.md` - **DOCUMENTO MAESTRO**
- `backend/docs/recomendaciones_equipo_asesor_externo.md` - Guía arquitectónica
- `backend/GEMINI.md` - Contexto del polimorfismo de datos

### **Configuración por Componente**
- `backend/CLAUDE.md` - Setup y convenciones backend
- `frontend/CLAUDE.md` - Setup y convenciones frontend  
- `supabase/CLAUDE.md` - Gestión de base de datos

### **Desarrollo y Evolución**
- `backend/DEVELOPMENT_LOG.md` - Lecciones aprendidas críticas
- `ROADMAP.md` - Hoja de ruta detallada (próximo documento)

## 🎯 Recomendaciones para Nuevo Desarrollador

### **Para comenzar inmediatamente:**
1. Leer `docs/resolucion_3280_de_2018_limpio.md` (contexto crítico)
2. Ejecutar setup completo usando comandos rápidos
3. Ejecutar `pytest -v` para validar entorno
4. Revisar `backend/models/atencion_materno_perinatal_model.py` para entender polimorfismo

### **Para contribuir efectivamente:**
1. Seguir patrón polimórfico establecido para nuevas RIAS
2. Siempre crear tests junto con nuevas funcionalidades  
3. Validar campos contra Resolución 3280 antes de implementar
4. Documentar decisiones arquitectónicas importantes

---

**Última revisión**: 2025-09-12  
**Próxima revisión programada**: Después de completar Hito 1 (RIAMP Completa)  
**Responsable**: Equipo Principal de Desarrollo