# 👨‍💻 Developer Onboarding - Backend

**⏱️ Tiempo estimado:** 20 minutos  
**🎯 Objetivo:** Primer endpoint funcionando + comprensión patrón vertical  
**✅ Métrica éxito:** Ejecutar test exitosamente + crear endpoint básico

---

## 🚀 **SETUP RÁPIDO (5 minutos)**

```bash
# 1. Activar entorno
cd backend
source venv/bin/activate

# 2. Verificar instalación
python --version  # Debe ser ≥ 3.12
pip list | grep fastapi  # Verificar FastAPI instalado

# 3. Test conectividad BD
supabase status  # Debe mostrar servicios running
```

## 📊 **COMPRENSIÓN ARQUITECTURA (10 minutos)**

### **🏗️ Patrón Vertical Consolidado**
```
ESTRUCTURA MÓDULO COMPLETO:
📦 atencion_infancia/
├── 📊 models/atencion_infancia_model.py      ← Pydantic + validaciones
├── 🌐 routes/atencion_infancia.py            ← FastAPI + endpoints  
├── 🗄️ migrations/create_atencion_infancia.sql ← Schema + RLS
├── 🧪 tests/test_atencion_infancia.py        ← Tests comprehensivos
└── 📖 docs/spec.md                           ← Documentación
```

### **🔄 Patrón Polimórfico 3 Pasos**
```python
# Ejemplo real implementado
async def crear_atencion_polimorfica():
    # PASO 1: Crear detalle específico (sin atencion_id)
    detalle = await crear_detalle_infancia(datos)
    
    # PASO 2: Crear atención general (referenciando detalle)
    atencion = await crear_atencion_general(detalle.id)
    
    # PASO 3: Actualizar detalle con referencia bidireccional
    await actualizar_detalle_con_atencion(detalle.id, atencion.id)
```

### **📋 Modelos Pydantic Ejemplo**
```python
# Patrón establecido: Crear/Actualizar/Response
class AtencionInfanciaCrear(BaseModel):
    # Campos obligatorios según Resolución 3280
    peso_kg: float = Field(gt=0, le=150, description="Obligatorio normativa")
    tamizaje_visual: ResultadoTamizaje = Field(description="Crítico edad escolar")

class AtencionInfanciaResponse(AtencionInfanciaBase):
    # Campos calculados automáticamente
    estado_nutricional: EstadoNutricionalInfancia
    desarrollo_apropiado_edad: bool
    proxima_consulta_recomendada_dias: int
```

## 🧪 **TESTING COMPREHENSIVO (5 minutos)**

### **🎯 Estructura Tests Establecida**
```python
# Patrón 6 grupos organizados
class TestCRUDBasico:          # CREATE, READ, UPDATE, DELETE
class TestEndpointsEspecializados:  # Por tipo, cronológicos  
class TestEstadisticasReportes:     # Analytics + métricas
class TestCasosEdge:               # Validaciones + errores
class TestIntegracion:             # Flujos completos
class TestEliminacion:             # Cleanup + cascade
```

### **✅ Ejecutar Tests Existentes**
```bash
# Test módulo completo (ejemplo)
pytest tests/test_atencion_infancia_completo.py -v

# Test específico por grupo  
pytest tests/test_atencion_infancia_completo.py::TestCRUDBasico -v

# Test con coverage
pytest tests/test_atencion_infancia_completo.py --cov=models --cov=routes
```

---

## 🎯 **PRIMERA TAREA PRÁCTICA (15 minutos)**

### **📋 MINI-PROYECTO: Endpoint Saludo Personalizado**

#### **Paso 1: Crear Modelo (5 min)**
```python
# Crear archivo: models/saludo_model.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SaludoCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    rol: str = Field(default="desarrollador")
    
class SaludoResponse(BaseModel):
    id: str
    mensaje: str
    timestamp: datetime
    modulos_disponibles: list[str]
```

