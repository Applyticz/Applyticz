from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.db.database import db_dependency
from app.models.database_models import Email, Application
from fastapi import Query
from app.models.pydantic_models import EmailRequest

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/create-email/", tags=['emails'], status_code=status.HTTP_201_CREATED)
async def create_email(email_request: EmailRequest, db: db_dependency, user: user_dependency):
    # Find the application associated with the same application id
    application = db.query(Application).filter(Application.id == email_request.app).first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching application found.")

    # Create a new Email object
    new_email = Email(
        app=application.id,  # Use the found application ID
        user_id=user['id'], 
        subject=email_request.subject,
        sender=email_request.sender,
        received_date=email_request.received_date,
        body=email_request.body,
        body_preview=email_request.body_preview,
        status=email_request.status
    )
    
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    
    return new_email 


@router.get("/emails/", tags=['emails'], status_code=status.HTTP_200_OK)
async def get_emails(db: db_dependency):
        
        emails = db.query(Email).all()
        
        return emails
    
@router.get("/emails/{email_id}", tags=['emails'], status_code=status.HTTP_200_OK)
async def get_email(email_id: int, db: db_dependency):
    
    email = db.query(Email).filter(Email.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    
    return email

@router.put("/emails/{email_id}", tags=['emails'], status_code=status.HTTP_200_OK)
async def update_email(email_id: int, email_request: EmailRequest, db: db_dependency):
        
        email = db.query(Email).filter(Email.id == email_id).first()
        
        if not email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        
        email.subject = email_request.subject
        email.sender = email_request.sender
        email.received_date = email_request.received_date
        email.body = email_request.body
        email.body_preview = email_request.body_preview
        email.status = email_request.status
        
        db.commit()
        db.refresh(email)
        
        return email
    
@router.delete("/emails/{email_id}", tags=['emails'], status_code=status.HTTP_200_OK)
async def delete_email(email_id: int, db: db_dependency):
        
        email = db.query(Email).filter(Email.id == email_id).first()
        
        if not email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        
        db.delete(email)
        db.commit()
        
        return "Email deleted successfully"