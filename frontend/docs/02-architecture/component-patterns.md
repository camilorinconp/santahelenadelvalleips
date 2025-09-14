# 🧩 Patrones de Componentes React - Frontend Médico

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Patrones arquitectónicos React para aplicaciones médicas  
**📍 Audiencia:** Developers React, Arquitectos Frontend  

---

## 🎯 **Filosofía Componentes Médicos**

Los componentes React del sistema IPS se diseñan siguiendo principios específicos para aplicaciones de salud:

### **🏥 Principios Fundamentales:**
1. **Medical-First**: Componentes optimizados para workflows médicos
2. **Compliance-Aware**: Validación automática Resolución 3280
3. **Performance-Critical**: Loading rápido para situaciones clínicas urgentes
4. **Accessibility-Mandatory**: WCAG compliance para inclusividad
5. **Integration-Seamless**: Polimorfismo backend transparente

---

## 🏗️ **Arquitectura Base Componentes**

### **📋 Jerarquía Estándar:**
```typescript
// Estructura tipo componente médico
interface MedicalComponentProps {
  pacienteId?: string;
  tipoAtencion?: TipoAtencionRIAS;
  compliance?: ResolucionField[];
  onValidationChange?: (isValid: boolean) => void;
  readonly?: boolean;
}

const MedicalComponent: React.FC<MedicalComponentProps> = ({
  pacienteId,
  tipoAtencion,
  compliance = [],
  onValidationChange,
  readonly = false
}) => {
  // 1. Hooks de estado
  const { data: paciente } = useQuery(['paciente', pacienteId]);
  const { mutate: guardarAtencion } = useMutation(guardarAtencionAPI);
  
  // 2. Validación compliance
  const validationSchema = useMemo(() => 
    createComplianceSchema(tipoAtencion, compliance), [tipoAtencion, compliance]
  );
  
  // 3. Form management
  const form = useForm({
    resolver: zodResolver(validationSchema),
    mode: 'onChange'
  });
  
  // 4. Render lógica médica
  return (
    <MedicalFormLayout>
      <ComplianceValidationProvider schema={validationSchema}>
        {/* Contenido específico */}
      </ComplianceValidationProvider>
    </MedicalFormLayout>
  );
};
```

---

## 🎨 **Patrones Específicos por Tipo**

### **1. 📝 Form Components Médicos**

#### **Patrón: MedicalFormWizard**
```typescript
// Componente para formularios médicos complejos
interface MedicalFormWizardProps {
  steps: FormStep[];
  tipoAtencion: TipoAtencionRIAS;
  onComplete: (data: AtencionMedica) => void;
  validationMode?: 'step' | 'complete';
}

const MedicalFormWizard: React.FC<MedicalFormWizardProps> = ({
  steps,
  tipoAtencion,
  onComplete,
  validationMode = 'step'
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  
  // Validación por paso vs. completa
  const validateStep = useCallback((stepData: any) => {
    if (validationMode === 'step') {
      return validateResolucion3280Fields(stepData, steps[currentStep].fields);
    }
    return true;
  }, [currentStep, validationMode]);
  
  return (
    <Stepper activeStep={currentStep}>
      {steps.map((step, index) => (
        <Step key={step.id}>
          <StepLabel error={step.hasErrors}>
            {step.label}
          </StepLabel>
          <StepContent>
            <DynamicFormStep
              fields={step.fields}
              data={formData}
              onChange={(data) => setFormData(prev => ({...prev, ...data}))}
              onValidate={validateStep}
            />
          </StepContent>
        </Step>
      ))}
    </Stepper>
  );
};
```

