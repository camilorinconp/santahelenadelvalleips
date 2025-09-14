# 📚 Lecciones Aprendidas - Frontend Médico

**📅 Migrado desde:** DEV_LOG_FRONTEND.md  
**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Mejores prácticas críticas desarrollo frontend médico  
**📍 Audiencia:** Frontend Developers, Team Leads  

---

## 🎯 **Filosofía Lecciones Aprendidas**

> **"Cada error en desarrollo médico se convierte en aprendizaje que previene errores clínicos"**

### **📋 Principios:**
1. **Medical-First Development:** Errores de código pueden impactar vidas humanas
2. **Documentation-Driven:** Cada problema documentado previene repetición  
3. **Team Knowledge Sharing:** Conocimiento debe ser transferible instantáneamente
4. **Continuous Improvement:** Cada sprint mejora quality assurance

---

## 🏗️ **Lecciones Arquitectura React**

### **📅 2025-09-10: Estructura Monorepo Establecida**

**🎯 Objetivo:** Establecer base proyecto frontend según arquitectura aprobada.

#### **✅ Decisiones Exitosas:**
1. **Monorepo Structure:**
   ```
   proyecto_salud/
   ├── backend/        # FastAPI + PostgreSQL
   ├── frontend/       # React + TypeScript  
   └── supabase/       # Database management
   ```

2. **Create React App:** Decisión correcta para bootstrap rápido
   - TypeScript out-of-the-box
   - Hot reloading funcional
   - Testing setup automático
   - Build optimization incluida

3. **Separación Clara:** Backend y Frontend completamente independientes
   - Permite desarrollo paralelo
   - Deploy independiente futuro
   - Testing aislado por stack

#### **📚 Aprendizajes Clave:**
- **Monorepo Benefits:** Shared configuration, consistent tooling, easier CI/CD
- **CRA Limitations:** Ejecting costs vs. benefits debe evaluarse temprano
- **Documentation Structure:** README específico por stack + README general

#### **🔄 Aplicación Futura:**
- Mantener separación clara backend/frontend en todos los features
- Documentar decisiones arquitectónicas en tiempo real
- Setup inicial debe incluir todas las herramientas core desde día 1

---

## 📦 **Lecciones Dependencies Management**

### **📅 2025-09-10: Stack Tecnológico Core**

**🎯 Objetivo:** Instalar dependencies principales React ecosystem médico.

#### **✅ Stack Final Exitoso:**
```json
{
  "core": {
    "react": "19.1.1",
    "typescript": "4.9.5"
  },
  "ui": {
    "@mui/material": "7.3.2",        // Design system médico
    "@emotion/react": "11.x",        // MUI dependency
    "@emotion/styled": "11.x"        // MUI dependency
  },
  "state": {
    "@tanstack/react-query": "5.87.4", // Server state management
    "react-hook-form": "7.62.0",       // Form state
    "zod": "4.1.5"                     // Validation schemas
  },
  "routing": {
    "react-router-dom": "7.8.2"      // SPA routing
  },
  "http": {
    "axios": "1.11.0"                 // API client
  }
}
```

#### **📚 Aprendizajes Críticos:**
1. **Material-UI Ecosystem:** Requires specific peer dependencies
   - @emotion packages are mandatory, not optional
   - Version compatibility critical for medical apps stability

2. **React Query vs. Redux:** RQ mejor para medical app
   - Built-in caching for server data
   - Optimistic updates out-of-the-box
   - Less boilerplate for API integration
   - Better DevTools for debugging API calls

3. **Form Libraries Comparison:**
   - **React Hook Form + Zod > Formik + Yup**
   - Better TypeScript integration
   - Performance superior for large medical forms
   - Schema validation más robusta para compliance

#### **❌ Errores Evitados:**
- **Not choosing Redux:** Overkill para medical forms, RQ + useState sufficient
- **Not using Zod:** Runtime validation crítico para medical data integrity
- **Version mismatches:** Lock all versions desde inicio para reproducibilidad

#### **🔄 Aplicación Futura:**
- Lock dependency versions desde día 1 en medical projects
- Document WHY each dependency was chosen, not just what
- Test dependency updates in isolated branch before merge

---

## 🚀 **Lecciones Desarrollo CRUD Pacientes**

### **📅 2025-09-10: CRUD Pacientes Implementado**

**🎯 Objetivo:** Implementar funcionalidad CRUD completa para gestión pacientes.

#### **✅ Implementación Exitosa:**

