# 📊 State Management - React Query + Forms Strategy

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Estrategia completa manejo estado en aplicación médica  
**📍 Audiencia:** Developers React, Arquitectos Estado  

---

## 🎯 **Filosofía State Management Médico**

### **🏥 Principios Fundamentales:**
1. **Server State ≠ Client State:** Separación clara entre datos servidor vs. UI state
2. **Medical Data Reliability:** Cache strategies para datos críticos médicos
3. **Optimistic Updates:** Feedback inmediato para workflows urgentes
4. **Offline Resilience:** Degradación elegante sin conectividad
5. **Compliance Tracking:** Estado validation Resolución 3280 siempre actualizado

### **📋 Arquitectura Estado:**
```
┌─ Server State (React Query)
│  ├─ Pacientes (cache: 10min, background refresh)
│  ├─ Atenciones Médicas (cache: 5min, real-time updates)
│  ├─ Catálogos Normativos (cache: 1 hora, rarely changes)
│  └─ Métricas Dashboard (cache: 2min, frequent updates)
│
├─ Client State (useState/useReducer)
│  ├─ UI State (modals, tabs, loading states)
│  ├─ Navigation State (current page, breadcrumbs)
│  ├─ User Preferences (theme, language, layouts)
│  └─ Temporary Data (search filters, pagination)
│
└─ Form State (React Hook Form)
   ├─ Form Data (controlled by RHF)
   ├─ Validation State (real-time + submit validation)
   ├─ Error State (field errors + global errors)
   └─ Submission State (loading, success, error)
```

---

## ⚡ **React Query: Server State Strategy**

### **🏥 Medical Data Queries**

#### **Configuración Base React Query**
```typescript
// queryClient.ts - Configuración optimizada para datos médicos
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Medical data strategies
      staleTime: 5 * 60 * 1000,      // 5 min - fresh medical data
      cacheTime: 10 * 60 * 1000,     // 10 min - keep in memory
      retry: (failureCount, error) => {
        // Critical medical data: retry more aggressively
        if (error instanceof MedicalDataError) {
          return failureCount < 5;
        }
        return failureCount < 3;
      },
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000)
    },
    mutations: {
      retry: 1, // Medical actions: retry once only
      onError: (error) => {
        // Global error handling para datos médicos
        if (error instanceof ComplianceError) {
          showComplianceAlert(error.message);
        }
      }
    }
  }
});
```

#### **Hooks Especializados Pacientes**
```typescript
// hooks/usePacienteQueries.ts
interface UsePacientesQueryOptions {
  filters?: PacienteFilters;
  pagination?: PaginationOptions;
  realTimeUpdates?: boolean;
}

export const usePacientes = (options: UsePacientesQueryOptions = {}) => {
  return useQuery({
    queryKey: ['pacientes', options.filters, options.pagination],
    queryFn: () => getPacientesAPI(options),
    staleTime: 2 * 60 * 1000, // 2 min para listados
    
    // Background refresh para datos críticos
    refetchInterval: options.realTimeUpdates ? 30 * 1000 : false,
    refetchOnWindowFocus: true,
    refetchOnReconnect: true
  });
};

export const usePaciente = (pacienteId: string) => {
  return useQuery({
    queryKey: ['paciente', pacienteId],
    queryFn: () => getPacienteAPI(pacienteId),
    staleTime: 10 * 60 * 1000, // 10 min para datos individuales
    enabled: !!pacienteId,
    
    // Error handling específico
    onError: (error: Error) => {
      if (error.message.includes('not found')) {
        toast.error('Paciente no encontrado');
        // Redirect to patients list
      }
    }
  });
};

// Prefetching strategy para navegación rápida
export const usePrefetchPaciente = () => {
  const queryClient = useQueryClient();
  
  return useCallback((pacienteId: string) => {
    queryClient.prefetchQuery({
      queryKey: ['paciente', pacienteId],
      queryFn: () => getPacienteAPI(pacienteId),
      staleTime: 10 * 60 * 1000
    });
  }, [queryClient]);
};
```

