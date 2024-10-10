from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.db.database import get_db, db_dependency
from app.models.database_models import User, Resume, Application

router = APIRouter()


#@router.get('/get_data', tags=['dashboard'], status_code=status.HTTP_200_OK)