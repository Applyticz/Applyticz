from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Annotated
from fastapi import Depends
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQLAlchemy Database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the declarative models
Base = declarative_base()

# Dependency to get a session for each request
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables (if needed) when this script is run directly
db_dependency = Annotated[Session, Depends(get_db)]

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)