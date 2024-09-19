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

# Load JWT secret key from environment variables
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id_str: str = payload.get('id')  # Retrieve user_id as a string

        if not username or not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        # Convert the string back to a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")

        # Return the user information if valid
        return {'username': username, 'id': user_id}

    except PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def hash_password(password: str) -> str:
    """Hashes the password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that the provided plain password matches the stored hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username: str, password: str, db):
    """Authenticates a user by verifying their password and checking their existence in the database."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: uuid.UUID, expires_delta: timedelta):
    """Creates a JWT token with an expiration time."""
    encode = {
        'sub': username, 
        'id': str(user_id)  # Convert UUID to string for encoding in JWT
    }
    
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def create_user_and_login(db, testClient):
# Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test_email@test.com',
    })

    assert register_response.status_code == 201

    # Log in to get an access token

    login_response = testClient.post('/auth/login', data={
        'username': 'test_user',
        'password': 'test_password',
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    assert login_response.status_code == 200

    access_token = login_response.json()['access_token']

    # Include the access token in the headers

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    return headers