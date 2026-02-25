import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fetch database URL from env, fallback to SQLite for local ease-of-use Let's ensure dotenv is loaded
from dotenv import load_dotenv
load_dotenv()

# Use absolute path for sqlite DB to ensure consistent location regardless of cwd
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
db_path = os.path.join(BASE_DIR, "cropsense.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Only pass check_same_thread to SQLite, as it breaks Postgres
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
