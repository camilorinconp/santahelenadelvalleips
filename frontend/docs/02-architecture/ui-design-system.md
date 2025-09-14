# 🎨 UI Design System - Material-UI Médico

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Sistema diseño completo para interfaces médicas profesionales  
**📍 Audiencia:** UI/UX Designers, Frontend Developers  

---

## 🎯 **Filosofía Design System Médico**

### **🏥 Principios Fundamentales:**
1. **Medical-First Design:** Interfaces optimizadas para workflows médicos urgentes
2. **Clarity Over Beauty:** Información crítica debe ser inmediatamente comprensible  
3. **Accessibility Mandatory:** WCAG 2.1 AA compliance para inclusividad total
4. **Performance Critical:** Componentes livianos para dispositivos médicos
5. **Consistency Across Profiles:** Base común + especializaciones por usuario

### **📱 Target Devices:**
- **Tablets médicas:** 10-12" primary target
- **Desktop workstations:** Secondary para call center
- **Mobile emergency:** Degradación elegante para consultas urgentes

---

## 🎨 **Theming Strategy**

### **🌈 Color Palette Médico**
```typescript
// theme/colors.ts - Paleta especializada salud
export const medicalColors = {
  primary: {
    main: '#1976d2',      // Azul médico confiable
    light: '#42a5f5',     // Highlights y estados active
    dark: '#1565c0',      // Headers y elementos importantes
    contrastText: '#fff'
  },
  
  secondary: {
    main: '#388e3c',      // Verde salud/éxito  
    light: '#66bb6a',     // Estados positivos
    dark: '#2e7d32',      // Confirmaciones importantes
    contrastText: '#fff'
  },
  
  // Medical-specific colors
  medical: {
    critical: '#d32f2f',      // Emergencias/crítico
    warning: '#f57c00',       // Advertencias médicas
    info: '#0288d1',          // Información neutral
    success: '#388e3c',       // Estados positivos/saludables
    
    // Clinical indicators
    vital: {
      normal: '#4caf50',      // Signos vitales normales
      elevated: '#ff9800',    // Valores elevados
      critical: '#f44336'     // Valores críticos
    },
    
    // Compliance indicators  
    compliance: {
      compliant: '#4caf50',   // Cumple Resolución 3280
      partial: '#ff9800',     // Compliance parcial
      violation: '#f44336'    // Violación normativa
    }
  },
  
  // Background variations
  background: {
    default: '#fafafa',       // Background principal
    paper: '#ffffff',         // Cards y surfaces
    medical: '#f8f9fa',       // Background formularios médicos
    dashboard: '#f5f5f5'      // Background dashboard/reportes
  },
  
  // Text colors optimized para legibilidad médica
  text: {
    primary: '#212121',       // Texto principal oscuro
    secondary: '#757575',     // Texto secundario
    disabled: '#bdbdbd',      // Estados disabled
    medical: '#1a1a1a'        // Texto datos médicos (max contrast)
  }
};
```

### **📝 Typography Médica**
```typescript
// theme/typography.ts
export const medicalTypography = {
  fontFamily: [
    '"Roboto"',               // Primary - excellent readability
    '"Inter"',                // Fallback - modern medical interfaces  
    '"Segoe UI"',             // Windows fallback
    'sans-serif'
  ].join(','),
  
  // Medical-specific font weights
  fontWeights: {
    regular: 400,
    medium: 500,              // Para labels importantes
    semibold: 600,            // Para datos críticos
    bold: 700                 // Para alerts y warnings
  },
  
  // Optimized sizes para tablets médicas
  h1: {
    fontSize: '2.125rem',     // 34px - Titles principales
    fontWeight: 600,
    lineHeight: 1.2,
    letterSpacing: '-0.01em'
  },
  
  h2: {
    fontSize: '1.5rem',       // 24px - Section headers
    fontWeight: 600, 
    lineHeight: 1.3,
    letterSpacing: '-0.005em'
  },
  
  // Medical data typography
  medicalData: {
    fontSize: '1rem',         // 16px - Datos médicos críticos
    fontWeight: 600,
    lineHeight: 1.4,
    fontFamily: '"Roboto Mono"', // Monospace para valores numéricos
  },
  
  // Form labels optimized
  formLabel: {
    fontSize: '0.875rem',     // 14px - Labels formularios
    fontWeight: 500,
    lineHeight: 1.4,
    color: medicalColors.text.primary
  },
  
  // Small text pero legible
  caption: {
    fontSize: '0.75rem',      // 12px - Captions y metadata
    fontWeight: 400,
    lineHeight: 1.4,
    color: medicalColors.text.secondary
  }
};
```