#### **Hooks Atenciones Médicas Polimórficas**
```typescript
// hooks/useAtencionesQueries.ts
export const useAtencionesPolimorficas = (pacienteId: string) => {
  return useQuery({
    queryKey: ['atenciones', pacienteId],
    queryFn: () => getAtencionesAPI(pacienteId),
    staleTime: 5 * 60 * 1000,
    select: (data: AtencionBase[]) => {
      // Transform polymorphic data for UI consumption
      return data.map(atencion => ({
        ...atencion,
        detalleEspecifico: getDetalleEspecifico(atencion),
        complianceStatus: checkCompliance(atencion)
      }));
    }
  });
};

export const useCreateAtencionPolimorfica = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: AtencionCreatePolimorfica) => {
      // Two-step creation: detalle first, then atencion
      const detalle = await createDetalleEspecificoAPI(data.detalle, data.tipo);
      const atencion = await createAtencionAPI({
        ...data.atencionBase,
        detalle_id: detalle.id,
        tipo_atencion: data.tipo
      });
      return { atencion, detalle };
    },
    
    // Optimistic updates para feedback inmediato
    onMutate: async (newAtencion) => {
      await queryClient.cancelQueries(['atenciones', newAtencion.paciente_id]);
      
      const previousAtenciones = queryClient.getQueryData(['atenciones', newAtencion.paciente_id]);
      
      // Optimistically update
      queryClient.setQueryData(['atenciones', newAtencion.paciente_id], (old: AtencionBase[] = []) => [
        ...old,
        { ...newAtencion, id: 'temp-' + Date.now(), status: 'creating' }
      ]);
      
      return { previousAtenciones };
    },
    
    onError: (err, newAtencion, context) => {
      // Rollback on error
      queryClient.setQueryData(['atenciones', newAtencion.paciente_id], context?.previousAtenciones);
      toast.error('Error creando atención médica');
    },
    
    onSuccess: (data, variables) => {
      // Invalidate and refetch
      queryClient.invalidateQueries(['atenciones', variables.paciente_id]);
      queryClient.invalidateQueries(['paciente', variables.paciente_id]); // May affect patient summary
      
      toast.success('Atención médica guardada correctamente');
    }
  });
};
```

---

## 📝 **Form State: React Hook Form Strategy**

### **🏥 Medical Forms Architecture**

#### **Base Medical Form Hook**
```typescript
// hooks/useMedicalForm.ts
interface UseMedicalFormProps<T> {
  schema: ZodSchema<T>;
  defaultValues?: Partial<T>;
  complianceFields?: ComplianceField[];
  autoSave?: boolean;
  autoSaveInterval?: number;
}

export const useMedicalForm = <T extends Record<string, any>>({
  schema,
  defaultValues,
  complianceFields = [],
  autoSave = false,
  autoSaveInterval = 30000 // 30 seconds
}: UseMedicalFormProps<T>) => {
  const form = useForm<T>({
    resolver: zodResolver(schema),
    defaultValues,
    mode: 'onChange', // Real-time validation for medical forms
    criteriaMode: 'all' // Show all validation errors
  });
  
  // Compliance validation state
  const [complianceViolations, setComplianceViolations] = useState<ComplianceViolation[]>([]);
  
  // Watch for compliance validation
  const watchedData = form.watch();
  
  useEffect(() => {
    const violations = validateCompliance(watchedData, complianceFields);
    setComplianceViolations(violations);
  }, [watchedData, complianceFields]);
  
  // Auto-save functionality
  useEffect(() => {
    if (autoSave && form.formState.isDirty) {
      const timer = setInterval(() => {
        const data = form.getValues();
        if (form.formState.isValid) {
          autoSaveAPI(data);
        }
      }, autoSaveInterval);
      
      return () => clearInterval(timer);
    }
  }, [autoSave, autoSaveInterval, form]);
  
  const submitWithCompliance = form.handleSubmit((data) => {
    // Final compliance check before submit
    const finalViolations = validateCompliance(data, complianceFields);
    if (finalViolations.length > 0) {
      setComplianceViolations(finalViolations);
      throw new ComplianceError('Datos no cumplen Resolución 3280', finalViolations);
    }
    return data;
  });
  
  return {
    ...form,
    complianceViolations,
    isCompliant: complianceViolations.length === 0,
    submitWithCompliance
  };
};
```

