# 🛠️ Database Development Scripts

**📅 Última actualización:** 14 septiembre 2025  
**🎯 Propósito:** Scripts automatizados para desarrollo y mantenimiento database  
**📍 Audiencia:** Database Developers, DevOps Engineers, Development Team  

---

## 📋 **Scripts Disponibles**

### **🏥 [health-check.sh](health-check.sh)**
**Verificación completa de salud del sistema database**

```bash
# Health check básico
./health-check.sh

# Health check detallado
./health-check.sh --detailed

# Exportar reporte
./health-check.sh --detailed --export-report
```

**Verifica:**
- ✅ Servicios Supabase funcionando
- ✅ Conectividad database
- ✅ Estado migraciones
- ✅ Salud tablas críticas
- ✅ Performance issues
- ✅ Tests básicos

### **💾 [backup-database.sh](backup-database.sh)**
**Sistema completo de backup database con múltiples estrategias**

```bash
# Backup completo
./backup-database.sh --type=full --compress

# Solo schema
./backup-database.sh --type=schema

# Solo datos
./backup-database.sh --type=data

# Backup incremental
./backup-database.sh --type=incremental --compress

# Backup con upload a cloud
./backup-database.sh --type=full --compress --upload
```

**Características:**
- 🔄 Múltiples tipos: full, schema, data, incremental
- 📦 Compresión automática con gzip
- ☁️ Upload a cloud storage (AWS, GCP, Azure)
- 🗑️ Limpieza automática backups antiguos
- 📋 Manifest detallado por sesión

### **🚀 [dev-setup.sh](dev-setup.sh)**
**Configuración automatizada entorno desarrollo completo**

```bash
# Setup básico
./dev-setup.sh

# Reset completo + setup
./dev-setup.sh --reset

# Setup con datos de ejemplo
./dev-setup.sh --with-data

# Reset + datos + skip dependencias
./dev-setup.sh --reset --with-data --skip-deps
```

**Incluye:**
- 🔍 Verificación dependencias automática
- 🚀 Configuración servicios Supabase
- 📋 Aplicación migraciones
- 🏗️ Verificación estructura database
- 📊 Carga datos de ejemplo (opcional)
- 📝 Archivos environment (.env)
- ⚡ Shortcuts desarrollo

---

## ⚡ **Quick Commands Reference**

### **🔥 Comandos Más Frecuentes:**
```bash
# Setup completo nuevo desarrollador
./dev-setup.sh --reset --with-data

# Health check diario
./health-check.sh --detailed

# Backup antes de cambios importantes  
./backup-database.sh --type=full --compress

# Reset rápido para testing
./shortcuts/reset-db.sh
```

### **🆘 Comandos Emergencia:**
```bash
# Diagnóstico completo problema
./health-check.sh --detailed --export-report

# Backup emergencia
./backup-database.sh --type=full --compress --upload

# Setup desde cero (CUIDADO: borra todo)
./dev-setup.sh --reset
```

---

## 📊 **Uso por Escenarios**

### **👨‍💻 Nuevo Desarrollador:**
1. **Primera vez:**
   ```bash
   ./dev-setup.sh --with-data
   ```
   - Configura todo automáticamente
   - Carga datos de ejemplo para testing
   - Crea shortcuts útiles

2. **Verificar que todo funciona:**
   ```bash
   ./health-check.sh --detailed
   ```

3. **Iniciar desarrollo:**
   ```bash
   ./shortcuts/start-all.sh
   ```

### **🔄 Desarrollo Diario:**
1. **Health check matutino:**
   ```bash
   ./health-check.sh
   ```

2. **Backup antes de cambios grandes:**
   ```bash
   ./backup-database.sh --type=full --compress
   ```

3. **Reset database para testing:**
   ```bash
   ./shortcuts/reset-db.sh
   ```

### **🚨 Resolución Problemas:**
1. **Diagnóstico completo:**
   ```bash
   ./health-check.sh --detailed --export-report
   ```

2. **Reset completo si hay corrupción:**
   ```bash
   ./dev-setup.sh --reset
   ```

3. **Verificar después del fix:**
   ```bash
   ./health-check.sh --detailed
   ```

### **📦 Deployment/Production:**
1. **Backup pre-deployment:**
   ```bash
   ./backup-database.sh --type=full --compress --upload
   ```

2. **Verificación post-deployment:**
   ```bash
   ./health-check.sh --detailed
   ```

---

## 🛡️ **Configuración Seguridad**

### **🔒 Configuración Backup Cloud:**
Para habilitar upload automático a cloud storage, configura en `backup-database.sh`:

```bash
# AWS S3
CLOUD_PROVIDER="aws"
CLOUD_BUCKET="your-backup-bucket"
CLOUD_REGION="us-west-2"

# Google Cloud Storage  
CLOUD_PROVIDER="gcp"
CLOUD_BUCKET="your-backup-bucket"
CLOUD_REGION="us-central1"

# Azure Blob Storage
CLOUD_PROVIDER="azure"
CLOUD_BUCKET="your-backup-container"
CLOUD_REGION="eastus"
```

