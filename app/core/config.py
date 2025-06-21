import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ECHO_LOGGING = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=ECHO_LOGGING,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """
    Dependency that yields a SQLAlchemy session and ensures it's closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
