from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.database_models import Test
from models.pydantic_models import TestBase
from database import db_dependency

router = APIRouter()

@router.get('/auth_route', tags=['auth'])
async def test():
  return {'message': 'Auth Route'}