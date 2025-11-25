# main app file (e.g., app/main.py or main.py)
from fastapi import FastAPI
from app.routes import farmers, analysis
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# NEW:
from app.routes import predict  # <— add this

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cotton Disease Detection API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farmers.router,  prefix="/farmers",  tags=["Farmers"])
app.include_router(analysis.router,  prefix="/analysis", tags=["Analysis"])
app.include_router(predict.router,   prefix="/predict",  tags=["Predict"])  
