from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv


load_dotenv()


# SQLAlchemy Database URL
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
        
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