#### **Patrón: PolymorphicForm**
```typescript
// Formularios que cambian según tipo de atención
interface PolymorphicFormProps {
  tipoAtencion: TipoAtencionRIAS;
  initialData?: Partial<AtencionBase>;
  onSubmit: (data: AtencionPolimórfica) => void;
}

const PolymorphicForm: React.FC<PolymorphicFormProps> = ({
  tipoAtencion,
  initialData,
  onSubmit
}) => {
  // Determinar componente específico basado en tipo
  const FormComponent = useMemo(() => {
    switch (tipoAtencion) {
      case 'MATERNO_PERINATAL':
        return MaternoPerinatalForm;
      case 'PRIMERA_INFANCIA':
        return PrimeraInfanciaForm;
      case 'CONTROL_CRONICIDAD':
        return CronicidadForm;
      default:
        return GenericAtencionForm;
    }
  }, [tipoAtencion]);
  
  return (
    <FormProvider>
      <FormComponent
        initialData={initialData}
        onSubmit={onSubmit}
        complianceFields={getComplianceFields(tipoAtencion)}
      />
    </FormProvider>
  );
};
```

### **2. 📊 Data Display Components**

#### **Patrón: MedicalDataGrid**
```typescript
// Grillas optimizadas para datos médicos
interface MedicalDataGridProps<T> {
  data: T[];
  columns: MedicalColumn<T>[];
  filterOptions?: MedicalFilterOption[];
  complianceHighlight?: boolean;
  onRowSelect?: (item: T) => void;
  loading?: boolean;
}

const MedicalDataGrid = <T extends BaseEntity>({
  data,
  columns,
  filterOptions = [],
  complianceHighlight = true,
  onRowSelect,
  loading = false
}: MedicalDataGridProps<T>) => {
  // Highlighting automático campos compliance
  const enhancedColumns = useMemo(() => 
    columns.map(col => ({
      ...col,
      renderCell: complianceHighlight 
        ? addComplianceHighlight(col.renderCell)
        : col.renderCell
    })), [columns, complianceHighlight]
  );
  
  return (
    <DataGrid
      rows={data}
      columns={enhancedColumns}
      loading={loading}
      components={{
        Toolbar: () => (
          <MedicalToolbar 
            filters={filterOptions}
            onExport={() => exportMedicalData(data)}
          />
        ),
        NoRowsOverlay: () => <EmptyStateMedical />
      }}
      onRowClick={(params) => onRowSelect?.(params.row)}
    />
  );
};
```

### **3. 📈 Dashboard Components**

#### **Patrón: MedicalMetricsCard**
```typescript
// Cards métricas específicas médicas
interface MedicalMetricsCardProps {
  metric: MedicalMetric;
  complianceTarget?: number;
  trend?: 'up' | 'down' | 'stable';
  alertLevel?: 'normal' | 'warning' | 'critical';
  onClick?: () => void;
}

const MedicalMetricsCard: React.FC<MedicalMetricsCardProps> = ({
  metric,
  complianceTarget,
  trend,
  alertLevel = 'normal',
  onClick
}) => {
  const alertColor = {
    normal: 'success',
    warning: 'warning', 
    critical: 'error'
  }[alertLevel];
  
  const isCompliant = complianceTarget 
    ? metric.value >= complianceTarget
    : true;
  
  return (
    <Card 
      sx={{ 
        cursor: onClick ? 'pointer' : 'default',
        border: !isCompliant ? 2 : 0,
        borderColor: 'error.main'
      }}
      onClick={onClick}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{metric.label}</Typography>
          <TrendIcon trend={trend} />
        </Box>
        
        <Typography variant="h3" color={alertColor}>
          {formatMedicalValue(metric.value, metric.type)}
        </Typography>
        
        {complianceTarget && (
          <ComplianceIndicator 
            current={metric.value}
            target={complianceTarget}
            label="Meta Resolución 3280"
          />
        )}
        
        <Typography variant="caption" color="textSecondary">
          Última actualización: {formatRelativeTime(metric.updatedAt)}
        </Typography>
      </CardContent>
    </Card>
  );
};
```

---

## 🔄 **Patrones Estado y Lifecycle**

### **1. 🏥 Medical State Hooks**

