from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    location = Column(String, nullable=True) # General location/region

    detections = relationship("Detection", back_populates="user")

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    disease_name = Column(String, index=True)
    confidence = Column(Float)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)
    spread_risk = Column(String) # HIGH, MEDIUM, LOW
    severity = Column(String, nullable=True) # Mild, Moderate, Severe, Unknown

    user = relationship("User", back_populates="detections")
