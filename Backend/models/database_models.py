from sqlalchemy import Integer, String, Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid



class Test(Base):
  __tablename__ = 'tests'
  id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
  username = Column(String, nullable=False, unique=True)
  email = Column(String, nullable=False, unique=True)
  password = Column(String)

class User(Base):
    __tablename__ = "users"

    # Define columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    userscol = Column(String(45), nullable=False)


