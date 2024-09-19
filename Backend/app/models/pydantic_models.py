from pydantic import BaseModel
from pydantic.dataclasses import ConfigDict


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
  date: str
  pdf_url: str

  model_config = ConfigDict(from_attributes=True)

class DeleteResumeRequest(BaseModel):
  title: str