---

## 🧩 **Component Library Médico**

### **📋 Form Components**

#### **MedicalTextField - Enhanced Input**
```typescript
// components/MedicalTextField.tsx
interface MedicalTextFieldProps extends TextFieldProps {
  complianceRule?: ComplianceRule;
  medicalType?: 'text' | 'numeric' | 'date' | 'time' | 'phone' | 'document';
  criticalField?: boolean;
  autoValidate?: boolean;
}

export const MedicalTextField: React.FC<MedicalTextFieldProps> = ({
  complianceRule,
  medicalType = 'text',
  criticalField = false,
  autoValidate = true,
  ...textFieldProps
}) => {
  const [complianceStatus, setComplianceStatus] = useState<'valid' | 'warning' | 'error'>('valid');
  
  // Real-time compliance validation
  useEffect(() => {
    if (autoValidate && complianceRule && textFieldProps.value) {
      const isValid = validateComplianceRule(textFieldProps.value, complianceRule);
      setComplianceStatus(isValid ? 'valid' : 'error');
    }
  }, [textFieldProps.value, complianceRule, autoValidate]);
  
  const getInputProps = () => {
    switch (medicalType) {
      case 'numeric':
        return {
          inputMode: 'numeric' as const,
          pattern: '[0-9]*'
        };
      case 'phone':
        return {
          inputMode: 'tel' as const,
          pattern: '[0-9+\\-\\s]*'
        };
      case 'document':
        return {
          inputMode: 'numeric' as const,
          maxLength: 12 // Colombian document ID max length
        };
      default:
        return {};
    }
  };
  
  return (
    <TextField
      {...textFieldProps}
      inputProps={{
        ...textFieldProps.inputProps,
        ...getInputProps()
      }}
      sx={{
        '& .MuiOutlinedInput-root': {
          // Critical field highlighting
          ...(criticalField && {
            backgroundColor: medicalColors.background.medical,
            '& fieldset': {
              borderWidth: 2,
              borderColor: complianceStatus === 'error' 
                ? medicalColors.medical.critical
                : medicalColors.primary.main
            }
          }),
          
          // Compliance status indicators
          '&::after': complianceRule && {
            content: complianceStatus === 'valid' ? '"✓"' : '"⚠"',
            position: 'absolute',
            right: 8,
            color: complianceStatus === 'valid' 
              ? medicalColors.medical.compliance.compliant
              : medicalColors.medical.compliance.violation
          }
        },
        ...textFieldProps.sx
      }}
    />
  );
};
```

#### **MedicalSelect - Enhanced Dropdown**
```typescript
// components/MedicalSelect.tsx
interface MedicalSelectProps extends SelectProps {
  options: MedicalOption[];
  complianceRequired?: boolean;
  searchable?: boolean;
  groupBy?: (option: MedicalOption) => string;
}

interface MedicalOption {
  value: string;
  label: string;
  description?: string;
  disabled?: boolean;
  complianceLevel?: 'required' | 'recommended' | 'optional';
}

export const MedicalSelect: React.FC<MedicalSelectProps> = ({
  options,
  complianceRequired = false,
  searchable = false,
  groupBy,
  ...selectProps
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredOptions = useMemo(() => {
    let filtered = options;
    
    // Search filtering
    if (searchTerm) {
      filtered = filtered.filter(option => 
        option.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
        option.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Group options if groupBy provided
    if (groupBy) {
      return filtered.reduce((groups, option) => {
        const group = groupBy(option);
        if (!groups[group]) groups[group] = [];
        groups[group].push(option);
        return groups;
      }, {} as Record<string, MedicalOption[]>);
    }
    
    return filtered;
  }, [options, searchTerm, groupBy]);
  
  const renderOption = (option: MedicalOption) => (
    <MenuItem 
      key={option.value} 
      value={option.value}
      disabled={option.disabled}
      sx={{
        // Compliance-based styling
        backgroundColor: option.complianceLevel === 'required' 
          ? 'rgba(25, 118, 210, 0.04)' 
          : 'transparent',
        '&::before': option.complianceLevel === 'required' && {
          content: '"*"',
          color: medicalColors.medical.critical,
          fontWeight: 'bold',
          marginRight: 1
        }
      }}
    >
      <Box>
        <Typography variant="body1">{option.label}</Typography>
        {option.description && (
          <Typography variant="caption" color="textSecondary">
            {option.description}
          </Typography>
        )}
      </Box>
    </MenuItem>
  );
  
  return (
    <FormControl fullWidth>
      <Select
        {...selectProps}
        MenuProps={{
          PaperProps: {
            sx: {
              maxHeight: 300,
              '& .MuiList-root': {
                padding: 0
              }
            }
          }
        }}
        sx={{
          // Compliance required indicator
          ...(complianceRequired && {
            '&::after': {
              content: '"*"',
              color: medicalColors.medical.critical,
              position: 'absolute',
              right: 32,
              top: '50%',
              transform: 'translateY(-50%)'
            }
          }),
          ...selectProps.sx
        }}
      >
        {/* Search input if searchable */}
        {searchable && (
          <Box sx={{ p: 1, borderBottom: 1, borderColor: 'divider' }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Buscar..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon />
              }}
            />
          </Box>
        )}
        
        {/* Render options or groups */}
        {groupBy && typeof filteredOptions === 'object' 
          ? Object.entries(filteredOptions).map(([group, options]) => [
              <ListSubheader key={group}>{group}</ListSubheader>,
              ...options.map(renderOption)
            ])
          : (filteredOptions as MedicalOption[]).map(renderOption)
        }
      </Select>
    </FormControl>
  );
};
```

