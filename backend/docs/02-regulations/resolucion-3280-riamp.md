# 🤱 RIAMP - Ruta Integral Atención Materno Perinatal

**📋 Base Normativa:** Resolución 3280 de 2018 - Artículo 4  
**🎯 Propósito:** Atención integral población materno-perinatal  
**📊 Estado Implementación:** 40% completado (estructura + modelos)

---

## 🏗️ **ARQUITECTURA POLIMÓRFICA ANIDADA**

### **📊 Estructura Implementada ✅**
```
atencion_materno_perinatal (Tabla Principal)
├── sub_tipo_atencion (Discriminador Nivel 2)
├── sub_detalle_id (Referencia Polimórfica Nivel 2)
└── Tablas de Sub-Detalle:
    ├── detalle_control_prenatal ✅
    ├── detalle_parto ✅  
    ├── detalle_recien_nacido ✅
    └── detalle_puerperio ✅
```

### **🔄 Patrón Polimórfico de 3 Niveles**
```
1. atenciones (General)
   ├── detalle_id → atencion_materno_perinatal
   
2. atencion_materno_perinatal (Especializada)
   ├── sub_detalle_id → detalle_control_prenatal
   ├── sub_detalle_id → detalle_parto
   ├── sub_detalle_id → detalle_recien_nacido
   └── sub_detalle_id → detalle_puerperio

3. Detalles Específicos (Ultra-Especializados)
   └── Campos granulares por tipo atención
```

---

## 📋 **COMPONENTES POR MOMENTO ATENCIÓN**

### **🤰 4.1 - Control Prenatal ✅ ESTRUCTURA COMPLETA**
```
ESTADO: ✅ Modelos y BD implementados
LÓGICA: ⏸️ Pendiente implementar

MODELO: detalle_control_prenatal
CAMPOS CRÍTICOS:
✅ semana_gestacional (4-42)
✅ peso_materno_kg 
✅ talla_materna_cm
✅ presion_arterial_sistolica/diastolica
✅ frecuencia_cardiaca_fetal
✅ altura_uterina_cm
✅ presentacion_fetal
✅ movimientos_fetales
✅ edemas_patologicos
✅ proteinuria_resultado
✅ bacteriuria_resultado  
✅ hemoglobina_resultado
✅ glucemia_resultado
✅ serologia_sifilis
✅ vih_resultado
✅ toxoplasma_resultado

CÁLCULOS AUTOMÁTICOS REQUERIDOS:
📋 imc_pregestacional
📋 ganancia_peso_recomendada
📋 edad_gestacional_confiable
📋 riesgo_obstetrico_integral
📋 categoria_riesgo (Bajo/Moderado/Alto)
📋 proxima_consulta_dias
📋 examenes_faltantes[]
```

### **👶 4.2 - Atención del Parto ✅ ESTRUCTURA COMPLETA**
```
ESTADO: ✅ Modelos y BD implementados  
LÓGICA: ⏸️ Pendiente implementar

MODELO: detalle_parto
CAMPOS CRÍTICOS:
✅ fecha_parto
✅ edad_gestacional_parto (semanas)
✅ tipo_parto (Vaginal/Cesárea/Instrumental)
✅ indicacion_cesarea
✅ duracion_trabajo_parto_horas
✅ presentacion_fetal
✅ peso_recien_nacido_gramos
✅ talla_recien_nacido_cm  
✅ apgar_1_minuto/5_minutos
✅ reanimacion_requerida
✅ complicaciones_maternas
✅ complicaciones_neonatales
✅ alumbramiento_completo
✅ revision_canal_parto
✅ perdida_sanguinea_ml

CÁLCULOS AUTOMÁTICOS REQUERIDOS:
📋 clasificacion_peso_rn (PEG/AEG/GEG)
📋 indice_apgar_categorizado
📋 riesgo_complicaciones
📋 necesidad_uci_neonatal
📋 duracion_hospitalizacion_estimada
```

### **👶 4.3 - Atención Recién Nacido ✅ ESTRUCTURA COMPLETA**
```
ESTADO: ✅ Modelos y BD implementados
LÓGICA: ⏸️ Pendiente implementar

MODELO: detalle_recien_nacido  
CAMPOS CRÍTICOS:
✅ fecha_nacimiento
✅ peso_nacimiento_gramos (500-6000)
✅ talla_nacimiento_cm (25-60)
✅ perimetro_cefalico_cm
✅ edad_gestacional_semanas
✅ apgar_1_minuto/5_minutos (0-10)
✅ reanimacion_requerida
✅ malformaciones_congenitas
✅ tamizaje_auditivo_realizado
✅ tamizaje_visual_realizado
✅ tamizaje_cardiaco_realizado
✅ vacuna_bcg_aplicada
✅ vacuna_hepatitis_b_aplicada
✅ vitamina_k_aplicada
✅ inicio_lactancia_materna
✅ tipo_alimentacion_egreso

CÁLCULOS AUTOMÁTICOS REQUERIDOS:
📋 clasificacion_peso_edad_gestacional
📋 percentil_peso_edad_gestacional
📋 percentil_talla_edad_gestacional
📋 percentil_perimetro_cefalico
📋 riesgo_nutricional_neonatal
📋 completitud_tamizajes_obligatorios
📋 adherencia_lactancia_materna
```

