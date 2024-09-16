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
from passlib.context import CryptContext
from jose import JWTError, jwt


router = APIRouter()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {'username': username, 'id': user_id }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/auth_route', tags=['auth'])
async def test():
  return {'message': 'Auth Route'}


@router.post("/register_account", status_code=status.HTTP_201_CREATED, tags=['auth'])
async def create_user( db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password=pwd_context.hash(create_user_request.password),
        email=create_user_request.email
    )
    
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
    
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub' : username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


    

@router.post('/login', status_code=status.HTTP_200_OK)
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


