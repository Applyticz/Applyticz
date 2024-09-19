from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.models.pydantic_models import UploadResumeRequest, DeleteResumeRequest
from app.db.database import get_db, db_dependency
from app.models.database_models import Resume
from app.models.database_models import User
from fastapi import Query



router = APIRouter()


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/upload_resume', tags=['resume'], status_code=status.HTTP_201_CREATED)
async def upload_resume(resume: UploadResumeRequest, user: user_dependency, db: db_dependency):
    upload_resume_model = Resume(
        user_id=user['id'],
        title=resume.title,
        description=resume.description,
        date=resume.date,
        pdf_url=resume.pdf_url
    )
    existing_resume = db.query(Resume).filter(upload_resume_model.title == Resume.title).first()
    if existing_resume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume already exists")
    
    db.add(upload_resume_model)
    db.commit()
    db.refresh(upload_resume_model)
    return "Resume uploaded successfully"


@router.get('/get_resumes', tags=['resume'], status_code=status.HTTP_200_OK)
async def get_resume(user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    print(f"User ID from token: {user_id_str}")
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        print(f"User not found with ID: {user_id_str}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id
    resumes = db.query(Resume).filter(Resume.user_id == user_id_str).all()
    if not resumes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resumes not found")
    
    # Convert the resumes to a list of dictionaries
    resume_list = []
    for resume in resumes:
        resume_dict = {
            'title': resume.title,
            'description': resume.description,
            'date': resume.date,
            'pdf_url': resume.pdf_url
        }
        resume_list.append(resume_dict)
    
    return resume_list

@router.get('/get_resume_by_title', tags=['resume'], status_code=status.HTTP_200_OK)
async def get_resume_by_title(title: str, user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id and title
    resume = db.query(Resume).filter(Resume.user_id == user_id_str, Resume.title == title).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    resume_dict = {
        'title': resume.title,
        'description': resume.description,
        'date': resume.date,
        'pdf_url': resume.pdf_url
    }
    
    return resume_dict

@router.delete('/delete_resume', tags=['resume'], status_code=status.HTTP_200_OK)
async def delete_resume(user: user_dependency, db: db_dependency, title: str = Query(..., description="Title of the resume to delete")):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id
    resume_to_delete = db.query(Resume).filter(Resume.user_id == user_id_str, Resume.title == title).first()
    if not resume_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    db.delete(resume_to_delete)
    db.commit()
    
    return {"message": "Resume deleted successfully"}

@router.delete('/delete_all_resumes', tags=['resume'], status_code=status.HTTP_200_OK)
async def delete_all_resumes(user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resumes associated with the user_id
    resumes_to_delete = db.query(Resume).filter(Resume.user_id == user_id_str).all()
    if not resumes_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resumes not found")
    
    for resume in resumes_to_delete:
        db.delete(resume)
    
    db.commit()
    
    return "All resumes deleted successfully"

@router.put('/update_resume', tags=['resume'], status_code=status.HTTP_201_CREATED)
async def update_resume(resume: UploadResumeRequest, user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id and title
    resume_to_update = db.query(Resume).filter(Resume.user_id == user_id_str, Resume.title == resume.title).first()

    if not resume_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    resume_to_update.description = resume.description
    resume_to_update.date = resume.date
    resume_to_update.pdf_url = resume.pdf_url
    
    db.commit()
    
    return "Resume updated successfully"