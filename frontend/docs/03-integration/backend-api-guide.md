# 🔗 Backend API Integration Guide - Polimorfismo Médico

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Guía completa integración frontend con APIs polimórficas backend  
**📍 Audiencia:** Frontend Developers, Integration Engineers  

---

## 🎯 **Arquitectura Integración**

### **🏗️ Visión General:**
```typescript
Frontend (React + TypeScript)  ↔  Backend (FastAPI + Pydantic)
│                                  │
├─ React Query (Server State)     ├─ RESTful APIs
├─ Zod Validation (Mirror)        ├─ Pydantic Models  
├─ TypeScript Types               ├─ PostgreSQL + Supabase
└─ Material-UI Components         └─ RLS Security
```

### **🔄 Flujo Polimórfico:**
```
1. Usuario selecciona tipo atención → TipoAtencionRIAS
2. Frontend determina schema específico → getSchemaForTipo()
3. Form dinámico renderizado → PolymorphicForm
4. Validación Zod (espejo Pydantic) → zodResolver()
5. Envío dual: detalle + atención → createDetalleAPI() + createAtencionAPI()
6. Backend manejo polimórfico → Nested polymorphism
7. Response unificada → React Query cache update
```

---

## 📡 **API Endpoints Disponibles**

### **👥 Pacientes API**
```typescript
// api/pacientesApi.ts
export interface PacienteAPI {
  // CRUD Operations
  getPacientes: (filters?: PacienteFilters) => Promise<PacienteResponse[]>;
  getPaciente: (id: string) => Promise<Paciente>;
  createPaciente: (data: PacienteCreate) => Promise<Paciente>;
  updatePaciente: (id: string, data: PacienteUpdate) => Promise<Paciente>;
  deletePaciente: (id: string) => Promise<void>;
  
  // Search & Filters
  searchPacientes: (query: string) => Promise<PacienteResponse[]>;
  getPacientesByDocumento: (documento: string) => Promise<PacienteResponse[]>;
}

// Endpoints disponibles
const PACIENTES_ENDPOINTS = {
  base: '/api/pacientes',
  byId: (id: string) => `/api/pacientes/${id}`,
  search: '/api/pacientes/search',
  byDocumento: '/api/pacientes/documento'
} as const;

// Example implementation with error handling
export const getPacienteAPI = async (id: string): Promise<Paciente> => {
  try {
    const response = await axiosInstance.get(PACIENTES_ENDPOINTS.byId(id));
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        throw new NotFoundError(`Paciente con ID ${id} no encontrado`);
      }
      throw new APIError(`Error obteniendo paciente: ${error.message}`);
    }
    throw error;
  }
};
```

### **🏥 Atenciones Polimórficas API**
```typescript
// api/atencionesApi.ts - Manejo polimorfismo complejo
export interface AtencionPolimorficaAPI {
  // Base operations
  getAtenciones: (pacienteId: string) => Promise<AtencionBase[]>;
  getAtencion: (id: string) => Promise<AtencionCompleta>;
  
  // Polymorphic creation - dos pasos
  createAtencionMaternoPerinatural: (data: MaternoPerinatalCreate) => Promise<AtencionMaternoPerinatal>;
  createAtencionPrimeraInfancia: (data: PrimeraInfanciaCreate) => Promise<AtencionPrimeraInfancia>;
  createAtencionCronicidad: (data: CronicidadCreate) => Promise<AtencionCronicidad>;
  
  // Generic polymorphic handler
  createAtencionPolimorfica: (data: AtencionPolimorficaCreate) => Promise<AtencionCompleta>;
}

// Polymorphic creation implementation
export const createAtencionPolimorfica = async (
  data: AtencionPolimorficaCreate
): Promise<AtencionCompleta> => {
  const { tipo, atencionBase, detalleEspecifico } = data;
  
  try {
    // Step 1: Create specific detail
    const detalleEndpoint = getDetalleEndpoint(tipo);
    const detalleResponse = await axiosInstance.post(detalleEndpoint, detalleEspecifico);
    
    // Step 2: Create base attention with detail reference
    const atencionData = {
      ...atencionBase,
      tipo_atencion: tipo,
      detalle_id: detalleResponse.data.id
    };
    
    const atencionResponse = await axiosInstance.post('/api/atenciones', atencionData);
    
    // Return combined result
    return {
      ...atencionResponse.data,
      detalleEspecifico: detalleResponse.data
    };
    
  } catch (error) {
    // Cleanup on error - delete detail if created
    if (detalleResponse?.data?.id) {
      await deleteDetalleEspecificoAPI(tipo, detalleResponse.data.id);
    }
    throw error;
  }
};

// Helper function for endpoint mapping
const getDetalleEndpoint = (tipo: TipoAtencionRIAS): string => {
  const endpointMap = {
    'MATERNO_PERINATAL': '/api/atencion-materno-perinatal',
    'PRIMERA_INFANCIA': '/api/atencion-primera-infancia', 
    'CONTROL_CRONICIDAD': '/api/control-cronicidad',
    'TAMIZAJE_ONCOLOGICO': '/api/tamizaje-oncologico'
  } as const;
  
  return endpointMap[tipo];
};
```

