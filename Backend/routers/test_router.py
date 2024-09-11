from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get('/testing_route')
async def test():
  return {'message': 'Testing Route'}