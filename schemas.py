from pydantic import BaseModel
from typing import List
from datetime import datetime

class FarmerBase(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    soil: str

class FarmerCreate(FarmerBase):
    pass

class Farmer(FarmerBase):
    id: int
    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    prediction: str
    confidence: str

class ImageResultCreate(BaseModel):
    farmer_id: int
    prediction: str
    confidence: str

class ImageResult(ImageBase):
    id: int
    farmer_id: int
    image_path: str
    created_at: datetime
    class Config:
        orm_mode = True