#### **Hook: usePacienteMedical**
```typescript
// Hook especializado para gestión estado paciente
interface UsePacienteMedicalReturn {
  paciente: Paciente | null;
  atenciones: AtencionMedica[];
  alerts: MedicalAlert[];
  isLoading: boolean;
  error: Error | null;
  
  // Actions
  updatePaciente: (data: Partial<Paciente>) => Promise<void>;
  createAtencion: (atencion: AtencionCreate) => Promise<void>;
  dismissAlert: (alertId: string) => void;
}

export const usePacienteMedical = (pacienteId: string): UsePacienteMedicalReturn => {
  // Queries
  const { data: paciente, isLoading: loadingPaciente } = useQuery(
    ['paciente', pacienteId],
    () => getPacienteAPI(pacienteId),
    { staleTime: 5 * 60 * 1000 } // 5 min cache
  );
  
  const { data: atenciones = [], isLoading: loadingAtenciones } = useQuery(
    ['atenciones', pacienteId],
    () => getAtencionesPacienteAPI(pacienteId),
    { enabled: !!pacienteId }
  );
  
  // Medical alerts derivadas
  const alerts = useMemo(() => 
    generateMedicalAlerts(paciente, atenciones), 
    [paciente, atenciones]
  );
  
  // Mutations
  const updatePacienteMutation = useMutation(updatePacienteAPI, {
    onSuccess: () => {
      queryClient.invalidateQueries(['paciente', pacienteId]);
    }
  });
  
  return {
    paciente,
    atenciones,
    alerts,
    isLoading: loadingPaciente || loadingAtenciones,
    error: updatePacienteMutation.error,
    
    updatePaciente: updatePacienteMutation.mutate,
    createAtencion: async (atencion) => {
      await createAtencionAPI(atencion);
      queryClient.invalidateQueries(['atenciones', pacienteId]);
    },
    dismissAlert: (alertId) => {
      // Handle alert dismissal
    }
  };
};
```

#### **Hook: useComplianceValidation**
```typescript
// Hook para validación compliance automática
interface UseComplianceValidationProps {
  tipoAtencion: TipoAtencionRIAS;
  formData: any;
  mode: 'realtime' | 'submit';
}

export const useComplianceValidation = ({
  tipoAtencion,
  formData,
  mode = 'submit'
}: UseComplianceValidationProps) => {
  const [violations, setViolations] = useState<ComplianceViolation[]>([]);
  
  // Validación en tiempo real o en submit
  useEffect(() => {
    if (mode === 'realtime') {
      const debounced = debounce(() => {
        const newViolations = validateResolucion3280(tipoAtencion, formData);
        setViolations(newViolations);
      }, 500);
      
      debounced();
      return debounced.cancel;
    }
  }, [formData, tipoAtencion, mode]);
  
  const validateOnSubmit = useCallback(() => {
    const newViolations = validateResolucion3280(tipoAtencion, formData);
    setViolations(newViolations);
    return newViolations.length === 0;
  }, [tipoAtencion, formData]);
  
  return {
    violations,
    isValid: violations.length === 0,
    validateOnSubmit,
    clearViolations: () => setViolations([])
  };
};
```

---

## 🎯 **Patrones Performance**

### **1. ⚡ Optimization Strategies**

#### **Lazy Loading Médico**
```typescript
// Lazy loading para componentes pesados médicos
const MaternoPerinatalForm = lazy(() => 
  import('./forms/MaternoPerinatalForm').then(module => ({
    default: module.MaternoPerinatalForm
  }))
);

const CronicidadForm = lazy(() => import('./forms/CronicidadForm'));
const PrimeraInfanciaForm = lazy(() => import('./forms/PrimeraInfanciaForm'));

// Componente con fallback médico apropiado
const LazyMedicalForm: React.FC<{tipo: TipoAtencionRIAS}> = ({tipo}) => (
  <Suspense fallback={<MedicalFormSkeleton />}>
    {tipo === 'MATERNO_PERINATAL' && <MaternoPerinatalForm />}
    {tipo === 'CONTROL_CRONICIDAD' && <CronicidadForm />}
    {tipo === 'PRIMERA_INFANCIA' && <PrimeraInfanciaForm />}
  </Suspense>
);
```