#### **Polymorphic Form Management**
```typescript
// hooks/usePolymorphicForm.ts
interface UsePolymorphicFormProps {
  tipoAtencion: TipoAtencionRIAS;
  pacienteId: string;
  initialData?: Partial<AtencionPolimorfica>;
}

export const usePolymorphicForm = ({
  tipoAtencion,
  pacienteId,
  initialData
}: UsePolymorphicFormProps) => {
  // Get appropriate schema based on tipo
  const schema = useMemo(() => 
    getSchemaForTipoAtencion(tipoAtencion), [tipoAtencion]
  );
  
  const complianceFields = useMemo(() => 
    getComplianceFields(tipoAtencion), [tipoAtencion]
  );
  
  // Base form with medical form features
  const baseForm = useMedicalForm({
    schema,
    defaultValues: initialData,
    complianceFields,
    autoSave: true // Auto-save for long medical forms
  });
  
  // Mutation for polymorphic creation
  const createMutation = useCreateAtencionPolimorfica();
  
  const onSubmit = async (data: any) => {
    try {
      const structuredData = {
        tipo: tipoAtencion,
        paciente_id: pacienteId,
        atencionBase: extractAtencionBase(data),
        detalle: extractDetalleEspecifico(data, tipoAtencion)
      };
      
      await createMutation.mutateAsync(structuredData);
      
      // Reset form after successful creation
      baseForm.reset();
      
    } catch (error) {
      if (error instanceof ComplianceError) {
        // Handle compliance errors specifically
        setComplianceAlert(error.violations);
      } else {
        // Generic error handling
        toast.error('Error guardando atención médica');
      }
    }
  };
  
  return {
    ...baseForm,
    onSubmit: baseForm.submitWithCompliance(onSubmit),
    isSubmitting: createMutation.isLoading,
    tipoAtencion
  };
};
```

---

## 🌐 **Global State: Context + Reducers**

### **🏥 Medical App Context**

#### **App State Provider**
```typescript
// context/MedicalAppContext.tsx
interface MedicalAppState {
  currentPaciente?: Paciente;
  activeProfile: 'CLINICO' | 'CALL_CENTER';
  notifications: MedicalNotification[];
  complianceAlerts: ComplianceAlert[];
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
}

type MedicalAppAction = 
  | { type: 'SET_CURRENT_PACIENTE'; payload: Paciente }
  | { type: 'SWITCH_PROFILE'; payload: 'CLINICO' | 'CALL_CENTER' }
  | { type: 'ADD_NOTIFICATION'; payload: MedicalNotification }
  | { type: 'DISMISS_COMPLIANCE_ALERT'; payload: string }
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' };

const medicalAppReducer = (state: MedicalAppState, action: MedicalAppAction): MedicalAppState => {
  switch (action.type) {
    case 'SET_CURRENT_PACIENTE':
      return { ...state, currentPaciente: action.payload };
      
    case 'SWITCH_PROFILE':
      return { 
        ...state, 
        activeProfile: action.payload,
        // Clear profile-specific data when switching
        notifications: state.notifications.filter(n => n.profile === action.payload)
      };
      
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [action.payload, ...state.notifications].slice(0, 10) // Keep max 10
      };
      
    case 'DISMISS_COMPLIANCE_ALERT':
      return {
        ...state,
        complianceAlerts: state.complianceAlerts.filter(alert => alert.id !== action.payload)
      };
      
    default:
      return state;
  }
};

export const MedicalAppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(medicalAppReducer, {
    activeProfile: 'CLINICO',
    notifications: [],
    complianceAlerts: [],
    theme: 'light',
    sidebarOpen: true
  });
  
  // Persist profile preference
  useEffect(() => {
    localStorage.setItem('activeProfile', state.activeProfile);
  }, [state.activeProfile]);
  
  const contextValue = useMemo(() => ({
    state,
    dispatch,
    // Convenience methods
    setCurrentPaciente: (paciente: Paciente) => 
      dispatch({ type: 'SET_CURRENT_PACIENTE', payload: paciente }),
    switchProfile: (profile: 'CLINICO' | 'CALL_CENTER') => 
      dispatch({ type: 'SWITCH_PROFILE', payload: profile }),
    addNotification: (notification: MedicalNotification) => 
      dispatch({ type: 'ADD_NOTIFICATION', payload: notification }),
  }), [state]);
  
  return (
    <MedicalAppContext.Provider value={contextValue}>
      {children}
    </MedicalAppContext.Provider>
  );
};
```

