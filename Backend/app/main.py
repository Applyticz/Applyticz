from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db, engine, Base, db_dependency
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.routers import test_router, auth_router, resume_router, application_router, dashboard_router, user_settings_router
from app.models.database_models import Test, User
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import status
from app.routers.auth_router import get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs at startup
    Base.metadata.create_all(bind=engine)
    yield  # This allows the app to continue running
    # This runs on shutdown (if needed)
    # Add any cleanup code here if necessary

app = FastAPI(lifespan=lifespan)

# CORS Middleware configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]

# Include the test router, assuming it's defined in routers/test_router.py
app.include_router(test_router.router, prefix='/test')
app.include_router(auth_router.router, prefix='/auth')
app.include_router(resume_router.router, prefix='/resume')
app.include_router(application_router.router, prefix='/application')
app.include_router(dashboard_router.router, prefix='/dashboard')
app.include_router(user_settings_router.router, prefix="/settings", tags=["settings"])
# Example endpoint template
# @app.get('/test')
# def test_(dependencies):
    #     pass  # Placeholder for actual dependency injection logic
    #     return {"message": "Hello, World!"}
    
@app.get("/")
async def entry():
    return {"message": "Welcome to the backend!"}
