# Frontend IPS Santa Helena del Valle

## 🎯 **Inicio Rápido - Arquitectura Frontend Completa**

👉 **Para entender la arquitectura completa del frontend:**  
📖 **[🎨 Ver Guía Frontend Maestra](docs/01-foundations/frontend-overview.md)** ⭐

Single Page Application (React + TypeScript) para gestión de RIAS con interfaces especializadas por perfil de usuario (Clínico + Call Center) y integración polimórfica con backend FastAPI.

## 🔧 **Configuración AI Assistant**
- 📋 [Configuración Frontend](CLAUDE.md) - Setup desarrollo React con AI
- 🧠 [Contexto Técnico](GEMINI.md) - Historia arquitectónica frontend

## 📚 **Documentación Organizada**
La documentación técnica está estructurada por especialización:
- **`docs/01-foundations/`** - Hub central y arquitectura React base
- **`docs/02-architecture/`** - Patrones React + TypeScript + MUI  
- **`docs/03-integration/`** - Integración backend polimórfico
- **`docs/04-development/`** - Setup, testing, deployment día a día
- **`docs/05-features/`** - Features médicos específicos implementados

---

## ⚡ **Setup Rápido Desarrollo**

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar desarrollo
npm start
# Aplicación disponible en http://localhost:3000

# 3. En paralelo: backend + BD
cd ../backend && uvicorn main:app --reload
cd ../supabase && supabase start
```

## 📊 **Estado Actual**
- **✅ Completado:** Gestión pacientes (CRUD 100%), Layout sistema, Form patterns
- **🚧 En desarrollo:** Workflows atención médica, Forms polimórficos  
- **📋 Pendiente:** Dual profiles UI, Dashboard reportería

## 🎯 **Stack Tecnológico**
- **Framework:** React 19 + TypeScript 4.9
- **UI Library:** Material-UI 7.3
- **State Management:** TanStack React Query 5.8
- **Forms:** React Hook Form + Zod validation
- **Integration:** Axios → FastAPI backend

## 🔧 **Comandos Esenciales**

```bash
npm start                    # Servidor desarrollo
npm test                     # Testing interactivo  
npm run build               # Build producción
npm test -- --coverage     # Coverage completo
npx tsc --noEmit           # Type checking
```

## 🔗 **Referencias Backend**
- **[Backend Overview](../backend/docs/01-foundations/architecture-overview.md)** - Arquitectura polimórfica  
- **[Backend APIs](../backend/CLAUDE.md)** - Endpoints disponibles
- **[Resolución 3280](../backend/docs/02-regulations/resolucion-3280-master.md)** - Compliance requirements

---

**📖 Para arquitectura completa, patrones React, integración backend y roadmap detallado:**  
**➡️ [Consultar Guía Frontend Maestra](docs/01-foundations/frontend-overview.md)**