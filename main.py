from fastapi import FastAPI
from routes import pacientes, atenciones, intervenciones_colectivas, atencion_primera_infancia #, medicos, codigos_rias

# Inicializar la aplicación de FastAPI
app = FastAPI(
    title="Santa Helena del Valle IPS API",
    version="0.1.0",
    description="API para la gestión de pacientes, médicos y atenciones."
)

# Incluir las rutas de los diferentes módulos
app.include_router(pacientes.router)
app.include_router(atenciones.router)
app.include_router(intervenciones_colectivas.router)
app.include_router(atencion_primera_infancia.router)
# app.include_router(medicos.router)
# app.include_router(codigos_rias.router)
