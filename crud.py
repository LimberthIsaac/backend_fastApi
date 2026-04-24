from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import time
import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# --- CRUD Cliente ---
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()

def get_cliente_by_email(db: Session, email: str):
    return db.query(models.Cliente).filter(models.Cliente.correo == email).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    hashed_password = get_password_hash(cliente.password)
    db_cliente = models.Cliente(
        nombres=cliente.nombres,
        apellidos=cliente.apellidos,
        ci_dni=cliente.ci_dni,
        telefono=cliente.telefono,
        correo=cliente.correo,
        password_hash=hashed_password,
        foto_perfil_url=cliente.foto_perfil_url
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# --- CRUD Taller ---
def get_talleres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Taller).offset(skip).limit(limit).all()

def create_taller(db: Session, taller: schemas.TallerCreate):
    hashed_password = get_password_hash(taller.password)
    
    db_taller = models.Taller(
        razon_social=taller.razon_social,
        nombre_representante=taller.nombre_representante,
        nit=taller.nit,
        correo=taller.correo,
        ubicacion_base_latitud=taller.ubicacion_base_latitud,
        ubicacion_base_longitud=taller.ubicacion_base_longitud,
        direccion_fisica=taller.direccion_fisica,
        telefono_taller=taller.telefono_taller,
        logo_url=taller.logo_url,
        es_24_7=taller.es_24_7,
        horario_apertura=taller.horario_apertura,
        horario_cierre=taller.horario_cierre,
        cuenta_bancaria=taller.cuenta_bancaria,
        password_hash=hashed_password
    )
    db.add(db_taller)
    db.commit()
    db.refresh(db_taller)
    return db_taller

# --- CRUD Incidente ---
def create_incidente(db: Session, incidente: schemas.IncidenteCreate):
    db_incidente = models.Incidente(**incidente.model_dump())
    db.add(db_incidente)
    db.commit()
    db.refresh(db_incidente)
    return db_incidente

def get_incidentes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Incidente).offset(skip).limit(limit).all()
