from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.db.database import get_db, db_dependency
from app.models.database_models import User, Resume, Application

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/get_data', tags=['dashboard'], status_code=status.HTTP_200_OK)
async def get_dashboard_data(user: user_dependency, db: db_dependency):
    user_id_str = str(user['id'])
    
    # Get total number of resumes and applications
    total_resumes = db.query(Resume).filter(Resume.user_id == user_id_str).count()
    total_applications = db.query(Application).filter(Application.user_id == user_id_str).count()
    
    # Get recent resumes and applications (e.g., last 5)
    recent_resumes = db.query(Resume).filter(Resume.user_id == user_id_str).order_by(Resume.date.desc()).limit(5).all()
    recent_applications = db.query(Application).filter(Application.user_id == user_id_str).order_by(Application.applied_date.desc()).limit(5).all()
    
    return {
        "totalResumes": total_resumes,
        "totalApplications": total_applications,
        "recentResumes": [{"title": r.title, "date": r.date} for r in recent_resumes],
        "recentApplications": [{"company": a.company, "position": a.position, "status": a.status} for a in recent_applications]
    }