---

## 🔄 **React Query Integration Patterns**

### **📊 Query Hooks Especializados**
```typescript
// hooks/useAtencionQueries.ts - Optimized for medical workflows
export const useAtencionesPolimorficas = (pacienteId: string) => {
  return useQuery({
    queryKey: ['atenciones', pacienteId],
    queryFn: () => getAtencionesAPI(pacienteId),
    staleTime: 5 * 60 * 1000, // 5 min - medical data freshness
    
    select: (atenciones: AtencionBase[]) => {
      // Transform for UI consumption
      return atenciones.map(atencion => ({
        ...atencion,
        // Add computed properties
        tipoDisplayName: getTipoDisplayName(atencion.tipo_atencion),
        complianceStatus: checkComplianceStatus(atencion),
        urgencyLevel: calculateUrgencyLevel(atencion),
        
        // Add formatted dates
        fechaFormateada: formatMedicalDate(atencion.fecha_atencion),
        tiempoTranscurrido: formatRelativeTime(atencion.fecha_atencion)
      }));
    },
    
    // Background updates for critical medical data
    refetchInterval: 2 * 60 * 1000, // 2 minutes
    refetchOnWindowFocus: true,
    
    // Error handling
    onError: (error: Error) => {
      console.error('Error loading atenciones:', error);
      toast.error('Error cargando atenciones médicas');
    }
  });
};

// Prefetching strategy for smooth navigation
export const usePrefetchAtencionDetalle = () => {
  const queryClient = useQueryClient();
  
  return useCallback((atencionId: string, tipo: TipoAtencionRIAS) => {
    // Prefetch detalle específico based on type
    queryClient.prefetchQuery({
      queryKey: ['atencion-detalle', atencionId, tipo],
      queryFn: () => getAtencionDetalleAPI(atencionId, tipo),
      staleTime: 10 * 60 * 1000
    });
  }, [queryClient]);
};
```

