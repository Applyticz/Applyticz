from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.database_models import Test
from models.pydantic_models import TestBase
from database import db_dependency

router = APIRouter()

@router.get('/testing_route', tags=['test'])
async def test():
  return {'message': 'Testing Route'}

@router.post('/create_test/', tags=['test'], status_code=status.HTTP_201_CREATED)
async def create_test(test:TestBase, db:db_dependency):
  db_test = Test(**test.model_dump())
  db.add(db_test)
  db.commit()

@router.get('/get_all_tests', tags=['test'], status_code=status.HTTP_200_OK)
async def get_all_tests(db:db_dependency):
  return db.query(Test).all()
