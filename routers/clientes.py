from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, schemas_auth
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ClienteResponse)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.correo)
    if db_cliente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    return crud.create_cliente(db=db, cliente=cliente)

@router.get("/", response_model=list[schemas.ClienteResponse])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.post("/login", response_model=schemas_auth.TokenResponse)
def login(request: schemas_auth.LoginRequest, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=request.correo)
    if not db_cliente or not crud.verify_password(request.password, db_cliente.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    return {
        "access_token": "fake-jwt-token-for-now", # En el futuro usar JWT real
        "token_type": "bearer",
        "user_id": db_cliente.id_cliente,
        "user_name": f"{db_cliente.nombres} {db_cliente.apellidos}"
    }
