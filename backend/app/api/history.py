from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..db.models import Detection, User
from ..schemas.all_schemas import DetectionOut
from ..core.dependencies import get_current_user

router = APIRouter()

@router.get("/user-history", response_model=List[DetectionOut])
async def get_history(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    detections = db.query(Detection).filter(Detection.user_id == current_user.id).order_by(Detection.timestamp.desc()).offset(skip).limit(limit).all()
    return detections