### **✨ Mutation Hooks con Optimistic Updates**
```typescript
// hooks/useAtencionMutations.ts
export const useCreateAtencionOptimistic = (pacienteId: string) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createAtencionPolimorfica,
    
    // Optimistic update for immediate UI feedback
    onMutate: async (newAtencion: AtencionPolimorficaCreate) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries(['atenciones', pacienteId]);
      
      // Snapshot previous value
      const previousAtenciones = queryClient.getQueryData<AtencionBase[]>(['atenciones', pacienteId]);
      
      // Optimistically update cache
      const optimisticAtencion: AtencionBase = {
        id: `temp-${Date.now()}`,
        paciente_id: pacienteId,
        tipo_atencion: newAtencion.tipo,
        fecha_atencion: new Date().toISOString(),
        estado: 'EN_PROGRESO',
        ...newAtencion.atencionBase,
        // Visual indicator for optimistic update
        isOptimistic: true
      };
      
      queryClient.setQueryData<AtencionBase[]>(['atenciones', pacienteId], old => 
        old ? [optimisticAtencion, ...old] : [optimisticAtencion]
      );
      
      return { previousAtenciones };
    },
    
    // Rollback on error
    onError: (error, newAtencion, context) => {
      queryClient.setQueryData(['atenciones', pacienteId], context?.previousAtenciones);
      
      // Handle specific medical errors
      if (error instanceof ComplianceError) {
        toast.error(`Error de compliance: ${error.message}`);
      } else if (error instanceof ValidationError) {
        toast.error(`Datos inválidos: ${error.message}`);
      } else {
        toast.error('Error creando atención médica');
      }
    },
    
    // Update cache with real data on success
    onSuccess: (createdAtencion, variables) => {
      // Remove optimistic update and add real data
      queryClient.setQueryData<AtencionBase[]>(['atenciones', pacienteId], old => 
        old?.filter(a => !a.isOptimistic).concat(createdAtencion) || [createdAtencion]
      );
      
      // Invalidate related queries
      queryClient.invalidateQueries(['paciente', pacienteId]);
      queryClient.invalidateQueries(['dashboard-metrics']);
      
      toast.success('Atención médica registrada exitosamente');
    }
  });
};
```

---

## 📋 **Type Safety & Validation**

### **🔒 TypeScript Types Sync**
```typescript
// types/medical.ts - Mirror of backend Pydantic models
export interface Paciente {
  id: string;
  tipo_documento: TipoDocumento;
  numero_documento: string;
  primer_nombre: string;
  segundo_nombre?: string;
  primer_apellido: string;
  segundo_apellido?: string;
  fecha_nacimiento: string; // ISO date string
  genero: Genero;
  telefono?: string;
  direccion?: string;
  municipio?: string;
  departamento?: string;
  
  // Computed fields (not in backend model)
  edad?: number;
  nombreCompleto?: string;
}

// Union types for polymorphic handling
export type TipoAtencionRIAS = 
  | 'MATERNO_PERINATAL'
  | 'PRIMERA_INFANCIA'  
  | 'CONTROL_CRONICIDAD'
  | 'TAMIZAJE_ONCOLOGICO';

// Base attention structure
export interface AtencionBase {
  id: string;
  paciente_id: string;
  tipo_atencion: TipoAtencionRIAS;
  fecha_atencion: string;
  estado: EstadoAtencion;
  observaciones?: string;
  
  // Polymorphic detail reference
  detalle_id: string;
}

// Polymorphic details - discriminated unions
export type AtencionDetalle = 
  | { tipo: 'MATERNO_PERINATAL'; detalle: DetalleMaternoPerinatural }
  | { tipo: 'PRIMERA_INFANCIA'; detalle: DetallePrimeraInfancia }
  | { tipo: 'CONTROL_CRONICIDAD'; detalle: DetalleCronicidad }
  | { tipo: 'TAMIZAJE_ONCOLOGICO'; detalle: DetalleTamizaje };

// Complete attention with polymorphic detail
export interface AtencionCompleta extends AtencionBase {
  detalleEspecifico: AtencionDetalle['detalle'];
}
```

