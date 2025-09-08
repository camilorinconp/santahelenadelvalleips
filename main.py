import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener las credenciales de Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Inicializar el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicializar la aplicación de FastAPI
app = FastAPI()

# Endpoint de prueba para verificar la conexión a la base de datos
from routes import pacientes

app.include_router(pacientes.router, tags=["Pacientes"])