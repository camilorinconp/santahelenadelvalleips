from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pacientes, atenciones, intervenciones_colectivas, atencion_primera_infancia, atencion_materno_perinatal, tamizaje_oncologico, control_cronicidad #, medicos, codigos_rias

# Inicializar la aplicación de FastAPI
app = FastAPI(
    title="Santa Helena del Valle IPS API",
    version="0.1.0",
    description="API para la gestión de pacientes, médicos y atenciones."
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


# Incluir las rutas de los diferentes módulos
app.include_router(pacientes.router)
app.include_router(atenciones.router)
app.include_router(intervenciones_colectivas.router)
app.include_router(atencion_primera_infancia.router)
app.include_router(atencion_materno_perinatal.router)
app.include_router(tamizaje_oncologico.router)
app.include_router(control_cronicidad.router)
# app.include_router(medicos.router)
# app.include_router(codigos_rias.router)