### **🤱 4.4 - Control Puerperio ✅ ESTRUCTURA COMPLETA**
```
ESTADO: ✅ Modelos y BD implementados
LÓGICA: ⏸️ Pendiente implementar

MODELO: detalle_puerperio
CAMPOS CRÍTICOS:
✅ fecha_control (post-parto)
✅ dia_puerperio (1-42 días)
✅ tipo_puerperio (Inmediato/Mediato/Tardío)
✅ involusion_uterina_adecuada
✅ caracteristicas_loquios
✅ cicatrizacion_episiotomia/cesarea
✅ dolor_nivel (0-10)
✅ lactancia_materna_exclusiva
✅ dificultades_lactancia
✅ estado_emocional
✅ tamizaje_depresion_postparto (Edinburgh)
✅ reanudacion_actividad_sexual
✅ metodo_planificacion_familiar
✅ signos_alarma_identificados

CÁLCULOS AUTOMÁTICOS REQUERIDOS:
📋 evolucion_puerperio_normal
📋 riesgo_depresion_postparto
📋 adherencia_lactancia_exclusiva
📋 necesidad_interconsulta_especializada
📋 proxima_consulta_recomendada
📋 completitud_educacion_materna
```

---

## 🎯 **ANÁLISIS DE IMPLEMENTACIÓN TÉCNICA**

### **✅ FORTALEZAS ACTUALES**

1. **🏗️ ARQUITECTURA SÓLIDA**
   ```
   ✅ Polimorfismo anidado funcional
   ✅ 4 modelos especializados completos
   ✅ Migraciones BD aplicadas exitosamente
   ✅ RLS policies configuradas
   ✅ Campos granulares según Resolución 3280
   ```

2. **📊 ESTRUCTURA DE DATOS EXHAUSTIVA**
   ```
   ✅ 50+ campos específicos por componente
   ✅ Validaciones según estándares médicos
   ✅ ENUMs para valores estandarizados
   ✅ Constraints de integridad referencial
   ✅ Audit trails automáticos
   ```

### **⚠️ GAPS CRÍTICOS**

1. **🔄 LÓGICA DE NEGOCIO AUSENTE**
   ```
   ❌ Sin cálculos obstétricos automáticos
   ❌ Sin validaciones médicas específicas
   ❌ Sin alertas riesgo materno-perinatal
   ❌ Sin seguimiento longitudinal embarazo
   ```

2. **📋 INSTRUMENTOS ANEXOS NO FUNCIONALES**
   ```
   ANEXOS REQUERIDOS:
   📋 Escala Riesgo Herrera y Hurtado
   📋 Escala Depresión Postnatal Edinburgh (EPDS)
   📋 Escala Obstétrica Alerta Temprana
   📋 Evaluación Nutricional Atalah
   📋 Evaluación Técnica Lactancia
   
   ESTADO ACTUAL: Documentos estáticos, no formularios funcionales
   ```

3. **🚨 ALERTAS Y PROTOCOLOS AUSENTES**
   ```
   CRÍTICOS FALTANTES:
   ❌ Detección automática embarazo alto riesgo
   ❌ Alertas trabajo parto prematuro  
   ❌ Protocolo emergencia obstétrica
   ❌ Seguimiento curvas crecimiento fetal
   ❌ Detección factores riesgo tromboembólico
   ```

---

## 🚀 **ROADMAP RIAMP COMPLETO**

### **📋 FASE A - Lógica Control Prenatal (Prioridad Alta)**
```
⏱️  ESTIMADO: 3-4 semanas
📊 COMPLEJIDAD: Alta (cálculos obstétricos complejos)

TASKS:
1. Implementar cálculos IMC pregestacional
2. Algoritmo ganancia peso Atalah
3. Cálculo edad gestacional confiable (FUM vs Eco)
4. Score riesgo obstétrico automático
5. Alertas valores fuera rango normal
6. Protocolo solicitud exámenes según semana
7. Seguimiento curvas crecimiento fetal
8. Detección factores riesgo tromboembólico

ENDPOINTS NUEVOS:
✅ POST /materno-perinatal/control-prenatal/
✅ PUT /materno-perinatal/control-prenatal/{id}
✅ GET /materno-perinatal/control-prenatal/{id}/riesgo
✅ GET /materno-perinatal/control-prenatal/{id}/examenes-pendientes
✅ POST /materno-perinatal/control-prenatal/{id}/alertas
```

