from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

class TestBase(BaseModel):
    username: str
    email: str
    password: str