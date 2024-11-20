from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.models.pydantic_models import UserSettingsRequest
from app.db.database import get_db, db_dependency
from app.models.database_models import UserSettings, User
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/get_settings', tags=['settings'], status_code=status.HTTP_200_OK)
async def get_settings(user: user_dependency, db: db_dependency):
    user_id_str = str(user['id'])
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == user_id_str).first()
    if not user_settings:
        # If settings don't exist, create default settings
        user_settings = UserSettings(user_id=user_id_str)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)
    
    return {
        "first_name": user_settings.first_name,
        "last_name": user_settings.last_name,
        "university": user_settings.university,
        "email": user_settings.email,
        "age": user_settings.age,
        "gender": user_settings.gender,
        "desired_role": user_settings.desired_role,
        "theme": user_settings.theme,
        "notification_preferences": user_settings.notification_preferences,
        "last_refresh_time": user_settings.last_refresh_time if user_settings.last_refresh_time else None
    }

@router.put('/update_settings', tags=['settings'], status_code=status.HTTP_200_OK)
async def update_settings(settings: UserSettingsRequest, user: user_dependency, db: db_dependency):
    user_id_str = str(user['id'])
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == user_id_str).first()
    if not user_settings:
        # If settings don't exist, create new settings
        user_settings = UserSettings(user_id=user_id_str)
        db.add(user_settings)
    
    # Update settings
    for field, value in settings.dict().items():
        setattr(user_settings, field, value)
    
    db.commit()
    db.refresh(user_settings)
    
    return {
        "message": "Settings updated successfully",
        "settings": {
            "first_name": user_settings.first_name,
            "last_name": user_settings.last_name,
            "university": user_settings.university,
            "email": user_settings.email,
            "age": user_settings.age,
            "gender": user_settings.gender,
            "desired_role": user_settings.desired_role,
            "theme": user_settings.theme,
            "notification_preferences": user_settings.notification_preferences,
            "last_refresh_time": user_settings.last_refresh_time
        }
    }
