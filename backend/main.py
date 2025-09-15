from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pacientes, atenciones, intervenciones_colectivas, atencion_primera_infancia, atencion_materno_perinatal, tamizaje_oncologico, control_cronicidad, entornos_salud_publica, familia_integral_salud_publica, atencion_integral_transversal_salud, catalogo_ocupaciones_simple #, medicos, codigos_rias

# Importar configuración de error handling, monitoring y security
from core.error_handling import setup_error_handling
from core.monitoring import setup_monitoring
from core.security import setup_security
from database import get_supabase_client

# Inicializar la aplicación de FastAPI
app = FastAPI(
    title="Santa Helena del Valle IPS API",
    version="1.0.0",
    description="API para la gestión de pacientes, atenciones RIAS y compliance Resolución 3280 de 2018"
)

# Configuración de CORS
# Orígenes permitidos (en desarrollo, el frontend de React)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir las rutas de los diferentes módulos - VERSIÓN CONSOLIDADA
app.include_router(pacientes.router)
app.include_router(atenciones.router)
app.include_router(intervenciones_colectivas.router)
app.include_router(atencion_primera_infancia.router)  # VERSIÓN CONSOLIDADA - Arquitectura vertical
app.include_router(atencion_materno_perinatal.router)
app.include_router(tamizaje_oncologico.router)
app.include_router(control_cronicidad.router)
app.include_router(entornos_salud_publica.router)
app.include_router(familia_integral_salud_publica.router)
app.include_router(atencion_integral_transversal_salud.router)
app.include_router(catalogo_ocupaciones_simple.router)  # Catálogo ocupaciones DANE para PEDT
# app.include_router(medicos.router)
# app.include_router(codigos_rias.router)

# =============================================================================
# CONFIGURACIÓN DE ERROR HANDLING Y MONITORING
# =============================================================================

# Configurar error handling centralizado
setup_error_handling(app)

# Configurar performance monitoring y health checks
setup_monitoring(app)

# Configurar sistema de seguridad avanzada
setup_security(app, get_supabase_client())

# Root endpoint con información básica
@app.get("/")
async def root():
    """Endpoint raíz con información básica del API."""
    return {
        "name": "Santa Helena del Valle IPS API",
        "version": "1.0.0", 
        "description": "API para gestión RIAS según Resolución 3280 de 2018",
        "status": "operational",
        "endpoints": {
            "health_check": "/health/",
            "api_docs": "/docs",
            "primera_infancia": "/atenciones-primera-infancia/",
            "pacientes": "/pacientes/",
            "ocupaciones": "/ocupaciones/"
        }
    }
