from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime, time

# --- Cliente Schemas ---
class ClienteBase(BaseModel):
    nombres: str
    apellidos: str
    ci_dni: str
    telefono: str
    correo: EmailStr
    foto_perfil_url: Optional[str] = None

class ClienteCreate(ClienteBase):
    password: str

class ClienteResponse(ClienteBase):
    id_cliente: int
    estado_cuenta: str
    calificacion_promedio: float

    model_config = ConfigDict(from_attributes=True)

# --- Taller Schemas ---
class TallerBase(BaseModel):
    razon_social: str
    nombre_representante: str
    nit: str = Field(..., pattern=r"^[0-9]+$")
    correo: EmailStr
    ubicacion_base_latitud: float
    ubicacion_base_longitud: float
    direccion_fisica: Optional[str] = None
    telefono_taller: Optional[str] = None
    logo_url: Optional[str] = None
    es_24_7: bool = False
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    cuenta_bancaria: Optional[str] = None

class TallerCreate(TallerBase):
    password: str

class TallerResponse(TallerBase):
    id_taller: int
    id_admin_aprobador: Optional[int] = None
    estado_aprobacion: str
    calificacion_promedio: float

    model_config = ConfigDict(from_attributes=True)

# --- Especialidad Schemas ---
class EspecialidadBase(BaseModel):
    nombre_especialidad: str
    descripcion: Optional[str] = None

class EspecialidadResponse(EspecialidadBase):
    id_especialidad: int
    model_config = ConfigDict(from_attributes=True)

# --- Tecnico Schemas ---
class TecnicoBase(BaseModel):
    nombres: str
    apellidos: str
    ci_tecnico: str
    telefono_contacto: str
    foto_perfil_url: Optional[str] = None

class TecnicoCreate(TecnicoBase):
    id_taller: int

class TecnicoResponse(TecnicoBase):
    id_tecnico: int
    id_taller: int
    en_turno: bool
    estado_operativo: str
    especialidades: List[EspecialidadResponse] = []

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
