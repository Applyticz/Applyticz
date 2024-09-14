from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.database_models import Test, User
from models.pydantic_models import TestBase, UserBase
from database import db_dependency
from utils import generate_password_hash as hash_password

router = APIRouter()

@router.get('/auth_route', tags=['auth'])
async def test():
  return {'message': 'Auth Route'}

@router.post('/register', tags=['auth'])
async def register_user(user:UserBase, db: Session = Depends(get_db)):
  if db.query(User).filter(User.username == 'test').first():
    return HTTPException(status_code=400, detail='User already exists')
  new_user = User(**user.model_dump())
  new_user.password = hash_password(new_user.password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
  