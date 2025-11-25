from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database


router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Farmer)
def create_farmer(farmer: schemas.FarmerCreate, db: Session = Depends(get_db)):
    db_farmer = db.query(models.Farmer).filter(models.Farmer.email == farmer.email).first()
    if db_farmer:
        raise HTTPException(status_code=400, detail="Farmer already exists")
    new_farmer = models.Farmer(**farmer.dict())
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)
    return new_farmer

@router.get("/{email}", response_model=schemas.Farmer)
def get_farmer(email: str, db: Session = Depends(get_db)):
    farmer = db.query(models.Farmer).filter(models.Farmer.email == email).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

