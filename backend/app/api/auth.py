from fastapi import APIRouter, Depends, HTTPException, status, Request
import time
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..db.models import User
from ..schemas.all_schemas import UserCreate, UserOut, LoginRequest
from ..core.security import get_password_hash, verify_password, create_access_token
from ..core.dependencies import get_current_user
from datetime import timedelta
import logging

logger = logging.getLogger("cropsense.auth")
router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    email_lower = user.email.lower()
    db_user = db.query(User).filter(User.email == email_lower).first()
    if db_user:
        logger.warning(f"Registration failed: Email {email_lower} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
        
    if len(user.password) < 8:
        logger.warning(f"Registration failed: Password too short for {email_lower}")
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name, 
        email=email_lower, 
        password_hash=hashed_password,
        location=user.location
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Registration successful for user: {email_lower}")
    return new_user

login_attempts = {}

@router.post("/login")
def login(request: LoginRequest, req: Request, db: Session = Depends(get_db)):
    client_ip = req.client.host if req.client else "unknown"
    now = time.time()
    
    if client_ip in login_attempts:
        attempts = [t for t in login_attempts[client_ip] if now - t < 60]
        if len(attempts) >= 5:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")
        attempts.append(now)
        login_attempts[client_ip] = attempts
    else:
        login_attempts[client_ip] = [now]

    email_lower = request.email.lower()
    user = db.query(User).filter(User.email == email_lower).first()
    if not user:
        logger.warning(f"Login failed: Email {email_lower} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    if not verify_password(request.password, user.password_hash):
        logger.warning(f"Login failed: Invalid password for {email_lower}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"Login successful for user: {request.email}")
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "name": user.name}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
