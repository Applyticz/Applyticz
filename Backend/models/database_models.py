from sqlalchemy import Integer, String, Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid



class User(Base):
  __tablename__ = 'users'
  id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
  username = Column(String, nullable=False, unique=True)
  email_address = Column(String, nullable=False, unique=True)
  password = Column(String)