### **✅ Zod Validation Schemas**
```typescript
// schemas/medicalSchemas.ts - Mirror Pydantic validation
import { z } from 'zod';

// Colombian document validation
export const colombianDocumentSchema = z
  .string()
  .min(6, 'Documento debe tener mínimo 6 caracteres')
  .max(12, 'Documento debe tener máximo 12 caracteres')
  .regex(/^\d+$/, 'Documento solo puede contener números')
  .refine((val) => !val.startsWith('0'), 'Documento no puede empezar con 0');

// Patient schema matching backend
export const pacienteSchema = z.object({
  tipo_documento: z.enum(['CC', 'TI', 'CE', 'PA', 'RC']),
  numero_documento: colombianDocumentSchema,
  primer_nombre: z.string().min(1, 'Primer nombre es requerido'),
  segundo_nombre: z.string().optional(),
  primer_apellido: z.string().min(1, 'Primer apellido es requerido'),
  segundo_apellido: z.string().optional(),
  fecha_nacimiento: z
    .string()
    .refine((date) => !isNaN(Date.parse(date)), 'Fecha inválida')
    .refine((date) => new Date(date) <= new Date(), 'Fecha no puede ser futura'),
  genero: z.enum(['M', 'F', 'O']),
  telefono: z.string().regex(/^3\d{9}$/, 'Teléfono debe ser formato colombiano').optional(),
  direccion: z.string().optional(),
  municipio: z.string().optional(),
  departamento: z.string().optional()
});

// Polymorphic schema factory
export const getAtencionSchema = (tipo: TipoAtencionRIAS) => {
  const baseSchema = z.object({
    paciente_id: z.string().uuid('ID paciente inválido'),
    fecha_atencion: z.string().refine(
      (date) => new Date(date) <= new Date(),
      'Fecha atención no puede ser futura'
    ),
    observaciones: z.string().optional()
  });
  
  switch (tipo) {
    case 'MATERNO_PERINATAL':
      return baseSchema.extend({
        detalle: maternoPerinatalSchema
      });
      
    case 'PRIMERA_INFANCIA':
      return baseSchema.extend({
        detalle: primeraInfanciaSchema
      });
      
    case 'CONTROL_CRONICIDAD':
      return baseSchema.extend({
        detalle: cronicidadSchema
      });
      
    default:
      return baseSchema;
  }
};

// Compliance validation schemas
export const complianceSchema = z.object({
  resolucion3280Fields: z.array(z.string()),
  complianceLevel: z.enum(['COMPLIANT', 'PARTIAL', 'VIOLATION']),
  violations: z.array(z.object({
    field: z.string(),
    rule: z.string(),
    message: z.string()
  }))
});
```

---

## 🔧 **Error Handling Strategy**

### **🚨 Error Types & Handling**
```typescript
// errors/medicalErrors.ts
export class MedicalError extends Error {
  constructor(
    message: string,
    public code: string,
    public context?: any
  ) {
    super(message);
    this.name = 'MedicalError';
  }
}

export class ComplianceError extends MedicalError {
  constructor(
    message: string,
    public violations: ComplianceViolation[]
  ) {
    super(message, 'COMPLIANCE_ERROR', { violations });
    this.name = 'ComplianceError';
  }
}

export class ValidationError extends MedicalError {
  constructor(
    message: string,
    public field: string,
    public value: any
  ) {
    super(message, 'VALIDATION_ERROR', { field, value });
    this.name = 'ValidationError';
  }
}

// Error handling hook
export const useErrorHandler = () => {
  const handleError = useCallback((error: Error) => {
    console.error('Medical app error:', error);
    
    if (error instanceof ComplianceError) {
      // Show compliance-specific error dialog
      showComplianceErrorDialog(error.violations);
      return;
    }
    
    if (error instanceof ValidationError) {
      // Highlight specific field error
      highlightFieldError(error.field, error.message);
      return;
    }
    
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const message = error.response?.data?.detail || error.message;
      
      switch (status) {
        case 404:
          toast.error('Recurso no encontrado');
          break;
        case 422:
          toast.error(`Datos inválidos: ${message}`);
          break;
        case 500:
          toast.error('Error del servidor. Contacte soporte técnico.');
          break;
        default:
          toast.error(`Error de conexión: ${message}`);
      }
      return;
    }
    
    // Generic error fallback
    toast.error('Error inesperado. Por favor intente de nuevo.');
  }, []);
  
  return { handleError };
};
```

### **🔄 Retry Strategy**
```typescript
// api/retryConfig.ts
export const medicalRetryConfig = {
  retries: 3,
  retryDelay: (attemptIndex: number) => Math.min(1000 * 2 ** attemptIndex, 10000),
  retryCondition: (error: AxiosError) => {
    // Don't retry on client errors (4xx)
    if (error.response?.status && error.response.status >= 400 && error.response.status < 500) {
      return false;
    }
    
    // Retry on network errors and 5xx server errors
    return !error.response || error.response.status >= 500;
  },
  
  // Special retry for critical medical operations
  criticalRetryConfig: {
    retries: 5,
    retryDelay: () => 2000, // Fixed 2s delay for critical operations
    retryCondition: () => true // Always retry critical operations
  }
};
```

