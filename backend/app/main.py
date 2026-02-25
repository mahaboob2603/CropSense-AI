import os
import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import predict, history, heatmap, auth, chat, tts
from .db.session import engine
from .db import models

# Configure proper logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("cropsense")

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CropSense AI")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
# In FastAPI, you CANNOT use wildcard origins `["*"]` with allow_credentials=True.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:3002", "http://localhost:3002"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(predict.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(heatmap.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(tts.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "CropSense AI Backend is running"}
