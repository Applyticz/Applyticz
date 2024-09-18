from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.models.pydantic_models import UploadResumeRequest
from app.db.database import get_db, db_dependency
from app.models.database_models import Resume



router = APIRouter()


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('upload_resume', tags=['resume'], status_code=status.HTTP_201_CREATED)
async def upload_resume(resume: UploadResumeRequest, user: user_dependency, db: db_dependency):
    upload_resume_model = Resume(
        user_id=user['id'],
        title=resume.title,
        description=resume.description,
        date=resume.date,
        pdf_url=resume.pdf_url
    )
    existing_resume = db.query(Resume).filter(upload_resume_model.id == Resume.id).first()
    if existing_resume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume already exists")
    
    db.add(upload_resume_model)
    db.commit()
    db.refresh(upload_resume_model)
    return "Resume uploaded successfully"