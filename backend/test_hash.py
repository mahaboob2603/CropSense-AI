from app.db.session import engine
from app.db.models import User
from sqlalchemy.orm import sessionmaker
from app.core.security import verify_password

Session = sessionmaker(bind=engine)
db = Session()
users = db.query(User).all()
for u in users:
    print(f"User: {u.email}")
    print(f"Hash: {u.password_hash}")
    # We don't know the exact password for older users, but let's see if passlib throws an error
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # Just check if it considers it a valid bcrypt hash format
        print(f"Identity check: {pwd_context.identify(u.password_hash)}")
    except Exception as e:
        print("Error checking hash:", e)
    print("---")
