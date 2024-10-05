from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from app.utils.utils import get_current_user
from typing import Annotated
import datetime
from app.models.pydantic_models import UploadResumeRequest, DeleteResumeRequest, EditResumeRequest
from app.db.database import get_db, db_dependency
from app.models.database_models import Resume
from app.models.database_models import User
from fastapi import Query
from app.utils.utils import get_current_time
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io


router = APIRouter()


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/upload_resume', tags=['resume'], status_code=status.HTTP_201_CREATED)
async def upload_resume(
    user: user_dependency,  # Dependency
    db: db_dependency,  # Dependency
    title: str = Form(...),  # Capture `title` as a form field
    description: str = Form(...),  # Capture `description` as a form field
    pdf: UploadFile = File(...)  # Default argument
):
    
    pdf_data = await pdf.read()

    # Create the resume object with the provided data
    upload_resume_model = Resume(
        user_id=user['id'],
        title=title,
        description=description,
        date=get_current_time(),
        modified_date=get_current_time(),
        pdf_data = pdf_data
    )
    
    
    # Check if a resume with the same title already exists for the same user
    existing_resume = db.query(Resume).filter(Resume.title == title, Resume.user_id == user['id']).first()
    
    # If a resume with the same title already exists, return an error
    if existing_resume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume already exists")
    
    # Add the new resume to the database
    db.add(upload_resume_model)
    db.commit()
    db.refresh(upload_resume_model)
    
    return {"message": "Resume uploaded successfully", "resume_id": upload_resume_model.id}

@router.put('/update_resume', tags=['resume'], status_code=status.HTTP_200_OK)
async def update_resume(
    title: str,
    user: user_dependency,
    db: db_dependency,
    description: str = Form(None),  # Make this optional
    pdf: UploadFile = File(None)    # Make this optional
):
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id and title
    resume_to_update = db.query(Resume).filter(Resume.user_id == user_id_str, Resume.title == title).first()

    if not resume_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    # Update the description if it was provided
    if description is not None:
        resume_to_update.description = description
    
    # Update PDF data if a new file is provided
    if pdf is not None:
        pdf_data = await pdf.read()
        resume_to_update.pdf_data = pdf_data
    
    # Update the modified date to the current time
    resume_to_update.modified_date = get_current_time()
    
    # Commit changes to the database
    db.commit()
    
    return {"message": "Resume updated successfully"}



@router.get('/get_resumes', tags=['resume'], status_code=status.HTTP_200_OK)
async def get_resume(user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # print(f"User ID from token: {user_id_str}")
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        # print(f"User not found with ID: {user_id_str}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Resume associated with the user_id
    resumes = db.query(Resume).filter(Resume.user_id == user_id_str).order_by(Resume.date).all()
    if not resumes:
        return []
    
    # Convert the resumes to a list of dictionaries
    resume_list = []
    for resume in resumes:
        resume_dict = {
            'title': resume.title,
            'description': resume.description,
            'date': resume.date,
            'modified_date': resume.modified_date,
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
        'modified_date': resume.modified_date,
        'pdf_url': resume.pdf_url,
    }
    
    return resume_dict

@router.get('/get_resume_pdf', tags=['resume'], status_code=status.HTTP_200_OK)
async def get_resume_pdf(title: str, user: user_dependency, db: db_dependency):
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

    # Assuming resume.pdf_data is a binary data representation of the PDF
    if resume.pdf_data:
        return StreamingResponse(io.BytesIO(resume.pdf_data), media_type="application/pdf")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF data not found")

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
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No resumes to delete")
    
    for resume in resumes_to_delete:
        db.delete(resume)
    
    db.commit()
    
    return "All resumes deleted successfully"

