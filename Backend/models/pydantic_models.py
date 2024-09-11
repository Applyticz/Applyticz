from pydantic import BaseModel


class TestBase(BaseModel):
  username: str
  email: str
  password: str
  