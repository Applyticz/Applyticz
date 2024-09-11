from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from models.pydantic_models import TestBase
from models.database_models import Test
from database import db_dependency

router = APIRouter()

@router.get('/testing_route')
async def test():
  return {'message': 'Testing Route'}

@router.post('/test/', status_code=status.HTTP_201_CREATED)
async def test(test: TestBase, db: db_dependency):
  db_test = Test(**test.model_dump())
  db.add(db_test)
  db.commit()