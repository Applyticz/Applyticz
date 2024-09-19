from sqlalchemy import Integer, String, Column, Float, ForeignKey, CHAR, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import get_db, engine, Base, db_dependency
from sqlalchemy.orm import relationship
import uuid

# Test Model
class Test(Base):
    __tablename__ = 'tests'

    # Store UUID as CHAR(36) for MySQL
    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    
    # Define String fields with lengths
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)


class User(Base):
    __tablename__ = "users"

    # Define columns
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    
    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")
    settings = relationship("UserSettings", back_populates="user", uselist=False)

class Resume(Base):
    __tablename__ = "resumes"

    # Define columns
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(String(255), nullable=False)
    pdf_url = Column(String(255), nullable=False)  # Store URL or file path to the PDF

    user = relationship("User", back_populates="resumes")

class Application(Base):
    __tablename__ = "applications"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    applied_date = Column(String(255), nullable=False)
    notes = Column(String(1000), nullable=True)

    user = relationship("User", back_populates="applications")

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, unique=True)
    theme = Column(String(50), nullable=False, default="light")
    notification_preferences = Column(String(255), nullable=True)

    user = relationship("User", back_populates="settings")