---

## 🔄 **State Synchronization Patterns**

### **📊 Server ↔ Client Sync**

#### **Real-time Updates Hook**
```typescript
// hooks/useRealTimeSync.ts
export const useRealTimeSync = (entities: string[]) => {
  const queryClient = useQueryClient();
  
  useEffect(() => {
    // WebSocket or Server-Sent Events for real-time updates
    const eventSource = new EventSource('/api/sse/medical-updates');
    
    eventSource.onmessage = (event) => {
      const update: MedicalUpdate = JSON.parse(event.data);
      
      // Invalidate relevant queries based on update type
      switch (update.type) {
        case 'PACIENTE_UPDATED':
          queryClient.invalidateQueries(['paciente', update.pacienteId]);
          queryClient.invalidateQueries(['atenciones', update.pacienteId]);
          break;
          
        case 'NUEVA_ATENCION':
          queryClient.invalidateQueries(['atenciones', update.pacienteId]);
          // Update optimistically if we have the data
          queryClient.setQueryData(['atenciones', update.pacienteId], (old: AtencionBase[] = []) => 
            [...old, update.atencion]
          );
          break;
          
        case 'COMPLIANCE_ALERT':
          // Add to global compliance alerts
          dispatch({ type: 'ADD_COMPLIANCE_ALERT', payload: update.alert });
          break;
      }
    };
    
    return () => eventSource.close();
  }, [queryClient, entities]);
};
```

---

## 🧪 **Testing State Management**

### **📋 Query Testing**
```typescript
// __tests__/hooks/usePacienteQueries.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { usePaciente } from '../hooks/usePacienteQueries';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false }
  }
});

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const testQueryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={testQueryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('usePaciente', () => {
  it('should fetch patient data successfully', async () => {
    const mockPaciente = createMockPaciente();
    
    // Mock API
    jest.mocked(getPacienteAPI).mockResolvedValue(mockPaciente);
    
    const { result } = renderHook(
      () => usePaciente(mockPaciente.id),
      { wrapper }
    );
    
    // Initial loading state
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeUndefined();
    
    // Wait for success
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });
    
    expect(result.current.data).toEqual(mockPaciente);
    expect(getPacienteAPI).toHaveBeenCalledWith(mockPaciente.id);
  });
});
```

### **📝 Form State Testing**
```typescript
// __tests__/hooks/useMedicalForm.test.ts
describe('useMedicalForm', () => {
  const mockSchema = z.object({
    fecha_nacimiento: z.string(),
    nombre: z.string().min(1)
  });
  
  it('should validate compliance in real-time', async () => {
    const complianceFields = [
      { field: 'fecha_nacimiento', rule: 'no_future_date' }
    ];
    
    const { result } = renderHook(() => 
      useMedicalForm({
        schema: mockSchema,
        complianceFields
      })
    );
    
    // Set future date (violation)
    act(() => {
      result.current.setValue('fecha_nacimiento', '2030-01-01');
    });
    
    await waitFor(() => {
      expect(result.current.complianceViolations).toHaveLength(1);
      expect(result.current.isCompliant).toBe(false);
    });
  });
});
```

---

## 📚 **Best Practices & Patterns**

### **✅ Do's:**
- **Separate concerns:** Server state (React Query) vs Client state (useState/Context)
- **Cache strategically:** Medical data deserves longer cache times
- **Optimistic updates:** For better UX in critical workflows
- **Error boundaries:** Graceful degradation for data loading errors
- **Compliance validation:** Real-time + submit validation
- **Auto-save:** For long medical forms to prevent data loss

### **❌ Don'ts:**
- **Don't:** Store server data in useState/Context
- **Don't:** Over-invalidate queries (performance impact)
- **Don't:** Skip error handling for medical data
- **Don't:** Forget offline scenarios for mobile usage
- **Don't:** Mix form state with server state
- **Don't:** Skip compliance validation for any medical form

---

**🔄 Este documento evoluciona con nuevos patterns de estado**  
**👥 Mantenido por:** Team Frontend Principal  
**🎯 Objetivo:** State management robusto para aplicación médica crítica