# 🛣️ Hoja de Ruta - Proyecto IPS Santa Helena del Valle

**Versión**: v1.0  
**Última actualización**: 13 de septiembre, 2025  
**Horizonte de planificación**: 12 meses

## 🎯 Visión del Proyecto

Crear el sistema de gestión de RIAS más completo y conforme a la normativa colombiana (Resolución 3280 de 2018), que permita a la IPS Santa Helena del Valle ofrecer atención integral de calidad con trazabilidad completa y reportería automatizada.

---

## 📊 Estado Actual - MILESTONE ARQUITECTURA TRANSVERSAL COMPLETADA

- **✅ Infraestructura**: 95% completa
- **✅ RIAMP**: 85% implementada  
- **🎉 Arquitectura Transversal**: 100% IMPLEMENTADA **[COMPLETADO 13-Sep-2025]**
- **✅ Estrategia Perfiles Duales**: 100% documentada
- **🔄 RPMS Integración**: 20% iniciada **[PRÓXIMO MILESTONE]**
- **❌ Frontend Call Center**: 0% implementado
- **❌ Indicadores**: 0% automatizados
- **✅ Testing**: 95% cobertura en áreas activas

### 🏗️ **MILESTONE CRÍTICO COMPLETADO - 13 Sep 2025**
**ARQUITECTURA TRANSVERSAL SEGÚN RESOLUCIÓN 3280:**
- ✅ **Entornos de Salud Pública**: 30+ endpoints operativos
- ✅ **Familia Integral**: Gestión completa de núcleo familiar  
- ✅ **Atención Integral Transversal**: Coordinación de cuidados
- ✅ **Base de datos robusta**: RLS configurado, 12 migraciones aplicadas
- ✅ **Backend remoto**: Supabase productivo conectado
- ✅ **Verificación funcional**: Todos los componentes probados

### 🎯 **Impacto del Milestone**
- **Base sólida** para escalamiento a todo el ecosistema RIAS
- **Puntos de retorno seguros** establecidos
- **Capacidad transversal** lista para integrar RPMS
- **Fundación robusta** para frontend especializado

---

## 🗓️ CRONOGRAMA EJECUTIVO

### **Q4 2024 (Oct-Dec)** - Fundación Sólida
**Objetivo**: RIAMP completa y operativa

### **Q1 2025 (Ene-Mar)** - Expansión RPMS  
**Objetivo**: Primera Infancia y sistema de indicadores

### **Q2 2025 (Abr-Jun)** - RPMS Completa
**Objetivo**: Todos los momentos del curso de vida

### **Q3 2025 (Jul-Sep)** - Optimización y Avanzadas
**Objetivo**: Dashboard avanzado, reportería e integraciones

---

## 🚀 FASE 1: Completar RIAMP (Q4 2024)
**Duración**: 12 semanas  
**Prioridad**: CRÍTICA

### **Hito 1.1: Control Prenatal Completo** ⏱️ 4 semanas
**Objetivo**: Implementar 100% de campos requeridos por Resolución 3280

#### **Semana 1-2: Modelado de Datos**
- [ ] **Agregar 47 campos faltantes** según Resolución 3280
  - Escala Herrera-Hurtado completa (riesgo biopsicosocial)
  - Todos los paraclínicos obligatorios (hemograma, glicemia, serología)
  - Signos vitales maternos por consulta
  - Factores de riesgo específicos por trimestre

- [ ] **Crear ENUMs específicos**:
  ```sql
  CREATE TYPE tipo_parto_enum AS ENUM ('VAGINAL', 'CESAREA', 'INSTRUMENTAL');
  CREATE TYPE riesgo_biopsicosocial_enum AS ENUM ('BAJO', 'MEDIO', 'ALTO');
  ```

- [ ] **Migración de base de datos**:
  ```bash
  supabase db diff -f complete_prenatal_care_resolution_3280
  ```

#### **Semana 3-4: Validaciones y Testing**
- [ ] **Validaciones por semana gestacional** en Pydantic models
- [ ] **20 tests unitarios** adicionales para nuevos campos  
- [ ] **5 tests de integración** para flujos completos
- [ ] **Documentación técnica** actualizada

**Entregables**:
- ✅ Modelo `DetalleControlPrenatal` 100% conforme Resolución 3280
- ✅ API endpoints con todas las validaciones
- ✅ Tests de cobertura 95%+

### **Hito 1.2: Atención del Parto Digital** ⏱️ 4 semanas
**Objetivo**: Partograma digital y registro completo del parto

#### **Semana 1-2: Partograma Digital**
- [ ] **Modelo de datos para partograma**:
  - Registro de dilatación cervical por hora
  - Frecuencia cardíaca fetal continua
  - Contracciones uterinas
  - Descenso fetal
  - Signos vitales maternos