### **📋 FASE B - Instrumentos Anexos Funcionales (Prioridad Alta)**
```
⏱️  ESTIMADO: 2-3 semanas  
📊 COMPLEJIDAD: Media (formularios dinámicos)

TASKS:
1. Escala Herrera y Hurtado como formulario React
2. EPDS (Edinburgh) automatizada con scoring
3. Escala Alerta Obstétrica con alertas automáticas
4. Evaluación Atalah gráfica interactiva
5. Checklist técnica lactancia con scoring
6. Integración anexos con atenciones específicas

NUEVOS MODELOS:
✅ herrera_hurtado_evaluation
✅ edinburgh_depression_scale
✅ obstetric_early_warning_scale
✅ atalah_nutritional_evaluation
✅ breastfeeding_technique_evaluation
```

### **📋 FASE C - Atención Parto y RN (Prioridad Media)**
```
⏱️  ESTIMADO: 2-3 semanas
📊 COMPLEJIDAD: Alta (protocolos emergencia)

TASKS:
1. Calculadora Apgar automática
2. Clasificación peso/edad gestacional automática
3. Protocolo reanimación neonatal
4. Alertas complicaciones maternas
5. Cálculo perdida sanguínea estimada
6. Seguimiento transición feto-neonatal
7. Protocolos UCI neonatal

CÁLCULOS CRÍTICOS:
✅ percentiles_crecimiento_fetal
✅ clasificacion_peso_edad_gestacional  
✅ score_apgar_categorizado
✅ riesgo_complicaciones_parto
✅ necesidad_cuidados_especiales
```

### **📋 FASE D - Puerperio y Seguimiento (Prioridad Media)**
```
⏱️  ESTIMADO: 2 semanas
📊 COMPLEJIDAD: Media

TASKS:
1. Seguimiento involución uterina
2. Evaluación automática lactancia
3. Detección depresión postparto (Edinburgh)
4. Alertas complicaciones puerperales
5. Planificación familiar automática
6. Educación maternal personalizada

MÉTRICAS AUTOMÁTICAS:
✅ evolucion_puerperio_score
✅ riesgo_depresion_postparto
✅ success_rate_lactancia_exclusiva
✅ adherencia_controles_programados
```

### **📋 FASE E - Reportería y Analytics (Prioridad Baja)**
```
⏱️  ESTIMADO: 1-2 semanas
📊 COMPLEJIDAD: Media

TASKS:
1. Dashboard morbi-mortalidad materna
2. Indicadores calidad atención obstétrica  
3. Reportes SISPRO materno-perinatal
4. Analytics outcomes neonatales
5. Métricas adherencia protocolos

REPORTES AUTOMÁTICOS:
✅ mortalidad_materna_evitable
✅ morbilidad_materna_extrema  
✅ outcomes_neonatales_adversos
✅ indicadores_calidad_atencion
```

---

## 📊 **COMPLIANCE CRÍTICO**

### **⚖️ Artículos Resolución 3280 - RIAMP**

| Artículo | Componente | Estado Técnico | Compliance % |
|----------|------------|----------------|--------------|
| **Art. 4.1.1** | Atención Preconcepcional | ⏸️ No implementado | 0% |
| **Art. 4.1.2** | Control Prenatal | 🔄 Estructura 100%, lógica 0% | 30% |
| **Art. 4.2** | Atención Parto | 🔄 Estructura 100%, lógica 0% | 30% |
| **Art. 4.3** | Atención RN | 🔄 Estructura 100%, lógica 0% | 30% |
| **Art. 4.4** | Control Puerperio | 🔄 Estructura 100%, lógica 0% | 30% |
| **Anexos 1-11** | Instrumentos Técnicos | ⏸️ Estáticos, no funcionales | 10% |

### **🎯 META COMPLIANCE RIAMP**
```
ACTUAL: 40% (estructura + modelos)
META Q4 2024: 90% (lógica + instrumentos + reportería)
CRÍTICO: Anexos funcionales (obligatorios auditoría)
```

---

## 📖 **Referencias Técnicas**

- **[Artículos Resolución](./resolucion-3280-articles.md)** - Marco normativo RIAMP
- **[Anexos Técnicos](./resolucion-3280-annexes/)** - Instrumentos evaluación  
- **[RPMS Complemento](./resolucion-3280-rpms.md)** - Integración momentos vida
- **[Estado Proyecto](../../PROJECT-STATUS.md)** - Progreso técnico actual

---

*🤱 Documento técnico especializado RIAMP. Para implementación prioritaria de lógica obstétrica automática consultar roadmap detallado.*