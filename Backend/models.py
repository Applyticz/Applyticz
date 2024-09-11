from sqlalchemy import Column, Integer, String
from database import Base

# Define the User model matching the table structure
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userscol = Column(String(45), nullable=False)  # VARCHAR(45)
