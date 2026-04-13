from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, schemas_auth
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TallerResponse)
def create_taller(taller: schemas.TallerCreate, db: Session = Depends(get_db)):
    # Check si el taller (correo) ya existe
    # TODO: Añadir validación completa por correo/nit.
    return crud.create_taller(db=db, taller=taller)

@router.get("/", response_model=list[schemas.TallerResponse])
def read_talleres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    talleres = crud.get_talleres(db, skip=skip, limit=limit)
    return talleres

def get_taller_by_email(db: Session, email: str):
    import models
    return db.query(models.Taller).filter(models.Taller.correo == email).first()

@router.post("/login", response_model=schemas_auth.TokenResponse)
def login(request: schemas_auth.LoginRequest, db: Session = Depends(get_db)):
    db_taller = get_taller_by_email(db, email=request.correo)
    if not db_taller or not crud.verify_password(request.password, db_taller.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    return {
        "access_token": "fake-jwt-token-taller",
        "token_type": "bearer",
        "user_id": db_taller.id_taller,
        "user_name": db_taller.razon_social
    }
