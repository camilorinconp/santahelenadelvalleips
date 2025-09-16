# 📋 Resolución 3280 - Artículos y Marco Normativo

**📅 Fuente:** Resolución 3280 de 2018 - Artículos 1° al 7°  
**🎯 Propósito:** Marco jurídico y operativo para implementación RIAS

---

## 🏛️ **ARTÍCULOS PRINCIPALES**

### **Artículo 1° - Objeto**
```
La presente resolución tiene por objeto adoptar los lineamientos técnicos y operativos de:
- Ruta Integral de Atención para la Promoción y Mantenimiento de la Salud (RPMS)
- Ruta Integral de Atención en Salud para la Población Materno Perinatal (RIAMP)

IMPACTO TÉCNICO: Base legal para implementar todos los módulos RIAS del sistema.
```

### **Artículo 2° - Campo de Aplicación**
```
OBLIGATORIO para:
✅ Entidades Territoriales
✅ Entidades Promotoras de Salud (EPS)
✅ Prestadores de servicios de salud
✅ Entidades responsables de intervenciones en salud

IMPACTO TÉCNICO: El sistema debe cumplir 100% con estas especificaciones.
```

### **Artículo 3° - Adaptación de las Rutas**
```
PRINCIPIO CLAVE: Las rutas pueden adaptarse según:
- Condiciones territoriales (urbano, rural, disperso)
- Diferentes grupos poblacionales
- PERO: Sin constituir barrera de acceso
- PERO: Sin requerir autorización previa

IMPACTO TÉCNICO: Flexibilidad de configuración manteniendo núcleo normativo.
```

### **Artículo 4° - Progresividad y Transitoriedad**
```
CRONOGRAMA:
- Implementación total desde vigencia de la resolución
- 6 meses para entrar en vigencia (desde agosto 2018)
- Derogación automática de Resolución 412 de 2000

IMPACTO TÉCNICO: No hay opcionalidad, es cumplimiento obligatorio total.
```

### **Artículo 5° - Talento Humano**
```
RECURSOS HUMANOS:
- Personal capacitado según lineamientos
- Competencias específicas por tipo de atención
- Educación médica continua obligatoria

IMPACTO TÉCNICO: Validaciones de usuario por rol y competencia.
```

### **Artículo 6° - Monitoreo y Evaluación**
```
REPORTERÍA OBLIGATORIA:
- Indicadores de proceso y resultado
- Reportes periódicos al SISPRO
- Evaluación continua de calidad

IMPACTO TÉCNICO: Sistema de métricas y reportería automatizada requerido.
```

### **Artículo 7° - Vigencias y Derogatorias**
```
TIMELINE:
- Vigencia: 6 meses después de publicación (febrero 2019)
- Derogatoria: Resolución 412 de 2000
- Transitoriedad: Implementación gradual permitida

IMPACTO TÉCNICO: Migración completa de marcos normativos anterior.
```

---

## 🎯 **IMPACTOS TÉCNICOS CRÍTICOS**

### **1. 🔒 Cumplimiento Obligatorio**
```
❌ NO opcional
❌ NO configurable como "deshabilitado"
✅ Debe implementarse 100%
✅ Auditable por autoridades
```

### **2. 📊 Reportería Automática**
```
SISPRO Reports required:
- Cobertura por momento de vida
- Indicadores de calidad
- Seguimiento longitudinal pacientes
- Métricas de acceso y oportunidad
```

### **3. 👥 Control de Acceso por Roles**
```
Perfiles técnicos requeridos:
- Médico general
- Especialistas por área
- Enfermería profesional
- Auxiliares de enfermería
- Psicología
- Trabajo social
```

### **4. 🏗️ Arquitectura Flexible pero Completa**
```
DEBE soportar:
- Configuración territorial
- Múltiples grupos poblacionales
- Sin barreras de acceso
- Autorización automática
```

---

## 📋 **CHECKLIST COMPLIANCE TÉCNICO**

### **✅ Implementado**
- [x] Estructura polimórfica para múltiples RIAS
- [x] Primera Infancia (0-5 años) completa
- [x] Infancia (6-11 años) completa
- [x] Base de datos con RLS y auditabilidad
- [x] API REST con validaciones normativas

### **⏸️ En Desarrollo**
- [ ] Reportería SISPRO automatizada
- [ ] Adolescencia y Juventud (12-29 años)
- [ ] Adultez (30-59 años)
- [ ] Vejez (60+ años)
- [ ] RIAMP completa (40% actual)

### **📋 Pendiente**
- [ ] Control de acceso granular por rol profesional
- [ ] Métricas en tiempo real para auditorías
- [ ] Configuración territorial automática
- [ ] Integración con otros sistemas SGSSS

---

## 🔗 **Referencias Técnicas**

- **[RPMS Detallada](./resolucion-3280-rpms.md)** - Promoción y mantenimiento específicos
- **[RIAMP Detallada](./resolucion-3280-riamp.md)** - Materno-perinatal específicos  
- **[Análisis Compliance](./compliance-analysis-3280.md)** - Estado técnico actual
- **[Resolución 202 Strategy](./resolucion-202-strategy.md)** - Reportería SISPRO

---

*📋 Para texto legal completo, consultar archivo histórico resolucion-3280-master.md*