#### **Memoization Patterns**
```typescript
// Memoización para componentes médicos complejos
const MedicalFormSection = React.memo<MedicalFormSectionProps>(({
  fields,
  data,
  onChange,
  complianceRules
}) => {
  // Expensive validation only when relevant data changes
  const validationErrors = useMemo(() => 
    validateComplexMedicalFields(data, complianceRules),
    [data, complianceRules] // NOT fields - avoid re-validation on field order changes
  );
  
  return (
    <FormSection>
      {fields.map(field => (
        <MedicalField 
          key={field.id}
          field={field}
          value={data[field.name]}
          error={validationErrors[field.name]}
          onChange={onChange}
        />
      ))}
    </FormSection>
  );
}, (prevProps, nextProps) => {
  // Custom comparison para evitar re-renders innecesarios
  return (
    prevProps.data === nextProps.data &&
    prevProps.complianceRules === nextProps.complianceRules &&
    prevProps.fields.length === nextProps.fields.length
  );
});
```

---

## 🧪 **Testing Patterns**

### **📋 Component Testing**
```typescript
// Test pattern para componentes médicos
describe('MaternoPerinatalForm', () => {
  const defaultProps = {
    pacienteId: 'test-paciente-id',
    onSubmit: jest.fn(),
    complianceFields: getMockComplianceFields('MATERNO_PERINATAL')
  };
  
  it('should validate Resolución 3280 compliance fields', async () => {
    render(<MaternoPerinatalForm {...defaultProps} />);
    
    // Llenar datos que violan compliance
    await user.type(screen.getByLabelText('Fecha Último Parto'), '2030-01-01');
    
    // Verificar violación detectada
    expect(screen.getByText(/fecha no puede ser futura/i)).toBeInTheDocument();
    
    // Verificar form no se puede enviar
    const submitButton = screen.getByRole('button', {name: /guardar/i});
    expect(submitButton).toBeDisabled();
  });
  
  it('should handle polymorphic data correctly', async () => {
    const mockSubmit = jest.fn();
    render(<MaternoPerinatalForm {...defaultProps} onSubmit={mockSubmit} />);
    
    // Llenar form válido
    await fillValidMaternoPerinatalForm();
    
    // Submit
    await user.click(screen.getByRole('button', {name: /guardar/i}));
    
    // Verificar estructura polimórfica correcta
    expect(mockSubmit).toHaveBeenCalledWith({
      tipo_atencion: 'MATERNO_PERINATAL',
      detalle_control_prenatal: expect.objectContaining({
        fecha_ultimo_parto: expect.any(String),
        numero_controles_prenatales: expect.any(Number)
      })
    });
  });
});
```

---

## 📚 **Referencias y Mejores Prácticas**

### **🔗 Documentos Relacionados:**
- **[UI Design System](./ui-design-system.md)** - Material-UI theming y components
- **[State Management](./state-management.md)** - React Query patterns
- **[Backend API Guide](../03-integration/backend-api-guide.md)** - Integration patterns

### **✅ Checklist Nuevo Componente:**
- [ ] TypeScript interfaces completas
- [ ] Props validation con PropTypes o TypeScript
- [ ] Compliance validation si aplica
- [ ] Error boundaries apropiados
- [ ] Loading states implementados
- [ ] Accessibility (ARIA labels, keyboard navigation)
- [ ] Tests unitarios escritos
- [ ] Performance optimizations aplicadas
- [ ] Documentation actualizada

### **⚠️ Anti-Patterns a Evitar:**
- ❌ Componentes monolíticos (>500 líneas)
- ❌ Props drilling excesivo (usar Context)
- ❌ Side effects en render
- ❌ Validación sin debounce en forms grandes
- ❌ State local para datos del servidor (usar React Query)

---

**🔄 Este documento se actualiza con cada nuevo patrón implementado**  
**👥 Mantenido por:** Team Frontend Principal  
**🎯 Objetivo:** Consistency y efficiency en desarrollo componentes médicos