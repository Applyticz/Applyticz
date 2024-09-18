from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jwt import PyJWTError
import jwt
import os
import bcrypt
from datetime import timedelta, datetime, timezone
from app.models.database_models import User
import uuid

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id_str: str = payload.get('id')  # Retrieve user_id as string

        if username is None or user_id_str is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        # Convert the string back to a UUID
        try:
            user_id = uuid.UUID(user_id_str)  # Convert the user_id back to UUID
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")

        return {'username': username, 'id': user_id }
    
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
 
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

import uuid

def create_access_token(username: str, user_id: uuid.UUID, expires_delta: timedelta):
    # Ensure user_id (UUID) is converted to a string before encoding
    encode = {
        'sub': username, 
        'id': str(user_id)  # Convert UUID to string
    }
    
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

