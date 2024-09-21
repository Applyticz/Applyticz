from fastapi import APIRouter, HTTPException, status, Depends
from app.db.database import get_db, db_dependency
from app.models.pydantic_models import Token, CreateUserRequest, UpdateUserRequest, GetAccountResponse
from app.models.database_models import User
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
import uuid
from dotenv import load_dotenv
from app.utils.utils import get_current_user, authenticate_user, create_access_token, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}
   
# Verify Auth Token
@router.post("/verify_token", status_code=status.HTTP_200_OK, tags=['auth'])
async def verify_token(token: Annotated[str, Depends(oauth2_bearer)]):
    return verify_token_expiration(token)


@router.get('/auth_route', tags=['auth'])
async def test():
  return {'message': 'Auth Route'}

@router.post("/register_account", status_code=status.HTTP_201_CREATED, tags=['auth'])
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    # Create the new user object
    create_user_model = User(
        id=str(uuid.uuid4()),  # Explicitly generate a UUID for the user
        username=create_user_request.username,
        password=hash_password(create_user_request.password),
        email=create_user_request.email
    )
    
    # Check if the username or email already exists
    if db.query(User).filter(User.username == create_user_request.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if db.query(User).filter(User.email == create_user_request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    # Add the new user to the database
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully"}

@router.put("/update_account", status_code=status.HTTP_201_CREATED, tags=['auth'])
async def update_user(db: db_dependency, update_user_request: UpdateUserRequest, user: user_dependency):
    # Fetch the user by ID
    user_id_str = str(user['id'])

    user_to_update = db.query(User).filter(User.id == user_id_str).first()
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update the user fields
    user_to_update.username = update_user_request.username
    
    db.commit()
    db.refresh(user_to_update)
    return {"message": "User updated successfully"}

@router.delete("/delete_account", status_code=status.HTTP_200_OK, tags=['auth'])
async def delete_account(user: user_dependency, db: db_dependency):
    # Fetch the user by id
    user_id_str = str(user['id'])

    user_to_delete = db.query(User).filter(User.id == user_id_str).first()
    
    # If user not found, raise an error (although this is unlikely because they are authenticated)
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Delete the user from the database
    db.delete(user_to_delete)
    
    # Commit the changes
    db.commit()

    return {"message": "User account successfully deleted"}

@router.get("/get_account", response_model=GetAccountResponse, tags=['auth'], status_code=status.HTTP_200_OK)
async def get_account(user: user_dependency, db: db_dependency):
    # Fetch the user by ID
    user_id_str = str(user['id'])

    user_to_get = db.query(User).filter(User.id == user_id_str).first()
    if not user_to_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Return user information
    return GetAccountResponse(username=user_to_get.username, email=user_to_get.email)

    

@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK, tags=['auth'])
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # Authenticate the user with the provided username and password
    user = authenticate_user(form_data.username, form_data.password, db)
    
    # If user is not found or password is invalid, raise HTTP 401 error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create the access token with an expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(username=user.username, user_id=user.id, expires_delta=access_token_expires)
    
    # Return the access token and token type (bearer)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post('/logout', status_code=status.HTTP_200_OK, tags=['auth'])
async def logout_user(db: db_dependency, user: user_dependency):
    return {
        "access_token": "null",
        "token_type": "null"
    }

@router.get("/", status_code=status.HTTP_200_OK, tags=["auth"])
async def user(user: user_dependency, db: db_dependency):
    # Fetch user information for the home route (if needed)
    pass

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication fail")
    return {"User": user}