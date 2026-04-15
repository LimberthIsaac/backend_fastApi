from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime, time

# --- Cliente Schemas ---
class ClienteBase(BaseModel):
    nombres: str
    apellidos: str
    telefono: str
    correo: EmailStr

class ClienteCreate(ClienteBase):
    password: str

class ClienteResponse(ClienteBase):
    id_cliente: int
    estado_cuenta: str
    calificacion_promedio: float
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Taller Schemas ---
class TallerBase(BaseModel):
    razon_social: str
    nit: str = Field(..., pattern=r"^[0-9]+$")
    correo: EmailStr
    ubicacion_base_latitud: float
    ubicacion_base_longitud: float
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    cuenta_bancaria: Optional[str] = None

class TallerCreate(TallerBase):
    password: str

class TallerResponse(TallerBase):
    id_taller: int
    estado_aprobacion: str
    calificacion_promedio: float

    model_config = ConfigDict(from_attributes=True)

# --- Incidente Schemas ---
class IncidenteBase(BaseModel):
    ubicacion_latitud: float
    ubicacion_longitud: float
    tipo_problema: str
    descripcion_manual: Optional[str] = None
    nivel_prioridad: Optional[str] = None

class IncidenteCreate(IncidenteBase):
    id_cliente: int
    id_vehiculo: int

class IncidenteResponse(IncidenteBase):
    id_incidente: int
    id_cliente: int
    id_vehiculo: int
    estado_solicitud: str
    fecha_hora_reporte: datetime
    distancia_km_calculada: Optional[float]

    model_config = ConfigDict(from_attributes=True)

# schemas/responses intermedios
class VehiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    año: int
    color: str
    tipo_transmision: str
    tipo_combustible: str

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoResponse(VehiculoBase):
    id_vehiculo: int
    id_cliente: int

    model_config = ConfigDict(from_attributes=True)
