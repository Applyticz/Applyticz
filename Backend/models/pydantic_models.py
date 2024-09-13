from pydantic import BaseModel


class TestBase(BaseModel):
  username: str
  email: str
  password: str
  
class GreetResponse(BaseModel):
    message: str
    name: str