from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid 
import logging
import os
from dotenv import load_dotenv

password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) ->str:
    hash = password_context.hash(password)
    return hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):

    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + expiry if expiry is not None else deltatime(seconds=ACCESS_TOKEN_EXPIRY)
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh


    token = jwt.encode(
        payload=payload,
        key=os.getenv("JWT_SECRET"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    return token

def decode_access_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token,
            key=os.getenv("JWT_SECRET"),
            algorithms=[os.getenv("JWT_ALGORITHM")]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None