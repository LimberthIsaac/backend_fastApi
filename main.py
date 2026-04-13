from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

# Crear las tablas en la base de datos si no existen (basado en models.py)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API - Plataforma Inteligente de Emergencias Vehiculares",
    description="Backend para la gestión de incidentes vehiculares, talleres y técnicos",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde Flutter y Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "up",
        "message": "Bienvenido a la API de Plataforma Inteligente de Emergencias Vehiculares"
    }

from routers import clientes, talleres, incidentes

app.include_router(clientes.router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(talleres.router, prefix="/api/talleres", tags=["Talleres"])
app.include_router(incidentes.router, prefix="/api/incidentes", tags=["Incidentes"])
