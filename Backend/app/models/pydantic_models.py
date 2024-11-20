from pydantic import BaseModel
from pydantic.dataclasses import ConfigDict
from typing import List, Optional
from datetime import date

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

    id: Optional[str] = None
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: Optional[str] = None
    notes: Optional[str] = None
    status_history: List[str] = []  # Updated to a list of strings
    applied_date: date
    last_update: date
    interview_notes: Optional[str] = None
    interview_dates: Optional[date] = None
    interview_round: Optional[str] = None
    is_active_interview: bool
    offer_notes: Optional[str] = None
    offer_interest: Optional[int] = None
    is_active_offer: bool
    previous_emails: List[str] = []  # Updated to a list of strings
    days_to_update: Optional[int] = None

class ApplicationUpdateRequest(BaseModel):
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: Optional[str] = None
    notes: Optional[str] = None
    status_history: List[str] = []  # Updated to a list of strings
    applied_date: Optional[str] = None
    last_update: Optional[str] = None
    interview_notes: Optional[str] = None
    interview_dates: Optional[date] = None
    interview_round: Optional[str] = None
    is_active_interview: Optional[bool] = None
    offer_notes: Optional[str] = None
    offer_interest: Optional[int] = None
    is_active_offer: Optional[bool] = None
    previous_emails: List[str] = []  # Updated to a list of strings
    days_to_update: Optional[int] = None


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
    applied_date: str
    body: str
    body_preview: str
    status: str