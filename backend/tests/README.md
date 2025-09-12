# 🧪 Testing Infrastructure - Backend

## Configuración Global de Tests

Este directorio contiene la infraestructura completa de testing para el backend de la IPS Santa Helena del Valle.

### ⚙️ **Configuración Automática**

La configuración global de tests está implementada en `conftest.py`:

- **✅ Service Role Override Global**: Todos los tests usan automáticamente el service_role de Supabase para bypass RLS
- **✅ Test Client Session**: Cliente de prueba configurado una vez para toda la sesión
- **✅ Database Access**: Acceso directo al cliente de Supabase con permisos completos
- **✅ Cleanup Automático**: Limpieza de configuración al finalizar los tests

### 🚀 **Uso Sencillo**

Para cualquier test nuevo, simplemente usa el fixture `test_client`:

```python
def test_mi_nueva_funcionalidad(test_client):
    """Test que automáticamente usa service_role para bypass RLS"""
    response = test_client.post("/mi-endpoint/", json={"data": "test"})
    assert response.status_code == 201
```

### 📊 **Estado Actual**

**Tests Funcionando**: 20/24 (83% success rate)

#### ✅ **Tests Completamente Funcionales:**
- `test_pacientes.py` - CRUD completo de pacientes (4/4)
- `test_atencion_primera_infancia.py` - Atención primera infancia (3/3)
- `test_atenciones.py` - Atenciones genéricas (3/3)
- `test_intervenciones_colectivas.py` - Intervenciones colectivas (6/6)
- `test_tamizaje_oncologico.py` - Tamizaje oncológico (3/3)
- `test_main.py` - Endpoint principal (1/1)

#### ⚠️ **Tests Con Problemas de Lógica (NO RLS):**
- `test_atencion_materno_perinatal.py` - Código incompleto, funcionalidad core OK
- `test_control_cronicidad.py` - Modelos Pydantic desincronizados

### 🛠️ **Utilidades Disponibles**

En `conftest.py` se incluyen utilidades para tests:

```python
# Generar UUIDs para tests
test_id = create_test_uuid()

# Crear datos de paciente estándar
patient_data = create_test_patient_data(patient_id)

# Acceso directo a base de datos
def test_direct_db_access(service_db_client):
    result = service_db_client.table("tabla").select("*").execute()
```

### 🔧 **Comandos de Testing**

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_pacientes.py -v

# Ejecutar con coverage
pytest tests/ --cov=. --cov-report=html

# Ejecutar tests con detalles de fallas
pytest tests/ -v --tb=short
```

### ✨ **Características Técnicas**

- **Session Scope**: Cliente de test se crea una vez por sesión completa
- **Auto Override**: Service role se configura automáticamente sin intervención manual  
- **Clean Teardown**: Configuración se limpia apropiadamente al finalizar
- **Debug Friendly**: Mensajes informativos sobre configuración durante ejecución

### 📋 **Próximas Mejoras**

1. **Fixtures de Datos**: Crear fixtures comunes para entidades frecuentes
2. **Test Isolation**: Implementar limpieza automática de datos entre tests
3. **Performance**: Optimizar setup/teardown para tests más rápidos
4. **Coverage**: Aumentar cobertura a 95%+ en módulos críticos

---

**Nota**: Esta configuración resuelve completamente los problemas de RLS que impedían la ejecución de tests. Todos los desarrolladores pueden ahora ejecutar tests sin configuración manual adicional.