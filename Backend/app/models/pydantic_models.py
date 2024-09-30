from pydantic import BaseModel
from pydantic.dataclasses import ConfigDict
from typing import Optional

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
    id: str = None
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: str = None
    notes: str = None

class ApplicationUpdateRequest(BaseModel):
    company: str
    position: str
    location: str
    status: str
    salary: str
    job_description: str
    notes: str

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

