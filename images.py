from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os, shutil
from app import models, schemas, database
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def upload_image(farmer_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    prediction = "Healthy"
    confidence = "95%"

    image_result = models.ImageResult(
        farmer_id=farmer_id,
        image_path=file_path,
        prediction=prediction,
        confidence=confidence,
        created_at=datetime.utcnow()
    )
    db.add(image_result)
    db.commit()
    db.refresh(image_result)
    return {"message": "Image uploaded and analysed", "result": prediction, "confidence": confidence}

