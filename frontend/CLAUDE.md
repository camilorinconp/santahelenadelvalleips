# Claude Code - Frontend Configuration

## 🎯 ENTRADA RÁPIDA
**¿Vienes a retomar desarrollo?** → Lee primero: `/DEV-CONTEXT.md`
**¿Necesitas contexto técnico específico?** → Continúa leyendo este archivo

## About This Project

Este es el frontend de la IPS Santa Helena del Valle, una Single Page Application (SPA) desarrollada con React y TypeScript que proporciona la interfaz de usuario para gestionar las Rutas Integrales de Atención en Salud (RIAS) según la normativa colombiana (Resolución 3280 de 2018).

## Architecture

### Core Concepts
- **Domain**: Interfaz de usuario para el sistema de salud colombiano
- **Pattern**: SPA con componentes modulares y reutilizables
- **State Management**: React Query (TanStack Query) para manejo de estado del servidor
- **UI Framework**: Material-UI (MUI) para componentes y diseño

### Application Structure
```
src/
├── components/     # Componentes reutilizables
├── pages/         # Componentes de página completa
├── api/           # Lógica de comunicación con el backend
├── hooks/         # Hooks personalizados de React
├── theme.ts       # Configuración del tema MUI
└── index.tsx      # Entry point de la aplicación
```

## Tech Stack

- **Framework**: React 19.1.1
- **Language**: TypeScript 4.9.5
- **UI Library**: Material-UI (MUI) 7.3.2
- **State Management**: TanStack React Query 5.87.4
- **Form Management**: React Hook Form 7.62.0 + Zod 4.1.5
- **HTTP Client**: Axios 1.11.0
- **Routing**: React Router DOM 7.8.2
- **Build Tool**: Create React App

## Key Files

### Application Core
- `src/index.tsx`: Application entry point with providers setup
- `src/App.tsx`: Main routing and layout configuration
- `src/theme.ts`: Material-UI theme customization

### Components
- `src/components/Layout.tsx`: Main application layout with navigation
- `src/pages/PacientesPage.tsx`: Patient management interface
- `src/pages/PacienteFormPage.tsx`: Patient creation/editing forms
- `src/pages/AtencionesPage.tsx`: Attention management interface

### API Integration
- `src/api/pacientesApi.ts`: Patient-related API calls
- API clients follow consistent patterns for CRUD operations

### Configuration
- `package.json`: Dependencies and scripts
- `tsconfig.json`: TypeScript configuration
- `public/`: Static assets and HTML template

## Development Guidelines

### Component Architecture
1. **Functional Components**: Use React functional components with hooks
2. **TypeScript**: Strict typing for all components and functions
3. **Material-UI**: Consistent use of MUI components and theme system
4. **Form Handling**: React Hook Form + Zod for validation

### API Communication
1. **Centralized API**: All backend calls through dedicated API modules
2. **React Query**: Server state management and caching
3. **Error Handling**: Consistent error handling patterns
4. **Loading States**: Proper loading indicators for async operations

### Code Organization
```typescript
// Component structure example
interface ComponentProps {
  // Props typing
}

const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks
  // Event handlers
  // Render logic
  return (
    // JSX with MUI components
  );
};

export default Component;
```

### Common Commands
**📖 Consultar**: `/docs/02-DEVELOPMENT-WORKFLOW.md` para el flujo completo de desarrollo

```bash
# Setup
cd frontend
npm install

# Development server
npm start

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false

# Build for production
npm run build

# Type checking
npx tsc --noEmit

# Linting (si está configurado)
npm run lint
```

## Current Implementation Status

### ✅ Completed Features
- **Layout System**: Navigation sidebar and header
- **Patient Management**: 
  - Patient listing with DataGrid
  - Create new patient form
  - Edit existing patient form
  - Delete patient functionality
- **Routing**: React Router setup with nested routes
- **Theme System**: Material-UI theme configuration
- **Form Validation**: Zod schemas with React Hook Form

### 🚧 In Progress
- **Attention Management**: Basic structure implemented, needs expansion
- **Form Improvements**: Better validation messages and error handling

### 📋 Planned Features
- **Maternal-Perinatal Care Interface**: Forms for nested polymorphic data
- **Chronic Disease Control**: Specialized forms for different chronic conditions
- **Oncological Screening**: Tamizaje oncológico interfaces
- **Reporting Dashboard**: Analytics and indicators visualization
- **User Authentication**: Login/logout and role-based access
- **Advanced Filtering**: Search and filter capabilities
- **Mobile Responsiveness**: Enhanced mobile experience