- [ ] **Frontend especializado**:
  - Componente gráfico para partograma
  - Alertas automáticas por desviaciones
  - Timer automático para controles

#### **Semana 3-4: Protocolos de Parto**
- [ ] **Manejo activo del alumbramiento**
- [ ] **Registro de complicaciones** según clasificación CIE-10
- [ ] **Contacto piel a piel** y lactancia temprana
- [ ] **Integración con recién nacido** (polimorfismo)

**Entregables**:
- ✅ Partograma digital funcional
- ✅ Protocolos automatizados de parto
- ✅ Integración madre-recién nacido

### **Hito 1.3: Recién Nacido Completo** ⏱️ 2 semanas  
**Objetivo**: Protocolos neonatales según normativa

#### **Implementaciones Críticas**:
- [ ] **Reanimación neonatal**: Protocolo paso a paso
- [ ] **Profilaxis obligatorias**: Oftálmica y vitamina K  
- [ ] **Tamizaje neonatal**: TSH, audición, cardiopatías
- [ ] **Antropometría completa**: Peso, talla, perímetro cefálico
- [ ] **Apgar automatizado**: Cálculo y registro

### **Hito 1.4: Puerperio y Seguimiento** ⏱️ 2 semanas
**Objetivo**: Seguimiento completo posparto

#### **Implementaciones**:  
- [ ] **Control puerperal temprano** (3-8 días)
- [ ] **Control puerperal tardío** (15-45 días)  
- [ ] **Tamizaje depresión posparto** (Escala Edimburgo)
- [ ] **Anticoncepción posparto** integrada
- [ ] **Lactancia materna** seguimiento y apoyo

**🎯 Resultado Fase 1**: RIAMP 100% operativa y conforme a Resolución 3280

---

## 🌟 FASE 2: RPMS Primera Infancia + Indicadores (Q1 2025)
**Duración**: 12 semanas  
**Prioridad**: ALTA

### **Hito 2.1: RPMS Primera Infancia (0-5 años)** ⏱️ 8 semanas

#### **Semana 1-3: Modelado Primera Infancia**
- [ ] **Valoración del desarrollo** según escalas validadas:
  - Escala Abreviada de Desarrollo (EAD-3)  
  - Tamizaje de desarrollo (ASQ-3)
  - Evaluación nutricional (curvas OMS)

- [ ] **Sistema de alertas por edad**:
  ```python
  # Ejemplo: alertas automáticas por hitos perdidos
  if edad_meses == 12 and not camina_solo:
      crear_alerta("Retraso motor - derivar pediatría especializada")
  ```

#### **Semana 4-6: Esquema de Vacunación**
- [ ] **Calendario nacional de vacunación** integrado
- [ ] **Alertas automáticas** por esquema incompleto
- [ ] **Contraindicaciones** y aplazamientos
- [ ] **Reacciones adversas** registro y seguimiento

#### **Semana 7-8: Detección Temprana**  
- [ ] **Tamizaje visual** (Hirschberg, cubrir-descubrir)
- [ ] **Tamizaje auditivo** (otoemisiones acústicas)
- [ ] **Salud oral** (higiene, caries, maloclusiones)
- [ ] **Crecimiento y desarrollo** seguimiento longitudinal

### **Hito 2.2: Sistema de Indicadores** ⏱️ 4 semanas

#### **Indicadores RIAMP Automatizados**:
- [ ] **Razón de Mortalidad Materna** (por 100,000 nv)
- [ ] **Tasa mortalidad neonatal** (por 1,000 nv)  
- [ ] **% gestantes con 4+ controles** prenatales
- [ ] **% partos institucionales**
- [ ] **Tasa sífilis congénita** (por 1,000 nv)

#### **Dashboard Ejecutivo**:
- [ ] **Visualización en tiempo real** de todos los indicadores
- [ ] **Alertas por metas** no cumplidas
- [ ] **Reportes automatizados** mensuales/trimestrales
- [ ] **Exportación** a formatos requeridos por entes de control

**🎯 Resultado Fase 2**: RPMS Primera Infancia + Sistema de indicadores operativo

---

## 📈 FASE 3: RPMS Completa (Q2 2025)  
**Duración**: 12 semanas
**Prioridad**: ALTA

### **Distribución por Momento del Curso de Vida**:

#### **Hito 3.1: Infancia (6-11 años)** ⏱️ 2 semanas
- Valoración nutricional y crecimiento
- Tamizaje visual y auditivo  
- Salud oral y prevención
- Detección temprana de problemas de aprendizaje

#### **Hito 3.2: Adolescencia (12-17 años)** ⏱️ 3 semanas  
- Atención integral del adolescente
- Salud sexual y reproductiva
- Detección consumo de sustancias
- Salud mental y prevención suicidio