### **📊 Data Display Components**

#### **MedicalCard - Enhanced Cards**
```typescript
// components/MedicalCard.tsx
interface MedicalCardProps extends CardProps {
  title: string;
  subtitle?: string;
  status?: 'normal' | 'warning' | 'critical' | 'success';
  complianceLevel?: 'compliant' | 'partial' | 'violation';
  lastUpdated?: Date;
  actionMenu?: React.ReactNode;
  criticalData?: boolean;
}

export const MedicalCard: React.FC<MedicalCardProps> = ({
  title,
  subtitle,
  status = 'normal',
  complianceLevel,
  lastUpdated,
  actionMenu,
  criticalData = false,
  children,
  ...cardProps
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'critical': return medicalColors.medical.critical;
      case 'warning': return medicalColors.medical.warning;
      case 'success': return medicalColors.medical.success;
      default: return medicalColors.primary.main;
    }
  };
  
  const getComplianceIcon = () => {
    if (!complianceLevel) return null;
    
    switch (complianceLevel) {
      case 'compliant':
        return <CheckCircleIcon color="success" />;
      case 'partial':
        return <WarningIcon color="warning" />;
      case 'violation':
        return <ErrorIcon color="error" />;
    }
  };
  
  return (
    <Card
      {...cardProps}
      sx={{
        // Critical data highlighting
        ...(criticalData && {
          border: 2,
          borderColor: getStatusColor(),
          boxShadow: `0 2px 8px rgba(${hexToRgb(getStatusColor())}, 0.15)`
        }),
        
        // Status indicator stripe
        borderLeft: 4,
        borderLeftColor: getStatusColor(),
        
        ...cardProps.sx
      }}
    >
      <CardHeader
        title={
          <Box display="flex" alignItems="center" gap={1}>
            <Typography 
              variant="h6" 
              sx={{ 
                fontWeight: criticalData ? 600 : 500,
                color: criticalData ? medicalColors.text.medical : 'inherit'
              }}
            >
              {title}
            </Typography>
            {getComplianceIcon()}
          </Box>
        }
        subheader={
          <Box>
            {subtitle && (
              <Typography variant="body2" color="textSecondary">
                {subtitle}
              </Typography>
            )}
            {lastUpdated && (
              <Typography variant="caption" color="textSecondary">
                Actualizado: {formatRelativeTime(lastUpdated)}
              </Typography>
            )}
          </Box>
        }
        action={actionMenu}
      />
      
      <CardContent>
        {children}
      </CardContent>
    </Card>
  );
};
```