## Important Considerations

### Resolution 3280 Compliance
The interface must accommodate the complex data structures required by Colombian health regulations. Form designs should support:
- Nested polymorphic data entry
- Multiple validation rules per field
- Complex workflows for different attention types
- Proper handling of medical terminology in Spanish

### Backend Integration
**📖 Referencias**: Ver `backend/CLAUDE.md` para detalles de integración

- API communication follows RESTful patterns
- All endpoints return consistent JSON responses  
- Error handling matches backend error structures
- Data validation on both client and server sides
- **Polimorfismo**: Frontend debe manejar estructura de datos anidada del backend
- **Compliance**: Formularios deben capturar todos los campos obligatorios según Resolución 3280

### User Experience
- Intuitive navigation for healthcare workers
- Clear form labels and instructions in Spanish
- Responsive design for various screen sizes
- Accessible interface following WCAG guidelines

## Communication Language

**IMPORTANTE**: Toda la comunicación con el asistente de IA debe realizarse en **español**. La aplicación está diseñada para profesionales de la salud en Colombia y toda la interfaz, mensajes y documentación debe estar en español.

## Quick Start para Desarrolladores Frontend

### **📋 Para comenzar inmediatamente:**
1. **Leer documentación crítica** (20 min):
   - `/docs/00-PROJECT-OVERVIEW.md` - Estado actual del proyecto
   - `/docs/01-ARCHITECTURE-GUIDE.md` - Arquitectura técnica completa
   - `backend/CLAUDE.md` - Entender APIs y estructura de datos

2. **Setup del entorno** (10 min):
   ```bash
   cd frontend && npm install && npm start
   # En otra terminal: cd backend && supabase start
   ```

3. **Explorar componentes existentes** (15 min):
   - Revisar `src/pages/PacientesPage.tsx` - Ejemplo de CRUD completo
   - Revisar `src/components/Layout.tsx` - Estructura base
   - Ejecutar `npm test` para ver tests existentes

### **🎯 Para desarrollar nuevas funcionalidades:**
- **Workflow**: `/docs/02-DEVELOPMENT-WORKFLOW.md` - Flujo completo de desarrollo
- **Arquitectura**: `/docs/01-ARCHITECTURE-GUIDE.md` - Patrones de frontend
- **Templates**: `/.github/` - Usar templates de Issues/PRs siempre

## Documentación de Referencia

### **📚 Documentación Reorganizada**

**👉 PUNTO DE ENTRADA:** [Guía Frontend Maestra](docs/01-foundations/frontend-overview.md) ⭐

### **📋 Por Especialización:**
- **`docs/01-foundations/`** - Hub central y arquitectura React base
- **`docs/02-architecture/`** - Patrones React + TypeScript + MUI  
- **`docs/03-integration/`** - Integración backend polimórfico
- **`docs/04-development/`** - Setup, testing, deployment día a día
- **`docs/05-features/`** - Features médicos específicos

### **🔗 Integración con Backend**
- **`../backend/docs/01-foundations/architecture-overview.md`**: Arquitectura backend polimórfica
- **`../backend/CLAUDE.md`**: APIs disponibles y estructura de datos
- **`../backend/docs/02-regulations/resolucion-3280-master.md`**: Compliance requirements

## Notes for AI Assistant

### **🔧 Reglas de Desarrollo Frontend:**
- **Material-UI First**: Usar consistentemente sistema de diseño MUI
- **TypeScript Strict**: Tipado fuerte para todos los componentes
- **React Query**: Manejo de estado del servidor obligatorio
- **React Hook Form + Zod**: Validación de formularios estándar
- **Español Exclusivo**: Toda UI y comunicación en español
- **Compliance Forms**: Formularios deben capturar todos los campos requeridos por Resolución 3280

### **📖 Referencias Obligatorias por Prioridad:**
1. **`docs/01-foundations/frontend-overview.md`** - Hub central y navegación completa ⭐
2. **`docs/03-integration/backend-api-guide.md`** - Integración polimórfica FastAPI
3. **`../backend/docs/02-regulations/resolucion-3280-master.md`** - Compliance requirements
4. **`docs/04-development/setup-guide.md`** - Configuración desarrollo completa

### **🎨 Consideraciones UX/UI:**
- **Profesionales de Salud**: Interfaces optimizadas para personal médico
- **Datos Complejos**: Manejar polimorfismo anidado del backend elegantemente
- **Validación Inteligente**: Validaciones en tiempo real sin ser intrusivas
- **Accesibilidad**: Cumplir WCAG guidelines para inclusividad