**1. Listar Pacientes:**
```typescript
// Pattern exitoso: DataGrid + useQuery
const PacientesPage = () => {
  const { data: pacientes, isLoading, error } = useQuery({
    queryKey: ['pacientes'],
    queryFn: getPacientesAPI,
    staleTime: 5 * 60 * 1000 // 5 min cache para medical data
  });

  return (
    <DataGrid 
      rows={pacientes || []}
      loading={isLoading}
      columns={pacientesColumns}
      onRowClick={(params) => navigate(`/pacientes/${params.id}`)}
    />
  );
};
```

**2. Crear Pacientes:**
```typescript
// Pattern exitoso: React Hook Form + Zod + useMutation
const PacienteForm = () => {
  const form = useForm({
    resolver: zodResolver(pacienteSchema),
    mode: 'onChange' // Real-time validation for medical forms
  });
  
  const createMutation = useMutation({
    mutationFn: createPacienteAPI,
    onSuccess: () => {
      queryClient.invalidateQueries(['pacientes']);
      toast.success('Paciente creado exitosamente');
      navigate('/pacientes');
    }
  });

  return (
    <form onSubmit={form.handleSubmit(createMutation.mutate)}>
      {/* Form fields with real-time validation */}
    </form>
  );
};
```

**3. Eliminar Pacientes:**
```typescript
// Pattern exitoso: Confirmation dialog + optimistic updates
const useDeletePaciente = () => {
  return useMutation({
    mutationFn: deletePacienteAPI,
    onMutate: async (pacienteId) => {
      await queryClient.cancelQueries(['pacientes']);
      
      const previousPacientes = queryClient.getQueryData(['pacientes']);
      
      // Optimistic update
      queryClient.setQueryData(['pacientes'], old => 
        old?.filter(p => p.id !== pacienteId)
      );
      
      return { previousPacientes };
    },
    onError: (err, pacienteId, context) => {
      // Rollback on error
      queryClient.setQueryData(['pacientes'], context?.previousPacientes);
    }
  });
};
```

#### **📚 Aprendizajes Críticos:**

**1. React Query Cache Strategy:**
```typescript
// Medical data requires specific cache strategy
const medicalCacheConfig = {
  pacientes: {
    staleTime: 5 * 60 * 1000,     // 5 min - patient data freshness
    cacheTime: 10 * 60 * 1000,    // 10 min - keep in memory
    refetchOnWindowFocus: true    // Refresh on tab switch (important for medical)
  }
};
```

**2. Form Validation Medical-Specific:**
```typescript
// Colombian medical validation patterns
const colombianDocumentSchema = z
  .string()
  .regex(/^\d{6,12}$/, 'Documento debe ser 6-12 dígitos')
  .refine(val => !val.startsWith('0'), 'No puede empezar con 0');

const colombianPhoneSchema = z
  .string()
  .regex(/^3\d{9}$/, 'Teléfono debe ser formato colombiano: 3XXXXXXXXX')
  .optional();
```

**3. Error Handling Medical Context:**
```typescript
// Medical-specific error handling
const handleMedicalError = (error: AxiosError) => {
  if (error.response?.status === 422) {
    // Validation errors - show field-specific feedback
    const validationErrors = error.response.data.detail;
    Object.entries(validationErrors).forEach(([field, message]) => {
      form.setError(field, { message });
    });
  } else if (error.response?.status === 409) {
    // Duplicate patient - medical compliance issue
    toast.error('Paciente ya existe en el sistema');
  } else {
    // Generic medical system error
    toast.error('Error en sistema médico. Contacte soporte.');
  }
};
```

#### **🔴 Problemas Identificados y Soluciones:**

**1. Edición Pacientes - Persistencia Backend:**
```typescript
// ❌ Problema: Datos no se persistían correctamente
// ✅ Solución: Verificar payload format exacto

// Before (problematic)
const updateData = { ...formData };

// After (working)  
const updateData = {
  ...formData,
  // Ensure null handling for optional fields
  segundo_nombre: formData.segundo_nombre || null,
  segundo_apellido: formData.segundo_apellido || null
};
```

**2. Advertencias React Input Null Values:**
```typescript
// ❌ Problema: Warning "value prop should not be null"
// ✅ Solución: Convert null to empty string for controlled inputs

// Before (warning)
<TextField value={data?.segundo_nombre} />

// After (no warning)
<TextField value={data?.segundo_nombre || ''} />

// Or better: use defaultValues in useForm
const form = useForm({
  defaultValues: {
    segundo_nombre: '',  // Empty string instead of undefined
    segundo_apellido: ''
  }
});
```

