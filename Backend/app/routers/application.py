from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.models.pydantic_models import ApplicationRequest, ApplicationUpdateRequest
from app.db.database import get_db, db_dependency
from app.models.database_models import Application, User
from fastapi import Query
from app.utils.utils import get_current_time

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/create_application', tags=['application'], status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationRequest, user: user_dependency, db: db_dependency):
    # Create the application object with the provided data
    create_application_model = Application(
        user_id=user['id'],
        company=application.company,
        position=application.position,
        location=application.location,
        status=application.status,
        applied_date=get_current_time(),
        last_update="",
        salary=application.salary,
        job_description=application.job_description,
        notes=application.notes
    )
    
    # Add the new application to the database
    db.add(create_application_model)
    db.commit()
    db.refresh(create_application_model)
    
    return {"message": "Application created successfully", "application_id": create_application_model.id}

@router.get('/get_applications', tags=['application'], status_code=status.HTTP_200_OK)
async def get_applications(user: user_dependency, db: db_dependency):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Applications associated with the user_id
    applications = db.query(Application).filter(Application.user_id == user_id_str).all()
    
    # Don't return the same application with different statuses
    # Sort the applications by last_update and company name
    applications = sorted(applications, key=lambda x: (x.last_update, x.company))
    
    if not applications:
        return []  # Return an empty list if no applications found
    
    # Convert the applications to a list of dictionaries
    application_list = []
    for app in applications:
        app_dict = {
            'id': app.id,
            'company': app.company,
            'location': app.location,
            'position': app.position,
            'status': app.status,
            'applied_date': app.applied_date,
            'last_update': app.last_update,
            'salary': app.salary,
            'job_description': app.job_description,
            'notes': app.notes
        }
        application_list.append(app_dict)
    
    return application_list

@router.put('/update_application', tags=['application'], status_code=status.HTTP_200_OK)
async def update_application(application: ApplicationUpdateRequest, user: user_dependency, db: db_dependency, id: str):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Application associated with the user_id and application id
    application_to_update = db.query(Application).filter(Application.user_id == user_id_str, Application.id == id).first()

    if not application_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    
    application_to_update.company = application.company
    application_to_update.position = application.position
    application_to_update.location = application.location
    application_to_update.status = application.status
    application_to_update.last_update = get_current_time()
    application_to_update.salary = application.salary
    application_to_update.job_description = application.job_description
    application_to_update.notes = application.notes
    
    db.commit()
    
    return "Application updated successfully"

@router.delete('/delete_application', tags=['application'], status_code=status.HTTP_200_OK)
async def delete_application(user: user_dependency, db: db_dependency, id: str = Query(..., description="ID of the application to delete")):
    # Ensure user['id'] is a string
    user_id_str = str(user['id'])
    
    # Query the User from the DB
    user_in_db = db.query(User).filter(User.id == user_id_str).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Query the Application associated with the user_id and application id
    application_to_delete = db.query(Application).filter(Application.user_id == user_id_str, Application.id == id).first()
    if not application_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    
    db.delete(application_to_delete)
    db.commit()
    
    return {"message": "Application deleted successfully"}