#### **Hito 3.3: Juventud (18-28 años)** ⏱️ 2 semanas
- Planificación familiar
- Tamizaje cáncer cuello uterino  
- Detección factores riesgo cardiovascular
- Promoción estilos de vida saludable

#### **Hito 3.4: Adultez (29-59 años)** ⏱️ 3 semanas
- Tamizajes oncológicos (mama, próstata, colon)
- Control enfermedades crónicas (diabetes, hipertensión)
- Salud ocupacional  
- Climaterio y menopausia

#### **Hito 3.5: Vejez (60+ años)** ⏱️ 2 semanas
- Valoración integral adulto mayor
- Detección deterioro cognitivo
- Prevención caídas
- Cuidado paliativo

**🎯 Resultado Fase 3**: RPMS 100% implementada para todos los momentos del curso de vida

---

## 🚀 FASE 4: Funcionalidades Avanzadas (Q3 2025)
**Duración**: 12 semanas  
**Prioridad**: MEDIA-ALTA

### **Hito 4.1: Dashboard y Reportería Avanzada** ⏱️ 4 semanas
- **Business Intelligence** integrado
- **Predicción de riesgos** con ML básico  
- **Mapas de calor** por territorio
- **Reportes ejecutivos** automatizados

### **Hito 4.2: Integraciones** ⏱️ 4 semanas  
- **RIPS automáticos** hacia ADRES
- **Historia clínica unificada** (estándar HL7)
- **APIs públicas** para terceros autorizados
- **Sincronización SIVIGILA** para eventos de notificación

### **Hito 4.3: Funcionalidades Premium** ⏱️ 4 semanas
- **Telemedicina básica** para seguimientos
- **App móvil** para pacientes (citas, resultados)
- **Sistema de agendamiento** inteligente
- **Notificaciones automáticas** (SMS, email, WhatsApp)

**🎯 Resultado Fase 4**: Sistema completo, integrado y con capacidades avanzadas

---

## 📋 CRITERIOS DE ÉXITO POR FASE

### **Fase 1 (RIAMP Completa)**
- [ ] ✅ 100% campos Resolución 3280 implementados
- [ ] ✅ 95% cobertura de tests automatizados  
- [ ] ✅ 15 indicadores RIAMP calculándose automáticamente
- [ ] ✅ 0 errores críticos en producción
- [ ] ✅ Tiempo respuesta API < 200ms

### **Fase 2 (RPMS + Indicadores)**  
- [ ] ✅ Primera Infancia 100% operativa
- [ ] ✅ Dashboard indicadores en tiempo real
- [ ] ✅ Reportes automatizados funcionando
- [ ] ✅ Sistema alertas por edad implementado

### **Fase 3 (RPMS Completa)**
- [ ] ✅ 6 momentos curso de vida implementados
- [ ] ✅ 50+ indicadores RPMS automatizados
- [ ] ✅ Seguimiento longitudinal operativo
- [ ] ✅ Performance < 500ms para consultas complejas

### **Fase 4 (Avanzadas)**
- [ ] ✅ Integraciones RIPS y ADRES operativas
- [ ] ✅ Dashboard BI funcional
- [ ] ✅ APIs públicas documentadas
- [ ] ✅ Sistema escalable para >10,000 pacientes

---

## ⚠️ RIESGOS Y MITIGATION  

### **Riesgo Alto: Complejidad Normativa**
- **Mitigation**: Revisión constante contra Resolución 3280
- **Checkpoint**: Validación semanal de conformidad

### **Riesgo Medio: Performance Base de Datos**  
- **Mitigation**: Optimización continua y monitoreo
- **Checkpoint**: Pruebas de carga mensuales

### **Riesgo Bajo: Cambios en Normativa**
- **Mitigation**: Arquitectura flexible y modular
- **Checkpoint**: Review trimestral de actualizaciones normativas

---

## 🎯 MÉTRICAS DE SEGUIMIENTO

### **Desarrollo**
- **Velocity**: Story points por sprint
- **Quality**: Defects por 1000 lines of code  
- **Coverage**: % tests automatizados
- **Performance**: Response time APIs

### **Negocio**  
- **Compliance**: % Resolución 3280 implementado
- **Efficiency**: Tiempo promedio de registro de atención
- **Quality**: % datos completos por atención
- **Impact**: Indicadores de salud mejorados

---

**Próxima revisión**: Final de cada fase  
**Owner**: Equipo Principal de Desarrollo  
**Aprobación**: Stakeholders IPS Santa Helena del Valle

---

*Esta hoja de ruta es un documento vivo que se actualiza según el progreso del proyecto y cambios en requerimientos normativos.*