---

## 📊 **Performance Optimization**

### **⚡ Caching Strategy**
```typescript
// api/cacheConfig.ts
export const medicalCacheConfig = {
  // Patient data - moderate caching
  pacientes: {
    staleTime: 5 * 60 * 1000,     // 5 minutes
    cacheTime: 10 * 60 * 1000,    // 10 minutes
    refetchOnWindowFocus: true
  },
  
  // Medical attention - fresh data critical
  atenciones: {
    staleTime: 2 * 60 * 1000,     // 2 minutes
    cacheTime: 5 * 60 * 1000,     // 5 minutes  
    refetchOnWindowFocus: true,
    refetchInterval: 2 * 60 * 1000 // Background refresh
  },
  
  // Catalogs - long caching (rarely change)
  catalogos: {
    staleTime: 60 * 60 * 1000,    // 1 hour
    cacheTime: 24 * 60 * 60 * 1000, // 24 hours
    refetchOnWindowFocus: false
  },
  
  // Dashboard metrics - frequent updates
  metrics: {
    staleTime: 30 * 1000,         // 30 seconds
    cacheTime: 2 * 60 * 1000,     // 2 minutes
    refetchInterval: 60 * 1000    // 1 minute refresh
  }
};
```

### **🔧 Request Optimization**
```typescript
// api/optimizations.ts
export const useRequestOptimization = () => {
  // Request deduplication
  const debouncedSearch = useMemo(
    () => debounce((query: string) => {
      if (query.length >= 3) {
        searchPacientesAPI(query);
      }
    }, 300),
    []
  );
  
  // Batch requests
  const batchRequests = useCallback(async (requests: Array<() => Promise<any>>) => {
    try {
      const results = await Promise.allSettled(requests.map(req => req()));
      return results.map(result => 
        result.status === 'fulfilled' ? result.value : null
      );
    } catch (error) {
      console.error('Batch request error:', error);
      throw error;
    }
  }, []);
  
  return {
    debouncedSearch,
    batchRequests
  };
};
```

---

## 🧪 **Testing Integration**

### **📋 API Testing Patterns**
```typescript
// __tests__/api/atencionesApi.test.ts
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { createAtencionPolimorfica } from '../api/atencionesApi';

// Mock server for testing
const server = setupServer(
  rest.post('/api/atencion-materno-perinatal', (req, res, ctx) => {
    return res(ctx.json({ 
      id: 'detalle-123',
      ...req.body 
    }));
  }),
  
  rest.post('/api/atenciones', (req, res, ctx) => {
    return res(ctx.json({ 
      id: 'atencion-456',
      ...req.body 
    }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Polymorphic Attention API', () => {
  it('should create materno-perinatal attention with proper polymorphic flow', async () => {
    const mockData = {
      tipo: 'MATERNO_PERINATAL' as const,
      atencionBase: {
        paciente_id: 'paciente-123',
        fecha_atencion: '2023-09-14',
        observaciones: 'Control prenatal rutinario'
      },
      detalleEspecifico: {
        semanas_gestacion: 20,
        peso_gestante: 65,
        presion_arterial: '120/80'
      }
    };
    
    const result = await createAtencionPolimorfica(mockData);
    
    // Verify polymorphic structure
    expect(result).toMatchObject({
      id: 'atencion-456',
      tipo_atencion: 'MATERNO_PERINATAL',
      detalle_id: 'detalle-123',
      detalleEspecifico: expect.objectContaining({
        semanas_gestacion: 20
      })
    });
  });
});
```

---

**🔗 Esta guía evoluciona con nuevas APIs y patrones de integración**  
**👥 Mantenido por:** Team Frontend + Backend Integration  
**🎯 Objetivo:** Integración robusta y type-safe con backend polimórfico médico