# app/routes/predict.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ml_infer import predict_image_bytes, get_labels

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "classes": get_labels()}

@router.post("/", summary="Predict cotton disease with trained model")
async def predict_leaf(file: UploadFile = File(...)):
    # Basic file type guard (optional)
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use JPG/PNG/BMP/TIFF.")
    img_bytes = await file.read()
    try:
        result = predict_image_bytes(img_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unreadable image: {e}")
    return {"uploaded_file": file.filename, **result}