#### **🔄 Aplicación Futura:**
- **Always handle null values** en forms médicos explícitamente
- **Cache strategy** debe ser medical-data aware (freshness crítica)
- **Error handling** debe ser medical-context specific 
- **Optimistic updates** críticos para UX en workflows urgentes médicos

---

## 🎨 **Lecciones UI/UX Médico**

### **🏥 Material-UI Medical Theming**

#### **✅ Patrones Exitosos:**
```typescript
// Medical theme customization
const medicalTheme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',        // Medical blue - trust and reliability
    },
    secondary: {
      main: '#388e3c',        // Medical green - health and success
    },
    error: {
      main: '#d32f2f',        // Critical medical alerts
    }
  },
  typography: {
    // Medical forms need larger, more readable text
    fontSize: 16,             // Base 16px instead of 14px
    h6: {
      fontSize: '1.1rem',     // Form section headers
      fontWeight: 600
    }
  },
  components: {
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',   // Better visual separation for medical forms
        margin: 'normal',      // Consistent spacing
        fullWidth: true        // Full width default para forms médicos
      }
    }
  }
});
```

#### **📚 Lecciones UX Medical:**
1. **Larger touch targets** para tablets médicas (44px minimum)
2. **High contrast** necesario para diferentes condiciones lighting médico
3. **Clear visual hierarchy** - información crítica debe destacar inmediatamente
4. **Consistent spacing** reduce cognitive load para profesionales médicos

---

## ⚠️ **Anti-Patterns Identificados**

### **❌ Evitar en Proyectos Médicos:**

**1. Client-Side Medical Data Storage:**
```typescript
// ❌ NEVER store medical data in localStorage
localStorage.setItem('currentPatient', JSON.stringify(patient));

// ✅ Use React Query cache with proper expiration
queryClient.setQueryData(['paciente', id], patient, {
  staleTime: 5 * 60 * 1000
});
```

**2. Optimistic Updates Without Rollback:**
```typescript
// ❌ NEVER optimistic update without error rollback in medical apps
const updatePaciente = useMutation({
  mutationFn: updatePacienteAPI,
  onMutate: (newData) => {
    queryClient.setQueryData(['paciente', id], newData);
    // Missing rollback strategy - DANGEROUS in medical context
  }
});

// ✅ Always implement rollback for medical data
// (Ver ejemplos arriba en sección CRUD)
```

**3. Silent Error Handling:**
```typescript
// ❌ NEVER silently fail in medical applications
try {
  await createPacienteAPI(data);
} catch (error) {
  console.log('Error:', error); // Silent failure - DANGEROUS
}

// ✅ Always surface medical errors to user
try {
  await createPacienteAPI(data);
} catch (error) {
  handleMedicalError(error);
  toast.error('Error crítico: Paciente no fue guardado');
}
```

---

## 🔄 **Métricas de Éxito Aprendizaje**

### **📊 KPIs Lecciones Aprendidas:**
- **Error Recurrence Rate:** 0% - No repetir errores documentados
- **Setup Time New Developer:** <15 min usando setup guide
- **Code Review Findings:** <2 architecture issues per PR
- **Medical Validation Coverage:** 100% campos críticos validados

### **✅ Checklist Nueva Feature:**
- [ ] Error handling medical-specific implementado
- [ ] Null value handling en all form fields
- [ ] Cache strategy defined para medical data
- [ ] Optimistic updates con rollback strategy
- [ ] TypeScript types match backend Pydantic models
- [ ] Validation schemas mirror backend exactly
- [ ] Testing includes medical edge cases
- [ ] Documentation updated con lessons learned

---

## 🎯 **Próximas Lecciones a Documentar**

### **📋 En Desarrollo:**
- **Polimorfismo UI:** Lessons desde formularios atención médica polimórficos
- **Performance Medical:** Bundle size optimization para tablets médicas  
- **Accessibility:** WCAG compliance específico para interfaces médicas
- **Testing Medical:** Patterns específicos para componentes médicos críticos

### **🔍 Areas to Monitor:**
- **Form Performance:** Large medical forms (>50 fields) optimization
- **Cache Invalidation:** Complex relationships patient/attention data
- **Real-time Updates:** WebSocket integration para updates críticos
- **Offline Support:** PWA features para tablets médicas sin conectividad

---

**📚 Estas lecciones evolucionan con cada feature implementado**  
**👥 Contributor Process:** Todo developer debe actualizar lessons learned en PRs  
**🎯 Objetivo:** Zero regression rate en errores médicos por desarrollo frontend