#### **VitalSignsDisplay - Specialized Component**
```typescript
// components/VitalSignsDisplay.tsx
interface VitalSign {
  label: string;
  value: number;
  unit: string;
  normalRange: { min: number; max: number };
  timestamp: Date;
}

interface VitalSignsDisplayProps {
  vitalSigns: VitalSign[];
  layout?: 'horizontal' | 'vertical' | 'grid';
  showTrends?: boolean;
  alertOnAbnormal?: boolean;
}

export const VitalSignsDisplay: React.FC<VitalSignsDisplayProps> = ({
  vitalSigns,
  layout = 'grid',
  showTrends = true,
  alertOnAbnormal = true
}) => {
  const getVitalStatus = (vital: VitalSign): 'normal' | 'elevated' | 'critical' => {
    const { value, normalRange } = vital;
    
    if (value < normalRange.min * 0.8 || value > normalRange.max * 1.2) {
      return 'critical';
    } else if (value < normalRange.min || value > normalRange.max) {
      return 'elevated';
    }
    return 'normal';
  };
  
  const renderVitalSign = (vital: VitalSign) => {
    const status = getVitalStatus(vital);
    const statusColor = medicalColors.medical.vital[status];
    
    return (
      <Paper
        key={vital.label}
        sx={{
          p: 2,
          textAlign: 'center',
          backgroundColor: status !== 'normal' 
            ? `${statusColor}08` 
            : medicalColors.background.paper,
          border: status !== 'normal' ? 2 : 1,
          borderColor: status !== 'normal' ? statusColor : 'divider'
        }}
      >
        <Typography variant="caption" color="textSecondary" gutterBottom>
          {vital.label}
        </Typography>
        
        <Typography 
          variant="h4" 
          sx={{ 
            fontFamily: medicalTypography.medicalData.fontFamily,
            fontWeight: 600,
            color: statusColor
          }}
        >
          {vital.value}
          <Typography component="span" variant="body2" sx={{ ml: 0.5 }}>
            {vital.unit}
          </Typography>
        </Typography>
        
        <Typography variant="caption" color="textSecondary">
          Normal: {vital.normalRange.min}-{vital.normalRange.max} {vital.unit}
        </Typography>
        
        {status !== 'normal' && alertOnAbnormal && (
          <Alert 
            severity={status === 'critical' ? 'error' : 'warning'} 
            sx={{ mt: 1, fontSize: '0.75rem' }}
          >
            {status === 'critical' ? 'Valor crítico' : 'Fuera de rango normal'}
          </Alert>
        )}
      </Paper>
    );
  };
  
  const getLayoutStyles = () => {
    switch (layout) {
      case 'horizontal':
        return { display: 'flex', gap: 2, flexWrap: 'wrap' };
      case 'vertical':
        return { display: 'flex', flexDirection: 'column', gap: 2 };
      case 'grid':
      default:
        return { 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: 2 
        };
    }
  };
  
  return (
    <Box sx={getLayoutStyles()}>
      {vitalSigns.map(renderVitalSign)}
    </Box>
  );
};
```

---

## 📱 **Responsive Design Strategy**

### **🎯 Breakpoints Médicos**
```typescript
// theme/breakpoints.ts
export const medicalBreakpoints = {
  values: {
    xs: 0,          // Mobile emergency access
    sm: 600,        // Large phones/small tablets
    md: 900,        // Tablets médicas (main target)
    lg: 1200,       // Desktop workstations
    xl: 1536        // Large displays/dashboards
  }
};

// Responsive patterns para dispositivos médicos
export const useResponsiveLayout = () => {
  const theme = useTheme();
  
  return {
    isMobile: useMediaQuery(theme.breakpoints.down('sm')),
    isTablet: useMediaQuery(theme.breakpoints.between('sm', 'lg')),
    isDesktop: useMediaQuery(theme.breakpoints.up('lg')),
    
    // Medical-specific responsive helpers
    isMedicalTablet: useMediaQuery('(min-width: 768px) and (max-width: 1024px)'),
    isTouch: useMediaQuery('(pointer: coarse)'),
    isLandscape: useMediaQuery('(orientation: landscape)')
  };
};
```

---

## ♿ **Accessibility Features**

### **🎯 WCAG 2.1 AA Compliance**
```typescript
// theme/accessibility.ts
export const accessibilityEnhancements = {
  // High contrast mode support
  contrastRatio: {
    minimum: 4.5,      // WCAG AA standard
    enhanced: 7.0      // Para datos médicos críticos
  },
  
  // Focus indicators enhanced
  focusVisible: {
    outline: `3px solid ${medicalColors.primary.main}`,
    outlineOffset: 2,
    borderRadius: 4
  },
  
  // Touch targets - especially important for medical tablets
  minTouchTarget: 44,  // 44px minimum touch target size
  
  // Motion preferences
  respectsReducedMotion: true,
  
  // Screen reader optimizations
  ariaLabels: {
    required: 'Campo obligatorio según Resolución 3280',
    compliance: 'Estado de cumplimiento normativo',
    criticalData: 'Información médica crítica'
  }
};

// Accessibility hook
export const useA11yFeatures = () => {
  const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');
  const prefersHighContrast = useMediaQuery('(prefers-contrast: high)');
  
  return {
    prefersReducedMotion,
    prefersHighContrast,
    
    // Accessibility helpers
    getAriaProps: (type: 'required' | 'compliance' | 'critical') => ({
      'aria-label': accessibilityEnhancements.ariaLabels[type],
      role: type === 'critical' ? 'status' : undefined,
      'aria-live': type === 'critical' ? 'polite' : undefined
    }),
    
    getFocusProps: () => ({
      sx: {
        '&:focus-visible': accessibilityEnhancements.focusVisible
      }
    })
  };
};
```

