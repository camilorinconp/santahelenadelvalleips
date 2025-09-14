# ⚡ Setup Guide Frontend - Desarrollo Médico

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Configuración completa desarrollo frontend React médico  
**📍 Tiempo estimado:** 15 minutos setup completo  

---

## 🎯 **Setup Rápido (TL;DR)**

```bash
# 1. Clonar y navegar
git clone https://github.com/camilorinconp/santahelenadelvalleips.git
cd santahelenadelvalleips/frontend

# 2. Instalar dependencias
npm install

# 3. Configurar entorno
cp .env.example .env.local
# Editar variables de entorno

# 4. Iniciar desarrollo
npm start
# ✅ Frontend disponible en http://localhost:3000

# 5. En paralelo: Backend + BD (terminal separado)
cd ../backend && uvicorn main:app --reload
cd ../supabase && supabase start
```

---

## 🔧 **Prerrequisitos**

### **📋 Software Requerido:**
- **Node.js:** >= 18.0.0 (LTS recomendado)
- **npm:** >= 9.0.0 (incluido con Node.js)
- **Git:** Última versión
- **IDE:** VSCode recomendado + extensiones

### **🔍 Verificar Versiones:**
```bash
node --version    # Should be >= 18.0.0
npm --version     # Should be >= 9.0.0
git --version     # Any recent version
```

---

## 📦 **Instalación Dependencias**

### **🚀 Core Dependencies:**
```json
{
  "dependencies": {
    "react": "19.1.1",
    "typescript": "4.9.5", 
    "@mui/material": "7.3.2",
    "@tanstack/react-query": "5.87.4",
    "react-hook-form": "7.62.0",
    "zod": "4.1.5",
    "react-router-dom": "7.8.2",
    "axios": "1.11.0"
  }
}
```

### **⚙️ Instalación:**
```bash
# Install all dependencies
npm install

# Verify installation
npm list --depth=0

# Check for vulnerabilities 
npm audit
```

---

## ⚙️ **Configuración Entorno**

### **📝 Variables de Entorno:**
```bash
# .env.local - Configuración desarrollo local
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SUPABASE_URL=http://localhost:54321
REACT_APP_SUPABASE_ANON_KEY=your_anon_key_here

# Medical app specific
REACT_APP_MEDICAL_APP_NAME="IPS Santa Helena del Valle"
REACT_APP_COMPLIANCE_MODE=strict
REACT_APP_DEFAULT_PROFILE=CLINICO

# Development flags
REACT_APP_DEBUG_MODE=true
REACT_APP_ENABLE_DEVTOOLS=true
REACT_APP_MOCK_API=false

# Performance monitoring
REACT_APP_ENABLE_PERFORMANCE_MONITORING=true
REACT_APP_ENABLE_ERROR_REPORTING=true
```

### **🔒 Configuración Segura:**
```bash
# .env.example - Template público (versionado)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_anon_key

# .env.local - Configuración real (NO versionado)
# Copiar desde .env.example y llenar valores reales
```

---

## 💻 **IDE Setup (VSCode)**

### **📦 Extensiones Esenciales:**
```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode", 
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "ms-vscode.vscode-eslint"
  ]
}
```

### **⚙️ VSCode Settings:**
```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "emmet.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  },
  "typescript.suggest.autoImports": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true
}
```

### **🔧 Launch Configuration:**
```json
// .vscode/launch.json - Debug configuration
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch React App",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/react-scripts",
      "args": ["start"],
      "env": {
        "NODE_ENV": "development"
      },
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
  ]
}
```

---

## 🚀 **Scripts Desarrollo**

### **📋 Scripts Disponibles:**
```bash
# Development
npm start                    # Servidor desarrollo (http://localhost:3000)
npm run dev                  # Alias para npm start

# Testing  
npm test                     # Testing interactivo
npm run test:coverage        # Coverage report
npm run test:ci             # Testing CI/CD mode

# Build
npm run build               # Build producción
npm run build:analyze       # Build + bundle analyzer

# Type Checking
npm run type-check          # TypeScript validation sin build
npm run type-check:watch    # TypeScript validation modo watch

# Linting & Formatting
npm run lint                # ESLint check
npm run lint:fix           # ESLint fix automático
npm run format             # Prettier formatting

# Performance
npm run lighthouse         # Performance audit
npm run bundle-analyzer    # Analyze bundle size
```

### **🔧 Custom Scripts Package.json:**
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "lint": "eslint src --ext .ts,.tsx,.js,.jsx",
    "lint:fix": "eslint src --ext .ts,.tsx,.js,.jsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    
    "test:coverage": "npm test -- --coverage --watchAll=false",
    "test:ci": "npm test -- --ci --coverage --watchAll=false",
    
    "build:analyze": "npm run build && npx source-map-explorer 'build/static/js/*.js'",
    "lighthouse": "lhci autorun",
    
    "medical:setup": "node scripts/medical-setup.js",
    "medical:validate": "node scripts/validate-compliance.js"
  }
}
```

---

## 🔗 **Integración Backend**

### **🔄 Desarrollo Concurrente:**
```bash
# Terminal 1: Frontend
cd frontend
npm start

