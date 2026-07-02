# SQLAlchemy engine banane ke liye
from sqlalchemy import create_engine

# Session aur Base banane ke liye
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL Connection URL
DATABASE_URL = "postgresql://postgres:128122@localhost:5432/bharatai_db"

# Engine
engine = create_engine(DATABASE_URL)

# Database Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Model
Base = declarative_base()
# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()