---

## 🎨 **Design Tokens System**

### **📏 Spacing & Sizing**
```typescript
// theme/tokens.ts
export const medicalTokens = {
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
    
    // Medical form specific spacing
    formSection: 24,      // Entre secciones formulario
    formField: 16,        // Entre campos relacionados
    criticalMargin: 32    // Para información crítica
  },
  
  borderRadius: {
    small: 4,
    medium: 8,
    large: 12,
    
    // Medical components
    card: 8,
    button: 6,
    input: 4
  },
  
  elevation: {
    card: '0 2px 8px rgba(0,0,0,0.1)',
    modal: '0 8px 32px rgba(0,0,0,0.15)',
    critical: '0 4px 16px rgba(211, 47, 47, 0.2)' // Red shadow for critical
  },
  
  animation: {
    duration: {
      short: 150,
      medium: 300,
      long: 500
    },
    easing: {
      standard: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
      decelerate: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
      accelerate: 'cubic-bezier(0.4, 0.0, 1, 1)'
    }
  }
};
```

---

## 🧪 **Testing Design System**

### **📋 Visual Regression Testing**
```typescript
// __tests__/components/MedicalTextField.stories.test.ts
import { render } from '@testing-library/react';
import { MedicalTextField } from '../components/MedicalTextField';
import { ThemeProvider } from '@mui/material';
import { medicalTheme } from '../theme';

describe('MedicalTextField Visual Tests', () => {
  const renderWithTheme = (component: React.ReactElement) => {
    return render(
      <ThemeProvider theme={medicalTheme}>
        {component}
      </ThemeProvider>
    );
  };
  
  it('should render critical field styling correctly', () => {
    const { container } = renderWithTheme(
      <MedicalTextField
        label="Campo Crítico"
        criticalField
        complianceRule={{ field: 'test', rule: 'required' }}
      />
    );
    
    // Verify critical styling
    const input = container.querySelector('.MuiOutlinedInput-root');
    expect(input).toHaveStyle({
      backgroundColor: medicalColors.background.medical,
      borderWidth: '2px'
    });
  });
  
  it('should meet accessibility contrast requirements', () => {
    const { getByLabelText } = renderWithTheme(
      <MedicalTextField
        label="Test Field"
        value="test"
      />
    );
    
    // Check contrast ratios programmatically
    const input = getByLabelText('Test Field');
    const computedStyles = window.getComputedStyle(input);
    const contrastRatio = calculateContrastRatio(
      computedStyles.color,
      computedStyles.backgroundColor
    );
    
    expect(contrastRatio).toBeGreaterThanOrEqual(4.5);
  });
});
```

---

## 📚 **Design System Documentation**

### **🎨 Storybook Integration**
```typescript
// stories/MedicalComponents.stories.tsx
export default {
  title: 'Medical UI/Form Components',
  component: MedicalTextField,
  parameters: {
    docs: {
      description: {
        component: 'Componente de input especializado para formularios médicos con validación de compliance automática.'
      }
    }
  }
} as ComponentMeta<typeof MedicalTextField>;

export const Default: ComponentStory<typeof MedicalTextField> = (args) => (
  <MedicalTextField {...args} />
);

export const CriticalField: ComponentStory<typeof MedicalTextField> = (args) => (
  <MedicalTextField 
    {...args} 
    criticalField 
    label="Campo Crítico Resolución 3280"
    complianceRule={{ field: 'fecha_nacimiento', rule: 'required' }}
  />
);

export const WithCompliance: ComponentStory<typeof MedicalTextField> = (args) => (
  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
    <MedicalTextField
      label="Estado Compliant"
      value="2023-01-01"
      complianceRule={{ field: 'fecha', rule: 'valid_date' }}
    />
    <MedicalTextField
      label="Estado Violación"
      value="2030-01-01" // Future date - violation
      complianceRule={{ field: 'fecha', rule: 'no_future_date' }}
    />
  </Box>
);
```

---

**🎨 Este design system evoluciona con feedback de profesionales médicos**  
**👥 Mantenido por:** Team Frontend + UX Medical Specialists  
**🎯 Objetivo:** Interfaces que maximizan eficiencia y minimizan errores médicos