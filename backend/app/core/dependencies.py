import logging
from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .security import SECRET_KEY, ALGORITHM
from ..db.session import get_db
from ..db.models import User

logger = logging.getLogger("cropsense.auth.deps")

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Token extraction failed: Missing or invalid Authorization header")
        raise credentials_exception
        
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Token decoding failed: Missing 'sub' (email) claim")
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        logger.warning("Token validation failed: Token has expired")
        raise credentials_exception
    except JWTError as e:
        logger.warning(f"Token decoding failed: {e}")
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"Token validation failed: User {email} not found in DB")
        raise credentials_exception
        
    return user
