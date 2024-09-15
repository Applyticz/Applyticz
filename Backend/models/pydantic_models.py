from pydantic import BaseModel


class TestBase(BaseModel):
  username: str
  email: str
  password: str
  

# Base model for common fields
class UserBase(BaseModel):
    username: str
    email: str
    disabled: bool = False

# Model for creating a new user (inherits from UserBase)
class UserCreate(UserBase):
    password: str

# Model for user login
class UserLogin(BaseModel):
    email: str
    password: str

# Model for a user in the database (includes hashed password)
class UserInDB(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    pass

# Token model for handling JWT tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data model for extracting information from the token
class TokenData(BaseModel):
    username: str | None = None

# Example for a response message
class GreetResponse(BaseModel):
    message: str
    name: str
