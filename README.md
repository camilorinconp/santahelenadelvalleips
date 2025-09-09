# API de Gestión para Santa Helena del Valle IPS

API para la gestión de pacientes, médicos y atenciones de la IPS Santa Helena del Valle. El proyecto utiliza FastAPI y se conecta a una base de datos PostgreSQL gestionada por Supabase.

## Estado del Proyecto

En desarrollo activo. La funcionalidad para Pacientes y Atenciones individuales está completa y estable. Se ha definido el modelo de datos y la estructura de base de datos para la gestión de Intervenciones Colectivas, alineando el proyecto con los requerimientos de la Resolución 3280.

## Stack Tecnológico

- **Backend:** Python 3.12
- **Framework:** FastAPI
- **Base de Datos:** PostgreSQL (a través de Supabase)
- **Testing:** Pytest
- **Servidor ASGI:** Uvicorn

---

## Configuración del Entorno Local

Sigue estos pasos para configurar el proyecto en tu máquina.

### 1. Prerrequisitos

- Tener Python 3.12 o superior instalado.
- Tener Git instalado.

### 2. Clonar el Repositorio

```bash
git clone https://github.com/camilorinconp/santahelenadelvalleips.git
cd santahelenadelvalleips
```

### 3. Crear y Activar Entorno Virtual

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar en macOS/Linux
source venv/bin/activate

# (Si usas Windows, el comando es: .\venv\Scripts\activate)
```

### 4. Instalar Dependencias

Crea un archivo `.env` a partir del ejemplo y luego instala los paquetes requeridos.

```bash
# (Asegúrate de rellenar .env con tus credenciales de Supabase)
cp .env.example .env

# Instalar paquetes
pip install -r requirements.txt
```

---

## Cómo Ejecutar la Aplicación

Con el entorno virtual activado, ejecuta el siguiente comando para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

La documentación interactiva (Swagger UI) se encuentra en `http://127.0.0.1:8000/docs`.

## Cómo Ejecutar las Pruebas

Para verificar que todo funciona correctamente, ejecuta el conjunto de pruebas automatizadas:

```bash
pytest -v
```
