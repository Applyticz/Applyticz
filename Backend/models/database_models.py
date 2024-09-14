from sqlalchemy import Integer, String, Column, Float, ForeignKey, CHAR
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid



class Test(Base):
    __tablename__ = 'tests'

    # Store UUID as CHAR(36) for MySQL
    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Define String fields with lengths
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"

    # Define columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

