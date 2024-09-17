from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db, db_dependency
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.pydantic_models import Token, CreateUserRequest, UpdateUserRequest
from models.database_models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta, datetime, timezone
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from jwt import PyJWTError
from utils import get_current_user, authenticate_user, create_access_token, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/auth_route', tags=['auth'])
async def test():
  return {'message': 'Auth Route'}

@router.post("/register_account", status_code=status.HTTP_201_CREATED, tags=['auth'])
async def create_user( db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password=hash_password(create_user_request.password),
        email=create_user_request.email
    )
    existig_user = db.query(User).filter(User.username == create_user_request.username).first()
    if existig_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if existing_email := db.query(User).filter(User.email == create_user_request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return "user created successfully"

@router.put("/update_account", status_code=status.HTTP_201_CREATED, tags=['auth'])
async def update_user( db: db_dependency, update_user_request: UpdateUserRequest, user: user_dependency):
    user_to_update = db.query(User).filter(User.id == user['id']).first()
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_to_update.username = update_user_request.username 
    
    db.commit()
    db.refresh(user_to_update)
    return "user updated successfully"

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}
    
@router.delete("/delete_account", status_code=status.HTTP_200_OK, tags=['auth'])
async def delete_account(user: user_dependency, db: db_dependency):
    # Fetch the user by id
    user_to_delete = db.query(User).filter(User.id == user['id']).first()
    
    # If user not found, raise an error (although this is unlikely because they are authenticated)
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Delete the user from the database
    db.delete(user_to_delete)
    
    # Commit the changes
    db.commit()

    return {"message": "User account successfully deleted"}

@router.get("/get_account", tags=['auth'], status_code=status.HTTP_200_OK)
async def get_account(user: user_dependency, db: db_dependency):
    user_to_get = db.query(User).filter(User.id == user['id']).first()
    if not user_to_get:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {"username": user_to_get.username, "email": user_to_get.email}

@router.post('/login', status_code=status.HTTP_200_OK, tags=['auth'])
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
    access_token = create_access_token(
        username=user.username, user_id=user.id, expires_delta=access_token_expires
    )
    
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
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication fail")
    return {"User": user}