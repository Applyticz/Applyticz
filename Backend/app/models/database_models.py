from sqlalchemy import Integer, String, Column, Float, ForeignKey, CHAR, DateTime, LargeBinary, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import get_db, engine, Base, db_dependency
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import JSON

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
    
    outlook_auth = relationship("OutlookAuth", back_populates="user", uselist=False)
    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    emails = relationship("Email", back_populates="user")
    gmail_auth = relationship("GmailAuth", back_populates="user", uselist=False)

class OutlookAuth(Base):
    __tablename__ = "outlook_auth"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)  # Reference to User table

    access_token = Column(String(2048), nullable=False)
    refresh_token = Column(String(2048), nullable=False)
    token_expiry = Column(DateTime, nullable=False)  # Store token expiration date/time
    scope = Column(String(512), nullable=True)  # Store token scope for permissions

    # Define relationship with the User model
    user = relationship("User", back_populates="outlook_auth")

class GmailAuth(Base):
    __tablename__ = "gmail_auth"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)  # Reference to User table

    access_token = Column(String(2048), nullable=False)
    refresh_token = Column(String(2048), nullable=False)
    token_expiry = Column(DateTime, nullable=False)  # Store token expiration date/time

    # Define relationship with the User model
    user = relationship("User", back_populates="gmail_auth")

class Resume(Base):
    __tablename__ = "resumes"

    # Define columns
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(String(255), nullable=False)
    modified_date = Column(String(255), nullable=True)
    pdf_data = Column(LargeBinary, nullable=False)  # Store binary PDF data

    user = relationship("User", back_populates="resumes")

class Application(Base):
    __tablename__ = "applications"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    status_history = Column(JSON, nullable=False)
    applied_date = Column(Date, nullable=False)
    last_update = Column(Date, nullable=False)
    salary = Column(String(255), nullable=False)
    job_description = Column(String(1000), nullable=True)
    notes = Column(String(1000), nullable=True)
    interview_notes = Column(String(1000), nullable=True)
    interview_dates = Column(Date, nullable=True)
    interview_round = Column(String(255), nullable=True)
    is_active_interview = Column(Boolean, nullable=False)
    offer_notes = Column(String(1000), nullable=True)
    offer_interest = Column(Integer, nullable=True)
    is_active_offer = Column(Boolean, nullable=False)
    previous_emails = Column(JSON, nullable=True)
    days_to_update = Column(Integer, nullable=True)

    user = relationship("User", back_populates="applications")
    emails = relationship("Email", back_populates="application")
    
    
class Email(Base):
    __tablename__ = "emails"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    app = Column(CHAR(36), ForeignKey('applications.id'), nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id'), nullable=False)
    subject = Column(String(255), nullable=False)
    sender = Column(String(255), nullable=False)
    received_date = Column(String(255), nullable=False)
    body = Column(String(1000), nullable=False)
    body_preview = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)


    user = relationship("User", back_populates="emails")
    application = relationship("Application", back_populates="emails")  

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey('users.id', name='fk_user_settings_user_id'), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    university = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    desired_role = Column(String(100), nullable=True)
    theme = Column(String(50), nullable=False, default="light")
    notification_preferences = Column(String(255), nullable=True)

    user = relationship("User", back_populates="settings")