#### **Paso 2: Crear Endpoint (5 min)**
```python
# Crear archivo: routes/saludo.py
from fastapi import APIRouter
from models.saludo_model import SaludoCrear, SaludoResponse
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/saludo", tags=["Developer Onboarding"])

@router.post("/", response_model=SaludoResponse)
async def crear_saludo(saludo_data: SaludoCrear):
    return SaludoResponse(
        id=str(uuid4()),
        mensaje=f"¡Hola {saludo_data.nombre}! Bienvenido como {saludo_data.rol}",
        timestamp=datetime.now(),
        modulos_disponibles=[
            "Primera Infancia ✅", 
            "Infancia ✅", 
            "Control Cronicidad ✅",
            "Tamizaje Oncológico ✅",
            "Adolescencia ⏸️ (Tu próximo módulo)"
        ]
    )
```

#### **Paso 3: Registrar Router (2 min)**
```python
# Editar: main.py (agregar línea)
from routes import saludo  # ← Agregar import

app.include_router(saludo.router)  # ← Agregar línea
```

#### **Paso 4: Crear Test (3 min)**
```python
# Crear archivo: tests/test_saludo_onboarding.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_saludo_desarrollador():
    datos = {
        "nombre": "Nuevo Dev",
        "rol": "backend_developer"
    }
    
    response = client.post("/saludo/", json=datos)
    assert response.status_code == 200
    
    data = response.json()
    assert "Hola Nuevo Dev" in data["mensaje"]
    assert "backend_developer" in data["mensaje"]
    assert "Primera Infancia ✅" in data["modulos_disponibles"]
    assert len(data["modulos_disponibles"]) >= 4
```

### **✅ Validar Implementación**
```bash
# 1. Ejecutar server
uvicorn main:app --reload

# 2. Probar endpoint manualmente
curl -X POST "http://localhost:8000/saludo/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Mi Nombre", "rol": "backend_ninja"}'

# 3. Ejecutar test
pytest tests/test_saludo_onboarding.py -v

# 4. Ver en FastAPI Docs
# Abrir: http://localhost:8000/docs
# Probar endpoint /saludo/ interactivamente
```

---

## 🎯 **SIGUIENTES PASOS RECOMENDADOS**

### **📚 Profundización Inmediata**
1. **[Architectural Patterns](../04-development/architectural-patterns.md)** - Entender polimorfismo profundo
2. **[Data Strategy](../04-development/data-strategy.md)** - Tipado en 3 capas + migrations
3. **[Testing Patterns](../04-development/testing-patterns.md)** - Suite completa testing

### **🛠️ Práctica Avanzada**
1. **Implementar módulo RIAS nuevo** siguiendo patrón vertical
2. **Contribuir a Adolescencia (12-29 años)** - Próximo en roadmap
3. **Optimizar queries existentes** usando data-strategy patterns

### **🚀 Convertirse en Experto**
1. **Mentoría nuevos developers** usando esta guía
2. **Proponer mejoras arquitectónicas** basadas en experiencia
3. **Liderar implementación módulos complejos**

---

## 📖 **RECURSOS COMPLEMENTARIOS**

### **🔧 Herramientas Esenciales**
- **FastAPI Docs:** http://localhost:8000/docs - API explorer interactivo
- **Supabase Studio:** http://127.0.0.1:54323 - Database management
- **Database URL:** postgresql://postgres:postgres@127.0.0.1:54322/postgres

### **📚 Documentación Crítica**
- **[Estado Proyecto](../../PROJECT-STATUS.md)** - Módulos completados vs pendientes
- **[RPMS Detallada](../02-regulations/resolucion-3280-rpms.md)** - Momentos curso vida
- **[Compliance Analysis](../02-regulations/compliance-analysis-3280.md)** - Gaps normativos

### **🤖 AI Assistant Setup**
- **Claude Code Assistant:** Ver `CLAUDE.md` para configuración completa
- **Patrones prompts:** Optimizados para arquitectura proyecto

---

## ✅ **CHECKLIST ONBOARDING COMPLETADO**

- [ ] ✅ Setup entorno funcionando (venv + supabase)
- [ ] ✅ Comprensión patrón vertical (modelo + ruta + test)  
- [ ] ✅ Polimorfismo 3 pasos entendido conceptualmente
- [ ] ✅ Primer endpoint implementado y funcionando
- [ ] ✅ Test ejecutado exitosamente
- [ ] ✅ FastAPI Docs explorado interactivamente

**🎉 ¡Felicitaciones! Estás listo para contribuir al proyecto. Tu próximo objetivo: implementar un módulo RIAS completo siguiendo el patrón establecido.**