### **📊 Configuración Monitoring:**
Los scripts generan logs y métricas para monitoring:
- `../reports/health_check_*.txt` - Reportes health check
- `../backups/backup_manifest_*.json` - Manifests backup
- `../logs/script_execution_*.log` - Logs de ejecución

---

## 📁 **Estructura Directorios Generados**

```
supabase/
├── scripts/                    # Scripts principales
│   ├── health-check.sh        # Health check sistema
│   ├── backup-database.sh     # Backup strategies  
│   ├── dev-setup.sh          # Setup automatizado
│   └── README.md             # Esta documentación
│
├── shortcuts/                 # Scripts rapidos (generados)
│   ├── start-all.sh          # Iniciar stack completo
│   ├── reset-db.sh           # Reset rápido database
│   ├── quick-backup.sh       # Backup rápido
│   └── health-check.sh       # Health check wrapper
│
├── backups/                   # Backups database (generados)
│   ├── full_backup_*.sql     # Backups completos
│   ├── schema_backup_*.sql   # Backups schema
│   ├── data_backup_*.sql     # Backups datos
│   └── backup_manifest_*.json # Manifests
│
├── reports/                   # Reportes sistema (generados)
│   └── health_check_*.txt    # Health check reports
│
└── temp/                      # Archivos temporales (generados)
    └── sample_data_*.sql     # Datos ejemplo
```

---

## 🔧 **Customización Scripts**

### **🎛️ Variables Configurables:**

**Database Connection (todos los scripts):**
```bash
DB_HOST="127.0.0.1"       # Host database
DB_PORT="54322"           # Puerto database
DB_NAME="postgres"        # Nombre database
DB_USER="postgres"        # Usuario database
DB_PASSWORD="postgres"    # Password database
```

**Health Check:**
```bash
DETAILED_MODE=true        # Modo detallado por defecto
EXPORT_REPORT=true        # Exportar reportes automáticamente
```

**Backup:**
```bash
RETENTION_DAYS=30         # Días retención backups
COMPRESS=true             # Compresión por defecto
UPLOAD=false              # Upload cloud por defecto
```

**Dev Setup:**
```bash
WITH_SAMPLE_DATA=true     # Cargar datos ejemplo
SKIP_DEPENDENCIES=false   # Verificar dependencias
```

### **🔌 Extensiones Scripts:**
Para agregar funcionalidad custom, modifica las funciones:
- `check_custom_requirements()` - Verificaciones adicionales
- `custom_backup_processing()` - Post-procesamiento backup
- `load_custom_sample_data()` - Datos ejemplo específicos

---

## 📚 **Troubleshooting Scripts**

### **❌ Problemas Comunes:**

**"command not found: supabase"**
```bash
# Instalar Supabase CLI
npm install -g @supabase/cli
# O usando brew en macOS
brew install supabase/tap/supabase
```

**"connection refused" database**
```bash
# Verificar servicios
supabase status
# Reiniciar si es necesario
supabase stop && supabase start
```

**Scripts no ejecutables**
```bash
# Hacer ejecutables
chmod +x scripts/*.sh
chmod +x shortcuts/*.sh
```

**Error permisos backup**
```bash
# Verificar permisos directorio
mkdir -p backups reports temp shortcuts
chmod 755 backups reports temp shortcuts
```

### **🔍 Debug Mode:**
Para debug detallado, agregar al inicio de cualquier script:
```bash
set -x  # Mostrar comandos ejecutados
```

---

## 🎯 **Mejores Prácticas**

### **✅ Uso Recomendado:**
1. **Health check diario** antes de comenzar desarrollo
2. **Backup antes de cambios** importantes o migraciones
3. **Reset database frecuente** para mantener consistencia
4. **Reportes exportados** para tracking de issues
5. **Scripts shortcuts** para operaciones repetitivas

### **⚠️ Precauciones:**
- **--reset borra TODOS los datos** - usar solo en desarrollo
- **Backup con --upload** verifica configuración cloud
- **Health check --export-report** genera archivos grandes
- **Dev setup --skip-deps** puede causar errores

### **🔄 Mantenimiento Scripts:**
- **Actualizar configuración** según ambiente
- **Revisar logs regularmente** en directorio reports/  
- **Limpiar backups antiguos** según política retención
- **Testear scripts** después de cambios en database

---

**🛠️ Scripts diseñados para máxima productividad desarrollo database**  
**👥 Maintained by:** Database Operations Team  
**🚀 Automation level:** 90% operaciones rutinarias automatizadas  
**📊 Success metric:** <5 min setup nuevo desarrollador + zero-effort daily operations