# Terminal 2: Backend  
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 3: Base de datos
cd supabase  
supabase start

# Verificar integración
curl http://localhost:8000/api/pacientes  # Backend OK
curl http://localhost:3000                # Frontend OK
```

### **🔍 Health Check Script:**
```bash
# scripts/health-check.sh
#!/bin/bash

echo "🔍 Checking development environment..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
  echo "✅ Backend running on :8000"
else
  echo "❌ Backend not running on :8000"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
  echo "✅ Frontend running on :3000" 
else
  echo "❌ Frontend not running on :3000"
fi

# Check database
if curl -s http://localhost:54321/health > /dev/null; then
  echo "✅ Supabase running on :54321"
else
  echo "❌ Supabase not running on :54321"
fi

echo "🏥 Medical development stack ready!"
```

---

## 🧪 **Testing Setup**

### **📋 Testing Configuration:**
```typescript
// src/setupTests.ts
import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Mock server setup
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});
```

### **🎭 MSW Mock Setup:**
```typescript
// src/mocks/handlers.ts - API mocking para desarrollo
import { rest } from 'msw';
import { mockPacientes, mockAtenciones } from './data/medical';

export const handlers = [
  // Pacientes endpoints
  rest.get('/api/pacientes', (req, res, ctx) => {
    return res(ctx.json(mockPacientes));
  }),
  
  rest.get('/api/pacientes/:id', (req, res, ctx) => {
    const { id } = req.params;
    const paciente = mockPacientes.find(p => p.id === id);
    
    if (!paciente) {
      return res(ctx.status(404), ctx.json({ detail: 'Paciente no encontrado' }));
    }
    
    return res(ctx.json(paciente));
  }),
  
  // Atenciones polimórficas
  rest.get('/api/atenciones', (req, res, ctx) => {
    const pacienteId = req.url.searchParams.get('paciente_id');
    const atenciones = mockAtenciones.filter(a => 
      !pacienteId || a.paciente_id === pacienteId
    );
    
    return res(ctx.json(atenciones));
  }),
  
  rest.post('/api/atencion-materno-perinatal', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({
      id: `detalle-${Date.now()}`,
      ...req.body
    }));
  })
];
```

---

## 🔧 **Troubleshooting**

### **❌ Problemas Comunes:**

#### **Puerto 3000 ocupado:**
```bash
# Encontrar proceso usando puerto
lsof -ti:3000

# Matar proceso
kill -9 $(lsof -ti:3000)

# O usar puerto diferente
PORT=3001 npm start
```

#### **Errores TypeScript:**
```bash
# Limpiar cache TypeScript
rm -rf node_modules/.cache
npm start

# Regenerar tipos
npm run type-check
```

#### **Problemas de dependencias:**
```bash
# Limpiar node_modules
rm -rf node_modules package-lock.json
npm install

# Verificar vulnerabilidades
npm audit fix
```

#### **Problemas CORS con backend:**
```typescript
// En desarrollo, el proxy automático debería funcionar
// Si no funciona, verificar package.json:
{
  "proxy": "http://localhost:8000"
}
```

### **🔍 Debug Tools:**
```bash
# React DevTools
npm install -g react-devtools

# Bundle analyzer
npm install -g source-map-explorer

# Performance profiling
npm install -g clinic
clinic doctor -- npm start
```

---

## 📊 **Métricas Setup Success**

### **✅ Checklist Verification:**
- [ ] Node.js >= 18.0.0 instalado
- [ ] npm install sin errores
- [ ] npm start ejecuta sin problemas  
- [ ] http://localhost:3000 carga correctamente
- [ ] Backend integration funciona
- [ ] TypeScript compila sin errores
- [ ] Tests ejecutan exitosamente
- [ ] VSCode configurado con extensiones
- [ ] Variables de entorno configuradas
- [ ] Mock API responde correctamente

### **📈 Performance Targets:**
- **Build time:** < 2 minutos
- **Hot reload:** < 3 segundos  
- **Bundle size:** < 3MB (gzipped)
- **Lighthouse score:** > 90
- **Test execution:** < 30 segundos

### **🎯 Development Ready Indicators:**
```bash
✅ Frontend: http://localhost:3000 (React app)
✅ Backend: http://localhost:8000 (FastAPI)
✅ Database: http://localhost:54321 (Supabase)
✅ Tests: npm test (passing)
✅ Types: npm run type-check (no errors)
✅ Build: npm run build (successful)
```

---

**⚡ Setup completado exitosamente - Ready para desarrollo médico!**  
**👥 Support:** Team Frontend Principal  
**🎯 Next:** [Component Patterns](../02-architecture/component-patterns.md) para empezar desarrollo