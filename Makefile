# =============================================================================
# Makefile - IPS Santa Helena del Valle
# Comandos de desarrollo y deployment simplificados
# =============================================================================

.PHONY: help setup dev test build docker-build docker-run clean lint health

# Variables
PYTHON := python3
PIP := pip
NODE := npm
DOCKER := docker
COMPOSE := docker-compose

# Default target
help:
	@echo "🏥 IPS Santa Helena del Valle - Development Commands"
	@echo ""
	@echo "📋 Setup y Configuración:"
	@echo "  setup          Configurar entorno de desarrollo completo"
	@echo "  install        Instalar dependencias solamente"
	@echo ""
	@echo "🚀 Desarrollo:"
	@echo "  dev            Iniciar servidor de desarrollo"
	@echo "  dev-backend    Iniciar solo backend"
	@echo "  dev-frontend   Iniciar solo frontend"
	@echo "  dev-full       Iniciar backend + frontend"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test           Ejecutar todos los tests"
	@echo "  test-backend   Ejecutar tests del backend"
	@echo "  test-coverage  Ejecutar tests con coverage"
	@echo "  lint           Ejecutar linting y formateo"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker-build   Construir imágenes Docker"
	@echo "  docker-dev     Iniciar en modo desarrollo con Docker"
	@echo "  docker-prod    Iniciar en modo producción con Docker"
	@echo "  docker-clean   Limpiar contenedores e imágenes"
	@echo ""
	@echo "🔧 Utilidades:"
	@echo "  health         Verificar estado del sistema"
	@echo "  logs           Ver logs de la aplicación"
	@echo "  db-reset       Resetear base de datos local"
	@echo "  clean          Limpiar archivos temporales"
	@echo ""
	@echo "📚 Documentación:"
	@echo "  docs           Generar documentación"
	@echo "  api-docs       Abrir documentación de API"

# =============================================================================
# SETUP Y CONFIGURACIÓN
# =============================================================================

setup:
	@echo "🚀 Configurando entorno de desarrollo..."
	@./scripts/dev-setup.sh

install: install-backend install-frontend

install-backend:
	@echo "📦 Instalando dependencias del backend..."
	@cd backend && $(PYTHON) -m venv venv || true
	@cd backend && source venv/bin/activate && $(PIP) install --upgrade pip
	@cd backend && source venv/bin/activate && $(PIP) install -r requirements.txt

install-frontend:
	@echo "📦 Instalando dependencias del frontend..."
	@if [ -d "frontend" ]; then cd frontend && $(NODE) install; fi

# =============================================================================
# DESARROLLO
# =============================================================================

dev: dev-backend

dev-backend:
	@echo "🚀 Iniciando servidor de desarrollo (backend)..."
	@cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "🚀 Iniciando servidor de desarrollo (frontend)..."
	@if [ -d "frontend" ]; then cd frontend && $(NODE) start; else echo "❌ Frontend no configurado"; fi

dev-full:
	@echo "🚀 Iniciando desarrollo full-stack..."
	@$(MAKE) -j2 dev-backend dev-frontend

# =============================================================================
# TESTING
# =============================================================================

test: test-backend

test-backend:
	@echo "🧪 Ejecutando tests del backend..."
	@cd backend && source venv/bin/activate && pytest -v

test-coverage:
	@echo "🧪 Ejecutando tests con coverage..."
	@cd backend && source venv/bin/activate && pytest --cov=. --cov-report=html --cov-report=term

test-ci:
	@echo "🧪 Ejecutando tests para CI..."
	@cd backend && source venv/bin/activate && pytest -v --tb=short

lint:
	@echo "🔍 Ejecutando linting..."
	@cd backend && source venv/bin/activate && python -m ruff check .
	@echo "✅ Linting completado"

format:
	@echo "🎨 Formateando código..."
	@cd backend && source venv/bin/activate && python -m ruff format .
	@echo "✅ Formateo completado"

# =============================================================================
# DOCKER
# =============================================================================

docker-build:
	@echo "🐳 Construyendo imágenes Docker..."
	@$(COMPOSE) build

docker-dev:
	@echo "🐳 Iniciando desarrollo con Docker..."
	@./scripts/docker-dev.sh start

docker-prod:
	@echo "🐳 Iniciando producción con Docker..."
	@$(COMPOSE) --profile production up -d

docker-stop:
	@echo "🐳 Deteniendo contenedores Docker..."
	@$(COMPOSE) down

docker-clean:
	@echo "🐳 Limpiando Docker..."
	@./scripts/docker-dev.sh clean

docker-logs:
	@echo "🐳 Mostrando logs de Docker..."
	@$(COMPOSE) logs -f --tail=50

# =============================================================================
# BASE DE DATOS
# =============================================================================

db-start:
	@echo "🗃️ Iniciando Supabase local..."
	@cd supabase && supabase start

db-stop:
	@echo "🗃️ Deteniendo Supabase local..."
	@cd supabase && supabase stop

db-reset:
	@echo "🗃️ Reseteando base de datos local..."
	@cd supabase && supabase db reset

db-migrate:
	@echo "🗃️ Aplicando migraciones..."
	@cd supabase && supabase db push

db-status:
	@echo "🗃️ Estado de Supabase..."
	@cd supabase && supabase status

# =============================================================================
# UTILIDADES
# =============================================================================

health:
	@echo "🏥 Verificando estado del sistema..."
	@./scripts/health-check.sh

logs:
	@echo "📋 Mostrando logs de la aplicación..."
	@if [ -f "app.log" ]; then tail -f app.log; else echo "No se encontraron logs"; fi

clean:
	@echo "🧹 Limpiando archivos temporales..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@find . -name "*.log" -delete 2>/dev/null || true
	@if [ -d "frontend/node_modules" ]; then rm -rf frontend/node_modules; fi
	@if [ -d "frontend/build" ]; then rm -rf frontend/build; fi
	@echo "✅ Limpieza completada"

# =============================================================================
# DOCUMENTACIÓN
# =============================================================================

docs:
	@echo "📚 Abriendo documentación principal..."
	@open backend/CLAUDE.md || echo "Ver: backend/CLAUDE.md"

api-docs:
	@echo "📚 Abriendo documentación de API..."
	@open http://localhost:8000/docs || echo "API Docs: http://localhost:8000/docs"

# =============================================================================
# QUICK COMMANDS
# =============================================================================

start: dev-backend
stop: docker-stop db-stop
restart: stop start
status: health

# Comandos de un solo carácter para desarrollo rápido
s: start
t: test
b: docker-build
h: health
c: clean