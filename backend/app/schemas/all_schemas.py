from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class DetectionBase(BaseModel):
    disease_name: str
    confidence: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    spread_risk: str
    severity: Optional[str] = None

class DetectionCreate(DetectionBase):
    pass

class RemedyLanguage(BaseModel):
    disease_name: str
    crop: str
    cause: str
    symptoms: List[str]
    treatment_steps: List[str]
    organic_options: List[str]
    chemical_options: List[str]
    prevention: List[str]

class StructuredRemedy(BaseModel):
    EN: RemedyLanguage
    HI: RemedyLanguage
    TE: RemedyLanguage

class DetectionOut(DetectionBase):
    id: int
    user_id: int
    timestamp: datetime
    grad_cam_base64: Optional[str] = None
    treatment: Optional[str] = None # Legacy, kept for backwards compatibility
    remedies: Optional[StructuredRemedy] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    location: Optional[str] = None

class UserCreate(UserBase):
    from pydantic import constr
    password: str # We can validate min length next, but Pydantic v2 has Field(min_length=8)
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    detections: List[DetectionOut] = []

    class Config:
        from_attributes = True
