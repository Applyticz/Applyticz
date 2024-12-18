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
import pytz
from app.db.database import db_dependency

# Load JWT secret key from environment variables
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], 
                           db: db_dependency):
    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id_str: str = payload.get('id')    # Retrieve user_id as a string
        
        email = db.query(User).filter(User.username == username).first().email
        if not username or not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        # Convert the string back to a UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format")

        # Return the user information if valid
        return {'username': username, 'id': user_id, 'email': email}

    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


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
    
    # Calculate the expiration time
    expires = datetime.now(timezone.utc) + expires_delta
    # Format the expiration time as DD-MM-YYYY HH:MM:SS AM/PM
    formatted_expires = expires.strftime("%d-%m-%Y %I:%M:%S %p")
    
    # Include both the expiration datetime object (for JWT) and the formatted string (for display)
    encode.update({'expires': formatted_expires})
    
    # print(encode)  # Optional: For debugging, prints the payload before encoding
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def update_access_token(token: str):
    
    token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = token_payload.get('sub')
    user_id = token_payload.get('id')
    expires = token_payload.get('expires')
    
    # Check if current token is expired
    if datetime.strptime(expires, "%d-%m-%Y %I:%M:%S %p").replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired TESTING")
    
    encode = {
        'sub': username,
        'id': str(user_id),  # Convert UUID to string for encoding in JWT
        'expires': expires
    }

    # Calculate the expiration time
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Format the expiration time as DD-MM-YYYY HH:MM:SS AM/PM
    formatted_expires = expires.strftime("%d-%m-%Y %I:%M:%S %p")

    encode.update({'expires': formatted_expires})

    # print("Expiration updated to:", formatted_expires)

    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


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


def get_current_time():
    # Get current time in UTC
    utc_now = datetime.now(pytz.UTC)

    # Convert to EST
    est_now = utc_now.astimezone(pytz.timezone('America/New_York'))

    # Format as mm-dd-yyyy hh-mm AM/PM
    formatted_time = est_now.strftime('%m-%d-%Y %I:%M %p')

    return formatted_time


def verify_token_expiration(token: str):
    """Verifies if the token is expired or still active."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        exp = payload.get('expires')
        # print(exp)
        if exp is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token has no expiration")

        # Parse the expiration string back to a datetime object
        expiration = datetime.strptime(exp, "%d-%m-%Y %I:%M:%S %p").replace(tzinfo=timezone.utc)

        # Use timezone-aware current time
        if expiration < datetime.now(timezone.utc):
            return {"status": "expired"}
        return {"status": "active"}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")


def verify_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token payload")
        verify_token_expiration(token)
        if verify_token_expiration(token)['status'] == "expired":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token has expired")
        return payload
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid or expired token")


def parse_email_for_company_name(email: str):
    """Parses the email address to extract the company name."""
    # Split the email address by the '@' symbol
    email_parts = email.split('@')
    # Split the domain name by the '.' symbol
    domain_parts = email_parts[1].split('.')
    # Return the first part of the domain name
    return domain_parts[0]
