from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.IncidenteResponse)
def create_incidente(incidente: schemas.IncidenteCreate, db: Session = Depends(get_db)):
    return crud.create_incidente(db=db, incidente=incidente)

@router.get("/", response_model=list[schemas.IncidenteResponse])
def read_incidentes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidentes = crud.get_incidentes(db, skip=skip, limit=limit)
    return incidentes
