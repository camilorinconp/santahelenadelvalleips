# 🧪 Guía de Testing - IPS Santa Helena del Valle

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía completa para testing en el proyecto  
**📍 Estado:** v1.0 - Migrada desde reorganización documental  

---

## 🎯 **Filosofía de Testing**

El proyecto sigue un enfoque **Test-Driven Development (TDD)** con énfasis en:
- **Cobertura completa:** 95%+ en áreas implementadas
- **Testing por capas:** Modelos → Servicios → Routes → Integración
- **Datos reales:** Tests con datos representativos del sistema de salud colombiano
- **Validación normativa:** Verificación automática de compliance con Resolución 3280

---

## 🏗️ **Estructura de Testing**

### **Framework y Herramientas**
```python
# Stack principal
pytest                    # Framework principal
pytest-asyncio           # Testing async/await
pytest-mock             # Mocking avanzado
pytest-cov              # Cobertura de código
httpx                    # Cliente HTTP para testing FastAPI
```

### **Organización de Tests**
```
backend/tests/
├── conftest.py                    # Configuración global, fixtures
├── test_pacientes.py             # Testing CRUD pacientes
├── test_atencion_materno_perinatal.py  # Testing polimorfismo anidado
├── test_control_cronicidad.py    # Testing cronicidad
├── test_reporteria_pedt_simple.py # Testing reportería híbrida
├── fixtures/                     # Datos de prueba
│   ├── pacientes_test_data.py
│   └── atencion_test_data.py
└── integration/                  # Tests de integración
    └── test_full_workflow.py
```

---

## 🔧 **Comandos Esenciales**

### **Ejecutar Tests**
```bash
# Todos los tests
pytest -v

# Tests específicos
pytest tests/test_atencion_materno_perinatal.py -v

# Con cobertura
pytest --cov=. --cov-report=html

# Solo tests que fallan
pytest --lf

# Tests en paralelo
pytest -n auto
```

### **Debugging Tests**
```bash
# Con output completo
pytest -s -v

# Parar en primer fallo
pytest -x

# Con debugger
pytest --pdb
```

---

## 📋 **Patrones de Testing Establecidos**

### **1. Testing Modelos Pydantic**
```python
def test_paciente_model_validation():
    """Test validación modelo Paciente con datos colombianos"""
    paciente_data = {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
        "primer_nombre": "María",
        "primer_apellido": "González",
        "fecha_nacimiento": "1985-05-15",
        "genero": "F",
        # ... campos adicionales
    }
    
    paciente = PacienteCreate(**paciente_data)
    assert paciente.tipo_documento == "CC"
    assert paciente.calcular_edad() > 0
```

### **2. Testing Polimorfismo Anidado**
```python
@pytest.mark.asyncio
async def test_crear_atencion_materno_perinatal_completa():
    """Test creación atención con polimorfismo anidado"""
    # 1. Crear detalle específico
    detalle = DetalleControlPrenatal(
        fecha_ultimo_parto="2020-01-15",
        numero_controles_prenatales=8,
        riesgo_biopsicosocial="BAJO"
    )
    
    # 2. Crear atención principal
    atencion = AtencionMaternoPerinatal(
        paciente_id=test_paciente_id,
        tipo_atencion="CONTROL_PRENATAL",
        detalle_control_prenatal=detalle
    )
    
    # 3. Verificar relaciones
    assert atencion.detalle_control_prenatal is not None
    assert atencion.tipo_atencion == "CONTROL_PRENATAL"
```

### **3. Testing APIs con FastAPI**
```python
def test_crear_paciente_endpoint(client):
    """Test endpoint creación paciente"""
    response = client.post(
        "/api/pacientes/",
        json=paciente_test_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["numero_documento"] == paciente_test_data["numero_documento"]
    assert "id" in data
```

### **4. Testing Base de Datos**
```python
@pytest.mark.asyncio
async def test_database_connection():
    """Test conexión y operaciones básicas BD"""
    async with get_db_session() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

---

## 🎯 **Testing por Módulo**

### **Pacientes (COMPLETADO)**
- ✅ Validación modelos Pydantic
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validaciones de negocio
- ✅ Endpoints FastAPI
- ✅ Manejo de errores

### **Atención Materno Perinatal (COMPLETADO)**
- ✅ Polimorfismo anidado
- ✅ Relaciones entre tablas
- ✅ Validaciones específicas por tipo
- ✅ Tests de integración completos

### **Control Cronicidad (COMPLETADO)**
- ✅ Modelos básicos
- ✅ Validaciones específicas
- ✅ Tests de creación/lectura

### **Reportería PEDT (EN DESARROLLO)**
- 🔄 Testing híbrido para variables calculadas
- 🔄 Validación compliance Resolución 202
- ❌ Testing reportes automáticos (pendiente)

---

## 📊 **Fixtures y Datos de Prueba**

### **Configuración en conftest.py**
```python
@pytest.fixture
async def db_session():
    """Sesión de BD para tests"""
    async with get_db_session() as session:
        yield session

@pytest.fixture
def client():
    """Cliente HTTP para tests de API"""
    return TestClient(app)

