# 🚀 Quick Start - Guías de Onboarding

**🎯 Propósito:** Onboarding rápido y efectivo por rol profesional  
**⏱️ Tiempo estimado:** 15-30 minutos según rol  
**📊 Éxito medido:** Capacidad ejecutar primera tarea en <1 hora

---

## 🎯 **SELECCIONA TU ROL**

### **👨‍💻 [DESARROLLADOR BACKEND](./developer-onboarding.md)** 
```
⏱️  Tiempo: 20 minutos
🎯 Objetivo: Primer endpoint funcionando
📋 Incluye: Setup, testing, primer módulo RIAS
```

### **🏗️ [ARQUITECTO / TECH LEAD](./architect-onboarding.md)**
```
⏱️  Tiempo: 30 minutos  
🎯 Objetivo: Comprensión arquitectónica completa
📋 Incluye: Patrones, decisiones técnicas, roadmap
```

### **⚙️ [DEVOPS / SRE](./devops-onboarding.md)**
```
⏱️  Tiempo: 25 minutos
🎯 Objetivo: Infraestructura operativa
📋 Incluye: Deployment, monitoring, troubleshooting
```

### **🏥 [PRODUCT OWNER / COMPLIANCE](./compliance-onboarding.md)**
```
⏱️  Tiempo: 15 minutos
🎯 Objetivo: Estado compliance y métricas
📋 Incluye: Normativas, gaps, plan cumplimiento
```

### **🎨 [FRONTEND DEVELOPER](./frontend-onboarding.md)**
```
⏱️  Tiempo: 20 minutos
🎯 Objetivo: Integración con backend polimórfico
📋 Incluye: API patterns, data types, componentes
```

---

## 🚀 **SETUP UNIVERSAL (Todos los roles)**

### **📋 Pre-requisitos (5 minutos)**
```bash
# Verificar herramientas instaladas
python --version    # ≥ 3.12
node --version      # ≥ 18 (si frontend)
docker --version    # Latest
git --version       # Latest

# Clonar repositorio
git clone [repo-url] proyecto_salud
cd proyecto_salud
```

### **🔧 Configuración Básica (10 minutos)**
```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Database setup (Supabase local)
cd ../supabase
supabase start

# Verificar funcionamiento
cd ../backend
pytest tests/test_pacientes.py -v  # Test básico
```

### **✅ Verificación Setup**
```bash
# API funcionando
curl http://localhost:8000/health/

# Base datos conectada  
curl http://localhost:8000/pacientes/

# Frontend funcionando (si aplica)
curl http://localhost:3000/
```

---

## 📊 **MÉTRICAS DE ÉXITO ONBOARDING**

| Rol | Tiempo Target | Métrica Éxito | Validación |
|-----|---------------|---------------|------------|
| **Developer** | 20 min | Ejecutar 1 test exitosamente | `pytest test_pacientes.py -v` |
| **Architect** | 30 min | Explicar polimorfismo anidado | Quiz conceptual |
| **DevOps** | 25 min | Deploy local funcionando | Health checks OK |
| **Compliance** | 15 min | Identificar gap crítico | Report compliance |
| **Frontend** | 20 min | Consumir 1 API endpoint | React component |

---

## 🎯 **RUTAS DE APRENDIZAJE**

### **🟢 BÁSICO (Primer día)**
1. **Setup universal** ✅
2. **Guía específica tu rol** ✅
3. **Primera tarea práctica** ✅

### **🟡 INTERMEDIO (Primera semana)**
1. **Arquitectura completa** → [Architecture Overview](../01-foundations/architecture-overview.md)
2. **Normativas clave** → [Resolución 3280](../02-regulations/resolucion-3280-overview.md)
3. **Patrones desarrollo** → [Best Practices](../04-development/best-practices-overview.md)

### **🔴 AVANZADO (Primer mes)**
1. **Especialización técnica profunda**
2. **Contribución módulos nuevos**
3. **Mentoría otros desarrolladores**

---

## 📚 **RECURSOS DE APOYO**

### **📖 Documentación Crítica**
- **[Arquitectura Maestra](../01-foundations/architecture-overview.md)** - Hub central navegación
- **[Estado Proyecto](../../PROJECT-STATUS.md)** - Progreso actual módulos
- **[Compliance 3280](../02-regulations/resolucion-3280-overview.md)** - Requerimientos normativos

### **🔧 Herramientas Desarrollo**
- **Supabase Studio:** http://127.0.0.1:54323 (DB management)
- **FastAPI Docs:** http://127.0.0.1:8000/docs (API explorer)
- **Health Check:** http://127.0.0.1:8000/health/ (System status)

### **💬 Comunicación**
- **Issues GitHub:** Reportar problemas/preguntas
- **Claude Code Assistant:** Configurado para proyecto (ver `CLAUDE.md`)

---

## ⚠️ **TROUBLESHOOTING COMÚN**

### **🔴 Setup Falló**
```bash
# Limpiar y reiniciar
supabase stop && supabase start
cd backend && source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### **🔴 Tests Fallan**
```bash
# Verificar BD funcionando
supabase status
cd backend && python -c "from database import get_supabase_client; print('DB OK')"
```

### **🔴 Puertos Ocupados**
```bash
# Identificar procesos
lsof -i :8000  # FastAPI
lsof -i :3000  # React
lsof -i :54321 # Supabase

# Matar si necesario
kill -9 [PID]
```

---

**🚀 ¡Comienza con tu rol específico! Cada guía está diseñada para máxima eficiencia y mínima fricción.**