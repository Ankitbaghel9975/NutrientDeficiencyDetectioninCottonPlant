from fastapi import APIRouter, UploadFile, File
import os, shutil
from app.ml_model import predict_disease

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
def analyze_leaf(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run image matching
    result = predict_disease(file_path)

    return {
        "uploaded_file": file.filename,
        "prediction": result["prediction"],
        "confidence": result["confidence"]
    }