@pytest.fixture
async def test_paciente(db_session):
    """Paciente de prueba"""
    paciente_data = {
        "tipo_documento": "CC",
        "numero_documento": f"TEST_{random.randint(1000000, 9999999)}",
        "primer_nombre": "Test",
        "primer_apellido": "Paciente"
        # ... campos adicionales
    }
    
    # Crear y retornar
    paciente = await create_paciente(db_session, paciente_data)
    yield paciente
    
    # Cleanup
    await delete_paciente(db_session, paciente.id)
```

### **Datos Representativos**
```python
# fixtures/pacientes_test_data.py
PACIENTES_COLOMBIA_SAMPLE = [
    {
        "tipo_documento": "CC",
        "numero_documento": "1234567890",
        "primer_nombre": "María",
        "segundo_nombre": "Isabel",
        "primer_apellido": "González",
        "segundo_apellido": "Rodríguez",
        "fecha_nacimiento": "1990-03-15",
        "genero": "F",
        "telefono": "3001234567",
        "direccion": "Carrera 7 # 32-16",
        "municipio": "Bogotá D.C.",
        "departamento": "Cundinamarca"
    },
    # ... más datos representativos
]
```

---

## ⚠️ **Testing de Edge Cases**

### **Validaciones Normativa Colombiana**
```python
def test_validacion_documento_identidad():
    """Test validación documentos según normativa colombiana"""
    # CC válida
    assert validar_cedula("1234567890") == True
    
    # Casos edge
    assert validar_cedula("0000000000") == False
    assert validar_cedula("1234567890123") == False
    
    # TI para menores
    assert validar_tarjeta_identidad("1234567890", edad=15) == True
    assert validar_tarjeta_identidad("1234567890", edad=20) == False
```

### **Fechas y Rangos**
```python
def test_validacion_fechas_medicas():
    """Test validaciones de fechas críticas"""
    # Fecha nacimiento no puede ser futura
    with pytest.raises(ValueError):
        crear_paciente(fecha_nacimiento="2026-01-01")
    
    # Último parto no puede ser futuro
    with pytest.raises(ValueError):
        crear_control_prenatal(fecha_ultimo_parto="2026-01-01")
```

---

## 🔍 **Testing de Performance**

### **Benchmarks Básicos**
```python
def test_performance_busqueda_pacientes():
    """Test performance búsqueda pacientes"""
    import time
    
    start = time.time()
    response = client.get("/api/pacientes/?limit=100")
    end = time.time()
    
    assert response.status_code == 200
    assert (end - start) < 0.5  # Menos de 500ms
```

### **Testing Carga**
```python
@pytest.mark.asyncio
async def test_creacion_masiva_pacientes():
    """Test creación masiva para verificar escalabilidad"""
    pacientes = [
        generar_paciente_aleatorio() 
        for _ in range(100)
    ]
    
    start = time.time()
    tasks = [crear_paciente_async(p) for p in pacientes]
    results = await asyncio.gather(*tasks)
    end = time.time()
    
    assert len(results) == 100
    assert (end - start) < 10  # Menos de 10 segundos para 100 pacientes
```

---

## 📈 **Métricas y Reportes**

### **Cobertura Actual**
- **Modelos:** 95% cobertura
- **Routes:** 90% cobertura
- **Services:** 85% cobertura
- **Total:** 92% cobertura promedio

### **Comando Reporte HTML**
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html  # macOS
```

### **CI/CD Integration**
```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: |
    pytest --cov=. --cov-report=xml --cov-fail-under=90
    
- name: Upload coverage
  uses: codecov/codecov-action@v1
```

---

## 🚀 **Testing Avanzado**

### **Mocking Supabase**
```python
@pytest.fixture
def mock_supabase():
    with patch('database.supabase') as mock:
        mock.table.return_value.select.return_value.execute.return_value = {
            'data': [test_paciente_data],
            'error': None
        }
        yield mock
```

### **Testing Async/Await**
```python
@pytest.mark.asyncio
async def test_async_database_operation():
    """Test operaciones asíncronas"""
    async with get_db_session() as session:
        result = await async_create_paciente(session, test_data)
        assert result.id is not None
```

---

## 📋 **Checklist Nuevo Feature**

Antes de considerar completado un feature:

### **Testing Obligatorio:**
- [ ] Tests unitarios para modelos Pydantic
- [ ] Tests para lógica de negocio/servicios
- [ ] Tests para endpoints FastAPI
- [ ] Tests de integración con BD
- [ ] Tests de edge cases y validaciones
- [ ] Cobertura mínima 90%

### **Testing Recomendado:**
- [ ] Tests de performance básicos
- [ ] Mocking para dependencias externas
- [ ] Tests con datos representativos colombianos
- [ ] Validación compliance normativo

### **Documentación Testing:**
- [ ] Docstrings descriptivos en tests
- [ ] Comentarios para lógica compleja
- [ ] Fixtures documentados
- [ ] Actualización de este guide si aplica

---

## 🔗 **Referencias y Recursos**

### **Documentación Oficial:**
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic Validators](https://pydantic-docs.helpmanual.io/usage/validators/)

### **Archivos Relacionados:**
- `backend/conftest.py` - Configuración global tests
- `backend/tests/` - Suite completa de tests
- `backend/requirements.txt` - Dependencias testing

---

**🔄 Este documento se actualiza con cada nuevo patrón de testing implementado**  
**👥 Mantenido por:** Equipo Técnico Principal  
**🎯 Objetivo:** Garantizar calidad y reliability del código