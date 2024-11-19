from pydantic import BaseModel
from pydantic.dataclasses import ConfigDict
from typing import Optional
from sqlalchemy import Date

# Base model for common fields
class TestBase(BaseModel):
  username: str
  email: str
  password: str
  

# Base model for common fields
class UserBase(BaseModel):
    username: str
    email: str

class CreateUserRequest(BaseModel):
  username: str
  email: str
  password: str
  
class LoginUserRequest(BaseModel):
  username: str
  password: str
  
class UpdateUserRequest(BaseModel):
  username: str = None
  
class Token(BaseModel):
  access_token: str
  token_type: str

class GetAccountResponse(BaseModel):
  username: str
  email: str

# Example for a response message
class GreetResponse(BaseModel):
    message: str
    name: str

class UploadResumeRequest(BaseModel):
  title: str
  description: str

class EditResumeRequest(BaseModel):
  description: str
  pdf_url: str

  model_config = ConfigDict(from_attributes=True)

class DeleteResumeRequest(BaseModel):
  title: str

class ApplicationRequest(BaseModel):
    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like SQLAlchemy types

    id: str = None
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: str = None
    notes: str = None
    status_history: dict = None
    applied_date: Date
    last_update: Date
    interview_notes: str = None
    interview_dates: str = None
    interview_round: str = None
    is_active_interview: bool
    offer_notes: str = None
    offer_interest: int = None
    is_active_offer: bool
    previous_emails: dict = None
    days_to_update: int = None

class ApplicationUpdateRequest(BaseModel):
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: str
    notes: str
    status_history: dict = None
    applied_date: str = None
    last_update: str = None
    interview_notes: str = None
    interview_dates: str = None
    interview_round: str = None
    is_active_interview: bool = None
    offer_notes: str = None
    offer_interest: int = None
    is_active_offer: bool = None
    previous_emails: dict = None
    days_to_update: int = None

class UserSettingsRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    university: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    desired_role: Optional[str] = None
    theme: str
    notification_preferences: Optional[str] = None

class UpdateEmailRequest(BaseModel):
    email: str
    
    
class EmailRequest(BaseModel):
    app: str
    subject: str
    sender: str
    received_date: str
    body: str
    body_preview: str
    status: str