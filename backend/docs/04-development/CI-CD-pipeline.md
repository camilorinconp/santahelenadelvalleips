# Guía de Implementación de CI/CD

**📅 Última actualización:** 2025-09-17  
**🎯 Propósito:** Guía técnica para evolucionar el pipeline actual a un sistema de CI/CD completo y automatizado.

---

## 1. Estado Actual (Auditoría)

El proyecto cuenta con una base de CI (Integración Continua) para el backend, pero carece de un pipeline de CD (Despliegue Continuo).

- **✅ Fortalezas:**
  - Existe un workflow (`ci.yml`) que ejecuta los tests del backend (`pytest`) de forma automática.
  - Utiliza correctamente servicios (PostgreSQL) y secretos de GitHub para las pruebas.
  - Existe un workflow de gobernanza (`architectural-review.yml`) muy maduro.

- **❌ Brechas y Ausencias:**
  - **No hay CI para el Frontend:** No se instalan dependencias ni se ejecutan tests de React.
  - **No hay Linting:** No se valida el estilo del código de forma automática.
  - **No hay Despliegue Continuo (CD):** La imagen de Docker se construye pero no se publica. No hay despliegue automático a ningún entorno.
  - **Migraciones Manuales:** Las migraciones de la base de datos (`supabase db push`) no están automatizadas.

---

## 2. Arquitectura Objetivo del Pipeline

El objetivo es un pipeline que automatice el ciclo completo: **Test -> Build -> Deploy**.

```mermaid
graph TD
    A[Push a `develop` o PR a `main`] --> B{Ejecutar CI};
    B --> C[🧪 Test Backend];
    B --> D[🧪 Test Frontend];
    C --> E{Éxito?};
    D --> E;
    E -- ✅ Pasa --> F[🚀 Iniciar Proceso de Despliegue (Solo en merge a `main`)];
    E -- ❌ Falla --> G[⛔ Notificar Fallo];
    
    subgraph Proceso de Despliegue
        F --> H[1. Construir y Publicar Imagen Docker];
        H --> I[2. Ejecutar Migraciones de BD (`supabase db push`)];
        I --> J[3. Desplegar Nueva Versión de la Aplicación];
    end

    J --> K[✅ Despliegue Exitoso];
```

---

## 3. Plan de Implementación Detallado

A continuación se presentan los cambios exactos necesarios en el archivo `.github/workflows/ci.yml`.

### Paso 1: Completar la Integración Continua (CI)

#### Tarea 1.1: Añadir Linting al Backend

Modifique el job `test-backend` para añadir un paso de linting con `ruff` antes de los tests.

```yaml
    # ... (dentro del job test-backend, después de instalar dependencias)
    - name: 🎨 Lint with ruff
      run: |
        cd backend
        pip install ruff
        ruff check .
```

#### Tarea 1.2: Crear Job de Pruebas para Frontend

Añada un nuevo job completo al archivo `ci.yml` que se ejecute en paralelo al del backend.

```yaml
  # =============================================================================
  # TESTING - Frontend App
  # =============================================================================
  test-frontend:
    name: ⚛️ Test Frontend App
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🟢 Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: 📦 Install dependencies
      run: |
        cd frontend
        npm install

    - name: 🧪 Run tests with npm
      run: |
        cd frontend
        npm test -- --watchAll=false
```

### Paso 2: Implementar el Despliegue Continuo (CD)

#### Tarea 2.1: Publicar Imagen Docker en GHCR

Modifique el job `build-docker` para que inicie sesión en el Registro de Contenedores de GitHub (GHCR) y publique la imagen.

```yaml
  # ... (en el job build-docker)
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🔐 Login to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: 🐳 Setup Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: 🏗️ Build and Push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true  # <--- CAMBIO CLAVE
        tags: ghcr.io/${{ github.repository }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

#### Tarea 2.2: Crear Job para Migraciones y Despliegue

Añada un nuevo job al final del archivo `ci.yml` que dependa de la construcción exitosa de la imagen.

```yaml
  # =============================================================================
  # DEPLOY - Staging/Production
  # =============================================================================
  deploy:
    name: 🚀 Deploy to Production
    runs-on: ubuntu-latest
    needs: [test-frontend, build-docker] # Depende de los tests y el build
    if: github.ref == 'refs/heads/main' # Solo se ejecuta en merges a main

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🗄️ Apply Database Migrations
      uses: supabase/cli@v1
      with:
        args: db push
        # El token de acceso debe tener permisos para ejecutar migraciones.
        access-token: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

    - name: ☁️ Deploy to Cloud Provider
      # Este paso es un EJEMPLO y depende de su proveedor de hosting.
      # Aquí se usaría SSH, kubectl, etc., para desplegar el contenedor.
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.DEPLOY_HOST }}
        username: ${{ secrets.DEPLOY_USERNAME }}
        key: ${{ secrets.DEPLOY_SSH_KEY }}
        script: |
          echo "Iniciando despliegue..."
          docker login ghcr.io -u ${{ github.actor }} -p ${{ secrets.GITHUB_TOKEN }}
          docker pull ghcr.io/${{ github.repository }}:latest
          # Detener y reiniciar el contenedor (ejemplo con docker-compose)
          docker-compose -f /path/to/your/docker-compose.prod.yml down
          docker-compose -f /path/to/your/docker-compose.prod.yml up -d
          echo "Despliegue completado."
```

---

## 4. Gestión de Secretos

Para que este pipeline funcione, se deben configurar los siguientes secretos en la configuración de su repositorio de GitHub (`Settings > Secrets and variables > Actions`):

- `SUPABASE_ACCESS_TOKEN`: Un token de acceso de Supabase con permisos para ejecutar migraciones. Se puede generar en `Account > Tokens` en su dashboard de Supabase.
- `DEPLOY_HOST`: La dirección IP o el hostname de su servidor de producción.
- `DEPLOY_USERNAME`: El usuario para conectar por SSH al servidor.
- `DEPLOY_SSH_KEY`: La clave privada SSH para autenticarse en el servidor.
- `GITHUB_TOKEN`: Este secreto ya existe por defecto y tiene permisos para publicar en el GHCR del repositorio.

Con estos cambios, el proyecto tendrá un pipeline de CI/CD robusto, seguro y completamente automatizado.
